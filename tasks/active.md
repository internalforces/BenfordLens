<!--
Purpose:        Track currently in-progress tasks
Owner:          Implementer / Planner
Update Trigger: Task started, completed, or blocked
Harness Version: 1.1
-->

# Active Tasks — Benford Lens

_Last updated: 2026-08-11_

## In Progress

### TASK-040: Add third-party license and attribution coverage to source and binary distributions

- **Owner**: Researcher / Implementer / Release Manager
- **Priority**: High
- **Milestone**: M3 / Public launch
- **Description**: Audit the exact locked runtime and packaged dependency set; add complete
  project-level third-party notices, applicable license texts and attributions; include the notice
  set in source, macOS app, Windows ZIP, and Windows MSI; and document the Qt/PySide6 LGPL/GPL/
  commercial boundary without unsupported legal conclusions.
- **Definition of Done**:
  - [x] The exact locked runtime, packaged dependencies, bundled fonts, native libraries, and
        packaging tools have a verified license/source inventory.
  - [x] Source-level notices contain applicable license texts, copyright notices, source/relinking
        information, and attributions.
  - [x] Packaging configuration includes the notice set in the macOS app, Windows ZIP, and MSI.
  - [x] Automated checks verify notice presence and content without relying on incidental
        PyInstaller license collection.
  - [x] Project metadata, public documentation, and harness records accurately describe the
        redistribution boundary.
  - [ ] After explicit human approval, native Windows/macOS builds verify notice presence and
        GPL-only Qt-module absence in every package.

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
  - [ ] The preparation PR passes standard and explicitly approved native checks and is merged.
  - [x] GitHub allows only GitHub-owned Actions and `astral-sh/setup-uv`.
  - [x] Active server-side rules protect `main` and semantic release tags without bypass.
  - [ ] Full SHA pinning is enforced after the pinned workflow reaches `main`.
  - [ ] Public-only security features are enabled and verified after visibility changes.

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
