---
name: q-plan-product-core
description: "Define the canonical product core from a product idea or the accepted proposal version. Use for stage 1 of the AI coding workflow when product intent, actors, journeys, requirements, business rules, scope, exclusions, assumptions, or pending decisions need a validated baseline. Requires the q-core-contract companion. Part of the Quasar AI delivery skills."
---

# Product core definition

Read the `q-core-contract` companion for shared governance; if it is missing, stop and install it with `npx skills add flaviogragnolati/ai-workflow --skill q-core-contract`. In orchestrated mode, write only owned domain artifacts and return a delta; do not write global state or artifact index.

## Inputs

Accept either:

- a product idea plus available research and project context; or
- the accepted proposal version (its commercial release) and its referenced discovery evidence.

Preserve source IDs and versions. Separate confirmed facts, supported inferences, assumptions, and unresolved questions. Never turn a proposal assumption into a product confirmation.

An adopted ideation snapshot may contribute one selected option, an outcome hypothesis, and its unresolved assumptions as supporting input. Revalidate problem, outcome, actors, journeys, scope, and business rules here; never copy a candidate into a requirement, and keep an unevidenced opportunity an assumption.

## Canonical output

Create `docs/development-workflow/product/01-product-core.md` as an authored, canonical `Working` artifact for product intent and scope. Include:

- problem and desired outcome;
- first useful increment, its acceptance signal, and later outcomes deliberately deferred;
- intended use (local, development or evaluation, shared internal, or external), decision owner, and known data or operational criticality;
- actors and responsibilities;
- critical journeys and scenarios;
- essential functional requirements and business rules;
- scope, exclusions, constraints, and non-goals;
- acceptance signals;
- assumptions, pending decisions, risks, and source references;
- proposal traceability when applicable.

Use stable IDs for requirements, rules, decisions, risks, and assumptions.

## Procedure

1. Load the smallest authoritative source slice and current relevant decisions. Reuse a confirmed onboarding request or existing brief without repeating its questions; revalidate only unsupported or contradictory meaning.
2. Resolve contradictions by source authority and version; do not silently merge incompatible claims.
3. Draft the smallest product core sufficient for technical work on the first useful increment. Separate current scope from future opportunity; expand discovery only when an unresolved question could change this increment or a cross-cutting constraint.
4. Ask only blocking questions that sources cannot answer.
5. Validate coverage, internal consistency, source traceability, and explicit uncertainty.
6. Mark readiness for `q-plan-tech-foundation`.

A product started without a proposal is valid. Record `commercial_contract: not_applicable` rather than inventing one.

## Gate

Complete when product intent, primary actors, core journeys, in/out scope, business rules, and blocking uncertainty are explicit. Return `blocked` when a missing decision would make technical planning speculative.

Obtain user confirmation of product scope and unresolved material assumptions before declaring that meaning approved. Reuse an explicit confirmation already supplied with the same scope; present only the remaining decisions together. The root records the exact approved version as `Baselined`; this skill authors `Working` artifacts and never treats onboarding or a completed draft alone as a product approval.

Return a valid `stage_result`. In standalone mode include `global_state_updated: false` and `reconciliation_required: true`.
