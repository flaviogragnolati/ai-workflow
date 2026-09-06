#!/usr/bin/env python3
"""Apply or verify Quasar's exact Archify patch during package maintenance."""

import argparse
import hashlib
from pathlib import Path
import subprocess

PATCH = Path(__file__).resolve().parent / "patches/archify-subprocess-diagnostics.patch"
UPSTREAM_CLI_SHA256 = "304fc9aa27d069b724dfd57f8df50e3aac574760199b20652dad987b3ca20594"
PATCHED_CLI_SHA256 = "ed009ef30d21b8b8329a3266115d2239d145fee74fb3a1ab6dc69806c8076962"
PATCH_SHA256 = "46e0503270a0ccc9d8a35179a0646e42c41a8b3fe9fe8e2fb7fa74f4426bab1a"


def require_hash(path: Path, expected: str) -> None:
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise ValueError(f"Archify patch integrity mismatch: {path}")


def verify_runtime_patch(runtime: Path) -> None:
    require_hash(PATCH, PATCH_SHA256)
    require_hash(runtime / "bin/archify.mjs", PATCHED_CLI_SHA256)
    metadata = dict(line.split("=", 1) for line in (runtime / "ARCHIFY_VERSION").read_text().splitlines() if "=" in line)
    if metadata.get("patch_sha256") != PATCH_SHA256:
        raise ValueError("Archify runtime metadata does not identify the maintained patch")


def apply_runtime_patch(runtime: Path) -> None:
    require_hash(PATCH, PATCH_SHA256)
    require_hash(runtime / "bin/archify.mjs", UPSTREAM_CLI_SHA256)
    subprocess.run(["patch", "--batch", "--forward", "--fuzz=0", "-p1", "-i", str(PATCH)],
                   cwd=runtime, check=True, capture_output=True, text=True)
    require_hash(runtime / "bin/archify.mjs", PATCHED_CLI_SHA256)
    metadata_path = runtime / "ARCHIFY_VERSION"
    metadata = metadata_path.read_text()
    metadata_path.write_text(metadata.rstrip("\n") + f"\npatch_sha256={PATCH_SHA256}\n")
    verify_runtime_patch(runtime)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("apply", "verify"))
    parser.add_argument("runtime", type=Path)
    args = parser.parse_args()
    try:
        (apply_runtime_patch if args.operation == "apply" else verify_runtime_patch)(args.runtime.resolve())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"{error}\n")
    print(f"Archify maintained patch: {args.operation} passed")


if __name__ == "__main__":
    main()
