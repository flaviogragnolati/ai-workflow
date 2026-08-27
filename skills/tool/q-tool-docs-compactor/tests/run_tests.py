#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "compaction_inventory.py"
FIXTURES = ROOT / "tests" / "fixtures"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
        cwd=ROOT,
    )


def main() -> int:
    passed = 0

    help_result = run("--help")
    assert help_result.returncode == 0, help_result.stderr
    help_text = " ".join(help_result.stdout.split())  # argparse wraps lines at terminal width
    assert "never a tokenizer count" in help_text
    assert "without network access or installation" in help_text
    passed += 1

    measured = run("measure", "--json", str(FIXTURES))
    assert measured.returncode == 0, measured.stderr
    payload = json.loads(measured.stdout)
    assert payload["schema_version"] == "1.0"
    assert payload["estimation"] == "characters-div-4-heuristic"
    assert {row["path"].rsplit("/", 1)[-1] for row in payload["files"]} == {"alpha.md", "beta.md", "legacy-notes.md"}
    for row in payload["files"]:
        text = Path(row["path"]).read_text(encoding="utf-8")
        assert row["characters"] == len(text)
        assert row["estimated_tokens"] == math.ceil(len(text) / 4)
        assert row["lines"] == len(text.splitlines())
    assert payload["total"]["estimated_tokens"] == sum(row["estimated_tokens"] for row in payload["files"])
    assert payload["total"]["files"] == 3
    passed += 1

    text_measure = run("measure", str(FIXTURES / "alpha.md"))
    assert text_measure.returncode == 0
    assert "estimated tokens" in text_measure.stdout
    passed += 1

    overlapped = run("overlap", "--json", str(FIXTURES / "alpha.md"), str(FIXTURES / "beta.md"), str(FIXTURES / "legacy-notes.md"))
    assert overlapped.returncode == 0, overlapped.stderr
    overlap_payload = json.loads(overlapped.stdout)
    assert overlap_payload["total"]["pairs_with_overlap"] == 1
    pair = overlap_payload["pairs"][0]
    assert {p.rsplit("/", 1)[-1] for p in pair["files"]} == {"alpha.md", "beta.md"}
    assert pair["shared_lines"] == 3
    assert len(pair["samples"]) == 3
    passed += 1

    flagged = run("markers", "--json", str(FIXTURES / "legacy-notes.md"), str(FIXTURES / "alpha.md"))
    assert flagged.returncode == 0, flagged.stderr
    marker_payload = json.loads(flagged.stdout)
    labels = {hit["marker"] for hit in marker_payload["hits"]}
    assert {"deprecated", "replaced", "todo", "antiguo", "ya-no", "no-longer"} <= labels, labels
    assert all(hit["line"] >= 1 and hit["snippet"] for hit in marker_payload["hits"])
    assert marker_payload["total"]["hits"] == len(marker_payload["hits"])
    passed += 1

    missing = run("measure", str(FIXTURES / "does-not-exist.md"))
    assert missing.returncode == 2
    assert "path not found" in missing.stderr
    passed += 1

    print(f"q-tool-docs-compactor tests: {passed} passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
