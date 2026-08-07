# Changelog

All notable changes to Benford Lens are documented in this file.

## [1.0.0] — 2026-08-07

### Added

- Explicit first-digit, second-digit, and combined analysis modes.
- User-controlled preprocessing with before/after preview.
- Advisory data-characteristics panel and optional MAD, Chi-square, KS, and sample-size details.
- Position-aware raw-row drill-down, substring search, and local CSV export.
- Mode-aware local HTML reports.
- Selectable English, Korean, Chinese, Japanese, Spanish, French, and Russian interfaces.
- PyInstaller configurations for macOS, Windows, and Linux.

### Changed

- Reused one preprocessing snapshot across combined first- and second-digit results.
- Improved 100k-row analysis performance by 30.0–31.8% in the recorded controller benchmark.
- Added a scroll-safe desktop workflow, responsive combined layouts, and readable chart minimums.
- Kept all result and report guidance neutral and reference-oriented.

### Security and privacy

- All file reading, preprocessing, analysis, charts, and report generation remain local.
- No login, telemetry, cloud analysis, or external data transmission is included.

[1.0.0]: https://github.com/internalforces/BenfordLens/releases/tag/v1.0.0
