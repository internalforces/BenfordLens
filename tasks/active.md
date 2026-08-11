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

### TASK-044: Change repository visibility and run the post-launch verification gate

- **Owner**: Release Manager / Security Reviewer / Tester
- **Priority**: High
- **Milestone**: M3 / Public launch
- **Description**: With a separate final human approval, change `internalforces/BenfordLens` from
  private to public, immediately restore or verify protections affected by the transition, enable
  public-only security controls, and prove anonymous source and release access.
- **Definition of Done**:
  - [ ] The final exposure summary is presented and explicit human approval is obtained
        immediately before the visibility change.
  - [ ] Repository visibility is changed to public only after that approval.
  - [ ] Anonymous access to source, the v1.0.1 tag, Release notes, all six assets, and checksum
        validation is verified without maintainer credentials.
  - [ ] The `main` and semantic release-tag rulesets, selected-Action allowlist, full-SHA policy,
        dependency protections, and required CI are re-read or reapplied after the transition.
  - [ ] Secret scanning, push protection, private vulnerability reporting, and CodeQL are enabled
        and verified where GitHub makes them available to the public repository.
  - [ ] README badges/links, topics, branches, pull requests, Actions history, and the latest
        release render correctly to an anonymous visitor.

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
