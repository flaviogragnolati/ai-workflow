# Author Archify typed JSON

Read this reference for `create`, `revise`, `deliver` when candidate authoring or revision is needed, or when validation requires a supported source repair.

## Start from approved meaning

Create the typed JSON from the exact source refs in `archify_request`. Preserve stable element and relationship IDs, names, direction, boundaries, protocols, and evidence classification. Do not add a component, dependency, trust boundary, responsibility, state, or claim because it would improve the picture.

For an approved `.mmd`, re-encode topology and explicit labels only. Do not copy Mermaid styling as system meaning. Include the `.mmd` path and version in `sources[].derived_from`; if the Mermaid source is absent, author only from the owner's narrative and record the missing upstream reference.

## Use runtime contracts without copying them

- Read [the Archify authoring contract](../runtime/references/authoring-contract.md) for schema choice, geometry, language, repair order, and type-specific placement.
- Read [the delivery contract](../runtime/references/delivery-contract.md) before final validation, atomic delivery, comparison, or browser evidence.
- Read [the schema guide](../runtime/schemas/README.md) and the matching JSON schema before authoring a diagram type.
- Use the matching file under [`runtime/examples/`](../runtime/examples/) for field shape and layout patterns, never for facts.

The upstream authoring contract's hand-placed fallback is not available in the Quasar wrapper. If the vendored renderer or `doctor` is unavailable, stop with a blocked result; do not hand-author HTML from the template or bypass deterministic delivery.

Set `meta.quality_profile` to `showcase` unless a standalone request explicitly accepts `standard`. Omit presentation extras by default. Prefer a short main path, explicit typed relationships, and the smallest view that satisfies the declared audience and purpose.

Complete authoring when the candidate is schema-valid, every visible fact resolves to an upstream source, Spanish or other unsupported locale limitations are disclosed, and no inferred meaning was introduced.
