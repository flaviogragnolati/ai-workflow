---
name: module-feature-decomposition
description: "Decompose validated T3 architecture into modules, features, vertical slices, behaviors, dependencies, and a supporting technical implementation sequence. Use for stage 5 before backlog planning; do not create delivery milestones, canonical epics, capacity plans, or product priorities."
---

# Module and feature decomposition

Read `../../00-cross-workflow-contract.md`.

## Ownership boundary

Own:

- module map and authoritative responsibility;
- feature index and feature specifications;
- use cases, commands, queries, events, validation, authorization, and failure behavior;
- vertical slices and technical dependencies;
- approximate technical order.

Do not own milestones, delivery epics, product priority, capacity, dates, or delivery roadmap. Those belong to `backlog-and-delivery-planning`.

## Outputs

Create under `docs/development-workflow/implementation/`:

- `05-module-map.md`;
- `05-feature-index.yaml`;
- feature or module specifications as needed;
- `05-technical-implementation-sequence.md`.

The technical sequence is supporting guidance for slicing and dependency order. Never name it or treat it as a delivery roadmap.

## Procedure

1. Load baselined architecture, application standards, domain model, and product requirements.
2. Identify cohesive modules with one authoritative owner per responsibility.
3. Map requirements and domain behaviors to bounded features.
4. Specify happy paths, alternate paths, authorization, validation, persistence, events, failures, and test scope.
5. Prefer vertical slices over horizontal technical task lists.
6. Define dependencies and approximate technical order without assigning delivery priority.
7. Verify every in-scope requirement is assigned or has an explicit exception.
8. Return unresolved scope or boundary decisions to their owning stage.

## Gate

Complete when modules and features are sufficiently defined for Stage 6 to create milestones and epics. No delivery milestone or canonical epic may be introduced here.

Return a valid `stage_result`; standalone execution does not update global state.
