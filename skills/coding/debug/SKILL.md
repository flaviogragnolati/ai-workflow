---
name: debug
description: "Diagnose and fix reproducible or hard failures in a T3 codebase using evidence, ranked hypotheses, focused tests, and proportional validation. Use when behavior is broken, failing, slow, flaky, or incorrect and the cause is not already confirmed."
---

# Debug

This skill supports `t3-core`. Read `HARD-BUGS.md` when the failure is flaky, non-deterministic, performance-sensitive, or requires a substantial reproduction harness.

## Procedure

1. Pin the expected and observed behavior, environment, frequency, and smallest known trigger.
2. Establish a fast pass/fail signal with a focused test or disposable reproduction.
3. Trace the relevant flow, data, boundaries, and recent changes.
4. Form a small ranked hypothesis set; state evidence that would falsify each.
5. Test hypotheses before editing.
6. Apply the smallest correction that resolves the verified cause.
7. Add or update regression coverage.
8. Run focused tests, type checking, and other proportional project checks.
9. Run the mini review required by the workflow.
10. Update the original durable execution record.

Use `simple-fix` when the cause and correction are already confirmed. Escalate to refinement when the change alters product behavior, architecture, or a cross-module contract.

Do not treat a throwaway reproduction, scratchpad, or internal plan as a durable artifact.
