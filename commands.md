<!--
Purpose:        Quick-reference commands for each agent role
Owner:          Implementer / Release Manager
Update Trigger: New commands added, environment changed
Harness Version: 1.1
-->

# commands.md — Benford Lens Quick Reference

_Last updated: 2026-08-04_

## Setup

```bash
uv sync                  # Install dependencies into a local virtual environment
```

No `.env` or credentials setup is required — Benford Lens makes no network calls and has no accounts.

## Development

```bash
uv run python -m benford_lens   # Launch the app in development mode
uv run pytest                    # Run tests
uv run ruff check .              # Lint
uv run ruff format .             # Format
uv run mypy src/                 # Type check
```

## Build & Package

```bash
uv run pyinstaller benford_lens.spec   # Build a standalone executable (Windows/macOS/Linux)
```

There is no staging/production server — Benford Lens is a local desktop application.
Packaged builds are attached to GitHub Releases after Reviewer sign-off.

```bash
# ⚠️ Publishing a release build: HUMAN APPROVAL required
gh release create vX.Y.Z dist/*
```

## Data / Storage

There is no database and no persisted application data beyond user-initiated exports
(HTML reports saved by explicit user action). No migration or seed commands apply.
