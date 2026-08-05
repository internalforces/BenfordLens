<!--
Purpose:        Track known bugs, technical debt, and temporary workarounds
Owner:          Debugger / Reviewer
Update Trigger: New bug found, issue resolved, new tech debt identified
Harness Version: 1.1
-->

# Known Issues — Benford Lens

_Last updated: 2026-08-05_

## Active Bugs

| ID | Severity | Description | Found | Owner |
|----|----------|-------------|-------|-------|
| ENV-001 | Medium | macOS local env: Recent `.venv`-affecting edits can set macOS hidden flag on native extensions (numpy, pandas, PySide6), causing pytest crashes with faulthandler dump during dynamic library loading. Workaround: `chflags -R nohidden .venv` before running tests. Does not affect Linux CI (ubuntu-latest). | 2026-08-04 | DevEnv |

## Technical Debt

| ID | Description | Impact | Target Resolution |
|----|-------------|--------|-------------------|
| TD-001 | CSV encoding detection uses fixed try-in-order fallback (utf-8-sig → utf-8 → cp949 → euc-kr → latin-1), not real content-based detection | A CP949-encoded file with byte sequences that are also valid UTF-8 could silently mis-decode | Revisit if real user reports occur; consider adding chardet/charset-normalizer if this becomes a problem |
| TD-002 | `test_summarize_result_uses_neutral_non_accusatory_language` (`tests/charts/test_benford_chart.py`) uses a 10-value sample; after the M1 final-review fix adding a `sample_size < 30` small-sample guard to `summarize_result`, that input now hits the new "too few valid values" branch instead of the "close to expected Benford distribution" branch it was meant to exercise — no test currently covers the "close" branch's wording | Test-coverage gap only, not a functional bug; all tests still pass | M2: bump that test's sample to ≥30 values, or add a dedicated ≥30-sample "close to Benford" test |
| TD-003 | `packaging/benford-lens-windows.spec` and `packaging/benford-lens-linux.spec` are written but unbuilt and untested — this dev environment is macOS-only with no Windows/Linux build target. The macOS build itself was only smoke-tested headlessly (`QT_QPA_PLATFORM=offscreen`, process starts and survives 5s), not verified interactively (no display in this environment). | Windows/Linux packaging correctness is unverified; macOS interactive behavior of the frozen bundle is unverified | Verify on an actual Windows/Linux machine or add cross-platform PyInstaller build+smoke-test jobs to CI |

## Resolved

| ID | Description | Resolved | Method |
|----|-------------|----------|--------|
| — | — | — | — |

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
