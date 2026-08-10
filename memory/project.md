<!--
Purpose:        Current project state snapshot — the first context file every agent reads
Owner:          All agents (read), Planner / Release Manager (write)
Update Trigger: Version change, milestone completed, major status shift
Harness Version: 1.1
-->

# Project: Benford Lens

_Last updated: 2026-08-09_

## Summary

An open-source desktop application that lets non-experts easily analyze Benford's Law on
their own CSV/Excel data, entirely on their local machine, with no data ever sent to an
external server.

## Current State

- **Version**: v1.0.0
- **Phase**: v1.0 implementation and cross-platform release-candidate hardening are merged to
  `main` through PR #13; no public v1.0.0 tag or GitHub Release has been published
- **Next milestone**: Sign and clean-machine-verify the approved macOS/Windows release assets,
  then create the v1.0.0 tag and GitHub Release; Linux remains a later verification target
- **Overall health**: 🟡 Feature-complete; public distribution trust and verification remain

## Tech Summary

| Field | Value |
|-------|-------|
| Language | Python 3.11 (pinned via `.python-version`) |
| Framework | PySide6 (UI); Pandas/NumPy/SciPy (analysis); Matplotlib (charts) |
| Infrastructure | None — local desktop app, packaged via PyInstaller plus a WiX MSI on Windows; macOS arm64, Windows x64 ZIP, and Windows x64 MSI candidates built + smoke-tested; Linux remains config-only per TD-003 |
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
├── resources/icons/          (approved macOS PNG/ICNS plus derived Windows multi-size ICO)
├── packaging/                 (PyInstaller specs plus WiX MSI source/build script)
├── docs/                      (public case study, architecture, verification, user guide,
│                                and synthetic-data visual assets)
├── reports/development/       (archived implementation plans and design specs)
├── scripts/                   (reproducible synthetic portfolio asset generator)
├── tests/                    (mirrors src/ layout; tests/conftest.py sets QT_QPA_PLATFORM=offscreen)
└── .github/workflows/ci.yml  (lint, format-check, type-check, test on push/PR to main)
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
| 2026-08-07 | TASK-028 built and verified a macOS arm64 PyInstaller distribution candidate, synchronized bundle version metadata with the project version, and produced a checksum-recorded ZIP; Developer ID signing/notarization remains required for public macOS distribution |
| 2026-08-07 | TASK-029 synchronized the package, lockfile, README, roadmap, and project metadata to v1.0.0, added the v1.0 changelog, and merged PR #9 after CI passed; release signing remains gated on a Developer ID Application identity and Apple notarization credentials |
| 2026-08-07 | TASK-033 adopted icon concept A and applied transparent PNG/ICNS assets to the macOS PyInstaller bundle; Windows/Linux icons remained unchanged in that task and no new distribution build was produced |
| 2026-08-08 | TASK-034 built and verified the Windows x64 PyInstaller package with a multi-resolution ICO derived from the approved macOS image; all 241 tests and both folder/ZIP startup smoke tests passed, and an unsigned checksum-recorded ZIP was produced |
| 2026-08-08 | TASK-035 added a pinned WiX 5.0.2 user-scoped MSI around the Windows x64 one-folder build; metadata, all 1,194 files, non-elevated install, startup, complete uninstall, and SHA-256 generation were verified |
| 2026-08-09 | Revalidated the latest `origin/main` baseline: Ruff lint and format checks pass, mypy reports no issues across 22 source files, and all 241 tests pass on macOS with Qt offscreen; portfolio-documentation readiness was audited without changing product scope |
| 2026-08-09 | TASK-037 implemented the approved portfolio documentation layer: Korean/English README entry points, four bilingual public guides, reproducible synthetic PNG/GIF assets, archived development plans under `reports/development/`, and an MIT license |

## Verified Implementation Baseline

| Area | Status | Evidence / Boundary |
|------|--------|---------------------|
| Core analysis | Complete | First-, second-, and combined-digit analysis; user-controlled preprocessing; advisory suitability metrics; optional MAD/Chi-square/KS references |
| Desktop workflow | Complete | Explicit file/sheet/column/mode choices, responsive results, position-aware drill-down, local CSV export, and local HTML reports |
| Internationalization | Complete for current scope | English plus complete KO/ZH/JA/ES/FR/RU catalogs; Windows CJK font handling verified |
| Automated quality gate | Passing | Ruff, format check, mypy (22 source files), and 241 pytest tests passed locally; GitHub Actions passed on PR #13 merge commit `b1d63df` |
| macOS packaging | Candidate verified | Apple Silicon app/ZIP built and headless-smoke-tested; Developer ID signing, notarization, and clean-machine verification remain |
| Windows packaging | Candidate verified | x64 ZIP and per-user MSI built; install/startup/uninstall smoke tests passed; Authenticode signing and clean-machine verification remain |
| Linux packaging | Configuration only | PyInstaller spec exists but has not been built or verified on Linux |
| Public release | Not published | Source version is 1.0.0, but no v1.0.0 tag or GitHub Release exists yet |

## Constraints

- 100% local processing — no internet connection required, no data upload, no login/accounts, no AI/API server calls
- User must explicitly choose which column to analyze — no auto-analysis
- All major preprocessing choices (negative handling, zero handling, decimal handling, blanks, duplicates, string-to-number parsing) are user-selectable, with a before/after preview
- Neutral, non-accusatory language only — never "manipulated" or "fraud"; the program never auto-confirms whether Benford's Law applies to a dataset
- MVP excludes: cloud storage, accounts/login, AI-based fraud detection, online upload, direct PDF export, real-time collaboration
