<!--
Purpose:        Track known bugs, technical debt, and temporary workarounds
Owner:          Debugger / Reviewer
Update Trigger: New bug found, issue resolved, new tech debt identified
Harness Version: 1.1
-->

# Known Issues — Benford Lens

_Last updated: 2026-08-04_

## Active Bugs

| ID | Severity | Description | Found | Owner |
|----|----------|-------------|-------|-------|
| — | — | (none — no code written yet) | — | — |

## Technical Debt

| ID | Description | Impact | Target Resolution |
|----|-------------|--------|-------------------|
| TD-001 | CSV encoding detection uses fixed try-in-order fallback (utf-8-sig → utf-8 → cp949 → euc-kr → latin-1), not real content-based detection | A CP949-encoded file with byte sequences that are also valid UTF-8 could silently mis-decode | Revisit if real user reports occur; consider adding chardet/charset-normalizer if this becomes a problem |

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
