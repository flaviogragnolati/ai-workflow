---
name: q-code-implementation-plan
description: "Produce a concrete, repository-grounded execution plan for settled work without writing code. Use to plan a feature, refactor, migration, integration, or fix after direction is known, with ordered file-level steps, acceptance criteria, testing, rollout, and rollback. Part of the Quasar AI delivery skills."
---

# Implementation plan

Use this skill when architecture and product direction are settled. Return to `q-code-grill-design` or `q-code-grill-feature` when material design decisions remain.

## Inputs

Accept a backlog item, issue, ticket, architecture document, specification, or explicit request. Preserve source IDs and constraints.

## Procedure

1. Inspect repository instructions, the applicable technical foundation and adopted guidance, the exact `design_system_ref` version for interface work, relevant code, tests, schemas, migrations, and docs.
2. Lock objective, scope, non-goals, deferred work, and must-not-break behavior.
3. Choose the implementation approach and strict sequence.
4. Break work into phases and tasks grounded in exact files, functions, data, and dependencies.
5. Identify pitfalls, compatibility concerns, migrations, observability, security, and rollback.
6. Define acceptance criteria and proportional verification using commands discovered from the project rather than assumed tooling.
7. Mark assumptions and blockers honestly.
8. Write one durable `Working` plan.

When `settled-work-needs-engine-specific-schema-or-migration-sequencing` and `q-tool-database-schema` is installed, use `schema-review` to ground the current relational state, `document-model-review` for a document model, or `migration-design` for the proposed transition. Supply exact repository evidence and the confirmed profile. Incorporate accepted sequencing, validation, recovery, and execution ownership into this plan; keep the specialist analysis transient. If the tool is absent, `continue-with-observed-repository-evidence-and-mark-the-specialist-database-gap`.

## Required content

Include objective, target outcome, source references, scope, non-goals, deferred work, current system context, approach, assumptions, ordered phases, detailed tasks, cross-cutting concerns, pitfalls, testing, rollout and rollback, documentation, risks, open questions, definition of done, and executor instructions.

This plan is not an implementation diary. It may be baselined, archived, or superseded. If tickets later absorb execution, `q-code-implement` updates the tickets rather than appending a parallel execution log here.
