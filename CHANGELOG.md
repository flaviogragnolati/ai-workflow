# Changelog

All notable changes to the Quasar AI delivery skills package are recorded here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
future package releases should use [Semantic Versioning](https://semver.org/).

This changelog was restarted on 2026-08-19 at the prerelease baseline described under
Unreleased; the package has no v0 release yet, and the entries written before that date
were retired — the Git history is their record. Every bullet starts with the ISO date it
landed (the commit date, not a release date), states the change in one sentence, and keeps
details in at most three sub-bullets under Added, Changed, Fixed, or Removed. Add a dated
release heading only when the package version and release boundary are deliberately
established.

## [Unreleased]

### Added

- **2026-09-05** — Added `q-tool-init` for guided project onboarding that agrees the starting evidence, included/excluded workflows, first outcome, usage and criticality, then hands a transient confirmed request to the selected root without creating another project artifact.
  - New and existing runs share an explicit initialization/recovery boundary, and known root workflows remain directly invocable.
  - Breaking prerelease resource move: workflow-state and artifact-index schemas now ship under `q-core-contract/references/`; update direct package-path consumers from `skills/schemas/`, with project state shapes unchanged.

- **2026-09-05** — Added `q-tool-archify`, a shared tool that authors, validates, delivers, and compares Archify typed-JSON diagrams as self-contained interactive HTML through a vendored, commit-pinned runtime (`tt-a1i/archify` 2.17.0-dev.1 at `d8e4daf`).
  - Typed JSON is authored support for `interactive-visual-representation`; HTML and Architecture Delta outputs are derived with no semantic authority, and `q-plan-architecture` remains the first semantic owner.
  - The request contract disables network, update checks, preview, opening, and brand capture; validation allows at most two supported repair rounds and records byte-bound receipts.
  - The package validator pins the runtime and its fixtures, while `sync-archify-runtime.sh` preserves the dependency license and third-party notices; the planned `v2.16.0` pin was rejected because its bundle omitted the brand-mark notice.
- **2026-08-27** — Added `q-tool-docs-compactor`, a standalone, decision-gated shared tool that measures a project docset, retires superseded content whose trace survives elsewhere, merges partial documents into one surviving artifact, replaces copied rules with pointers, and condenses the rest so agents load fewer tokens.
  - It never edits a `Released` version, touches a `Baselined` version only with explicit approval and a recorded decision, and reports absorbed documents through `stale_artifacts` instead of writing the artifact index.
  - Its bundled `compaction_inventory.py` (`measure`, `overlap`, `markers`) returns before/after estimates plus duplicate and legacy signals; a contract `Documentation compaction` section, marker `S-83`, and three behavior cases pin the boundary.
- **2026-08-26** — Added an optional outline working-document branch before an extensive consulting deliverable or when structural approval is requested; it is never the default path and archives when the deliverable version is approved.
- **2026-08-26** — Added `q-consult-session`, an invocable consulting capability for classified kickoff, interview, workshop, training, committee, and acceptance-session records with attributable statements, decisions, actions, attachment extraction, and evidence deltas.
  - It is callable from any engagement point without entering the four-stage sequence and routes diagnostic hypotheses to current state and intervention options to intervention.
  - Its engagement-record frontmatter schema, valid/invalid fixtures, public interface metadata, and positive/negative routing boundary make the new surface executable and reviewable.
- **2026-08-26** — Added six executable consulting schemas with valid/invalid fixtures for commitments, evidence, deliverable and working-document frontmatter, acceptance, and execution release.
  - Semantic checks pin resolvable acceptance criteria, evidence-gated dispositions, releases containing only accepted exact versions, unique run-wide `EVD-nnn` IDs, and compound-component provenance.
  - Behavior cases `consult-criteria-ref-must-resolve`, `consult-disposition-without-evidence-is-deferred`, `consult-release-names-only-accepted-versions`, and `consult-evidence-ids-unique-per-run` exercise the failure direction explicitly.
- **2026-08-26** — Added the public, non-invocable `q-core-identity` companion as the authoritative source for Quasar brand identity, document and deck systems, editorial standards, nine document-kind structures, and shared reusable assets.
  - Proposal and report renderers now declare the companion directly instead of borrowing identity through another renderer.
  - The companion keeps DOCX and Marp source assets editable and regenerable while separating declared typography from locally resolved raster-generation fonts.
  - Validator marker `S-77` and four behavior cases pin public internal-mode registration plus portable cross-group sibling resolution.
- **2026-08-20** — Added `q-review-plan`, a read-only quality skill that audits a multi-slice feature, epic, or milestone against its approved plan hierarchy (architecture → features → plan → tickets), gives every slice a conformance disposition, verifies deviations were documented and reconciled in the owning durable records, and returns a transient diagnostic.
  - The delivery orchestrator routes it as an optional macro checkpoint at a front, milestone, or pre-release-candidate boundary; it may route affected durable artifacts to `q-review-docs`.
  - Three package-validator behavior checks pin its active quality registration, read-only contract, and documentation-QA collaboration edge.
- **2026-08-19** — Added a contract rule for post-release client feedback (record, then route by kind; never edit a `Released` version) with the matching paragraph in the delivery, consulting, and proposal orchestrators, and stated once that no skill estimates effort (audit item 8).
- **2026-08-19** — Wired verified PDF/DOCX/XLSX extraction into `q-research-investigate` and `q-proposal-discovery`, humanizer into the three prose authors (`q-proposal-design`, `q-report-source`, `q-consult-intervention`) and the authored copy of `q-report-deck` and `q-proposal-web`, gave `q-tool-database-schema` a request schema, fixtures, and integration contract, added contract sections for database-schema and prose delegation, and let `ai-coding` delegate research (`adopt-as-planning-input`) (audit G5, G6, C8 residue, G8).

### Changed

- **2026-11-25** — Integrated Google Modern Web Guidance into browser implementation and review, and Fallow into change-scoped and codebase reviews of TypeScript packages, with reproducible CLI commands and explicit coverage gaps.

- **2026-09-05** — Aligned `q-maint-ai-workflow` with progressive onboarding and delivery through selective contract loading, reconciliation of supplied analyses against current sources, and maintenance-only regression scenarios for affected handoffs, approval reuse, design-system applicability, and proportional releases.

- **2026-09-05** — Made idea-to-delivery planning progressive, reused existing material approvals when baselining exact outputs, preserved design-system non-applicability across code and QA, and scaled release evidence to actual use, criticality and delivery target.
  - Shared workflow and format rules now load through conditional contract references; runtime continuity checks reuse the active evidence slice, while package fixtures reject missing fronts, stale or unresolved references, and the wrong delivery profile.
  - Local and development releases retain exact version, proportional verification and named human acceptance without invented production environments; real deployments and migrations retain their separate approvals.
  - `q-review-code` now declares `q-core-contract` so installed consumers receive the same design-system disposition rules; install that companion alongside the reviewer when it is absent.

- **2026-09-04** — Made AI-coding continuation explicit and reduced routine delivery ceremony while preserving reconciliation, review, and approval gates.
  - Breaking prerelease change for `ai-coding`: its workflow-state profile moves to `1.1` with `active_front` and `next_actor`; unchanged workflows retain `1.0`, while the delivery root recovers exact references on resume and asks the user instead of guessing when an older state is ambiguous.
  - Delivery now reads state and pending sidecars before loading the active evidence slice, keeps status queries read-only, resolves blockers and reconciliation before the authorized front, and returns a compact derived continuation view.
  - Tickets use concrete coordination triggers, backlog modes exclude operational status updates, and both mini reviews consume one current transient evidence bundle while retaining separate outcomes and verified empty coverage.
- **2026-09-01** — Extended `q-tool-humanizer` with an optional `ste-informed-technical` profile for high-cost English technical ambiguity while keeping `general` as the default and making no ASD-STE100 compliance or certification claim.
  - Progressive disclosure loads original technical-clarity guidance only for the English technical branch, with the meaning lock taking precedence over mechanical limits and Spanish or creative, commercial, and persuasive prose excluded by default.
  - The root attribution catalog records ASD-STE100 Issue 9 and the MIT-licensed `danyuchn/asd-ste100-skill` reference at revision `d5ce157870cf9c41efd1d6e836706a2be3c7b9da`.
  - Eight deterministic behavior cases cover positive routing, nearby non-triggers, certification refusal, meaning preservation, and simultaneous-action exceptions.
- **2026-08-26** — Split consulting evidence into `01-evidence.yaml` through `04-evidence.yaml`, enforced run-wide unique `EVD-nnn` IDs, added `service` commitments and `service-report` evidence, and required recorded or explicitly absent client validation at the assessment gate.
  - Confidentiality is monotonic: restricted source content is never persisted, confidential content stays within the engagement root, and every report or artifact channel inherits the maximum source classification.
  - Validator marker `S-79`, the engagement-record fixture pair, and `consult-evidence-ids-unique-across-stage-registers` pin the session, confidentiality, and evidence contract.
- **2026-08-26** — Extended `q-report-document` with the maintainer-approved artifact channel for exact canonical `Baselined`/`Released` consulting artifacts, alongside its existing report-source channel.
  - Governance is intentionally limited to document rendering: the channel never creates a report source, changes lifecycle, or acquires semantic authority; edits return to the artifact owner and outputs retain exact provenance.
  - Consulting uses the channel at the design gate for acceptance presentation and may regenerate a status-seal render after release; progress, committee, and completion reports still use `q-report-source`.
  - Contract marker `S-78` and behavior case `consult-workflow-uses-report-document` pin the decision.
- **2026-08-26** — Defined consulting `engagement-record`, `working-document`, and `consulting-deliverable` classes plus simple and compound deliverable forms with one canonical `deliverable.md` and only supporting or derived registered components.
  - Intervention now declares `q-core-identity`, working-document and component outputs, and optional spreadsheet, DOCX, and deck component mechanics.
  - Client-owned documents stay outside the artifact index; evidence records exact locators and classification, while authorized extractions remain derived.
- **2026-08-26** — Centralized Quasar typography on declared Aptos/Arial and Aptos Mono/Consolas chains, with Cambria Math retained only for equations and an explicit Arial raster-generation slot that records its local resolution in `font_profile` provenance.
  - Proposal DOCX generation now resolves Arial → Liberation Sans → DejaVu Sans locally and reports both the declared and resolved faces; the former `font_resolution` result key is replaced by `font_profile`.
  - One-level sibling references now resolve a registered skill ID across repository group directories, while `../../` traversal and missing targets remain invalid.
  - The proposal, report, Marp, humanizer, PPTX, and product-design-system boundaries now point to the owning identity or editorial source without applying Quasar branding to client product UI.
- **2026-08-26** — Made deliverable and acceptance-criterion IDs resolvable on both commercial paths: `q-proposal-design` types acceptance criteria, `q-consult-engagement-plan` authors `01-commitment-register.yaml` by literal copy, the orchestrator registers an external agreement as `engagement-agreement`, marks confirmed design outputs `Baselined`, and documentation QA moves to `q-consult-intervention` (audit H-01, H-02, H-09, H-12–H-14).
  - Contract marker `S-76` and behavior cases `consult-acceptance-does-not-use-review-docs`, `consult-intervention-uses-review-docs`, `consult-current-state-uses-humanizer`, and `consult-workflow-owns-engagement-agreement` pin the routing and lifecycle contract.
  - `q-consult-current-state` may delegate a meaning-locked humanizer pass over client-facing prose.
  - Acceptance returns late documentation-QA findings to intervention before presenting a deliverable.
- **2026-08-26** — Tightened the comment gate against over-commenting: `q-review-comments` now judges necessity and brevity as well as accuracy, calibrates to the repository convention, and returns remove/rewrite/add/keep findings with severity and a pass/fail outcome; `q-code-implement`, `q-code-fix`, and `q-code-debug` state the comment discipline while writing and apply the reviewer's remove and rewrite findings before close.
  - The contract's mini-review rule states that remove and rewrite findings change no behavior and are applied by the implementing skill, never carried as follow-ups.
  - Validator contract-marker case `S-75` pins the rubric markers in the reviewer, the three writers, and the contract.
- **2026-08-19** — Closed the upstream gaps the README audit exposed: `q-code-fix` and `q-code-debug` declare `update-original-execution-record`; the delivery loop states that `q-code-grill-design` hands its next slice back to refinement and lists `q-code-implementation-plan` as a depth; `q-plan-domain-model` and `q-proposal-design` declare their artifact directories; the contract no longer claims skills.sh sections derive from `group`; and `q-plan-tech-foundation` and `q-plan-design-system` declare `q-code-research` as an optional collaborator.
- **2026-08-19** — Made the human documentation teach the package by workflow: the root README now presents the six workflow ids with a start-here table, an approval-gate map, an example artifact tree, a glossary, the language convention, and motivated invariants; added guides for `ask`, `ideation`, `core`, and `maint` (audit § 6, roadmap item 7).
- **2026-08-19** — Defined where each root workflow run keeps its state and index (`docs/<workflow>-workflow/`), named the four release records and the single term "accepted proposal version", listed the artifact roots the standalone-persistence rule discovers, and gave a standalone ideation approval its record (audit G4/D-j, G8).
- **2026-08-19** — Made the mini review enforceable without a hard dependency: `q-code-implement`, `q-code-fix`, and `q-code-debug` now declare `q-review-code` and `q-review-comments` in `uses` with a blocker fallback; fix and debug return a `stage_result` and require `q-core-contract`; the delivery loop routes defect items to fix or debug; the contract states who selects the backlog item, the item → plan → ticket precedence, single authorship of acceptance criteria, and the grill / `targeted-refinement` distinction (audit G1, G3, G7; deferred D-a, D-f).
- **2026-08-19** — Restarted this changelog at the prerelease baseline: commit `b217f92`, 67 skills (64 public), thirteen groups, six workflows, validator `Passed` with 0 errors and 0 warnings. Earlier entries are retired to Git history.

### Fixed

- **2026-09-06** — Fixed misleading JSON errors in Web Markdown tests and Archify subprocess consumers when execution fails or a required receipt is empty or invalid.
  - Transport errors and signals take precedence over exit status, with deterministic regressions for `EPERM` even alongside status `0` or an expected rejection status; failed Archify delivery and comparison preserve existing artifacts and receipts.
  - Archify retains its upstream commit and version with a maintained MIT patch whose input, patch, and output hashes are checked during synchronization and package validation.

- **2026-08-26** — Fixed Proposal Document schema tests so Draft 2020-12 `minLength` diagnostics accept the installed validator wording, acceptance criteria require `satisfies`, and the reported pass count is calculated.
- **2026-08-19** — Made the root README and the thirteen group guides accurate against the manifest, contract, and skill procedures after the 2026-08-19 README audit (7 high, 23 medium, 44 low findings): corrected tool-source authority, PPTX backend ownership, ideation's `participation_mode`, proposal ideation adoption, research delegation from Delivery planning, and eleven flow diagrams covering proposal release, defect and refinement routing, reporting gates, consulting change control, delivery acceptance and documentation QA, direct analysis, planning returns, and release ordering.

### Removed

- **2026-08-27** — Removed prerelease compatibility branches for project-root workflow state and the retired `t3-core` / `t3-only` package profile values.
  - Root orchestrators now resume only from their declared artifact roots; state or index files elsewhere are not recognized as workflow state.
  - Workflow and manifest schemas accept only `any` or `project-defined`, while T3 Core remains an advisory technology recommendation rather than a compatibility profile.
  - Maintenance now removes superseded prerelease forms by default, and the package validator rejects their reintroduction.
- **2026-08-26** — Removed duplicated renderer-owned Quasar logos, templates, and identity prose after moving their authoritative copies to `q-core-identity`.
  - Removed the implicit `q-report-document` → `q-report-deck` identity dependency and the proposal renderer's duplicate logo files.
  - Removed the `FREE_FONT_CANDIDATES` abstraction and its ambiguous `font_resolution` output in favor of an explicit declared-family and generation-slot contract.
