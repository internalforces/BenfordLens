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

---

### ADR-004: UI Language Defaults & i18n Scope

- **Date**: 2026-08-04
- **Status**: Accepted
- **Decided by**: User

**Context**: A UI mockup review (TASK-014) surfaced two open questions: (1) whether the expert
statistics panel should be hidden by default, and (2) what the MVP default UI language is,
since the mockup was entirely in Korean but `roadmap.md` only listed "multi-language (i18n)
support" as M3 scope with no stated default.

**Decision**:
1. The expert statistics panel (MAD, Chi-square, KS Test, sample size, deviation) stays
   **hidden by default**, confirming the existing design in `memory/architecture.md` and
   TASK-011. No change from the original PRD reading.
2. Default UI language is **English**. A language selector is added, scoped through M2 to
   exactly 4 languages: English (default), Korean, Chinese, Japanese. This moves basic i18n
   scaffolding up from M3 into M2 (M3 remains available for expanding beyond this set).

**Rationale**: Keeping expert stats hidden by default matches the PRD's original intent of a
plain-language-first results view. English-default with a constrained 4-language set gives
the mockup's Korean UI a home (as a selectable option, not the default) without committing to
open-ended i18n scope this early.

**Trade-offs**: Language selection + string externalization work now lands in M2 instead of
M3, adding scope to that milestone (translation maintenance for 3 non-default languages).

**Consequences**:
- `roadmap.md` M2 gains a UI language selection item; M3's multi-language item is narrowed to
  "beyond the initial 4-language set."
- Recommended implementation approach: PySide6/Qt's built-in translation system (`QTranslator`
  + `.ts`/`.qm` files via `pyside6-lupdate`/`pyside6-lrelease`) — no new external dependency,
  since PySide6 is already an approved dependency. See `tech-stack.md`.
- New backlog item TASK-015 tracks the i18n scaffolding + language selector work.

---

### ADR-005: Pin Dev Environment to Python 3.11

- **Date**: 2026-08-04
- **Status**: Accepted
- **Decided by**: Implementer (subagent-driven-development, M1), controller-diagnosed

**Context**: While implementing TASK-005/006 (analysis engine, chart), `uv run mypy src/` started failing with `Type statement is only supported in Python 3.12 and greater` inside numpy's bundled `__init__.pyi` type stub. Root cause: the dev `.venv` had no pinned interpreter, so `uv sync` picked up the newest available Python (3.13) and resolved a numpy build whose stub unconditionally uses PEP 695 `type X = ...` syntax — which `mypy` refuses to parse when its `python_version` target is `"3.11"` (the project's documented floor, unchanged from `tech-stack.md`/`requires-python = ">=3.11"`). Downgrading numpy was tried and ruled out: no numpy version with a working `cp313` wheel avoided the issue, and older numpy has no `cp313` wheel at all (fails building from source in this environment).

**Decision**: Pin the project's dev interpreter to Python 3.11 via a committed `.python-version` file (`uv python pin 3.11`), matching `requires-python` and matching what CI (TASK-012, `.github/workflows/ci.yml`) already runs (`uv python install 3.11`).

**Rationale**: Under a real Python 3.11 venv, `uv` resolves a numpy build whose stub parses cleanly at mypy's `python_version = "3.11"` target — verified directly, zero errors. This required no change to `pyproject.toml`, no numpy version pin, and no relaxation of the project's stated Python floor. It also closes a latent local/CI drift risk (a contributor's unpinned local venv silently running a newer Python than CI checks against).

**Trade-offs**: None identified — this only makes local dev match the project's own stated minimum version and CI's actual runtime; it doesn't narrow or widen supported Python versions.

**Consequences**: `.python-version` (containing `3.11`) is now a tracked repo file. Contributors running `uv sync` from a fresh checkout get a Python 3.11 venv automatically. No other config changed.
