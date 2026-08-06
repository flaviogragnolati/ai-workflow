---
name: ai-coding-workflow
description: "Orchestrate Quasar product planning, T3 implementation, change-scoped review, integral QA, and delivery. Use to start, resume, route, or validate the full AI coding workflow, execute a named planning stage, coordinate development from a backlog item, or recover project state."
---

# AI coding workflow

Read `../../skill-manifest.yaml` and `../../00-cross-workflow-contract.md` before routing. Remain the single writer of `00-workflow-state.yaml` and `00-artifact-index.yaml`.

## Preconditions

1. Load project state, artifact index, baselines, decisions, risks, and open change requests.
2. Accept either a product idea or a versioned proposal contract. Do not fabricate a commercial contract when work starts from an idea.
3. Confirm `stack_profile: t3-core`. Record the concrete framework, ORM, runtime, and versions through `technical-foundation-definition`.
4. Stop with an explicit coverage blocker for a non-T3 project.

## Planning stages

Run only the stage needed by current state or `target_stage`:

1. `product-core-definition`
2. `technical-foundation-definition`
3. `domain-data-modeling`
4. `high-level-architecture-standards`
5. `module-feature-decomposition`
6. `backlog-and-delivery-planning`

Do not duplicate stage templates or domain procedure here. Validate each returned `stage_result`, then apply its delta to state and index.

Stage 6 closes initial app-flow only when the high-level backlog contains milestones, epics, known features or workstreams, checkpoints, primary dependencies, readiness, and a selectable next front. Tickets and exhaustive task detail are not exit criteria.

## Development loop

For each selected backlog item:

1. Check whether it is sufficiently defined.
2. If refinement is needed, choose one depth:
   - `design-grill` for broad or cross-cutting architecture;
   - `feature-grill` for a bounded feature with meaningful complexity;
   - `simple-grill` for a small contained change.
3. Skip a grill when the item is already execution-ready.
4. Ask whether distribution, a tracker, or multiple executors justify durable tickets.
5. Run `to-tickets` only when useful. A single executor may continue from the ready backlog item, issue, or implementation plan.
6. Run `implement`. Keep its internal plan, scratchpad, and delegations transient.
7. Require verification proportional to acceptance criteria. Enable `tdd` only when requested or explicitly selected.
8. Run a mini review:
   - `code-review` for technical and specification conformance;
   - `review-code-comments` for affected comments and docstrings.
9. Correct failures and update the original durable record: ticket when present, otherwise the selected backlog item, issue, or explicit plan.
10. Integrate or continue. Do not create a parallel durable implementation diary.

Backlog changes discovered during development return to `backlog-and-delivery-planning` in `targeted-refinement` or `replan-and-synchronize` mode.

## Integral QA and delivery

Run integral QA on a release candidate, not on each diff. Create or update:

- `07-release-candidate.yaml`;
- `07-integral-validation.md`;
- `08-delivery-manifest.yaml`;
- `08-release-notes.md` when applicable.

Cover architecture, integrations, critical flows, security, relevant NFRs, migrations, deployment, delivery documentation, and UAT or acceptance when applicable. Do not treat `codebase-review` alone as acceptance; reconcile all relevant evidence and blockers.

After delivery, offer `generate-quasar-deck` as optional reporting. Upstream completion does not depend on reporting unless a project contract explicitly says so.

## Change control and recovery

When technical work affects accepted commercial scope, price, schedule, or commitments:

1. Create a change request with impacted IDs.
2. Keep the accepted release immutable.
3. Mark dependent artifacts stale.
4. Block affected work until the required decision.
5. Regenerate derivatives after approval.

On resume, rebuild context from state, index, baselines, decisions, risks, blockers, and housekeeping. Do not reopen closed decisions without new evidence.

## Completion response

Return current outcome, changed artifact IDs, validations, warnings, blockers, reconciled state, and one next action. A directly invoked stage remains standalone and never changes global state.
