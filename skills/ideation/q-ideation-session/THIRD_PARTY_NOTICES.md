# Third-party notices

## scientific-brainstorming (K-Dense Inc.)

`q-ideation-session` adapts the method design and the offline CLI utilities of the
`scientific-brainstorming` skill.

- **Source repository:** <https://github.com/K-Dense-AI/scientific-agent-skills>
- **Source skill:** `skills/scientific-brainstorming` (skill metadata version `1.1`)
- **Commit consulted:** `13385c7c4db02fdcc84a020752c07cce91ef780e` (2026-08-13)
- **Copyright:** © 2025 K-Dense Inc.
- **License:** MIT (repository `LICENSE.md`; the skill's own frontmatter also declares `license: MIT`)

### Files derived from that source

| File here | Relationship to the source |
|---|---|
| `scripts/_common.py` | Copied with minor edits; shared bounded-input, safe-output, and JSON helpers. |
| `scripts/session_scaffold.py` | Adapted; generalized to profiles, intents, participation modes, decision context, and versioned input refs. |
| `scripts/validate_register.py` | Rewritten against the Quasar register schema; retains the source's provenance, link, and bounded-field checking approach. |
| `scripts/evaluate_matrix.py` | Adapted; same disclosed weighted-additive model, normalization, interval, and one-at-a-time weight-sensitivity behavior, applied to candidates and gate columns. |
| `references/method-core.md`, `references/evaluation-and-gates.md`, `references/responsible-ai.md`, `references/sources.md` | Adapted prose and dated source list, generalized beyond scientific research. |
| `references/ideation-register.schema.json`, `scripts/freeze_baseline.py`, the profile references, and `references/handoffs.md` | Original Quasar work; no source equivalent. |

### Quasar modifications

- Generalized `idea` to `candidate` with profile-scoped kinds, `predicted_observations` to `expected_signals`, and `literature_checks` to routed `evidence_requests`.
- Replaced in-session literature search with typed handoffs to the Quasar research, technical-research, and prototype owners.
- Added decision context, information governance, adoption dispositions, an approved snapshot with a required approval block, and the package artifact-authority, lifecycle, and single-writer rules.
- Kept the scientific gates inside the scientific profile and added generic, product, and consulting gate families.

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
