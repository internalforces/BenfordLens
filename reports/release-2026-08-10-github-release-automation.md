# GitHub Release Automation Verification — 2026-08-10

## Result

PR #15 implements the user-approved unsigned GitHub Releases distribution path. The first native
pull-request run completed successfully on GitHub-hosted Windows x64 and macOS arm64 runners.

## Workflow

- Run: `31378776699`
- Release metadata: pass in 10 seconds
- macOS arm64: pass in 1 minute 35 seconds
- Windows x64: pass in 7 minutes 1 second
- Publication job: correctly skipped for a pull request; it runs only for an exact version tag

## Windows verification

- PyInstaller x64 one-folder package built from the locked Python 3.11 environment.
- Portable ZIP produced, extracted into a fresh temporary directory, and started for 8 seconds.
- Extracted executable SHA-256 matched the pre-archive executable.
- WiX 5.0.2 MSI produced with 1,238 packaged files.
- Per-user silent install, installed-app 8-second startup, silent uninstall, and residue checks
  passed.
- Executable and MSI Authenticode status were both `NotSigned`, matching the release notice.
- PR-run ZIP SHA-256: `9FDFB46B6F03BB001897C12535132C3A25F584B4BF7BD77E5BF2A2C7B2230DBB`.
  The tag build will produce and publish its own authoritative checksum.

## macOS verification

- PyInstaller app bundle and ZIP built on GitHub's standard `macos-14` arm64 runner.
- Bundle version and build version matched `1.0.0`.
- Main executable architecture was exactly arm64.
- All six application translation catalogs were present.
- Ad-hoc signature integrity passed before and after ZIP extraction.
- Original and extracted apps each remained active for the 8-second headless smoke interval.
- A matching SHA-256 file was produced. The tag build checksum will be authoritative.

## Publication safety boundary

The workflow creates a draft Release only for a semantic-version tag whose version exactly matches
`pyproject.toml`. Windows and macOS upload distinct asset names to that draft. The final job makes
the Release public only when both native jobs succeed. Reruns may replace assets only while the
Release remains a draft; an already-public Release is not replaced.

## Remaining gate

Project standards prohibit self-merge and require reviewer sign-off. After PR #15 is reviewed and
merged, create an annotated `v1.0.0` tag on the approved `main` commit. The tag run must succeed,
publish all six package/checksum assets, and be verified before TASK-029 is completed.
