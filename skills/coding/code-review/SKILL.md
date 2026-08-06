---
name: code-review
description: "Review a branch, pull request, working tree, or change since a fixed baseline along two separate axes: repository standards and originating specification. Use as the change-scoped technical mini review after implementation. Report findings without applying fixes."
---

# Code review

Review one change, not the whole codebase. Do not modify code.

## Inputs

Require:

- a fixed comparison baseline;
- the changed files or diff;
- repository instructions and standards;
- the originating backlog item, issue, ticket, plan, specification, or acceptance criteria.

If the baseline or specification is missing, state the limitation instead of inventing it.

## Two-axis review

Keep results separate:

1. **Standards axis:** correctness, security, data integrity, failure handling, maintainability, tests, architecture, and repository conventions.
2. **Specification axis:** requested behavior, scope, acceptance criteria, non-goals, migration, and unintended changes.

Use independent reviewers or parallel passes when that capability is available. Otherwise run two sequential passes with separate notes and context. Do not require a particular tool or agent name.

## Finding format

For each finding include priority, axis, exact location, evidence, impact, and recommended correction. Merge only true duplicates while preserving both axes.

Distinguish blockers from suggestions. Do not report pre-existing issues outside the changed surface unless the change makes them newly relevant.

## Close

Return:

- baseline and scope;
- standards findings;
- specification findings;
- verification gaps;
- outcome: pass, pass with findings, or fail;
- recommended next action.

The implementer records the result in the original durable ticket or execution record.
