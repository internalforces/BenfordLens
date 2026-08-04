<!--
Purpose:        Prioritized list of tasks not yet started
Owner:          Planner
Update Trigger: New task added, priority changed, milestone adjusted
Harness Version: 1.1
-->

# Backlog — Benford Lens

_Last updated: 2026-08-04_

| ID | Task | Priority | Milestone | Size | Notes |
|----|------|----------|-----------|------|-------|
| TASK-001 | Initial project environment setup (`uv init`, project layout, ruff/mypy/pytest config) | High | M1 | S | — |
| TASK-002 | CSV file loader with automatic encoding detection | High | M1 | M | No auto column analysis |
| TASK-003 | Excel file loader with sheet selection | High | M1 | M | — |
| TASK-004 | Column selector UI (manual selection only) | High | M1 | S | Must not auto-pick or auto-analyze a column |
| TASK-005 | First-digit Benford calculation (Analysis Engine, UI-independent) | High | M1 | M | Core statistics; needs strong unit test coverage |
| TASK-006 | Expected vs. actual distribution chart (Matplotlib) | High | M1 | M | — |
| TASK-007 | Preprocessing options UI + pipeline (negative/zero/decimal/blank/duplicate/string-number) with before/after preview | High | M2 | L | — |
| TASK-008 | Data suitability check (🟢/🟡/🔴) | Medium | M2 | M | Must never auto-confirm applicability — advisory only |
| TASK-009 | Raw data drill-down from chart digit click | Medium | M2 | M | — |
| TASK-010 | HTML report generation | Medium | M2 | M | — |
| TASK-011 | Expert statistics panel (MAD, Chi-square, KS Test) — hidden by default | Low | M2 | S | — |
| TASK-012 | GitHub Actions CI: lint, type-check, test on PR | Medium | M1 | S | — |
| TASK-013 | PyInstaller packaging config for macOS/Windows/Linux | Medium | M2 | M | — |

## Size Reference

| Size | Estimated Effort |
|------|-----------------|
| XS | Under 1 hour |
| S | 1–4 hours |
| M | Half day to full day |
| L | 1–3 days |
| XL | 3+ days → must be decomposed |
