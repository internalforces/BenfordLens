<!--
Purpose:        Current project state snapshot — the first context file every agent reads
Owner:          All agents (read), Planner / Release Manager (write)
Update Trigger: Version change, milestone completed, major status shift
Harness Version: 1.1
-->

# Project: Benford Lens

_Last updated: 2026-08-05_

## Summary

An open-source desktop application that lets non-experts easily analyze Benford's Law on
their own CSV/Excel data, entirely on their local machine, with no data ever sent to an
external server.

## Current State

- **Version**: v0.2.0.dev0
- **Phase**: M2 (Phase 2) complete on `main` via PR #2 and merge-gate follow-up PR #3
- **Next milestone**: M3 — v1.0 (second-digit analysis, combined analysis, performance, expanded i18n)
- **Overall health**: 🟢 Good

## Tech Summary

| Field | Value |
|-------|-------|
| Language | Python 3.11 (pinned via `.python-version`) |
| Framework | PySide6 (UI); Pandas/NumPy (analysis); Matplotlib (charts) — SciPy still not added, deferred to TASK-011's expert statistics panel, blocked on its own dependency approval |
| Infrastructure | None — local desktop app, packaged via PyInstaller (`packaging/*.spec`; macOS built + headless-smoke-tested, Windows/Linux config-only per TD-003) |
| Repo Structure | Single Repo |

## Key Paths

```
BenfordLens/
├── src/benford_lens/
│   ├── io/                   (csv_loader.py, excel_loader.py)
│   ├── analysis/              (benford.py — first-digit calculation; preprocessing.py;
│   │                            suitability.py — all zero UI dependency)
│   ├── charts/                (benford_chart.py — chart + result summary)
│   ├── report/                 (html_report.py — stdlib string.Template, no new dependency)
│   └── ui/                    (controller.py — framework-agnostic session state;
│                                main_window.py — PySide6 MainWindow; preprocessing_panel.py;
│                                suitability_panel.py; drill_down_panel.py; __main__.py entry point)
├── resources/i18n/           (benford_lens_{ko,zh,ja}.ts/.qm — QTranslator translations)
├── packaging/                 (benford-lens-{macos,windows,linux}.spec — PyInstaller)
├── tests/                    (mirrors src/ layout; tests/conftest.py sets QT_QPA_PLATFORM=offscreen)
├── .github/workflows/ci.yml  (lint, format-check, type-check, test on push/PR to main)
└── docs/superpowers/plans/    (2026-08-04-m1-mvp.md, 2026-08-05-m2-phase2.md — subagent-driven-development plans)
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

## Constraints

- 100% local processing — no internet connection required, no data upload, no login/accounts, no AI/API server calls
- User must explicitly choose which column to analyze — no auto-analysis
- All major preprocessing choices (negative handling, zero handling, decimal handling, blanks, duplicates, string-to-number parsing) are user-selectable, with a before/after preview
- Neutral, non-accusatory language only — never "manipulated" or "fraud"; the program never auto-confirms whether Benford's Law applies to a dataset
- MVP excludes: cloud storage, accounts/login, AI-based fraud detection, online upload, direct PDF export, real-time collaboration
