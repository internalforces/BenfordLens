<!--
Purpose:        Track known bugs, technical debt, and temporary workarounds
Owner:          Debugger / Reviewer
Update Trigger: New bug found, issue resolved, new tech debt identified
Harness Version: 1.1
-->

# Known Issues — Benford Lens

_Last updated: 2026-08-09_

## Active Bugs

| ID | Severity | Description | Found | Owner |
|----|----------|-------------|-------|-------|
| ENV-001 | Medium | macOS local env: Recent `.venv`-affecting edits can set macOS hidden flag on native extensions (numpy, pandas, PySide6), causing pytest crashes with faulthandler dump during dynamic library loading. Workaround: `chflags -R nohidden .venv` before running tests. Does not affect Linux CI (ubuntu-latest). | 2026-08-04 | DevEnv |

## Technical Debt

| ID | Description | Impact | Target Resolution |
|----|-------------|--------|-------------------|
| TD-001 | CSV encoding detection uses fixed try-in-order fallback (utf-8-sig → utf-8 → cp949 → euc-kr → latin-1), not real content-based detection | A CP949-encoded file with byte sequences that are also valid UTF-8 could silently mis-decode | Revisit if real user reports occur; consider adding chardet/charset-normalizer if this becomes a problem |
| TD-003 | `packaging/benford-lens-linux.spec` is written but remains unbuilt and untested. The macOS build was only smoke-tested headlessly (`QT_QPA_PLATFORM=offscreen`, process starts and survives 5s), not verified interactively. | Linux packaging correctness and macOS interactive behavior remain unverified | Verify on an actual Linux machine and an interactive macOS session, or add platform build-and-smoke-test jobs to CI |
| TD-005 | CI does not collect or enforce the 80% coverage standard | Local merge-gate review measured 91% total line coverage, so the standard is currently met, but future regressions are not automatically blocked | Consider approved CI coverage tooling in a later developer-infrastructure task |
| TD-007 | The macOS PyInstaller candidate is Apple Silicon-only and ad-hoc signed; no Developer ID certificate or Apple notarization credentials are configured | The local ZIP passes structural, signature-integrity, and headless startup checks, but Gatekeeper may warn or block it on another Mac and Intel Macs cannot run the arm64 binary | Before public distribution, build the approved target architectures, sign with Developer ID, notarize with Apple, staple the ticket, and verify on a clean Mac |
| TD-008 | The Windows x64 PyInstaller ZIP and WiX MSI candidates are not Authenticode-signed and have only been verified on the build machine | Windows SmartScreen may warn on another PC even though ZIP startup and MSI install/startup/uninstall smoke tests pass locally | Sign the application executable and MSI with an approved code-signing certificate, then verify both assets on a clean supported Windows machine before treating them as broadly trusted public releases |

## Resolved

| ID | Description | Resolved | Method |
|----|-------------|----------|--------|
| ENV-002 | Windows offscreen Qt expanded the Russian combined-results window from 900 px to 972 px because all translated toolbar controls shared one row | 2026-08-07 | Split the fixed toolbar into two rows and strengthened the compact Russian layout test to verify both the exact window size and every control's horizontal bounds |
| ISS-001 | A failed file load or cancelled Excel sheet selection could change the report source name while leaving the previous analysis active | 2026-08-05 | Assign `_source_path` only after the new dataframe opens; added regression tests for both failure and cancellation |
| TD-002 | `test_summarize_result_uses_neutral_non_accusatory_language` (`tests/charts/test_benford_chart.py`) used a 10-value sample that hit the "too few valid values" branch instead of the "close to expected Benford distribution" branch — no test covered the "close" branch's wording | 2026-08-05 | Added a dedicated test (`test_summarize_result_flags_a_close_match_for_a_large_benford_like_sample`), using powers of 2 (a classic near-Benford sample) at ≥30 values, during the Task 11 final-review sanity pass |
| TD-004 | README and package/project version metadata did not describe the implemented M2 state | 2026-08-05 | Expanded README and synchronized the source version to `0.2.0.dev0` |
| TD-006 | Milestone documentation was inconsistent after the M2 merge | 2026-08-06 | Marked M2 merged in `roadmap.md` and corrected the glossary's second-digit target to M3/v1.0 |
| ISS-002 | Result-summary and HTML-report copy contained a term prohibited by the stricter wording rule in `AGENTS.md` | 2026-08-06 | Replaced it with neutral guidance focused on interpreting data characteristics; synchronized UI/report tests and regenerated KO/ZH/JA `.qm` catalogs |
| ISS-003 | The single-page UI exceeded common screen heights and compressed suitability metrics and combined charts below a readable size | 2026-08-07 | Added a scroll-bounded workflow, responsive stacked/side-by-side result layout, 300 px minimum chart height, result auto-reveal, and geometry regression tests; 900x700 now remains 900x700 with 828x400 compact charts |
| TD-009 | The repository described Benford Lens as open source but had no root `LICENSE` file | 2026-08-09 | The user selected MIT; added the standard MIT license with 2026 Benford Lens contributors copyright notice |
| TD-010 | Public documentation lacked representative visuals, a concise case study, and a short architecture/verification path | 2026-08-09 | Accepted ADR-017; added Korean/English landing pages, four bilingual public guides, and reproducible synthetic-data screenshots/GIF while preserving internal evidence |

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
