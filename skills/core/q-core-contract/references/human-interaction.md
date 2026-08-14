# Human interaction digest

Derived view of `skill-manifest.yaml` for consumers that need to inspect the
declared conversation cadence without loading the full package registry. It has
no independent authority: the manifest owns the mapping and the cross-workflow
contract defines the values. The package validator rejects any drift.

```yaml
q-core-contract:
  internal: none
q-tool-mermaid:
  orchestrated: on-demand
  standalone: on-demand
q-tool-database-schema:
  orchestrated: on-demand
  standalone: on-demand
q-ideation-session:
  orchestrated: decision-gated
  standalone: dialogue-led
q-ask-project:
  standalone: on-demand
q-ask-analyze:
  standalone: on-demand
q-review-docs:
  orchestrated: review-at-boundaries
  standalone: review-at-boundaries
q-review-skill:
  standalone: review-at-boundaries
q-delivery-workflow:
  orchestrated: decision-gated
q-plan-backlog:
  orchestrated: decision-gated
  standalone: decision-gated
q-plan-domain-model:
  orchestrated: decision-gated
  standalone: decision-gated
q-plan-architecture:
  orchestrated: decision-gated
  standalone: decision-gated
q-plan-features:
  orchestrated: decision-gated
  standalone: decision-gated
q-plan-product-core:
  orchestrated: decision-gated
  standalone: decision-gated
q-plan-tech-foundation:
  orchestrated: decision-gated
  standalone: decision-gated
q-review-codebase:
  orchestrated: review-at-boundaries
  standalone: review-at-boundaries
q-review-code:
  orchestrated: review-at-boundaries
  standalone: review-at-boundaries
q-code-debug:
  orchestrated: on-demand
  standalone: on-demand
q-code-grill-design:
  orchestrated: dialogue-led
  standalone: dialogue-led
q-code-explain:
  standalone: on-demand
q-code-explore:
  orchestrated: on-demand
  standalone: on-demand
q-code-grill-feature:
  orchestrated: dialogue-led
  standalone: dialogue-led
q-code-handoff:
  standalone: on-demand
q-code-implement:
  orchestrated: on-demand
  standalone: on-demand
q-code-implementation-plan:
  orchestrated: decision-gated
  standalone: decision-gated
q-code-prototype:
  standalone: on-demand
q-code-research:
  orchestrated: on-demand
  standalone: on-demand
q-research-workflow:
  orchestrated: decision-gated
q-research-scope:
  orchestrated: decision-gated
  standalone: dialogue-led
q-research-investigate:
  orchestrated: on-demand
  standalone: on-demand
q-research-market-analysis:
  orchestrated: decision-gated
  standalone: decision-gated
q-research-synthesize:
  orchestrated: review-at-boundaries
  standalone: review-at-boundaries
q-code-merge-conflicts:
  standalone: on-demand
q-review-comments:
  orchestrated: review-at-boundaries
  standalone: review-at-boundaries
q-code-fix:
  orchestrated: on-demand
  standalone: on-demand
q-code-grill-simple:
  orchestrated: dialogue-led
  standalone: dialogue-led
q-code-tdd:
  orchestrated: on-demand
  standalone: on-demand
q-code-tickets:
  orchestrated: decision-gated
  standalone: decision-gated
q-maint-writing-for-agents:
  internal: none
q-maint-skill-quality:
  internal: none
q-code-zoom-out:
  standalone: on-demand
q-proposal-design:
  orchestrated: decision-gated
  standalone: decision-gated
q-proposal-document:
  orchestrated: decision-gated
  standalone: decision-gated
q-proposal-workflow:
  orchestrated: decision-gated
q-proposal-web:
  orchestrated: decision-gated
  standalone: decision-gated
q-proposal-discovery:
  orchestrated: decision-gated
  standalone: decision-gated
q-maint-ai-workflow:
  standalone: decision-gated
q-report-workflow:
  orchestrated: decision-gated
q-report-source:
  orchestrated: decision-gated
  standalone: decision-gated
q-report-document:
  orchestrated: decision-gated
  standalone: decision-gated
q-report-deck:
  orchestrated: decision-gated
  standalone: decision-gated
```
