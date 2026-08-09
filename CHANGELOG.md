# Changelog

All notable changes to Benford Lens are documented in this file.

## 1.0.0 — release candidate (unpublished)

The source and package metadata use version 1.0.0, but no public `v1.0.0` tag or GitHub Release
has been published. The entries below describe the current release-candidate baseline.

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
