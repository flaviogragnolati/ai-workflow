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

- Package-level governance through `skill-manifest.yaml` and
  `00-cross-workflow-contract.md`, including routing, ownership, lifecycle,
  semantic authority, approvals, and the orchestrator single-writer rule.
- Coordinated workflows for discovery and commercial proposals, AI coding and
  delivery, and optional reporting.
- Schema-backed workflow state, artifact index, and stage-result contracts with
  valid and invalid fixtures.
- Package validation for registry consistency, skill metadata, Codex metadata,
  local links, artifact semantics, and cross-workflow acceptance scenarios.
- Administrative `$maintain-ai-workflow` housekeeping for impact analysis,
  philosophy and anti-pattern review, synchronized package updates, and
  regression validation outside project runtime.
- Repo-scoped discovery for `$maintain-ai-workflow` through
  `.agents/skills/maintain-ai-workflow`, linked to its canonical package source.
- Shared maintenance instructions in `AGENTS.md`, with `CLAUDE.md` importing the
  same source for native Claude and Codex compatibility without duplicated rules.

### Changed

- Removed an obsolete third-party provenance assertion and its corresponding
  package-validator requirement after ownership was confirmed.
- Maintenance routing and validation now resolve the repository-root layout
  consistently, including the canonical manifest, shared contract, and validator.
- The AI coding workflow now coordinates six planning stages, selective
  refinement, optional tickets and TDD, implementation, change-scoped technical
  and comment review, release-candidate QA, and delivery.
- Stages return structured deltas while the workflow orchestrator remains the
  only writer of global workflow state and the artifact index.
- Development records distinguish durable execution sources from transient
  scratchpads, internal plans, and delegation messages.
- Accepted commercial scope and released artifacts are changed through explicit
  change control instead of in-place rewrites.

### Compatibility

- Development and integral QA are currently limited to the `t3-core` stack
  profile. Unsupported stacks must produce an explicit coverage blocker rather
  than a false approval.
