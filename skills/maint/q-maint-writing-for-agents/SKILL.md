---
name: q-maint-writing-for-agents
description: Internal writing discipline for artifacts consumed primarily by AI agents, including skills, AGENTS.md or CLAUDE.md, context pointers, plans, handoffs, intermediate working documents, temporary instructions, and generated references. Repository agents and owning skills must load it when creating, restructuring, or materially editing those artifacts; it is not a user entry point.
metadata:
  internal: true
---

# Write for agents

Act as an internal writing companion. Make an agent-consumed artifact route the right context, preserve authority, produce a predictable execution path, and reveal when its work is complete. Packaging differs across skills, agent instructions, and working artifacts; the writing discipline does not. Optimize for the agent following the same process, not producing identical output.

Inherit authorization and write scope from the owning task; do not create a second source of truth or an independently authoritative output.

When the target is a skill, also read [`SKILL-MECHANICS.md`](SKILL-MECHANICS.md). Otherwise, do not load skill-specific mechanics.

## 1. Establish the artifact contract

Identify before drafting:

- the primary consumer and the action it must take;
- the artifact's one-sentence job and defining constraint;
- the authority it owns, supports, derives, or does not have;
- its authoritative inputs and downstream consumers;
- whether it is durable, intermediate, temporary, or generated;
- the context pointer or owner that makes the consumer reach it;
- the permission boundary inherited from the owning task.

Treat a missing consumer, owner, lifetime, or route as a design gap. Complete this step when the job, constraint, authority, lifecycle, route, and write boundary are explicit.

## 2. Inspect sources and neighbours

Read the authoritative inputs, the instruction that routes to the artifact, and the immediate consumers that depend on its shape. Inspect nearby artifacts only when they clarify naming, IDs, structure, or lifecycle.

Keep each meaning in one authoritative source. Link or derive from that owner instead of restating it. Mark assumptions and unresolved conflicts; never let a summary, render, generated reference, or temporary note silently replace canonical meaning. Treat unsupported specificity as fabrication: turn missing evidence into a targeted lookup, assumption, or blocker instead of a generic procedure.

Complete this step when every material claim is traceable to a source or visibly marked as an assumption, and every affected consumer is known.

## 3. Choose the narrowest useful artifact

Use the artifact profile that matches the consumer:

| Profile | Writing decision |
|---|---|
| Always-loaded instruction | Keep only routing, hard constraints, and broadly applicable rules; every line spends context on every run. |
| Skill | Put the execution path in `SKILL.md`; disclose branch-specific reference only when its pointer has a precise load condition. |
| Durable intermediate | Declare owner, semantic authority, lifecycle, stable identifiers, sources, and the downstream decision it supports. |
| Handoff or working note | Preserve only the state, evidence, decisions, blockers, and next action another agent needs to continue. |
| Temporary instruction or scratch artifact | State its scope, authoritative inputs, non-authority, and discard or expiry condition. Keep it out of durable indexes. |
| Generated or derived reference | Record provenance and regeneration source; assign no semantic authority of its own. |

Every placement trades two budgets:

- **Context load** is the tokens and attention spent whenever material is loaded, whether or not the current branch needs it.
- **Cognitive load** is the human effort of remembering that material exists and when to reach it. Spend it where human judgment must choose; remove it where an agent can route deterministically.

Arrange material on an **information hierarchy** according to when the consumer needs it:

1. Put ordered actions in an in-file step.
2. Keep definitions, rules, and facts needed across the active task as in-file reference.
3. Move branch-specific reference behind a disclosed pointer with an explicit load condition.

Inline what every branch needs and disclose what only some branches use. Disclosing too little creates sprawl and thins attention; disclosing too much hides instructions the agent needs to act.

A **leading word** is a compact concept from the model's prior knowledge that anchors a region of behavior without restating its full definition. Prefer an existing term over an invented label.

A **context pointer** names out-of-context material and encodes the condition for loading it. Its wording, not merely its target, determines retrieval. State what it reaches and one genuine trigger per branch; front-load the leading word, collapse synonymous triggers, and omit identity already clear from the target. Sharpen a weak pointer before moving its body inline.

Prefer editing the existing owner over adding a parallel document. Complete this step when the artifact has one owner, one reachable route, no competing semantic authority, and each piece of content sits at the narrowest tier that every consumer needing it can reliably reach.

## 4. Write the execution path

Lead with the outcome and state the defining constraint as direct prose. Then:

- write ordered actions in imperative form when sequence matters;
- express choices as a table or list so each branch is visible;
- co-locate a concept's definition, rules, exceptions, and failure handling instead of scattering one meaning across the file;
- name exact files, fields, IDs, tools, and commands only when the consumer cannot discover them cheaply;
- use stable vocabulary and repeat the chosen leading word consistently to anchor execution in the body as well as retrieval in its pointer;
- state the positive target behavior, adding prohibitions only for hard guardrails and pairing them with the action to take;
- preserve domain terms, provenance, lifecycle, and authority labels across transformations;
- expose blockers, fallbacks, approvals, and irreversible effects where the decision occurs.

Write for the consumer's task, not as a tour of the source material. Complete this step when a fresh agent can identify what to do next, what not to decide, what evidence to use, and where each branch ends.

## 5. Make completion observable

End every procedural step with a completion criterion that has both **clarity** and **demand**. Clarity makes done distinguishable from not-done; demand sets the required coverage of the evidenced scope, not speculative branches. Make criteria checkable and exhaustive enough to cover every affected item, not merely produce a document-shaped result.

A vague bound invites premature completion as later visible steps pull attention toward finishing. Sharpen the bound first. If the bound is irreducibly fuzzy and real runs still rush it, split the sequence only across a genuine context boundary such as a handoff or isolated delegation; an inline substep does not hide later work or reset attention.

Name signals the consumer can inspect in its own work or trace: a reconciled ID set, an explicit next action, a passing validator, a complete branch table, a declared expiry, or a blocker tied to missing evidence. For intermediate or temporary artifacts, state who consumes the result next and when the artifact stops being useful.

Complete this step when success and failure can be distinguished without inferring the author's intent or reopening this skill.

## 6. Prune and verify

Remove:

- duplicated meaning, while allowing a leading word to repeat as a token without restating its definition;
- cached facts that files, configuration, directory structure, or `--help` expose cheaply; document only the convention, rationale, or gotcha the environment cannot reveal;
- lines that no longer affect routing, execution, judgment, or verification before they accumulate as sediment;
- no-op instructions that do not change behavior relative to the model's default; settle uncertainty with a realistic run and delete the whole sentence when it has no effect;
- stale branches, aliases, placeholders, and temporary material past its lifetime;
- headings or templates retained only for visual symmetry.

Verify links, paths, IDs, terminology, provenance, and affected schemas or validators. Re-read the artifact from the consumer's entry pointer with no hidden context. For a consequential or branching artifact, forward-test a realistic task with only the context the real consumer receives.

Complete this step when every remaining line changes routing, execution, judgment, or verification and the consumer has one truthful next action.

## Done when

- The artifact's job and defining constraint are explicit.
- Authority, lifecycle, provenance, and write scope are honest.
- A strong pointer or owner makes the artifact reachable without user invocation.
- Steps, branches, approvals, fallbacks, and completion criteria are visible where needed.
- Durable, intermediate, temporary, and derived material cannot be confused.
- No duplicate source of truth, stale cache, orphan document, or no-op instruction remains.
- The real consumer can act and verify completion from the context it will actually receive.
