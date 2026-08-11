<!--
Purpose:        Track currently in-progress tasks
Owner:          Implementer / Planner
Update Trigger: Task started, completed, or blocked
Harness Version: 1.1
-->

# Active Tasks — Benford Lens

_Last updated: 2026-08-11_

## In Progress

### TASK-042: Harden GitHub Actions and default-branch governance

- **Owner**: Security Reviewer / Release Manager
- **Priority**: High
- **Milestone**: M3 / Public launch
- **Description**: Pin external automation identities, minimize token permissions, monitor
  dependency updates, define workflow ownership, and enforce merge/release-ref protections before
  accepting public contributions.
- **Definition of Done**:
  - [x] Every external Action uses a full commit SHA and uv uses an exact version.
  - [x] Native build jobs are read-only; only the successful tag publisher can write Releases.
  - [x] Dependabot covers uv and Actions; CODEOWNERS covers release/supply-chain paths.
  - [x] Public-only CodeQL and importable tested `main`/release-tag rulesets exist.
  - [x] The preparation PR passes standard and explicitly approved native checks and is merged.
  - [x] GitHub allows only GitHub-owned Actions and `astral-sh/setup-uv`.
  - [x] Active server-side rules protect `main` and semantic release tags without bypass.
  - [x] Full SHA pinning is enforced after the pinned workflow reaches `main`.
  - [ ] Public-only security features are enabled and verified after visibility changes.

### TASK-043: Revalidate the release that will become publicly downloadable

- **Owner**: Release Manager / Security Reviewer / Tester
- **Priority**: High
- **Milestone**: M3 / Public launch
- **Description**: Publish a separately versioned v1.0.1 from an exact reviewed `main` tag so the
  notice-complete package set, rather than the older v1.0.0 package set, becomes the public
  download. Preserve immutable provenance and verify every release artifact independently.
- **Definition of Done**:
  - [x] v1.0.1 is selected instead of silently replacing established v1.0.0 assets.
  - [ ] Explicit human approval is obtained immediately before the tag-triggered native builds,
        Release publication, and v1.0.0 draft transition.
  - [ ] An annotated v1.0.1 tag targets the exact reviewed `main` merge commit.
  - [ ] Native GitHub-hosted macOS and Windows jobs pass metadata, architecture, notice,
        denylist, extraction/startup, and MSI install/startup/uninstall checks.
  - [ ] The v1.0.1 Release contains exactly three packages plus their three SHA-256 files and
        retains complete platform trust and support disclosures.
  - [ ] v1.0.0 is returned to draft without deleting or overwriting its tag or assets.
  - [ ] Every v1.0.1 asset is re-downloaded and independently verified before TASK-044 approval.

## Task Detail Template

```
### TASK-XXX: [Title]
- **Owner**: [Agent Role]
- **Priority**: High | Medium | Low
- **Milestone**: M[N]
- **Description**:
- **Definition of Done**:
  - [ ] [Condition 1]
  - [ ] [Condition 2]
```
