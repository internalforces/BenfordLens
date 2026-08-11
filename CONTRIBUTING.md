# Contributing to Benford Lens

Thank you for helping improve Benford Lens. Contributions are welcome when they preserve the
project's local-first, user-directed analysis boundary.

## Before opening an issue

- Search existing issues and discussions first.
- Never upload a real or sensitive dataset, even when reproducing a bug. Use the smallest
  synthetic CSV/XLSX fixture that demonstrates the behavior.
- Use [Support](SUPPORT.md) for usage questions and the private process in
  [Security](SECURITY.md) for security-sensitive reports.

## Development setup

Benford Lens targets Python 3.11 and uses [uv](https://docs.astral.sh/uv/).

```bash
uv sync --locked --group dev
uv run benford-lens
```

The application must remain fully local: no login, telemetry, cloud analysis, remote update
check, or user-data upload path may be introduced.

## Make a change

1. Create a topic branch; do not commit directly to `main`.
2. Keep worksheet, column, preprocessing, and analysis-mode choices explicit.
3. Never modify the source CSV/XLSX file.
4. Use neutral, exploratory wording. The application describes distributions and data
   characteristics; it does not make an automatic applicability or misconduct determination.
5. Discuss a new external dependency or supported file format in an issue before implementation.
6. Update English and all six translation catalogs when changing UI text.
7. Add focused tests and update relevant documentation, notices, and project records.

## Verify locally

```bash
uv run ruff check .
uv run ruff format --check src/ tests/ scripts/
uv run mypy src/
QT_QPA_PLATFORM=offscreen uv run pytest
```

Packaging changes should also run the static notice-policy tests. Native distribution builds and
release publication are maintainer-gated because they create downloadable artifacts.

## Pull requests

Keep each pull request focused and explain:

- the user-visible outcome;
- how the local-data and explicit-choice boundaries are preserved;
- tests performed and any verification that remains platform-specific;
- dependency, packaging, translation, notice, or documentation impact.

By contributing, you agree that your contribution is provided under the repository's
[MIT License](LICENSE). Please follow the [Code of Conduct](CODE_OF_CONDUCT.md).
