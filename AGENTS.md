# Agent instructions

Use this file as the shared source of package guidance for Codex and Claude. `CLAUDE.md` imports it so both harnesses receive the same rules.

## Maintenance trigger

Use `$q-maint-ai-workflow` for every package-maintenance change or audit: add, remove, rename, change, or reorganize a workflow or skill; change a contract, schema, manifest entry, route, agent instruction, metadata file, fixture, compatibility rule, or validator; or assess package health and workflow philosophy. Read `skills/maint/q-maint-ai-workflow/SKILL.md` before making the change.

`q-maint-ai-workflow` is administrative housekeeping. Do not invoke it while executing a client or project workflow; route that work through `skill-manifest.yaml`.

## Context and authority

For maintenance, the maintenance skill owns the procedure and philosophy gate. Load only the affected branch of the package. Use `skill-manifest.yaml` for identity and routing, `skills/core/q-core-contract/SKILL.md` for shared governance, the relevant `SKILL.md` for domain procedure, project state and approved artifacts for a live execution, and `README.md` only as an explanatory view.

Change the authoritative source first, then synchronize connected views. Link to shared rules instead of copying them. Preserve applicable third-party notices when importing or adapting material.

## Agent-consumed writing

Load `skills/maint/q-maint-writing-for-agents/SKILL.md` whenever creating, restructuring, or materially editing an artifact consumed primarily by agents, including skills, agent instructions, context pointers, plans, handoffs, intermediate working documents, temporary instructions, and generated references. It is an internal companion, not a user entry point; apply it inside the authority and write scope of the owning task.

## Maintenance completion

Package maintenance is complete only when `$q-maint-ai-workflow` has applied its impact map and philosophy gate, synchronized every affected authoritative source and view, recorded notable changes under `CHANGELOG.md` `Unreleased`, preserved applicable third-party notices, and produced clean package and skill validation or explicitly separated pre-existing blockers. Store temporary acceptance evidence outside skill directories.
