<!--
Purpose:        Evidence and disposition for the private-to-public exposure audit
Owner:          Planner / Security Reviewer
Update Trigger: Public-launch surface or findings change
Harness Version: 1.1
-->

# Public Exposure Audit — 2026-08-11

## Decision

TASK-039 found no critical or high-risk exposure in the Git repository, GitHub conversations,
Actions logs, release metadata, or downloadable release archives. The existing engineering
records are suitable to retain under ADR-017. No Git history rewrite is recommended.

The repository must remain private until TASK-043 is resolved and the final TASK-044 approval is
received. TASK-040 was subsequently completed by the notice-complete PR #17 native builds;
TASK-042 is complete for private-repository controls, with public-only features deliberately left
for immediate post-visibility verification. The existing v1.0.0 packages still do not contain the
complete project-level notice set and must not become the public download. The final visibility
approval must also acknowledge the maintainer display name described below.

GitHub documents that changing a private repository to public exposes the code and Actions history
and logs, permits public forks, publishes activity, and disables push rulesets. Protections must
therefore be verified or reapplied immediately after TASK-044 changes visibility:

- <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility>
- <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches>

## Scope and reproducible evidence

The audit used the fetched `origin/main` state at `1cdf0ea379189132398115d55cedc5d5253799b7`
and the authenticated GitHub repository `internalforces/BenfordLens`. Scans reported locations and
classifications only; they did not print candidate secret values.

| Surface | Inventory | Review result |
|---|---:|---|
| Git commits | 101 | All reachable history inspected; no credential, private-key body, personal absolute path, personal email, sensitive filename, or source-dataset filename finding |
| Reachable path objects | 945 | 443 text blobs content-scanned, 26 binary blobs filename-classified, no blob skipped for size |
| Remote branches | 7 | `main` plus six merged topic branches; every topic tip is an ancestor of `main` and has zero unique commits |
| Tags | 1 | Annotated `v1.0.0`; tag message and target inspected |
| Pull requests | 16 | All merged; no open or closed-unmerged pull request |
| Pull-request conversation records | 20 | 16 title/body records plus four issue comments; no review or inline-review records; no sensitive finding |
| Actions runs | 42 | 41 successful and one failed run; all 115 available log files (3,123,992 bytes) scanned with no sensitive finding |
| Actions artifacts | 0 | No retained artifact remains available |
| Releases | 1 | Non-draft v1.0.0 Release with three packages and three checksum files |
| Tracked files | 145 | All filenames and reachable historical contents covered by the Git scan |
| Engineering records | 49 | 13 `memory/`, 12 `prompts/`, 21 `reports/`, and three `tasks/` files reviewed under ADR-017 |
| Issues | 0 | No issue conversation exists |

The high-confidence content scan covered private-key structures, common provider token formats,
credential assignments, macOS/Linux/Windows user paths, and non-noreply email addresses. It also
classified sensitive filenames, source-data extensions, and generated/binary artifacts. This is
strong audit evidence, not a mathematical proof that no sensitive value exists.

## Git and GitHub findings

### Accepted public metadata

- Commit author metadata contains 84 entries using the `internalforces` display name and 17 using
  the `MyeongGwan Son` display name. All 101 author entries use the same GitHub noreply address.
  The real display name is not treated as confidential by this audit, but it must be explicitly
  visible in the final TASK-044 approval summary so the maintainer can reconsider before exposure.
- Twenty-eight commit messages contain an `anthropic.com` AI co-author trailer. This is tool
  attribution rather than a personal contact address.
- All six topic branches are fully merged into `main`. Their names and older tree states are
  ordinary development evidence, and their reachable contents were already covered by the full
  history scan. They are acceptable to retain publicly.
- All pull-request text and Actions logs were authored or generated within the repository workflow.
  The scan found no credential, private path, or personal-email indicator.

### Preserved engineering evidence

ADR-017 explicitly retains internal engineering evidence. The 49 tracked records under `memory/`,
`tasks/`, `prompts/`, and `reports/` contain design decisions, plans, verification results, and
release evidence. The audit found no secret, personal absolute path, source dataset, or unsuitable
confidential name in their reachable history, so all records remain tracked.

The stale filename `memory/session 2.md` was unsuitable as a current-session sibling. Its content
was preserved and moved to `memory/sessions/2026-08-07-macOS-Packaging.md`; no material record was
deleted. The user-owned `README 2.md` remains untracked and was not read, modified, staged, or
deleted.

## Release findings

All six v1.0.0 assets were downloaded to an isolated temporary directory. Independent SHA-256
comparison confirmed that the macOS ZIP, Windows ZIP, and Windows MSI each match their companion
checksum file and GitHub's asset digest. The initial Windows comparison was case-sensitive; after
normalizing hexadecimal case, both Windows checksums matched.

The macOS ZIP contains 954 members and the Windows ZIP contains 1,262 members. Archive-member and
embedded-byte review found:

- three Matplotlib `mpl-data/sample_data` CSV files in each ZIP; these are upstream library sample
  files, not user or project source data;
- upstream build-path components such as `runner`, `qt`, `Administrator`, and `runneradmin`, but no
  path belonging to the Benford Lens maintainer;
- Qt/OpenSSL private-key format strings without a matching footer and plausible encoded key body;
- public upstream project/author email domains in metadata and license material, plus a few binary
  byte-sequence false positives; and
- no provider-token candidate after the stricter member-level validation.

The audited v1.0.0 packages contain incidental dependency license files (47 matching members in
the macOS ZIP and 30 in the Windows ZIP), but this is not a complete redistribution notice
solution. TD-012 and TASK-040 were resolved after the audit by PR #17 run `31447586711`; TASK-043
still requires the separately versioned v1.0.1 Release to be published and independently
revalidated before any package becomes anonymously downloadable.

## Repository security state

At audit time:

- the repository is private;
- `main` is not protected and no repository ruleset exists;
- Actions are enabled for all actions and workflows;
- full-length Action SHA pinning is not required;
- default workflow token permissions are read-only and workflows cannot approve pull requests;
- dependency alerts, secret scanning, code scanning, and private vulnerability reporting are not
  enabled or not available in the current private-repository state; and
- the repository has no retained Actions artifact.

GitHub states that full commit SHA pinning is the only immutable way to reference an Action, and
that branch protection and rulesets are available to public repositories on GitHub Free:

- <https://docs.github.com/en/actions/reference/security/secure-use>
- <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets>

These items are tracked by TASK-042 and must be rechecked after the visibility change because
GitHub disables push rulesets during a private-to-public transition.

## Finding disposition

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| EXP-001 | Medium | Public packages lack a complete project-level third-party notice set | Resolved for v1.0.1 by TASK-040 and PR #17 native run `31447586711`; TASK-043 publication/revalidation remains |
| EXP-002 | Medium | Repository protections and security features are absent in the private state | Selected Actions, full-SHA enforcement, dependency protection, and no-bypass rulesets now active; public-only controls remain under TD-011 / TASK-042 for immediate post-TASK-044 verification |
| EXP-003 | Low | Seventeen commits expose the maintainer's real display name | Accepted for preparation; surface again immediately before final visibility approval |
| EXP-004 | Low | Packages contain upstream sample CSVs, build paths, and public attribution strings | Accepted third-party content; include in TASK-040 inventory and notices |
| EXP-005 | Low | Stale tracked session filename looked like an accidental duplicate | Resolved by preserving the record under the dated session archive |

No critical or high-risk public-exposure finding remains. No history rewrite, remote-branch
deletion, release deletion, or material-record deletion is recommended.
