<!--
Purpose:        Agent collaboration sequences and Human Approval Gates
Owner:          Architect / Planner
Update Trigger: New workflow added, roles changed, approval policy updated
Harness Version: 1.1
-->

# ORCHESTRATOR.md — Benford Lens Workflow Playbooks

_Last updated: 2026-08-04_

---

## Feature Workflow

```
[Planner]   Decompose feature → add to tasks/backlog.md
    ↓
[Architect] Design (for complex features only, e.g. new preprocessing step, new suitability metric)
    ↓ ⚠️ HUMAN APPROVAL if new dependency, new file format support, or any change touching data egress
[Implementer] Implement
    ↓
[Tester]    Write/extend tests, especially for statistical correctness (MAD, Chi-square, KS test, digit-frequency math)
    ↓
[Reviewer]  Code review → save to reports/ (includes a Tone Rules check per AGENTS.md)
    ↓ ⚠️ HUMAN APPROVAL before merge
```

## BugFix Workflow

```
[Debugger]    Reproduce → root cause → register in known-issues.md
    ↓
[Implementer] Fix
    ↓
[Tester]      Add regression test
    ↓
[Reviewer]    Review
    ↓ ⚠️ HUMAN APPROVAL before release build
```

## Research Workflow

```
[Researcher]  Research (e.g. Matplotlib vs. PyQtGraph, CSV encoding detection, Excel sheet parsing edge cases) → reports/research-*.md
    ↓
[Architect]   Decision → memory/decisions.md (ADR)
    ↓
[Planner]     Convert to tasks if needed
```

## Documentation Workflow

```
[Documenter]  Draft/update user guide, README, in-app help text, or HTML report copy
    ↓          (must comply with Product Philosophy & Tone Rules in AGENTS.md)
[Reviewer]    Review for accuracy and tone compliance
```

## Release Workflow

```
[Reviewer]    Final review → write CHANGELOG
    ↓
[Architect]   Confirm impact → update memory/architecture.md
    ↓ ⚠️ HUMAN APPROVAL for release tag and PyInstaller build distribution
After release: update memory/project.md version, clean up tasks/completed.md
```

---

## Human Approval Gates Summary

| Situation | Reason |
|-----------|--------|
| New external dependency | Security, license, and "does it phone home" review |
| Any code path that could send data off the local machine | Violates the 100% Local-First core value |
| New supported file format (e.g. XLS, ODS, TSV) | Scope change beyond MVP (PRD §5) |
| Any MVP-excluded feature (accounts, login, cloud storage, AI-based fraud detection, PDF export, real-time collab) | Explicit scope boundary (PRD §17) |
| Public API interface change (analysis engine functions) | Backward compatibility impact |
| Release build / distribution | Final responsibility stays with humans |
