## Design system reference

The design-system stage is conditional. It applies only to a product with a durable visual interface whose reusable design decisions outlive one feature; `q-plan-design-system` owns the applicability criteria and confirms the disposition. Keep three runtime states distinguishable: `not_applicable` for a product the criteria exclude, an accepted omission recorded as a decision and, when warranted, a risk, and an executed stage.

Every interface consumer resolves that existing disposition before requiring a reference. Load the exact specification and token version only for an executed stage. For `not_applicable`, apply the product's application standards, feature behavior and accessibility requirements; a null reference is expected and creates no design-system gap. For an accepted omission, retain its exact decision and warranted risks without repeatedly reopening it. An unexplained missing reference or a changed interface that invalidates the disposition returns to the owner for assessment. Carry the disposition or its decision reference into tickets so a cold executor can make the same distinction.

When the stage applies and completes, it authors exactly two related persistent artifacts with separated authority:

| Artifact | Owns |
|---|---|
| Design system specification | Principles, art direction, token taxonomy, component and pattern contracts, accessibility contracts, coverage, and governance. |
| Design token set | Machine-readable token values, aliases, groups, themes, and modes. |

The specification names the exact token-set ID and version and never copies its values; the token set never restates narrative decisions, inventories, or accessibility requirements. Workflow state carries one `design_system_ref` as an artifact ID and version, and that specification version resolves the compatible token set. Do not add a second global reference field.

Design-system conformance is a criterion inside the standards axis of change review and codebase audit, never a third authority axis and never a reason to widen a reviewed diff. Downstream consumers load the exact referenced version; a material change makes them stale and returns reconciliation to the owner. Planning never claims accessibility conformance: it authors reusable requirements, and implementation and QA gather the evidence.
