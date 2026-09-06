# Workflow initialization

Load this reference only when a root run does not yet have state, onboarding hands off a start request, or initialization is explicitly requested. The existing root remains the sole writer; `q-tool-init` only aligns a transient request.

## Select or resume the run

Use the requested workspace and the selected workflow's declared artifact root. Reuse the user's starting-point, boundary, and route decisions; ask only for a missing choice that affects the next action. Direct invocation of a known root does not require onboarding first.

- A status or project question is read-only, including when no run exists. Report that state instead of creating files.
- If state and index already exist, validate the referenced active slice and follow the root's recovery procedure. Never reset the run because the user said "init".
- If only one exists, or existing artifacts or pending sidecars precede state, recover from that evidence through the root; preserve files and uncertainty instead of overwriting or assuming every artifact is approved.
- If neither exists and the authorized action starts a new run, create both under that root after establishing the selected workflow and its immediate input boundary. Do not pre-create files for future workflows.

Complete selection with one existing run to resume, one authorized new run, or one localized recovery decision. Existing files outside the declared root are evidence only, not another runtime authority.

## Initialize under the selected root

Use the bundled `workflow-state.schema.yaml` and `artifact-index.schema.yaml` in this companion's `references/` as the authoritative shapes. Validate new state and index before handing work to the first stage. Schemas are loaded on creation or structural change, not on every status turn.

Create the run's `project_id`, workflow identity, and an index with no invented domain artifacts. Set `status: not_started`, the first applicable stage as `current_stage`, empty stage status and blockers, and only decisions or risks actually established. Record the confirmed start compactly in the root's existing decision mechanism: evidence locators, included/excluded/deferred work, first outcome, operating context, and confirmation reference. This is an attributable starting decision, not a competing product specification or commercial commitment; route semantic adoption to the first domain owner.

If the run has no decision register yet, store one compact, attributable string in state `decisions` with the start decision ID, confirmation reference and agreed boundary; do not create a dangling decision ID or a separate onboarding file. Once the domain owner adopts that meaning, replace copied domain detail with its exact artifact or decision reference, retaining the start ID and workflow boundary.

For `ai-coding`, use schema `1.1`, `stack_profile: project-defined`, `active_front: null`, and null technical/design references until those artifacts exist. Set one executable `next_action` and its `next_actor`. Other workflows retain schema `1.0` and their declared profile and stage prerequisites. The absence of a proposal never blocks an idea-to-delivery route; Product Core records its commercial applicability.

Existing source artifacts retain their IDs, versions, authority and lifecycle. Reconcile standalone sidecars before continuing, and reference a predecessor's released inputs without importing its state or marking successor stages complete.

Complete initialization when state and index agree on project identity, contain no fabricated completion or reference, preserve supplied evidence, and name the authorized next action. Pass only the selected stage's evidence and already established decisions; do not ask for the same intake again.
