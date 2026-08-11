# Public Launch Preparation — v1.0.1

_Prepared: 2026-08-11_

## Scope

This record covers the source, governance, license, automation, local checks, explicitly approved
native verification, and PR #17 merge completed before any Release or public visibility change.
The repository remains private.

## Prepared release

- Source version: `1.0.1`
- Intended tag: annotated `v1.0.1` on the reviewed `main` merge commit
- Intended assets:
  - `Benford-Lens-1.0.1-windows-x64.zip` and checksum
  - `Benford-Lens-1.0.1-windows-x64.msi` and checksum
  - `Benford-Lens-1.0.1-macOS-arm64.zip` and checksum
- Release notes: `.github/release-notes/1.0.1.md`
- Trust boundary: unsigned Windows packages; ad-hoc signed, unnotarized macOS package; warnings
  remain explicit in README and release notes

The private v1.0.0 Release and tag are not deleted or replaced. Before public visibility, the
release-publication approval should also authorize returning v1.0.0 to draft so its older package
set is retained for evidence but not anonymously downloadable. v1.0.1 becomes the only published
desktop Release.

## Completed preparation

- TASK-039 exposure audit and preserve/no-rewrite decision
- TASK-040 exact notices, source hashes, Qt reduction/denylist, relinking guide, in-app access,
  package inclusion policy, and automated static checks
- TASK-041 contribution, support, security, conduct, issue/PR guidance, package project URLs,
  GitHub description/homepage/topics, and README entry points
- TASK-042 immutable workflow references, exact uv, least-privilege release handoff, Dependabot,
  CODEOWNERS, public-only CodeQL, and tested importable ref rules

## Local verification

| Check | Result |
|---|---|
| uv 0.11.30 lock validation | Pass — 40 packages |
| Ruff lint | Pass |
| Ruff format | Pass |
| mypy | Pass — 22 source files |
| pytest | Pass — 258 tests |
| Translation compilation | Pass — six catalogs, 95 entries each |
| Workflow / issue-form YAML parsing | Pass |
| Tracked Markdown link and image validation | Pass — 50+ local targets and 8+ images |
| macOS release shell syntax | Pass |
| Notice generator reproducibility and hash/source tests | Pass |
| Restricted user-facing wording scan for new content | No finding |
| User-owned `README 2.md` | Untracked, unread, unmodified, unstaged |

PowerShell is not installed on the macOS preparation host, so Windows script parsing and package
behavior were verified by the native Windows job. No local PyInstaller distribution, tag, Release
asset, or visibility mutation was produced during the local gate.

## Hosted and native verification

- PR #17 head: `665793a7b1ddae8d87ef4b1309c3cbb87b5b0833`
- Linux CI run `31447586712`: pass, including Ruff, formatting, mypy, and 258 tests
- Native run `31447586711`: pass
  - release metadata: pass
  - macOS arm64 ZIP build/notice/denylist/integrity/startup verification: pass in 1m42s
  - Windows x64 ZIP/MSI build/notice/denylist/startup/install/uninstall verification: pass in 5m10s
  - tag-only publisher: correctly skipped for the PR event
- Retained verification artifacts expire after seven days:
  - `release-macos-arm64`, 78,833,003 bytes, expires 2026-08-18T00:55:52Z
  - `release-windows-x64`, 199,358,606 bytes, expires 2026-08-18T00:59:11Z
- PR #17 merge commit: `49edb74bf9d07df8957b1642957fe52a64627907`
- Post-merge `main` CI run `31447921264`: pass on the exact merge commit
- Post-merge Actions policy: `sha_pinning_required=true`

## Gate status

1. [x] Commit and push the preparation branch without `README 2.md`.
2. [x] Obtain explicit approval before PR-triggered native distribution checks.
3. [x] Pass Linux CI, release metadata, and both native package jobs on the exact PR head.
4. [x] Merge through protected `main`, then enable and re-read full-SHA enforcement.
5. [x] Obtain explicit release approval; tag `v1.0.1`, publish its six verified assets, and return
   v1.0.0 to draft without deleting its tag/assets.
6. [x] Re-download v1.0.1 and independently verify every file before visibility approval.
7. [ ] Surface the 17 real-display-name commits, retained records, branches/PRs/Actions history,
   unsigned packages, and exact visibility consequences at the final human gate.
8. [ ] After visibility changes, re-verify both rulesets and enable/test public-only
   scanning/reporting features.
