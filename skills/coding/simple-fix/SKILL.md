---
name: simple-fix
description: "Apply a guarded minimal fix in a T3 codebase when the cause and correction are already confirmed. Use for a narrow defect with a clear diagnosis; escalate to debug when investigation is needed or to refinement when behavior or architecture must change."
---

# Simple fix

This skill supports `t3-core`.

## Procedure

1. Confirm the reported cause in the real code.
2. Map the blast radius and must-not-break behavior.
3. Stop if the correction crosses modules, changes a contract, or requires product or architecture decisions.
4. Apply the smallest complete fix.
5. Add or update regression coverage.
6. Run focused tests, type checking, and other proportional project checks.
7. Run the required mini review.
8. Update the original durable execution record.

Do not use this path to hide a feature or design change. Use `debug` when the cause is uncertain. Keep internal notes transient.
