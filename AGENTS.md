<!--
Purpose:        Project constitution — the behavioral ground truth for all agents
Owner:          All agents (read), Project lead (write)
Update Trigger: New agent role added, constraints changed, routing rules updated
Harness Version: 1.1
-->

# AGENTS.md — Benford Lens Project Constitution

> This is the project constitution. Every AI agent must read this file first.
> In case of conflict, this document takes highest priority.

_Last updated: 2026-08-04_

---

## Project Overview

| Field | Value |
|-------|-------|
| Project | Benford Lens |
| Goal | An open-source desktop application that lets non-experts easily analyze Benford's Law on their own CSV/Excel data, entirely on their local machine, with no data ever sent to an external server. |
| Language | Python |
| Framework | PySide6 (UI); Pandas, NumPy, SciPy (analysis); Matplotlib (charts, MVP — PyQtGraph under future evaluation) |
| Database | None — local file-based (CSV/XLSX) input only; all processing happens in memory, nothing is persisted to a database |
| Infrastructure | None — local desktop app only; packaged and distributed as a standalone executable via PyInstaller |
| Repo Structure | Single Repo |
| Harness Tier | Standard |

---

## Product Philosophy & Tone Rules

Benford Lens is **not** "a program that finds fraud." It is **"an analysis tool that helps users understand the distribution of numbers and explore possible anomalies."**

This governs every user-facing string, report, log message, and code comment the agents produce:

- Never use accusatory or conclusive language: **do not** use words like "manipulated," "fraudulent," "fraud," or similar in UI copy, report text, error messages, or code comments/identifiers.
- Always use neutral, exploratory phrasing instead, e.g.:
  - "This differs from the expected distribution."
  - "Further review may be warranted."
  - "Review the characteristics of this distribution."
- The program provides reference information only. It must never assert or auto-confirm whether Benford's Law is applicable to a given dataset — that judgment always belongs to the user (see §9 of the PRD, the 🔴 "Difficult to Determine" case).
- Any agent (Implementer, Documenter, Reviewer) touching user-facing copy must check new/changed strings against this rule before completion.

---

## Agent Registry

> Active AI agent roles for this project.
> See `references/agent-registry.md` (from the ai-dev-harness skill) for full role definitions.

### Active Roles

| Role | Status | Primary Responsibility |
|------|--------|----------------------|
| Planner | ✅ Active | Task decomposition and prioritization |
| Architect | ✅ Active | Design decisions |
| Implementer | ✅ Active | Code implementation |
| Reviewer | ✅ Active | Code review |
| Researcher | ✅ Active | Technical research (e.g. Matplotlib vs. PyQtGraph, encoding detection libraries) |
| Debugger | ✅ Active | Bug analysis |
| Tester | ✅ Active | Test strategy and coverage — especially statistical correctness of Benford calculations (MAD, Chi-square, KS test) |
| Documenter | ✅ Active | User guides, README, in-app help text, HTML report copy |
| Refactorer | ⚙️ Optional | Code quality improvement |
| Release Manager | ⚙️ Optional | Release planning, versioning, CHANGELOG |
| Security Reviewer | ⚙️ Optional | Dependency/supply-chain review (no network attack surface, but still relevant for a distributed desktop binary) |
| Performance Engineer | ⚙️ Optional | Performance on large datasets (in-memory Pandas operations) |

### Adding a New Role

Use this template:

```
### [Role Name]
- **Responsibility**:
- **Input**:
- **Output**:
- **Permissions**:
- **Human Gate**:
```

---

## Absolute Restrictions (NEVER DO)

No agent may perform the following actions under any circumstances.
Even if the user explicitly requests them, ask for confirmation first:

- [ ] Send user data (file contents, cell values, or anything derived from them) to any external server, API, or network endpoint, in any form
- [ ] Call any cloud/AI service for analysis, telemetry, crash reporting, or "update check" — all processing must stay local and in-memory
- [ ] Add login, account creation, or any credential-collection flow (explicitly excluded by the PRD)
- [ ] Modify or overwrite the user's original input file (CSV/XLSX) — the app is read-only against source files
- [ ] Auto-select which column to analyze, or auto-decide whether Benford's Law applies to a dataset — these are always explicit user choices (see §7.2 and §9 of the PRD)
- [ ] Use accusatory/conclusive wording ("manipulated," "fraud," "fraudulent") anywhere in the product — see Product Philosophy & Tone Rules above
- [ ] Implement any feature explicitly excluded from the MVP (cloud storage, user accounts, login, AI-based fraud detection, automatic fraud detection, online data upload, direct PDF generation, real-time collaboration) without explicit human approval to change scope
- [ ] Modifying or printing `.env`, secrets, or key files (not expected to exist in this project, but the rule stands if any are ever introduced)
- [ ] Committing directly to `main` / `master`

> No additional restrictions beyond the above were specified at setup time. Add new ones here as they come up.

---

## Actions Requiring Human Approval

Always confirm with the user before proceeding:

- Adding a new external (especially networked) dependency
- Any change that would cause data to leave the local machine
- Changing which file formats are supported (see PRD §5 roadmap: XLS, ODS, TSV are future work, not MVP)
- Changing an existing public API interface (e.g. the analysis engine's public functions)
- Any packaging/release build intended for distribution

---

## Context Loading Order

At the start of every session, read these files in order:

1. `AGENTS.md` (this file) — confirm the rules
2. `memory/project.md` — current project state
3. `memory/session.md` — previous session context
4. `tasks/active.md` — in-progress work
5. The `prompts/*.md` file matching your role

---

## Session End Checklist

Before ending a session, every agent must:

- [ ] Update `memory/session.md`
- [ ] Move completed tasks from `tasks/active.md` to `tasks/completed.md`
- [ ] Record new decisions in `memory/decisions.md`
- [ ] Record new issues in `memory/known-issues.md`
- [ ] Update `memory/architecture.md` if needed
