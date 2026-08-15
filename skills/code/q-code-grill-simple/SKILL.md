---
name: q-code-grill-simple
description: "Run a short alignment for a small, well-contained change and create a reduced durable implementation plan. Use for a component, page, function, or simple flow that needs no more than five material questions; escalate when scope spans modules or architecture. Do not use for a defect report, even one that names the file: route a confirmed cause to q-code-fix and an unconfirmed one to q-code-debug. Part of the Quasar AI delivery skills."
---

# Simple grill

This is the lightest refinement level.

## Procedure

1. Inspect the relevant code, project context, and applicable technical foundation or repository standards. When the change touches a user interface and `design_system_ref` exists, load that exact version and reuse its contracts instead of inventing local styling.
2. Confirm objective, integration point, must-not-break behavior, scope, and acceptance.
3. Ask at most five questions that cannot be answered from evidence and materially reduce risk.
4. Cover important edge cases, validation, authorization, and testing.
5. Stop and escalate to `q-code-grill-feature` or `q-code-grill-design` if the work expands, or hand off to `q-code-fix` or `q-code-debug` if the change turns out to be a defect.
6. Produce a concise ordered plan.

## Durable output

Create one `Working` reduced implementation plan with objective, alignment, scope and non-goals, integration points, ordered steps, edge cases, tests, assumptions, open questions, and definition of done.

Do not include an execution log. `q-code-implement` keeps its internal plan transient and updates the original durable execution record.
