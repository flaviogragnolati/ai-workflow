# Delivery workflow guide

The `delivery` group holds two skills: `q-delivery-workflow`, the orchestrator of the AI-coding workflow, and `q-delivery-release`, its release engineering stage. The orchestrator routes a product idea or accepted software engagement through planning, iterative development, release, integral QA, and delivery, and it is the only writer of its own run's workflow state and artifact index, kept under the run's artifact root (`docs/development-workflow/`); another root run in the same project — a proposal, consulting execution, research, or reporting — keeps its own.

This guide is an explanatory view. [`skill-manifest.yaml`](../../skill-manifest.yaml) is the registry; each `SKILL.md` owns its procedure.

## How delivery flows

```mermaid
flowchart TB
    INIT["q-tool-init<br/>optional guided onboarding"] --> W
    IDEA["Product idea or internal brief"] --> W
    CR["Accepted commercial release<br/>(from Proposal)"] --> W["q-delivery-workflow"]
    W --> PL["Planning stages 1-6, plus 5b when it applies<br/>(plan group)"]
    PL --> B["High-level backlog"]
    B --> L["Development loop per backlog item<br/>(code group)"]
    L -->|"next item"| L
    L --> RC["q-delivery-release<br/>form release candidate"]
    RC --> AU["q-review-codebase<br/>audit over the candidate scope"]
    AU --> EX["q-delivery-release<br/>execute release plus UAT<br/>(one explicit approval per environment and operation)"]
    EX --> QA["q-review-release<br/>integral validation"]
    QA -. "optional documentation QA" .-> RD["q-review-docs"]
    QA --> DEC{"Acceptance<br/>(orchestrator plus user)"}
    DEC -->|"ready, or accepted risks"| DEL["q-delivery-release<br/>close delivery"]
    DEC -->|"blocked: findings to owners,<br/>then a new candidate version"| L
    INC["Incident on a released version"] -. "diagnose and fix" .-> L
    INC -. "hotfix candidate" .-> RC
    L -. "optional checkpoint" .-> R["Reporting"]
    DEL -. "optional" .-> R
```

## When to use each skill

| Skill | Use it when |
|---|---|
| [`q-delivery-workflow`](q-delivery-workflow/SKILL.md) | Starting, resuming, routing, recovering, or reporting the current position of a software delivery; running one named planning stage; coordinating the development loop; deciding release acceptance; opening the hotfix route for an incident on a released version. |
| [`q-delivery-release`](q-delivery-release/SKILL.md) | Forming an exact release candidate, verifying local delivery or executing actual approved deployments and migrations, checking applicable recovery, coordinating human acceptance, and closing delivery with the manifest and release notes. It never validates its own release. |

A new run initializes its state and index under the declared root; an existing run resumes. Planning adopts existing evidence and details the first useful increment progressively. Material decisions remain with the user, while routine stage transitions and baselining of already approved meaning add no confirmation turn. Interface consumers preserve a valid design-system non-applicability or accepted omission.

Release requirements follow confirmed usage, criticality, data and actual delivery target. Local package/source delivery and development evaluation need proportional verification and named human acceptance; remote environments and meetings are required only when the release context calls for them.

## What the orchestrator owns

| Concern | How it works |
|---|---|
| Routing | Routes the next planning stage, the user-selected backlog item, loop step, QA, or delivery action; a named `target_stage` runs one stage only. |
| Single writer | Stages return deltas; only the orchestrator writes this run's `00-workflow-state.yaml` and `00-artifact-index.yaml`. The development loop returns deltas too: each grill, plan, ticket set, implementation close, and fix or debug close returns a `stage_result` that is reconciled before the next step. |
| Defect route | A defect item in work that is not yet `Released` skips the grill and goes to `q-code-debug` (cause unknown) or `q-code-fix` (cause confirmed), then rejoins the loop at the durable-record update; a defect against a `Released` version goes to the hotfix route instead. |
| Runtime references | Carries `technical_foundation_ref` and `design_system_ref` so later stages load exact approved versions. |
| Continuity | Workflow-state schema `1.1` gives `ai-coding` an `active_front` (`item_ref` plus current durable `record_ref`), one `next_action`, and its `next_actor`; an open run cannot leave the action or actor empty. |
| Release | Routes candidate formation, execution, UAT, and validation to their owners; every deployment or migration needs its own explicit approval per environment and per operation, and production is never inferred from a lower environment (see the contract's Release engineering section); records the acceptance decision — `ready` or `ready_with_accepted_risks` closes delivery, `blocked` returns findings to the loop and forms a new candidate version; marks lifecycles. The audit alone is not acceptance. |
| Recovery | Reads state first, discovers every sidecar, resolves blockers and pending reconciliation before the authorized front, and loads only the active record and exact dependencies. A malformed or contradictory sidecar remains pending; a status query reports it without writing. |

## Integration with the other groups

Planning stages live in the [plan group](../plan/README.md); the per-item development loop lives in the [code group](../code/README.md); the mini review, the codebase audit, and the integral release validation live in the [review group](../review/README.md). Documentation QA by `q-review-docs` is optional: the orchestrator or `q-review-release` routes to it when the user asks for it or the release risk warrants a documentation pass; its diagnostic stays transient. Delegated reporting returns a composite delta and resumes at the supplied return target (see the [reporting guide](../report/README.md)). Delegated [research](../research/README.md) returns the same way; the root then records `adopt-as-planning-input`, `retain-as-independent`, or `defer-decision`, and only `q-plan-product-core` or `q-plan-tech-foundation` registers an adopted baseline. Structured ideation and standalone database analysis are optional collaborators declared in the manifest.

Invoke a stage directly only when standalone output is intentional: a standalone stage writes its owned artifact, returns `reconciliation_required: true`, and does not claim global workflow completion.
