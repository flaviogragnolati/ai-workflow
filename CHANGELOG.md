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
- Contract and validation support for active internal companion skills that are
  reachable by owning agents without exposing a user invocation surface.
- Active `$explore` routing for read-only, repository-grounded orientation over
  codebases, modules, features, and documents, with transient non-artifact output.
- Active optional `$audit-docs` routing for evidence-backed QA of durable project
  documentation, with read-only transient findings and owner-routed remediation.
- Active `$reporting-workflow` orchestration for progress, feature, milestone,
  release, completion, consulting, executive, and custom reporting from approved
  versioned artifacts, with root-writer delegation and return routing.
- Active `$reporting-source-design` ownership of the structured, schema-backed
  semantic report source and active `$generate-report` rendering to Markdown,
  DOCX, and PDF.
- Report-source schema semantics and valid/invalid fixtures covering snapshot
  approval, source authority, stable IDs, and evidence eligibility.
- A conditional web-stack recommendation owned by
  `technical-foundation-definition`: T3 Core as the preferred starting point for
  suitable greenfield web applications, with Zod, Zustand, shadcn/ui, React Hook
  Form, and one of Drizzle or Prisma evaluated as secondary candidates.
- A technical-foundation artifact template for versioned stack selections,
  project commands, adopted recommendations, pitfalls, antipatterns, NFR fit,
  and precise external-source provenance.

### Changed

- The planned, non-invocable `cleanup-docs` identifier was replaced before
  activation by the clearer `audit-docs` name; no compatibility alias or
  migration is required.
- Removed an obsolete third-party provenance assertion and its corresponding
  package-validator requirement after ownership was confirmed.
- Maintenance routing and validation now resolve the repository-root layout
  consistently, including the canonical manifest, shared contract, and validator.
- `writing-for-agents` is now a non-user-invocable internal companion for skills,
  agent instructions, durable intermediates, handoffs, temporary artifacts, and
  generated references. Its artifact-contract workflow retains the original
  context-pointer, information-hierarchy, completion, leading-word, and pruning
  mechanics without restoring incompatible invocation behavior.
- The AI coding workflow now coordinates six planning stages, selective
  refinement, optional tickets and TDD, implementation, change-scoped technical
  and comment review, release-candidate QA, and delivery.
- Stages return structured deltas while the workflow orchestrator remains the
  only writer of global workflow state and the artifact index.
- Development records distinguish durable execution sources from transient
  scratchpads, internal plans, and delegation messages.
- Accepted commercial scope and released artifacts are changed through explicit
  change control instead of in-place rewrites.
- Reporting now uses one approved semantic source for document and presentation
  channels; Markdown, DOCX, PDF, and PPTX outputs remain derived with no semantic
  authority and require regeneration after source changes.
- `generate-quasar-deck` now distinguishes PPTX and PDF artifacts, requires a
  baselined source for released reporting channels, and returns a structured
  stage delta for orchestration.
- Delegated subworkflows inherit a root orchestrator and return composite deltas,
  preserving one global writer for project state and the artifact index.
- Manifest validation now verifies active workflow entry skills, stage and
  renderer ownership, and optional next routes in addition to skill registration.
- Development and integral QA are now profile-driven rather than T3-only.
  `technical-foundation-definition` owns the selected project profile and
  downstream stages route contradictory evidence back to that owner.
- Workflow state can carry `technical_foundation_ref` as an exact artifact ID and
  version; downstream state requires it once technical foundation work is complete.
- Planning, refinement, implementation, debugging, TDD, and review procedures now
  discover project tooling and consume applicable profile guidance instead of
  assuming TypeScript-specific commands.
- `codebase-review` now combines generic software criteria, the selected project
  profile, repository standards, and current official technology sources. The
  previous project-specific T3 and library checklists were removed from shared
  runtime context.

### Compatibility

- `project-defined` is the active development compatibility profile. Existing
  runtime states using `stack_profile: t3-core` remain valid during migration;
  after technical-foundation reconciliation they should add an exact
  `technical_foundation_ref`. Baselined project artifacts are versioned or
  superseded rather than rewritten in place.
- Non-T3 projects may use the full development workflow. Missing stack-specific
  evidence must be reported as a bounded coverage gap, and no skill may issue a
  false technology-specific approval.
- Direct user invocation of `$writing-for-agents` is no longer supported. Route
  writing work through its owning task; repository instructions or the owning
  skill load the internal companion when the target is agent-consumed.
- DOCX and PDF report rendering requires a compatible document runtime. Missing
  requested formats block full completion or require an explicitly approved
  partial release; Markdown alone never implies unavailable binary coverage.
