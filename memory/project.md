<!--
Purpose:        Current project state snapshot — the first context file every agent reads
Owner:          All agents (read), Planner / Release Manager (write)
Update Trigger: Version change, milestone completed, major status shift
Harness Version: 1.1
-->

# Project: Benford Lens

_Last updated: 2026-08-07_

## Summary

An open-source desktop application that lets non-experts easily analyze Benford's Law on
their own CSV/Excel data, entirely on their local machine, with no data ever sent to an
external server.

## Current State

- **Version**: v0.2.0.dev0
- **Phase**: M3 merged to `main` through PR #6; TASK-027 responsive desktop layout follow-up
  complete
- **Next milestone**: Synchronize v1.0 release metadata after the TASK-027 delivery gate
- **Overall health**: 🟢 Good

## Tech Summary

| Field | Value |
|-------|-------|
| Language | Python 3.11 (pinned via `.python-version`) |
| Framework | PySide6 (UI); Pandas/NumPy/SciPy (analysis); Matplotlib (charts) |
| Infrastructure | None — local desktop app, packaged via PyInstaller (`packaging/*.spec`; macOS built + headless-smoke-tested, Windows/Linux config-only per TD-003) |
| Repo Structure | Single Repo |

## Key Paths

```
BenfordLens/
├── src/benford_lens/
│   ├── io/                   (csv_loader.py, excel_loader.py)
│   ├── analysis/              (benford.py — first/second/combined calculation;
│   │                            preprocessing.py; suitability.py; expert_statistics.py — all
│   │                            zero UI dependency)
│   ├── charts/                (benford_chart.py — chart + result summary)
│   ├── report/                 (html_report.py — stdlib string.Template, no new dependency)
│   └── ui/                    (controller.py — framework-agnostic session state;
│                                main_window.py — PySide6 MainWindow; preprocessing_panel.py;
│                                suitability_panel.py; digit_result_panel.py;
│                                expert_statistics_panel.py; drill_down_panel.py;
│                                __main__.py entry point)
├── resources/i18n/           (benford_lens_{ko,zh,ja,es,fr,ru}.ts/.qm — QTranslator translations)
├── packaging/                 (benford-lens-{macos,windows,linux}.spec — PyInstaller)
├── tests/                    (mirrors src/ layout; tests/conftest.py sets QT_QPA_PLATFORM=offscreen)
├── .github/workflows/ci.yml  (lint, format-check, type-check, test on push/PR to main)
└── docs/superpowers/plans/    (M1, M2, and 2026-08-06-m3-v1.md implementation plans)
```

## Recent Changes

| Date | Change |
|------|--------|
| 2026-08-04 | AI Development Harness v1.1 initial setup (Standard tier), generated from the PRD |
| 2026-08-04 | UI mockup reviewed (TASK-014); ADR-004 decided: expert stats stay hidden by default, default UI language is English with Korean/Chinese/Japanese selectable by M2 (TASK-015) |
| 2026-08-04 | M1 (MVP) implemented on `feature/m1-mvp` via subagent-driven-development: TASK-001–006, TASK-012 done. Dev environment pinned to Python 3.11 (`.python-version`) after a numpy/mypy stub incompatibility surfaced mid-implementation — see `memory/decisions.md` ADR-005 and `memory/known-issues.md` |
| 2026-08-05 | M2 (Phase 2) implemented: preprocessing, suitability check, drill-down, HTML report, i18n (real KO/ZH/JA translations), PyInstaller packaging specs |
| 2026-08-05 | M2 PR #2 merged to `main`; follow-up review fixed report-source state handling, synchronized README/version metadata, and verified 91% line coverage |
| 2026-08-05 | M2 merge-gate follow-up PR #3 passed CI and merged to `main`; TASK-016 complete |
| 2026-08-05 | TASK-011 implemented approved SciPy-backed MAD, Chi-square, and KS reference statistics in a hidden-by-default expert details panel |
| 2026-08-06 | TASK-011 PR #4 passed CI, merged to `main`, and passed post-merge review (162 tests) |
| 2026-08-06 | M3 combined analysis defined as first- and second-digit results displayed together in one view; compatibility-first architecture accepted as ADR-009 |
| 2026-08-06 | M3 TASK-018–024 implemented on `codex/m3-core`: neutral copy cleanup, second/combined analysis, generic statistics, immutable snapshots, reusable UI, mode-aware reports, complete EN/KO/ZH/JA additions, and 30.0–31.8% faster 100k-row analysis |
| 2026-08-06 | TASK-025 added complete 93-message Spanish and French UI catalogs with compiled `.qm` files and catalog completeness tests; M3 feature scope complete |
| 2026-08-06 | TASK-026 added a complete 93-message Russian UI catalog, compiled resource, selector entry, and state-preserving UI coverage to M3 PR #6 |
| 2026-08-07 | TASK-027 resolved the clipped M3 desktop UI with a scroll-bounded workflow, responsive combined charts, readable chart minimums, automatic result reveal, and geometry regression coverage; all 232 tests pass |

## Constraints

- 100% local processing — no internet connection required, no data upload, no login/accounts, no AI/API server calls
- User must explicitly choose which column to analyze — no auto-analysis
- All major preprocessing choices (negative handling, zero handling, decimal handling, blanks, duplicates, string-to-number parsing) are user-selectable, with a before/after preview
- Neutral, non-accusatory language only — never "manipulated" or "fraud"; the program never auto-confirms whether Benford's Law applies to a dataset
- MVP excludes: cloud storage, accounts/login, AI-based fraud detection, online upload, direct PDF export, real-time collaboration
