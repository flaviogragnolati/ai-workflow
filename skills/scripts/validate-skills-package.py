from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import yaml_subset as yaml  # noqa: E402

TYPE_MAP = {
    "object": dict,
    "array": list,
    "string": str,
    "boolean": bool,
    "number": (int, float),
    "integer": int,
    "null": type(None),
}

# Agent Skills specification: 1-64 lowercase alphanumerics and hyphens, no
# leading, trailing, or consecutive hyphen.
SKILL_NAME_PATTERN = re.compile(r"(?!-)(?!.*--)[a-z0-9-]{1,64}(?<!-)")

RELATIVE_REFERENCE_PATTERN = re.compile(r"(?:\.\./)+[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*")

SKILLS_SH_SCHEMA_URL = "https://skills.sh/schemas/skills.sh.schema.json"

CORE_CONTRACT = SKILLS_ROOT / "core" / "q-core-contract"
ROUTING_DIGEST = CORE_CONTRACT / "references" / "routing.md"
HUMAN_INTERACTION_DIGEST = CORE_CONTRACT / "references" / "human-interaction.md"
IGNORED_PATH_PARTS = {".git", "node_modules", "__pycache__", ".venv"}


def ignored_path(path: Path) -> bool:
    return any(part in IGNORED_PATH_PARTS for part in path.parts)


def load(path: Path) -> Any:
    return yaml.load(path)


def schema_errors(value: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    out: list[str] = []
    if "const" in schema and value != schema["const"]:
        out.append("%s: expected %r, got %r" % (path, schema["const"], value))
    if "enum" in schema and value not in schema["enum"]:
        out.append("%s: %r is not in %r" % (path, value, schema["enum"]))
    expected = schema.get("type")
    if expected is not None:
        names = expected if isinstance(expected, list) else [expected]
        ok = any(
            name in TYPE_MAP
            and isinstance(value, TYPE_MAP[name])
            and not (name in {"number", "integer"} and isinstance(value, bool))
            for name in names
        )
        if not ok:
            out.append("%s: expected type %r, got %s" % (path, names, type(value).__name__))
            return out
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                out.append("%s: missing required key %r" % (path, key))
        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        for key, item in value.items():
            child = "%s.%s" % (path, key)
            if key in properties:
                out.extend(schema_errors(item, properties[key], child))
            elif additional is False:
                out.append("%s: additional property is not allowed" % child)
            elif isinstance(additional, dict):
                out.extend(schema_errors(item, additional, child))
    if isinstance(value, list):
        minimum = schema.get("minItems")
        if isinstance(minimum, int) and len(value) < minimum:
            out.append("%s: requires at least %d item(s)" % (path, minimum))
        if isinstance(schema.get("items"), dict):
            for index, item in enumerate(value):
                out.extend(schema_errors(item, schema["items"], "%s[%d]" % (path, index)))
    return out


def frontmatter(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        return None, ["%s: invalid UTF-8 (%s)" % (path, exc)]
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, ["%s: missing opening frontmatter" % path]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None, ["%s: missing closing frontmatter" % path]
    try:
        data = yaml.loads("\n".join(lines[1:end]))
    except Exception as exc:
        return None, ["%s: invalid frontmatter YAML (%s)" % (path, exc)]
    errors: list[str] = []
    if not isinstance(data, dict):
        return None, ["%s: frontmatter must be a mapping" % path]
    if set(data) - {"metadata"} != {"name", "description"}:
        errors.append("%s: frontmatter keys must be name, description, and optional metadata" % path)
    if "metadata" in data and data["metadata"] != {"internal": True}:
        errors.append("%s: frontmatter metadata must be exactly {internal: true}" % path)
    name = data.get("name")
    desc = data.get("description")
    if not isinstance(name, str) or not SKILL_NAME_PATTERN.fullmatch(name):
        errors.append("%s: invalid name %r" % (path, name))
    if not isinstance(desc, str) or not desc.strip():
        errors.append("%s: description must be non-empty" % path)
    elif len(desc) > 1024:
        errors.append("%s: description exceeds 1024 characters" % path)
    return data, errors


def slug(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text.strip().lower())
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    return text.replace(" ", "-")


def anchors(path: Path) -> set[str]:
    found: set[str] = set()
    counts: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match:
            base = slug(match.group(1))
            count = counts.get(base, 0)
            counts[base] = count + 1
            found.add(base if count == 0 else "%s-%d" % (base, count))
    return found


def link_errors(root: Path) -> tuple[list[str], int]:
    errors: list[str] = []
    checked = 0
    pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    for path in root.rglob("*.md"):
        if ignored_path(path):
            continue
        text = path.read_text(encoding="utf-8-sig")
        for raw in pattern.findall(text):
            href = raw.strip().split()[0].strip("<>")
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            checked += 1
            target_text, _, anchor = href.partition("#")
            target = path if not target_text else (path.parent / target_text).resolve()
            try:
                target.relative_to(root.resolve())
            except ValueError:
                errors.append("%s: local link escapes package: %s" % (path, href))
                continue
            if not target.exists():
                errors.append("%s: broken local link: %s" % (path, href))
            elif anchor and target.suffix.lower() == ".md" and anchor not in anchors(target):
                errors.append("%s: missing anchor %r in %s" % (path, anchor, target))
    return errors, checked


def openai_errors(directory: Path, skill_id: str) -> list[str]:
    path = directory / "agents" / "openai.yaml"
    if not path.is_file():
        return ["%s: missing agents/openai.yaml" % skill_id]
    try:
        data = load(path)
    except Exception as exc:
        return ["%s: invalid YAML (%s)" % (path, exc)]
    interface = data.get("interface") if isinstance(data, dict) else None
    if not isinstance(interface, dict):
        return ["%s: missing interface mapping" % path]
    errors: list[str] = []
    for key in ("display_name", "short_description", "default_prompt"):
        if not isinstance(interface.get(key), str) or not interface[key].strip():
            errors.append("%s: interface.%s must be non-empty" % (path, key))
    short = interface.get("short_description", "")
    if isinstance(short, str) and not 25 <= len(short) <= 64:
        errors.append("%s: short_description must contain 25-64 characters" % path)
    prompt = interface.get("default_prompt", "")
    if isinstance(prompt, str) and ("$" + skill_id) not in prompt:
        errors.append("%s: default_prompt must mention $%s" % (path, skill_id))
    return errors


def internal_skill_errors(directory: Path, skill_id: str, entry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if entry.get("execution_modes") != ["internal"]:
        errors.append("%s: a non-invocable active skill must use only internal execution" % skill_id)
    if entry.get("persistent_outputs"):
        errors.append("%s: an internal companion cannot own persistent outputs" % skill_id)
    interface = directory / "agents" / "openai.yaml"
    if interface.exists():
        errors.append("%s: an internal companion must not expose agents/openai.yaml" % skill_id)

    pointer_paths = [REPO_ROOT / "AGENTS.md"]
    pointer_paths.extend(
        path for path in SKILLS_ROOT.rglob("SKILL.md")
        if not ignored_path(path) and path.parent.resolve() != directory.resolve()
    )
    if not any(
        path.is_file() and skill_id in path.read_text(encoding="utf-8-sig")
        for path in pointer_paths
    ):
        errors.append("%s: internal companion is unreachable from AGENTS.md or an owning skill" % skill_id)
    return errors


def distribution_errors(skill_id: str, entry: dict[str, Any], metadata: dict[str, Any] | None) -> list[str]:
    errors: list[str] = []
    declared = entry.get("distribution", "public")
    marked = isinstance(metadata, dict) and metadata.get("metadata") == {"internal": True}
    if declared == "internal" and not marked:
        errors.append("%s: internal distribution requires frontmatter metadata.internal true" % skill_id)
    if declared != "internal" and marked:
        errors.append("%s: frontmatter hides a skill the manifest distributes publicly" % skill_id)
    return errors


def human_interaction_errors(skill_id: str, entry: dict[str, Any]) -> list[str]:
    modes = entry.get("execution_modes", [])
    interaction = entry.get("human_interaction")
    if not isinstance(modes, list) or not isinstance(interaction, dict):
        return []
    errors: list[str] = []
    mode_set = set(modes)
    key_set = set(interaction)
    if key_set != mode_set:
        missing = sorted(mode_set - key_set)
        extra = sorted(key_set - mode_set)
        errors.append("%s: human_interaction keys must equal execution_modes; missing=%s extra=%s"
                      % (skill_id, missing, extra))
    if "internal" in mode_set and interaction.get("internal") != "none":
        errors.append("%s: internal execution requires human_interaction none" % skill_id)
    if entry.get("invocable") is True and "none" in interaction.values():
        errors.append("%s: an invocable skill cannot use human_interaction none" % skill_id)
    if entry.get("invocable") is False and set(interaction.values()) != {"none"}:
        errors.append("%s: a non-invocable companion must use only human_interaction none" % skill_id)
    return errors


def identity_errors(skill_id: str, directory: Path, entry: dict[str, Any],
                    metadata: dict[str, Any] | None) -> list[str]:
    """`group` is authoritative: the name, both folders, and attribution derive from it."""
    errors: list[str] = []
    group = entry.get("group")
    if not isinstance(group, str):
        return errors
    prefix = "q-%s-" % group
    if not skill_id.startswith(prefix) or len(skill_id) <= len(prefix):
        errors.append("%s: name must be q-%s-<leaf>" % (skill_id, group))
    if directory.name != skill_id:
        errors.append("%s: folder name is %r" % (skill_id, directory.name))
    if directory.parent.name != group:
        errors.append("%s: category folder is %r, not the group %r"
                      % (skill_id, directory.parent.name, group))
    description = metadata.get("description", "") if isinstance(metadata, dict) else ""
    if entry.get("distribution", "public") != "internal" and "Quasar" not in description:
        errors.append("%s: a publicly distributed skill must name Quasar in its description" % skill_id)
    return errors


def outside_references(directory: Path) -> list[tuple[Path, str]]:
    """(file, raw) for every relative reference that leaves the skill directory."""
    found: list[tuple[Path, str]] = []
    seen: set[str] = set()
    for path in sorted(directory.rglob("*")):
        if ignored_path(path) or not path.is_file() or path.suffix.lower() not in {".md", ".yaml", ".yml"}:
            continue
        for raw in RELATIVE_REFERENCE_PATTERN.findall(path.read_text(encoding="utf-8-sig")):
            if raw in seen:
                continue
            try:
                (path.parent / raw).resolve().relative_to(directory)
            except ValueError:
                seen.add(raw)
                found.append((path, raw))
    return found


def sibling_owner(directory: Path, source: Path, raw: str, folders: dict[Path, str]) -> str | None:
    """The registered skill that owns a one-level `../<sibling>/…` reference.

    Skills are siblings both in this repository and in an installed agent
    directory, so exactly one level up still resolves for a consumer. Two or
    more levels leave the installed catalog and never resolve.
    """
    if not raw.startswith("../") or raw.startswith("../../"):
        return None
    target = (source.parent / raw).resolve()
    for candidate in (target, *target.parents):
        name = folders.get(candidate)
        if name:
            return name if candidate.parent == directory.parent else None
    return None


def reference_errors(
    skill_id: str,
    directory: Path,
    entry: dict[str, Any],
    skills: dict[str, Any],
    folders: dict[Path, str],
) -> list[str]:
    """Every reference leaving the skill must be a declared, one-level sibling."""
    errors: list[str] = []
    declared = entry.get("requires") or []
    public = entry.get("distribution", "public") != "internal"
    escapes: list[str] = []

    for source, raw in outside_references(directory):
        owner = sibling_owner(directory, source, raw, folders)
        if owner is None:
            escapes.append(raw)
        elif owner not in declared:
            errors.append("%s: sibling reference %r is not declared in requires" % (skill_id, raw))

    if public and escapes:
        errors.append("%s: reference escapes the skill directory and breaks on install: %s"
                      % (skill_id, ", ".join(sorted(escapes))))

    body = "".join(
        path.read_text(encoding="utf-8-sig")
        for path in sorted(directory.rglob("*"))
        if not ignored_path(path) and path.is_file() and path.suffix.lower() in {".md", ".yaml", ".yml"}
    )
    for name in declared:
        if name == skill_id:
            errors.append("%s: cannot require itself" % skill_id)
        elif name not in skills:
            errors.append("%s: requires unregistered skill %r" % (skill_id, name))
        elif public and skills[name].get("distribution", "public") == "internal":
            errors.append("%s: a publicly distributed skill cannot require the internal skill %r"
                          % (skill_id, name))
        if name not in body:
            errors.append("%s: requires %r but never references it" % (skill_id, name))
        elif public and "--skill %s" % name not in body:
            errors.append("%s: requires %r without an integrity check naming the install command"
                          % (skill_id, name))
    return errors


def optional_use_semantics(skills: dict[str, Any]) -> list[str]:
    """Validate optional collaboration without turning it into a hard dependency."""
    errors: list[str] = []
    for skill_id, entry in skills.items():
        if not isinstance(entry, dict):
            continue
        uses = entry.get("uses", [])
        if not isinstance(uses, list):
            continue
        seen: set[str] = set()
        required = set(entry.get("requires", [])) if isinstance(entry.get("requires"), list) else set()
        public = entry.get("distribution", "public") != "internal"
        for use in uses:
            if not isinstance(use, dict):
                continue
            target = use.get("skill")
            if not isinstance(target, str):
                continue
            if target in seen:
                errors.append("%s: uses duplicates %r" % (skill_id, target))
            seen.add(target)
            if target == skill_id:
                errors.append("%s: cannot optionally use itself" % skill_id)
            elif target not in skills:
                errors.append("%s: uses unregistered skill %r" % (skill_id, target))
            elif public and skills[target].get("distribution", "public") == "internal":
                errors.append("%s: a publicly distributed skill cannot use the internal skill %r"
                              % (skill_id, target))
            if target in required:
                errors.append("%s: %r cannot appear in both requires and uses" % (skill_id, target))
    return errors


def optional_use_body_errors(skill_id: str, directory: Path, entry: dict[str, Any]) -> list[str]:
    """Keep each optional trigger and fallback observable in the consuming skill."""
    uses = entry.get("uses", [])
    if not isinstance(uses, list) or not uses:
        return []
    body = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in sorted(directory.rglob("*"))
        if not ignored_path(path) and path.is_file() and path.suffix.lower() in {".md", ".yaml", ".yml"}
    )
    errors: list[str] = []
    for use in uses:
        if not isinstance(use, dict):
            continue
        for key in ("skill", "when", "fallback"):
            value = use.get(key)
            if isinstance(value, str) and value not in body:
                errors.append("%s: uses %r but its %s %r is absent from the skill body"
                              % (skill_id, use.get("skill"), key, value))
    return errors


def routing_digest_body(workflows: dict[str, Any]) -> str:
    """The routing view an installed orchestrator gets instead of the manifest."""
    lines: list[str] = []
    for workflow_id, entry in workflows.items():
        if not isinstance(entry, dict) or entry.get("status") != "active":
            continue
        lines.append("%s:" % workflow_id)
        lines.append("  entry_skill: %s" % entry.get("entry_skill"))
        for key in ("stages", "planning_stages", "renderers", "current_tools", "delegates"):
            route = entry.get(key)
            if route:
                lines.append("  %s: [%s]" % (key, ", ".join(route)))
        if entry.get("scope"):
            lines.append("  scope: %s" % entry["scope"])
        if entry.get("optional_next"):
            lines.append("  optional_next: [%s]" % ", ".join(entry["optional_next"]))
    return "\n".join(lines)


def routing_digest_errors(workflows: dict[str, Any]) -> list[str]:
    """The digest is derived; drift between it and the manifest is an error."""
    if not ROUTING_DIGEST.is_file():
        return ["Missing routing digest %s" % ROUTING_DIGEST.relative_to(REPO_ROOT)]
    block = re.search(r"(?ms)^```yaml\n(.*?)^```", ROUTING_DIGEST.read_text(encoding="utf-8-sig"))
    if not block:
        return ["routing digest is missing its generated ```yaml block"]
    if block.group(1).strip("\n") != routing_digest_body(workflows):
        return ["routing digest is stale; regenerate it from skill-manifest.yaml"]
    return []


def human_interaction_digest_body(skills: dict[str, Any]) -> str:
    lines: list[str] = []
    for skill_id, entry in skills.items():
        if not isinstance(entry, dict):
            continue
        interaction = entry.get("human_interaction")
        if not isinstance(interaction, dict):
            continue
        lines.append("%s:" % skill_id)
        for mode in entry.get("execution_modes", []):
            lines.append("  %s: %s" % (mode, interaction.get(mode)))
    return "\n".join(lines)


def human_interaction_digest_errors(skills: dict[str, Any]) -> list[str]:
    if not HUMAN_INTERACTION_DIGEST.is_file():
        return ["Missing human interaction digest %s" % HUMAN_INTERACTION_DIGEST.relative_to(REPO_ROOT)]
    block = re.search(
        r"(?ms)^```yaml\n(.*?)^```",
        HUMAN_INTERACTION_DIGEST.read_text(encoding="utf-8-sig"),
    )
    if not block:
        return ["human interaction digest is missing its generated ```yaml block"]
    if block.group(1).strip("\n") != human_interaction_digest_body(skills):
        return ["human interaction digest is stale; regenerate it from skill-manifest.yaml"]
    return []


def skills_sh_errors(skills: dict[str, Any]) -> list[str]:
    path = REPO_ROOT / "skills.sh.json"
    if not path.is_file():
        return ["Missing skills.sh.json repository page configuration"]
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return ["skills.sh.json: invalid JSON (%s)" % exc]

    errors: list[str] = []
    if data.get("$schema") != SKILLS_SH_SCHEMA_URL:
        errors.append("skills.sh.json: $schema must be %s" % SKILLS_SH_SCHEMA_URL)
    if data.get("notGrouped") not in {"top", "bottom"}:
        errors.append("skills.sh.json: notGrouped must be top or bottom")

    groupings = data.get("groupings")
    if not isinstance(groupings, list) or not groupings:
        return errors + ["skills.sh.json: groupings must be a non-empty list"]
    if len(groupings) > 50:
        errors.append("skills.sh.json: only the first 50 groups are used")

    listed: list[str] = []
    for index, group in enumerate(groupings):
        if not isinstance(group, dict):
            errors.append("skills.sh.json: grouping %d must be a mapping" % index)
            continue
        title = group.get("title")
        if not isinstance(title, str) or not title.strip():
            errors.append("skills.sh.json: grouping %d requires a title" % index)
        members = group.get("skills")
        if not isinstance(members, list) or not members:
            errors.append("skills.sh.json: group %r requires a non-empty skills list" % title)
            continue
        if len(members) > 500:
            errors.append("skills.sh.json: only the first 500 skills of group %r are used" % title)
        listed.extend(members)

    internal = {
        skill_id
        for skill_id, entry in skills.items()
        if isinstance(entry, dict) and entry.get("distribution") == "internal"
    }
    duplicates = sorted({skill_id for skill_id in listed if listed.count(skill_id) > 1})
    if duplicates:
        errors.append("skills.sh.json groups duplicate skills: %s" % ", ".join(duplicates))
    listed_set = set(listed)
    for label, difference in (
        ("omits public skills", sorted(set(skills) - internal - listed_set)),
        ("lists unknown skills", sorted(listed_set - set(skills))),
        ("lists internal skills", sorted(listed_set & internal)),
    ):
        if difference:
            errors.append("skills.sh.json %s: %s" % (label, ", ".join(difference)))
    return errors


def anti_pattern_errors(skills: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    research_skills = {
        "q-research-workflow",
        "q-research-scope",
        "q-research-investigate",
        "q-research-synthesize",
    }
    required = {
        skill_id
        for skill_id, entry in skills.items()
        if isinstance(entry, dict)
        and (entry.get("kind") in {"orchestrator", "quality"} or skill_id in research_skills)
    }
    header = "| # | Anti-pattern | How it shows up | Correct behavior |"
    separator = "|---|---|---|---|"
    for skill_id in sorted(required):
        entry = skills.get(skill_id, {})
        path = SKILLS_ROOT / str(entry.get("path", "")) / "SKILL.md"
        text = path.read_text(encoding="utf-8-sig")
        section = re.search(r"(?ms)^## Anti-patterns\s*\n(.*?)(?=^## |\Z)", text)
        if not section:
            errors.append("%s: missing exact '## Anti-patterns' section" % skill_id)
            continue
        lines = [line.strip() for line in section.group(1).splitlines() if line.strip()]
        if header not in lines:
            errors.append("%s: anti-pattern table has the wrong header" % skill_id)
        if separator not in lines:
            errors.append("%s: anti-pattern table has the wrong separator" % skill_id)
        rows = [
            line for line in lines
            if line.startswith("|") and line not in {header, separator}
        ]
        if not 1 <= len(rows) <= 7:
            errors.append("%s: anti-pattern table requires 1-7 rows, got %d" % (skill_id, len(rows)))
        for row in rows:
            if row.count("|") != 5:
                errors.append("%s: anti-pattern row must have four columns: %s" % (skill_id, row))
    return errors


def stray_file_errors() -> list[str]:
    return [
        "%s: Windows alternate-data-stream artifact must not ship inside a skill" % path.relative_to(REPO_ROOT)
        for path in sorted(SKILLS_ROOT.rglob("*"))
        if not ignored_path(path) and path.is_file() and path.name.endswith(":Zone.Identifier")
    ]


def mermaid_runtime_errors(skills: dict[str, Any]) -> list[str]:
    entry = skills.get("q-tool-mermaid")
    if not isinstance(entry, dict) or entry.get("status") != "active":
        return []
    directory = SKILLS_ROOT / str(entry.get("path", ""))
    runtime = directory / "runtime"
    required = [
        runtime / "package.json",
        runtime / "package-lock.json",
        runtime / "mermaid.mjs",
        directory / "tests" / "run-tests.mjs",
    ]
    errors = ["q-tool-mermaid: missing runtime file %s" % path.relative_to(REPO_ROOT)
              for path in required if not path.is_file()]
    node = shutil.which("node")
    if node and (runtime / "mermaid.mjs").is_file():
        run = subprocess.run(
            [node, str(runtime / "mermaid.mjs"), "--help"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            timeout=20,
            check=False,
        )
        if run.returncode != 0 or "q-tool-mermaid local runtime" not in run.stdout:
            errors.append("q-tool-mermaid: runtime --help smoke failed: %s"
                          % (run.stderr.strip() or run.stdout.strip() or run.returncode))
    return errors


def artifact_semantics(data: Any, active: set[str]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    if not isinstance(data, dict):
        return ["artifact index must be a mapping"]
    for item in data.get("artifacts", []):
        if not isinstance(item, dict):
            continue
        artifact_id = item.get("artifact_id")
        if artifact_id in seen:
            errors.append("duplicate artifact_id %r" % artifact_id)
        if isinstance(artifact_id, str):
            seen.add(artifact_id)
        if item.get("owner_skill") not in active:
            errors.append("unknown owner_skill %r" % item.get("owner_skill"))
        if item.get("creation_mode") == "derived" and item.get("semantic_authority") != "none":
            errors.append("derived artifact %r must have semantic_authority none" % artifact_id)
        if item.get("creation_mode") == "derived":
            provenance = item.get("provenance")
            if not isinstance(provenance, dict):
                errors.append("derived artifact %r requires generation provenance" % artifact_id)
            elif provenance.get("generator_skill") not in active:
                errors.append("derived artifact %r has unknown provenance generator_skill %r"
                              % (artifact_id, provenance.get("generator_skill")))
    return errors


def stage_semantics(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return ["stage result must be a mapping"]
    stage = data.get("stage_result", {})
    orchestration = data.get("orchestration", {})
    errors: list[str] = []
    if isinstance(stage, dict) and isinstance(orchestration, dict) and stage.get("mode") == "standalone":
        if orchestration.get("global_state_updated") is not False:
            errors.append("standalone result cannot update global state")
        if orchestration.get("reconciliation_required") is not True:
            errors.append("standalone result must require reconciliation")
    return errors


def workflow_state_semantics(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return ["workflow state must be a mapping"]
    errors: list[str] = []
    downstream = {
        "q-plan-domain-model",
        "q-plan-architecture",
        "q-plan-features",
        "q-plan-backlog",
    }
    stage_status = data.get("stage_status", {})
    foundation_completed = (
        isinstance(stage_status, dict)
        and stage_status.get("q-plan-tech-foundation") == "completed"
    )
    if (data.get("current_stage") in downstream or foundation_completed) and not data.get("technical_foundation_ref"):
        errors.append("downstream workflow state requires technical_foundation_ref")
    return errors


def report_source_semantics(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return ["report source must be a mapping"]

    errors: list[str] = []
    report = data.get("report", {})
    snapshot = data.get("source_snapshot", {})
    sources = snapshot.get("sources", []) if isinstance(snapshot, dict) else []
    known: dict[str, dict[str, Any]] = {}

    for source in sources if isinstance(sources, list) else []:
        if not isinstance(source, dict):
            continue
        artifact_id = source.get("artifact_id")
        if isinstance(artifact_id, str):
            if artifact_id in known:
                errors.append("duplicate report source artifact_id %r" % artifact_id)
            known[artifact_id] = source

    if isinstance(report, dict) and report.get("lifecycle") == "Baselined":
        if not isinstance(snapshot, dict) or snapshot.get("status") != "approved":
            errors.append("a Baselined report requires an approved source snapshot")
        if not isinstance(snapshot, dict) or not snapshot.get("approval_ref"):
            errors.append("a Baselined report requires a source snapshot approval_ref")
        if not data.get("approvals"):
            errors.append("a Baselined report requires semantic approval evidence")
    if isinstance(snapshot, dict) and snapshot.get("status") == "approved" and not snapshot.get("approved_at"):
        errors.append("an approved source snapshot requires approved_at")

    semantic_kinds = {"fact", "metric", "estimate", "interpretation", "recommendation", "projection"}
    section_ids: set[str] = set()
    block_ids: set[str] = set()
    sections = data.get("sections", [])
    for section in sections if isinstance(sections, list) else []:
        if not isinstance(section, dict):
            continue
        section_id = section.get("section_id")
        if isinstance(section_id, str):
            if section_id in section_ids:
                errors.append("duplicate report section_id %r" % section_id)
            section_ids.add(section_id)
        blocks = section.get("blocks", [])
        for block in blocks if isinstance(blocks, list) else []:
            if not isinstance(block, dict):
                continue
            block_id = block.get("block_id")
            if isinstance(block_id, str):
                if block_id in block_ids:
                    errors.append("duplicate report block_id %r" % block_id)
                block_ids.add(block_id)
            refs = block.get("source_refs", [])
            refs = refs if isinstance(refs, list) else []
            for ref in refs:
                if ref not in known:
                    errors.append("report block %r references unknown source %r" % (block_id, ref))
            if block.get("kind") in semantic_kinds:
                if not refs:
                    errors.append("report block %r requires source_refs" % block_id)
                    continue
                eligible = False
                for ref in refs:
                    source = known.get(ref, {})
                    lifecycle = source.get("lifecycle")
                    authority = source.get("semantic_authority")
                    approved_working = lifecycle == "Working" and bool(source.get("reporting_approval_ref"))
                    if authority in {"canonical", "supporting"} and (
                        lifecycle in {"Baselined", "Released"} or approved_working
                    ):
                        eligible = True
                if not eligible:
                    errors.append("report block %r has no eligible authoritative source" % block_id)

    channels = data.get("channels_requested", [])
    if isinstance(channels, list) and len(channels) != len(set(channels)):
        errors.append("report channels_requested contains duplicates")
    return errors


def research_brief_semantics(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return ["research brief must be a mapping"]
    errors: list[str] = []
    brief = data.get("brief", {})
    if isinstance(brief, dict) and brief.get("status") == "authorized" and not brief.get("approval_ref"):
        errors.append("an authorized research brief requires approval_ref")
    if isinstance(brief, dict) and brief.get("status") != "authorized":
        errors.append("a runnable research brief must be authorized")

    questions = data.get("questions", [])
    known: set[str] = set()
    question_ids: list[str] = []
    for question in questions if isinstance(questions, list) else []:
        if not isinstance(question, dict):
            continue
        question_id = question.get("question_id")
        if isinstance(question_id, str):
            question_ids.append(question_id)
            known.add(question_id)
        radar = question.get("radar", {})
        if isinstance(radar, dict):
            keys = ("researchable", "anchored", "decision_linked", "adds_evidence", "relevant")
            scores = [radar.get(key) for key in keys]
            if all(isinstance(score, (int, float)) and not isinstance(score, bool) for score in scores):
                average = sum(scores) / len(scores)
                if not isinstance(radar.get("average"), (int, float)) or abs(radar["average"] - average) > 0.01:
                    errors.append("question %r has an inconsistent RADAR average" % question_id)
                expected = average >= 3.0 and min(scores) >= 2
                if radar.get("passes") is not expected:
                    errors.append("question %r has an inconsistent RADAR pass result" % question_id)
    duplicates = sorted({item for item in question_ids if question_ids.count(item) > 1})
    if duplicates:
        errors.append("duplicate research question IDs: %s" % ", ".join(duplicates))

    for question in questions if isinstance(questions, list) else []:
        if not isinstance(question, dict):
            continue
        parent = question.get("parent_question_ref")
        if parent is not None and parent not in known:
            errors.append("question %r has unknown parent %r" % (question.get("question_id"), parent))
    for item in data.get("search_plan", []) if isinstance(data.get("search_plan"), list) else []:
        if isinstance(item, dict) and item.get("question_ref") not in known:
            errors.append("search plan references unknown question %r" % item.get("question_ref"))
    return errors


def cited_findings_semantics(data: Any, known_questions: set[str] | None = None) -> list[str]:
    if not isinstance(data, dict):
        return ["cited findings register must be a mapping"]
    errors: list[str] = []
    register = data.get("register", {})
    if isinstance(register, dict):
        scope_ref = register.get("scope_ref", {})
        if register.get("research_type") == "engagement":
            if not isinstance(scope_ref, dict) or scope_ref.get("reference_type") != "research-brief":
                errors.append("engagement cited findings require a research-brief scope_ref")
            if not isinstance(scope_ref, dict) or not isinstance(scope_ref.get("version"), str) or not scope_ref.get("version", "").strip():
                errors.append("engagement cited findings require an exact research-brief version")
        if isinstance(scope_ref, dict) and scope_ref.get("reference_type") == "project-artifact":
            if not isinstance(scope_ref.get("version"), str) or not scope_ref.get("version", "").strip():
                errors.append("project-artifact scope_ref requires an exact version")
    sources: dict[str, dict[str, Any]] = {}
    source_ids: list[str] = []
    for source in data.get("sources", []) if isinstance(data.get("sources"), list) else []:
        if not isinstance(source, dict):
            continue
        source_id = source.get("source_id")
        if isinstance(source_id, str):
            source_ids.append(source_id)
            sources.setdefault(source_id, source)
    duplicates = sorted({item for item in source_ids if source_ids.count(item) > 1})
    if duplicates:
        errors.append("duplicate cited source IDs: %s" % ", ".join(duplicates))

    search_ids: list[str] = []
    for search in data.get("search_log", []) if isinstance(data.get("search_log"), list) else []:
        if not isinstance(search, dict):
            continue
        search_id = search.get("search_id")
        if isinstance(search_id, str):
            search_ids.append(search_id)
        if known_questions is not None and search.get("question_ref") not in known_questions:
            errors.append("search %r references unknown question %r"
                          % (search_id, search.get("question_ref")))
    duplicates = sorted({item for item in search_ids if search_ids.count(item) > 1})
    if duplicates:
        errors.append("duplicate cited search IDs: %s" % ", ".join(duplicates))

    finding_ids: list[str] = []
    for finding in data.get("findings", []) if isinstance(data.get("findings"), list) else []:
        if not isinstance(finding, dict):
            continue
        finding_id = finding.get("finding_id")
        if isinstance(finding_id, str):
            finding_ids.append(finding_id)
        if known_questions is not None and finding.get("question_ref") not in known_questions:
            errors.append("finding %r references unknown question %r"
                          % (finding_id, finding.get("question_ref")))
        refs = finding.get("evidence_refs", [])
        refs = refs if isinstance(refs, list) else []
        supports = []
        groups: set[str] = set()
        for ref in refs:
            if not isinstance(ref, dict):
                continue
            source_ref = ref.get("source_ref")
            source = sources.get(source_ref)
            if source is None:
                errors.append("finding %r references unknown source %r" % (finding_id, source_ref))
            elif ref.get("relation") == "supports":
                supports.append(ref)
                group = source.get("independence_group")
                if isinstance(group, str):
                    groups.add(group)
            if not isinstance(ref.get("locator"), str) or not ref.get("locator", "").strip():
                errors.append("finding %r has evidence without a locator" % finding_id)
        if finding.get("finding_status") == "supported" and not supports:
            errors.append("supported finding %r requires a supports relation" % finding_id)
        if finding.get("corroboration") == "multiple-independent" and len(groups) < 2:
            errors.append("multiple-independent finding %r requires two independence groups" % finding_id)
    duplicates = sorted({item for item in finding_ids if finding_ids.count(item) > 1})
    if duplicates:
        errors.append("duplicate cited finding IDs: %s" % ", ".join(duplicates))

    def misplaced_not_found(value: Any, key: str | None = None) -> bool:
        if isinstance(value, dict):
            return any(misplaced_not_found(item, child_key) for child_key, item in value.items())
        if isinstance(value, list):
            return any(misplaced_not_found(item, key) for item in value)
        return value == "not-found" and key != "source_verification"

    if misplaced_not_found(data):
        errors.append("not-found is valid only as source_verification")
    return errors


def research_synthesis_semantics(
    data: Any,
    known_findings: set[str],
    known_questions: set[str],
) -> list[str]:
    if not isinstance(data, dict):
        return ["research synthesis must be a mapping"]
    errors: list[str] = []
    answer_refs: list[str] = []
    reference_fields = {
        "supporting_finding_refs",
        "contradicting_finding_refs",
        "finding_refs",
        "adverse_finding_refs",
    }

    def inspect(value: Any, key: str | None = None) -> None:
        if isinstance(value, dict):
            for child_key, item in value.items():
                inspect(item, child_key)
        elif isinstance(value, list):
            if key in reference_fields:
                for ref in value:
                    if ref not in known_findings:
                        errors.append("research synthesis references unknown finding %r" % ref)
            else:
                for item in value:
                    inspect(item, key)

    answers = data.get("answers", [])
    for answer in answers if isinstance(answers, list) else []:
        if isinstance(answer, dict) and isinstance(answer.get("question_ref"), str):
            answer_refs.append(answer["question_ref"])
            if answer["question_ref"] not in known_questions:
                errors.append("research synthesis answer references unknown question %r"
                              % answer["question_ref"])
    duplicates = sorted({item for item in answer_refs if answer_refs.count(item) > 1})
    if duplicates:
        errors.append("duplicate research synthesis answers: %s" % ", ".join(duplicates))
    for collection, id_key in (("themes", "theme_id"), ("debates", "debate_id"), ("gaps", "gap_id")):
        identifiers = [
            item.get(id_key)
            for item in data.get(collection, [])
            if isinstance(item, dict) and isinstance(item.get(id_key), str)
        ] if isinstance(data.get(collection), list) else []
        duplicates = sorted({item for item in identifiers if identifiers.count(item) > 1})
        if duplicates:
            errors.append("duplicate research synthesis %s IDs: %s"
                          % (collection, ", ".join(duplicates)))
    for gap in data.get("gaps", []) if isinstance(data.get("gaps"), list) else []:
        if isinstance(gap, dict) and gap.get("question_ref") not in known_questions:
            errors.append("research synthesis gap references unknown question %r"
                          % gap.get("question_ref"))
    inspect(data)
    return errors


def research_baseline_semantics(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return ["research baseline must be a mapping"]
    errors: list[str] = []
    baseline = data.get("baseline", {})
    if not isinstance(baseline, dict):
        return errors
    for key in ("version", "as_of", "approval_ref"):
        if not isinstance(baseline.get(key), str) or not baseline.get(key, "").strip():
            errors.append("research baseline requires non-empty %s" % key)
    for key in ("brief_ref", "findings_ref", "synthesis_ref"):
        ref = baseline.get(key, {})
        if not isinstance(ref, dict) or not isinstance(ref.get("version"), str) or not ref.get("version", "").strip():
            errors.append("research baseline %s requires an exact version" % key)
    return errors


def ideation_baseline_semantics(data: Any) -> list[str]:
    """An approved snapshot must stay traceable, gated, and non-self-adopting."""

    if not isinstance(data, dict):
        return ["ideation baseline must be a mapping"]

    errors: list[str] = []
    baseline = data.get("baseline", {})
    if isinstance(baseline, dict):
        for key in ("version", "as_of"):
            if not isinstance(baseline.get(key), str) or not baseline.get(key, "").strip():
                errors.append("ideation baseline requires non-empty %s" % key)
    register = data.get("source_register", {})
    if not isinstance(register, dict) or not isinstance(register.get("version"), str) or not register.get("version", "").strip():
        errors.append("ideation baseline source_register requires an exact version")

    approval = data.get("approval", {})
    for key in ("approved_by", "approval_ref", "approved_at"):
        value = approval.get(key) if isinstance(approval, dict) else None
        if not isinstance(value, str) or not value.strip():
            errors.append("an approved ideation snapshot requires a non-empty %s" % key)

    gates = data.get("gates_applied", [])
    gates = gates if isinstance(gates, list) else []
    blocking = {"failed", "redesign-required", "review-required"}
    gate_results = {
        gate.get("gate_id"): gate.get("result")
        for gate in gates
        if isinstance(gate, dict)
    }

    requested: set[str] = set()
    known_candidates = {
        item.get("candidate_ref")
        for item in data.get("candidate_dispositions", [])
        if isinstance(item, dict)
    }
    for request in data.get("evidence_requests", []) if isinstance(data.get("evidence_requests"), list) else []:
        if not isinstance(request, dict):
            continue
        refs = request.get("candidate_refs", [])
        refs = refs if isinstance(refs, list) else []
        requested.update(refs)
        for ref in refs:
            if ref not in known_candidates:
                errors.append("evidence request %r references unknown candidate %r"
                              % (request.get("request_id"), ref))
        route = request.get("recommended_route")
        if not isinstance(route, str) or not route.startswith("q-") or route == "q-ideation-session":
            errors.append("evidence request %r must route to another registered skill"
                          % request.get("request_id"))

    seen: list[str] = []
    for item in data.get("candidate_dispositions", []) if isinstance(data.get("candidate_dispositions"), list) else []:
        if not isinstance(item, dict):
            continue
        candidate_ref = item.get("candidate_ref")
        if isinstance(candidate_ref, str):
            seen.append(candidate_ref)
        disposition = item.get("disposition")
        route = item.get("recommended_route")
        if not isinstance(item.get("rationale"), str) or not item.get("rationale", "").strip():
            errors.append("candidate %r has a disposition without a rationale" % candidate_ref)
        for gate_ref in item.get("gate_refs", []) if isinstance(item.get("gate_refs"), list) else []:
            if gate_ref not in gate_results:
                errors.append("candidate %r references unknown gate %r" % (candidate_ref, gate_ref))
            elif disposition == "advance" and gate_results.get(gate_ref) in blocking:
                errors.append("candidate %r advances with the unresolved gate %r" % (candidate_ref, gate_ref))
        if disposition == "advance" and (
            not isinstance(route, dict) or not route.get("skill") or not route.get("intended_use")
        ):
            errors.append("advancing candidate %r requires an owner route" % candidate_ref)
        if disposition in {"evidence-needed", "prototype-needed"} and candidate_ref not in requested:
            errors.append("candidate %r needs evidence without a routed request" % candidate_ref)
        if isinstance(route, dict) and route.get("skill") == "q-ideation-session":
            errors.append("candidate %r cannot be routed back to the ideation session" % candidate_ref)
    duplicates = sorted({item for item in seen if seen.count(item) > 1})
    if duplicates:
        errors.append("duplicate candidate dispositions: %s" % ", ".join(duplicates))
    return errors


def database_analysis_semantics(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return ["database analysis must be a mapping"]
    analysis = data.get("database_analysis", {})
    if not isinstance(analysis, dict):
        return ["database_analysis must be a mapping"]

    errors: list[str] = []
    request_id = analysis.get("request_id")
    if not isinstance(request_id, str) or not request_id.strip():
        errors.append("database analysis requires a non-empty request_id")
    next_action = analysis.get("next_recommended_action")
    if not isinstance(next_action, str) or not next_action.strip():
        errors.append("database analysis requires one next_recommended_action")

    profile = analysis.get("database_profile", {})
    if analysis.get("task") in {"physical-design", "migration-design"}:
        for key in ("model_family", "engine", "version"):
            if not isinstance(profile, dict) or not isinstance(profile.get(key), str) or not profile.get(key, "").strip():
                errors.append("%s requires a confirmed database profile %s" % (analysis.get("task"), key))

    finding_ids: list[str] = []
    for finding in analysis.get("findings", []) if isinstance(analysis.get("findings"), list) else []:
        if isinstance(finding, dict) and isinstance(finding.get("id"), str):
            finding_ids.append(finding["id"])
        if isinstance(finding, dict) and finding.get("owner_route") == "q-tool-database-schema":
            errors.append("database findings must route to an owning skill, not q-tool-database-schema")
    duplicates = sorted({item for item in finding_ids if finding_ids.count(item) > 1})
    if duplicates:
        errors.append("duplicate database finding IDs: %s" % ", ".join(duplicates))

    gaps = analysis.get("coverage_gaps", [])
    if analysis.get("outcome") == "completed" and isinstance(gaps, list) and gaps:
        errors.append("a completed database analysis cannot retain coverage gaps")
    if analysis.get("outcome") == "completed":
        sources = analysis.get("source_refs", [])
        authoritative = [
            source for source in sources if isinstance(source, dict)
            and source.get("authority") in {"canonical", "observed", "user-supplied"}
        ] if isinstance(sources, list) else []
        if not authoritative:
            errors.append("a completed database analysis requires authoritative source evidence")
        facts = analysis.get("observed_facts", [])
        if not isinstance(facts, list) or not facts:
            errors.append("a completed database analysis requires observed facts")

        candidate = analysis.get("candidate_design", {})
        task = analysis.get("task")
        family = profile.get("model_family") if isinstance(profile, dict) else None
        if task == "physical-design" and family == "relational" and (
            not isinstance(candidate, dict) or not candidate.get("relations")
        ):
            errors.append("a completed relational physical design requires candidate relations")
        if task == "physical-design" and family == "document" and (
            not isinstance(candidate, dict) or not candidate.get("documents")
        ):
            errors.append("a completed document physical design requires candidate documents")
        if task == "migration-design" and (
            not isinstance(candidate, dict) or not candidate.get("migration_steps")
        ):
            errors.append("a completed migration design requires migration steps")

    handoff = analysis.get("verification_handoff", {})
    if isinstance(handoff, dict) and handoff.get("recommended_commands") and not handoff.get("execution_owner"):
        errors.append("recommended database commands require an execution_owner")
    return errors


def fixture_pair(
    schema_path: Path,
    valid_path: Path,
    invalid_path: Path,
    semantic,
    active: set[str],
    min_invalid_errors: int = 1,
) -> list[str]:
    schema = load(schema_path)
    valid = load(valid_path)
    invalid = load(invalid_path)
    valid_errors = schema_errors(valid, schema)
    invalid_errors = schema_errors(invalid, schema)
    if semantic is artifact_semantics:
        valid_errors.extend(semantic(valid, active))
        invalid_errors.extend(semantic(invalid, active))
    elif semantic:
        valid_errors.extend(semantic(valid))
        invalid_errors.extend(semantic(invalid))
    errors: list[str] = []
    if valid_errors:
        errors.append("%s rejected: %s" % (valid_path.name, "; ".join(valid_errors)))
    if len(invalid_errors) < min_invalid_errors:
        errors.append("%s produced %d error(s); expected at least %d"
                      % (invalid_path.name, len(invalid_errors), min_invalid_errors))
    return errors


def manifest_use_fixture_errors(schema: dict[str, Any], fixtures: Path) -> list[str]:
    valid_path = fixtures / "skill-manifest-uses.valid.yaml"
    invalid_path = fixtures / "skill-manifest-uses.invalid.yaml"
    valid = load(valid_path)
    invalid = load(invalid_path)
    valid_errors = schema_errors(valid, schema)
    invalid_errors = schema_errors(invalid, schema)
    valid_skills = valid.get("skills", {}) if isinstance(valid, dict) else {}
    invalid_skills = invalid.get("skills", {}) if isinstance(invalid, dict) else {}
    valid_errors.extend(optional_use_semantics(valid_skills))
    invalid_errors.extend(optional_use_semantics(invalid_skills))
    errors: list[str] = []
    if valid_errors:
        errors.append("%s rejected: %s" % (valid_path.name, "; ".join(valid_errors)))
    if len(invalid_errors) < 4:
        errors.append("%s produced %d error(s); expected at least 4"
                      % (invalid_path.name, len(invalid_errors)))
    return errors


def acceptance_errors() -> tuple[list[str], int]:
    checks = {
        "S-01": [
            ("proposal/q-proposal-workflow/SKILL.md", "accepted_without_development"),
            ("proposal/q-proposal-workflow/SKILL.md", "future/manual execution"),
        ],
        "S-02": [
            ("proposal/q-proposal-workflow/SKILL.md", "proposal object IDs"),
            ("proposal/q-proposal-discovery/SKILL.md", "assumptions"),
        ],
        "S-03": [
            ("plan/q-plan-product-core/SKILL.md", "started without a proposal"),
        ],
        "S-04": [
            ("plan/q-plan-backlog/SKILL.md", "initial-generation"),
            ("plan/q-plan-backlog/SKILL.md", "Do not require all stories"),
        ],
        "S-05": [
            ("plan/q-plan-backlog/SKILL.md", "replan-and-synchronize"),
            ("plan/q-plan-backlog/SKILL.md", "required approval"),
        ],
        "S-06": [
            ("delivery/q-delivery-workflow/SKILL.md", "Skip a grill"),
            ("delivery/q-delivery-workflow/SKILL.md", "Enable `q-code-tdd` only"),
        ],
        "S-07": [
            ("code/q-code-tickets/SKILL.md", "Tickets are durable"),
            ("code/q-code-tickets/SKILL.md", "preserve backlog, requirement, decision, and plan IDs"),
        ],
        "S-08": [
            ("code/q-code-implement/SKILL.md", "internal plans, scratchpads, and delegation messages transient"),
            ("code/q-code-implement/SKILL.md", "Update only the original durable record"),
        ],
        "S-09": [
            ("proposal/q-proposal-workflow/SKILL.md", "Return scope, price, schedule, commitment, or source errors"),
            ("proposal/q-proposal-workflow/SKILL.md", "visual, layout, accessibility"),
        ],
        "S-10": [
            ("delivery/q-delivery-workflow/SKILL.md", "accepted commercial scope"),
            ("delivery/q-delivery-workflow/SKILL.md", "Keep the accepted release immutable"),
        ],
        "S-11": [
            ("review/q-review-code/SKILL.md", "sequential passes"),
            ("review/q-review-code/SKILL.md", "Keep results separate"),
        ],
        "S-12": [
            ("plan/q-plan-tech-foundation/SKILL.md", "Never block solely because the selected stack is not T3"),
            ("core/q-core-contract/SKILL.md", "profile-driven"),
        ],
        "S-13": [
            ("delivery/q-delivery-workflow/SKILL.md", "On resume"),
            ("delivery/q-delivery-workflow/SKILL.md", "Do not reopen closed decisions"),
        ],
        "S-14": [
            ("core/q-core-contract/SKILL.md", "Domain or architecture Mermaid source"),
            ("core/q-core-contract/SKILL.md", "SVG, PNG, or PDF rendered from Mermaid"),
        ],
        "S-15": [
            ("report/q-report-workflow/SKILL.md", "Reporting is optional"),
            ("report/q-report-source/SKILL.md", "approved as a reporting snapshot"),
            ("proposal/q-proposal-workflow/SKILL.md", "Reporting is optional"),
        ],
        "S-16": [
            ("core/q-core-contract/SKILL.md", "must not commit, publish, message external systems"),
            ("skill-manifest.yaml", "approval_policy"),
        ],
        "S-17": [
            ("core/q-core-contract/SKILL.md", "reconciliation_required: true"),
            ("core/q-core-contract/SKILL.md", "global_state_updated: false"),
        ],
        "S-18": [
            ("code/q-code-explore/SKILL.md", "Return the summary in the conversation as transient context"),
            ("delivery/q-delivery-workflow/SKILL.md", "do not register it as an artifact"),
        ],
        "S-19": [
            ("review/q-review-docs/SKILL.md", "Return the diagnostic in the conversation as transient context"),
            ("review/q-review-docs/SKILL.md", "Record any later implemented documentation change through the owning workflow"),
            ("review/q-review-docs/SKILL.md", "stop and route the request to `q-maint-ai-workflow`"),
            ("delivery/q-delivery-workflow/SKILL.md", "`q-review-docs` is optional"),
            ("proposal/q-proposal-workflow/SKILL.md", "`q-review-docs` is optional"),
        ],
        "S-20": [
            ("core/q-core-contract/SKILL.md", "root orchestrator"),
            ("report/q-report-workflow/SKILL.md", "composite delta with `global_state_updated: false`"),
            ("delivery/q-delivery-workflow/SKILL.md", "Remain the global state writer"),
        ],
        "S-21": [
            ("report/q-report-source/SKILL.md", "single semantic source"),
            ("report/q-report-document/SKILL.md", "semantic_authority: none"),
            ("report/q-report-deck/SKILL.md", "semantic_authority: none"),
        ],
        "S-22": [
            ("report/q-report-document/SKILL.md", "Return semantic edits to `q-report-source`"),
            ("report/q-report-deck/SKILL.md", "Return semantic edits to `q-report-source`"),
            ("report/q-report-document/SKILL.md", "missing requested format"),
        ],
        "S-23": [
            ("plan/q-plan-tech-foundation/references/web-stack-recommendation.md", "TypeScript"),
            ("plan/q-plan-tech-foundation/references/web-stack-recommendation.md", "Next.js App Router"),
            ("plan/q-plan-tech-foundation/references/web-stack-recommendation.md", "tRPC"),
            ("plan/q-plan-tech-foundation/references/web-stack-recommendation.md", "Zod"),
            ("plan/q-plan-tech-foundation/references/web-stack-recommendation.md", "Zustand"),
            ("plan/q-plan-tech-foundation/references/web-stack-recommendation.md", "shadcn/ui"),
            ("plan/q-plan-tech-foundation/references/web-stack-recommendation.md", "React Hook Form"),
            ("plan/q-plan-tech-foundation/references/web-stack-recommendation.md", "Drizzle or Prisma"),
        ],
        "S-24": [
            ("plan/q-plan-tech-foundation/SKILL.md", "Preserve an existing stack"),
            ("plan/q-plan-tech-foundation/SKILL.md", "Evaluate an explicit user proposal"),
            ("plan/q-plan-tech-foundation/SKILL.md", "current primary sources"),
        ],
        "S-25": [
            ("core/q-core-contract/SKILL.md", "sole owner of the authored technical foundation"),
            ("delivery/q-delivery-workflow/SKILL.md", "technical_foundation_ref"),
            ("plan/q-plan-architecture/SKILL.md", "never edit their owned artifacts directly"),
        ],
        "S-26": [
            ("review/q-review-codebase/SKILL.md", "A recommended but unselected library is not"),
            ("review/q-review-codebase/SKILL.md", "generic and repository-grounded criteria"),
            ("review/q-review-codebase/SKILL.md", "do not issue a full stack-specific approval"),
        ],
        "S-27": [
            ("ask/q-ask-project/SKILL.md", "Ask only when the ambiguity would change"),
            ("ask/q-ask-project/SKILL.md", "Return the answer in the conversation as transient context"),
            ("ask/q-ask-project/SKILL.md", "Do not create a file"),
        ],
        "S-28": [
            ("ask/q-ask-analyze/SKILL.md", "Analyze every relevant dimension"),
            ("ask/q-ask-analyze/SKILL.md", "compatible with conditions"),
            ("ask/q-ask-analyze/SKILL.md", "do not start it unless the user separately authorizes"),
        ],
        "S-29": [
            ("research/q-research-workflow/SKILL.md", "For a direct root run"),
            ("research/q-research-workflow/SKILL.md", "`discovery-proposal`, `reporting`, and `close`"),
        ],
        "S-30": [
            ("research/q-research-workflow/SKILL.md", "Start none of them without an explicit user choice"),
            ("research/q-research-workflow/SKILL.md", "Research is optional consulting or engagement work"),
        ],
        "S-31": [
            ("research/q-research-workflow/SKILL.md", "composite delta with `global_state_updated: false`"),
            ("proposal/q-proposal-workflow/SKILL.md", "`adopt-as-proposal-input`"),
            ("proposal/q-proposal-workflow/SKILL.md", "`retain-as-independent`"),
        ],
        "S-32": [
            ("research/q-research-investigate/SKILL.md", "untrusted evidence"),
            ("research/q-research-investigate/SKILL.md", "Do not send client names"),
            ("research/q-research-investigate/SKILL.md", "planned-search-complete"),
        ],
        "S-33": [
            ("code/q-code-research/SKILL.md", "do not start `q-research-workflow`"),
            ("code/q-code-research/SKILL.md", "stage delta with `global_state_updated: false`"),
            ("core/q-core-contract/SKILL.md", "references/cited-findings.schema.yaml"),
        ],
        "S-34": [
            ("review/q-review-comments/SKILL.md", "Validating intention without code"),
            ("review/q-review-code/SKILL.md", "Silencing corroborating observations"),
        ],
        "S-35": [
            ("review/q-review-codebase/SKILL.md", "Reviewing only known issues"),
            ("review/q-review-codebase/SKILL.md", "Auditing against unadopted standards"),
            ("report/q-report-workflow/SKILL.md", "Rewriting upstream truth through reporting"),
        ],
        "S-36": [
            ("core/q-core-contract/SKILL.md", "This field describes cadence only"),
            ("core/q-core-contract/SKILL.md", "`approval_policy` remains authoritative"),
            ("core/q-core-contract/references/human-interaction.md", "The package validator rejects any drift"),
        ],
        "S-37": [
            ("review/q-review-skill/SKILL.md", "Keep the review read-only"),
            ("review/q-review-skill/SKILL.md", "positive trigger and one nearby negative trigger"),
            ("review/q-review-skill/SKILL.md", "heuristic with no approval authority"),
        ],
        "S-38": [
            ("maint/q-maint-skill-quality/SKILL.md", "structural validation sequence owned by `q-maint-ai-workflow`"),
            ("maint/q-maint-skill-quality/SKILL.md", "resolve every `blocker` and `high` finding"),
            ("maint/q-maint-ai-workflow/SKILL.md", "load `q-maint-skill-quality`"),
        ],
        "S-39": [
            ("tool/q-tool-mermaid/SKILL.md", "caller retains semantic ownership"),
            ("tool/q-tool-mermaid/SKILL.md", "semantic ambiguity"),
            ("core/q-core-contract/SKILL.md", "Diagram delegation"),
        ],
        "S-40": [
            ("tool/q-tool-mermaid/SKILL.md", "local runtime never installs dependencies"),
            ("tool/q-tool-mermaid/SKILL.md", "derived with `semantic_authority: none`"),
            ("review/q-review-docs/SKILL.md", "read-only validation"),
        ],
        "S-41": [
            ("tool/q-tool-database-schema/SKILL.md", "must not choose the stack"),
            ("tool/q-tool-database-schema/SKILL.md", "`performance-review` requires supplied evidence"),
            ("tool/q-tool-database-schema/SKILL.md", "must not replace it"),
            ("tool/q-tool-database-schema/SKILL.md", "Recommended commands are a handoff only"),
        ],
        "S-42": [
            ("plan/q-plan-domain-model/SKILL.md", "existing-database-schema-or-material-confirmed-profile-needs-physical-persistence-assistance"),
            ("plan/q-plan-domain-model/SKILL.md", "continue-with-persistence-neutral-domain-model-and-record-the-database-assistance-gap"),
            ("plan/q-plan-domain-model/SKILL.md", "A physical schema is not an exit criterion"),
        ],
        "S-43": [
            ("tool/q-tool-database-schema/references/document-model-review.md", "A document schema is a physical model"),
            ("tool/q-tool-database-schema/references/migration-strategies.md", "Classify rollback as"),
        ],
        "S-44": [
            ("core/q-core-contract/SKILL.md", "Structured ideation is optional"),
            ("core/q-core-contract/SKILL.md", "The adopting workflow owns the lifecycle transition"),
            ("ideation/q-ideation-session/SKILL.md", "Never browse, cite, or change the candidate pool from unauthorized research"),
            ("ideation/q-ideation-session/SKILL.md", "never writes `00-workflow-state.yaml`"),
        ],
        "S-45": [
            ("proposal/q-proposal-workflow/SKILL.md", "adopt-as-supporting-input"),
            ("delivery/q-delivery-workflow/SKILL.md", "never becomes a requirement, a business rule, an ADR, or a stack selection"),
            ("plan/q-plan-product-core/SKILL.md", "never copy a candidate into a requirement"),
            ("report/q-report-source/SKILL.md", "never as `fact`, `metric`, or accepted scope"),
            ("ideation/q-ideation-session/references/handoffs.md", "A recommended route is a suggestion"),
        ],
        "S-46": [
            ("ideation/q-ideation-session/references/evaluation-and-gates.md", "Gates are non-compensatory"),
            ("ideation/q-ideation-session/references/method-core.md", "never a consulted stakeholder"),
            ("ideation/q-ideation-session/references/responsible-ai.md", "no synthetic panel"),
        ],
    }
    errors: list[str] = []
    for scenario, requirements in checks.items():
        for relative, phrase in requirements:
            path = (REPO_ROOT / relative) if relative == "skill-manifest.yaml" else (SKILLS_ROOT / relative)
            text = path.read_text(encoding="utf-8-sig")
            if phrase not in text:
                errors.append("%s: missing acceptance evidence %r in %s" % (scenario, phrase, relative))
    return errors, len(checks)


def readme_planned_errors(planned: set[str]) -> list[str]:
    path = REPO_ROOT / "README.md"
    text = path.read_text(encoding="utf-8-sig")
    section = re.search(r"(?ms)^## Planned capabilities\s*(.*?)(?=^## |\Z)", text)
    if not section:
        return ["README.md is missing the Planned capabilities section"]

    listed = re.findall(r"(?m)^- `([a-z0-9-]+)`\s*$", section.group(1))
    errors: list[str] = []
    duplicates = sorted({skill_id for skill_id in listed if listed.count(skill_id) > 1})
    if duplicates:
        errors.append("README planned capabilities contain duplicates: %s" % ", ".join(duplicates))

    listed_set = set(listed)
    missing = sorted(planned - listed_set)
    stale = sorted(listed_set - planned)
    if missing:
        errors.append("README omits planned capabilities: %s" % ", ".join(missing))
    if stale:
        errors.append("README lists non-planned capabilities: %s" % ", ".join(stale))
    return errors


def package_doc_errors() -> list[str]:
    errors: list[str] = []
    required = ('AGENTS.md', 'CLAUDE.md', 'CHANGELOG.md', 'LICENSE')
    for relative in required:
        if not (REPO_ROOT / relative).is_file():
            errors.append('Missing package reference document: %s' % relative)

    claude = REPO_ROOT / 'CLAUDE.md'
    if claude.is_file() and claude.read_text(encoding='utf-8-sig').strip() != '@AGENTS.md':
        errors.append('CLAUDE.md must import AGENTS.md as the shared instruction source')

    agents = REPO_ROOT / 'AGENTS.md'
    if agents.is_file():
        text = agents.read_text(encoding='utf-8-sig')
        for phrase in ('$q-maint-ai-workflow', 'administrative housekeeping', 'CHANGELOG.md'):
            if phrase not in text:
                errors.append('AGENTS.md is missing maintenance pointer %r' % phrase)

    readme = REPO_ROOT / 'README.md'
    if readme.is_file():
        text = readme.read_text(encoding='utf-8-sig')
        for phrase in ('npx skills add', 'skills.sh'):
            if phrase not in text:
                errors.append('README.md is missing external installation guidance %r' % phrase)

    changelog = REPO_ROOT / 'CHANGELOG.md'
    if changelog.is_file() and '## [Unreleased]' not in changelog.read_text(encoding='utf-8-sig'):
        errors.append('CHANGELOG.md must contain an Unreleased section')

    license_path = REPO_ROOT / 'LICENSE'
    if license_path.is_file():
        text = license_path.read_text(encoding='utf-8-sig')
        for phrase in ('MIT License',):
            if phrase not in text:
                errors.append('LICENSE is missing required notice %r' % phrase)

    maintenance = SKILLS_ROOT / 'maint' / 'q-maint-ai-workflow' / 'SKILL.md'
    if maintenance.is_file():
        text = maintenance.read_text(encoding='utf-8-sig')
        for phrase in (
            'Act as the package housekeeper',
            'Run the philosophy and anti-pattern gate',
            'Do not return a project `stage_result`',
        ):
            if phrase not in text:
                errors.append('q-maint-ai-workflow is missing governance evidence %r' % phrase)

    installed = REPO_ROOT / '.agents' / 'skills' / 'q-maint-ai-workflow'
    canonical = SKILLS_ROOT / 'maint' / 'q-maint-ai-workflow'
    if not installed.exists():
        errors.append('q-maint-ai-workflow is not installed in .agents/skills')
    elif not installed.is_symlink():
        errors.append('q-maint-ai-workflow repo installation must link to its canonical package source')
    elif installed.resolve() != canonical.resolve():
        errors.append('q-maint-ai-workflow repo installation points to the wrong source')
    return errors


def run() -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        manifest = load(REPO_ROOT / "skill-manifest.yaml")
        schema = load(SKILLS_ROOT / "schemas" / "skill-manifest.schema.yaml")
    except Exception as exc:
        return {
            "status": "Failed",
            "errors": ["Cannot load manifest or schema: %s" % exc],
            "warnings": [],
            "checked_skills": 0,
            "checked_references": 0,
            "checked_artifacts": 0,
        }
    errors.extend(schema_errors(manifest, schema, "manifest"))
    skills = manifest.get("skills", {}) if isinstance(manifest, dict) else {}
    planned = manifest.get("planned_capabilities", {}) if isinstance(manifest, dict) else {}
    active = set(skills)
    workflows = manifest.get("workflows", {}) if isinstance(manifest, dict) else {}
    discovered = {
        p.parent.resolve()
        for p in SKILLS_ROOT.rglob("SKILL.md")
        if not ignored_path(p) and "_to_delete" not in p.parts
    }
    registered: set[Path] = set()
    checked_artifacts = 0

    if isinstance(workflows, dict):
        terminal_routes = {"close", "return-to-caller"}
        for workflow_id, workflow_entry in workflows.items():
            if not isinstance(workflow_entry, dict):
                errors.append("workflow %s must be a mapping" % workflow_id)
                continue
            entry_skill = workflow_entry.get("entry_skill")
            if workflow_entry.get("status") == "active":
                entry = skills.get(entry_skill) if isinstance(entry_skill, str) else None
                if not isinstance(entry, dict):
                    errors.append("active workflow %s has unknown entry_skill %r" % (workflow_id, entry_skill))
                elif entry.get("workflow") != workflow_id:
                    errors.append("workflow %s entry_skill %r has the wrong workflow owner" % (workflow_id, entry_skill))
                elif workflow_entry.get("scope") == "package-administration":
                    if entry.get("kind") != "tool":
                        errors.append("administrative workflow %s entry_skill %r must be a tool" % (workflow_id, entry_skill))
                elif entry.get("kind") != "orchestrator":
                    errors.append("workflow %s entry_skill %r is not an orchestrator" % (workflow_id, entry_skill))
            for route_key in ("stages", "planning_stages", "renderers", "current_tools"):
                route = workflow_entry.get(route_key, [])
                if not isinstance(route, list):
                    errors.append("workflow %s.%s must be a list" % (workflow_id, route_key))
                    continue
                for skill_id in route:
                    skill = skills.get(skill_id)
                    if not isinstance(skill, dict):
                        errors.append("workflow %s.%s references unknown skill %r" % (workflow_id, route_key, skill_id))
                    elif skill.get("workflow") != workflow_id:
                        errors.append("workflow %s.%s references cross-owned skill %r" % (workflow_id, route_key, skill_id))
            delegates = workflow_entry.get("delegates", [])
            if not isinstance(delegates, list):
                errors.append("workflow %s.delegates must be a list" % workflow_id)
            else:
                duplicates = sorted({target for target in delegates if delegates.count(target) > 1})
                if duplicates:
                    errors.append("workflow %s.delegates contains duplicates: %s"
                                  % (workflow_id, ", ".join(duplicates)))
                for target in delegates:
                    target_entry = workflows.get(target)
                    if target == workflow_id:
                        errors.append("workflow %s cannot delegate to itself" % workflow_id)
                    elif not isinstance(target_entry, dict) or target_entry.get("status") != "active":
                        errors.append("workflow %s.delegates references inactive or unknown workflow %r"
                                      % (workflow_id, target))
            optional_next = workflow_entry.get("optional_next", [])
            if not isinstance(optional_next, list):
                errors.append("workflow %s.optional_next must be a list" % workflow_id)
            else:
                for target in optional_next:
                    if target not in workflows and target not in terminal_routes:
                        errors.append("workflow %s.optional_next references unknown route %r" % (workflow_id, target))

    folders = {
        (SKILLS_ROOT / str(entry.get("path", ""))).resolve(): skill_id
        for skill_id, entry in skills.items()
        if isinstance(entry, dict)
    }

    errors.extend(optional_use_semantics(skills))

    for skill_id, entry in skills.items():
        if not isinstance(entry, dict):
            errors.append("%s: manifest entry must be a mapping" % skill_id)
            continue
        directory = (SKILLS_ROOT / str(entry.get("path", ""))).resolve()
        registered.add(directory)
        skill_file = directory / "SKILL.md"
        if not skill_file.is_file():
            errors.append("%s: missing SKILL.md" % skill_id)
            continue
        metadata, current = frontmatter(skill_file)
        errors.extend(current)
        if metadata and metadata.get("name") != skill_id:
            errors.append("%s: frontmatter name is %r" % (skill_id, metadata.get("name")))
        errors.extend(identity_errors(skill_id, directory, entry, metadata))
        errors.extend(distribution_errors(skill_id, entry, metadata))
        errors.extend(human_interaction_errors(skill_id, entry))
        errors.extend(reference_errors(skill_id, directory, entry, skills, folders))
        errors.extend(optional_use_body_errors(skill_id, directory, entry))
        if entry.get("invocable") is False:
            errors.extend(internal_skill_errors(directory, skill_id, entry))
        else:
            if "internal" in entry.get("execution_modes", []):
                errors.append("%s: a user-invocable skill cannot use internal execution" % skill_id)
            errors.extend(openai_errors(directory, skill_id))
        outputs = entry.get("persistent_outputs", [])
        if isinstance(outputs, list):
            checked_artifacts += len(outputs)
            for output in outputs:
                if isinstance(output, dict) and output.get("creation_mode") == "derived":
                    if output.get("semantic_authority") != "none":
                        errors.append("%s: derived output %r must have authority none" % (skill_id, output.get("type")))

    for directory in sorted(discovered - registered):
        errors.append("Unregistered skill: %s" % directory.relative_to(SKILLS_ROOT))
    for directory in sorted(registered - discovered):
        errors.append("Manifest path has no skill: %s" % directory.relative_to(SKILLS_ROOT))

    for skill_id, entry in planned.items():
        if not isinstance(entry, dict):
            errors.append("%s: planned entry must be a mapping" % skill_id)
        elif entry.get("status") != "planned" or entry.get("invocable") is not False or "path" in entry:
            errors.append("%s: planned capability must be non-invocable and pathless" % skill_id)
        if skill_id in active:
            errors.append("%s: cannot be active and planned" % skill_id)

    if any("_to_delete" in p.parts for p in SKILLS_ROOT.rglob("*")):
        errors.append("Deprecated _to_delete content remains inside SKILLS")

    known = active | set(planned)
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8-sig")
    for ref in set(re.findall(r"\$([a-z0-9-]+)", readme)):
        if ref not in known:
            errors.append("README references unknown skill $%s" % ref)

    current_links, checked_references = link_errors(REPO_ROOT)
    errors.extend(current_links)

    banned_patterns = {
        r"(?<![a-z0-9-])proposal-discover(?![a-z0-9-])": "q-proposal-discovery",
        r"(?<![a-z0-9-])quasar-crear-presentacion-consultoria(?![a-z0-9-])": "q-report-deck",
        r"(?<![a-z0-9-])05-implementation-roadmap\.md(?![a-z0-9-])": "05-technical-implementation-sequence.md",
        r"(?<![a-z0-9-])render_docx\.py(?![a-z0-9-])": "document_builder.py",
    }
    for path in REPO_ROOT.rglob("*"):
        if ignored_path(path) or path.resolve() == Path(__file__).resolve():
            continue
        if not path.is_file() or path.suffix.lower() not in {".md", ".yaml", ".yml", ".py", ".json"}:
            continue
        text = path.read_text(encoding="utf-8-sig")
        for pattern, new in banned_patterns.items():
            match = re.search(pattern, text)
            if match:
                errors.append("%s: obsolete reference %r; use %r" % (path, match.group(0), new))

    schemas = SKILLS_ROOT / "schemas"
    fixtures = SKILLS_ROOT / "fixtures"
    errors.extend(manifest_use_fixture_errors(schema, fixtures))
    errors.extend(fixture_pair(
        schemas / "artifact-index.schema.yaml",
        fixtures / "artifact-index.valid.yaml",
        fixtures / "artifact-index.invalid.yaml",
        artifact_semantics,
        active,
    ))
    errors.extend(fixture_pair(
        schemas / "workflow-state.schema.yaml",
        fixtures / "workflow-state.valid.yaml",
        fixtures / "workflow-state.invalid.yaml",
        workflow_state_semantics,
        active,
    ))
    errors.extend(fixture_pair(
        CORE_CONTRACT / "references" / "stage-result.schema.yaml",
        fixtures / "stage-result.valid.yaml",
        fixtures / "stage-result.invalid.yaml",
        stage_semantics,
        active,
    ))
    errors.extend(fixture_pair(
        SKILLS_ROOT / "tool" / "q-tool-database-schema" / "references" / "database-analysis.schema.yaml",
        fixtures / "database-analysis.valid.yaml",
        fixtures / "database-analysis.invalid.yaml",
        database_analysis_semantics,
        active,
        min_invalid_errors=5,
    ))
    errors.extend(fixture_pair(
        SKILLS_ROOT / "tool" / "q-tool-database-schema" / "references" / "database-analysis.schema.yaml",
        fixtures / "database-analysis.valid.yaml",
        fixtures / "database-analysis-incomplete.invalid.yaml",
        database_analysis_semantics,
        active,
        min_invalid_errors=3,
    ))
    errors.extend(fixture_pair(
        CORE_CONTRACT / "references" / "report-source.schema.yaml",
        fixtures / "report-source.valid.yaml",
        fixtures / "report-source.invalid.yaml",
        report_source_semantics,
        active,
    ))
    valid_brief = load(fixtures / "research-brief.valid.yaml")
    known_questions = {
        item.get("question_id")
        for item in valid_brief.get("questions", [])
        if isinstance(item, dict) and isinstance(item.get("question_id"), str)
    }
    errors.extend(fixture_pair(
        SKILLS_ROOT / "research" / "q-research-scope" / "references" / "research-brief.schema.yaml",
        fixtures / "research-brief.valid.yaml",
        fixtures / "research-brief.invalid.yaml",
        research_brief_semantics,
        active,
        min_invalid_errors=2,
    ))
    errors.extend(fixture_pair(
        CORE_CONTRACT / "references" / "cited-findings.schema.yaml",
        fixtures / "cited-findings.valid.yaml",
        fixtures / "cited-findings.invalid.yaml",
        lambda value: cited_findings_semantics(value, known_questions),
        active,
        min_invalid_errors=2,
    ))
    known_findings = {
        item.get("finding_id")
        for item in load(fixtures / "cited-findings.valid.yaml").get("findings", [])
        if isinstance(item, dict) and isinstance(item.get("finding_id"), str)
    }
    errors.extend(fixture_pair(
        SKILLS_ROOT / "research" / "q-research-synthesize" / "references" / "research-synthesis.schema.yaml",
        fixtures / "research-synthesis.valid.yaml",
        fixtures / "research-synthesis.invalid.yaml",
        lambda value: research_synthesis_semantics(value, known_findings, known_questions),
        active,
        min_invalid_errors=2,
    ))
    errors.extend(fixture_pair(
        SKILLS_ROOT / "research" / "q-research-workflow" / "references" / "research-baseline.schema.yaml",
        fixtures / "research-baseline.valid.yaml",
        fixtures / "research-baseline.invalid.yaml",
        research_baseline_semantics,
        active,
        min_invalid_errors=2,
    ))
    errors.extend(fixture_pair(
        CORE_CONTRACT / "references" / "ideation-baseline.schema.yaml",
        fixtures / "ideation-baseline.valid.yaml",
        fixtures / "ideation-baseline.invalid.yaml",
        ideation_baseline_semantics,
        active,
        min_invalid_errors=5,
    ))

    current_acceptance_errors, checked_scenarios = acceptance_errors()
    errors.extend(current_acceptance_errors)
    errors.extend(readme_planned_errors(set(planned)))
    errors.extend(package_doc_errors())
    errors.extend(routing_digest_errors(workflows))
    errors.extend(human_interaction_digest_errors(skills))
    errors.extend(skills_sh_errors(skills))
    errors.extend(anti_pattern_errors(skills))
    errors.extend(stray_file_errors())
    errors.extend(mermaid_runtime_errors(skills))

    return {
        "status": "Failed" if errors else ("Passed with warnings" if warnings else "Passed"),
        "errors": errors,
        "warnings": warnings,
        "checked_skills": len(skills),
        "checked_references": checked_references,
        "checked_artifacts": checked_artifacts,
        "checked_scenarios": checked_scenarios,
    }


def emit_yaml(result: dict[str, Any]) -> None:
    print("status: %s" % json.dumps(result["status"], ensure_ascii=False))
    for key in ("errors", "warnings"):
        if not result[key]:
            print("%s: []" % key)
        else:
            print("%s:" % key)
            for value in result[key]:
                print("  - %s" % json.dumps(value, ensure_ascii=False))
    for key in ("checked_skills", "checked_references", "checked_artifacts", "checked_scenarios"):
        print("%s: %s" % (key, result[key]))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the Quasar SKILLS package.")
    parser.add_argument("--format", choices=("yaml", "json"), default="yaml")
    args = parser.parse_args()
    result = run()
    print(json.dumps(result, ensure_ascii=False, indent=2)) if args.format == "json" else emit_yaml(result)
    return 1 if result["status"] == "Failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
