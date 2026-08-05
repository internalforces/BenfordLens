<!--
Purpose:        Current project state snapshot — the first context file every agent reads
Owner:          All agents (read), Planner / Release Manager (write)
Update Trigger: Version change, milestone completed, major status shift
Harness Version: 1.1
-->

# Project: Benford Lens

_Last updated: 2026-08-04_

## Summary

An open-source desktop application that lets non-experts easily analyze Benford's Law on
their own CSV/Excel data, entirely on their local machine, with no data ever sent to an
external server.

## Current State

- **Version**: v0.1.0-dev
- **Phase**: M1 (MVP) implemented on `feature/m1-mvp`, pending final whole-branch review and human approval before merge to `main`
- **Next milestone**: M1 sign-off and merge, then M2 (preprocessing, suitability check, drill-down, HTML report, i18n)
- **Overall health**: 🟢 Good

## Tech Summary

| Field | Value |
|-------|-------|
| Language | Python 3.11 (pinned via `.python-version`) |
| Framework | PySide6 (UI); Pandas/NumPy (analysis); Matplotlib (charts) — SciPy not yet added, deferred to M2's expert statistics panel (TASK-011) |
| Infrastructure | None — local desktop app, packaged via PyInstaller (packaging itself is M2, TASK-013) |
| Repo Structure | Single Repo |

## Key Paths

```
BenfordLens/
├── src/benford_lens/
│   ├── io/                   (csv_loader.py, excel_loader.py)
│   ├── analysis/              (benford.py — first-digit calculation, zero UI dependency)
│   ├── charts/                (benford_chart.py — chart + result summary)
│   └── ui/                    (controller.py — framework-agnostic session state;
│                                main_window.py — PySide6 MainWindow; __main__.py entry point)
├── tests/                    (mirrors src/ layout; tests/conftest.py sets QT_QPA_PLATFORM=offscreen)
├── .github/workflows/ci.yml  (lint, format-check, type-check, test on push/PR to main)
└── docs/superpowers/plans/2026-08-04-m1-mvp.md   ← M1 implementation plan (subagent-driven-development)
```

## Recent Changes

| Date | Change |
|------|--------|
| 2026-08-04 | AI Development Harness v1.1 initial setup (Standard tier), generated from the PRD |
| 2026-08-04 | UI mockup reviewed (TASK-014); ADR-004 decided: expert stats stay hidden by default, default UI language is English with Korean/Chinese/Japanese selectable by M2 (TASK-015) |
| 2026-08-04 | M1 (MVP) implemented on `feature/m1-mvp` via subagent-driven-development: TASK-001–006, TASK-012 done. Dev environment pinned to Python 3.11 (`.python-version`) after a numpy/mypy stub incompatibility surfaced mid-implementation — see `memory/decisions.md` ADR-005 and `memory/known-issues.md` |

## Constraints

- 100% local processing — no internet connection required, no data upload, no login/accounts, no AI/API server calls
- User must explicitly choose which column to analyze — no auto-analysis
- All major preprocessing choices (negative handling, zero handling, decimal handling, blanks, duplicates, string-to-number parsing) are user-selectable, with a before/after preview
- Neutral, non-accusatory language only — never "manipulated" or "fraud"; the program never auto-confirms whether Benford's Law applies to a dataset
- MVP excludes: cloud storage, accounts/login, AI-based fraud detection, online upload, direct PDF export, real-time collaboration
