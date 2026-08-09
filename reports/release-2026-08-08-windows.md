# Windows x64 Build Verification — 2026-08-08

## Result

Benford Lens v1.0.0 was built successfully as a PyInstaller one-folder Windows x64 package.
The executable embeds a multi-resolution ICO derived from the same approved 1024 px PNG used
for the macOS icon.

## Quality Gate

- Ruff check: pass
- Ruff format check: 46 code files already formatted
- mypy: pass, 22 source files
- pytest: 241 passed
- PyInstaller: 6.21.0 with Python 3.11.15

## Package Verification

- PE machine: `0x8664` (x64)
- Packaged translations: KO, ZH, JA, ES, FR, and RU plus built-in English
- Build-folder startup smoke test: pass (process remained active for 8 seconds)
- ZIP extraction: pass
- Extracted executable hash comparison: pass
- Extracted-ZIP startup smoke test: pass (process remained active for 8 seconds)
- Executable Authenticode status: `NotSigned`
- Uncompressed package size: 279,731,590 bytes
- ZIP size: 119,239,813 bytes

## Checksums

- ZIP SHA-256: `EEB9AD9785745D0D3AA81551CA6D0B1EA15E3C276F24085C4FAAA417C70AA8FF`
- Executable SHA-256: `B6C6E0AD0228B3116CB885A7B51CA09C318B066F2F0A3AF84D4C3FEB41D6A637`

## Distribution Boundary

This is an unsigned Windows x64 build candidate. Another PC may display a Windows SmartScreen
warning. Authenticode signing and clean-machine verification remain required before treating it
as a broadly trusted public release.
