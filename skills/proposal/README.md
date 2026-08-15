# Discovery and proposal guide

The `proposal` group turns raw client evidence into a traceable discovery brief, a canonical commercial proposal, and optional web and document channels. Commercial meaning lives in one source owned by Proposal Design; every channel regenerates from it and never rewrites it.

This guide is an explanatory view. [`skill-manifest.yaml`](../../skill-manifest.yaml) is the registry; each `SKILL.md` owns its procedure.

## How a proposal flows

```mermaid
flowchart TB
    E["Client evidence"] --> W["q-proposal-workflow"]
    W --> D1["q-proposal-discovery<br/>Discovery Brief and readiness"]
    D1 --> D2["q-proposal-design<br/>canonical proposal source"]
    D2 -->|"optional channel"| WCH["q-proposal-web<br/>interactive proposal"]
    D2 -->|"optional channel"| DCH["q-proposal-document<br/>DOCX / PDF"]
    W --> G{"Client disposition"}
    G -->|"accepted software or mixed"| DEL["Delivery workflow"]
    G -->|"consulting or other service"| MAN["Commercial close or<br/>future/manual execution"]
    G -->|"review or negotiation"| D2
    G -->|"rejected or expired"| CLO["Commercial close"]
    D1 -. "authorized external uncertainty" .-> RES["Research delegation"]
    RES -. "explicit adoption disposition" .-> D1
```

## When to use each skill

| Skill | Use it when |
|---|---|
| [`q-proposal-workflow`](q-proposal-workflow/SKILL.md) | Starting, resuming, or reconciling the commercial flow; name a target stage when only one stage is needed. It owns workflow state, the artifact index, and the commercial release. |
| [`q-proposal-discovery`](q-proposal-discovery/SKILL.md) | Turning client evidence into a traceable brief, open questions, risks, and a proposal-readiness assessment. |
| [`q-proposal-design`](q-proposal-design/SKILL.md) | Defining canonical scope, solution, deliverables, schedule, investment, terms, and commitments. |
| [`q-proposal-web`](q-proposal-web/SKILL.md) | Rendering an interactive proposal from approved commercial meaning; publication remains a separate approval. |
| [`q-proposal-document`](q-proposal-document/SKILL.md) | Generating, visually validating, reconciling, and releasing proposal DOCX/PDF files without changing commercial meaning. |

## Boundaries

- No fabrication: Discovery records what the client evidence supports and routes blocking assumptions to the user.
- A channel renderer never rewrites accepted commercial scope; semantic errors return to Proposal Design.
- Release approval and publication are separate approvals.
- An adopted research baseline enters as `external-research` through an explicit disposition; Research never edits the Discovery Brief.
- An ideation snapshot becomes a client fact, requirement, scope, price, or commitment only through this workflow's explicit adoption.

## Integration with the other groups

An accepted software engagement continues to the [delivery workflow](../delivery/README.md). A material external uncertainty may be delegated to [research](../research/README.md). Discovery may call `q-review-evidence` (see the [review guide](../review/README.md)) for a claim that could mislead a commitment. `q-proposal-document` requires `q-proposal-design` and may delegate PDF mechanics to `q-tool-pdf` (see the [shared tools guide](../tool/README.md)). A commercial checkpoint may optionally produce a [report](../report/README.md).
