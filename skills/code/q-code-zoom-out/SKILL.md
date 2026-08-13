---
name: q-code-zoom-out
description: "Map the relevant modules, callers, dependencies, and domain responsibilities one abstraction level above the current code. Use when the user or agent needs orientation before reasoning about an unfamiliar implementation area. Part of the Quasar AI delivery skills."
---

Inspect the repository and present a concise map of the relevant modules, callers, dependencies, ownership, and main data or control flow. Use project domain vocabulary. State the evidence inspected and any uncertainty. Do not modify files.

When `user-requests-a-transient-higher-level-module-map` and `q-tool-mermaid` is installed, delegate the observed map and return the result transiently. If the tool is absent, `return-the-textual-module-map-and-state-the-visual-capability-gap`.
