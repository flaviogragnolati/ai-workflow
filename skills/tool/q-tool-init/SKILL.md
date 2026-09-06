---
name: q-tool-init
description: "Guide Quasar workflow onboarding when the user wants to initialize a project or choose its starting point: existing work or a new idea, commercial proposal or direct delivery, included and excluded workflows, first outcome, users, and operating constraints. Agree a small start request and hand it to the selected root orchestrator. Do not use for routine resume, status, a bounded project question, or a named stage whose route is already settled."
---

# Initialize the workflow journey

Agree where the project starts and what the user wants to do next. Keep onboarding conversational and bounded to decisions needed to choose the first workflow; detailed discovery belongs to that workflow's stages.

Read the `q-core-contract` companion for shared governance and its Workflow initialization section; if it is missing, stop and install it with `npx skills add flaviogragnolati/ai-workflow --skill q-core-contract`. Read the relevant manifest routes when available, otherwise the companion's `references/routing.md`. Load only the chosen root after selection.

## Establish the starting point

1. Use the supplied idea, documents, project destination, and decisions first. Inspect only the named workspace, existing run state, and source locators needed to distinguish new work from an existing run. Do not inventory the whole repository or read every workflow's artifacts.
2. Establish the desired first outcome and the engagement: internal or external users, whether a commercial agreement is needed or already exists, existing code or evidence, included work, exclusions, and deliberately deferred work. Ask only unresolved questions that change the route or its immediate scope; propose concrete alternatives instead of presenting a catalog questionnaire.
3. For software, establish the intended initial use (local, development or evaluation, shared internal, or external), decision owner, and known data or operational criticality. Unknown implementation details remain deferred to their owner. An internal customer does not imply low risk, and an external customer does not automatically require a new proposal.
4. Recommend one first workflow. Show other included workflows as conditional later destinations and keep excluded ones out of the route. Confirm the starting point, boundary, and first action together when they are ready; reuse explicit choices already made by the user.

Complete alignment when one next workflow and its authorized first action are clear, or one material unresolved decision has a named owner. Do not ask the user to create a workflow-state file.

## Route the confirmed start

| Starting need | Destination |
|---|---|
| Discover an engagement and agree a commercial proposal | `q-proposal-workflow` |
| Plan or build software from an idea, an internal brief, existing code, or accepted software scope | `q-delivery-workflow` |
| Execute consulting or other non-software services against an accepted proposal or supplied agreement | `q-consult-workflow` |
| Investigate an external uncertainty before the next commitment | `q-research-workflow` |
| Communicate available versioned project evidence | `q-report-workflow` |

The destination owns its prerequisites. An onboarding choice is not an accepted proposal, product baseline, authorized research brief, release approval, or reporting snapshot. If required evidence is absent, preserve the gap and let the selected owner resolve it; do not invent predecessor artifacts or silently substitute another workflow.

Use the optional collaboration matching the confirmed choice:

- When `confirmed-start-selects-discovery-proposal`, hand off to `q-proposal-workflow`; if absent, `return-the-confirmed-start-and-install-command-for-q-proposal-workflow`.
- When `confirmed-start-selects-ai-coding`, hand off to `q-delivery-workflow`; if absent, `return-the-confirmed-start-and-install-command-for-q-delivery-workflow`.
- When `confirmed-start-selects-consulting-execution`, hand off to `q-consult-workflow`; if absent, `return-the-confirmed-start-and-install-command-for-q-consult-workflow`.
- When `confirmed-start-selects-research`, hand off to `q-research-workflow`; if absent, `return-the-confirmed-start-and-install-command-for-q-research-workflow`.
- When `confirmed-start-selects-reporting`, hand off to `q-report-workflow`; if absent, `return-the-confirmed-start-and-install-command-for-q-report-workflow`.

Each install command is `npx skills add flaviogragnolati/ai-workflow --skill <selected-root-id>`. Return a gap instead of initializing its state yourself. An existing run resumes through its owning root; initialization never resets it.

## Handoff and completion

Return one transient `workflow-start-request`: project destination and identity when known, starting evidence locators and exact versions when available, included/excluded/deferred work, first outcome, operating context and decision owner, selected workflow/root, authorized next action, unresolved questions, and the user's confirmation reference. Omit unavailable or irrelevant fields instead of generating empty registers.

Pass that request directly to the chosen root when the first action is authorized. The root owns initialization and records the confirmed start in its existing decisions; the first domain stage adopts only the context it owns. Keep future workflows as intent until their prerequisites and execution are authorized. Do not remain a parent orchestrator, write project state or an artifact index, create an onboarding document or sidecar, select backlog fronts, install tools, or perform Git or external operations.

Finish when the chosen root has received the request, or return the exact remaining user decision or missing capability plus one next action. Summarize the agreed boundary and destination in the user's language; no full workflow inventory is required.
