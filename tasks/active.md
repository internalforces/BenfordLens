<!--
Purpose:        Track currently in-progress tasks
Owner:          Implementer / Planner
Update Trigger: Task started, completed, or blocked
Harness Version: 1.1
-->

# Active Tasks — Benford Lens

_Last updated: 2026-08-10_

## In Progress

| ID | Task | Owner | Started | Due |
|----|------|-------|---------|-----|
| TASK-029 | v1.0 release preparation and publication | Release Manager / Tester | 2026-08-07 | — |

### TASK-029: v1.0 release preparation and publication
- **Owner**: Release Manager / Tester
- **Priority**: High
- **Milestone**: M3 / v1.0
- **Status**: User approved GitHub Releases as the unsigned distribution path; native PR package
  checks pass, while PR review/merge, tag creation, and final asset publication remain
- **Description**: Synchronize v1.0 metadata, build and smoke-test the Windows x64 ZIP/MSI and
  macOS arm64 ZIP on native GitHub runners, publish checksums and transparent security guidance,
  then tag and publish the verified assets through GitHub Releases.
- **Definition of Done**:
  - [x] Package, lockfile, README, roadmap, changelog, and project metadata use v1.0.0
  - [x] All quality checks and the v1.0 PyInstaller build pass
  - [x] The Windows ZIP/MSI and macOS ZIP pass native release-workflow verification
  - [x] Release notes clearly disclose the unsigned/notarized status and expected OS behavior
  - [x] The release metadata PR is merged to `main`
  - [ ] The release automation PR is reviewed and merged to `main`
  - [ ] Annotated `v1.0.0` tag points to the approved `main` commit
  - [ ] GitHub Release contains Windows ZIP/MSI, macOS ZIP, and matching SHA-256 files

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
