from __future__ import annotations

import argparse
import json
import re
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
    if set(data) != {"name", "description"}:
        errors.append("%s: frontmatter keys must be exactly name and description" % path)
    name = data.get("name")
    desc = data.get("description")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9-]{1,63}", name):
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
        path for path in SKILLS_ROOT.rglob("SKILL.md") if path.parent.resolve() != directory.resolve()
    )
    if not any(
        path.is_file() and skill_id in path.read_text(encoding="utf-8-sig")
        for path in pointer_paths
    ):
        errors.append("%s: internal companion is unreachable from AGENTS.md or an owning skill" % skill_id)
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
        "domain-data-modeling",
        "high-level-architecture-standards",
        "module-feature-decomposition",
        "backlog-and-delivery-planning",
    }
    stage_status = data.get("stage_status", {})
    foundation_completed = (
        isinstance(stage_status, dict)
        and stage_status.get("technical-foundation-definition") == "completed"
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


def fixture_pair(
    schema_path: Path,
    valid_path: Path,
    invalid_path: Path,
    semantic,
    active: set[str],
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
    if not invalid_errors:
        errors.append("%s was incorrectly accepted" % invalid_path.name)
    return errors


def acceptance_errors() -> tuple[list[str], int]:
    checks = {
        "S-01": [
            ("discovery/discovery-proposal-workflow/SKILL.md", "accepted_without_development"),
            ("discovery/discovery-proposal-workflow/SKILL.md", "future/manual execution"),
        ],
        "S-02": [
            ("discovery/discovery-proposal-workflow/SKILL.md", "proposal object IDs"),
            ("discovery/proposal-discovery/SKILL.md", "assumptions"),
        ],
        "S-03": [
            ("app-flow/product-core-definition/SKILL.md", "started without a proposal"),
        ],
        "S-04": [
            ("app-flow/backlog-and-delivery-planning/SKILL.md", "initial-generation"),
            ("app-flow/backlog-and-delivery-planning/SKILL.md", "Do not require all stories"),
        ],
        "S-05": [
            ("app-flow/backlog-and-delivery-planning/SKILL.md", "replan-and-synchronize"),
            ("app-flow/backlog-and-delivery-planning/SKILL.md", "required approval"),
        ],
        "S-06": [
            ("app-flow/ai-coding-workflow/SKILL.md", "Skip a grill"),
            ("app-flow/ai-coding-workflow/SKILL.md", "Enable `tdd` only"),
        ],
        "S-07": [
            ("coding/to-tickets/SKILL.md", "Tickets are durable"),
            ("coding/to-tickets/SKILL.md", "preserve backlog, requirement, decision, and plan IDs"),
        ],
        "S-08": [
            ("coding/implement/SKILL.md", "internal plans, scratchpads, and delegation messages transient"),
            ("coding/implement/SKILL.md", "Update only the original durable record"),
        ],
        "S-09": [
            ("discovery/discovery-proposal-workflow/SKILL.md", "Return scope, price, schedule, commitment, or source errors"),
            ("discovery/discovery-proposal-workflow/SKILL.md", "visual, layout, accessibility"),
        ],
        "S-10": [
            ("app-flow/ai-coding-workflow/SKILL.md", "accepted commercial scope"),
            ("app-flow/ai-coding-workflow/SKILL.md", "Keep the accepted release immutable"),
        ],
        "S-11": [
            ("coding/code-review/SKILL.md", "sequential passes"),
            ("coding/code-review/SKILL.md", "Keep results separate"),
        ],
        "S-12": [
            ("app-flow/technical-foundation-definition/SKILL.md", "Never block solely because the selected stack is not T3"),
            ("00-cross-workflow-contract.md", "profile-driven"),
        ],
        "S-13": [
            ("app-flow/ai-coding-workflow/SKILL.md", "On resume"),
            ("app-flow/ai-coding-workflow/SKILL.md", "Do not reopen closed decisions"),
        ],
        "S-14": [
            ("00-cross-workflow-contract.md", "Domain or architecture Mermaid source"),
            ("00-cross-workflow-contract.md", "SVG, PNG, or PDF rendered from Mermaid"),
        ],
        "S-15": [
            ("reporting/reporting-workflow/SKILL.md", "Reporting is optional"),
            ("reporting/reporting-source-design/SKILL.md", "approved as a reporting snapshot"),
            ("discovery/discovery-proposal-workflow/SKILL.md", "Reporting is optional"),
        ],
        "S-16": [
            ("00-cross-workflow-contract.md", "must not commit, publish, message external systems"),
            ("skill-manifest.yaml", "approval_policy"),
        ],
        "S-17": [
            ("00-cross-workflow-contract.md", "reconciliation_required: true"),
            ("00-cross-workflow-contract.md", "global_state_updated: false"),
        ],
        "S-18": [
            ("coding/explore/SKILL.md", "Return the summary in the conversation as transient context"),
            ("app-flow/ai-coding-workflow/SKILL.md", "do not register it as an artifact"),
        ],
        "S-19": [
            ("quality/audit-docs/SKILL.md", "Return the diagnostic in the conversation as transient context"),
            ("quality/audit-docs/SKILL.md", "Record any later implemented documentation change through the owning workflow"),
            ("quality/audit-docs/SKILL.md", "stop and route the request to `maintain-ai-workflow`"),
            ("app-flow/ai-coding-workflow/SKILL.md", "`audit-docs` is optional"),
            ("discovery/discovery-proposal-workflow/SKILL.md", "`audit-docs` is optional"),
        ],
        "S-20": [
            ("00-cross-workflow-contract.md", "root orchestrator"),
            ("reporting/reporting-workflow/SKILL.md", "composite delta with `global_state_updated: false`"),
            ("app-flow/ai-coding-workflow/SKILL.md", "Remain the global state writer"),
        ],
        "S-21": [
            ("reporting/reporting-source-design/SKILL.md", "single semantic source"),
            ("reporting/generate-report/SKILL.md", "semantic_authority: none"),
            ("reporting/generate-quasar-deck/SKILL.md", "semantic_authority: none"),
        ],
        "S-22": [
            ("reporting/generate-report/SKILL.md", "Return semantic edits to `reporting-source-design`"),
            ("reporting/generate-quasar-deck/SKILL.md", "Return semantic edits to `reporting-source-design`"),
            ("reporting/generate-report/SKILL.md", "missing requested format"),
        ],
        "S-23": [
            ("app-flow/technical-foundation-definition/references/web-stack-recommendation.md", "TypeScript"),
            ("app-flow/technical-foundation-definition/references/web-stack-recommendation.md", "Next.js App Router"),
            ("app-flow/technical-foundation-definition/references/web-stack-recommendation.md", "tRPC"),
            ("app-flow/technical-foundation-definition/references/web-stack-recommendation.md", "Zod"),
            ("app-flow/technical-foundation-definition/references/web-stack-recommendation.md", "Zustand"),
            ("app-flow/technical-foundation-definition/references/web-stack-recommendation.md", "shadcn/ui"),
            ("app-flow/technical-foundation-definition/references/web-stack-recommendation.md", "React Hook Form"),
            ("app-flow/technical-foundation-definition/references/web-stack-recommendation.md", "Drizzle or Prisma"),
        ],
        "S-24": [
            ("app-flow/technical-foundation-definition/SKILL.md", "Preserve an existing stack"),
            ("app-flow/technical-foundation-definition/SKILL.md", "Evaluate an explicit user proposal"),
            ("app-flow/technical-foundation-definition/SKILL.md", "current primary sources"),
        ],
        "S-25": [
            ("00-cross-workflow-contract.md", "sole owner of the authored technical foundation"),
            ("app-flow/ai-coding-workflow/SKILL.md", "technical_foundation_ref"),
            ("app-flow/high-level-architecture-standards/SKILL.md", "never edit their owned artifacts directly"),
        ],
        "S-26": [
            ("coding/codebase-review/SKILL.md", "A recommended but unselected library is not"),
            ("coding/codebase-review/SKILL.md", "generic and repository-grounded criteria"),
            ("coding/codebase-review/SKILL.md", "do not issue a full stack-specific approval"),
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
        for phrase in ('$maintain-ai-workflow', 'administrative housekeeping', 'CHANGELOG.md'):
            if phrase not in text:
                errors.append('AGENTS.md is missing maintenance pointer %r' % phrase)

    changelog = REPO_ROOT / 'CHANGELOG.md'
    if changelog.is_file() and '## [Unreleased]' not in changelog.read_text(encoding='utf-8-sig'):
        errors.append('CHANGELOG.md must contain an Unreleased section')

    license_path = REPO_ROOT / 'LICENSE'
    if license_path.is_file():
        text = license_path.read_text(encoding='utf-8-sig')
        for phrase in ('MIT License',):
            if phrase not in text:
                errors.append('LICENSE is missing required notice %r' % phrase)

    maintenance = SKILLS_ROOT / 'maintenance' / 'maintain-ai-workflow' / 'SKILL.md'
    if maintenance.is_file():
        text = maintenance.read_text(encoding='utf-8-sig')
        for phrase in (
            'Act as the package housekeeper',
            'Run the philosophy and anti-pattern gate',
            'Do not return a project `stage_result`',
        ):
            if phrase not in text:
                errors.append('maintain-ai-workflow is missing governance evidence %r' % phrase)

    installed = REPO_ROOT / '.agents' / 'skills' / 'maintain-ai-workflow'
    canonical = SKILLS_ROOT / 'maintenance' / 'maintain-ai-workflow'
    if not installed.exists():
        errors.append('maintain-ai-workflow is not installed in .agents/skills')
    elif not installed.is_symlink():
        errors.append('maintain-ai-workflow repo installation must link to its canonical package source')
    elif installed.resolve() != canonical.resolve():
        errors.append('maintain-ai-workflow repo installation points to the wrong source')
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
    discovered = {p.parent.resolve() for p in SKILLS_ROOT.rglob("SKILL.md") if "_to_delete" not in p.parts}
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
            optional_next = workflow_entry.get("optional_next", [])
            if not isinstance(optional_next, list):
                errors.append("workflow %s.optional_next must be a list" % workflow_id)
            else:
                for target in optional_next:
                    if target not in workflows and target not in terminal_routes:
                        errors.append("workflow %s.optional_next references unknown route %r" % (workflow_id, target))

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
        if directory.name != skill_id:
            errors.append("%s: folder name is %r" % (skill_id, directory.name))
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
        r"(?<![a-z0-9-])proposal-discover(?![a-z0-9-])": "proposal-discovery",
        r"(?<![a-z0-9-])quasar-crear-presentacion-consultoria(?![a-z0-9-])": "generate-quasar-deck",
        r"(?<![a-z0-9-])05-implementation-roadmap\.md(?![a-z0-9-])": "05-technical-implementation-sequence.md",
        r"(?<![a-z0-9-])render_docx\.py(?![a-z0-9-])": "document_builder.py",
    }
    for path in REPO_ROOT.rglob("*"):
        if path.resolve() == Path(__file__).resolve():
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
        schemas / "stage-result.schema.yaml",
        fixtures / "stage-result.valid.yaml",
        fixtures / "stage-result.invalid.yaml",
        stage_semantics,
        active,
    ))
    errors.extend(fixture_pair(
        schemas / "report-source.schema.yaml",
        fixtures / "report-source.valid.yaml",
        fixtures / "report-source.invalid.yaml",
        report_source_semantics,
        active,
    ))

    current_acceptance_errors, checked_scenarios = acceptance_errors()
    errors.extend(current_acceptance_errors)
    errors.extend(readme_planned_errors(set(planned)))
    errors.extend(package_doc_errors())

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
