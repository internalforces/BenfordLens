<!--
Purpose:        Technology decisions and rationale
Owner:          Architect
Update Trigger: New technology adopted, existing technology replaced
Harness Version: 1.1
-->

# tech-stack.md — Benford Lens Technology Stack

_Last updated: 2026-08-04_

## Stack Overview

| Layer | Technology | Version | Rationale |
|-------|-----------|---------|-----------|
| Language | Python | 3.11+ | Strong data-analysis ecosystem (Pandas/NumPy/SciPy), good desktop packaging story via PyInstaller |
| UI Framework | PySide6 | Latest stable | Official Qt for Python bindings, LGPL-licensed (open-source friendly), mature desktop widget set |
| Data Processing | Pandas, NumPy | Latest stable | Standard for tabular data loading, cleaning, and preprocessing |
| Statistics | SciPy | Latest stable | Chi-square and KS test implementations for expert statistics view |
| Charting | Matplotlib (MVP); PyQtGraph (under future evaluation) | Latest stable | Matplotlib for fastest MVP delivery; PyQtGraph considered later for smoother interactive/large-dataset rendering |
| Database | None | — | All data stays in memory for the session; no persistence layer, by design (Local-First core value) |
| Infrastructure | None | — | Distributed as a standalone desktop binary; no servers, no hosting |
| Package Manager | uv | Latest | Fast, modern Python dependency/venv management |
| CI/CD | GitHub Actions | — | Lint, type-check, and test on PRs; build PyInstaller artifacts on release tags |

## Internationalization (i18n)

- **Default language**: English. Selectable options through M2: Korean, Chinese, Japanese (see ADR-004 in `memory/decisions.md`).
- **Approach**: PySide6/Qt's built-in translation system (`QTranslator` loading `.qm` files compiled from `.ts` source via `pyside6-lupdate` / `pyside6-lrelease`). No new external dependency — this tooling ships with the already-approved PySide6 dependency.
- **Scope note**: Language selection is a UI-layer concern only; the Analysis Engine (Pandas/NumPy/SciPy) has no user-facing strings and stays language-agnostic.

## Architecture Patterns

- **Structure**: Layered desktop architecture — UI layer (PySide6 widgets/windows) → Application/Controller layer (session state, workflow orchestration) → Analysis Engine (Pandas/NumPy/SciPy, framework-agnostic and independently testable) → Report/Export layer (HTML report generation)
- **API style**: None external; internal module boundaries only (Analysis Engine exposes a plain-Python API consumed by the UI layer)
- **State management**: In-memory session state (selected file/sheet/column, preprocessing choices, analysis results) held by the Controller layer and driven by Qt signals/slots — no external state store

## Environments

Benford Lens is a local desktop application, not a hosted service. There is no staging or
production server; "environments" here refer to build/distribution channels instead:

| Environment | Purpose | Access |
|-------------|---------|--------|
| Local (dev) | Local development, run from source | Developer machine only |
| Packaged build | Pre-release verification of the PyInstaller binary | Reviewer / tester machines |
| GitHub Release | Public distribution of tagged versions | End users, via download |
