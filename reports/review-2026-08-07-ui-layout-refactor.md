# UI Layout Refactor Review

_Date: 2026-08-07_
_Scope: TASK-027 / ISS-003_
_Verdict: Approved_

## Result

The refactor resolves both high-severity findings from
`reports/review-2026-08-07-ui-layout.md` without changing analysis behavior or public analysis
interfaces.

## Review Findings

No blocking findings.

- The top-level window no longer inherits the full workflow's vertical minimum size.
- Vertical overflow is reachable through a resizable scroll viewport instead of being clipped.
- Combined charts stack on compact viewports and switch to side-by-side only when both retain a
  readable width.
- Chart canvases retain at least 300 pixels of height.
- The responsive breakpoint uses hysteresis, preventing scrollbar width changes from repeatedly
  flipping orientation.
- A successful analysis reveals the result while leaving every preceding section reachable.
- Compact, wide, and Russian translated combined layouts have geometry regression coverage.

## Measured Before and After

| Scenario | Before | After |
|---|---|---|
| Requested 900x700 combined window | Expanded to 900x944 | Remains 900x700 |
| Compact combined chart | About 420x101 each, side by side | About 828x400 each, stacked |
| Suitability metrics | Compressed below minimum; rows clipped | At or above minimum; scroll-reachable |
| 1280x900 combined chart | Vertically compressed | About 592x400 each, side by side |
| Horizontal overflow | Layout-dependent clipping risk | No horizontal scroll at tested widths |

## Verification

- Ruff check: pass
- Ruff format check: pass (46 files)
- mypy: pass (22 source files)
- pytest: 232 passed
- Visual QA: 900x700 stacked and 1280x900 side-by-side combined views inspected
- No new dependency or network path
- No changes to analysis calculations, applicability judgment, column selection, report content,
  or source-file handling
