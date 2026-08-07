<!--
Purpose:        Track currently in-progress tasks
Owner:          Implementer / Planner
Update Trigger: Task started, completed, or blocked
Harness Version: 1.1
-->

# Active Tasks — Benford Lens

_Last updated: 2026-08-07_

## In Progress

| ID | Task | Owner | Started | Due |
|----|------|-------|---------|-----|
| TASK-029 | v1.0 release preparation and publication | Release Manager / Tester | 2026-08-07 | — |

### TASK-029: v1.0 release preparation and publication
- **Owner**: Release Manager / Tester
- **Priority**: High
- **Milestone**: M3 / v1.0
- **Description**: Synchronize v1.0 metadata, build the macOS arm64 app, sign and notarize it,
  then tag and publish the verified ZIP through GitHub Releases.
- **Definition of Done**:
  - [x] Package, lockfile, README, roadmap, changelog, and project metadata use v1.0.0
  - [x] All quality checks and the v1.0 PyInstaller build pass
  - [ ] The app is signed with Developer ID Application and accepted by Apple notarization
  - [ ] The notarization ticket is stapled and the final ZIP passes clean extraction checks
  - [ ] The release metadata PR is merged to `main`
  - [ ] Annotated `v1.0.0` tag points to the approved `main` commit
  - [ ] GitHub Release contains the notarized ZIP and checksum

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
