# Changelog

All notable changes to the Quasar AI delivery skills package are recorded here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
future package releases should use [Semantic Versioning](https://semver.org/).

This changelog was restarted on 2026-08-19 at the prerelease baseline described under
Unreleased; the package has no v0 release yet, and the entries written before that date
were retired — the Git history is their record. Every bullet starts with the ISO date it
landed (the commit date, not a release date), states the change in one sentence, and keeps
details in at most three sub-bullets under Added, Changed, Fixed, or Removed. Add a dated
release heading only when the package version and release boundary are deliberately
established.

## [Unreleased]

### Added

- **2026-08-19** — Added a contract rule for post-release client feedback (record, then route by kind; never edit a `Released` version) with the matching paragraph in the delivery, consulting, and proposal orchestrators, and stated once that no skill estimates effort (audit item 8).
- **2026-08-19** — Wired verified PDF/DOCX/XLSX extraction into `q-research-investigate` and `q-proposal-discovery`, humanizer into the three prose authors (`q-proposal-design`, `q-report-source`, `q-consult-intervention`) and the authored copy of `q-report-deck` and `q-proposal-web`, gave `q-tool-database-schema` a request schema, fixtures, and integration contract, added contract sections for database-schema and prose delegation, and let `ai-coding` delegate research (`adopt-as-planning-input`) (audit G5, G6, C8 residue, G8).

### Changed

- **2026-08-19** — Made the human documentation teach the package by workflow: the root README now presents the six workflow ids with a start-here table, an approval-gate map, an example artifact tree, a glossary, the language convention, and motivated invariants; added guides for `ask`, `ideation`, `core`, and `maint` (audit § 6, roadmap item 7).
- **2026-08-19** — Defined where each root workflow run keeps its state and index (`docs/<workflow>-workflow/`), named the four release records and the single term "accepted proposal version", listed the artifact roots the standalone-persistence rule discovers, and gave a standalone ideation approval its record (audit G4/D-j, G8).
- **2026-08-19** — Made the mini review enforceable without a hard dependency: `q-code-implement`, `q-code-fix`, and `q-code-debug` now declare `q-review-code` and `q-review-comments` in `uses` with a blocker fallback; fix and debug return a `stage_result` and require `q-core-contract`; the delivery loop routes defect items to fix or debug; the contract states who selects the backlog item, the item → plan → ticket precedence, single authorship of acceptance criteria, and the grill / `targeted-refinement` distinction (audit G1, G3, G7; deferred D-a, D-f).
- **2026-08-19** — Restarted this changelog at the prerelease baseline: commit `b217f92`, 67 skills (64 public), thirteen groups, six workflows, validator `Passed` with 0 errors and 0 warnings. Earlier entries are retired to Git history.
