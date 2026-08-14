---
name: q-research-scope
description: "Turn a bounded Quasar engagement uncertainty into an authorized Research Brief with stable questions, decision links, explicit inclusions and exclusions, search strategies, privacy limits, and a time or cost budget. Use before consulting research begins or when its scope must be reconciled. Requires the q-core-contract companion."
---

# Scope engagement research

Produce an authorized Research Brief that makes the decision, evidence boundary, and stopping conditions inspectable before investigation begins.

Read the `q-core-contract` companion for shared governance; if it is missing, stop and install it with `npx skills add flaviogragnolati/ai-workflow --skill q-core-contract`. Validate the output against `references/research-brief.schema.yaml`.

## Inputs

Accept a direct question or unresolved external uncertainty from intake, a Discovery Brief, a `q-ask-*` result, an ideation snapshot's evidence requests, or another approved project artifact. Preserve source IDs and separate client evidence, accepted facts, assumptions, and evidence gaps.

Treat an evidence request from ideation as a candidate question with a recorded decision impact, not an authorized one: it still passes RADAR, boundaries, privacy limits, budget, and explicit approval here.

## Question readiness

When a clear question already identifies its decision and boundaries, validate it directly. When ambiguity would change the investigation, propose one to five candidate questions and assess each with **RADAR**:

- **Researchable:** a plausible evidence strategy fits the authorized budget.
- **Anchored:** geography, period, market or population, segment, and key terms are bounded.
- **Decision-linked:** the answer can change a named decision.
- **Adds evidence:** the work addresses a real gap instead of repeating accepted client evidence.
- **Relevant:** the answer remains useful at the decision horizon.

Score each criterion from 1 to 5. A candidate passes when its average is at least 3.0 and no criterion is below 2. Use the score to focus human judgment; it is not a scientific-validity claim.

## Procedure

1. Assign stable `RQ-*` IDs and link each question to one or more decision IDs.
2. Define `in_scope`, `out_of_scope`, assumptions, known evidence, and privacy constraints.
3. Declare planned search strategies, relevant source classes, time or cost limits, and stopping conditions per question.
4. Make subquestions inherit the parent boundary. Treat any expansion as a proposed scope change that requires approval.
5. Obtain explicit approval of questions, limits, strategies, privacy boundary, and budget.
6. Write the versioned `Working` Research Brief and return its stage delta.

Complete only with an authorized brief. If no question is researchable within the available boundary, return `blocked` with candidate questions, reasons, and one recovery action.

## Anti-patterns

| # | Anti-pattern | How it shows up | Correct behavior |
|---|---|---|---|
| 1 | Manufacturing alternatives | The agent invents candidate questions although the supplied question is already clear. | Validate the clear question and spend alignment only on material ambiguity. |
| 2 | Letting a score approve scope | A passing RADAR average is treated as user authorization. | Present the assessment and obtain explicit approval of questions, limits, and budget. |
| 3 | Hiding scope expansion in a subquestion | A child question silently adds a geography, segment, or time horizon. | Inherit the parent boundary or record and approve a scope change. |
