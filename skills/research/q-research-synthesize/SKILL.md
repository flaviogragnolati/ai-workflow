---
name: q-research-synthesize
description: "Synthesize exact Quasar Research Brief and Findings Register versions into answers, cross-cutting themes, unresolved debates, gaps, and decision implications without duplicating claims or sources. Use after engagement investigation and before an approved Research Baseline. Requires the q-core-contract companion."
---

# Synthesize engagement research

Create a versioned Research Synthesis that interprets the Findings Register by stable reference. Keep claims and source records with the investigation owner.

Read the `q-core-contract` companion for shared governance; if it is missing, stop and install it with `npx skills add flaviogragnolati/ai-workflow --skill q-core-contract`. Validate the output against `references/research-synthesis.schema.yaml`.

## Inputs

Require exact artifact IDs and versions for an authorized Research Brief and its Findings Register. Stop or qualify the result when IDs do not resolve, versions are stale, or the findings do not cover the approved questions.

## Procedure

1. Answer every `question_ref` with confidence, coverage, supporting and contradicting finding refs, and a possible decision implication.
2. Identify two to five cross-cutting themes when the evidence supports them. Give each theme supporting and contradicting finding refs plus a reasoned strength of `strong`, `moderate`, or `emerging`.
3. Preserve material debates as competing positions with finding refs and an explained balance. Do not average a contradiction away.
4. State evidence gaps, limited coverage, and the decision that may be affected.
5. Run a counter-evidence check: select adverse findings, articulate the strongest counterargument, test dependence on the strongest source, inspect circular sourcing, and preserve real limitations.
6. Return the versioned `Working` synthesis and its stage delta.

Base strength on directness, independence, currency, conflicts, contradiction, and coverage. A proposal implication remains supporting advice; it cannot create scope, price, schedule, acceptance, or another commercial commitment.

## Anti-patterns

| # | Anti-pattern | How it shows up | Correct behavior |
|---|---|---|---|
| 1 | Rebuilding the evidence register | The synthesis copies complete claims and source records for convenience. | Point to stable finding IDs and keep only cross-finding interpretation here. |
| 2 | Cherry-picking | The strongest narrative omits contradicting findings or limited coverage. | Preserve adverse refs, debates, gaps, and the counter-evidence result. |
| 3 | Overriding client or commercial truth | External research is presented as a new project commitment. | Mark implications as supporting and return any accepted change to its owner. |

## Completion

Complete when every brief question has an answer or explicit gap, all finding refs resolve, contradictions and circularity remain visible, no source collection is duplicated, and the caller has one next action.
