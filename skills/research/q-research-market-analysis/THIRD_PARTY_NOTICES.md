# Third-party notices

## market-research-reports (K-Dense Inc.)

`q-research-market-analysis` adapts selected method design and offline CLI utilities from the `market-research-reports` skill.

- **Source repository:** <https://github.com/K-Dense-AI/scientific-agent-skills>
- **Source skill:** `skills/market-research-reports` (skill metadata version `1.2`)
- **Commit consulted:** `13385c7c4db02fdcc84a020752c07cce91ef780e` (2026-08-13)
- **Copyright:** © 2025 K-Dense Inc.
- **License:** MIT (repository `LICENSE.md`; the skill frontmatter also declares `license: MIT`)

### File-by-file relationship

| File here | Relationship to the source |
|---|---|
| `SKILL.md` | Rewritten for Quasar stage activation, ownership, approvals, lifecycle, and Reporting boundaries; adapts measurement-first sizing, reconciliation, scenario, sensitivity, competitor, and ethics principles. |
| `references/measurement-and-sizing.md` | Adapted from the upstream skill and `references/data_analysis_patterns.md`; preserves disjoint coverage, top-down/bottom-up sizing, TAM/SAM/SOM, and denominator normalization. |
| `references/forecast-and-sensitivity.md` | Adapted from the upstream skill and `references/data_analysis_patterns.md`; preserves conditional scenarios, rate paths, sensitivity, switching values, and non-probabilistic limits. |
| `references/competitor-and-concentration.md` | Adapted from the upstream skill and `references/methods_and_ethics.md`; preserves comparable matrix scope, `unknown`, share coverage, and descriptive concentration limits. |
| `references/methods-and-ethics.md` | Adapted and narrowed from the upstream ethics guidance; all fieldwork operations and raw-response processing are excluded. |
| `scripts/_common.py` | Adapted from upstream `_common.py`; retains bounded regular-file inputs, symlink rejection, atomic JSON output, and deterministic validation errors. |
| `scripts/calculate_market_sizing.py` | Adapted from the upstream script to Quasar finding/assumption IDs and output lineage. |
| `scripts/forecast_sensitivity.py` | Adapted from the upstream script to Quasar scenario and assumption IDs. |
| `scripts/check_unit_consistency.py` | Adapted from the upstream script to Quasar measurement-contract fields and finding refs. |
| `scripts/validate_competitor_matrix.py` | Adapted from the upstream script to cross-check Findings Register IDs instead of an upstream source ledger. |
| `references/market-analysis.schema.yaml`, `references/custom-methods.md`, `scripts/calculate_concentration.py`, `scripts/validate_market_analysis.py`, tests, fixtures, and `assets/market-analysis.example.yaml` | Original Quasar work; no copied source equivalent. |

### Deliberately not incorporated

Quasar does not incorporate the upstream report scaffold, LaTeX template/style, source ledger, claims ledger, evidence-ledger validator, or citation-audit script. Their responsibilities remain with `q-research-investigate`, the shared schemas, `market-analysis.yaml`, and the Reporting workflow. Quasar also removes source acquisition and primary-research operations from this stage.

### Quasar modifications

- Replaced source and claim ledgers with exact Research Brief, Findings Register, calculation, assumption, scenario, and published-result refs.
- Added a single supporting `market-analysis.yaml`, explicit derived-export non-authority, material-change approvals, stale propagation, and standalone single-writer limits.
- Added deterministic HHI/CRn calculation, artifact validation, custom-method lineage, and package fixtures.
- Removed all network behavior, participant operations, raw survey-response processing, report generation, and any implication of legal, investment, or commercial authority.

### MIT License

```text
MIT License

Copyright (c) 2025 K-Dense Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
