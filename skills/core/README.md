# Core guide

The `core` group holds one skill: the shared governance companion every coordinated Quasar skill loads before acting. It is a companion, not an entry point — you never invoke it directly. A skill that declares it in `requires` reads it and, when it is absent, stops and prints the exact install command instead of proceeding on assumed rules.

This guide is an explanatory view. [`skill-manifest.yaml`](../../skill-manifest.yaml) is the registry; each `SKILL.md` owns its procedure.

## When to use each skill

| Skill | Use it when |
|---|---|
| [`q-core-contract`](q-core-contract/SKILL.md) | Never directly. A workflow, orchestrator, stage, renderer, tool, or quality skill reads it for routing, human-interaction cadence, dependencies and optional collaboration, single-writer rules, stage results, artifact authority and lifecycle, change control, stack compatibility, delegation contracts, and the bundled shared schemas. |

## Reading map

The contract is long because it is shared. Load the section your task needs, not the file as a tour.

| If you are … | Load … |
|---|---|
| deciding which source wins a conflict | Purpose and authority |
| choosing how much conversation a mode implies | Human interaction |
| routing an orchestrator, a `target_stage`, or a delegated subworkflow | Invocation and routing |
| deciding whether a skill ships to consumers | External distribution |
| adding a `requires`, a `uses`, or a bundled reference | Skill identity and dependencies |
| writing workflow state, the artifact index, or starting a second root run | Single-writer rule |
| staging, committing, pushing, or touching a ref | Git operations |
| returning a stage delta, or persisting one standalone | Stage result (including Standalone persistence) |
| assigning authority, lifecycle, stable IDs, provenance, an artifact root, or naming a release | Artifact ownership and authority (including Release records and Artifact roots) |
| deciding whether a diagram is canonical, and who renders it | Diagram authority · Diagram delegation |
| recording a decision, a risk, a change request, or a date or effort figure | Decisions, risks, and changes |
| running the development loop: durable records, precedence, the mini review, grill vs `targeted-refinement` | Durable and transient development records |
| forming, executing, or validating a release | Release engineering |
| executing an accepted non-software engagement | Consulting execution |
| working against a project stack, or with none | Stack compatibility · Design system reference |
| delegating or adopting a research baseline | Engagement research |
| adopting an ideation snapshot | Structured ideation |
| building or delegating a report | Reporting |
| handling what a client said after a release or acceptance | Client feedback |
| delegating format mechanics | PDF · Document · Spreadsheet · PPTX · Marp · Database-schema · Prose delegation |
| finishing package work | Validation |

## Bundled resources

Four schemas travel with the contract because several skills validate against the same shape: [`stage-result.schema.yaml`](q-core-contract/references/stage-result.schema.yaml), [`cited-findings.schema.yaml`](q-core-contract/references/cited-findings.schema.yaml), [`ideation-baseline.schema.yaml`](q-core-contract/references/ideation-baseline.schema.yaml), and [`report-source.schema.yaml`](q-core-contract/references/report-source.schema.yaml). [`git-worktrees.md`](q-core-contract/references/git-worktrees.md) covers isolated-worktree execution.

Two references are **generated** views of `skill-manifest.yaml`, regenerated whenever the manifest changes and carrying no authority of their own: [`routing.md`](q-core-contract/references/routing.md) (workflow entry skills, stages, delegates, optional next) and [`human-interaction.md`](q-core-contract/references/human-interaction.md) (the cadence mapping). They exist so an agent can answer a routing or cadence question without loading the whole manifest — the manifest remains the source of truth, and package validation fails on drift.

## Boundaries

- The contract is never copied into an individual skill. Skills link to it and add only their own rules.
- It governs shared lifecycle, ownership, authority, and change control. It does not own domain procedure — the skill does — and it does not override the manifest on identity, paths, status, side effects, or routing.
- It is `invocable: false`. Reaching it means a skill declared it in `requires`, not that a user asked for it.

## Integration with the other groups

Every group depends on it. Orchestrators load it for routing and the single-writer rule ([delivery](../delivery/README.md), [proposal](../proposal/README.md), [consult](../consult/README.md), [research](../research/README.md), [report](../report/README.md)); stages load it for stage results and artifact authority ([plan](../plan/README.md), [code](../code/README.md)); reviewers load it for evidence and lifecycle rules ([review](../review/README.md)); tools load their own delegation section ([tool](../tool/README.md)). The maintenance group owns changes to it (see the [maint guide](../maint/README.md)).
