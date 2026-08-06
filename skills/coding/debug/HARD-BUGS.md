# HARD-BUGS — the heavy gear of the `debug` skill

Open this annex from `debug` when any of these is true:

- It's a **performance regression** — logs lie about timing; you need baselines, profiling, and bisection.
- It's **flaky / non-deterministic / a heisenbug** — you can't get a signal that fails reliably enough to debug against.
- Reproducing it needs an **elaborate harness** — multi-service orchestration, captured production traffic, a bisection rig.
- The two everyday signal techniques (focused vitest run, sandbox script) **don't reach the bug**.

Everything in the main SKILL.md still applies — the loop is the same. This annex changes the *posture*: spend disproportionate effort on the feedback loop, be aggressive, be creative, refuse to give up. On hard bugs, generate **3–5 ranked hypotheses** instead of 2–3 — the cause space is genuinely larger. And here the gate is strict: **no red-capable command, no hypothesizing.** If you're reading code to build a theory before that command exists, stop.

## The full catalog — ways to construct a feedback loop

Try them in roughly this order; combine freely:

1. **Failing test** at whatever seam reaches the bug — unit, integration, e2e (`pnpm test`, `pnpm test:e2e`).
2. **Curl / HTTP script** against a running dev server — for tRPC, replay the exact batched request the client sent.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright) — drives the UI, asserts on DOM / console / network. The `e2e/` setup is already there; a throwaway spec is cheap.
5. **Replay a captured trace.** Save a real network request / payload / event log to disk; replay it through the code path in isolation. The real tRPC input or the exact DB row that breaks is worth more than ten synthetic fixtures.
6. **Throwaway harness.** Spin up a minimal subset of the system (one procedure, mocked deps) that exercises the bug code path with a single function call.
7. **Property / fuzz loop.** If the bug is "sometimes wrong output", run 1000 random inputs (vitest + a seeded generator) and look for the failure mode.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old-version vs new-version (or two configs) and diff outputs.
10. **HITL bash script.** Last resort. If a human must click, drive *them* with `scripts/hitl-loop.template.sh` so the loop is still structured — the script prompts the user step by step and prints captured answers as `KEY=VALUE` for you to parse.

Build the right feedback loop, and the bug is 90% fixed. Then tighten it exactly as the main skill says: faster, sharper assertion, more deterministic.

## Non-deterministic bugs

The goal is not a clean repro but a **higher reproduction rate**. Loop the trigger 100×, parallelise, add stress, narrow timing windows, inject sleeps at suspected race points. A 50%-flake bug is debuggable; a 1% one is not — keep raising the rate until it's debuggable, then treat that pinned rate as your "deterministic enough" signal (e.g. "fails ≥40 of 100 runs" is a red/green verdict).

Common determinism levers in this stack: seed RNG, pin time (`vi.setSystemTime`), isolate the DB per run, freeze network with mocks, serialize concurrent test files.

## Performance regressions

Logs are usually wrong about timing. Instead:

1. **Baseline first.** A timing harness around the suspect path (`performance.now()`, vitest bench, a profiler run, or the DB query plan via `EXPLAIN ANALYZE` for Prisma-generated SQL). No baseline, no claims.
2. **Measure, then bisect** — over commits (`git bisect run` with the timing harness as the verdict), over inputs (which payload size / shape triggers the cliff), or over layers (is the time in the procedure, the query, or the render?).
3. Only then fix — and prove it against the same baseline, same machine, same data.

A perf "signal" is a threshold assertion: *"this command completes in < X ms on fixture Y"* — red now, green after the fix.

## When you genuinely cannot build a loop

Stop and say so explicitly. List what you tried. Ask the user for:

- (a) access to whatever environment reproduces it,
- (b) a captured artifact — HAR file, log dump, core dump, screen recording with timestamps — you can replay or inspect, or
- (c) permission to add temporary, tagged (`[DEBUG-...]`) production instrumentation.

Do **not** proceed to hypothesize without a loop. A theory without a signal to test it against is exactly the failure this skill exists to prevent.
