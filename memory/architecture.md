<!--
Purpose:        System design decisions and architecture structure
Owner:          Architect
Update Trigger: New component added, design decision changed, dependency structure changed
Harness Version: 1.1
-->

# Architecture — Benford Lens

_Last updated: 2026-08-10_

## System Overview

A local-first desktop system built to achieve: non-experts can easily analyze Benford's Law
on their own CSV/Excel data, entirely on their local machine, with no data leaving it.

**Pattern**: Layered desktop architecture (UI → Controller → Analysis Engine → Report/Export),
with the Analysis Engine kept framework-agnostic (plain Python + Pandas/NumPy/SciPy) so it can
be unit tested independently of the PySide6 UI.

## Component Structure

```
UI Layer (PySide6)
├── Bounded workflow viewport — implemented TASK-027/032: the translation-safe two-row toolbar
│   remains fixed without increasing the requested window width, while the
│   vertically growing workflow scrolls within the requested window size; chart canvases leave
│   wheel input to this enclosing viewport so scrolling continues under the pointer (TASK-031)
├── File Open (file picker; CSV encoding auto-detected via fixed fallback list — see TD-001 in
│   memory/known-issues.md; Excel sheet is always an explicit user choice, never auto-picked)
├── Sheet & Column Selector (user picks the sheet and the column to analyze — never automatic)
├── Preprocessing Options Panel — implemented M2: src/benford_lens/ui/preprocessing_panel.py
│   (negative / zero / decimal / blank / duplicate / string-number handling, with a before →
│   after preview)
├── Suitability Check Panel — implemented M2: src/benford_lens/ui/suitability_panel.py
│   (🟢/🟡/🔴 result + underlying metrics)
├── Analysis Results View
│   ├── Analysis mode selector — implemented M3 (first digit / second digit / first + second;
│   │   always user-triggered)
│   ├── Reusable digit-result panel (position title, chart, summary, click signal)
│   │   └── Combined mode keeps both panels in one view: stacked at compact widths and side by
│   │       side when the result viewport is at least 1100 px wide (TASK-027 / ADR-012)
│   ├── Expert statistics — implemented by TASK-011: hidden by default in
│   │   src/benford_lens/ui/expert_statistics_panel.py; M3 separates per-position MAD and
│   │   Chi-square from the shared log-mantissa KS result — implemented TASK-022
│   └── Raw data explorer — implemented M2: src/benford_lens/ui/drill_down_panel.py (click a
│       digit on a chart → filtered original rows; M3 click events include digit position —
│       implemented TASK-021/022)
└── Report Export (HTML) — implemented M2

Application / Controller Layer
└── Orchestrates the flow above; holds in-memory session state (selected file, sheet, column,
    preprocessing choices, analysis results, selected UI language)

Internationalization (UI Layer only) — implemented M2, expanded M3
└── Language selector (default English; Korean/Chinese/Japanese from ADR-004 plus
    Spanish/French from ADR-010 and Russian from ADR-011) via Qt's QTranslator; real, complete
    translations live under resources/i18n/ and the Analysis Engine remains language-agnostic.
    Matplotlib chart labels and legends select installed fonts by CJK script. Qt language
    switching likewise applies locale-specific application-font fallbacks, and language-selector
    entries use their own script fonts. Both paths include Windows system-font candidates while
    retaining macOS/Linux fallbacks (TASK-030).

Analysis Engine (Pandas / NumPy / SciPy — no UI dependency)
├── File loaders (CSV, XLSX) — implemented M1: src/benford_lens/io/
├── Preprocessing pipeline — implemented M2: src/benford_lens/analysis/preprocessing.py
├── Suitability checker — implemented M2: src/benford_lens/analysis/suitability.py
├── Benford digit-frequency calculator (first digit — implemented M1; second digit and a
│   compatibility-preserving combined result — implemented M3 TASK-019/024)
└── Statistical tests (MAD, Chi-square, KS Test) — implemented by TASK-011 in
    src/benford_lens/analysis/expert_statistics.py; SciPy approved by the user on 2026-08-05

Report Generator — implemented M2, mode-aware M3: src/benford_lens/report/html_report.py
└── Assembles first-, second-, or combined-mode HTML reports from one immutable snapshot using
    stdlib `string.Template` only — no new dependency

Packaging — implemented M2: packaging/*.spec (PyInstaller)
└── Standalone executable, no separate runtime install required. macOS uses the approved
    concept A icon from resources/icons/macos/ (TASK-033 / ADR-014), and has been built and
    headless-smoke-tested locally. Windows derives a multi-resolution ICO from the same image,
    embeds it in the x64 executable, and has passed native folder and extracted-ZIP startup
    smoke tests (TASK-034 / ADR-015). A WiX 5.0.2 project wraps that one-folder output in a
    per-user MSI under LocalAppData, with a Start menu shortcut, standard major upgrades, and
    uninstall behavior; its metadata, 1,194 packaged files, non-elevated install, startup, and
    complete removal are verified by `packaging/build-windows-msi.ps1` (TASK-035 / ADR-016).
    Exact version tags rebuild the Windows ZIP/MSI and macOS arm64 ZIP on native GitHub runners,
    verify their lifecycle behavior, generate SHA-256 files, upload them to a draft Release, and
    make it public only after every platform succeeds (ADR-018). The first public run produced
    v1.0.0; release CLI calls now carry explicit repository context, and Windows checksum files use
    LF endings for portable verification. Linux remains config-only and untested (TD-003).
```

## Data Flow

```
File (CSV/XLSX)
  → Sheet selection (user)
  → Column selection (user)
  → Preprocessing (user-configured, previewed before applying)
  → Preprocessed data (in-memory only — never written back to the source file)
  → Suitability check
  → Explicit analysis mode (first / second / first + second)
  → One analysis snapshot (digit-frequency results + statistical tests)
  → One result panel, or two simultaneously visible panels for combined mode
  → optional: position-aware drill-down to filtered raw rows
  → optional: mode-aware HTML report export (explicit user action, local file write only)
```

No step in this pipeline makes a network call. Nothing is transmitted off the local machine
at any point.

## Design Decision Summary

> See memory/decisions.md for full details

| Decision | Choice | Date |
|----------|--------|------|
| Harness adoption | AI Development Harness v1.1, Standard tier | 2026-08-04 |
| Package manager | `uv` (ADR-002) | 2026-08-04 |
| CI/CD | GitHub Actions (ADR-003) | 2026-08-04 |
| UI language defaults & i18n scope | English default; KO/ZH/JA selectable by M2 (ADR-004) | 2026-08-04 |
| M3 language expansion | Spanish and French added as selectable UI languages (ADR-010) | 2026-08-06 |
| M3 Russian expansion | Russian added as a selectable UI language (ADR-011) | 2026-08-06 |
| Dev environment Python version | Pinned to 3.11 via `.python-version`, matching `requires-python` and CI (ADR-005) | 2026-08-04 |
| Data suitability thresholds | Heuristic defaults per ADR-006 | 2026-08-05 |
| Expert-statistics methodology | MAD/Chi-square on first digits; KS on log mantissas; no automated verdict (ADR-008) | 2026-08-05 |
| M3 analysis modes | Combined means independent first- and second-digit results shown together; shared generic internals with public compatibility wrappers (ADR-009) | 2026-08-06 |
| Responsive desktop layout | Bounded vertical scrolling; combined charts stack below 1100 px and sit side by side on wide viewports (ADR-012) | 2026-08-07 |
| macOS bundle metadata | Numeric app-bundle version derives from the package version; public builds require Developer ID signing and notarization (ADR-013) | 2026-08-07 |
| Application icon | Concept A (lens + descending distribution) is applied to macOS first; Windows/Linux remain unchanged (ADR-014) | 2026-08-07 |
| Windows installer | WiX 5.0.2 per-user MSI wrapping the PyInstaller one-folder build (ADR-016) | 2026-08-08 |
| Portfolio documentation | Korean/English landing pages and four bilingual public guides; internal evidence preserved separately (ADR-017) | 2026-08-09 |
| Public distribution | Native tag builds publish verified unsigned Windows ZIP/MSI and macOS arm64 ZIP assets with checksums and explicit trust warnings (ADR-018) | 2026-08-10 |

## Architecture Constraints

- Analysis Engine must have zero dependency on PySide6, so it can be tested and reasoned about independently of the UI
- No component may open a network socket or make an HTTP request
- No component may write to the user's original input file

## M3 Extension Boundary

Status: implemented on `codex/m3-core` by TASK-019–024; retained here as the compatibility and
review boundary for the merge gate.

M3 must generalize the fixed first-digit behavior without copying the current pipeline. The
accepted design is detailed in
`reports/development/specs/2026-08-06-m3-analysis-modes-design.md`:

- keep the existing first-digit public functions unchanged;
- add second-digit and combined entry points;
- preprocess once and snapshot all derived results together;
- reuse one digit-result panel once or twice depending on the selected mode;
- pass digit position through chart clicks and drill-down;
- render one shared KS result alongside per-position MAD/Chi-square values;
- make HTML reports mode-aware from the same immutable snapshot.

## Documentation Topology

- Public entry points: `README.md` (English) and `README.ko.md` (Korean).
- Public detail path: `docs/portfolio-case-study.md`, `docs/architecture.md`,
  `docs/verification.md`, and `docs/user-guide.md`, plus synthetic assets under `docs/assets/`.
- Internal evidence: `memory/`, `tasks/`, and `reports/`. Historical implementation plans and
  design specs are archived under `reports/development/` rather than exposed in `docs/`.
- Reproducibility: `scripts/generate_portfolio_assets.py` drives the real application with
  deterministic synthetic data and regenerates the public PNG/GIF assets without user data.
