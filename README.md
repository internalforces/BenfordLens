# Benford Lens

Benford Lens is a local desktop application for exploring first-digit distributions in CSV
and Excel data. It compares the selected column with the expected Benford distribution and
provides neutral, reference-oriented context for further review.

All file reading, preprocessing, analysis, charts, and report generation happen on your own
machine. The application has no account system, telemetry, or network-based analysis.

## M2 feature set

- CSV and XLSX loading, with explicit column selection
- User-controlled handling of negative, zero, decimal, blank, duplicate, and text-formatted
  values, including a before/after preview
- First-digit expected-versus-observed chart
- Advisory data-characteristics panel with the underlying metrics
- Raw-row drill-down from chart digits, substring search, and local CSV export
- Local HTML report export
- English, Korean, Chinese, Japanese, Spanish, and French UI selection
- PyInstaller specifications for macOS, Windows, and Linux

Benford Lens does not decide whether Benford's Law applies to a dataset. The suitability
panel describes characteristics of the selected data so that the user can make that judgment.

## Requirements

- Python 3.11
- [uv](https://docs.astral.sh/uv/)

## Run from source

```bash
uv sync --locked --group dev
uv run benford-lens
```

The application reads the selected source file without modifying it. Report and drill-down
exports are written only when the user chooses a separate destination.

## Development checks

```bash
uv run ruff check .
uv run ruff format --check src/ tests/
uv run mypy src/
QT_QPA_PLATFORM=offscreen uv run pytest
```

On macOS, if Qt or a native package fails to load after environment changes, clear the hidden
file flag as documented in `memory/known-issues.md` before rerunning the checks.

## Packaging status

PyInstaller specifications live in `packaging/`. The macOS specification has been built and
headless-smoke-tested. The Windows and Linux specifications still require verification on
their target platforms before a distribution release.

## Project status

The current source version is `0.2.0.dev0`. M2 adds preprocessing, data-characteristics
guidance, drill-down, HTML reporting, internationalization, and packaging configuration.
See `roadmap.md` for planned M3 work.
