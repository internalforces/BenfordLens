<!--
Purpose:        Key technical decision history in ADR format
Owner:          Architect / Researcher
Update Trigger: Record immediately after any significant technical decision
Harness Version: 1.1
-->

# Decision Log — Benford Lens

_Last updated: 2026-08-11_

## Template

```
### ADR-NNN: [Decision Title]
- **Date**: YYYY-MM-DD
- **Status**: Proposed | Accepted | Deprecated | Superseded
- **Decided by**: [Role / User]

**Context**: Why was this decision needed?
**Decision**: What was chosen?
**Rationale**: Why was this chosen?
**Trade-offs**: What are the downsides?
**Consequences**: What changed as a result?
```

---

### ADR-001: AI Development Harness v1.1 Adoption

- **Date**: 2026-08-04
- **Status**: Accepted
- **Decided by**: User

**Context**: Consistent context delivery and task tracking were needed for AI-assisted development on a project with strict local-first / privacy constraints that must be enforced consistently across agents and sessions.
**Decision**: Adopt AI Development Harness v1.1 (Standard tier) to structure agent roles, workflows, and memory, generated from the Benford Lens PRD.
**Rationale**: Eliminates context loss between sessions; structures multi-agent collaboration; encodes the project's tone and privacy rules (AGENTS.md) so they survive across every future session.
**Trade-offs**: Upfront documentation cost; the Harness must be kept in sync with the PRD as scope evolves.
**Consequences**: All agents operate from a shared, consistent context, including the non-negotiable local-first and tone constraints.

---

### ADR-002: Package Manager — uv

- **Date**: 2026-08-04
- **Status**: Accepted
- **Decided by**: User

**Context**: Needed a Python dependency/environment manager for a new project.
**Decision**: Use `uv` for dependency management and virtual environments.
**Rationale**: Fast, modern tooling with a single command surface for install/run/sync.
**Trade-offs**: Newer tool than pip/Poetry; smaller (but growing) ecosystem familiarity.
**Consequences**: `commands.md` and CI workflows are written against `uv`.

---

### ADR-003: CI/CD — GitHub Actions

- **Date**: 2026-08-04
- **Status**: Accepted
- **Decided by**: User

**Context**: Benford Lens is an open-source project; needed a CI approach for lint/test/build automation.
**Decision**: Use GitHub Actions for lint, type-check, test, and PyInstaller build-verification workflows.
**Rationale**: Standard default for open-source GitHub repositories; no additional infra to manage.
**Trade-offs**: Ties CI specifically to GitHub as the hosting platform.
**Consequences**: A CI workflow file will be added under `.github/workflows/` once the codebase exists.

---

### ADR-004: UI Language Defaults & i18n Scope

- **Date**: 2026-08-04
- **Status**: Accepted
- **Decided by**: User

**Context**: A UI mockup review (TASK-014) surfaced two open questions: (1) whether the expert
statistics panel should be hidden by default, and (2) what the MVP default UI language is,
since the mockup was entirely in Korean but `roadmap.md` only listed "multi-language (i18n)
support" as M3 scope with no stated default.

**Decision**:
1. The expert statistics panel (MAD, Chi-square, KS Test, sample size, deviation) stays
   **hidden by default**, confirming the existing design in `memory/architecture.md` and
   TASK-011. No change from the original PRD reading.
2. Default UI language is **English**. A language selector is added, scoped through M2 to
   exactly 4 languages: English (default), Korean, Chinese, Japanese. This moves basic i18n
   scaffolding up from M3 into M2 (M3 remains available for expanding beyond this set).

**Rationale**: Keeping expert stats hidden by default matches the PRD's original intent of a
plain-language-first results view. English-default with a constrained 4-language set gives
the mockup's Korean UI a home (as a selectable option, not the default) without committing to
open-ended i18n scope this early.

**Trade-offs**: Language selection + string externalization work now lands in M2 instead of
M3, adding scope to that milestone (translation maintenance for 3 non-default languages).

**Consequences**:
- `roadmap.md` M2 gains a UI language selection item; M3's multi-language item is narrowed to
  "beyond the initial 4-language set."
- Recommended implementation approach: PySide6/Qt's built-in translation system (`QTranslator`
  + `.ts`/`.qm` files via `pyside6-lupdate`/`pyside6-lrelease`) — no new external dependency,
  since PySide6 is already an approved dependency. See `tech-stack.md`.
- New backlog item TASK-015 tracks the i18n scaffolding + language selector work.

---

### ADR-005: Pin Dev Environment to Python 3.11

- **Date**: 2026-08-04
- **Status**: Accepted
- **Decided by**: Implementer (subagent-driven-development, M1), controller-diagnosed

**Context**: While implementing TASK-005/006 (analysis engine, chart), `uv run mypy src/` started failing with `Type statement is only supported in Python 3.12 and greater` inside numpy's bundled `__init__.pyi` type stub. Root cause: the dev `.venv` had no pinned interpreter, so `uv sync` picked up the newest available Python (3.13) and resolved a numpy build whose stub unconditionally uses PEP 695 `type X = ...` syntax — which `mypy` refuses to parse when its `python_version` target is `"3.11"` (the project's documented floor, unchanged from `tech-stack.md`/`requires-python = ">=3.11"`). Downgrading numpy was tried and ruled out: no numpy version with a working `cp313` wheel avoided the issue, and older numpy has no `cp313` wheel at all (fails building from source in this environment).

**Decision**: Pin the project's dev interpreter to Python 3.11 via a committed `.python-version` file (`uv python pin 3.11`), matching `requires-python` and matching what CI (TASK-012, `.github/workflows/ci.yml`) already runs (`uv python install 3.11`).

**Rationale**: Under a real Python 3.11 venv, `uv` resolves a numpy build whose stub parses cleanly at mypy's `python_version = "3.11"` target — verified directly, zero errors. This required no change to `pyproject.toml`, no numpy version pin, and no relaxation of the project's stated Python floor. It also closes a latent local/CI drift risk (a contributor's unpinned local venv silently running a newer Python than CI checks against).

**Trade-offs**: None identified — this only makes local dev match the project's own stated minimum version and CI's actual runtime; it doesn't narrow or widen supported Python versions.

**Consequences**: `.python-version` (containing `3.11`) is now a tracked repo file. Contributors running `uv sync` from a fresh checkout get a Python 3.11 venv automatically. No other config changed.

---

### ADR-006: Data Suitability Check Thresholds

- **Date**: 2026-08-05
- **Status**: Accepted
- **Decided by**: User (via M2 design spec approval)

**Context**: TASK-008 requires a 🟢/🟡/🔴 data suitability signal, but `roadmap.md` does not
specify concrete thresholds for sample count, digit-magnitude range, duplicate rate, zero
rate, negative rate, missing rate, or distinct-value count.

**Decision**: Adopt the following heuristic advisory thresholds (`src/benford_lens/analysis/suitability.py`):
- Sample count: < 30 → 🔴, 30–299 → 🟡, ≥ 300 → 🟢 (the 30-value floor reuses
  `MIN_MEANINGFUL_SAMPLE`, already established in `charts/benford_chart.py` for M1).
- Orders of magnitude spanned (`digit_range`): ≤ 1 → 🔴, 2–3 → 🟡, ≥ 4 → 🟢.
- Distinct-value ratio (`distinct_value_count / sample_count`): < 0.1 → 🔴, 0.1–0.29 → 🟡,
  ≥ 0.3 → 🟢.
- Zero rate > 0.3, negative rate > 0.5, or missing rate > 0.3 each add a 🟡-only advisory
  note (none of these alone escalate to 🔴).
- Overall level is the most severe of the above.

**Rationale**: Sample-count and magnitude-range floors reflect widely cited Benford-analysis
practice (a useful comparison needs both enough observations and enough orders of magnitude
for the leading-digit distribution to approach its asymptotic shape); the distinct-ratio
floor flags data that looks more like repeated codes/IDs than natural transactional
magnitudes. These are deliberately heuristic, not derived from a formal test.

**Trade-offs**: Arbitrary heuristic cutoffs, not statistically derived; may need retuning
once real user datasets are seen.

**Consequences**: `analysis/suitability.py` implements these values as named constants.
The suitability check remains advisory only — it never states or implies whether Benford's
Law applies to the dataset, per AGENTS.md's Product Philosophy & Tone Rules.

---

### ADR-007: Close the UI Mockup Review Without Automated Per-Column Verdicts

- **Date**: 2026-08-05
- **Status**: Accepted
- **Decided by**: Implementer / Reviewer, applying AGENTS.md constraints

**Context**: TASK-014 reviewed a visual mockup and proposed several details. Most were folded
into M1/M2, but its pre-selection column table included an automated per-column
"good/caution/unsuitable" hint, while the project constitution requires column choice and
the judgment about Benford applicability to remain with the user.

**Decision**: Close TASK-014 as a completed review. Keep the adopted preprocessing defaults,
neutral summary style, drill-down search/export, hidden expert details, and four-language
direction. Do not add a pre-selection per-column verdict. The existing suitability panel
continues to describe data characteristics only after the user explicitly selects a column.
A standalone filter icon and persistent shell trust badge are deferred to later UI polish;
search already performs the drill-down filtering, while the report and README state that
processing is local.

**Rationale**: This preserves the useful interaction details from the mockup without adding
an automated judgment that could influence column choice or be mistaken for an applicability
decision.

**Trade-offs**: The M2 window does not visually reproduce every decorative element in the
mockup.

**Consequences**: TASK-014 moves to `tasks/completed.md`. Future UI polish may add a neutral
local-processing badge, but must not introduce automated column selection or applicability
claims.

---

### ADR-008: Expert Statistics Methodology and Presentation

- **Date**: 2026-08-05
- **Status**: Accepted
- **Decided by**: User (SciPy approval and TASK-011 instruction) / Implementer

**Context**: TASK-011 requires MAD, Chi-square, and KS statistics. A KS test applied directly
to the nine discrete first-digit buckets would use a continuous-distribution p-value outside
its assumptions, while the product constitution also prohibits turning any statistic into an
automatic applicability judgment.

**Decision**:
- MAD is the mean absolute difference between the nine observed and expected first-digit
  proportions.
- Chi-square compares the nine observed counts with expected counts derived from Benford's
  first-digit probabilities and reports both the statistic and p-value.
- KS tests the fractional parts of `log10(abs(value))` against a uniform distribution. This
  uses the continuous log-mantissa form equivalent to Benford's Law instead of treating the
  discrete leading digits as continuous observations.
- Empty samples expose no statistic (`None` in the engine, `—` in the UI). The panel displays
  values only, adds a neutral reference caption, and remains collapsed by default; it does not
  assign thresholds, labels, or conclusions.

**Rationale**: This keeps each calculation statistically explicit, makes the KS p-value's
continuous-distribution assumption appropriate, and preserves the user's responsibility for
interpretation.

**Consequences**: SciPy is an approved runtime dependency. `analysis/expert_statistics.py`
stays PySide6-free, and `ui/expert_statistics_panel.py` handles formatting, translation, and
the hidden-by-default interaction.

---

### ADR-009: M3 Analysis Modes and Combined Results View

- **Date**: 2026-08-06
- **Status**: Accepted
- **Decided by**: User / Architect

**Context**: M3 adds second-digit and combined analysis, while the current calculation entry
point, chart, drill-down, expert details, and report are fixed to first digit. Extending each
path independently would duplicate workflow and make the two displayed results vulnerable to
different preprocessing or state.

**Decision**:

- Define combined analysis as independent first- and second-significant-digit results shown
  together in one results view. It is not a joint 10–99 first-two-digit distribution.
- Keep existing first-digit public entry points available unchanged. Add second-digit and
  combined functions backed by shared internal digit extraction and aggregation.
- Preprocess once per user action and store first/second results, statistics, suitability, and
  row-to-digit mappings in one immutable controller snapshot.
- Build a reusable digit-result panel. Single modes render one instance; combined mode renders
  first and second instances side by side with neither hidden behind tabs.
- Make chart clicks and drill-down position-aware. Keep the existing first-digit drill-down
  call as a compatibility wrapper.
- Calculate MAD and Chi-square per position. Show the sample-level log-mantissa KS result once
  in combined mode.
- Make HTML reporting mode-aware and render all sections from the same snapshot.

**Rationale**: A shared engine and reusable panel eliminate the largest duplication risks while
preserving working M1/M2 behavior. One snapshot guarantees that combined results describe the
same user-selected column and preprocessing choices.

**Trade-offs**: The controller and report context need a deliberate migration, and combined
mode needs more horizontal space. Compatibility wrappers remain until a separately approved
public API cleanup is warranted.

**Consequences**: M3 implementation follows
`reports/development/specs/2026-08-06-m3-analysis-modes-design.md`. No new dependency is required,
and the local-only, explicit-selection, and neutral-interpretation constraints remain intact.

---

### ADR-010: M3 Language Expansion to Spanish and French

- **Date**: 2026-08-06
- **Status**: Accepted
- **Decided by**: User

**Context**: ADR-004 established English, Korean, Chinese, and Japanese for M2 and left M3
language expansion open. TASK-025 required a bounded language choice before translation work.

**Decision**: Add Spanish and French as fully selectable UI languages in M3. Each language
must cover every current translatable message, preserve formatting placeholders, compile to a
packaged `.qm` catalog, and keep English as the default.

**Rationale**: These are the two languages explicitly selected by the user to complete M3's
expanded-i18n scope.

**Trade-offs**: The maintained catalog set grows from three translated catalogs to five, so
future UI strings require two additional translations and completeness checks.

**Consequences**: `resources/i18n/` now contains complete ES/FR `.ts` and `.qm` files, the
language selector exposes Español and Français, and automated catalog tests enforce the same
93-message key set and placeholder structure across KO/ZH/JA/ES/FR.

---

### ADR-011: M3 Russian Language Expansion

- **Date**: 2026-08-06
- **Status**: Accepted
- **Decided by**: User

**Context**: After TASK-025 completed the Spanish and French expansion, the user requested
Russian as an additional language in the same M3 pull request.

**Decision**: Add Russian as a fully selectable UI language. The Russian catalog must cover
all current translatable messages, preserve formatting placeholders, compile to a packaged
`.qm` resource, and keep English as the default.

**Rationale**: Russian is the additional language explicitly selected by the user before the
M3 pull request is merged.

**Trade-offs**: The maintained translated-catalog set grows from five to six, so future UI
strings require one additional translation and completeness check.

**Consequences**: `resources/i18n/` contains complete RU `.ts` and `.qm` files, the selector
exposes Русский, and automated catalog tests enforce the same 93-message key set and
placeholder structure across KO/ZH/JA/ES/FR/RU.

---

### ADR-012: Responsive, Scroll-Bounded Desktop Workflow

- **Date**: 2026-08-07
- **Status**: Accepted
- **Decided by**: User / Implementer

**Context**: After M2/M3 added preprocessing, suitability, a second result panel, expert
statistics, and drill-down to the original M1 vertical page, a requested 900x700 window expanded
to 900x944 and still clipped child content. Combined charts were compressed to roughly 420x101
pixels each.

**Decision**: Keep the toolbar outside a resizable `QScrollArea`, place all vertically growing
workflow content inside it, and enforce layout minimum sizes so overflow becomes reachable
scrolling instead of clipping. Combined results stay in one view but stack vertically below a
1100-pixel result width and switch to side-by-side above it, with hysteresis to avoid oscillation
around scrollbar boundaries. Every rendered chart keeps a 300-pixel minimum height, and a
successful analysis scrolls the new result into view.

**Rationale**: This preserves the existing workflow and ADR-009's simultaneous combined results
while making compact windows usable. It introduces no new user-facing strings, dependency, or
analysis behavior.

**Trade-offs**: Compact combined mode requires vertical scrolling between the first- and
second-digit charts; wide layouts continue to show both charts side by side.

**Consequences**: The 900x700 window remains 900x700, compact charts render at approximately
828x400, suitability content respects its minimum height, and horizontal scrolling is not needed
at tested 900- and 1280-pixel viewports. Geometry tests cover compact, wide, and Russian combined
states.

---

### ADR-013: macOS Bundle Version and Distribution Boundary

- **Date**: 2026-08-07
- **Status**: Accepted
- **Decided by**: User / Release Manager

**Context**: The first post-TASK-027 macOS PyInstaller candidate built successfully, but its
generated `Info.plist` reported the PyInstaller default version `0.0.0`. The build host has no
Apple Developer ID certificate or notarization credentials and produces an arm64 binary.

**Decision**: Read the package version from `pyproject.toml` in the macOS PyInstaller
specification and use its numeric release line for both `CFBundleShortVersionString` and
`CFBundleVersion`. Treat locally ad-hoc-signed arm64 archives as distribution candidates, not
public macOS releases. Public distribution requires an explicitly approved target architecture,
Developer ID signing, notarization, ticket stapling, and clean-machine verification.

**Rationale**: One version source prevents package/bundle drift, while the distribution boundary
avoids presenting a locally valid ad-hoc signature as equivalent to Apple's public trust chain.

**Trade-offs**: Development suffixes such as `.dev0` are omitted from the numeric macOS bundle
version. The source package metadata remains the authoritative full development version.

**Consequences**: The earlier `0.2.0.dev0` source produced a macOS bundle version of `0.2.0`.
After the v1.0 metadata synchronization, the same specification produces a `1.0.0` bundle
without a second manual version edit.

---

### ADR-014: Application Icon Concept A and macOS-First Rollout

- **Date**: 2026-08-07
- **Status**: Accepted
- **Decided by**: User / Implementer

**Context**: Benford Lens had no application icon in its PyInstaller bundle. Four neutral,
analysis-oriented icon concepts were reviewed, and the user selected concept A: a magnifying
lens framing a descending digit-distribution chart.

**Decision**: Adopt concept A as the application icon and apply it to the macOS package first.
Store a transparent 1024 px PNG source and a standard multi-resolution `.icns` under
`resources/icons/macos/`, and reference the `.icns` only from the macOS PyInstaller spec.

**Rationale**: The concept remains recognizable at 16 px, communicates distribution
exploration without warning or accusatory symbolism, and uses the existing chart-blue visual
direction. A platform-specific first step keeps the change bounded and independently verifiable.

**Trade-offs**: Windows and Linux packages continue to use their current default icons until
separate platform assets and packaging changes are approved. The generated raster source is
not a resolution-independent master.

**Consequences**: The macOS `.app` bundle will embed `benford-lens.icns`. The source PNG has
transparent outer corners, and the ICNS contains all standard 16–1024 px representations.

---

### ADR-015: Reuse the Approved Icon for the Windows x64 Package

- **Date**: 2026-08-08
- **Status**: Accepted
- **Decided by**: User / Release Manager / Implementer

**Context**: The Windows package still used PyInstaller's default icon after concept A was
approved and applied to macOS. The user requested a native Windows build using the same image.

**Decision**: Derive a Windows `.ico` containing 16, 20, 24, 32, 40, 48, 64, 96, 128, and
256 px representations from the approved 1024 px macOS PNG, reference it from the Windows
PyInstaller specification, and produce an x64 one-folder package and ZIP. Treat the output as
an unsigned build candidate, not a broadly trusted public release.

**Rationale**: A platform-native multi-resolution ICO keeps the approved visual identity while
remaining crisp in Explorer and taskbar contexts. The existing one-folder specification is the
smallest packaging change and keeps verification aligned with the established configuration.

**Trade-offs**: The Windows asset is derived from a raster source, and the unsigned executable
may trigger SmartScreen on another machine.

**Consequences**: `resources/icons/windows/benford-lens.ico` is embedded in the Windows x64
executable. The local build folder and a fresh extraction of the ZIP both pass startup smoke
tests; public distribution still needs approved Authenticode signing and clean-machine testing.

---

### ADR-016: Add a User-Scoped WiX MSI for Windows

- **Date**: 2026-08-08
- **Status**: Accepted
- **Decided by**: User / Release Manager / Architect / Implementer

**Context**: The verified Windows x64 deliverable was a portable PyInstaller one-folder ZIP.
The user approved an MSI so Windows users can use standard installation, Start menu, upgrade,
repair, and uninstall behavior while retaining the ZIP as a portable alternative.

**Decision**: Pin `WixToolset.Sdk` 5.0.2 and wrap the PyInstaller one-folder output in an
embedded-CAB, x64, per-user MSI installed under `%LOCALAPPDATA%\Programs\Benford Lens`. Keep a
stable UpgradeCode, derive the product version from `pyproject.toml`, create only a Start menu
shortcut, and add no file associations, services, auto-updater, or network behavior. The build
script disables .NET CLI telemetry and can explicitly run install/startup/uninstall smoke tests.

**Rationale**: Per-user installation avoids an administrator prompt while providing native
Windows lifecycle behavior. WiX 5.0.2 supplies built-in recursive file harvesting without the
separate maintenance EULA acceptance required by WiX 7, and its version is reproducibly pinned.

**Trade-offs**: Windows Installer's legacy ICE38/ICE64/ICE91 profile rules do not accept
automatically harvested per-user file trees, and ICE60 flags language metadata in third-party
PyInstaller binaries. Only those four ICE checks are suppressed; actual file-count, install,
startup, shortcut, uninstall, and residue checks compensate for the profile-specific warnings.
The MSI is larger and more complex than the portable ZIP.

**Consequences**: `packaging/benford-lens-installer.wixproj`,
`packaging/benford-lens-installer.wxs`, and `packaging/build-windows-msi.ps1` define a repeatable
MSI build and verification path. The current unsigned candidate passes local non-elevated
installation and complete removal, but Authenticode signing and clean-machine verification
remain required before broad public distribution.

---

### ADR-017: Separate Public Portfolio Documentation from Internal Development Records

- **Date**: 2026-08-09
- **Status**: Accepted
- **Decided by**: User / Planner / Documenter

**Context**: The repository contains strong implementation evidence across `memory/`, `tasks/`,
`reports/`, and detailed plans, but the README does not yet give a recruiter or first-time user
a short path through the problem, design choices, visual proof, and verified outcomes. Rewriting
or deleting the internal records would discard useful engineering evidence.

**Decision**: Keep the internal harness records intact and introduce a deliberately small public
documentation layer: an English README and matching Korean entry point, one portfolio case study,
one architecture summary, one verification summary, and one user guide. Public pages should link
selectively to existing evidence instead of exposing every internal session and task record in the
primary navigation. Screenshots and demo data must be synthetic.

**Rationale**: This separates audiences without duplicating the full development history. It lets
the README lead with user value and measurable engineering outcomes while retaining traceable ADR,
test, performance, and release evidence for deeper review.

**Trade-offs**: The public summaries can drift from internal records unless status claims are
checked during releases. A bilingual entry point also adds maintenance work.

**Consequences**: The English `README.md` and matching Korean `README.ko.md` now lead to four
bilingual public documents: case study, architecture, verification, and user guide. Synthetic
screenshots/GIFs are reproducibly generated from the real application, and previous implementation
plans/specs moved from `docs/superpowers/` to `reports/development/` so they remain evidence without
appearing in the public documentation path. The user selected the MIT license. The original audit
and execution rationale remain in `reports/portfolio-documentation-audit-2026-08-09.md`.

---

### ADR-018: Publish Verified Unsigned Packages through GitHub Releases

- **Date**: 2026-08-10
- **Status**: Accepted
- **Decided by**: User / Release Manager / Architect

**Context**: Developer ID/notarization and Authenticode identities add recurring cost and identity
approval gates. The user selected GitHub Releases as the initial distribution path and accepted
that operating-system trust warnings remain. Previously verified package files were not retained
on the current build host, so publishing old checksums without reproducible assets is not viable.

**Decision**: Build every public asset again from an exact semantic-version tag on native GitHub
Actions runners. Produce a Windows x64 portable ZIP, a Windows x64 per-user MSI, and a macOS arm64
ZIP. Verify extracted startup on both platforms, MSI install/startup/uninstall on Windows, macOS
bundle metadata/architecture/ad-hoc signature integrity, and all matching SHA-256 files. Upload to
a draft GitHub Release and publish it within the repository only after every platform job passes.
Release notes and
README download guidance must disclose that Windows packages lack Authenticode and the macOS app
lacks Developer ID signing/notarization.

**Rationale**: Native tag builds remove reliance on missing workstation artifacts, checksums tie
downloads to one verified workflow run, and draft-first publication prevents a partially populated
Release. Transparent warnings let testers make an informed choice without presenting unsigned
packages as broadly trusted by either operating system.

**Trade-offs**: SmartScreen may warn, Smart App Control or managed Windows policies may block the
app, and Gatekeeper may require a manual Open Anyway exception. GitHub availability is required to
download packages, although the installed application remains fully local and offline. Windows
and macOS signing can be added later without replacing this reproducible build boundary.

**Consequences**: ADR-013, ADR-015, and ADR-016 still define the distinction between package
integrity and platform trust, but signing is no longer a prerequisite for initial publication.
GitHub Actions becomes release infrastructure only; no application code or user data is sent to
GitHub. TASK-029 completes only after reviewer approval, an annotated `v1.0.0` tag, successful
native jobs, and verification of all six published asset files. Those gates were satisfied on
2026-08-10 for the non-draft v1.0.0 Release inside the private repository; anonymous public access
still depends on the separate repository-visibility decision.

---

### ADR-019: Preserve the Audited Public Repository History and Engineering Evidence

- **Date**: 2026-08-11
- **Status**: Accepted
- **Decided by**: User objective / Planner / Security Reviewer

**Context**: Changing the repository from private to public will expose all reachable Git history,
remote branches and tags, pull-request conversations, and Actions history/logs. ADR-017 already
preserves internal engineering evidence unless specific sensitive or unsuitable content is found.

**Decision**: Preserve the complete reachable history, all six fully merged topic branches, the
v1.0.0 tag, pull-request conversations, Actions logs, and the audited `memory/`, `tasks/`,
`prompts/`, and `reports/` evidence. Do not rewrite history. Preserve the stale
`memory/session 2.md` content under the dated session archive. Keep the user-owned untracked
`README 2.md` outside version control.

**Rationale**: The TASK-039 scan found no critical/high-risk exposure, credential, private-key
body, personal absolute path, personal email, or source dataset in reachable project history.
All topic branches are ancestors of `main`, so their contents are already reachable. Retaining the
records provides traceable engineering evidence without adding a new sensitive surface.

**Trade-offs**: Public history exposes 17 commits with the maintainer's real display name and 28
AI co-author trailers. The final TASK-044 approval must surface the real-name exposure again. The
existing release remains blocked separately by incomplete third-party notices and absent repository
protections.

**Consequences**: No destructive history operation or branch deletion is required. TASK-040,
TASK-042, and TASK-043 remain mandatory before the visibility change. See
`reports/security-2026-08-11-public-exposure.md`.

---

### ADR-020: Limit Qt Distribution to the Audited Essentials Runtime

- **Date**: 2026-08-11
- **Status**: Accepted
- **Decided by**: User objective / Architect / Security Reviewer / Release Manager

**Context**: The `pyside6` metapackage installed both Essentials and Addons. Although Benford Lens
uses only QtCore, QtGui, QtWidgets, and QtSvg, the previous private v1.0.0 package consequently
contained unused Qt Virtual Keyboard files, which Qt 6.11 offers under GPL-3.0-only terms. The
source repository and future public packages also need a complete, reproducible notice and source
availability record rather than incidental license files collected by PyInstaller.

**Decision**: Depend on `pyside6-essentials` instead of the `pyside6` metapackage. Maintain a
complete Qt 6.11 GPL-only module denylist in both native PyInstaller specifications and fail native
release verification if any matching module file remains. Ship `THIRD_PARTY_NOTICES.md`, the
offline `third_party_licenses/` set, and `docs/qt-relinking.md` in source and every desktop package,
and expose the primary notice document through a local-only in-app dialog. Preserve exact
Qt/PySide source identifiers and license-document hashes. Supersede the private v1.0.0 packages
with a separately versioned notice-complete release; do not replace or delete the existing release.

**Rationale**: The distribution boundary now matches the code's actual Qt use, removes an unused
GPL-only module before public exposure, and turns licensing expectations into deterministic tests
and native package checks. Dynamic Qt loading plus documented library replacement preserves a
practical relinking path without changing the application's local-only architecture.

**Trade-offs**: Essentials still contains unused permissively/LGPL-licensed Qt modules, so the
denylist and completed-package scan remain necessary. The checked-in notice set is large, and
license/source inventories must be updated whenever a locked runtime or packaging tool changes.
This engineering record is not legal advice.

**Consequences**: The source and static checks can complete before a distribution build, but
TASK-040 remains open until explicit human approval is received and native Windows/macOS packages
prove that the complete notice set is present and every denied Qt module is absent. See
`reports/research-2026-08-11-third-party-licensing.md`.

---

### ADR-021: Gate Public Contributions and Releases with Immutable Automation

- **Date**: 2026-08-11
- **Status**: Accepted
- **Decided by**: User objective / Security Reviewer / Release Manager

**Context**: The private repository allowed every Action, used mutable major tags, granted write
tokens to all release jobs, and had no branch or tag protection. Public pull requests and
anonymously downloadable packages increase the impact of a compromised workflow dependency,
over-permissioned job, or moved release tag.

**Decision**: Pin every Action to a full commit SHA with a release-tag comment, pin the uv tool
version, allow only GitHub-owned Actions plus `astral-sh/setup-uv`, and enable repository-wide
full-SHA enforcement after the pinned workflow is merged. Give build jobs read-only tokens and
centralize Release writes in one tag-only publisher after the complete asset set is verified.
Monitor uv and Actions through Dependabot; run CodeQL when the repository is public. Require PRs
and current CI for `main`, block main deletion/force-push, and block semantic release-tag deletion
or movement through repository rulesets with no standing bypass.

**Rationale**: Immutable identities and a narrow allowlist reduce upstream substitution risk.
Separating build and publication removes write credentials from untrusted PR build paths.
Rulesets preserve a review/check trail without requiring a second maintainer's approval for this
currently single-maintainer project.

**Trade-offs**: Dependabot must deliberately update both SHA and version comments. Hosted-runner
major-version changes need real CI verification. A ruleset with zero required approvals prevents
direct pushes but cannot provide independent human review by itself. Public-only security
features must be enabled immediately after visibility changes rather than proven while private.

**Consequences**: `.github/rulesets/` stores importable, tested policy definitions, but their
server-side enforcement remains a launch operation. See
`reports/security-2026-08-11-github-hardening.md`.
