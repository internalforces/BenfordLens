<!--
Purpose:        External dependency tracking and version constraints
Owner:          Architect / Implementer
Update Trigger: Dependency added, removed, or version changed (HUMAN APPROVAL required)
Harness Version: 1.1
-->

# dependencies.md — Benford Lens Dependencies

_Last updated: 2026-08-08_

## Core Dependencies

| Package | Version | Purpose | License |
|---------|---------|---------|---------|
| PySide6 | latest stable (TBD at implementation) | Desktop UI framework | LGPL-3.0 |
| pandas | latest stable (TBD) | Tabular data loading and preprocessing | BSD-3-Clause |
| numpy | latest stable (TBD) | Numerical operations underlying Pandas/SciPy | BSD-3-Clause |
| scipy | >=1.14 | MAD / Chi-square / KS expert statistics | BSD-3-Clause |
| matplotlib | latest stable (TBD) | Expected vs. actual distribution charts (MVP) | PSF-based (BSD-style) |
| openpyxl (or equivalent) | latest stable (TBD) | XLSX reading via Pandas | MIT |

## Dev Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pytest | latest stable (TBD) | Test runner |
| ruff | latest stable (TBD) | Linting and formatting |
| mypy | latest stable (TBD) | Static type checking |
| pyinstaller | latest stable (TBD) | Packaging into a standalone executable |
| .NET SDK | 8.0 | Build host for the Windows installer project only |
| WixToolset.Sdk | 5.0.2 | Build the Windows x64 MSI; pinned MS-RL release |

## External Services / APIs

| Service | Purpose | Auth | Notes |
|---------|---------|------|-------|
| — | (none) | — | By design: Benford Lens makes no external API or network calls of any kind (see AGENTS.md Absolute Restrictions) |

## Approval Record

- **2026-08-05 — SciPy**: Explicitly approved by the user for TASK-011. SciPy runs entirely
  in-process on the locally preprocessed values; no dataset content or derived value leaves
  the machine.

- **2026-08-08 — WiX MSI packaging**: Explicitly approved by the user for TASK-035. WiX and
  the .NET SDK are build-time dependencies only; the installed application has no .NET runtime
  dependency and no network or update-check behavior was added.

## Version Policy

- Major upgrades: HUMAN APPROVAL + full test suite required
- Minor / patch: Reviewer sign-off then proceed
- Security patches: Apply immediately, Reviewer reviews after
- Any **new** dependency (not just upgrades) requires HUMAN APPROVAL, with explicit confirmation that it makes no network calls
