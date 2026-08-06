---
name: technical-foundation-definition
description: "Define and validate the T3 technical foundation from an approved product core, including concrete framework and library versions, data access, deployment, security, operations, testing, and architecture-driving NFRs. Use for stage 2 before domain modeling or architecture."
---

# Technical foundation definition

Read `../../00-cross-workflow-contract.md`. This package supports `t3-core`; do not claim generic coverage for another stack.

## Required inputs

- baselined or sufficiently mature product core;
- applicable proposal constraints and technical commitments;
- repository evidence when a codebase exists;
- confirmed hosting, security, compliance, and operational constraints.

## Canonical output

Create `docs/development-workflow/technical/02-technical-foundation.md` as an authored, canonical `Working` artifact covering:

- `stack_profile: t3-core`;
- concrete versions and selections for TypeScript, Next.js, tRPC, testing, ORM/data layer, database, auth, and deployment;
- NFRs and architecture drivers;
- security and privacy baseline;
- observability, operations, recovery, and environments;
- testing strategy and required quality signals;
- constraints, decisions, risks, assumptions, and unresolved items;
- source and requirement traceability.

Resolve the ORM and library choices from project evidence; do not hard-code a product that the repository does not use.

## Procedure

1. Verify product readiness.
2. Inspect the real repository when available.
3. Separate mandated choices from recommendations.
4. Record every architecture-driving choice with rationale and consequences.
5. Identify unsupported or conflicting commitments.
6. Validate that the selected T3 profile can satisfy the required NFRs.
7. Mark downstream readiness.

## Compatibility gate

If the project is not T3-compatible, return `blocked` with the detected stack and missing adapter. Do not continue to T3 QA or issue a false approval.

Return a valid `stage_result`; the orchestrator alone updates global state and artifact index.
