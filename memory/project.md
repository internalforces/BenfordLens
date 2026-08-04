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
- **Phase**: Initial setup — no code written yet, Harness just established
- **Next milestone**: M1 — MVP (CSV/Excel reading, column selection, first-digit analysis, chart output)
- **Overall health**: 🟢 Good

## Tech Summary

| Field | Value |
|-------|-------|
| Language | Python |
| Framework | PySide6 (UI); Pandas/NumPy/SciPy (analysis); Matplotlib (charts) |
| Infrastructure | None — local desktop app, packaged via PyInstaller |
| Repo Structure | Single Repo |

## Key Paths

```
BenfordLens/
├── src/                      (not yet created — planned application source)
├── tests/                    (not yet created — planned test suite)
└── benford-lens-harness/     ← this AI Development Harness
```

## Recent Changes

| Date | Change |
|------|--------|
| 2026-08-04 | AI Development Harness v1.1 initial setup (Standard tier), generated from the PRD |

## Constraints

- 100% local processing — no internet connection required, no data upload, no login/accounts, no AI/API server calls
- User must explicitly choose which column to analyze — no auto-analysis
- All major preprocessing choices (negative handling, zero handling, decimal handling, blanks, duplicates, string-to-number parsing) are user-selectable, with a before/after preview
- Neutral, non-accusatory language only — never "manipulated" or "fraud"; the program never auto-confirms whether Benford's Law applies to a dataset
- MVP excludes: cloud storage, accounts/login, AI-based fraud detection, online upload, direct PDF export, real-time collaboration
