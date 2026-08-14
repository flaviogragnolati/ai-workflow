---
name: q-maint-ai-workflow
description: Maintain and evolve the Quasar AI delivery workflow and its related skills. Use whenever adding, removing, renaming, reorganizing, reviewing, or changing a workflow, orchestrator, stage, skill, contract, schema, manifest entry, agent instruction, routing rule, compatibility rule, metadata file, fixture, or package validator. This is an administrative maintenance tool; do not invoke it while executing the delivery workflow for a project.
metadata:
  internal: true
---

# Maintain AI workflow

Act as the package housekeeper. Preserve a small, composable, evidence-driven workflow while making the requested change coherent across every affected contract surface. Operate on the `SKILLS` package, never on a project's runtime workflow state or artifact index.

Read the `q-core-contract` companion before any Git inspection or separately requested Git mutation. Package-write authorization does not authorize staging, committing, continuing an operation, pushing, opening a pull request, or deleting a ref; apply its operation-scoped Git policy and stop before any unapproved effect.

## Philosophy

Use these invariants as the design filter for every change:

- Keep human judgment in charge of scope, commitments, irreversible actions, and genuine governance changes.
- Compose narrow skills behind explicit ownership boundaries. Keep orchestrators focused on routing, reconciliation, and global state rather than copying domain procedure.
- Load only the route and references needed for the current task. Treat context and attention as shared budgets.
- Keep each meaning in one authoritative source. Use pointers and derived views instead of duplicating rules.
- Prefer small deliberate changes with fast, credible feedback loops. Require verification proportional to risk; keep tickets and TDD optional.
- Preserve artifact authority, lifecycle, stable IDs, provenance, and traceability. Never let a derived presentation silently become semantic truth.
- State compatibility honestly. Stop or add an adapter when coverage is missing instead of issuing a false approval.
- Make external or irreversible side effects explicit and approval-gated.

Treat a proposal that changes one of these invariants as a governance change, not ordinary housekeeping. Explain the conflict, show a compatible alternative, and obtain an explicit user decision before changing the governing sources.

## 1. Establish the baseline

Resolve these paths from the repository root and read, in this order:

1. `AGENTS.md` and `CLAUDE.md` when present;
2. `skill-manifest.yaml`;
3. `skills/core/q-core-contract/SKILL.md`, the `q-core-contract` companion;
4. `README.md` and `CHANGELOG.md`;
5. the affected `SKILL.md`, `agents/openai.yaml`, schemas, fixtures, scripts, and neighboring owners;
6. `skills/scripts/validate-skills-package.py` and any affected executable tests or help output.

Inspect repository status or create an explicit changed-file inventory when version control is unavailable. Preserve unrelated user work. Run the package validator before editing when possible so pre-existing failures remain distinguishable from regressions.

Complete this step only when the current authority, affected surfaces, validation baseline, and requested outcome are explicit.

## 2. Build the impact map

Trace the change through:

- invocation and routing into the changed capability;
- upstream inputs and downstream consumers;
- ownership, execution mode, side effects, approvals, fallback, and stack compatibility;
- persistent versus transient outputs and their semantic authority;
- manifest, contracts, orchestrators, routers, schemas, fixtures, scripts, agent metadata, and explanatory docs;
- migration needs for renamed IDs, paths, outputs, or behavior;
- provenance and license obligations for incorporated third-party material.

Read only the connected skills and references. Do not load the entire package without an impact reason.

Complete this step when every changed contract has an owner and every affected consumer has a planned update or a documented reason to remain unchanged.

## 3. Run the philosophy and anti-pattern gate

Challenge the proposal before implementation. Flag any change that creates:

- a monolithic orchestrator that duplicates stage procedure;
- multiple writers for workflow state or the artifact index;
- mandatory ceremony unrelated to risk or coordination needs;
- duplicated or contradictory sources of truth;
- an invocable capability that is unregistered, planned, empty, or unreachable;
- a derived artifact with semantic authority;
- silent mutation of accepted, released, or baselined meaning;
- T3 approval for an unsupported stack or another compatibility pretense;
- unapproved commit, publication, messaging, or remote-state changes;
- agent instructions without a strong context pointer or completion criterion;
- an invocation mismatch between `SKILL.md`, `agents/openai.yaml`, routing, and actual intent;
- a maintenance capability embedded in project runtime execution;
- placeholders, stale aliases, dead links, or empty capability folders.

If the requested implementation is an anti-pattern, pause that implementation, provide concrete evidence, and recommend the smallest philosophy-compatible alternative. Proceed with a philosophy-breaking version only after the user explicitly chooses the governance change and its consequences are updated in the canonical contract, documentation, validations, and changelog.

Complete this step with one of three dispositions: compatible, compatible with named safeguards, or governance change awaiting or holding explicit approval.

## 4. Implement the smallest coherent patch

Make one cohesive change across the impact map. Apply these maintenance chores when relevant:

- **Skill lifecycle:** align folder name, frontmatter `name` and trigger-rich `description`, imperative body, `agents/openai.yaml`, invocation mode, and manifest entry.
- **Routing:** update the owning workflow, orchestrator, router, README entry, and any agent context pointer that would otherwise lie.
- **Contracts:** update schemas, fixtures, acceptance evidence, stable IDs, artifact ownership, authority, lifecycle, side effects, approvals, fallback, and stack profile together.
- **Behavior:** add migration or compatibility guidance and re-sync affected consumers without copying the same rule into multiple files.
- **History:** add a user-visible `CHANGELOG.md` entry under `Unreleased`; identify breaking changes and migrations explicitly.
- **Provenance:** treat the root `LICENSE` as the sole repository-level license and attribution catalog. List every externally referenced repository there with a link, affected Quasar scope, source revision, modifications, and applicable terms. Do not create skill-root copies or per-skill notice catalogs. Preserve license files owned by bundled third-party dependencies, and require the package validator to distinguish those dependency files from forbidden skill-root duplicates before removing a superseded notice.
- **Removal or rename:** remove stale references, provide a transition path when consumers may still use the old ID, and avoid silent aliases.

Load [`q-maint-writing-for-agents`](../q-maint-writing-for-agents/SKILL.md) before creating, restructuring, or materially editing an agent-consumed artifact. Apply its internal writing discipline inside this maintenance task's authority and write scope.

Keep housekeeping artifacts outside skill directories unless they are required runtime resources for that skill. Never create a durable project execution diary for maintenance work.

## 5. Validate from structure to behavior

Run the strongest available checks in this order:

1. Run `python3 skills/scripts/validate-skills-package.py` from the repository root and require no new errors or warnings.
2. Run the official `quick_validate.py` for every active skill; at minimum run it for every added or changed skill when full-package execution is unavailable.
3. Run affected script tests, schema fixtures, and `--help` smoke checks.
4. Verify local links, renamed paths, IDs, metadata, routing, and references to planned or removed capabilities.
5. Re-read the diff against the impact map and philosophy gate. Confirm documentation describes behavior the package actually enforces.
6. Forward-test a complex or behavior-changing skill on a realistic request with minimal leaked context when safe and useful.

For skill additions, material skill changes, or skill audits, load `q-maint-skill-quality` through the repository instruction pointer and satisfy its semantic, trigger, provenance, and package-acceptance checks in addition to the structural sequence above.

Treat a failing new check as a blocker. Record unrelated baseline failures separately; do not hide them by weakening the validator or deleting evidence.

Complete this step only when every affected surface has evidence, remaining limitations are explicit, and the package retains one truthful next action.

## 6. Hand back the maintenance result

Report:

- the requested outcome and philosophy-gate disposition;
- changed files and contract surfaces;
- compatibility, migration, and provenance decisions;
- exact validation evidence and any baseline-only failures;
- unresolved risks or approvals;
- one next recommended maintenance action, or `none` when complete.

Do not return a project `stage_result`, update project `00-workflow-state.yaml`, or register package maintenance in a project's `00-artifact-index.yaml`.
