## Outcome

Describe the user-visible or engineering outcome.

## Scope and boundaries

- [ ] Data processing remains local; no user data, telemetry, or update check leaves the machine.
- [ ] Source CSV/XLSX files remain read-only.
- [ ] Worksheet, column, preprocessing, analysis mode, and applicability judgments remain explicit.
- [ ] User-facing wording is neutral and exploratory.
- [ ] No real or sensitive dataset is included in code, tests, screenshots, logs, or fixtures.

## Verification

- [ ] `uv run ruff check .`
- [ ] `uv run ruff format --check src/ tests/ scripts/`
- [ ] `uv run mypy src/`
- [ ] `QT_QPA_PLATFORM=offscreen uv run pytest`

List platform-specific or manual checks and any verification that remains.

## Change impact

- Dependency or supported-file-format change:
- UI translations:
- Packaging / release:
- Third-party notices:
- Documentation / project records:
