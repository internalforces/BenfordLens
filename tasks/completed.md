<!--
Purpose:        Archive of completed tasks (accumulate; do not delete)
Owner:          Implementer / Planner
Update Trigger: Task completed
Harness Version: 1.1
-->

# Completed Tasks — Benford Lens

_Last updated: 2026-08-04_

| ID | Task | Completed | Owner | Notes |
|----|------|-----------|-------|-------|
| — | AI Development Harness v1.1 initial setup | 2026-08-04 | — | Generated from PRD, Standard tier |
| TASK-001 | Initial project environment setup (uv, project layout, ruff/mypy/pytest config) | 2026-08-04 | Implementer | `feature/m1-mvp` branch, subagent-driven-development. Pinned dev interpreter to Python 3.11 via `.python-version` (added mid-M1, see TASK-005 note) |
| TASK-002 | CSV file loader with automatic encoding detection | 2026-08-04 | Implementer | `src/benford_lens/io/csv_loader.py`. Fixed try-in-order encoding fallback (no new dependency) — known limitation logged as TD-001 in `memory/known-issues.md` |
| TASK-003 | Excel file loader with sheet selection | 2026-08-04 | Implementer | `src/benford_lens/io/excel_loader.py`. Sheet selection always explicit, never auto-picked by this module |
| TASK-004 | Column selector UI (manual selection only) | 2026-08-04 | Implementer | `src/benford_lens/ui/controller.py` (SessionController.select_column) + `src/benford_lens/ui/main_window.py` (QTableWidget, SelectRows behavior). Column selection is 100% user-click-driven; a review round caught and fixed a missing `setSelectionBehavior` that silently broke real mouse clicks — see `docs/superpowers/plans/2026-08-04-m1-mvp.md` Task 7 fix round 1 |
| TASK-005 | First-digit Benford calculation (Analysis Engine, UI-independent) | 2026-08-04 | Implementer | `src/benford_lens/analysis/benford.py`, zero PySide6 dependency. Mid-task, resolving a real `mypy`/numpy stub incompatibility required pinning the dev environment to Python 3.11 (`.python-version`) — logged as the resolution path, not a scope change |
| TASK-006 | Expected vs. actual distribution chart (Matplotlib) | 2026-08-04 | Implementer | `src/benford_lens/charts/benford_chart.py` (`build_first_digit_figure`, `summarize_result`). Result-summary text uses the TASK-014-approved tone-compliant phrasing verbatim |
| TASK-012 | GitHub Actions CI: lint, type-check, test on PR | 2026-08-04 | Implementer | `.github/workflows/ci.yml`, `ubuntu-latest`, Python 3.11, ruff/mypy/pytest. Format-check scoped to `src/ tests/` (excludes the plan doc under `docs/`) |
