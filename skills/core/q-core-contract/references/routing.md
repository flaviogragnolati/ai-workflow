# Routing digest

Derived view of `skill-manifest.yaml` for orchestrators that run from an
installed catalog and cannot read the manifest. It carries no authority: in this
repository the manifest decides, and the package validator regenerates this block
on every run, so a mismatch is drift rather than a second opinion.

```yaml
discovery-proposal:
  entry_skill: q-proposal-workflow
  stages: [q-proposal-discovery, q-proposal-design, q-proposal-web, q-proposal-document]
  delegates: [research, reporting]
  optional_next: [ai-coding, reporting, close]
ai-coding:
  entry_skill: q-delivery-workflow
  planning_stages: [q-plan-product-core, q-plan-tech-foundation, q-plan-domain-model, q-plan-architecture, q-plan-features, q-plan-design-system, q-plan-backlog]
  delegates: [reporting]
  optional_next: [reporting, close]
research:
  entry_skill: q-research-workflow
  profiles: [general, market]
  stages: [q-research-scope, q-research-investigate, q-research-market-analysis, q-research-synthesize]
  stage_conditions:
    q-research-market-analysis: market-profile-with-analysis-modules-or-explicit-target
  optional_next: [discovery-proposal, reporting, close]
reporting:
  entry_skill: q-report-workflow
  content_profiles: [general, market-research]
  stages: [q-report-source]
  renderers: [q-report-document, q-report-deck]
  optional_next: [return-to-caller, close]
maintenance:
  entry_skill: q-maint-ai-workflow
  scope: package-administration
```

Route by skill name. Each stage, renderer, and orchestrator declares its own
side effects, approvals, and fallback in its `SKILL.md`; this digest declares
only which capabilities exist and in what order they run.
