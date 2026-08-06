---
name: high-level-architecture-standards
description: "Define canonical T3 architecture, ADRs, and project application standards plus supporting diagrams from validated product, technical, and domain inputs. Use for stage 4 before module and feature decomposition."
---

# High-level architecture and standards

Read `../../00-cross-workflow-contract.md`. Use the confirmed `t3-core` foundation; stop if compatibility is unresolved.

## Outputs and authority

Create under `docs/development-workflow/architecture/`:

- `04-architecture.md`: canonical architecture narrative;
- `04-application-standards.md`: canonical project-specific engineering rules;
- ADRs for durable decisions;
- context, container, deployment, or sequence `.mmd` sources: authored and supporting;
- visual renders: derived with no semantic authority.

ADRs and narrative text own decisions. Mermaid owns only the visual representation.

## Procedure

1. Load product, foundation, domain model, decisions, risks, and existing repository constraints.
2. Define boundaries, components, responsibilities, interactions, and data ownership.
3. Cover security, failure behavior, observability, deployment, migration, and operational constraints.
4. Turn architecture-driving choices into ADRs.
5. Define standards that are specific enough for downstream implementation and review.
6. Generate diagrams that reflect, but do not replace, the narrative.
7. Validate every requirement and domain boundary has a responsible architectural element.
8. Record alternatives, trade-offs, pending decisions, and downstream constraints.

## Gate

Complete when the architecture can guide module ownership and implementation without hidden critical decisions. Return to product, technical, or domain stages when an upstream contradiction is found.

Return a valid `stage_result`; only the orchestrator reconciles state and index.
