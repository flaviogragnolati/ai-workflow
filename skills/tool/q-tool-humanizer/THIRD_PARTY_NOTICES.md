# Third-party notices

## Softaworks agent-toolkit

`q-tool-humanizer` adapts selected pattern organization and clear-writing concepts from two Agent Skills in Softaworks' `agent-toolkit`.

- **Source repository:** <https://github.com/softaworks/agent-toolkit>
- **Commit consulted:** `3027f20f3181758385a1bb8c022d4041dfb4de84`
- **Source skills:** [`humanizer`](https://github.com/softaworks/agent-toolkit/tree/3027f20f3181758385a1bb8c022d4041dfb4de84/skills/humanizer) and [`writing-clearly-and-concisely`](https://github.com/softaworks/agent-toolkit/tree/3027f20f3181758385a1bb8c022d4041dfb4de84/skills/writing-clearly-and-concisely)
- **Copyright:** © 2026 Leonardo Flores
- **License:** MIT, reproduced below
- **Upstream credit preserved by `humanizer`:** original skill by [`@blader`](https://github.com/blader/humanizer)

### File-by-file relationship

| File here | Relationship to the source |
|---|---|
| `SKILL.md` | Original Quasar procedure and authority model. Adapts the upstream separation of pattern detection, rewriting, voice, and clear-writing principles into three explicit tasks with anti-fabrication, bilingual routing, transient outputs, and approval boundaries. |
| `references/patterns-en.md` | Reorganizes selected upstream pattern concepts under Quasar `H1` through `H9`; all examples and correction guidance were rewritten to avoid unsupported specificity. The Wikipedia adaptation below also applies. |
| `references/patterns-es.md` | Original native-Spanish pattern catalog aligned to the Quasar `H` taxonomy; it is not a translation of the upstream English watch list. The Wikipedia adaptation below also applies. |
| `references/clarity-en.md` | Adapts the source skill's selection of composition principles into a modern checklist with original examples and Quasar meaning-preservation rules. |
| `references/clarity-es.md` | Original Spanish adaptation of the `C` taxonomy with native syntax, usage, register, and language-clear concerns. |
| `agents/openai.yaml` | Original Quasar invocation metadata. |

### Deliberately not incorporated

Quasar does not copy the upstream frontmatter, universal activation rule, subagent dispatch strategy, README files, full *Elements of Style* chapters, embedded `signs-of-ai-writing.md`, output template, or examples that add facts absent from their source text. It also does not import Wikipedia-specific cleanup policy, wikitext handling, or deletion procedure.

### Quasar modifications

- Split detection, humanization, and clarity into `detect`, `rewrite`, and `improve` while retaining one semantic owner.
- Added English and Spanish reference routing with honest partial coverage for other languages.
- Replaced binary authorship claims with localized indicators, density, severity, and evidence-owner routes.
- Made facts, quotations, citations, uncertainty, and commitments immutable during editing.
- Assigned generic wordiness to `C4` so one span is not reported under both AI-pattern and clarity families.
- Added explicit write and overwrite approval boundaries and no durable artifact authority.

### MIT License

```text
MIT License

Copyright (c) 2026 Leonardo Flores

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

## Wikipedia contributors

The descriptive `H1` through `H9` taxonomy, its caution against binary detection, and the separation between surface indicators and evidence problems adapt material from these English Wikipedia project pages:

- [*Wikipedia:Signs of AI writing*, revision `1369279283`](https://en.wikipedia.org/w/index.php?oldid=1369279283&title=Wikipedia%3ASigns_of_AI_writing), 14 August 2026.
- [*Wikipedia:WikiProject AI Cleanup*, revision `1369089165`](https://en.wikipedia.org/w/index.php?oldid=1369089165&title=Wikipedia%3AWikiProject_AI_Cleanup), 13 August 2026.
- **Authors:** Wikipedia contributors; each page history identifies individual contributors.
- **License:** [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/) (CC BY-SA 4.0).

`references/patterns-en.md` and `references/patterns-es.md` are adapted materials under CC BY-SA 4.0. Quasar condensed and generalized the Wikipedia-specific field guide, assigned stable `H` IDs, removed Wikipedia-only policy and markup procedure, added bilingual and owner-routing rules, and replaced source examples with original examples that preserve supplied facts. No endorsement by Wikipedia or its contributors is implied.

The source pages and their attribution and share-alike requirements remain authoritative for the adapted portions. The repository's MIT license continues to cover original Quasar material outside separately licensed portions identified here.

## William Strunk Jr., The Elements of Style

The `C1` through `C9` taxonomy is conceptually informed by composition principles in William Strunk Jr.'s early *The Elements of Style*. The source skill identifies the 1918 text; [Project Gutenberg ebook 37134](https://www.gutenberg.org/ebooks/37134) provides a 1920 edition and marks it public domain in the United States.

Quasar incorporates no verbatim Strunk prose, examples, usage chapter, manuscript-formatting chapter, or historically dated word list. `references/clarity-en.md` distills selected principles with original modern examples. `references/clarity-es.md` adapts the principles independently to Spanish and adds original language-specific guidance.
