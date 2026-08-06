# Skill mechanics

Read this reference only when the target artifact is a skill. Apply the shared writing procedure in [`SKILL.md`](SKILL.md) first; use this file for skill packaging and reachability.

## Choose the invocation surface

| Skill role | Manifest and interface |
|---|---|
| User entry point | Set `invocable: true`, use `orchestrated` or `standalone` execution as appropriate, and provide matching `agents/openai.yaml` metadata. |
| Internal companion | Set `invocable: false` with `execution_modes: [internal]`, omit `agents/openai.yaml`, and add a strong pointer from `AGENTS.md` or every owning skill that must load it. |

An internal companion is not a direct target and inherits authority, side effects, and approval boundaries from its caller. Keep its persistent outputs empty; the owning task owns any durable artifact.

Split out another skill only when it needs independent reach: it has a distinct trigger concept used in real prompts or another owner must load it directly. Otherwise keep the branch in the existing skill or disclose it as reference. The independent route must justify the context and pointer load it adds.

## Write the context pointer

Treat frontmatter `description` as the skill's top-level context pointer and apply the pointer rules in [`SKILL.md`](SKILL.md#3-choose-the-narrowest-useful-artifact). Make `name` match the folder and manifest ID. For an internal companion, name its consumers and state that it is not a user entry point.

## Keep the body executable

Write the skill in imperative form. Keep the shared path in `SKILL.md`, move branch-only detail into directly linked references, and state when each reference must be read. Avoid nested reference chains and supplementary README or changelog files inside the skill directory.

Complete the skill only when its manifest role, folder, frontmatter, pointers, invocation surface, side effects, output authority, and validation evidence agree.
