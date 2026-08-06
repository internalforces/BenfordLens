# M3 Analysis Modes Design

**Date:** 2026-08-06  
**Status:** Accepted  
**Scope:** First-digit, second-digit, and combined analysis in M3/v1.0

## Product Definition

M3 adds three explicit analysis modes:

1. **First digit** — the existing 1–9 distribution.
2. **Second digit** — the second significant digit, 0–9.
3. **First + second** — both independent distributions shown together in one results view.

“Combined analysis” does **not** mean a joint 10–99 first-two-digit distribution and does not
merge both positions into one statistic. It is a presentation and workflow mode that computes
both results from one preprocessing snapshot and keeps both visible at the same time.

The user still explicitly selects the source column and starts analysis. The application does
not choose an analysis target or decide whether a Benford comparison is appropriate.

## Statistical Definitions

### Second significant digit

For each finite, non-zero magnitude, the first two digits of the normalized scientific
mantissa are used. The second digit therefore ranges from 0 through 9. A value with one
explicit significant digit, such as `5`, contributes second digit `0`, consistent with its
normalized representation `5.0 × 10^0`. Zero and non-finite values remain excluded, and
negative handling continues to follow the user-selected preprocessing option.

Expected second-digit probability for digit `d` is:

`sum(log10(1 + 1 / (10 * first + d)) for first in 1..9)`

This definition and boundary cases must be covered by table-driven unit tests before UI work.

### Reference statistics

- MAD and Chi-square are calculated separately for each displayed distribution: nine buckets
  for first digit and ten buckets for second digit.
- The log-mantissa KS calculation describes the shared preprocessed sample, so combined mode
  shows it once rather than duplicating the same value under both panels.
- No threshold, verdict, or automatic applicability conclusion is added.

## Compatibility-First Analysis API

The existing `BenfordResult`, `first_digit()`, `expected_first_digit_distribution()`, and
`analyze_first_digit()` interfaces stay available unchanged.

M3 adds:

```python
class DigitPosition(Enum):
    FIRST = "first"
    SECOND = "second"


@dataclass(frozen=True)
class CombinedBenfordResult:
    first: BenfordResult
    second: BenfordResult


def second_digit(value: float | int | None) -> int | None: ...
def expected_second_digit_distribution() -> dict[int, float]: ...
def analyze_second_digit(series: Iterable[float] | pd.Series) -> BenfordResult: ...
def analyze_combined(series: Iterable[float] | pd.Series) -> CombinedBenfordResult: ...
```

Internally, digit extraction and bucket aggregation are shared helpers. Combined analysis
extracts both positions in one pass; it must not call two independent preprocessing pipelines.
This preserves current callers while removing the first-digit-only duplication pressure.

## Controller and Snapshot

Add an explicit `AnalysisMode` (`FIRST`, `SECOND`, `COMBINED`) selected by the user. The
controller preprocesses the selected column once and records an immutable analysis snapshot
containing:

- mode;
- preprocessing options and preview;
- suitability assessment;
- first and/or second digit results;
- per-position MAD/Chi-square statistics;
- one shared log-mantissa KS result;
- the preprocessed row-to-digit mapping needed for drill-down.

Changing the file, sheet, column, preprocessing options, or analysis mode invalidates the
entire snapshot and all derived UI. Drill-down becomes position-aware:

```python
drill_down_digit(position: DigitPosition, digit: int) -> pd.DataFrame
```

The existing `drill_down(digit)` remains as a first-digit compatibility wrapper. Both methods
return original, unmodified source rows selected through the stored snapshot mapping, so the
table always agrees with the chart that was clicked.

## Results UI

Create a reusable `DigitResultPanel` that owns one position's title, summary, chart canvas,
and chart-click signal.

- First- or second-digit mode instantiates one panel.
- Combined mode instantiates two panels in the same results view, first digit on the left and
  second digit on the right. Both remain visible; tabs or a mode toggle must not hide either
  result.
- A shared, collapsed expert-details section appears below the result panels. It shows the
  relevant per-position MAD/Chi-square values and one KS result.
- One drill-down panel remains below the results. Its heading identifies the clicked position
  and digit, and a click in either result panel replaces its rows.

The main window coordinates reusable panels; it does not contain position-specific chart or
click logic.

## Chart and Summary Boundaries

Introduce position-neutral chart and summary helpers that accept bucket labels and translated
presentation labels. Keep `build_first_digit_figure()` as a compatibility wrapper. The second
digit x-axis is 0–9; click validation must derive its valid bucket set from the result instead
of hard-coding 1–9.

Result summaries remain separate for first and second digit in combined mode. They use the
same neutral, exploratory message codes, but each rendered sentence identifies which position
it describes. A difference in one distribution must not be presented as a conclusion about
the dataset.

## HTML Report

Report context becomes mode-aware while preserving the current first-digit rendering path.
Combined reports contain two clearly labeled sections, charts, summaries, and distribution
tables from the same snapshot. Shared preprocessing, suitability, and KS content is rendered
once. Report generation remains an explicit local file write and never modifies the source.

## Implementation Order

1. Shared digit extraction plus second-digit formulas and tests.
2. Combined result and generic statistics engine with first-digit compatibility tests.
3. Mode-aware controller snapshot and position-aware drill-down tests.
4. Reusable result panel, single modes, then the two-panel combined layout.
5. Mode-aware report and i18n strings.
6. Large-dataset profiling and optimization using the single-pass extraction boundary.

Each step must keep the current first-digit behavior passing. No new dependency is required.

## Acceptance Criteria

- First-digit behavior and public entry points remain compatible.
- Second-digit probabilities sum to 1 within floating-point tolerance and match reference
  values for digits 0–9.
- Combined mode preprocesses once and renders both independent results simultaneously.
- Chart clicks filter by both position and digit and return only original source rows.
- Combined expert details do not duplicate the shared KS result.
- HTML export reflects the selected mode and the exact analysis snapshot.
- EN/KO/ZH/JA UI strings are complete; all wording remains neutral and advisory.
- Ruff, mypy, the full test suite, and at least 80% line coverage pass.
