## Structured ideation

Structured ideation is optional and never a mandatory first stage. `q-ideation-session` owns one recorded session: its candidate space, provenance, assessments, dispositions, and the approved snapshot. It generates options and evidence requests; it does not investigate external evidence, edit another owner's artifact, or write workflow state or the artifact index.

The approved Ideation Baseline is canonical only for the frozen register version, each candidate disposition, the criteria and gates applied, retained dissent, and the authorized handoff. It does not make a candidate true, feasible, in scope, or committed. `baseline` names the role of the content — an approved, frozen snapshot — not a lifecycle state: like every other non-orchestrator output, both authored ideation artifacts are created and remain `Working` under the skill's ownership.

The adopting workflow owns the lifecycle transition. After a session returns, its root orchestrator records one disposition:

- `adopt-as-supporting-input`: register the exact snapshot version, mark that version `Baselined` in the index, and name the target skill, intended use, and selected candidate refs;
- `retain-as-independent`: keep the session artifacts without using them in the current work;
- `defer-decision`: leave the disposition open and block only the dependent commitment;
- `reject`: record the reason and adopt nothing.

A consumer may use a snapshot whose exact version is `Baselined` in the adopting workflow's index, or explicitly approved by the named decision owner when the session ran standalone. A snapshot without an approval block is eligible only for `defer-decision` or `reject`. A later round produces a new version; adopting it marks the previously adopted version `Superseded`. When the session ran standalone, the approval record is the snapshot's own `approval` block (`approved_by`, `approval_ref`, `approved_at`); adoption is recorded only by an adopting root orchestrator's index entry, so a standalone snapshot nobody adopted has no adoption record by design, and its persisted `stage_result` sidecar is how a later root run discovers it.

Each consumer adopts only what its own authority allows: problem frames, questions, assumptions, and interpretation risks into discovery; solution, engagement, and workstream options into proposal design; evidence requests and candidate questions into research scope; a selected option, outcome hypothesis, and assumptions into product core; technology or architecture alternatives into their owning stage; diagnostic and causal hypotheses into current-state assessment for validation; intervention, governance, operating-model, and measurement options into intervention design; stakeholder actions into the engagement plan. A candidate never becomes a client fact, an authorized research question, a requirement, an ADR, scope, price, schedule, or a commitment without the owning skill's own procedure. Validate the snapshot against `references/ideation-baseline.schema.yaml`.
