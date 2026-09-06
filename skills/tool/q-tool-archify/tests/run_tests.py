#!/usr/bin/env python3
"""Offline contract and runtime tests for q-tool-archify."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


SKILL_ROOT = Path(__file__).resolve().parents[1]
RUNTIME = SKILL_ROOT / "runtime"
PROBE = SKILL_ROOT / "scripts" / "detect_archify_runtime.py"
NODE = os.environ.get("NODE", "node")
ENV = dict(os.environ, ARCHIFY_UPDATE_CHECK_DISABLED="1")


def run(command: list[str], timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=SKILL_ROOT,
        env=ENV,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def json_stdout(result: subprocess.CompletedProcess[str]) -> dict:
    require(result.returncode == 0, result.stderr or result.stdout)
    return json.loads(result.stdout)


def main() -> int:
    passed = 0

    failures = run([sys.executable, str(SKILL_ROOT / "tests" / "test_subprocess_failures.py")])
    require(failures.returncode == 0, failures.stderr or failures.stdout)
    passed += 1

    help_result = run([sys.executable, str(PROBE), "--help"])
    require(help_result.returncode == 0, help_result.stderr)
    require("without network access or installation" in help_result.stdout, "probe help contract missing")
    passed += 1

    detected = json_stdout(run([sys.executable, str(PROBE), "--json"]))
    require(detected["network_used"] is False, "probe used network")
    require(detected["installation_performed"] is False, "probe installed software")
    require(all(detected["policy_guards"].values()), "probe policy guards failed")
    require(detected["doctor"]["status"] == "ready", json.dumps(detected["doctor"]))
    passed += 1

    with tempfile.TemporaryDirectory() as empty:
        unavailable = json_stdout(run([sys.executable, str(PROBE), "--json", "--runtime-root", empty]))
        require(unavailable["doctor"]["status"] == "unavailable", "missing runtime was not unavailable")
    passed += 1

    cli = RUNTIME / "bin" / "archify.mjs"
    example = RUNTIME / "examples" / "web-app.architecture.json"
    validated = json_stdout(run([NODE, str(cli), "validate", "architecture", str(example), "--quality", "showcase", "--json"]))
    require(len(validated["checks"]) == 9, "validate did not run nine checks")
    require(validated["composition"]["summary"]["errors"] == 0, "validate reported composition errors")
    passed += 1

    with tempfile.TemporaryDirectory() as temporary:
        output = Path(temporary) / "web-app.html"
        delivered = json_stdout(run([NODE, str(cli), "deliver", "architecture", str(example), str(output), "--quality", "showcase", "--json"]))
        require(delivered.get("ok") is True and output.is_file(), "deliver did not create the artifact")
        actual = hashlib.sha256(output.read_bytes()).hexdigest()
        require(delivered["artifact"]["sha256"] == actual, "delivery hash does not match artifact")
    passed += 1

    with tempfile.TemporaryDirectory() as temporary:
        output = Path(temporary) / "delta.html"
        base = RUNTIME / "examples" / "checkout-platform.base.architecture.json"
        head = RUNTIME / "examples" / "checkout-platform.head.architecture.json"
        compared = json_stdout(run([NODE, str(cli), "compare", "architecture", str(base), str(head), str(output), "--json"]))
        require(compared.get("ok") is True and output.is_file(), "compare did not create the delta")
    passed += 1

    metadata = {}
    for line in (RUNTIME / "ARCHIFY_VERSION").read_text(encoding="utf-8").splitlines():
        key, separator, value = line.partition("=")
        if separator:
            metadata[key] = value
    release = json.loads((RUNTIME / "skill-release.json").read_text(encoding="utf-8"))
    require(metadata.get("version") == release.get("version"), "runtime version files disagree")
    passed += 1

    require(not any(RUNTIME.rglob("SKILL.md")), "nested SKILL.md found in runtime")
    require(not (RUNTIME / "scripts" / "check-update.mjs").exists(), "update checker found in runtime")
    passed += 1

    print(f"q-tool-archify tests: {passed} passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
