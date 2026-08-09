<!-- Archived development evidence; not part of the public documentation path. -->

# M2 (Phase 2) — Design Spec

_Date: 2026-08-05_
_Status: Approved by user_

## Goal

Implement the M2 milestone from `roadmap.md`: preprocessing options, data suitability
check, raw data drill-down, HTML report generation, and UI language selection (i18n).
TASK-013 (packaging) is included as an M2 backlog item; TASK-011 (expert statistics,
requires a new SciPy dependency) is explicitly **out of scope** for this spec — it needs
its own separate dependency-approval gate per `dependencies.md`.

Builds directly on the M1 layered architecture (UI → Controller → Analysis Engine →
Report/Export) established in `memory/architecture.md`. All M1 architecture constraints
still apply: Analysis Engine has zero PySide6 dependency; no network calls; never write to
the user's original input file; never auto-select a column or auto-judge Benford
applicability; neutral/non-accusatory tone everywhere.

## Components

### 1. Preprocessing pipeline (TASK-007)

New module `src/benford_lens/analysis/preprocessing.py` (Analysis Engine layer, no UI
dependency):

- `PreprocessingOptions` dataclass:
  - `negative_handling: Literal["keep", "absolute", "exclude"]` — default `"absolute"`
  - `zero_handling: Literal["keep", "exclude"]` — default `"exclude"`
  - `decimal_handling: Literal["as_is", "round", "truncate"]` — default `"as_is"`
  - `blank_handling: Literal["exclude"]` — only sensible option for a blank/missing value;
    kept as a `Literal` (not a plain constant) so a future option can be added without an
    interface break
  - `duplicate_handling: Literal["keep", "exclude"]` — default `"keep"`
  - `string_to_number: bool` — default `True`; strips common currency/thousands
    formatting (e.g. `"1,200원"`, `"$100"` → `1200`, `100`) before numeric coercion
  - Defaults match the mockup-derived values in `tasks/backlog.md` TASK-014 detail.
- `PreprocessingPreview` dataclass: `total_before: int`, `total_after: int`,
  `excluded_negative: int`, `excluded_zero: int`, `excluded_blank: int`,
  `excluded_non_numeric: int`, `sample_before: list`, `sample_after: list` (first N values
  of each, for the UI's before/after preview — not the full series, to keep the preview
  panel light).
- `apply_preprocessing(raw_series: pd.Series, options: PreprocessingOptions) -> tuple[pd.Series, PreprocessingPreview]`.

`SessionController` changes:
- New `preprocessing_options: PreprocessingOptions` field on `SessionState` (default
  instance).
- `configure_preprocessing(options: PreprocessingOptions) -> PreprocessingPreview` — runs
  preprocessing on the currently selected column and returns the preview without mutating
  analysis state, so the UI can show before/after live as the user changes options.
- `analyze()` now applies `apply_preprocessing` to the selected column before calling
  `analyze_first_digit`, using `self.state.preprocessing_options`.

UI: new `PreprocessingPanel` (`src/benford_lens/ui/preprocessing_panel.py`), a `QWidget`
with one combo box per option, enabled once a column is selected, with a "Preview" button
that calls `configure_preprocessing` and renders the before/after counts and a couple of
sample rows in two small read-only tables.

### 2. Data suitability check (TASK-008)

New module `src/benford_lens/analysis/suitability.py`:

- `SuitabilityLevel` enum: `GOOD`, `CAUTION`, `DIFFICULT` (UI maps these to 🟢/🟡/🔴 —
  the enum itself carries no color/emoji, keeping the Analysis Engine presentation-free).
- `SuitabilityMetrics` dataclass: `sample_count`, `min_value`, `max_value`, `digit_range`
  (count of distinct order-of-magnitude buckets, i.e. `floor(log10(abs(x))) + 1` for
  nonzero finite values), `duplicate_rate`, `zero_rate`, `negative_rate`, `missing_rate`,
  `distinct_value_count`.
- `compute_suitability_metrics(preprocessed_series, raw_series) -> SuitabilityMetrics` —
  rates (zero/negative/missing/duplicate) are computed against the raw selected-column
  series (before preprocessing removes anything), so the check reflects the source data's
  actual characteristics; `sample_count`/`min`/`max`/`digit_range`/`distinct_value_count`
  are computed on the preprocessed series that will actually feed the analysis.
- `assess_suitability(metrics: SuitabilityMetrics) -> SuitabilityAssessment` where
  `SuitabilityAssessment` holds `level: SuitabilityLevel`, `metrics`, and
  `notes: list[str]` (neutral, non-prescriptive one-line observations — see thresholds
  below).

**Thresholds — recorded as ADR-006 in `memory/decisions.md`** (heuristic advisory
defaults, not a statistical test; never auto-confirms whether Benford's Law applies):

| Metric | 🔴 Difficult | 🟡 Caution | 🟢 Good |
|---|---|---|---|
| `sample_count` | < 30 | 30–299 | ≥ 300 |
| `digit_range` (orders of magnitude spanned) | ≤ 1 | 2–3 | ≥ 4 |
| distinct ratio (`distinct_value_count / sample_count`) | < 0.1 | 0.1–0.29 | ≥ 0.3 |

Plus 🟡-only advisory flags (never escalate to 🔴 alone): `zero_rate > 0.3`,
`negative_rate > 0.5`, `missing_rate > 0.3`. Overall level = the most severe of the three
primary rows; the 30-sample floor reuses the existing `_MIN_MEANINGFUL_SAMPLE` constant
from `charts/benford_chart.py` (moved to a shared location so both modules reference the
same value instead of duplicating the literal).

`SessionController.check_suitability() -> SuitabilityAssessment` — runs after
preprocessing, before analysis, per the data flow already documented in
`memory/architecture.md`.

UI: new `SuitabilityPanel` — colored badge + metrics table + a fixed caption: "These are
data characteristics, not a determination of whether Benford's Law applies — that
judgment is yours to make."

### 3. Raw data drill-down (TASK-009)

`SessionController.drill_down(digit: int) -> pd.DataFrame` — maps preprocessed values back
to their original row indices, filters to rows whose analyzed value's leading digit
matches, and returns the corresponding **original, unmodified** rows from
`state.dataframe` (never the preprocessed values) for user inspection.

UI: clicking a bar in the chart (`FigureCanvasQTAgg.mpl_connect("button_press_event", ...)`,
mapped to the nearest digit by x-coordinate) opens a drill-down panel: a `QTableWidget` of
the returned rows, a search `QLineEdit` that filters visible rows by substring match
across all columns, and an "Export CSV…" button (`QFileDialog.getSaveFileName` +
`DataFrame.to_csv`) — both additions called for in the TASK-014 mockup notes.

### 4. HTML report generation (TASK-010)

New module `src/benford_lens/report/html_report.py`:

- `render_html_report(context: ReportContext) -> str` using `string.Template` — a
  hand-written HTML page with inline CSS (no new dependency, per the earlier decision).
- `ReportContext` dataclass bundles: source filename, sheet/column analyzed,
  preprocessing options used + before/after counts, suitability assessment, the chart
  (re-rendered via Matplotlib to a PNG and embedded as a base64 data URI — Matplotlib is
  already a dependency), the result summary text, the digit-frequency table, a generation
  timestamp, and a fixed tone-compliant footer (local-only processing note + "not a
  determination of data manipulation" disclaimer, reusing `summarize_result`'s existing
  phrasing conventions).

UI: "Export Report…" button → `QFileDialog.getSaveFileName` (filter `HTML files (*.html)`)
→ write the rendered HTML to the user-chosen path. This is a local file the user
explicitly creates at a destination they pick — not writing to the source data file, and
not a network action.

### 5. UI language selection / i18n (TASK-015)

Per ADR-004/`tech-stack.md`: Qt's built-in `QTranslator` system, no new dependency.

- Wrap every user-facing string across `main_window.py` and the new panels/dialogs in
  `self.tr(...)`.
- `resources/i18n/benford_lens_{en,ko,zh,ja}.ts` source files, compiled to `.qm` via
  `pyside6-lrelease` (compiled `.qm` files are committed, since there's no separate build
  step in the packaging pipeline yet — `packaging/*.spec` bundles them as `datas`).
  English is the source language embedded directly in the code via `tr()`; the `en.ts`
  file exists for completeness/tooling symmetry but its compiled `.qm` is effectively a
  no-op identity translation.
- I will write the actual Korean/Chinese/Japanese translation text for every UI string —
  not placeholders.
- A `QComboBox` language selector in the main window's top bar (English / 한국어 / 中文 /
  日本語). On change: install the corresponding `QTranslator` on `QApplication`, then call
  `_retranslate_ui()` on `MainWindow` (and any currently-open panels) to refresh visible
  text immediately, via Qt's `changeEvent(QEvent.LanguageChange)` hook — no app restart
  required.
- Scope stays UI-layer only: the Analysis Engine (`analysis/`, `io/`) has no user-facing
  strings and remains language-agnostic, per the existing architecture constraint.

### 6. PyInstaller packaging (TASK-013)

New `packaging/` directory: `benford-lens-macos.spec`, `benford-lens-windows.spec`,
`benford-lens-linux.spec`, each targeting `src/benford_lens/__main__.py`, with
`hiddenimports` for `matplotlib.backends.backend_qtagg` and PySide6 plugins, and `datas`
bundling the compiled `.qm` translation files.

- macOS spec: built and smoke-tested locally in this session — `uv run pyinstaller
  packaging/benford-lens-macos.spec`, then launched headlessly
  (`QT_QPA_PLATFORM=offscreen`) to confirm the frozen binary starts and exits cleanly.
  This confirms the bundle is structurally sound but is **not** a full interactive GUI
  check (no display available in this environment) — logged as a known limitation
  alongside the Windows/Linux gap below.
- Windows/Linux specs: written but config-only and untested (this dev machine is macOS
  only) — logged in `memory/known-issues.md` as a known limitation pending a Windows/Linux
  build environment or CI coverage.

## Testing

Following M1's pattern (`tests/` mirrors `src/` structure):
- `tests/analysis/test_preprocessing.py`, `tests/analysis/test_suitability.py` — pure-Python
  unit tests, no Qt dependency, covering each handling option and each threshold boundary.
- `tests/ui/test_controller.py` extended for `configure_preprocessing`, `check_suitability`,
  `drill_down`.
- `tests/report/test_html_report.py` — asserts required content appears in rendered output
  and that tone rules hold (no accusatory wording).
- `tests/ui/test_main_window.py` extended for the drill-down click flow and language
  switching (asserting a widget's text actually changes after selecting a language).
- No automated test for the PyInstaller build itself (no CI runner change proposed here);
  the local macOS smoke test in this session is manual/one-off, matching the "config only"
  scope agreed for packaging.

## Out of scope

- TASK-011 (expert statistics: MAD, Chi-square, KS Test) — needs a new SciPy dependency,
  which is its own Human Approval Gate per `dependencies.md`. Not touched by this spec.
- Any MVP-excluded feature (cloud storage, accounts, AI-based fraud detection, PDF export,
  real-time collaboration) — unchanged, still excluded.
- Expanding language support beyond EN/KO/ZH/JA (M3 scope per ADR-004).
