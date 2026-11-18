#!/usr/bin/env python3
"""Validate skills and plugin manifests.

- Every skills/**/SKILL.md has YAML frontmatter with `name` (== folder name, lowercase-hyphen) and `description`.
- Skill names are unique across categories (Cursor identifies skills by folder name).
- .claude-plugin/plugin.json lists every skill folder, and nothing else.
- Claude and Cursor manifests carry the same name and version.

  python3 scripts/validate_skills.py
"""
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    return yaml.safe_load(m.group(1))


def main():
    errors = []
    seen = {}
    skill_dirs = []
    for skill_md in sorted((ROOT / "skills").rglob("SKILL.md")):
        if "assets" in skill_md.parts:
            continue
        folder = skill_md.parent
        skill_dirs.append("./" + str(folder.relative_to(ROOT)))
        fm = frontmatter(skill_md)
        rel = skill_md.relative_to(ROOT)
        if not fm:
            errors.append(f"{rel}: missing frontmatter")
            continue
        name, desc = fm.get("name"), fm.get("description")
        if name != folder.name:
            errors.append(f"{rel}: name '{name}' must equal folder '{folder.name}'")
        if not name or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
            errors.append(f"{rel}: invalid name '{name}'")
        if not desc or len(desc) < 40:
            errors.append(f"{rel}: description missing or too short")
        if len(desc or "") > 1024:
            errors.append(f"{rel}: description longer than 1024 characters")
        if name in seen:
            errors.append(f"{rel}: duplicate skill name '{name}' (also {seen[name]})")
        seen[name] = rel
    claude = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    cursor = json.loads((ROOT / ".cursor-plugin" / "plugin.json").read_text())
    listed = set(claude.get("skills", []))
    if listed != set(skill_dirs):
        errors.append(f"plugin.json skills mismatch: missing {sorted(set(skill_dirs) - listed)}, extra {sorted(listed - set(skill_dirs))}")
    for key in ("name", "version"):
        if claude.get(key) != cursor.get(key):
            errors.append(f"manifest {key} differs: claude={claude.get(key)} cursor={cursor.get(key)}")
    for mp in (ROOT / ".claude-plugin" / "marketplace.json", ROOT / ".cursor-plugin" / "marketplace.json"):
        data = json.loads(mp.read_text())
        if not any(p.get("name") == claude["name"] for p in data.get("plugins", [])):
            errors.append(f"{mp.relative_to(ROOT)}: plugin '{claude['name']}' not listed")
    if errors:
        print("Skill validation FAILED:\n- " + "\n- ".join(errors))
        sys.exit(1)
    print(f"{len(skill_dirs)} skills valid; manifests consistent (v{claude['version']})")


if __name__ == "__main__":
    main()
