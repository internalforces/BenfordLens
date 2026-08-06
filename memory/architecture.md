<!--
Purpose:        System design decisions and architecture structure
Owner:          Architect
Update Trigger: New component added, design decision changed, dependency structure changed
Harness Version: 1.1
-->

# Architecture — Benford Lens

_Last updated: 2026-08-06_

## System Overview

A local-first desktop system built to achieve: non-experts can easily analyze Benford's Law
on their own CSV/Excel data, entirely on their local machine, with no data leaving it.

**Pattern**: Layered desktop architecture (UI → Controller → Analysis Engine → Report/Export),
with the Analysis Engine kept framework-agnostic (plain Python + Pandas/NumPy/SciPy) so it can
be unit tested independently of the PySide6 UI.

## Component Structure

```
UI Layer (PySide6)
├── File Open (file picker; CSV encoding auto-detected via fixed fallback list — see TD-001 in
│   memory/known-issues.md; Excel sheet is always an explicit user choice, never auto-picked)
├── Sheet & Column Selector (user picks the sheet and the column to analyze — never automatic)
├── Preprocessing Options Panel — implemented M2: src/benford_lens/ui/preprocessing_panel.py
│   (negative / zero / decimal / blank / duplicate / string-number handling, with a before →
│   after preview)
├── Suitability Check Panel — implemented M2: src/benford_lens/ui/suitability_panel.py
│   (🟢/🟡/🔴 result + underlying metrics)
├── Analysis Results View
│   ├── M3 mode selector (first digit / second digit / first + second; always user-triggered)
│   ├── Reusable digit-result panel (position title, chart, summary, click signal)
│   │   └── Combined mode places first and second panels side by side in the same view
│   ├── Expert statistics — implemented by TASK-011: hidden by default in
│   │   src/benford_lens/ui/expert_statistics_panel.py; M3 separates per-position MAD and
│   │   Chi-square from the shared log-mantissa KS result
│   └── Raw data explorer — implemented M2: src/benford_lens/ui/drill_down_panel.py (click a
│       digit on a chart → filtered original rows; M3 click events include digit position)
└── Report Export (HTML) — implemented M2

Application / Controller Layer
└── Orchestrates the flow above; holds in-memory session state (selected file, sheet, column,
    preprocessing choices, analysis results, selected UI language)

Internationalization (UI Layer only) — implemented M2
└── Language selector (default English; Korean/Chinese/Japanese — see ADR-004) via Qt's
    QTranslator, real (not placeholder) KO/ZH/JA translations under resources/i18n/; the
    Analysis Engine remains language-agnostic

Analysis Engine (Pandas / NumPy / SciPy — no UI dependency)
├── File loaders (CSV, XLSX) — implemented M1: src/benford_lens/io/
├── Preprocessing pipeline — implemented M2: src/benford_lens/analysis/preprocessing.py
├── Suitability checker — implemented M2: src/benford_lens/analysis/suitability.py
├── Benford digit-frequency calculator (first digit — implemented M1; M3 adds second digit
│   and a compatibility-preserving combined result calculated from one preprocessing pass)
└── Statistical tests (MAD, Chi-square, KS Test) — implemented by TASK-011 in
    src/benford_lens/analysis/expert_statistics.py; SciPy approved by the user on 2026-08-05

Report Generator — implemented M2: src/benford_lens/report/html_report.py
└── Assembles the HTML report (analysis target, preprocessing options, suitability result,
    chart, first-digit distribution table, plain-language explanation, caveats) using stdlib
    `string.Template` only — no new dependency

Packaging — implemented M2: packaging/*.spec (PyInstaller)
└── Standalone executable, no separate runtime install required. macOS built and
    headless-smoke-tested locally; Windows/Linux specs are config-only, untested (TD-003 in
    memory/known-issues.md)
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
| Dev environment Python version | Pinned to 3.11 via `.python-version`, matching `requires-python` and CI (ADR-005) | 2026-08-04 |
| Data suitability thresholds | Heuristic defaults per ADR-006 | 2026-08-05 |
| Expert-statistics methodology | MAD/Chi-square on first digits; KS on log mantissas; no automated verdict (ADR-008) | 2026-08-05 |
| M3 analysis modes | Combined means independent first- and second-digit results shown together; shared generic internals with public compatibility wrappers (ADR-009) | 2026-08-06 |

## Architecture Constraints

- Analysis Engine must have zero dependency on PySide6, so it can be tested and reasoned about independently of the UI
- No component may open a network socket or make an HTTP request
- No component may write to the user's original input file

## M3 Extension Boundary

M3 must generalize the fixed first-digit behavior without copying the current pipeline. The
accepted design is detailed in
`docs/superpowers/specs/2026-08-06-m3-analysis-modes-design.md`:

- keep the existing first-digit public functions unchanged;
- add second-digit and combined entry points;
- preprocess once and snapshot all derived results together;
- reuse one digit-result panel once or twice depending on the selected mode;
- pass digit position through chart clicks and drill-down;
- render one shared KS result alongside per-position MAD/Chi-square values;
- make HTML reports mode-aware from the same immutable snapshot.
