# M3 Core Review

**Date:** 2026-08-06
**Branch:** `codex/m3-core`
**Scope:** TASK-018–026 against `main` at PR #5 merge commit `a62d9dc`

## Verdict

**Approved** — no blocking findings.

## Review Summary

- Existing first-digit analysis and compatibility wrappers remain available.
- Second-digit and combined analysis use shared extraction and preserve explicit user control
  over the file, column, preprocessing options, and analysis mode.
- One frozen controller snapshot supplies charts, statistics, drill-down, and report export;
  source/column/options/mode changes invalidate it as a unit.
- Drill-down returns original source rows from stored mappings. The application does not write
  to the source CSV/XLSX file.
- Combined mode displays both distributions simultaneously, calculates per-position MAD and
  Chi-square, and presents the sample-level log-mantissa KS result once.
- First, second, and combined HTML reports render from the exact snapshot and keep shared
  preprocessing/suitability/KS context single.
- Result/report wording and all seven UI languages remain neutral and exploratory. Restricted
  wording searches return no product-source matches.
- KO/ZH/JA/ES/FR/RU catalogs each contain the same 93 messages, have no empty translations, and
  preserve every formatting placeholder. All six `.qm` files compile and are included by the
  existing packaging resource-directory rule.
- No network call, credential flow, new file format, source-file mutation, or new dependency
  was introduced.
- The measured repeated-extraction bottleneck was removed; 100k-row controller medians improved
  30.0–31.8% without changing the existing first-digit public API.

## Verification

- Ruff lint: pass
- Ruff format check: pass
- mypy (`src/`): pass
- pytest: 229 passed
- Line coverage: 95.00% (1,578 / 1,661 executable lines), including TASK-026
- `git diff --check`: pass
- Translation compilation: 93 finished, 0 unfinished for Spanish, French, and Russian

## Existing Non-Blocking Context

- TD-003 remains: Windows/Linux PyInstaller specs have not been built on their target operating
  systems. The translation files use the already-tested whole-directory resource inclusion, so
  M3 does not add a new packaging mechanism.
- TD-005 remains: CI does not yet enforce the 80% coverage threshold automatically.
