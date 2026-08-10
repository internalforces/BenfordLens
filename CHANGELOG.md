# Changelog

All notable changes to Benford Lens are documented in this file.

## 1.0.1 — 2026-08-11

This public-readiness patch supersedes the private v1.0.0 desktop packages with a reduced,
notice-complete runtime and adds open-source project governance. It does not change the analysis
method or local-data boundary.

### Added

- Complete checked-in third-party license, attribution, source, and hash inventories.
- Qt/PySide source availability and dynamic-library replacement guidance.
- A translated local in-app view for third-party notices.
- Contribution, security, support, conduct, issue, and pull-request guidance.
- Dependabot coverage for uv and GitHub Actions, CODEOWNERS, public-only CodeQL, and tested
  repository ruleset definitions.

### Changed

- Replaced the broad PySide6 metapackage with PySide6 Essentials and removed Addons.
- Excluded every Qt 6.11 GPL-only module from native package collection and made completed
  package checks fail if one is present.
- Included the complete notice set in macOS app, Windows portable ZIP, and Windows MSI paths.
- Pinned every GitHub Action to a full commit SHA and uv to an exact version.
- Restricted release writes to one tag-only publisher after the complete verified asset set is
  available.

### Security and privacy

- Audited reachable Git history, branches, pull requests, Actions logs, and private v1.0.0 assets
  before public exposure; no critical/high-risk exposure remained.
- The application still performs all user-data processing locally and adds no network behavior.

## 1.0.0 — 2026-08-10

The initial release inside the private repository contains verified but unsigned Windows x64
ZIP/MSI and macOS arm64 ZIP packages, matching SHA-256 files, and explicit platform-security
notices.

### Added

- Explicit first-digit, second-digit, and combined analysis modes.
- User-controlled preprocessing with before/after preview.
- Advisory data-characteristics panel and optional MAD, Chi-square, KS, and sample-size details.
- Position-aware raw-row drill-down, substring search, and local CSV export.
- Mode-aware local HTML reports.
- Selectable English, Korean, Chinese, Japanese, Spanish, French, and Russian interfaces.
- PyInstaller configurations for macOS, Windows, and Linux.
- A user-scoped WiX MSI build and verification workflow for Windows x64.
- Matching Korean and English portfolio landing pages plus four bilingual public guides.
- Reproducible real-application screenshots and a workflow GIF generated with synthetic data.
- The MIT License.
- A tag-driven native Windows/macOS release workflow with package smoke tests, checksums, and
  atomic draft-to-public GitHub Release publication.

### Changed

- Reused one preprocessing snapshot across combined first- and second-digit results.
- Improved 100k-row analysis performance by 30.0–31.8% in the recorded controller benchmark.
- Added a scroll-safe desktop workflow, responsive combined layouts, and readable chart minimums.
- Kept all result and report guidance neutral and reference-oriented.
- Moved historical implementation plans and design specs under `reports/development/` so the
  public `docs/` path contains only the case study, architecture, verification, and user guide.

### Security and privacy

- All file reading, preprocessing, analysis, charts, and report generation remain local.
- No login, telemetry, cloud analysis, or external data transmission is included.
