---
name: feature-grill
description: "Align a bounded but non-trivial T3 feature and produce a durable execution-ready implementation plan. Use when work has meaningful behavior or dependencies but does not require system-wide architecture; escalate to design-grill or de-escalate to simple-grill as scope changes."
---

# Feature grill

This is the middle refinement level. Inspect the real repository and existing domain language before asking questions.

## Procedure

1. Confirm the objective, user-visible outcome, source backlog or requirement IDs, and must-not-break behavior.
2. Map current modules, flows, data, contracts, tests, and applicable decisions.
3. Resolve only material questions about behavior, scope, integration, edge cases, authorization, failure, migration, rollout, and acceptance.
4. Challenge fuzzy terminology and update project context only when a durable term changes.
5. Offer an ADR only for a durable architectural decision.
6. Produce an ordered implementation plan grounded in exact files, functions, data, dependencies, and tests.
7. Validate the plan with the user.

## Durable output

Create one `Working` feature implementation plan. Include objective, alignment, scope and non-goals, current context, approach, assumptions, ordered phases and tasks, cross-cutting concerns, pitfalls, testing, rollout and rollback, documentation, risks, open questions, definition of done, and instructions for execution.

Do not add an execution log. When execution begins, `implement` updates the original ticket or execution record, not this plan as a work diary.
