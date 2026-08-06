---
name: simple-grill
description: "Run a short alignment for a small, well-contained T3 change and create a reduced durable implementation plan. Use for a component, page, function, or simple flow that needs no more than five material questions; escalate when scope spans modules or architecture."
---

# Simple grill

This is the lightest refinement level.

## Procedure

1. Inspect the relevant code and project context.
2. Confirm objective, integration point, must-not-break behavior, scope, and acceptance.
3. Ask at most five questions that cannot be answered from evidence and materially reduce risk.
4. Cover important edge cases, validation, authorization, and testing.
5. Stop and escalate to `feature-grill` or `design-grill` if the work expands.
6. Produce a concise ordered plan.

## Durable output

Create one `Working` reduced implementation plan with objective, alignment, scope and non-goals, integration points, ordered steps, edge cases, tests, assumptions, open questions, and definition of done.

Do not include an execution log. `implement` keeps its internal plan transient and updates the original durable execution record.
