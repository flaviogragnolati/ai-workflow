# Web and TypeScript checks

Select each check independently for the affected package and behavior. Browser-delivered HTML, CSS and browser APIs qualify for Modern Web Guidance, including server-rendered markup. Fallow applies to code or dependency changes in a TypeScript package. Confirm TypeScript from project-owned source or build configuration. A JavaScript-only package with transitive type declarations does not qualify. A TypeScript web application can use both checks, a headless TypeScript service only Fallow.

Honor project tooling exclusions. Prefer a compatible project CLI and read its version with `--version`. The examples assume its executable is on the path. With Node.js 22+ and a populated npm cache, substitute `npx --offline --yes modern-web-guidance@1.0.2` or `npx --offline --yes fallow@3.48.0` for the command name.

For first use, someone authorized to download tools can populate the cache from a temporary directory with the applicable command. A read-only reviewer with a cache miss can consume supplied evidence or report the gap.

```sh
DISABLE_TELEMETRY=1 npx --yes --ignore-scripts modern-web-guidance@1.0.2 --version
DO_NOT_TRACK=1 npx --yes --ignore-scripts fallow@3.48.0 --version
```

## Browser code

1. Before implementing a browser behavior, search in English for the user interaction and retrieve the matching guide. These commands look up a form that shows errors before the user touches a field.

   ```sh
   DISABLE_TELEMETRY=1 modern-web-guidance search "validate a form field after interaction"
   DISABLE_TELEMETRY=1 modern-web-guidance retrieve validate-input-after-interaction
   ```

   Read the returned guide or its reported temporary file. Check the recommended feature against the project's browser targets, accessibility requirements and design system. Preserve necessary fallbacks and verify the affected interaction with the project's browser checks. [Google Modern Web Guidance](https://developer.chrome.com/docs/modern-web-guidance)

2. For review, set `web_path` to the affected file or directory and run the scanner. For a diff, verify each match against the fixed comparison. For a broader audit, use the agreed web surface.

   ```sh
   DISABLE_TELEMETRY=1 modern-web-guidance legacy-scan "$web_path" --json
   ```

   Inspect the scanned file count and the rule's `keepWhen` and `dropWhen` criteria. Retrieve the guide behind a relevant match and check the surrounding code. A clean scan covers only the deterministic rules on the files actually scanned. Use the guide and browser evidence for behavior outside that set. [Google modernization workflow](https://developer.chrome.com/docs/modern-web-guidance/modernization-workflow)

## TypeScript code

Run Fallow from the project root so it can resolve workspace imports and entry points. Set `ts_scope` to the in-scope TypeScript package or directory. Use `.` for a whole TypeScript project. For a mini review, set `review_diff` to the unified diff for the fixed baseline and reviewed snapshot. Include new files in scope and use paths relative to the project root.

```sh
# Mini review
DO_NOT_TRACK=1 fallow --no-cache --format json --diff-file "$review_diff" "$ts_scope"

# Codebase audit
DO_NOT_TRACK=1 fallow --no-cache --format json "$ts_scope"
```

Inspect the JSON findings and stderr, including skipped files, missing dependencies and unresolved entry points. The combined report can exit zero with findings. Check unused exports against public and dynamic consumers, and trace duplication, cycles or complexity to a concrete impact. Project-wide findings can survive a diff filter. Include them in a mini review only when the change introduces or exposes the problem. Keep the project's typecheck and tests as separate evidence. [Fallow](https://github.com/fallow-rs/fallow)

## Return evidence

Record the tool version, command, actual paths or diff identity, applicable guide or rule, confirmed locations and coverage limits. The implementer passes evidence in the existing review bundle. The reviewer returns its conclusions in the standards review or codebase audit. Reuse a run only for the same snapshot and scope. Keep raw reports transient. If a CLI, compatible runtime, required comparison or meaningful scan coverage is missing, identify the gap and continue with applicable project checks. Block only when the missing evidence is required for acceptance. Return corrections to the implementation owner.
