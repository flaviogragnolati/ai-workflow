# Changelog

All notable changes to the Quasar AI delivery skills package are recorded here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
future package releases should use [Semantic Versioning](https://semver.org/).

This changelog begins with the current package baseline because no authoritative
earlier release history is available. Do not reconstruct older versions from file
timestamps; add a dated release only when the package version and release boundary
are deliberately established.

## [Unreleased]

### Added

- Added the public `q-tool-database-schema` capability for transient, profile-driven physical design, relational schema review, document-model review, migration design, and supplied-evidence performance analysis. It delegates no execution, preserves domain, stack, architecture, implementation, and review ownership, and ships verified PostgreSQL and MongoDB profiles.
- Added conditional database-schema collaboration to domain modeling, architecture, deep and feature refinement, implementation planning, debugging, change review, codebase review, and delivery routing, with explicit fallbacks when the optional tool is unavailable.
- Added the public, independently installable `q-tool-mermaid` capability for Mermaid creation, revision, validation, bounded repair, local SVG/PNG/PDF and optional ASCII/Unicode rendering, transactional Markdown compilation, structured requests/results, provenance, profiles, fixtures, and offline runtime checks.
- Added the `tool` manifest group and optional `uses` collaboration contract with schema, fixture, package-validation, trigger, fallback, distribution, self-use, and hard-dependency overlap checks.
- Integrated `q-plan-domain-model` and `q-plan-architecture` as hard Mermaid-tool consumers while preserving their semantic ownership, and added conditional collaboration to selected planning, code orientation, documentation review, proposal web, and report renderer skills.
- Added the public `q-review-skill` read-only diagnostic, the internal `q-maint-skill-quality` acceptance companion, and package regression scenarios for their core boundaries. The design adapts the useful context-value, progressive-disclosure, freedom-calibration, and usability ideas from Softaworks' MIT-licensed Skill Judge while replacing its fixed universal score with evidence, severity, target authority, and behavioral checks.

### Changed

- Removed `THIRD_PARTY_NOTICES.md` file-presence and content assertions from the package validator; provenance guidance remains unchanged.
- Advanced the manifest schema from `1.1` to `1.2` for the additive `tool` group and `uses` relationship. Existing `requires` semantics remain unchanged; optional consumers continue through their declared fallback when Mermaid is not installed.
