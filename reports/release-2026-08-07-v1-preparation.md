# v1.0.0 Release Preparation — 2026-08-07

## Completed

- Synchronized `pyproject.toml`, `uv.lock`, README, roadmap, changelog, and project records to
  version `1.0.0`.
- Verified the installed package metadata reports `1.0.0`.
- Passed Ruff lint and format checks, mypy, and all 232 tests.
- Built the macOS application with PyInstaller 6.21.0 and Python 3.11.15.
- Verified `CFBundleShortVersionString` and `CFBundleVersion` are both `1.0.0`.
- Verified the application is an arm64 Mach-O bundle with six translated `.qm` catalogs plus
  built-in English.
- Passed strict deep signature-integrity validation for the generated ad-hoc bundle.
- Passed the headless startup smoke interval.

## Release Gate

The build host currently has one `Apple Development` identity but no `Developer ID Application`
identity. No approved `notarytool` keychain profile or notarization environment credentials were
detected. The bundle therefore cannot yet be Developer ID signed, submitted to Apple, stapled, or
published as the v1.0.0 public release asset.

The `v1.0.0` tag and GitHub Release remain intentionally absent until this gate is satisfied.
