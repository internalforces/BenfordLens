<!--
Purpose:        Archived session handoff for TASK-011
Owner:          All agents (read)
Update Trigger: None — historical record
Harness Version: 1.1
-->

# Session Archive — TASK-011 Expert Statistics

## Session Info

- **Date**: 2026-08-05
- **Agent Role**: Implementer / Tester
- **Session Goal**: Complete TASK-011 on `codex/task-011-expert-statistics`: add the
  user-approved SciPy dependency, statistically explicit MAD/Chi-square/KS calculations,
  and a hidden-by-default expert details panel.

## Previous Session Summary

The previous session completed and merged M2 plus its merge-gate follow-up into `main` through
PRs #2 and #3. The post-merge audit confirmed 152 tests and all static checks passed. TASK-011
remained the next candidate only until the user approved SciPy in this session.

## TASK-011 Work

- [x] Create `codex/task-011-expert-statistics` without committing directly to `main`
- [x] Add and lock the user-approved SciPy runtime dependency
- [x] Implement and unit-test MAD, Chi-square, and continuous log-mantissa KS calculations
- [x] Snapshot expert statistics from the same preprocessed series used by the chart
- [x] Add the hidden-by-default expert panel and analysis-invalidation behavior
- [x] Add and compile Korean/Chinese/Japanese translations
- [x] Verify 162 tests, Ruff, mypy, and 95.19% traced line coverage
- [x] Commit and push `cb266e4`; open draft PR #4 against `main`

## Retained M2 Implementation History

- [x] Create `feature/m2-phase2` from `main` in an isolated worktree
- [x] Write `reports/development/plans/2026-08-05-m2-phase2.md`
- [x] Execute all 11 implementation-plan tasks
- [x] Complete the final whole-branch sanity pass and coverage-gap fixes
- [x] Confirm 150 tests plus Ruff and mypy during the implementation-status audit
- [x] Complete the separate M2 review with an Approved verdict
- [x] Merge M2 PR #2 and the merge-gate follow-up PR #3
- [x] Complete the post-merge audit on `main`: 152 tests and all static checks passed

## Completed

- [x] Added the PySide6-free expert statistics engine and default-collapsed panel
- [x] Added deterministic calculation, controller, panel, integration, invalidation, and i18n
  tests; full suite reached 162 passing tests
- [x] Recorded the methodology as ADR-008 and the dependency approval in `dependencies.md`
- [x] Added `reports/test-coverage-2026-08-05.md`; TASK-011 engine and panel both measured 100%
  and total traced line coverage measured 95.19%
- [x] Preserved completed M2 TASK-007/008/009/010/013/015 records and roadmap status

## Issues and Decisions

- **ADR-008**: MAD and Chi-square operate on the nine first-digit buckets; KS operates on the
  continuous fractional parts of `log10(abs(value))`. No threshold, verdict, or automatic
  applicability decision is produced.
- **SciPy approval**: the user explicitly approved SciPy for TASK-011. All calculations remain
  local and in memory.
- **ENV-001**: the macOS hidden-file flag recurred in the fresh `.venv` and was handled with
  the documented workaround before successful verification.
- **ADR-006**: retained the advisory data-characteristic thresholds from M2.
- **TD-003**: Windows/Linux packaging specifications remained unverified on target platforms.
- **Stale chart/drill-down mismatch**: resolved by clearing analysis UI when the column or
  preprocessing options change, with regression tests.
- **TD-002**: resolved the missing close-distribution summary branch test using a sufficiently
  large powers-of-two sample.
- **Suitability branch coverage**: added negative-rate and missing-rate caution-note tests.
- **ISS-001**: fixed report source state after failed or cancelled file changes.
- **TD-004**: synchronized README and version metadata to `0.2.0.dev0`.
- **TD-005**: CI still did not enforce the documented 80% coverage threshold.
- **TD-006**: recorded that the roadmap and glossary needed post-M2 merge cleanup.
- An older untracked suitability-panel copy was treated as user-owned and excluded from PRs.

## Handoff

1. Review PR #4 and confirm the merge result.
2. Synchronize local `main` after merge.
3. Archive this session, fix TD-006, and begin M3 design.

TASK-011 was implemented, tested, documented, and ready for review. The analysis engine
remained UI-independent, and the panel remained hidden until the user explicitly expanded it.
