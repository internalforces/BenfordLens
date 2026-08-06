# Review — TASK-011 Post-Merge (PR #4)

- **Date**: 2026-08-06
- **Scope**: PR #4, merged as `fd1fa98` into `main`
- **Verdict**: Approved

## Summary

PR #4 correctly adds local SciPy-backed reference statistics, snapshots them from the same
preprocessed series as the first-digit result, and presents them in a disabled and collapsed
panel until analysis is run. The change preserves manual column selection, produces no
automatic applicability judgment, introduces no network path, and does not write to source
files.

No blocking defect was found in the merged diff.

## Verification

- GitHub CI `lint-type-test`: passed before merge
- Ruff lint: passed
- Ruff format check: passed (43 files)
- mypy: passed (21 source files)
- pytest: 162 passed
- Recorded traced line coverage: 95.19%; both TASK-011 modules 100%
- Product-code network-call scan: no matches
- PR-added product-copy review: neutral and advisory
- SciPy approval and local-only use: recorded in `dependencies.md`

## Review Notes

- MAD and Chi-square use the nine first-digit buckets and normalize expected counts to the
  observed total.
- KS uses fractional base-10 log mantissas rather than applying a continuous KS p-value to
  discrete digit buckets.
- Empty samples return explicit `None` values, rendered as an em dash, instead of exposing
  undefined numeric output.
- Controller state, UI invalidation, language refresh, and tests cover the new panel lifecycle.
- The current fixed first-digit boundaries in the engine, chart, drill-down, expert details,
  and report are a planned M3 refactor concern, not a TASK-011 regression. ADR-009 and the M3
  design spec define the compatibility-preserving extraction points.

## Residual Items

- ENV-001: the documented macOS hidden-file flag workaround remains necessary in some local
  environments.
- TD-003: Windows/Linux packaging still needs target-platform verification.
- TD-005: CI still does not enforce the project's coverage threshold.
- ISS-002: a pre-existing restricted term remains in current result/report copy and should be
  replaced in a focused copy-only change. PR #4 did not introduce that wording.
