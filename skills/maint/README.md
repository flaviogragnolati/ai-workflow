# Maintenance guide

The `maint` group changes this package. All three skills are `distribution: internal`: they are never installed by a consumer and never run inside a client or project workflow. Repository maintainers invoke `$q-maint-ai-workflow`; the other two are its internal companions, reached through the repository instruction pointer in [`AGENTS.md`](../../AGENTS.md) rather than by a user.

This guide is an explanatory view. [`skill-manifest.yaml`](../../skill-manifest.yaml) is the registry; each `SKILL.md` owns its procedure.

## When to use each skill

| Skill | Use it when |
|---|---|
| [`q-maint-ai-workflow`](q-maint-ai-workflow/SKILL.md) | Any package-maintenance change or audit: add, remove, rename, or reorganize a workflow or skill; change a contract, schema, manifest entry, route, agent instruction, metadata file, fixture, compatibility rule, or validator; or assess package health and workflow philosophy. |
| [`q-maint-writing-for-agents`](q-maint-writing-for-agents/SKILL.md) | Creating, restructuring, or materially editing an artifact consumed primarily by agents — a skill, agent instructions, a context pointer, a plan, a handoff, an intermediate working document, a temporary instruction, or a generated reference. Load it inside the owning task's authority and write scope. |
| [`q-maint-skill-quality`](q-maint-skill-quality/SKILL.md) | Maintenance creates, materially changes, or audits a skill, its resources, or its invocation metadata. It requires `q-review-skill` and `q-maint-writing-for-agents`, applies the public review lenses together with package validators and trigger tests, and returns transient acceptance evidence. |

## The maintenance loop

| Step | What it produces |
|---|---|
| 1. Establish the baseline | Current authority, affected surfaces, a pre-change validator run, and the requested outcome — all explicit. Read `AGENTS.md`, the manifest, the contract, `README.md`, `CHANGELOG.md`, then the affected skill and its neighbours. |
| 2. Build the impact map | Every changed contract has an owner and every affected consumer has a planned update or a documented reason to stay unchanged. Trace invocation, routing, upstream and downstream, ownership, side effects, approvals, fallback, persistence, migration, and provenance. |
| 3. Run the philosophy and anti-pattern gate | One of three dispositions: compatible, compatible with named safeguards, or a governance change awaiting or holding explicit user approval. |
| 4. Implement the smallest coherent patch | One cohesive change across the impact map: skill lifecycle and layout, routing, contracts, behavior and migration, a dated `CHANGELOG.md` entry, provenance in the root `LICENSE`, and a transition path for any removal or rename. |
| 5. Validate from structure to behavior | `validate-skills-package.py` clean with no new errors or warnings, `quick_validate.py` for every active skill (changed skills only when a full run is unavailable), affected script tests and fixtures, link and ID checks, a re-read of the diff against the impact map, and a forward test for behavior-changing work. |
| 6. Hand back | Disposition, changed surfaces, compatibility and provenance decisions, exact validation evidence, unresolved risks, and one next recommended action — or `none`. |

## Boundaries

- Maintenance is administrative housekeeping. It never runs while executing a client or project workflow, never returns a project `stage_result`, never updates a project's `00-workflow-state.yaml`, and never registers itself in a project's `00-artifact-index.yaml`.
- Package-write authorization is not Git authorization. Staging, committing, continuing an operation, pushing, opening a pull request, and deleting a ref each need their own approval; stop before any unapproved effect.
- A proposal that breaks one of the eight package invariants is a governance change, not housekeeping: explain the conflict, show a compatible alternative, and obtain an explicit user decision before changing the governing sources.
- Housekeeping artifacts — acceptance evidence, staging copies, working notes — stay outside skill directories unless they are required runtime resources of that skill, and no durable project execution diary is created for maintenance work.
- The root [`LICENSE`](../../LICENSE) is the sole repository-level license and attribution catalog. Skills never carry their own notice file; licenses belonging to bundled third-party dependencies remain with those dependencies.

## Integration with the other groups

Maintenance can touch any group, so it loads only the branch its impact map names. It owns changes to the shared contract (see the [core guide](../core/README.md)) and to `skill-manifest.yaml`, and it synchronizes the derived views — the root `README.md`, every group guide, and the generated routing and human-interaction digests — in the same change. For a diagnostic on a skill *outside* this package, use the public `q-review-skill` in the [review group](../review/README.md); remediation and package acceptance stay here.
