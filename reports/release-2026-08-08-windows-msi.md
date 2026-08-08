# Windows x64 MSI Verification — 2026-08-08

## Result

Benford Lens v1.0.0 was packaged successfully as a user-scoped Windows x64 MSI. The installer
wraps the verified PyInstaller one-folder application, installs under
`%LOCALAPPDATA%\Programs\Benford Lens`, and creates a Start menu shortcut.

## Toolchain

- Python: 3.11.15
- PyInstaller: 6.21.0
- .NET SDK: 8.0.423, build-time only
- WixToolset.Sdk: 5.0.2, pinned MS-RL release
- Build-tool telemetry: explicitly disabled by the build script

## Package Verification

- Product name: `Benford Lens`
- Product version: `1.0.0`
- UpgradeCode: `{A256B439-D3D1-4538-B385-7DFAA4F5E283}`
- Installation scope: current user; verified from a non-elevated process
- Embedded PyInstaller files: 1,194 of 1,194
- MSI validation: pass with only documented per-user harvesting ICE exclusions
- Silent install: pass
- Installed application startup: pass; remained active for 8 seconds offscreen
- Start menu shortcut: pass
- Silent uninstall: pass
- Post-uninstall application directory, shortcut directory, and installer marker: absent
- MSI size: 91,573,116 bytes
- Authenticode status: `NotSigned`

## Checksum

- MSI SHA-256: `85B7FB0702583B715FBD4D612564EFDF701F53B021B0C4205708AB63B48EF355`

## Distribution Boundary

This is an unsigned build-machine candidate, not a broadly trusted public release. Sign the
application executable and MSI with an approved Authenticode certificate, then repeat the
installation, startup, upgrade, and uninstall checks on a clean supported Windows machine.
