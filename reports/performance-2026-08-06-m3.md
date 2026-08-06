# M3 Large-Column Performance Check

**Date:** 2026-08-06
**Environment:** Apple arm64, macOS 26.5.2, Python 3.11.15
**Scope:** Controller analysis only; no file I/O, chart rendering, or report rendering

## Workload

- 100,000 deterministic synthetic numeric values (`numpy.random.default_rng(20260806)`)
- Log-uniform magnitudes from `0.01` through `10,000,000`
- Every eleventh value made negative
- Default preprocessing options
- One warm-up followed by five measured runs per mode; median reported
- All values remained local and in memory

## Confirmed bottleneck

The controller previously extracted significant digits once for analysis and then twice more
while building first/second drill-down mappings. Profiling showed nearly identical latency in
all three modes because this repeated Python-level formatting dominated the small difference
between one and two result distributions.

The optimized path returns aligned first/second digit pairs from the same engine pass used to
build the combined result. All controller modes reuse that result and those pairs. Tests now
assert exactly one preprocessing call and one digit extraction per retained value for every
mode.

## Results

| Mode | Before median | After median | Improvement |
|------|--------------:|-------------:|------------:|
| First digit | 0.284455 s | 0.195216 s | 31.4% |
| Second digit | 0.277398 s | 0.194066 s | 30.0% |
| First + second | 0.281804 s | 0.192316 s | 31.8% |

Individual runs fluctuate with local scheduling, so these numbers are comparative development
measurements rather than a user-facing performance guarantee. The change removes the measured
duplicate work without adding a dependency or changing the existing first-digit public API.

## Reproduction outline

Create the deterministic NumPy array described above, place it in an in-memory Pandas
`DataFrame`, assign it to a fresh `SessionController`, explicitly select the `amount` column,
warm each `AnalysisMode` once, then measure five calls with `time.perf_counter()` and report
`statistics.median()`.
