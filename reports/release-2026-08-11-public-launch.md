# Public Launch Verification — TASK-044

_Verified: 2026-08-11_

## Approval and visibility

Immediately before the visibility change, the final exposure summary disclosed the retained Git
history, branches, tags, pull requests, Actions history, tracked engineering records, 17 commits
with the maintainer's real display name, 28 AI co-author trailers, and the unsigned-package trust
boundaries. The user explicitly approved TASK-044 after that disclosure.

`internalforces/BenfordLens` was then changed from private to public. The anonymous repository API
and repository page both report public visibility with `main` as the default branch.

## Anonymous access verification

Unauthenticated HTTP requests returned success for the repository, branch list, pull-request list,
Actions history, tag list, latest Release API, repository page, v1.0.1 tag page, v1.0.1 Release
page, Actions page, both README files, the CI badge, and all three README visual assets.

The anonymous API exposed:

- nine branches, including `main` and the open Dependabot branch;
- 20 pull requests, with Dependabot PR #18 open at verification time;
- 71 Actions runs;
- all eight repository topics; and
- v1.0.1 as the latest non-draft Release with exactly six assets.

All six v1.0.1 assets were downloaded through their public Release URLs without maintainer
credentials. The three package/checksum pairs matched after normalizing the uppercase Windows
checksum text:

| Package | SHA-256 |
|---|---|
| `Benford-Lens-1.0.1-macOS-arm64.zip` | `a19383e48ff4230fe94255083b3a66a2ae3c2611805a5e92a898ddb880d92d84` |
| `Benford-Lens-1.0.1-windows-x64.msi` | `e2986f8de4d05c4880168de17efb8363570142be72bfafef012606fe072921d5` |
| `Benford-Lens-1.0.1-windows-x64.zip` | `c844e4ded0c2728ba2dea22dbb0a5ea017773aace792800d4bb3973609f35ed3` |

Both ZIP integrity tests passed. The MSI was identified as an x64 WiX Toolset 5.0.2 installation
database. v1.0.0 remains a draft with its tag and six retained assets unchanged.

## Post-transition protections

The visibility transition preserved and the API re-read confirmed:

- active `Protect main` ruleset ID `20656284`, requiring a pull request, current
  `lint-type-test`, resolved review conversations, and blocking deletion/non-fast-forward updates,
  with no bypass actor;
- active `Protect release tags` ruleset ID `20656289`, blocking semantic release-tag deletion and
  non-fast-forward updates, with no bypass actor;
- Actions limited to GitHub-owned Actions and `astral-sh/setup-uv@*`;
- repository-wide full-SHA Action pinning;
- read-only default workflow permissions and no workflow permission to approve pull requests;
- enabled Dependabot security updates, vulnerability alerts, and automated security fixes, with
  no alerts at verification time; and
- the existing required `lint-type-test` CI context on `main`.

## Public-only security controls

Secret scanning and push protection were enabled after the transition. The initial secret-scanning
alert list was empty. Private vulnerability reporting was enabled, and Dependabot automated
security fixes remain active. GitHub left the optional non-provider-pattern and validity-check
extensions disabled; they are not part of the TASK-044 completion gate.

The repository's pinned advanced CodeQL workflow is present on `main`. Its first public analysis
is intentionally triggered by the protected evidence pull request for this record; TASK-042 and
TASK-044 remain open until that run succeeds and the final result is recorded here.

## Retained distribution boundaries

- The macOS package targets Apple Silicon, is ad-hoc signed, and is not Developer ID signed or
  notarized.
- The Windows ZIP and MSI are not Authenticode signed.
- Gatekeeper, SmartScreen, Smart App Control, or managed device policy may warn or block these
  packages even though their integrity and native smoke checks passed.
- The installed application remains local-only and does not upload user data.
