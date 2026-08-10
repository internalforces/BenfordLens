# GitHub Release Automation Verification — 2026-08-10

## Result

PR #15 implemented the user-approved unsigned GitHub Releases distribution path. After review and
merge, annotated tag `v1.0.0` triggered native builds and the verified six-asset Release was
published at <https://github.com/internalforces/BenfordLens/releases/tag/v1.0.0>.

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

## v1.0.0 tag publication

- Approved merge commit: `a59aa6f0439b5788b1239714e7ef28ee2abde70e`
- Annotated tag: `v1.0.0`
- Tag workflow run: `31386790097`
- Release metadata: pass in 7 seconds
- macOS arm64 build, smoke test, and upload: pass in 1 minute 56 seconds
- Windows x64 ZIP/MSI build, lifecycle tests, and upload: pass in 5 minutes 33 seconds

The final publication job initially failed because it ran without a repository checkout and the
`gh release edit` command did not specify `--repo`. All native jobs and six uploads had already
succeeded. The draft's asset names and GitHub digests were checked, all assets were downloaded,
the three package hashes were verified, both ZIP archives passed integrity testing, and the MSI
was identified as a WiX 5.0.2 x64 installer before the existing draft was manually published with
explicit repository context. The workflow now passes `--repo "$GITHUB_REPOSITORY"` for future
publication jobs.

Windows checksum files used CRLF endings. Their hash values were valid, but macOS `shasum -c`
treated the carriage return as part of the filename. The release verification normalized only the
line endings while checking the published files, and the Windows writers now emit LF endings.

## Authoritative package checksums

| Package | SHA-256 |
|---|---|
| `Benford-Lens-1.0.0-macOS-arm64.zip` | `d4e320b11ed53705be088503286fb48077bb0068472ff6a806f05f8c75f9cc71` |
| `Benford-Lens-1.0.0-windows-x64.zip` | `f86fa1fe85dcd5be830db554fe3a24089157519beedfe92ddb56baf1c2eed8f8` |
| `Benford-Lens-1.0.0-windows-x64.msi` | `9fdefe43e0f09d9eb0c49cfc0af2732a254bf16ace8fbac4d498eda4160e55ae` |

TASK-029 is complete. Platform signing and notarization remain deliberately separate trust
improvements tracked by TD-007 and TD-008.
