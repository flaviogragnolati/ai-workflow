# Agent instructions

Use this file as the shared source of package guidance for Codex and Claude. `CLAUDE.md` imports it so both harnesses receive the same rules.

## Maintenance trigger

Use `$maintain-ai-workflow` for every package-maintenance change or audit: add, remove, rename, change, or reorganize a workflow or skill; change a contract, schema, manifest entry, route, agent instruction, metadata file, fixture, compatibility rule, or validator; or assess package health and workflow philosophy. Read `maintenance/maintain-ai-workflow/SKILL.md` before making the change.

`maintain-ai-workflow` is administrative housekeeping. Do not invoke it while executing a client or project workflow; route that work through `skill-manifest.yaml`.

## Context and authority

For maintenance, the maintenance skill owns the procedure and philosophy gate. Load only the affected branch of the package. Use `skill-manifest.yaml` for identity and routing, `00-cross-workflow-contract.md` for shared governance, the relevant `SKILL.md` for domain procedure, project state and approved artifacts for a live execution, and `README.md` only as an explanatory view.

Change the authoritative source first, then synchronize connected views. Link to shared rules instead of copying them. Preserve applicable third-party notices when importing or adapting material.

## Maintenance completion

Package maintenance is complete only when `$maintain-ai-workflow` has applied its impact map and philosophy gate, synchronized every affected authoritative source and view, recorded notable changes under `CHANGELOG.md` `Unreleased`, preserved applicable third-party notices, and produced clean package and skill validation or explicitly separated pre-existing blockers. Store temporary acceptance evidence outside skill directories.
