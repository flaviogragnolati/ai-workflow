# Cross-workflow contract

## Purpose and authority

Use this contract for governance shared by every Quasar workflow. Use `skill-manifest.yaml` for discovery and routing, each `SKILL.md` for stage procedure, and project runtime files for execution state. When they conflict, apply this order:

1. `skill-manifest.yaml` for package identity, paths, status, side effects, and routing.
2. This contract for shared lifecycle, ownership, authority, and change control.
3. The owning skill for domain procedure.
4. Project state and approved artifacts for the current execution.
5. `README.md` and diagrams as explanatory views.

Do not copy this contract into individual skills. Link to it and add only skill-specific rules.

## Invocation and routing

Invoke one orchestrator and name the target stage:

```text
Use $ai-coding-workflow to execute backlog-and-delivery-planning.
```

Treat a stage name supplied with an orchestrator as `target_stage`, not as a second independent invocation. The orchestrator must load the manifest before routing.

The user-invoked or project-owning orchestrator is the **root orchestrator**. It may delegate a registered subworkflow while remaining the only global state writer. Pass `root_orchestrator`, `global_state_writer`, and `return_to` in the orchestration context. A delegated subworkflow routes its owned stages, validates their results, and returns one composite delta with `global_state_updated: false`; it does not replace the caller's active workflow state. When a workflow such as reporting is invoked directly for the project, its entry skill is the root orchestrator.

A stage invoked directly runs in standalone mode. It may write its owned domain artifacts, but it must not mark a global workflow stage complete or silently update the workflow state or artifact index.

An active skill with `invocable: false` and `execution_modes: [internal]` is an internal companion, not a direct user entry point. It must be reached through a strong context pointer in `AGENTS.md` or an owning skill, inherit the caller's authority and write scope, produce no independently authoritative project artifact, and expose no `agents/openai.yaml` invocation surface.

## Single-writer rule

The root orchestrator is the only writer of:

- `00-workflow-state.yaml`;
- `00-artifact-index.yaml`;
- cross-workflow stage completion and recovery status;
- reconciled traceability, decision, and risk deltas when those registers are managed centrally.

A stage owns its domain artifacts and returns a structured delta. A delegated subworkflow may aggregate owned stage deltas but cannot apply them globally. The root orchestrator validates the resulting delta, reconciles IDs and dependencies, then updates state and index.

Research, prototype, review, rendering, and other tools must not commit, publish, message external systems, or change remote state unless the manifest policy and the current user authorization allow that side effect.

## Stage result

Return this structure from every orchestrated or standalone stage:

```yaml
schema_version: "1.0"
stage_result:
  skill_id: "skill-id"
  mode: "orchestrated"
  outcome: "completed"
  authored_outputs: []
  derived_outputs: []
  updated_outputs: []
  references_added: []
  traceability_delta: []
  decisions_added_or_updated: []
  risks_added_or_updated: []
  stale_artifacts: []
  blockers: []
  warnings: []
  required_user_actions: []
  next_recommended_action: null
orchestration:
  mode: "orchestrated"
  global_state_updated: false
  reconciliation_required: true
```

Use `completed`, `completed_with_warnings`, or `blocked` for `outcome`. A stage always reports `global_state_updated: false`; only the orchestrator changes it to true after applying the delta. In standalone mode, keep `reconciliation_required: true`.

Validate the result against `schemas/stage-result.schema.yaml`.

## Artifact ownership and authority

Register every persistent project artifact in the artifact index with:

- `artifact_id`;
- `artifact_type`;
- `path`;
- `owner_workflow`;
- `owner_skill`;
- `creation_mode: authored | derived`;
- `semantic_authority: canonical | supporting | none`;
- `authority_scope` when authority is partial;
- `lifecycle`;
- `version`;
- `source_refs`;
- generation provenance when `creation_mode: derived`.

Use these lifecycle states:

- `Working`: mutable and not yet baselined.
- `Baselined`: approved input for downstream work.
- `Released`: immutable delivery or accepted commercial release.
- `Superseded`: replaced by a newer version and retained for traceability.
- `Archived`: no longer active, retained outside the active working set.
- `Transient`: never added to the artifact index.

An authored artifact may be canonical only for a declared scope. A derived artifact must reference its sources and cannot silently change their meaning.

## Diagram authority

Classify diagrams explicitly:

| Artifact | Creation mode | Semantic authority |
|---|---|---|
| Package workflow diagram in `README.md` | authored explanatory view | none |
| Domain or architecture Mermaid source | authored | supporting |
| Domain narrative, dictionary, ADR, or standards text | authored | canonical for its declared scope |
| SVG, PNG, or PDF rendered from Mermaid | derived | none |

Mermaid is the canonical source of the visual representation, not the canonical source of domain or architectural semantics. No critical rule may exist only as an unlabeled visual edge.

## Decisions, risks, and changes

Reuse stable IDs. Do not reopen a resolved decision without new evidence or an objective contradiction.

When new information affects an accepted or baselined upstream artifact:

1. Record a change request or decision with impacted IDs.
2. Mark affected downstream artifacts stale when appropriate.
3. Do not rewrite an accepted commercial release in place.
4. Obtain the approval required by the manifest before changing priority, scope, price, schedule, or another commitment.
5. Regenerate derived outputs from the corrected canonical source.

A gate may return work to the owning stage. Record the return in state, a decision/risk register, or a change request. Diagrams may show this with one shared feedback note instead of one arrow per gate.

## Durable and transient development records

Treat these as durable when they exist:

- the selected backlog item;
- a workflow implementation plan created before execution;
- tracker or Markdown tickets;
- release-candidate, integral-validation, delivery-manifest, and release-note artifacts;
- the original issue or explicit execution record when no ticket exists.

Treat the implementer's scratchpad, internal plan, delegation messages, and subagent coordination as transient. `implement` must update the original durable execution record and must not create a second durable work diary.

Tickets and TDD are optional. Verification proportional to the change and its acceptance criteria is required. After implementation and verification, run a change-scoped technical review and comment/docstring review. Run integral QA later against a release candidate.

## Stack compatibility

The package development profile is `t3-core`. `technical-foundation-definition` records the project's concrete selections and versions. Technical skills must stop or declare missing coverage for a non-T3 project; they must not issue a false approval.

## Reporting

Reporting is optional and does not change upstream completion criteria. `reporting-workflow` accepts explicit, versioned artifact references from discovery, proposal, planning, implementation, validation, delivery, consulting, or another registered workflow. Resolve them through the artifact index and load only the approved reporting scope.

`reporting-source-design` owns the single semantic source for a reporting run. It is canonical only for report selection, narrative, and approved interpretation; upstream artifacts retain authority over their facts, commitments, decisions, risks, and delivery status. A `Working` artifact may support planning, but its exact version must be baselined, released, or explicitly approved as a reporting snapshot before the report source is baselined.

`generate-report` and `generate-quasar-deck` consume the same baselined report source when they run as reporting channels. Their Markdown, DOCX, PDF, and PPTX outputs are derived with no semantic authority. A manual semantic edit returns to `reporting-source-design`, creates a new approved source version, and makes affected channels stale. Generation or release approval never authorizes publication or external sending.

When another workflow delegates progress, feature, milestone, release, completion, or other reporting, that workflow remains root orchestrator and reconciles the composite reporting delta. Direct standalone renderers never write workflow state or the artifact index.

## Manual DOCX reconciliation

Do not implement partial hashes or editable-field tracking in this version. When a proposal DOCX is edited manually, reintroduce the edited file to `commercial-proposal-document`, reconcile it with canonical sources, and regenerate affected derivatives.

## Validation

Before completing package work:

1. Run `python3 skills/scripts/validate-skills-package.py` from the repository root.
2. Run the official `quick_validate.py` for every active skill.
3. Run affected script tests and `--help` checks.
4. Verify local links and references.
5. Record acceptance evidence outside `SKILLS`.

Do not store temporary QA output inside a skill directory.
