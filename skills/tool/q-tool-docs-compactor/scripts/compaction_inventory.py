#!/usr/bin/env python3
"""Inventory a documentation scope for compaction: measure size, find shared passages, flag superseded-content signals.

Runs offline on local files only. Token figures are estimates (characters / 4),
never a tokenizer count; use them to compare a before and an after, not as an
absolute claim.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "1.0"
ESTIMATION = "characters-div-4-heuristic"
DEFAULT_EXTENSIONS = {".md", ".markdown", ".mdx", ".txt", ".rst", ".adoc", ".yaml", ".yml"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".cache", "dist", "build"}

MARKERS: tuple[tuple[str, str], ...] = (
    ("todo", r"\b(?:TODO|FIXME|XXX)\b"),
    ("deprecated", r"\bdeprecated\b"),
    ("legacy", r"\blegacy\b"),
    ("obsolete", r"\bobsolete\b"),
    ("superseded", r"\bsuperseded\b"),
    ("no-longer", r"\bno longer\b"),
    ("previously", r"\b(?:previously|formerly)\b"),
    ("old-version", r"\bold (?:version|approach|implementation|process|flow)\b"),
    ("replaced", r"\b(?:was|were|has been|have been) replaced\b"),
    ("removed", r"\b(?:was|were|has been|have been) removed\b"),
    ("migrated", r"\bmigrated (?:from|to)\b"),
    ("historical", r"\bhistorical(?:ly)?\b"),
    ("obsoleto", r"\bobsolet[oa]s?\b"),
    ("antiguo", r"\bantigu[oa]s?\b"),
    ("anteriormente", r"\banteriormente\b"),
    ("ya-no", r"\bya no\b"),
    ("reemplazado", r"\b(?:fue|fueron|ha sido|han sido) reemplazad[oa]s?\b"),
    ("heredado", r"\b(?:heredad[oa]s?|legado)\b"),
    ("superado", r"\bsuperad[oa]s?\b"),
    ("eliminado", r"\b(?:fue|fueron|ha sido|han sido) eliminad[oa]s?\b"),
)
MARKER_PATTERNS = tuple((label, re.compile(pattern, re.IGNORECASE)) for label, pattern in MARKERS)
TABLE_SEPARATOR = re.compile(r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?$")


def collect_files(paths: Iterable[str], all_files: bool) -> tuple[list[Path], list[str]]:
    files: list[Path] = []
    missing: list[str] = []
    seen: set[Path] = set()
    for raw in paths:
        path = Path(raw)
        if not path.exists():
            missing.append(raw)
            continue
        candidates = [path] if path.is_file() else sorted(
            p for p in path.rglob("*")
            if p.is_file() and not any(part in SKIP_DIRS or part.startswith(".") for part in p.relative_to(path).parts[:-1])
        )
        for candidate in candidates:
            if not all_files and candidate.suffix.lower() not in DEFAULT_EXTENSIONS:
                continue
            resolved = candidate.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            files.append(candidate)
    return files, missing


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def estimate_tokens(text: str) -> int:
    return int(math.ceil(len(text) / 4)) if text else 0


def measure(files: list[Path]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for path in files:
        text = read_text(path)
        rows.append({
            "path": str(path),
            "lines": len(text.splitlines()),
            "words": len(text.split()),
            "characters": len(text),
            "estimated_tokens": estimate_tokens(text),
        })
    rows.sort(key=lambda row: (-row["estimated_tokens"], row["path"]))
    total = {key: sum(row[key] for row in rows) for key in ("lines", "words", "characters", "estimated_tokens")}
    total["files"] = len(rows)
    return {"schema_version": SCHEMA_VERSION, "command": "measure", "estimation": ESTIMATION, "files": rows, "total": total}


def normalize(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip()).lower()


def overlap(files: list[Path], min_chars: int) -> dict[str, Any]:
    index: dict[str, dict[str, str]] = {}
    for path in files:
        for line in read_text(path).splitlines():
            key = normalize(line)
            if len(key) < min_chars or TABLE_SEPARATOR.match(line.strip()) or key.startswith("```"):
                continue
            index.setdefault(key, {}).setdefault(str(path), line.strip())
    pairs: dict[tuple[str, str], list[str]] = {}
    per_file: dict[str, int] = {}
    for key, owners in index.items():
        if len(owners) < 2:
            continue
        names = sorted(owners)
        for name in names:
            per_file[name] = per_file.get(name, 0) + 1
        for i, left in enumerate(names):
            for right in names[i + 1:]:
                pairs.setdefault((left, right), []).append(owners[left])
    pair_rows = [
        {"files": [left, right], "shared_lines": len(samples), "samples": [s[:80] for s in samples[:3]]}
        for (left, right), samples in pairs.items()
    ]
    pair_rows.sort(key=lambda row: (-row["shared_lines"], row["files"]))
    file_rows = [{"path": name, "lines_shared_with_other_files": count} for name, count in sorted(per_file.items(), key=lambda item: (-item[1], item[0]))]
    return {
        "schema_version": SCHEMA_VERSION,
        "command": "overlap",
        "min_line_chars": min_chars,
        "pairs": pair_rows,
        "files": file_rows,
        "total": {"files": len(files), "pairs_with_overlap": len(pair_rows), "shared_lines": sum(row["shared_lines"] for row in pair_rows)},
    }


def markers(files: list[Path]) -> dict[str, Any]:
    hits: list[dict[str, Any]] = []
    counts: dict[str, int] = {}
    for path in files:
        for number, line in enumerate(read_text(path).splitlines(), 1):
            for label, pattern in MARKER_PATTERNS:
                if pattern.search(line):
                    hits.append({"path": str(path), "line": number, "marker": label, "snippet": line.strip()[:100]})
                    counts[label] = counts.get(label, 0) + 1
    return {
        "schema_version": SCHEMA_VERSION,
        "command": "markers",
        "hits": hits,
        "counts": dict(sorted(counts.items(), key=lambda item: (-item[1], item[0]))),
        "total": {"files": len(files), "hits": len(hits)},
    }


def print_table(headers: list[str], rows: list[list[Any]]) -> None:
    widths = [max(len(str(cell)) for cell in column) for column in zip(headers, *rows)] if rows else [len(h) for h in headers]
    line = " | ".join(str(cell).ljust(width) for cell, width in zip(headers, widths))
    print(line)
    print("-+-".join("-" * width for width in widths))
    for row in rows:
        print(" | ".join(str(cell).ljust(width) for cell, width in zip(row, widths)))


def emit_text(result: dict[str, Any]) -> None:
    command = result["command"]
    if command == "measure":
        print_table(
            ["path", "lines", "words", "chars", "est_tokens"],
            [[r["path"], r["lines"], r["words"], r["characters"], r["estimated_tokens"]] for r in result["files"]],
        )
        t = result["total"]
        print("\ntotal: %d files, %d lines, %d words, %d chars, ~%d estimated tokens (%s)"
              % (t["files"], t["lines"], t["words"], t["characters"], t["estimated_tokens"], result["estimation"]))
    elif command == "overlap":
        if not result["pairs"]:
            print("no passages of %d+ characters are shared between files" % result["min_line_chars"])
            return
        for pair in result["pairs"]:
            print("%s <-> %s: %d shared lines" % (pair["files"][0], pair["files"][1], pair["shared_lines"]))
            for sample in pair["samples"]:
                print("    %s" % sample)
        t = result["total"]
        print("\ntotal: %d file pairs share %d lines" % (t["pairs_with_overlap"], t["shared_lines"]))
    else:
        for hit in result["hits"]:
            print("%s:%d [%s] %s" % (hit["path"], hit["line"], hit["marker"], hit["snippet"]))
        print("\ntotal: %d signals in %d files; signals are candidates for review, not verdicts"
              % (result["total"]["hits"], result["total"]["files"]))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="compaction_inventory.py",
        description=(
            "Inventory a documentation scope for compaction without network access or installation: "
            "measure size, find passages shared between files, and flag superseded-content signals. "
            "Token figures are estimates (characters / 4), never a tokenizer count."
        ),
    )
    parser.add_argument("command", choices=("measure", "overlap", "markers"))
    parser.add_argument("paths", nargs="+", help="files or directories; directories are searched recursively")
    parser.add_argument("--json", action="store_true", help="emit a JSON object instead of text")
    parser.add_argument("--all-files", action="store_true", help="include every regular file, not only documentation extensions")
    parser.add_argument("--min-line-chars", type=int, default=40, help="overlap: ignore normalized lines shorter than this (default 40)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    files, missing = collect_files(args.paths, args.all_files)
    if missing:
        print("error: path not found: %s" % ", ".join(missing), file=sys.stderr)
        return 2
    if not files:
        print("error: no documentation files found under the given paths", file=sys.stderr)
        return 2
    if args.command == "measure":
        result = measure(files)
    elif args.command == "overlap":
        result = overlap(files, args.min_line_chars)
    else:
        result = markers(files)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        emit_text(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
