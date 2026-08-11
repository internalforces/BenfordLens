# Public Launch Preparation — v1.0.1

_Prepared: 2026-08-11_

## Scope

This record covers the source, governance, license, automation, and local verification prepared
before any native distribution build or public visibility change. The repository remains private.

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
behavior remain part of the native Windows job. No PyInstaller distribution, ZIP, MSI, tag,
Release asset, or visibility mutation was produced during this local gate.

## Required next gates

1. Commit and push the preparation branch without `README 2.md`.
2. Obtain explicit human approval immediately before opening the PR, because its path filters run
   the native Windows/macOS distribution jobs.
3. Require standard CI, release metadata, and both native package jobs to pass; inspect retained
   packages for notice presence, Qt denylist absence, checksums, startup/install lifecycle, and
   exact inventory.
4. Merge the reviewed PR; then enable full-SHA enforcement. The selected-Action allowlist and
   active no-bypass `main`/release-tag rulesets are already enforced.
5. Re-verify both rulesets and enable public-only scanning/reporting features immediately after
   visibility changes.
6. Obtain explicit release approval; tag `v1.0.1`, publish its six verified assets, and return
   v1.0.0 to draft without deleting its tag/assets.
7. Re-download v1.0.1 and independently verify all files before requesting visibility approval.
8. Surface the 17 real-display-name commits, retained records, branches/PRs/Actions history,
   unsigned packages, and exact visibility consequences at the final human gate.
