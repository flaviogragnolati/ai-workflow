## Diagram authority

Classify diagrams explicitly:

| Artifact | Creation mode | Semantic authority |
|---|---|---|
| Package workflow diagram in `README.md` | authored explanatory view | none |
| Domain or architecture Mermaid source | authored | supporting |
| C4 Mermaid or C4-PlantUML source | authored | supporting for `visual-representation` |
| Structurizr `workspace.dsl` | authored | supporting for `visual-model` |
| Structurizr `workspace.json` carrying manual layout | authored | supporting for `visual-layout` |
| Archify typed JSON source (architecture, workflow, sequence, dataflow, lifecycle) | authored | supporting for `interactive-visual-representation` |
| Self-contained HTML or Architecture Delta rendered by Archify | derived | none |
| Domain narrative, dictionary, ADR, or standards text | authored | canonical for its declared scope |
| SVG, PNG, or PDF rendered from Mermaid | derived | none |

An authored diagram source may be the maintained source of its visual representation or visual model, but it is not the canonical source of domain, architecture, feature, or report semantics. A Structurizr model does not replace narrative or ADR authority, and compiled or rendered output cannot silently become semantic truth. No critical rule may exist only as an unlabeled visual edge.

## Diagram delegation

An owning skill may delegate Mermaid encoding, validation, bounded syntactic repair, and rendering to `q-tool-mermaid`. The caller retains semantic ownership, supplies exact source refs and forbidden inferences, reviews the returned source for fidelity, and includes accepted artifacts in its own result. The tool inherits only the caller's authorized write paths and overwrite decision; it does not expand scope, decide domain or architecture meaning, publish, or write global state.

Keep Mermaid source authored and supporting for `visual-representation`. Keep SVG, PNG, and PDF renders derived with `semantic_authority: none` and generation provenance. Syntax or layout defects may return to the tool; cardinality, ownership, trust boundaries, protocols, state meaning, schedule, commercial scope, and every other semantic ambiguity return to the owning skill. Only the root orchestrator reconciles persistent source and renders into the artifact index.

An owning skill may delegate C4 abstraction, cross-view consistency, capability-based backend selection, source validation, and rendering to `q-tool-c4`. The caller still owns the approved people, systems, containers, components, responsibilities, relationships, deployments, feature meaning, and report intent. `q-tool-c4` may delegate exact Mermaid encoding and rendering to `q-tool-mermaid`; neither tool may repair semantic ambiguity or choose architecture. Keep Structurizr DSL authored and supporting for `visual-model`, optional compiled JSON authored and supporting only for `visual-layout`, C4-PlantUML authored and supporting for `visual-representation`, and all renders derived with no semantic authority.

An owning skill may delegate Archify authoring, geometric validation, bounded supported repair, deterministic delivery, and architecture comparison to `q-tool-archify`. The caller supplies exact narrative, ADR, repository, or approved `.mmd` source refs plus forbidden inferences and remains the semantic owner. An Archify source is never the first source of meaning: it re-encodes approved meaning and cites its upstream. Keep the typed JSON authored and supporting for `interactive-visual-representation`; keep delivered HTML and every Architecture Delta derived with no semantic authority. A delta is review evidence, never a decision, and only the root orchestrator reconciles persistent sources and renders.
