#!/usr/bin/env python3
"""Inject child results at the Node boundary; no renderer or browser is launched."""

import json
import os
from pathlib import Path
import subprocess
import tempfile

RUNTIME = Path(__file__).resolve().parents[1] / "runtime"


def main():
    passed = 0
    with tempfile.TemporaryDirectory(prefix="archify-subprocess-tests-") as temporary:
        root = Path(temporary)
        hook = root / "child-result.mjs"
        hook.write_text("""
import childProcess from 'node:child_process';
import {syncBuiltinESMExports} from 'node:module';
const injected = JSON.parse(process.env.ARCHIFY_TEST_CHILD_RESULT);
childProcess.spawnSync = (_command, args) => {
  const checker = args[0].endsWith('/check-render-output.mjs');
  if (checker !== (process.env.ARCHIFY_TEST_CHILD === 'checker')) {
    return {status: 0, signal: null, stdout: '', stderr: ''};
  }
  return injected;
};
syncBuiltinESMExports();
""", encoding="utf-8")
        cases = [
            ({"status": status, "error": {"code": "EPERM", "message": "capture denied"}, "stdout": stdout}, "EPERM")
            for status in (0, 1) for stdout in ("", '{"ok":true}')
        ] + [
            ({"status": 0, "signal": "SIGTERM"}, "SIGTERM"),
            ({"status": None}, "no exit status"),
        ]
        invalid_receipts = [({"status": 0, "stdout": stdout}, "subprocess-receipt-invalid")
                            for stdout in ("", " \n", "{", "null", "[]", '{}', '{"ok":false}')]
        example = str(RUNTIME / "examples/web-app.architecture.json")
        for command in ("validate", "layout", "deliver", "compare"):
            for child in ("renderer", "checker"):
                if command == "layout" and child == "checker":
                    continue
                selected = cases + (invalid_receipts if child == "checker" else [])
                if command == "layout":
                    selected += invalid_receipts
                for overrides, expected in selected:
                    output = root / "existing.html"
                    receipt = root / "existing.receipt.json"
                    output.write_bytes(b"previous trusted artifact")
                    receipt.write_bytes(b"previous trusted receipt")
                    args = ["validate", "architecture", example, "--json"]
                    if command == "layout":
                        args += ["--layout-json"]
                    elif command == "deliver":
                        args = ["deliver", "architecture", example, str(output), "--json"]
                    elif command == "compare":
                        args = ["compare", "architecture", example, example, str(output), "--receipt", str(receipt), "--json"]
                    env = dict(os.environ, ARCHIFY_UPDATE_CHECK_DISABLED="1",
                               ARCHIFY_TEST_CHILD=child,
                               ARCHIFY_TEST_CHILD_RESULT=json.dumps({"status": 0, "signal": None, "stdout": "", "stderr": "", **overrides}))
                    result = subprocess.run([os.environ.get("NODE", "node"), "--import", str(hook),
                                             str(RUNTIME / "bin/archify.mjs"), *args],
                                            env=env, capture_output=True, text=True, timeout=20)
                    label = f"{command}/{child}/{overrides}"
                    assert result.returncode != 0, label
                    payload = json.loads(result.stdout)
                    assert payload.get("ok") is False, label
                    assert expected in json.dumps(payload), (label, payload)
                    assert "SyntaxError:" not in result.stderr, (label, result.stderr)
                    assert output.read_bytes() == b"previous trusted artifact", label
                    assert receipt.read_bytes() == b"previous trusted receipt", label
                    assert not list(root.glob(".archify-*")), label
                    passed += 1
    print(f"q-tool-archify subprocess diagnostics tests: {passed} passed")


if __name__ == "__main__":
    main()
