<!--
Purpose:        Project milestones and feature planning
Owner:          Planner
Update Trigger: Milestone completed, new feature added, priorities changed
Harness Version: 1.1
-->

# roadmap.md — Benford Lens Roadmap

_Last updated: 2026-08-09_

## Goal

An open-source desktop application that lets non-experts easily analyze Benford's Law on
their own CSV/Excel data, entirely on their local machine, with no data ever sent to an
external server.

## Milestones

### M1 — MVP (PRD Phase 1) — implemented and merged to `main` (PR #1)
- [x] CSV file reading (with automatic encoding detection)
- [x] Excel file reading (with sheet selection)
- [x] Manual column selection (no auto-analysis of "numeric-looking" columns)
- [x] First-digit Benford analysis
- [x] Expected vs. actual distribution chart output

### M2 — Phase 2 — implemented and merged to `main` (PRs #2–#4)
- [x] Preprocessing options (negative handling, zero handling, decimal handling, blank handling, duplicate handling, string-to-number parsing) with before/after preview
- [x] Data suitability check (🟢/🟡/🔴) with sample count, min/max, digit range, duplicate rate, zero rate, negative rate, missing rate, distinct-value count
- [x] Raw data drill-down (click a leading digit in the chart → filtered original rows)
- [x] HTML report generation
- [x] UI language selection — default English; selectable Korean/Chinese/Japanese (i18n scaffolding, see ADR-004)
- [x] Expert statistics panel (MAD, Chi-square, KS Test, sample size) — hidden by default

### M3 — v1.0 (Phase 3) — implemented and merged to `main` (PRs #5–#8)
- [x] Second-digit analysis
- [x] Combined first+second-digit analysis — both independent results shown together in one
  results view (not a joint first-two-digit distribution; see ADR-009)
- [x] Performance optimization for large datasets — removed repeated digit extraction;
  100k-row controller benchmark improved 30.0–31.8% (TASK-024)
- [x] Expand language support beyond the initial EN/KO/ZH/JA set added in M2 — Spanish,
  French, and Russian added in M3 (ADR-010, ADR-011)

### v1.0 release hardening — implementation complete; public release pending (PRs #9–#13)

- [x] Synchronize source, package, and changelog metadata to 1.0.0
- [x] Build and headless-smoke-test a macOS arm64 PyInstaller candidate
- [x] Apply the approved application icon to macOS and Windows packages
- [x] Build and smoke-test a Windows x64 PyInstaller ZIP
- [x] Build and verify a user-scoped Windows x64 MSI, including install/startup/uninstall
- [ ] Sign, notarize, staple, and clean-machine-verify the macOS distribution
- [ ] Authenticode-sign and clean-machine-verify the Windows ZIP/MSI distributions
- [ ] Create the annotated v1.0.0 tag and publish verified GitHub Release assets
- [ ] Build and verify the Linux package on a Linux target (post-v1.0 distribution follow-up)

### Portfolio documentation — implemented on 2026-08-09

- [x] Create matching Korean and English recruiter-oriented README landing pages
- [x] Limit the public documentation path to a bilingual case study, architecture, verification,
  and user guide
- [x] Preserve internal memory/tasks/reports and archive previous plans/specs under
  `reports/development/`
- [x] Capture real application PNG/GIF assets with deterministic synthetic data
- [x] Add the user-approved MIT license

## Backlog Ideas

- Additional file format support: XLS, ODS, TSV (PRD §5, explicitly post-MVP)
- Evaluate migrating charts from Matplotlib to PyQtGraph for smoother interaction on large datasets

## Out of Scope (MVP)

- Cloud storage
- User accounts / login
- AI-based fraud judgment or automatic fraud detection
- Online data upload
- Direct PDF generation (HTML report only for now)
- Real-time collaboration
