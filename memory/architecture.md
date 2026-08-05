<!--
Purpose:        System design decisions and architecture structure
Owner:          Architect
Update Trigger: New component added, design decision changed, dependency structure changed
Harness Version: 1.1
-->

# Architecture — Benford Lens

_Last updated: 2026-08-05_

## System Overview

A local-first desktop system built to achieve: non-experts can easily analyze Benford's Law
on their own CSV/Excel data, entirely on their local machine, with no data leaving it.

**Pattern**: Layered desktop architecture (UI → Controller → Analysis Engine → Report/Export),
with the Analysis Engine kept framework-agnostic (plain Python + Pandas/NumPy; SciPy anticipated
for TASK-011's expert statistics, pending its own dependency approval — not yet added) so it can
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
│   ├── Chart (expected vs. actual distribution)
│   ├── Result summary (plain-language explanation)
│   ├── Expert statistics (hidden by default — MAD, Chi-square, KS Test, sample size, deviation;
│   │   still pending — see TASK-011 in tasks/backlog.md, blocked on its own SciPy dependency
│   │   approval)
│   └── Raw data explorer — implemented M2: src/benford_lens/ui/drill_down_panel.py (click a
│       digit on the chart → filtered original rows, wired via `mpl_connect`)
└── Report Export (HTML) — implemented M2

Application / Controller Layer
└── Orchestrates the flow above; holds in-memory session state (selected file, sheet, column,
    preprocessing choices, analysis results, selected UI language)

Internationalization (UI Layer only) — implemented M2
└── Language selector (default English; Korean/Chinese/Japanese — see ADR-004) via Qt's
    QTranslator, real (not placeholder) KO/ZH/JA translations under resources/i18n/; the
    Analysis Engine remains language-agnostic

Analysis Engine (Pandas / NumPy — no UI dependency; SciPy not added — still pending TASK-011's
own dependency approval, out of scope for this M2 plan)
├── File loaders (CSV, XLSX) — implemented M1: src/benford_lens/io/
├── Preprocessing pipeline — implemented M2: src/benford_lens/analysis/preprocessing.py
├── Suitability checker — implemented M2: src/benford_lens/analysis/suitability.py
├── Benford digit-frequency calculator (first digit — implemented M1: src/benford_lens/analysis/;
│   second digit / combined — M3)
└── Statistical tests (MAD, Chi-square, KS Test) — still pending TASK-011, requires SciPy (human
    approval needed for the new dependency per dependencies.md)

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
  → Benford analysis (digit-frequency calculation + statistical tests)
  → Chart + plain-language explanation
  → optional: drill-down to filtered raw rows
  → optional: HTML report export (explicit user action, local file write only)
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

## Architecture Constraints

- Analysis Engine must have zero dependency on PySide6, so it can be tested and reasoned about independently of the UI
- No component may open a network socket or make an HTTP request
- No component may write to the user's original input file
