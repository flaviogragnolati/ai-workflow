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

- `q-ask-project`, a read-only project-question skill that conditionally aligns
  ambiguous questions, reconciles documented intent, workflow state, artifact
  authority, and observable implementation, and returns only a transient answer.
- `q-ask-analyze`, a read-only extension of the same alignment and evidence path
  for multidimensional proposal fit, benefits, downsides, risks, problems,
  compatibility, alternatives, confidence, and an optional next routing choice.
- The public `ask` group, matching skills.sh catalog section, dependency guidance,
  and package acceptance scenarios for conditional alignment, answer-only behavior,
  compatibility qualification, and planning boundaries.
- A README quick skill guide that maps proposal, the six planning stages,
  iterative development, mini review, integral QA, delivery, reporting,
  cross-cutting support, and package maintenance to the relevant skills. Its
  Mermaid overview and decision table are explicitly derived routing aids;
  `skill-manifest.yaml` remains the authoritative registry.
- `q-core-contract`, the shared governance companion. The cross-workflow
  contract moved from `skills/00-cross-workflow-contract.md` into
  `skills/core/q-core-contract/SKILL.md`, and the `stage-result` and
  `report-source` schemas moved into its `references/`, so the 17 coordinated
  workflow skills can reach shared governance from an installed catalog. It is
  `invocable: false` and `distribution: public`: a companion, not an entry point,
  but shipped to every consumer that installs a skill requiring it.
- `references/routing.md` in `q-core-contract`, a derived routing digest for
  orchestrators that run from an installed catalog and cannot read
  `skill-manifest.yaml`. The validator regenerates and compares it on every run,
  so it can go stale but never becomes a second opinion.
- Manifest field `group`, the authoritative grouping. Skill name, skill folder,
  category folder, and the `skills.sh.json` sections all derive from it. Values:
  `proposal`, `delivery`, `plan`, `code`, `review`, `report`, `core`, `maint`.
- Manifest field `requires`, declaring the companions a skill cannot work
  without, with a validated dependency graph: a requirement must be registered,
  actually referenced in the body, and — for a public skill — backed by an
  integrity check that names the exact install command.
- Package validation for the new invariants: `name` equals `q-<group>-<leaf>`,
  the category folder equals `group`, every public skill names Quasar in its
  `description`, a one-level `../<sibling>/…` reference must be declared in
  `requires`, a public skill cannot require an internal one, and the routing
  digest must match the manifest.
- External distribution through the [skills.sh](https://skills.sh) CLI, so any
  Agent Skills client can install the catalog with
  `npx skills add flaviogragnolati/ai-workflow`. The repository already matched
  the required `skills/<category>/<name>/SKILL.md` catalog layout; the CLI
  discovers all skills without a structural change.
- `skills.sh.json` groups the public catalog into eight sections on the
  skills.sh repository page. It is a derived presentation of `group`;
  `skill-manifest.yaml` remains the authority for what exists.
- Manifest field `distribution` (`public` by default, `internal` for
  package-only skills), documented in the shared contract under
  External distribution. `SKILL.md` frontmatter `metadata.internal: true` is its
  derived view and the validator enforces both directions.
- Package validation for external distribution: `skills.sh.json` coverage
  against the manifest, distribution and frontmatter agreement, Agent Skills
  name rules, README installation guidance, and stray Windows
  alternate-data-stream files inside skills.
- Portability rule blocking a publicly distributed skill from referencing files
  outside its own directory, because installers copy one skill folder at a time.
  The rule shipped with a 18-entry allow list of known offenders; that list is
  gone and the rule is now unconditional.
- Package-level governance through `skill-manifest.yaml` and
  the shared cross-workflow contract, including routing, ownership, lifecycle,
  semantic authority, approvals, and the orchestrator single-writer rule.
- Coordinated workflows for discovery and commercial proposals, AI coding and
  delivery, and optional reporting.
- Schema-backed workflow state, artifact index, and stage-result contracts with
  valid and invalid fixtures.
- Package validation for registry consistency, skill metadata, Codex metadata,
  local links, artifact semantics, and cross-workflow acceptance scenarios.
- Administrative `$q-maint-ai-workflow` housekeeping for impact analysis,
  philosophy and anti-pattern review, synchronized package updates, and
  regression validation outside project runtime.
- Repo-scoped discovery for `$q-maint-ai-workflow` through
  `.agents/skills/q-maint-ai-workflow`, linked to its canonical package source.
- Shared maintenance instructions in `AGENTS.md`, with `CLAUDE.md` importing the
  same source for native Claude and Codex compatibility without duplicated rules.
- Contract and validation support for active internal companion skills that are
  reachable by owning agents without exposing a user invocation surface.
- Active `$q-code-explore` routing for read-only, repository-grounded orientation over
  codebases, modules, features, and documents, with transient non-artifact output.
- Active optional `$q-review-docs` routing for evidence-backed QA of durable project
  documentation, with read-only transient findings and owner-routed remediation.
- Active `$q-report-workflow` orchestration for progress, feature, milestone,
  release, completion, consulting, executive, and custom reporting from approved
  versioned artifacts, with root-writer delegation and return routing.
- Active `$q-report-source` ownership of the structured, schema-backed
  semantic report source and active `$q-report-document` rendering to Markdown,
  DOCX, and PDF.
- Report-source schema semantics and valid/invalid fixtures covering snapshot
  approval, source authority, stable IDs, and evidence eligibility.
- A conditional web-stack recommendation owned by
  `q-plan-tech-foundation`: T3 Core as the preferred starting point for
  suitable greenfield web applications, with Zod, Zustand, shadcn/ui, React Hook
  Form, and one of Drizzle or Prisma evaluated as secondary candidates.
- A technical-foundation artifact template for versioned stack selections,
  project commands, adopted recommendations, pitfalls, antipatterns, NFR fit,
  and precise external-source provenance.

### Changed

- **BREAKING — every skill ID changed.** IDs now follow `q-<group>-<leaf>`, so
  the catalog is recognizable and self-sorting inside a shared agent directory.
  Category folders were renamed to their group and skill folders to their new
  name; the repository is not flattened. The longest ID dropped from 33 to 26
  characters. There is no published package version, so no aliases were created
  — reinstall with the new names.

  | Old ID | New ID |
  |---|---|
  | `debug` | `q-code-debug` |
  | `explain` | `q-code-explain` |
  | `explore` | `q-code-explore` |
  | `simple-fix` | `q-code-fix` |
  | `design-grill` | `q-code-grill-design` |
  | `feature-grill` | `q-code-grill-feature` |
  | `simple-grill` | `q-code-grill-simple` |
  | `handoff` | `q-code-handoff` |
  | `implement` | `q-code-implement` |
  | `implementation-plan` | `q-code-implementation-plan` |
  | `resolve-merge-conflicts` | `q-code-merge-conflicts` |
  | `prototype` | `q-code-prototype` |
  | `research` | `q-code-research` |
  | `tdd` | `q-code-tdd` |
  | `to-tickets` | `q-code-tickets` |
  | `zoom-out` | `q-code-zoom-out` |
  | `ai-coding-workflow` | `q-delivery-workflow` |
  | `maintain-ai-workflow` | `q-maint-ai-workflow` |
  | `writing-for-agents` | `q-maint-writing-for-agents` |
  | `high-level-architecture-standards` | `q-plan-architecture` |
  | `backlog-and-delivery-planning` | `q-plan-backlog` |
  | `domain-data-modeling` | `q-plan-domain-model` |
  | `module-feature-decomposition` | `q-plan-features` |
  | `product-core-definition` | `q-plan-product-core` |
  | `technical-foundation-definition` | `q-plan-tech-foundation` |
  | `commercial-proposal-design` | `q-proposal-design` |
  | `proposal-discovery` | `q-proposal-discovery` |
  | `commercial-proposal-document` | `q-proposal-document` |
  | `interactive-web-proposal` | `q-proposal-web` |
  | `discovery-proposal-workflow` | `q-proposal-workflow` |
  | `generate-quasar-deck` | `q-report-deck` |
  | `generate-report` | `q-report-document` |
  | `reporting-source-design` | `q-report-source` |
  | `reporting-workflow` | `q-report-workflow` |
  | `code-review` | `q-review-code` |
  | `codebase-review` | `q-review-codebase` |
  | `review-code-comments` | `q-review-comments` |
  | `audit-docs` | `q-review-docs` |

- The planned, non-invocable `cleanup-docs` identifier was replaced before
  activation by the clearer `q-review-docs` name; no compatibility alias or
  migration is required.
- Removed an obsolete third-party provenance assertion and its corresponding
  package-validator requirement after ownership was confirmed.
- Maintenance routing and validation now resolve the repository-root layout
  consistently, including the canonical manifest, shared contract, and validator.
- `q-maint-writing-for-agents` is now a non-user-invocable internal companion for skills,
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
- `q-report-deck` now distinguishes PPTX and PDF artifacts, requires a
  baselined source for released reporting channels, and returns a structured
  stage delta for orchestration.
- Delegated subworkflows inherit a root orchestrator and return composite deltas,
  preserving one global writer for project state and the artifact index.
- Manifest validation now verifies active workflow entry skills, stage and
  renderer ownership, and optional next routes in addition to skill registration.
- Development and integral QA are now profile-driven rather than T3-only.
  `q-plan-tech-foundation` owns the selected project profile and
  downstream stages route contradictory evidence back to that owner.
- Workflow state can carry `technical_foundation_ref` as an exact artifact ID and
  version; downstream state requires it once technical foundation work is complete.
- Planning, refinement, implementation, debugging, TDD, and review procedures now
  discover project tooling and consume applicable profile guidance instead of
  assuming TypeScript-specific commands.
- `q-review-codebase` now combines generic software criteria, the selected project
  profile, repository standards, and current official technology sources. The
  previous project-specific T3 and library checklists were removed from shared
  runtime context.
- `q-maint-ai-workflow` and `q-maint-writing-for-agents` are `distribution: internal`
  and no longer appear to consumers installing the package. Repository
  maintainers reach them unchanged; `INSTALL_INTERNAL_SKILLS=1` still lists them.
- `README.md` documents installation, the `q-<group>-<leaf>` scheme, and the
  skill dependencies a consumer must install together.

### Removed

- Eight tracked `*:Zone.Identifier` Windows alternate-data-stream artifacts from
  the coding skills, which were being copied into every consumer installation.
  `.gitignore` now excludes them.
- `CROSS_SKILL_REFERENCE_DEBT` from the validator. The 18 listed skills are now
  self-contained or reach their companion through a declared dependency, so the
  rule is unconditional instead of allow-listed.
- The rule that forced every companion to `distribution: internal`. `invocable`
  and `distribution` are independent axes; the enforced invariant is now that a
  public skill may not depend on an internal one.
- `skills/00-cross-workflow-contract.md` and `skills/schemas/stage-result.schema.yaml`
  and `report-source.schema.yaml` as standalone package files; they now live
  inside `q-core-contract`.

### Compatibility

- The two `q-ask-*` additions are backward-compatible and do not change project
  runtime schemas or existing workflow routes. Install `q-core-contract` with
  `q-ask-project`; install both with `q-ask-analyze`, which reuses the former's
  alignment and evidence procedure.
- The skill rename is breaking and unaliased. An existing installation keeps
  working under its old folder names but receives no updates; reinstall with the
  new IDs from the table above. Saved prompts, scripts, and routing notes that
  invoke `$<old-id>` must be updated. Project runtime files that record a
  `skill_id`, `owner_skill`, `current_stage`, or `stage_status` key carry old IDs
  and should be migrated with the same table when those artifacts are next
  reconciled.
- Installing a coordinated workflow skill now also requires installing
  `q-core-contract`. A skill whose companion is missing stops and prints the
  install command rather than proceeding on assumed governance.
- `project-defined` is the active development compatibility profile. Existing
  runtime states using `stack_profile: t3-core` remain valid during migration;
  after technical-foundation reconciliation they should add an exact
  `technical_foundation_ref`. Baselined project artifacts are versioned or
  superseded rather than rewritten in place.
- Non-T3 projects may use the full development workflow. Missing stack-specific
  evidence must be reported as a bounded coverage gap, and no skill may issue a
  false technology-specific approval.
- Direct user invocation of `$q-maint-writing-for-agents` is no longer supported. Route
  writing work through its owning task; repository instructions or the owning
  skill load the internal companion when the target is agent-consumed.
- DOCX and PDF report rendering requires a compatible document runtime. Missing
  requested formats block full completion or require an explicitly approved
  partial release; Markdown alone never implies unavailable binary coverage.
