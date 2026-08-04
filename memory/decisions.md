<!--
Purpose:        Key technical decision history in ADR format
Owner:          Architect / Researcher
Update Trigger: Record immediately after any significant technical decision
Harness Version: 1.1
-->

# Decision Log — Benford Lens

_Last updated: 2026-08-04_

## Template

```
### ADR-NNN: [Decision Title]
- **Date**: YYYY-MM-DD
- **Status**: Proposed | Accepted | Deprecated | Superseded
- **Decided by**: [Role / User]

**Context**: Why was this decision needed?
**Decision**: What was chosen?
**Rationale**: Why was this chosen?
**Trade-offs**: What are the downsides?
**Consequences**: What changed as a result?
```

---

### ADR-001: AI Development Harness v1.1 Adoption

- **Date**: 2026-08-04
- **Status**: Accepted
- **Decided by**: User

**Context**: Consistent context delivery and task tracking were needed for AI-assisted development on a project with strict local-first / privacy constraints that must be enforced consistently across agents and sessions.
**Decision**: Adopt AI Development Harness v1.1 (Standard tier) to structure agent roles, workflows, and memory, generated from the Benford Lens PRD.
**Rationale**: Eliminates context loss between sessions; structures multi-agent collaboration; encodes the project's tone and privacy rules (AGENTS.md) so they survive across every future session.
**Trade-offs**: Upfront documentation cost; the Harness must be kept in sync with the PRD as scope evolves.
**Consequences**: All agents operate from a shared, consistent context, including the non-negotiable local-first and tone constraints.

---

### ADR-002: Package Manager — uv

- **Date**: 2026-08-04
- **Status**: Accepted
- **Decided by**: User

**Context**: Needed a Python dependency/environment manager for a new project.
**Decision**: Use `uv` for dependency management and virtual environments.
**Rationale**: Fast, modern tooling with a single command surface for install/run/sync.
**Trade-offs**: Newer tool than pip/Poetry; smaller (but growing) ecosystem familiarity.
**Consequences**: `commands.md` and CI workflows are written against `uv`.

---

### ADR-003: CI/CD — GitHub Actions

- **Date**: 2026-08-04
- **Status**: Accepted
- **Decided by**: User

**Context**: Benford Lens is an open-source project; needed a CI approach for lint/test/build automation.
**Decision**: Use GitHub Actions for lint, type-check, test, and PyInstaller build-verification workflows.
**Rationale**: Standard default for open-source GitHub repositories; no additional infra to manage.
**Trade-offs**: Ties CI specifically to GitHub as the hosting platform.
**Consequences**: A CI workflow file will be added under `.github/workflows/` once the codebase exists.
