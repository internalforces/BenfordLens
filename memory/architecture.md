<!--
Purpose:        System design decisions and architecture structure
Owner:          Architect
Update Trigger: New component added, design decision changed, dependency structure changed
Harness Version: 1.1
-->

# Architecture — Benford Lens

_Last updated: 2026-08-04_

## System Overview

A local-first desktop system built to achieve: non-experts can easily analyze Benford's Law
on their own CSV/Excel data, entirely on their local machine, with no data leaving it.

**Pattern**: Layered desktop architecture (UI → Controller → Analysis Engine → Report/Export),
with the Analysis Engine kept framework-agnostic (plain Python + Pandas/NumPy/SciPy) so it can
be unit tested independently of the PySide6 UI.

## Component Structure

```
UI Layer (PySide6)
├── File Open (drag & drop / file picker; CSV encoding + Excel sheet auto-detection)
├── Sheet & Column Selector (user picks the column to analyze — never automatic)
├── Preprocessing Options Panel (negative / zero / decimal / blank / duplicate / string-number
│   handling, with a before → after preview)
├── Suitability Check Panel (🟢/🟡/🔴 result + underlying metrics)
├── Analysis Results View
│   ├── Chart (expected vs. actual distribution)
│   ├── Result summary (plain-language explanation)
│   ├── Expert statistics (hidden by default — MAD, Chi-square, KS Test, sample size, deviation)
│   └── Raw data explorer (click a digit → filtered original rows)
└── Report Export (HTML)

Application / Controller Layer
└── Orchestrates the flow above; holds in-memory session state (selected file, sheet, column,
    preprocessing choices, analysis results, selected UI language)

Internationalization (UI Layer only)
└── Language selector (default English; Korean/Chinese/Japanese through M2 — see ADR-004) via
    Qt's QTranslator; the Analysis Engine remains language-agnostic

Analysis Engine (Pandas / NumPy / SciPy — no UI dependency)
├── File loaders (CSV, XLSX)
├── Preprocessing pipeline
├── Suitability checker
├── Benford digit-frequency calculator (first digit MVP; second digit / combined later)
└── Statistical tests (MAD, Chi-square, KS Test)

Report Generator
└── Assembles the HTML report (analysis target, preprocessing options, suitability result,
    charts, statistics, plain-language explanation, caveats)

Packaging
└── PyInstaller → standalone executable, no separate runtime install required
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
| UI language defaults & i18n scope | English default; KO/ZH/JA selectable by M2 (ADR-004) | 2026-08-04 |

## Architecture Constraints

- Analysis Engine must have zero dependency on PySide6, so it can be tested and reasoned about independently of the UI
- No component may open a network socket or make an HTTP request
- No component may write to the user's original input file
