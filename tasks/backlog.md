<!--
Purpose:        Prioritized list of tasks not yet started
Owner:          Planner
Update Trigger: New task added, priority changed, milestone adjusted
Harness Version: 1.1
-->

# Backlog — Benford Lens

_Last updated: 2026-08-05_

| ID | Task | Priority | Milestone | Size | Notes |
|----|------|----------|-----------|------|-------|
| — | (none) | — | — | — | — |

## TASK-014 Review Record — Completed

TASK-014 is archived in `tasks/completed.md`. This record is retained here as reference for
future UI polish; ADR-007 documents which mockup details were adopted or deferred.

**Source**: A single screenshot shared by the user, described as a "simple UI demo version" (목업). No source code or working prototype exists behind it — it's a visual reference only.

**Confirms existing design**: The mockup's tab layout (분석 결과 / 데이터 적합성 검사 / 전처리 미리보기 / 보고서) matches the planned Results / Suitability / Preprocessing-preview / Report views in `memory/architecture.md` and TASK-007/008/010. No scope change.

**New details to fold into implementation** (not currently captured in the docs):
- **Column selector (TASK-004)**: table has 열 이름 / 타입 (날짜, 문자, 숫자) / 적합성 (적합/주의/부적합) columns — a per-column advisory hint shown alongside manual selection (distinct from the dataset-level 🟢/🟡/🔴 suitability check in TASK-008; this one flags individual columns like ID/code columns as 부적합 before the user even picks one).
- **Preprocessing options (TASK-007)**: mockup shows concrete default choices worth using as a starting point — 음수 처리: 절댓값으로 변환, 0 처리: 제외, 소수 처리: 그대로 사용, 빈 값 처리: 제외, 문자열→숫자 자동 변환 (예: "1,200원", "$100"), 중복값 처리: 유지.
- **Result summary tone (TASK-006 / Documenter)**: mockup's summary text is a good AGENTS.md-compliant example to reuse as a style reference: "전체 분포는 벤포드 기대 분포와 다소 차이가 있습니다... 이 결과만으로 데이터 오류나 조작을 판단할 수 없습니다." — neutral, exploratory, no accusatory language.
- **Drill-down table (TASK-009)**: mockup adds a CSV export button, a search box, and a filter icon on top of the filtered raw-row table.
- **Local-first trust signal**: mockup's top bar shows a lock icon + "모든 분석은 로컬에서 수행됩니다" — worth keeping somewhere persistent in the shell as a standing reassurance, not just in docs/marketing copy.

**Open discrepancies — resolved via ADR-004 (`memory/decisions.md`)**:
1. Expert statistics panel (MAD, Chi-square, KS Test, sample size): stays **hidden by default**, confirming the original design in `memory/architecture.md` and TASK-011. The mockup's always-visible "주요 통계" block is not adopted as-is.
2. MVP default UI language: **English**, with a language selector scoped through M2 to English/Korean/Chinese/Japanese (tracked in TASK-015). The mockup's Korean UI becomes a selectable option, not the default.

## Size Reference

| Size | Estimated Effort |
|------|-----------------|
| XS | Under 1 hour |
| S | 1–4 hours |
| M | Half day to full day |
| L | 1–3 days |
| XL | 3+ days → must be decomposed |
