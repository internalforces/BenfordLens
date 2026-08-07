# macOS PyInstaller Distribution Candidate — 2026-08-07

## Scope

Build and locally verify the post-TASK-027 Benford Lens macOS application without changing the
analysis pipeline, source-data protections, or local-only behavior.

## Artifact

- File: `dist/Benford-Lens-0.2.0-macOS-arm64.zip`
- Source version: `0.2.0.dev0`
- macOS bundle versions: `0.2.0`
- Architecture: Apple Silicon (`arm64`)
- Uncompressed app bundle: 202 MB
- ZIP archive: 81 MB
- SHA-256: `537fbb55bad689b461b4b848d1d535d49cf21558bd67cf1161d83550c9773764`

## Verification

- Ruff lint passed.
- Ruff format check passed for 46 files.
- mypy passed for 22 source files.
- All 232 tests passed with the offscreen Qt platform.
- PyInstaller 6.21.0 completed the bundle build.
- The bundle contains all six translated `.qm` catalogs; English remains built in as default.
- Strict deep signature validation passed for the staged ad-hoc-signed bundle.
- The frozen executable started headlessly and remained running through the smoke interval.
- The ZIP passed compressed-data validation.
- After extracting the ZIP into a clean temporary directory, strict deep signature validation
  passed again.

## Distribution Boundary

This is a locally verified distribution candidate. It is not signed with an Apple Developer ID
and has not been notarized or tested on a clean external Mac. Public macOS distribution requires
those steps, and the current artifact supports arm64 Macs only. Windows and Linux builds remain
unverified on their target platforms.
