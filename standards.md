<!--
Purpose:        Code and documentation quality standards
Owner:          Reviewer
Update Trigger: Code style changes, new tooling, test coverage threshold changes
Harness Version: 1.1
-->

# standards.md — Benford Lens Standards

_Last updated: 2026-08-04_

## Code Style

- **Language**: Python (target 3.11+)
- **Indentation**: 4 spaces
- **Max line length**: 100 (enforced via `ruff`)
- **Naming**: variables/functions `snake_case`, classes `PascalCase`, constants `UPPER_SNAKE_CASE`, modules `snake_case`
- **Formatting/linting**: `ruff format` + `ruff check`; `mypy` for type checking on `src/`

## Commit Messages

```
<type>(<scope>): <subject>
```
Types: `feat` | `fix` | `docs` | `style` | `refactor` | `test` | `chore` | `security`

## PR Rules

- Title follows commit message format
- Reviewer agent sign-off required before merge
- Self-merge is not allowed

## Test Standards

- Unit tests: all business logic, especially:
  - preprocessing pipeline (negative/zero/decimal/blank/duplicate handling, string-to-number parsing)
  - suitability check thresholds and 🟢/🟡/🔴 classification logic
  - Benford digit-frequency calculations and statistical tests (MAD, Chi-square, KS test)
- Integration tests: file loading (CSV encodings, Excel multi-sheet), end-to-end analysis flow, HTML report generation
- UI tests: core PySide6 flows (file open → column select → preprocess → analyze → drill-down → export) where practical
- Minimum coverage: 80%

## Security Standards

- No hardcoded secrets in code (none expected — the app has no credentials)
- Validate all inputs, especially untrusted file contents (malformed CSV/XLSX, encoding issues, oversized files)
- Regular dependency vulnerability scanning (`pip-audit` or equivalent) even though the app is offline, since a compromised dependency in the shipped binary is still a risk
- No code path may open a network connection; this is a standing constraint, not just a style preference (see AGENTS.md Absolute Restrictions)

## Documentation Standards

- Comments required on all public functions/APIs in the analysis engine
- Inline explanation for non-obvious statistical logic (e.g. why a given MAD threshold was chosen)
- All user-facing strings must comply with the Product Philosophy & Tone Rules in AGENTS.md
- Record key decisions in `memory/decisions.md`

## Review Checklist (before requesting review)

- [ ] Code style compliant
- [ ] Test coverage met
- [ ] No security issues
- [ ] No new network calls introduced
- [ ] User-facing copy uses neutral, non-accusatory wording
- [ ] Documentation complete
- [ ] No AGENTS.md restrictions violated
