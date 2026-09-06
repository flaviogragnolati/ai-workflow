---
name: q-delivery-workflow
description: "Orchestrate Quasar product planning, profile-driven implementation, change-scoped review, release engineering, integral QA, and delivery. Use to start, resume, route, validate, or report the current position of the full AI coding workflow, execute a named planning stage, coordinate development from a backlog item, or recover project state. Requires the q-core-contract companion."
---

# AI coding workflow

Read the `q-core-contract` companion for shared governance; if it is missing, stop and install it with `npx skills add flaviogragnolati/ai-workflow --skill q-core-contract`. Load `skill-manifest.yaml` for routing when the package registry is available, otherwise load the companion's generated `references/routing.md`; do not load both by routine. Remain the root orchestrator and single global state writer while delegating any subworkflow.

## Preconditions

1. Inspect whether this run's state and index exist under `docs/development-workflow/`. For an authorized new run or a `workflow-start-request`, follow the contract's Workflow initialization reference; reuse the confirmed starting point and boundary. For an existing run, read `00-workflow-state.yaml` first, inspect only the artifact-index entries it references, and discover every pending standalone stage-result sidecar under that root. Then load the active record, exact source versions, decisions, risks, and open change requests needed by the selected route. A read-only status query stops after the evidence needed to report position and pending reconciliation; it does not initialize a run, apply a delta, delete a sidecar, or rewrite state.
2. Accept either a product idea or the accepted proposal version (its commercial release, exact `02-proposal-source.yaml` ID and version). Do not fabricate a commercial reference when work starts from an idea.
3. Require workflow state to use `stack_profile: project-defined`, then load `technical_foundation_ref` and, for work that touches a user interface, `design_system_ref`, each at its exact artifact version when it exists.
4. Route missing or stale technical selections to `q-plan-tech-foundation`. Block only on an unresolved requirement, decision, execution capability, or evidence gap that makes the next action unsafe.

Reuse content already read while its exact version and file remain unchanged. Expand the loaded slice only for a contradiction, changed reference, concurrent edit, insufficient evidence, or uncertain recovery; never treat a timestamp alone as proof that cached meaning is current.

## Planning stages

Run only the stage needed by current state or `target_stage`:

1. `q-plan-product-core`
2. `q-plan-tech-foundation`
3. `q-plan-domain-model`
4. `q-plan-architecture`
5. `q-plan-features`
6. `q-plan-backlog`

Stage 5b, `q-plan-design-system`, runs between stages 5 and 6 only when it applies. Existing stage numbers do not shift.

Do not duplicate stage templates or domain procedure here. Validate each returned `stage_result`, then apply its delta to state and index.

Plan progressively from the first useful increment and its cross-cutting constraints. Keep later outcomes and uncertainties visible without loading or specifying their full context in advance. An existing brief or repository may satisfy part of a stage; the owner verifies and adopts that evidence instead of restarting discovery. Missing commands in a new repository become bounded bootstrap work, not invented technical evidence.

At each planning boundary, distinguish completed work, confirmed decisions, and artifact lifecycle. Obtain only the owning stage's required material decisions that remain unresolved; reuse confirmations whose scope and evidence still apply. After validation and those decisions, mark the exact sufficient output versions consumed downstream `Baselined` and record their approval references. When the meaning was already explicitly approved, reconciling its artifact version adds no decision turn. Keep blocked or unapproved meaning `Working`; a stage returning `completed` alone never establishes approval. A named `target_stage` stops at its requested boundary; otherwise continue within the authorized planning scope to the next unresolved decision.

After `q-plan-tech-foundation` completes, reconcile the returned artifact ID and version into `technical_foundation_ref`. If a later stage discovers a stack contradiction, mark the referenced version stale when appropriate and route `reconcile-and-update` to its owner; do not let another stage edit the technical foundation.

After `q-plan-features`, decide the design-system route from one question: does the product have a durable visual interface whose reusable design decisions outlive a single feature? Route to `q-plan-design-system` when it does or when the answer is unclear, and let that stage own the full applicability criteria and confirm the disposition. When it plainly does not — a headless API, worker, infrastructure, CLI, or throwaway prototype — record `stage_status: not_applicable`, keep `design_system_ref` null, and continue to `q-plan-backlog`.

Reconcile an assessment that excludes a minimal interface as `not_applicable`, not as a completed design-system artifact. Pass the recorded disposition to code and review consumers under the contract's Design system reference rules.

Reconcile a completed run into `design_system_ref` as an artifact ID and version, and register both the specification and its token set in the index. If the user declines an applicable stage, record that omission as a decision plus any warranted risk; never write it as `not_applicable`. Do not treat an unvalidated token set as a missing artifact: carry its declared coverage gap forward to implementation and QA.

Stage 6 closes initial app-flow only when the high-level backlog contains milestones, epics, known features or workstreams, checkpoints, primary dependencies, readiness, and a selectable next front. Tickets and exhaustive task detail are not exit criteria.

## Exploration and orientation

Route to `q-code-explore` when the user asks for a high-level understanding of a codebase, module, feature, or document, for a map exactly one abstraction level above a named code location, or when a specific question requires repository-grounded orientation before another stage. Supply the current target and question as its lens. Treat its summary as transient context: do not register it as an artifact, use it as stage-completion evidence, or run it as routine ceremony when the needed context is already available.

Use `q-code-research` for bounded technical questions and a durable Findings Register that follows the shared cited-findings contract, and `q-review-codebase` for a formal quality audit. Technical research may return an orchestrated delta, but it does not run the engagement-research workflow or open Proposal.

When `user-requests-standalone-database-schema-migration-or-performance-analysis` and `q-tool-database-schema` is installed, route the bounded read-only request to it without changing active stage ownership. Route domain meaning to `q-plan-domain-model`, stack selection to `q-plan-tech-foundation`, durable physical decisions to `q-plan-architecture`, execution to implementation or debugging, and audit findings to the applicable review owner. If the tool is absent, `route-to-the-current-domain-architecture-refinement-debug-or-review-owner-with-database-capability-gap`.

## Optional structured ideation

When `user-requests-structured-ideation-before-product-core-opportunity-discovery-on-the-existing-product-or-a-bounded-technical-option-set` and `q-ideation-session` is installed, route that session to it with the decision, its owner, and the versioned inputs, then record one adoption disposition from the contract's structured-ideation section before any stage consumes the result. `q-plan-product-core` may receive a selected option, an outcome hypothesis, and assumptions; technology and architecture options return to `q-plan-tech-foundation` or `q-plan-architecture`. A candidate never becomes a requirement, a business rule, an ADR, or a stack selection. If it is absent, `continue-with-the-owning-planning-stage-and-record-the-unexplored-option-space-as-a-gap`.

## Optional engagement research

When planning exposes an external uncertainty that materially affects a product or technology decision and the project's own evidence cannot resolve it, offer delegation to `q-research-workflow`. Start it only after the user authorizes the questions, boundary, privacy treatment, and budget. Pass `root_orchestrator: q-delivery-workflow`, `global_state_writer: q-delivery-workflow`, and an exact `return_to`; remain the global state writer and reconcile its composite delta.

After Research returns, obtain one explicit disposition:

- `adopt-as-planning-input` — route the exact Research Baseline ID and version to `q-plan-product-core` or `q-plan-tech-foundation`, whichever owns the affected meaning, to register as `external-research`;
- `retain-as-independent` — preserve the research artifacts without using them in this delivery;
- `defer-decision` — keep the disposition unresolved and block only the planning commitment that depends on it.

Research never edits a planning artifact and never opens a planning stage by itself. Treat its claims and synthesis as supporting evidence; the planning owners retain their declared authority.

## Development loop

For each backlog item the user selects — or confirms from the backlog's next recommended front — set `active_front.item_ref` to that exact item ID or locator and version and `active_front.record_ref` to the current durable execution record. Until a separate plan or ticket exists, use the item itself as `record_ref`; do not invent another identifier. Then:

1. Check whether it is sufficiently defined and load the referenced technical foundation, application standards, and relevant ADRs.
2. If refinement is needed, choose one depth:
   - `q-code-grill-design` for broad or cross-cutting architecture — it yields a feature architecture document, not an executable plan; route the next slice it names, at the depth its `next_recommended_action` states, back through this step (`q-code-grill-feature`, `q-code-grill-simple`, or `q-code-implementation-plan`);
   - `q-code-grill-feature` for a bounded feature with meaningful complexity;
   - `q-code-grill-simple` for a small contained change;
   - `q-code-implementation-plan` when direction is settled and only the file-level sequence is missing.
3. For a defect item — failing, broken, slow, or incorrect behavior in work that is not yet `Released` — skip the grill: route `q-code-debug` when the cause is not confirmed, or `q-code-fix` when the cause and correction are confirmed; either ends with the mini review and the durable-record update, and a correction that alters product behavior, architecture, or a cross-module contract is reclassified as change work and re-enters at step 2 (the reclassification rule those skills state). Then continue at step 10.
4. Skip a grill when the item is already execution-ready.
5. Determine ticket need from an explicit tracker request, an established project preference, or a concrete distribution, multi-executor, or cold-start continuity need. Ask only when an unresolved tracker or publication choice materially changes execution.
6. Run `q-code-tickets` only when that trigger is present. A single executor with a sufficient durable record continues without a ticket decision turn.
7. Run `q-code-implement`. Keep its internal plan, scratchpad, and delegations transient.
8. Require verification proportional to acceptance criteria. Enable `q-code-tdd` only when requested or explicitly selected.
9. Run the mini review — required; an executor whose reviewer is not installed returns a blocker naming it, and the item stays open until the review runs:
   - `q-review-code` for technical and specification conformance;
   - `q-review-comments` for affected comments and docstrings; its remove and rewrite findings are applied before the item closes.
10. Correct failures and update the original durable record: ticket when present, otherwise the selected backlog item, issue, or explicit plan. Route any newly required technology selection back to `q-plan-tech-foundation`.
11. Integrate or continue. Do not create a parallel durable implementation diary.
12. Validate every `stage_result` the loop returns — from each grill, implementation plan, ticket set, implementation close, and fix or debug close — and apply its delta before selecting the next step or item: register authored plans, tickets, and feature architecture documents in the artifact index as `Working` with their declared authority; record decisions and ADRs; route each `stale_artifacts` entry to its owning stage; update `active_front.record_ref`; and convert the exact `next_recommended_action` into one actionable `next_action` plus `next_actor` (`agent`, `user`, or `external`). A recommendation never authorizes selection of another front.

Backlog changes discovered during development return to `q-plan-backlog` in `targeted-refinement` or `replan-and-synchronize` mode. A backlog item that a grill or plan cannot execute as approved — scope, priority, or acceptance criteria must change — returns there too; the item is the commitment, the plan is its execution record. When a grill-design result lists a canonical planning artifact under `stale_artifacts` — architecture, features, domain model, technical foundation, or design system — route reconciliation to that owning stage before the affected slice enters implementation; the feature architecture document never replaces the planning version.

`q-review-plan` is optional. Route to it when a multi-slice front, a milestone boundary, or release-candidate preparation warrants verifying implemented work against the approved plan chain — backlog item, implementation plan or feature architecture document, feature and module definitions, architecture and ADRs — and confirming that recorded deviations reached their owning artifacts. Supply the front or milestone ID, the exact artifact versions, and the repository baseline. Keep its diagnostic transient and unregistered; route each finding to its owner: replanning to `q-plan-backlog`, a contradicted canonical planning artifact to its owning stage, missing implementation back into this loop, and documentation health to `q-review-docs`. A clean conformance diagnostic is not release acceptance and not UAT evidence.

## Release, integral QA, and delivery

Route release engineering to `q-delivery-release` and integral validation to `q-review-release`; author no release artifact here. Run integral QA on a release candidate, not on each diff.

Carry the confirmed usage, audience, criticality, data and environment constraints from Product Core and Technical Foundation into candidate preparation. The release owner selects applicable evidence for that context; local or development use does not imply public deployment, and internal use does not waive material risk controls.

1. When the backlog front or a milestone marks a releasable increment, route `q-delivery-release` in `form-release-candidate` mode; on user confirmation mark `07-release-candidate.yaml` `Baselined`.
2. Route `q-review-codebase` over the release candidate scope.
3. Route `q-delivery-release` in `execute-release` and `coordinate-uat` modes; every environment and operation needs its own explicit approval, and human-executed steps enter the evidence with provenance.
4. Route `q-review-release` with the release candidate, audit, evidence, and the exact `technical_foundation_ref` and `design_system_ref`; mark `07-integral-validation.md` `Baselined` when it returns.
5. Decide acceptance: on `ready`, or on `ready_with_accepted_risks` with the user's confirmation of each risk, route `q-delivery-release` in `close-delivery` mode and mark `08-delivery-manifest.yaml` `Released`; on `blocked`, return each finding to its owner through the development loop and form a new release candidate version.

Do not treat `q-review-codebase` alone as acceptance; the validation reconciles all relevant evidence and blockers, and the acceptance decision is recorded here.

`q-review-docs` is optional. Route to it when the user requests extended documentation QA, when upstream change makes drift likely, or before a baseline or release whose risk warrants a documentation pass. Supply the active artifact IDs or explicit durable scope. Keep its diagnostic transient and unregistered; route any approved remediation to the owning skill and record the implemented change in the applicable workflow changelog or change-control record.

## Incidents and hotfixes

When a defect or incident is reported against a `Released` version, record it as a change-control entry with the impacted release, severity, and decision owner, and keep the released version immutable. Route diagnosis to `q-code-debug`, or `q-code-fix` when the cause is confirmed, scoped to that release's exact commit or tag, then the mini review. Route `q-delivery-release` to form and execute a hotfix release candidate — `release_kind: hotfix`, base the released version — and `q-review-release` at proportional scope; deliver the result as a new version. A rollback is a release operation formed, executed, and evidenced by `q-delivery-release`. Return the root cause to `q-plan-backlog` in `targeted-refinement` mode when the hotfix was a mitigation. Other client feedback on a `Released` version follows the contract's Client feedback rule: record it, then route a change to change control, a question to `q-ask-project`, and an acknowledgement to the delivery record or a completion report.

## Reporting checkpoints

At an explicit progress, feature, milestone, release, or completion reporting checkpoint, delegate to `q-report-workflow`. Pass the reporting request, candidate artifact IDs and versions, `root_orchestrator: q-delivery-workflow`, `global_state_writer: q-delivery-workflow`, and the exact `return_to` stage or action.

Remain the global state writer, validate the composite reporting delta, and reconcile its approved artifacts after the subworkflow returns. Do not mark upstream completion from a report, and do not let reporting replace the active development stage. After delivery, reporting may instead run as the next root workflow. Reporting is optional unless a project contract explicitly requires it.

## Change control and recovery

When technical work affects accepted commercial scope, price, schedule, or commitments:

1. Create a change request with impacted IDs.
2. Keep the accepted release immutable.
3. Mark dependent artifacts stale.
4. Block affected work until the required decision.
5. Regenerate derivatives after approval.

On resume or "continue delivery", resolve continuation in this order: blockers that prevent progress, every pending sidecar, work inside the authorized `active_front`, then selection of another backlog front by the user. Inspect all sidecars under `docs/development-workflow/`, validate each one, and apply compatible deltas once before continuing; summarize the batch and delete a successfully applied sidecar only after the updated state and index validate. Keep a malformed, stale, or contradictory sidecar in place with a localized diagnostic and route semantic conflicts to the owner. State or index files outside that artifact root do not belong to the run and must not be used as workflow state. Do not reopen closed decisions without new evidence.

Workflow-state schema `1.1` adds `active_front` and `next_actor` for `ai-coding`. For an older state, recover the exact item and record references from the durable record and current evidence on the next authorized resume write. If more than one front remains plausible, keep `active_front: null`, set the user decision as `next_action`, and do not guess. Keep `active_front` null before selection and clear it when the workflow completes or closes. In `not_started`, `working`, or `blocked`, keep `next_action` non-empty and name its actor; `completed` or `closed` may use null when no continuation remains. Closing one stage does not complete the workflow.

A pure "where are we?" query is a Read-only status query: report pending sidecars without applying or deleting them. A nearby technical question keeps its current owner and does not start delivery housekeeping merely because it reads workflow state.

Before executing a selected step, check coherence using the already loaded state, index entries, and active record: the stage and action agree, each required reference resolves to its exact version, and implementation has an authorized front and technical foundation. Resolve a nested item against its owning backlog or ticket record, not a fabricated artifact-index entry. Reuse valid resolutions until their evidence changes; do not scan unrelated artifacts, build another continuity register, or load the package validator during project execution. An ambiguous recovery remains blocked on the affected action instead of guessing.

## Anti-patterns

| # | Anti-pattern | How it shows up | Correct behavior |
|---|---|---|---|
| 1 | Reimplementing a stage in the coordinator | The workflow authors architecture, backlog detail, or code instead of routing the registered owner. | Select the narrow skill, validate its result, and reconcile the delta. |
| 2 | Mandatory refinement ceremony | Every backlog item is forced through a grill, tickets, and TDD regardless of readiness or risk. | Use only the refinement and verification that the item actually needs. |
| 3 | Treating one audit as release acceptance | A clean `q-review-codebase` report is used as the whole delivery gate. | Reconcile tests, UAT, security, deployment, profile freshness, and other applicable evidence. |
| 4 | Writing a second execution diary | Implementation scratch notes become a durable record beside the selected item or ticket. | Update the original durable execution source and keep coordination transient. |
| 5 | Loop output outside the state machinery | A grill plan, ticket set, or implementation close is written and the loop moves on without a validated `stage_result`, so the artifact never enters the index. | Treat every loop step as a stage: validate its delta and reconcile it before the next step. |
| 6 | Executing or accepting a release on inferred approval | A staging approval is read as production approval, or a clean audit becomes the delivery decision. | Obtain per-environment approval, reconcile the validation verdict, and record the acceptance decision. |

## Completion response

Return a compact derived status view: current stage and active front, sufficient evidence links, blockers or exceptions, one next action with its actor, whether user intervention is needed, and how to resume. Keep detailed evidence in its durable record and do not print the complete state YAML or empty result lists by default. A directly invoked stage remains standalone, reports pending reconciliation, and never changes global state.
