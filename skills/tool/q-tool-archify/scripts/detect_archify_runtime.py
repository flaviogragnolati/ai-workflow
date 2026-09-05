#!/usr/bin/env python3
"""Detect the vendored Archify runtime without network access or installation."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect the vendored Archify runtime without network access or installation."
    )
    parser.add_argument("--json", action="store_true", help="Emit one JSON capability record")
    parser.add_argument("--runtime-root", type=Path, help="Override the vendored runtime root")
    parser.add_argument("--node", help="Override the Node.js executable")
    return parser.parse_args()


def version_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            key, separator, value = line.partition("=")
            if separator:
                values[key] = value
    except OSError:
        pass
    return values


def find_browser() -> str | None:
    for variable in ("CHROME_PATH", "PUPPETEER_EXECUTABLE_PATH"):
        candidate = os.environ.get(variable)
        if candidate and Path(candidate).is_file() and os.access(candidate, os.X_OK):
            return candidate
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        candidate = shutil.which(name)
        if candidate:
            return candidate
    return None


def probe(runtime_root: Path, node_override: str | None) -> dict[str, Any]:
    metadata = version_file(runtime_root / "ARCHIFY_VERSION")
    release_version = None
    try:
        release_version = json.loads((runtime_root / "skill-release.json").read_text(encoding="utf-8"))["version"]
    except (OSError, KeyError, TypeError, json.JSONDecodeError):
        pass

    nested_skill_absent = not any(runtime_root.rglob("SKILL.md")) if runtime_root.is_dir() else True
    update_checker_absent = not (runtime_root / "scripts" / "check-update.mjs").exists()
    node_path = node_override or shutil.which("node")
    node_version = None
    node_status = "unavailable"
    doctor_status = "unavailable"
    failed_checks: list[str] = []

    if node_path:
        try:
            version_run = subprocess.run(
                [node_path, "--version"], capture_output=True, text=True, timeout=10, check=False
            )
            node_version = version_run.stdout.strip() or version_run.stderr.strip() or None
            match = re.match(r"v?(\d+)", node_version or "")
            node_status = "ready" if version_run.returncode == 0 and match and int(match.group(1)) >= 18 else "unsupported"
        except (OSError, subprocess.TimeoutExpired):
            node_status = "unavailable"

    cli = runtime_root / "bin" / "archify.mjs"
    metadata_matches = bool(metadata.get("version") and metadata.get("version") == release_version)
    if node_status == "ready" and cli.is_file() and metadata_matches and nested_skill_absent and update_checker_absent:
        environment = dict(os.environ)
        environment["ARCHIFY_UPDATE_CHECK_DISABLED"] = "1"
        try:
            doctor = subprocess.run(
                [str(node_path), str(cli), "doctor"],
                cwd=runtime_root,
                env=environment,
                capture_output=True,
                text=True,
                timeout=20,
                check=False,
            )
            failed_checks = [line[7:].strip() for line in doctor.stdout.splitlines() if line.startswith("[fail]")]
            doctor_status = "ready" if doctor.returncode == 0 and "Archify is ready." in doctor.stdout else "degraded"
            if doctor.returncode != 0 and not failed_checks:
                failed_checks = [(doctor.stderr or doctor.stdout or "doctor failed").strip()]
        except (OSError, subprocess.TimeoutExpired) as error:
            doctor_status = "degraded"
            failed_checks = [str(error)]

    browser_path = find_browser()
    return {
        "schema_version": "1.0",
        "network_used": False,
        "installation_performed": False,
        "runtime": {
            "root": str(runtime_root.resolve()),
            "version": metadata.get("version") or release_version,
            "commit": metadata.get("commit"),
            "synced": metadata.get("synced"),
        },
        "node": {"path": node_path, "version": node_version, "status": node_status},
        "doctor": {"status": doctor_status, "failed_checks": failed_checks},
        "browser": {"status": "available" if browser_path else "unavailable", "path": browser_path},
        "policy_guards": {
            "update_checker_absent": update_checker_absent,
            "nested_skill_absent": nested_skill_absent,
        },
    }


def main() -> int:
    args = parse_args()
    default_root = Path(__file__).resolve().parents[1] / "runtime"
    result = probe((args.runtime_root or default_root).resolve(), args.node)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("runtime: %s %s" % (result["runtime"]["version"] or "unknown", result["doctor"]["status"]))
        print("node: %s" % result["node"]["status"])
        print("browser: %s" % result["browser"]["status"])
        print("network_used: false")
        print("installation_performed: false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
