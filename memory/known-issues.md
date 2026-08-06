<!--
Purpose:        Track known bugs, technical debt, and temporary workarounds
Owner:          Debugger / Reviewer
Update Trigger: New bug found, issue resolved, new tech debt identified
Harness Version: 1.1
-->

# Known Issues — Benford Lens

_Last updated: 2026-08-06_

## Active Bugs

| ID | Severity | Description | Found | Owner |
|----|----------|-------------|-------|-------|
| ENV-001 | Medium | macOS local env: Recent `.venv`-affecting edits can set macOS hidden flag on native extensions (numpy, pandas, PySide6), causing pytest crashes with faulthandler dump during dynamic library loading. Workaround: `chflags -R nohidden .venv` before running tests. Does not affect Linux CI (ubuntu-latest). | 2026-08-04 | DevEnv |

## Technical Debt

| ID | Description | Impact | Target Resolution |
|----|-------------|--------|-------------------|
| TD-001 | CSV encoding detection uses fixed try-in-order fallback (utf-8-sig → utf-8 → cp949 → euc-kr → latin-1), not real content-based detection | A CP949-encoded file with byte sequences that are also valid UTF-8 could silently mis-decode | Revisit if real user reports occur; consider adding chardet/charset-normalizer if this becomes a problem |
| TD-003 | `packaging/benford-lens-windows.spec` and `packaging/benford-lens-linux.spec` are written but unbuilt and untested — this dev environment is macOS-only with no Windows/Linux build target. The macOS build itself was only smoke-tested headlessly (`QT_QPA_PLATFORM=offscreen`, process starts and survives 5s), not verified interactively (no display in this environment). | Windows/Linux packaging correctness is unverified; macOS interactive behavior of the frozen bundle is unverified | Verify on an actual Windows/Linux machine or add cross-platform PyInstaller build+smoke-test jobs to CI |
| TD-005 | CI does not collect or enforce the 80% coverage standard | Local merge-gate review measured 91% total line coverage, so the standard is currently met, but future regressions are not automatically blocked | Consider approved CI coverage tooling in a later developer-infrastructure task |

## Resolved

| ID | Description | Resolved | Method |
|----|-------------|----------|--------|
| ISS-001 | A failed file load or cancelled Excel sheet selection could change the report source name while leaving the previous analysis active | 2026-08-05 | Assign `_source_path` only after the new dataframe opens; added regression tests for both failure and cancellation |
| TD-002 | `test_summarize_result_uses_neutral_non_accusatory_language` (`tests/charts/test_benford_chart.py`) used a 10-value sample that hit the "too few valid values" branch instead of the "close to expected Benford distribution" branch — no test covered the "close" branch's wording | 2026-08-05 | Added a dedicated test (`test_summarize_result_flags_a_close_match_for_a_large_benford_like_sample`), using powers of 2 (a classic near-Benford sample) at ≥30 values, during the Task 11 final-review sanity pass |
| TD-004 | README and package/project version metadata did not describe the implemented M2 state | 2026-08-05 | Expanded README and synchronized the source version to `0.2.0.dev0` |
| TD-006 | Milestone documentation was inconsistent after the M2 merge | 2026-08-06 | Marked M2 merged in `roadmap.md` and corrected the glossary's second-digit target to M3/v1.0 |
| ISS-002 | Result-summary and HTML-report copy contained a term prohibited by the stricter wording rule in `AGENTS.md` | 2026-08-06 | Replaced it with neutral guidance focused on interpreting data characteristics; synchronized UI/report tests and regenerated KO/ZH/JA `.qm` catalogs |

## Issue Template

```
### ISS-XXX: [Title]
- **Severity**: Critical | High | Medium | Low
- **Found**: YYYY-MM-DD
- **Reproduction steps**:
- **Root cause**:
- **Workaround**:
- **Permanent fix direction**:
```
