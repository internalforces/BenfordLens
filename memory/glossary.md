<!--
Purpose:        Project-specific terms and abbreviations
Owner:          All agents (contribute), Documenter (maintain)
Update Trigger: New domain term introduced, existing term meaning changed
Harness Version: 1.1
-->

# Glossary — Benford Lens

_Last updated: 2026-08-04_

## Domain Terms

| Term | Definition |
|------|-----------|
| Benford's Law | A statistical pattern predicting the expected frequency of leading digits (1–9) in many naturally occurring numerical datasets |
| First-digit analysis | Comparing the observed frequency of each first significant digit against the Benford-expected frequency (MVP scope) |
| Second-digit analysis | Same comparison for the second digit (planned for v2) |
| Suitability check | Automated pre-analysis check (sample count, min/max, digit range, duplicate rate, zero rate, negative rate, missing rate, distinct-value count) used to flag, but never auto-decide, whether a dataset may be appropriate for Benford analysis |
| MAD | Mean Absolute Deviation — a common metric for how closely an observed distribution matches the Benford-expected one |
| Chi-square test | Statistical goodness-of-fit test comparing observed vs. expected digit distributions |
| KS Test | Kolmogorov–Smirnov test, another goodness-of-fit test used in the expert statistics view |
| Preprocessing options | User-selectable transformations applied before analysis: negative handling, zero handling, decimal handling, blank handling, duplicate handling, string-to-number parsing |
| Drill-down | Clicking a digit in the results chart to view the original rows whose leading digit matches |

## Abbreviations

| Abbr | Full Form | Description |
|------|-----------|-------------|
| ADR | Architecture Decision Record | Log of technical decisions |
| MVP | Minimum Viable Product | Smallest shippable version |
| Gate | Human Approval Gate | Checkpoint requiring user approval |
| PRD | Product Requirements Document | The Benford Lens spec this Harness was generated from |

## Harness Terms

| Term | Definition |
|------|-----------|
| Harness | The full AI development OS document structure |
| Session | A single agent work unit |
| Active Task | A task currently in tasks/active.md |
| Registry | The list of active agent roles |
