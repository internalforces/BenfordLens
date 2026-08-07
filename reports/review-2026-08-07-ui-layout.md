# UI Layout Review — Clipping and Narrow Combined Results

_Date: 2026-08-07_
_Role: Reviewer / Debugger_
_Verdict: Request Changes_

## Scope

Review the report that the desktop UI is clipped and too narrow. This was a diagnostic review;
no application source code was changed.

## Findings

### 1. High — The main workflow has no scroll boundary and exceeds common screen heights

`MainWindow` places the toolbar, column table, preprocessing panel, suitability panel, result
panels, expert statistics, and drill-down table in one uninterrupted vertical layout
(`src/benford_lens/ui/main_window.py:143-154`). The entry point requests a 900x700 window
(`src/benford_lens/__main__.py:14-16`), but Qt expands it to satisfy the layout's minimum size.

Offscreen reproduction measurements:

| State | Requested | Actual | Minimum size hint | Preferred central size |
|---|---:|---:|---:|---:|
| Initial | 900x700 | 900x928 | 514x928 | 514x1147 |
| Combined result | 900x700 | 900x944 | 514x944 | 1260x1553 |

The actual combined window is already taller than a 900-pixel display before accounting for
the operating-system title bar and dock/taskbar. Even at 944 pixels, the suitability panel is
allocated 191 pixels against a 264-pixel minimum-size hint, so its metric rows are visibly
clipped. There is no `QScrollArea`, splitter, tab, stacked workflow page, or collapsible boundary
that lets a user reach content outside the available screen.

### 2. High — Combined mode halves the chart width without a responsive fallback

The two `DigitResultPanel` widgets are always placed side by side in one `QHBoxLayout`
(`src/benford_lens/ui/main_window.py:132-134`). Each chart is authored as a 6x4-inch Matplotlib
figure (`src/benford_lens/charts/benford_chart.py:63`) and inserted without an explicit readable
minimum, aspect policy, or narrow-width layout switch
(`src/benford_lens/ui/digit_result_panel.py:51-60`).

Measured combined-mode chart allocations:

| Window width | Panel size (each) | Canvas size (each) |
|---:|---:|---:|
| 600 px | 288x191 | 270x86 |
| 800 px | 388x191 | 370x101 |
| 900 px | 438x191 | 420x101 |
| 1200 px | 588x191 | 570x116 |

At 900 pixels the canvas is only about 101 pixels high, and at 600 pixels the legend consumes a
large share of the plot. Axis labels and tick labels are clipped or crowded. Widening the window
alone does not restore chart height because the oversized vertical stack remains the limiting
constraint.

### 3. Medium — Existing UI tests verify widget state, not usable geometry

`tests/ui/test_main_window.py` verifies that result panels and canvases exist in combined mode,
but does not show the window at supported viewport sizes or assert that important child widgets
fit inside their allocated geometry. This allowed a functionally correct combined layout to pass
while remaining unreadable on a laptop-sized screen.

## Root Cause

The M1 single-page vertical layout accumulated M2/M3 panels without being restructured for the
larger workflow. M3 then placed two fixed-aspect chart concepts side by side inside the same
already-constrained page. Qt responds by growing the top-level window and compressing selected
children below their usable size.

## Recommended Fix Direction

1. Introduce a real viewport boundary: place the workflow content in a resizable `QScrollArea`,
   or preferably split the workflow into selection/setup and result/detail pages or tabs.
2. Give results the primary space after analysis. Do not keep the full preprocessing form,
   suitability metrics, two charts, and drill-down table simultaneously expanded.
3. Make combined results responsive: side by side only above a tested width; otherwise stack the
   two result panels vertically or provide first/second tabs.
4. Give the chart canvas a tested minimum readable height and let the result area expand before
   the empty drill-down table.
5. Add geometry regression tests at representative compact and laptop viewports, including a
   non-English language and combined mode.

Changing only `window.resize(...)` is not sufficient: the measured preferred combined content is
1260x1553, so the structure must become scrollable or progressive.

## Compliance Check

- No user data was sent anywhere; reproduction data was synthetic and processed locally.
- No network calls or dependencies were introduced.
- No original input file was modified.
- No user-facing product wording was changed.
