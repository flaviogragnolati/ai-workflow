---
name: codebase-review
description: "Audit a T3 web codebase, module, feature, or release candidate against repository standards and applicable quality criteria. Use for evidence-based integral quality assessment with ranked findings, exact locations, impact, remediation, and references; not for a single diff or for applying fixes."
---

# Codebase review

Use this skill for a broad T3 quality audit. Use `code-review` for one diff and `review-code-comments` for comment quality alone. Do not modify code unless the user separately asks for fixes.

## Coverage

Read repository instructions, architecture, standards, product requirements, and the applicable references:

- `references/t3-stack.md`;
- `references/generic-standards.md`;
- `references/libraries.md`;
- `assets/report-template.md`.

Confirm the project is compatible with `t3-core`. Stop or declare missing coverage for another stack.

Review:

- architecture and module boundaries;
- security, authorization, privacy, and data integrity;
- errors, resilience, observability, and operations;
- performance and scalability risks;
- maintainability, module depth, and testability;
- testing quality and critical-flow coverage;
- accessibility where applicable;
- migrations, deployment, and delivery documentation;
- requirement and acceptance coverage for a release candidate.

## Evidence standard

Every finding must cite an exact location or reproducible artifact, describe the concrete failure mode, name the applicable standard, explain impact, propose a fitting remediation, and state confidence. Separate confirmed defects from risks and optional improvements.

Rank findings by severity and likelihood. Do not bury blockers under style observations.

## Procedure

1. Lock scope, baseline, and review criteria.
2. Map relevant architecture, flows, data, and standards.
3. Inspect evidence across the coverage axes.
4. Cross-check findings to remove duplicates and unsupported claims.
5. Produce the Markdown audit using the template.
6. Summarize release blockers, high-priority findings, accepted risks, and coverage gaps.

This report is supporting quality evidence. Integral acceptance remains an orchestrator decision reconciled with tests, UAT, security, deployment, and other evidence.
