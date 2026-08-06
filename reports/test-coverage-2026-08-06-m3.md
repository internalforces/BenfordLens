# M3 Test and Coverage Report

**Date:** 2026-08-06
**Branch:** `codex/m3-core`

## Result

- Tests: **229 passed**
- Executable source lines: **1,661**
- Executed source lines: **1,578**
- Aggregate line coverage: **95.00%**
- Required minimum: **80%** — met

## Method

The full pytest suite ran under Python 3.11's standard-library `trace` counter with
`QT_QPA_PLATFORM=offscreen`. Executable lines were identified for every Python file under
`src/`; executed source lines were divided by total executable source lines. This avoids adding
an unapproved coverage dependency. The ordinary untraced suite was also run independently.

## M3 Coverage Added

- Second significant-digit boundary extraction and expected 0–9 probabilities
- First/second compatibility and one-pass combined analysis
- Position-generic MAD and Chi-square plus one shared log-mantissa KS result
- All three controller modes, single preprocessing, single digit extraction, frozen snapshot
  invalidation, and position-aware original-row drill-down
- Generic 0–9 charts, reusable result panels, single/combined layouts, and shared KS UI
- First, second, and combined HTML reports from the exact snapshot
- Complete KO/ZH/JA/ES/FR/RU catalogs for all 93 current messages, including mode, result,
  chart, and combined-statistics strings
- Catalog parity, non-empty translation, placeholder-preservation, compiled-resource, and
  live Spanish/French/Russian UI-switching regression tests
- 100,000-row performance-path regression checks through explicit extraction-count tests

## Quality Gates

- Ruff lint: pass
- Ruff format check: pass
- mypy on `src/`: pass
- New dependency: none
