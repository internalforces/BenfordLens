# Benford Lens

Benford Lens is a local desktop application for exploring first- and second-digit distributions
in CSV and Excel data. It compares the user-selected column with the expected Benford
distributions and provides neutral, reference-oriented context for further review.

All file reading, preprocessing, analysis, charts, and report generation happen on your own
machine. The application has no account system, telemetry, or network-based analysis.

## v1.0 feature set

- CSV and XLSX loading, with explicit column selection
- User-controlled handling of negative, zero, decimal, blank, duplicate, and text-formatted
  values, including a before/after preview
- First-digit, second-digit, and combined expected-versus-observed charts
- Advisory data-characteristics panel with the underlying metrics
- Optional expert details with MAD, Chi-square, KS, and sample-size references
- Raw-row drill-down from chart digits, substring search, and local CSV export
- Local HTML report export
- English, Korean, Chinese, Japanese, Spanish, French, and Russian UI selection
- Scroll-safe desktop workflow with responsive combined charts
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
headless-smoke-tested on Apple Silicon, and its bundle version is derived from the project
version. The Windows x64 specification and WiX 5.0.2 MSI have been built and smoke-tested on
Windows. Build the Windows application and user-scoped installer with .NET 8 SDK available:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File packaging/build-windows-msi.ps1
```

Add `-InstallSmokeTest` to verify installation, startup, and removal; add `-SkipPyInstaller`
only when reusing an already verified `dist/benford-lens` folder. Public macOS distribution
still requires Developer ID signing and notarization. Public Windows distribution requires
Authenticode signing and clean-machine verification. Linux remains unverified on its target
platform.

## Project status

The current source version is `1.0.0`. M3/v1.0 is implemented and includes first-, second-, and
combined-digit analysis, responsive results, seven UI languages, expert reference statistics,
drill-down, HTML reporting, and local-only packaging configuration. See `roadmap.md` for milestone
history and post-v1.0 ideas.
