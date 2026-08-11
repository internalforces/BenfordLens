<!--
Purpose:        Current session state — context handoff between agents
Owner:          Currently active agent
Update Trigger: Read at session start; must update before session ends
Harness Version: 1.1
-->

# Current Session — Benford Lens

> Archive this file after the next implementation session is completed.

## Session Info

- **Date**: 2026-08-11
- **Agent Role**: Planner / Researcher / Implementer / Security Reviewer / Release Manager
- **Session Goal**: Complete TASK-039–044 and every evidence, merge, package, release,
  hardening, and visibility gate required for a safe public launch.

## Completed This Session

- [x] Created `codex/public-launch-preparation` from current `origin/main` while preserving the
  unrelated user-owned `README 2.md` as untracked, unread, and unstaged.
- [x] Completed TASK-039: scanned 101 commits and all reachable objects, seven remote branches,
  16 PR conversations, 42 Actions runs/logs, the tag and six Release assets; independently
  verified every package checksum and archive; found no critical/high-risk exposure.
- [x] Preserved the complete audited history and engineering evidence under ADR-019, moved the
  stale `memory/session 2.md` content to a dated archive without deletion, and documented the
  17 real-display-name commits that must be surfaced again at the visibility gate.
- [x] Audited exact Python/Qt/native/build-tool licensing, recorded ADR-020, replaced the broad
  PySide6 metapackage with Essentials, removed Addons, and added a deterministic offline
  notice/source/hash inventory plus Qt relinking guidance.
- [x] Added GPL-only Qt module deny rules and completed-package checks for both native platforms,
  embedded the notice set in source/specs/ZIP/MSI paths, and exposed it through a local-only
  translated in-app dialog. Approved PR #17 run `31447586711` passed the resulting macOS arm64
  ZIP and Windows x64 ZIP/MSI package checks, completing TASK-040.
- [x] Completed TASK-041: added contribution, security, support, conduct, issue/PR guidance;
  package project URLs; README notice/community links; and verified GitHub description,
  homepage, and eight topics while keeping visibility private.
- [x] Prepared TASK-042 under ADR-021: pinned every Action to a full SHA and uv to 0.11.30,
  restricted Release writes to one tag-only publisher, added uv/Actions Dependabot, CODEOWNERS,
  public-only CodeQL, and importable tested `main`/release-tag rulesets.
- [x] Enforced the selected-Action allowlist and active no-bypass `main`/release-tag rulesets on
  GitHub; enabled the dependency graph, alerts, and security updates; confirmed zero initial open
  Dependabot alerts. Full-SHA enforcement is now enabled after the pinned workflow merge;
  public-only secret scanning/reporting/CodeQL remain unavailable while private.
- [x] Local gate passes: uv lock check, Ruff, formatting, mypy across 22 source files, workflow/
  issue-form YAML parsing, tracked Markdown link/image validation, translation compilation, and
  all 258 tests.
- [x] PR #17 was opened after the native-build approval gate. The first Linux CI run exposed a
  platform-assumption bug in the deterministic license generator: macOS-only `macholib` was
  required in Linux CI. Its exact MIT notice now lives with the other platform-specific notices,
  the platform-neutral bundle regenerates on every target, and regression coverage preserves the
  boundary without adding a dependency or weakening notice coverage.
- [x] The follow-up CI run proved that native NumPy wheels embed platform-specific library paths
  in otherwise equivalent license files. Bundle verification now checks the exact locked
  distribution/version set and a recorded full-bundle SHA-256 on every platform, while retaining
  byte-for-byte canonical reproduction on the macOS arm64 audit platform.
- [x] PR #17 passed Linux CI plus explicitly approved macOS and Windows native verification at
  `665793a`, then merged through the protected branch as `49edb74`. The full-SHA repository policy
  was enabled and re-read as true immediately afterward; post-merge `main` CI run `31447921264`
  also passed.
- [x] Merged the follow-up project-record PR #19 as `021a01f`; its post-merge `main` CI run
  `31448491305` passed before the release tag was created.
- [x] Received explicit TASK-043 approval immediately before distribution, created annotated tag
  object `19def39` for v1.0.1 at exact reviewed `main` commit `021a01f`, and triggered native run
  `31448799504` without changing repository visibility.
- [x] The run's metadata, macOS arm64, and Windows x64 jobs passed. The macOS package passed
  architecture, version, notice, denylist, ad-hoc integrity, extraction, and startup checks; the
  Windows ZIP/MSI passed notice, denylist, extraction/startup, and install/startup/uninstall checks.
- [x] The publisher rejected the verified Windows artifact because `actions/download-artifact`
  preserved its `msi/` subdirectory while the strict gate searched only one directory level.
  No partial Release existed and the protected tag was not moved or replaced.
- [x] Recovered from the same immutable run artifacts: independently verified all three package
  checksums and formats, manually created a draft, uploaded exactly six explicit files, matched
  every GitHub digest, and published v1.0.1 with its complete trust/support disclosures.
- [x] Re-downloaded all six assets from the published Release into a fresh directory; all three
  checksum files, both ZIP integrity checks, and all six GitHub digests matched.
- [x] Returned v1.0.0 to draft only after v1.0.1 verification. Its annotated tag still resolves
  to `a59aa6f`, and all six original asset IDs, sizes, and digests are unchanged.
- [x] Presented the final exposure summary, including the 17 real-display-name commits, 28 AI
  co-author trailers, retained public history/records, and unsigned-package trust boundaries;
  received explicit TASK-044 approval immediately before the change.
- [x] Changed `internalforces/BenfordLens` from private to public and anonymously verified the
  repository, tag, Release, README/badge/assets, nine branches, 20 pull requests, 71 Actions runs,
  eight topics, and all six v1.0.1 Release assets.
- [x] Fresh anonymous downloads matched all three SHA-256 files; both ZIP archives passed integrity
  checks and the MSI was identified as a valid WiX 5.0.2 x64 installation database.
- [x] Re-read both active no-bypass rulesets, selected Actions, full-SHA enforcement, read-only
  workflow defaults, Dependabot protections, and required CI after the visibility transition.
- [x] Enabled secret scanning, push protection, and private vulnerability reporting; both secret
  and CodeQL alert lists were empty, and the first public CodeQL analysis passed in run
  `31451987591` alongside `lint-type-test` run `31451987687` on PR #21.

## Current Recommendation

Keep the repository public under the verified rulesets and security controls. Merge PR #21 through
protected `main` after its recorded checks, then continue with the next approved documentation
milestone. Retain TD-007 and TD-008 until macOS Developer ID/notarization and Windows signing or
Store distribution are addressed.

## Previous Session Summary

The v1.0.0 source and release-candidate hardening were merged through PR #13. macOS arm64 and
Windows x64 distribution candidates were built and smoke-tested; Windows compatibility issues
were resolved; public signing and clean-machine verification remain. The detailed handoff is
archived in `memory/sessions/2026-08-08-Release-Packaging.md`.

## Previous Release Session — Completed Work

- [x] Read the project constitution and required context files in the prescribed order.
- [x] Fetched the latest remote state and created `codex/portfolio-docs-audit` from
  `origin/main` (`b1d63df`, PR #13) without committing to `main`.
- [x] Confirmed the source version is 1.0.0 and that no v1.0.0 tag is present.
- [x] Confirmed the GitHub Release list is empty and CI succeeded on the PR #13 merge commit.
- [x] Revalidated Ruff lint, Ruff formatting, mypy, and the full pytest suite.
- [x] Synchronized `memory/project.md`, `README.md`, `roadmap.md`, `CHANGELOG.md`, and
  `tasks/active.md` with the implemented and unpublished release-candidate state.
- [x] Audited portfolio-documentation readiness and recorded the recommended structure in
  `reports/portfolio-documentation-audit-2026-08-09.md`.
- [x] Received user approval for ADR-017 and implemented the audience-separated documentation
  structure.
- [x] Recorded missing open-source license metadata and portfolio-documentation gaps as TD-009
  and TD-010, then resolved both through TASK-037.
- [x] Completed TASK-036 and archived the previous release-packaging session summary.
- [x] Rewrote `README.md` as the English recruiter landing page and added the matching Korean
  `README.ko.md` entry point.
- [x] Added four bilingual public documents only: portfolio case study, architecture,
  verification, and user guide.
- [x] Preserved internal evidence and moved previous `docs/superpowers/` plans/specs into
  `reports/development/` so they no longer appear in the public documentation path.
- [x] Added a reproducible asset generator and visually checked three PNG screenshots plus a
  five-frame workflow GIF captured from the real app with deterministic synthetic data.
- [x] Added the user-selected MIT License and marked ADR-017 accepted.
- [x] Completed TASK-037.

## Previous Release Verification

- Remote baseline: `origin/main` at `b1d63df` (PR #13)
- GitHub Actions CI on `b1d63df`: pass
- GitHub Release list: empty
- Ruff check: pass
- Ruff format check: pass (47 files across `src/`, `tests/`, and `scripts/`)
- mypy: pass (22 source files)
- pytest: 241 passed on macOS with `QT_QPA_PLATFORM=offscreen`
- Source version: 1.0.0
- v1.0.0 tag: absent
- Product source or public analysis API changes: none
- New dependency, network analysis path, or source-data mutation: none
- Public documentation: 2 README entry points + 4 bilingual detail guides
- Local markdown links/images: validated, no missing targets
- Visual assets: three 1440×960 PNGs plus one five-frame 960×640 GIF (8.2 seconds)
- Asset provenance: real application, deterministic synthetic data only
- Public-copy restricted-term scan: no findings
- License: standard MIT text, 2026 Benford Lens contributors

## Current Implementation Status

- v1.0 product scope is feature-complete and merged to `main`.
- The v1.0.0 macOS arm64 and Windows x64 ZIP/MSI packages exist in the private repository's
  GitHub Release and have been independently downloaded and checksum-verified by an authenticated
  maintainer; they are not yet publicly accessible.
- macOS Developer ID signing/notarization and Windows Authenticode remain future trust
  improvements; the public notes disclose the current unsigned status.
- Linux has a PyInstaller specification but no target-platform build verification.
- Annotated tag `v1.0.0` targets approved `main` merge commit `a59aa6f`.

## Portfolio Documentation State

Accepted ADR-017 retains internal harness evidence while exposing a small public portfolio layer:
English and Korean README entry points, four bilingual guides, and synthetic-data visuals. The
public README navigation does not expose session/task history, while evidence remains available
under `memory/`, `tasks/`, and `reports/`. The repository now uses the MIT License.

## Follow-up Research — 2026-08-10

- Investigated free and approval-free Windows/macOS distribution paths using current Apple,
  Microsoft, GitHub, and SignPath documentation.
- Confirmed that new individual Microsoft Store registration is now free and that Store-submitted
  MSIX packages receive complimentary signing and hosting, while identity verification and app
  certification remain.
- Confirmed that trusted public macOS distribution still requires Apple Developer Program
  membership and an Apple-issued Developer ID certificate; the fee waiver is limited to eligible
  nonprofit, accredited educational, and government legal entities.
- Documented GitHub Releases as a free no-platform-approval hosting path whose unsigned artifacts
  retain Gatekeeper, SmartScreen, and possible Smart App Control friction.
- Recommended the minimum-cost production combination: Windows Store MSIX plus paid macOS
  Developer ID/notarization, with GitHub Releases for release artifacts and checksums.
- Refined TD-008 to include the newly confirmed Windows Smart App Control blocking risk and the
  Microsoft Store MSIX resolution path.
- Added `reports/research-2026-08-10-free-desktop-distribution.md`; no architecture decision,
  dependency, product code, release artifact, task status, or public-release state changed.

## Remaining Work

1. Review and merge the post-release records and workflow-hardening PR. This was completed as
   PR #16, but repository visibility remained private.

## Release Distribution Implementation — 2026-08-10

- Received explicit human approval to distribute Windows ZIP/MSI packages through GitHub Releases
  and adopted the same transparent unsigned path for the existing macOS arm64 target.
- Created `codex/github-releases-distribution` from the latest merged documentation baseline while
  preserving the unrelated untracked `README 2.md` file.
- Added native release scripts for Windows and macOS plus a tag-only, draft-first GitHub Release
  workflow; no application network path or dependency was added.
- Added v1.0.0 release notes and Korean/English download guidance that disclose SmartScreen,
  Smart App Control, Gatekeeper, Authenticode, Developer ID, and notarization boundaries.
- Recorded ADR-018 and updated TASK-029 from the earlier paid-signing publication gate to verified
  unsigned assets plus checksums and explicit warnings.
- Local verification: Ruff, formatting, mypy, 241 tests, workflow YAML, shell syntax, macOS arm64
  package metadata, six translations, ad-hoc signature integrity, original/extracted startup, and
  checksum verification all passed.
- Pushed commits `0b2da02` and `38040b2`, then opened draft PR #15.
- PR #15 verification: standard CI passed; release metadata passed; macOS arm64 passed in 1m35s;
  Windows x64 passed in 7m1s with 1,238 MSI files, ZIP startup, and MSI install/startup/uninstall.
- Publication correctly remained skipped because the event was a pull request rather than a tag.
- Added `reports/release-2026-08-10-github-release-automation.md` with the verification evidence.

## v1.0.0 Publication — 2026-08-10

- Confirmed PR #15 was human-reviewed and merged to `main` as `a59aa6f`.
- Created and pushed annotated tag `v1.0.0` on that exact merge commit.
- Tag workflow `31386790097` passed release metadata, macOS arm64 build/smoke/upload, and Windows
  x64 ZIP/MSI build/install/startup/uninstall/upload jobs.
- Diagnosed the final publication failure: the no-checkout job did not provide repository context
  to `gh release edit`; package outputs were not affected.
- Downloaded all six assets from the draft, verified the three package SHA-256 values, tested both
  ZIP archives, and confirmed the MSI is a WiX 5.0.2 x64 installation database.
- Changed the verified draft to a non-draft Release v1.0.0 with explicit repository context; the
  Release remained accessible only to repository readers because repository visibility was private.
- Fixed future publication commands to pass `--repo "$GITHUB_REPOSITORY"` and changed Windows
  checksum writers to emit LF endings for cross-platform verification.
- Follow-up validation passed workflow YAML parsing, Ruff lint/format, mypy across 22 source
  files, and all 241 tests after applying the recorded ENV-001 macOS workaround.
- Completed TASK-029 and retained TD-007/TD-008 as transparent platform-trust limitations.
- Preserved the unrelated untracked `README 2.md` file without modification.
