---
name: q-maint-skill-quality
description: Internal acceptance companion for Quasar package maintenance that creates, materially changes, or audits Agent Skills and their invocation metadata. It combines the public q-review-skill diagnostic with package contracts, deterministic validators, trigger tests, context-budget review, and provenance checks before q-maint-ai-workflow can accept skill work. Repository agents must load it for those maintenance branches; it is not a user entry point.
metadata:
  internal: true
---

# Accept skill quality

Act as the skill-quality acceptance companion inside `q-maint-ai-workflow`. Inherit the maintenance task's authority and write scope. Produce transient acceptance evidence; do not become a second package maintainer, registry, or durable audit owner.

Read `q-review-skill` for the public evidence lenses and `q-maint-writing-for-agents` for agent-consumed editing discipline before assessing or changing a skill. If either registered dependency is missing, stop and report the package inconsistency instead of reconstructing its rules.

## 1. Fix the acceptance scope

1. Identify every added or materially changed skill, resource, invocation surface, manifest entry, derived catalog view, package instruction, validator, fixture, and downstream consumer in the maintenance impact map.
2. Preserve the pre-change validator result and changed-file inventory so regressions remain distinct from baseline failures.
3. Record the skill's consumer, one-sentence job, defining constraint, authority, execution mode, distribution, side effects, output lifecycle, provenance obligations, and positive and negative trigger examples.
4. For a package-wide audit, enumerate the full set or define an explicit risk-ranked sample. Never promote sample evidence to complete-package acceptance.

Complete this step when every in-scope contract surface has an owner and acceptance evidence can be tied to a before/after baseline.

## 2. Confirm mechanical evidence

Use the structural validation sequence owned by `q-maint-ai-workflow`; do not create a parallel command policy. Confirm that its evidence covers the package validator, the official `quick_validate.py` for every added or changed active skill, affected tests and smoke checks, and link, ID, dependency, distribution, invocation, and agent-metadata reconciliation. Require full active-skill `quick_validate.py` coverage when package-wide execution is practical.

Return any missing check to the maintenance owner. Keep deterministic failures separate from semantic findings. Do not weaken a validator to make the change pass, and do not present a passing parser as evidence that the skill routes or behaves correctly.

Complete this step when the package has no new structural failure or warning and every unavailable check has an explicit coverage limitation.

## 3. Apply semantic and behavioral acceptance

Apply the complete `q-review-skill` procedure to each in-scope skill using this package's authority order and philosophy gate. Add these package-specific checks:

- `skill-manifest.yaml`, folder, frontmatter, `agents/openai.yaml`, `skills.sh.json`, generated digests, and README routing tell the same truth;
- internal companions have a strong conditional pointer and no user invocation surface;
- public skills remain installable with declared public dependencies and one-level portable resources;
- no skill duplicates shared governance, another skill's procedure, or a derived view;
- outputs, side effects, approvals, fallbacks, stack coverage, and semantic authority match observable behavior;
- every branch has a demanded completion criterion and one truthful next action.

Forward-test at least one realistic positive trigger and one nearby non-trigger for a new or materially changed invocable skill. Exercise the riskiest branch or fallback when consequences justify it. Use an isolated agent with minimal leaked context when permitted; otherwise run a minimal-context dry run and record that limitation.

Complete this step when all applicable quality lenses and trigger paths have evidence or a named gap, and every blocker or high-severity finding has a planned owner-routed correction.

## 4. Reconcile and accept

Apply approved corrections through the authoritative owner first, using `q-maint-writing-for-agents` for agent-consumed artifacts, then synchronize connected views. Preserve third-party notices for copied or substantially adapted material and retain a concise provenance pointer when external concepts materially shape the result.

Use findings rather than a numeric grade as the gate:

- resolve every `blocker` and `high` finding;
- resolve each `medium` finding or record why it is consciously accepted within the requested scope;
- treat `low` findings as optional unless they reveal drift across contract surfaces;
- block acceptance when a missing authority, dependency, behavior test, or compatibility proof makes approval unsafe.

Re-run mechanical and semantic checks after correction. Return the exact commands and results, behavior-test coverage, finding dispositions, provenance decision, remaining limitations, and one next maintenance action to `q-maint-ai-workflow`. Do not create a durable scorecard inside a skill directory.

Complete acceptance when changed skills are structurally valid, behaviorally reachable, authority-safe, context-efficient, provenance-complete, and free of unresolved blocker or high findings.

## Anti-patterns

| # | Anti-pattern | How it shows up | Correct behavior |
|---|---|---|---|
| 1 | Parallel quality authority | The internal companion invents a second rubric or registry. | Reuse `q-review-skill` lenses and the package's canonical manifest and contracts. |
| 2 | Structural pass as acceptance | Package validation passes, so trigger behavior and authority are left untested. | Require semantic findings and proportional positive, negative, and fallback tests. |
| 3 | Sample promoted to package proof | One or two representative skills stand in for the whole catalog. | Enumerate full coverage or label the risk-ranked sample and its limits. |
| 4 | Audit-owned scorecard | A durable grade becomes a competing source of package truth. | Keep acceptance evidence transient and record notable implemented change only in `CHANGELOG.md`. |
