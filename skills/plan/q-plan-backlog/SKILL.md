---
name: q-plan-backlog
description: "Create and maintain the canonical rolling-wave delivery backlog from product, technical, domain, architecture, and feature inputs. Use for initial high-level backlog generation at stage 6, targeted refinement of near-term work, or approved structural replanning during development. Requires the q-core-contract companion. Part of the Quasar AI delivery skills."
---

# Backlog and delivery planning

Read the `q-core-contract` companion for shared governance; if it is missing, stop and install it with `npx skills add flaviogragnolati/ai-workflow --skill q-core-contract`. Own delivery structure; do not require tickets or exhaustive task detail to close initial app-flow.

## Canonical outputs

Create under `docs/development-workflow/backlog/`:

- `06-backlog.yaml`: canonical structured backlog;
- `06-backlog-changelog.md`: structural change history;
- `06-backlog.md` and `06-milestones.md`: derived views with no semantic authority.

The backlog owns milestones, epics, feature assignment, delivery dependencies, checkpoints, proposed priority, readiness, related risks and decisions, and the next recommended front. It also owns capacity assumptions, target dates, and the delivery roadmap only when the user supplies or approves them; it never estimates effort or invents dates, and without approved dates the derived Gantt view is simply unavailable.

## Modes

An operational execution update is not a backlog-planning mode. An authorized implementer or the root may record progress, verification evidence, mini-review outcomes, and completion on the current execution record without opening this skill. If that record is the backlog item, change only its operational fields; a scope, acceptance-criterion, priority, dependency, or structural change returns here in one of the modes below.

### initial-generation

Run at the end of app-flow. Produce the first complete high-level backlog with:

- main outcome-oriented milestones;
- principal epics;
- known features or workstreams;
- checkpoints and validation points;
- important dependencies and blockers;
- proposed priority and readiness;
- one next front the user can select for a grill, validation, or implementation.

Do not require all stories, tasks, subtasks, tickets, or future work to be `Ready`. State that the backlog is rolling-wave and not exhaustive.

### targeted-refinement

Refine one milestone, epic, feature, or next iteration. Add only useful stories, tasks, subtasks, acceptance criteria, fine dependencies, enabling work, and readiness evidence. Preserve traceability to upstream IDs.

### replan-and-synchronize

Incorporate new information by adding, splitting, combining, reordering, deferring, superseding, or retiring milestones and epics. Update dependencies, views, and changelog. Do not change confirmed priority or commercial commitments without the required approval and change control.

## Procedure

1. Load the current increment's upstream baselines and relevant slices of the existing backlog, changelog, state, decisions, risks, and delivery constraints. When `design_system_ref` exists, load that exact version and treat its downstream needs — build, adoption, and migration work — as candidate backlog input alongside features.
2. Choose exactly one mode.
3. Reconcile every known feature with a backlog assignment or explicit exception.
4. Preserve stable IDs when meaning is unchanged.
5. Record structural changes, rationale, affected IDs, approvals, and stale downstream artifacts.
6. Validate dependency direction, readiness, checkpoints, and next action.
7. Regenerate only the derived views whose source meaning changed. Do not add a structural changelog entry for an operational execution update; when a derived view displays the changed operational status, refresh that view so it does not publish stale information.

When `approved-backlog-visual-intent-requires-a-derived-gantt-view` and `q-tool-mermaid` is installed, delegate only approved backlog dates, dependencies, and milestones and register the result as a derived view with no semantic authority. If the tool is absent, `continue-with-canonical-backlog-and-textual-derived-views`.

## Initial exit criteria

Close app-flow when:

1. outcomes map to milestones;
2. central capabilities map to epics;
3. known features are assigned or justified;
4. primary dependencies and blockers are visible;
5. at least one next front can begin a grill, validation, or implementation;
6. uncertainty and non-exhaustiveness are explicit;
7. tickets are not required;
8. next actions are clear.

## Ticket boundary

`q-code-tickets` is optional and downstream. Use it only when distribution, tracker needs, multiple executors, or multiple sessions justify durable tickets.

Confirm initial priority and structural replanning when required, reusing unchanged approved decisions. Present the concrete next-front selection with its priority decision when both are ready; reconciliation alone does not add another approval turn.

Return a valid `stage_result` whose `next_recommended_action` names the exact backlog item or version and destination skill. The root converts that recommendation into workflow-state `next_action` and `next_actor`; this skill never selects a front for the user. In standalone mode set `global_state_updated: false` and `reconciliation_required: true`.
