## Reporting

Reporting is optional and does not change upstream completion criteria. `q-report-workflow` accepts explicit, versioned artifact references from discovery, proposal, planning, implementation, validation, delivery, consulting, or another registered workflow. Resolve them through the artifact index and load only the approved reporting scope.

`q-report-source` owns the single semantic source for a reporting run. It is canonical only for report selection, narrative, and approved interpretation; upstream artifacts retain authority over their facts, commitments, decisions, risks, and delivery status. A `Working` artifact may support planning, but its exact version must be baselined, released, or explicitly approved as a reporting snapshot before the report source is baselined.

`report_type` states the communication purpose; `content_profile` states the semantic source pattern. `market-research` blocks that state facts, metrics, estimates, interpretations, recommendations, or projections require typed `evidence_refs` resolving to an exact artifact ID and version in `source_snapshot`. Reporting may communicate only Market Analysis `published_results` and their qualifiers; it does not search, recalculate, or use a derived/none export as the sole semantic support.

`q-report-document` and `q-report-deck` consume the same baselined report source when they run as reporting channels. Their Markdown, DOCX, Marp source bundle, HTML, PDF, PPTX, and image outputs are derived with no semantic authority. The Marp bundle remains technically editable and regenerable, but that editability does not give it report authority. A manual semantic edit returns to `q-report-source`, creates a new approved source version, and makes affected channels stale. Generation or release approval never authorizes publication or external sending.

`q-report-document` also accepts an exact canonical artifact in `Baselined` or `Released` lifecycle plus its `deliverable_kind` as an artifact channel. This channel never produces a report source, never changes the source lifecycle, and never acquires authority: every DOCX or PDF is derived with `semantic_authority: none` and provenance to the exact artifact ID and version. Semantic edits return to the artifact owner named in provenance, never to `q-report-source`. Progress, committee, close, and other consulting reports still use a baselined report source through the reporting workflow.

Reporting and artifact channels inherit the maximum classification of all sources. They exclude `confidential` or `restricted` material from an output whose approved classification is lower, and they never persist restricted source content merely to render it.

When another workflow delegates progress, feature, milestone, release, completion, consulting, or other reporting, that workflow remains root orchestrator and reconciles the composite reporting delta. Direct standalone renderers never write workflow state or the artifact index.
