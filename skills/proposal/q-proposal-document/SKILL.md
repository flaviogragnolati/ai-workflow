---
name: q-proposal-document
description: "Generate, validate, reconcile, and release branded Quasar proposal DOCX and PDF files from the canonical proposal source. Use for the document channel to author one Markdown mapping with YAML frontmatter, preserve IDs and provenance, run render-based visual QA, and reprocess manually edited documents without silently changing commercial meaning. Requires the q-core-contract and q-proposal-design companions. Do not use a planned document or PDF capability as evidence that a binary runtime exists."
---

# Commercial proposal document

Read the `q-core-contract` companion for shared governance, `q-proposal-design` for the canonical Proposal Source contract, and the references in this directory; if either companion is missing, stop and install both with `npx skills add flaviogragnolati/ai-workflow --skill q-core-contract --skill q-proposal-design`. Use only a document runtime whose generation, rendering, and inspection capabilities are verified in the current environment. `q-tool-document` and `q-tool-pdf` are planned capabilities, not callable dependencies.

## Inputs

Require:

- versioned `02-proposal-source.yaml`;
- proposal release or draft status;
- the `q-proposal-design` source schema;
- `references/04-document-mapping.schema.yaml`;
- brand and style assets;
- applicable general terms;
- any manually edited DOCX being reconciled.

## Outputs and authority

Create:

- `04-document-mapping.md` with YAML frontmatter: authored, supporting channel mapping;
- editable DOCX: derived with no semantic authority;
- matching delivery PDF: derived with no semantic authority;
- validation report and provenance;
- render previews as transient QA evidence.

The canonical proposal source owns scope, price, schedule, and terms.

## Scripts

- Use `scripts/build_document.py` as the public CLI.
- Use `scripts/document_builder.py` as the internal document construction module.
- Use `scripts/validate_document.py` for structural and content validation.
- Use `scripts/simple_yaml.py` only for the supported local YAML subset.

Keep imports aligned with these names. Run each affected CLI with `--help` and execute its tests or representative generation flow after changes.

## Procedure

1. Validate the proposal source and mapping.
2. Build the DOCX from canonical objects and stable IDs.
3. Render and inspect every page.
4. Validate content, tables, totals, pagination, typography, headers, footers, and provenance.
5. Generate the PDF from the verified DOCX.
6. Mark a release only after explicit approval.
7. Register DOCX and PDF as derived artifacts with source references.

If `python-docx`, Pillow, JSON Schema Draft 2020-12 support, YAML parsing, conversion, rendering, or visual inspection is unavailable, identify the missing capability and block only the affected format. A mapping-only result or another supported subset requires explicit partial-release approval and must name every omitted output.

## Manual edit reconciliation

Do not track partial hashes or editable fields in this version. When a user edits a DOCX:

1. accept the edited document as an input;
2. compare it with the canonical source and mapping;
3. classify differences as semantic or channel-only;
4. return semantic differences to `q-proposal-design`;
5. reconcile approved source changes;
6. regenerate affected derivatives.

Return a valid `stage_result` with `artifact_index_delta`, `state_delta`, `traceability_delta`, `decision_delta`, and `risk_delta`. Set `global_state_updated: false` and `reconciliation_required: true`; the root orchestrator alone applies those deltas. Standalone execution never updates global state or the artifact index.
