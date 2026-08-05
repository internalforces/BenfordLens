<!--
Purpose:        Archive of completed tasks (accumulate; do not delete)
Owner:          Implementer / Planner
Update Trigger: Task completed
Harness Version: 1.1
-->

# Completed Tasks — Benford Lens

_Last updated: 2026-08-05_

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
| TASK-007 | Preprocessing options + before/after preview | 2026-08-05 | Implementer | `analysis/preprocessing.py`, `ui/preprocessing_panel.py` |
| TASK-008 | Data suitability check (🟢/🟡/🔴) | 2026-08-05 | Implementer | `analysis/suitability.py`, `ui/suitability_panel.py`; thresholds recorded as ADR-006 |
| TASK-009 | Raw data drill-down from chart digit click | 2026-08-05 | Implementer | `ui/drill_down_panel.py`; chart click wired via `mpl_connect` |
| TASK-010 | HTML report generation | 2026-08-05 | Implementer | `report/html_report.py`, stdlib `string.Template`, no new dependency |
| TASK-013 | PyInstaller packaging config for macOS/Windows/Linux | 2026-08-05 | Implementer | `packaging/*.spec`; macOS built + headless-smoke-tested locally; Windows/Linux config-only (TD-003) |
| TASK-014 | Review UI demo mockup and reconcile its design details | 2026-08-05 | Planner / Reviewer | Adopted preprocessing defaults, neutral result tone, drill-down search/export, hidden expert details, and EN/KO/ZH/JA language direction. A pre-selection per-column verdict was not adopted because column choice and applicability judgment remain user-owned; decorative/filter-shell ideas are deferred to later UI polish. See ADR-007. |
| TASK-015 | UI language selection & i18n scaffolding | 2026-08-05 | Implementer | `resources/i18n/*.ts/.qm`, `QTranslator`-based switching in `ui/main_window.py`; real KO/ZH/JA translations, not placeholders |
| TASK-016 | M2 merge-gate hardening, final review, and follow-up merge | 2026-08-05 | Implementer / Reviewer / Release Manager | Fixed ISS-001, synchronized README/version metadata, verified 152 tests and 91% coverage, received an Approved review verdict, and merged follow-up PR #3 after CI passed. |
