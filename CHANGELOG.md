# Changelog

All notable changes to Benford Lens are documented in this file.

## 1.0.0 — 2026-08-10

The first public release distributes verified but unsigned Windows x64 ZIP/MSI and macOS arm64
ZIP packages through GitHub Releases, with matching SHA-256 files and explicit platform-security
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
