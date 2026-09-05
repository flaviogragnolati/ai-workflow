# Archify integration contract

Read this reference for orchestrated work, persistent output, architecture comparison, or a repository-evidence handoff.

## Ownership flow

The semantic owner supplies approved meaning and exact source versions in one `archify_request`. `q-tool-archify` re-encodes that meaning as typed JSON, validates geometry, performs bounded supported repairs, and invokes the vendored runtime. The tool never becomes the owner of architecture, workflow, sequence, dataflow, lifecycle, or report meaning.

```text
semantic owner -> archify_request -> q-tool-archify -> pinned local runtime
```

| Caller | Allowed use | Semantic owner |
|---|---|---|
| `q-plan-architecture` | Interactive architecture presentation or Architecture Delta after narrative and ADR meaning is approved | `q-plan-architecture` |
| Standalone user | Explicit supplied narrative, typed JSON, or approved `.mmd` source | The named owner in the request |
| Consulting, reporting, proposal, and review skills | Not routed in this iteration | No call is made |

## Artifact authority

| Artifact | Creation mode | Semantic authority |
|---|---|---|
| Archify typed JSON | authored | supporting for `interactive-visual-representation` |
| Self-contained HTML | derived | none |
| Architecture Delta HTML | derived | none |
| Validation, delivery, comparison, or browser receipt | transient by default; derived if explicitly persisted | none |

Every typed source cites the exact upstream narrative, ADR, repository revision, approved `.mmd`, or earlier Archify source. It is never the first source of meaning. Only the root orchestrator reconciles persistent outputs into the artifact index.

## Outcome contract

- Return `completed` only when the requested source validates, `showcase` reports 9/9 checks with zero errors and warnings, delivery or comparison succeeds when requested, and every required receipt is bound to the returned bytes.
- Return `completed_with_warnings` only when optional browser evidence is unavailable or a standalone user explicitly selected `standard` and accepted its warnings.
- Return `blocked` for contract failure, semantic ambiguity, unsupported inference, missing required runtime capability, exhausted repair rounds, validation failure, or failed delivery or comparison.

Do not inspect a previous output after a failed delivery. Preserve the previous trusted HTML, report the failed candidate, and return the next owner action.

## Delegation boundaries

When repository evidence is required, `q-code-explore` returns only a bounded evidence map; this tool still owns encoding and validation. When an approved Mermaid file is supplied, use it only as a topology source and preserve its exact path and version. `q-tool-mermaid` remains the owner of editable Mermaid syntax and rendering; Archify does not render or repair Mermaid.

Complete the handoff when request and result validate, every output has honest authority and provenance, and the caller has one explicit reconciliation or correction action.
