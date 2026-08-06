<!--
Purpose:        Project milestones and feature planning
Owner:          Planner
Update Trigger: Milestone completed, new feature added, priorities changed
Harness Version: 1.1
-->

# roadmap.md — Benford Lens Roadmap

_Last updated: 2026-08-06_

## Goal

An open-source desktop application that lets non-experts easily analyze Benford's Law on
their own CSV/Excel data, entirely on their local machine, with no data ever sent to an
external server.

## Milestones

### M1 — MVP (PRD Phase 1) — implemented and merged to `main` (PR #1)
- [x] CSV file reading (with automatic encoding detection)
- [x] Excel file reading (with sheet selection)
- [x] Manual column selection (no auto-analysis of "numeric-looking" columns)
- [x] First-digit Benford analysis
- [x] Expected vs. actual distribution chart output

### M2 — Phase 2 — implemented and merged to `main` (PRs #2–#4)
- [x] Preprocessing options (negative handling, zero handling, decimal handling, blank handling, duplicate handling, string-to-number parsing) with before/after preview
- [x] Data suitability check (🟢/🟡/🔴) with sample count, min/max, digit range, duplicate rate, zero rate, negative rate, missing rate, distinct-value count
- [x] Raw data drill-down (click a leading digit in the chart → filtered original rows)
- [x] HTML report generation
- [x] UI language selection — default English; selectable Korean/Chinese/Japanese (i18n scaffolding, see ADR-004)
- [x] Expert statistics panel (MAD, Chi-square, KS Test, sample size) — hidden by default

### M3 — v1.0 (Phase 3)
- [x] Second-digit analysis
- [x] Combined first+second-digit analysis — both independent results shown together in one
  results view (not a joint first-two-digit distribution; see ADR-009)
- [x] Performance optimization for large datasets — removed repeated digit extraction;
  100k-row controller benchmark improved 30.0–31.8% (TASK-024)
- [x] Expand language support beyond the initial EN/KO/ZH/JA set added in M2 — Spanish,
  French, and Russian added in M3 (ADR-010, ADR-011)

## Backlog Ideas

- Additional file format support: XLS, ODS, TSV (PRD §5, explicitly post-MVP)
- Evaluate migrating charts from Matplotlib to PyQtGraph for smoother interaction on large datasets

## Out of Scope (MVP)

- Cloud storage
- User accounts / login
- AI-based fraud judgment or automatic fraud detection
- Online data upload
- Direct PDF generation (HTML report only for now)
- Real-time collaboration
