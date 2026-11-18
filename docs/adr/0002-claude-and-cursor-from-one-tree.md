# 🏛️ ADR 0002 — Support Claude and Cursor from the same skill files

> [!NOTE]
> **Status:** ✅ accepted

## 📑 Contents

- [🧭 Context](#-context)
- [✅ Decision](#-decision)
- [⚖️ Consequences](#️-consequences)

---

## 🧭 Context

Both Claude and Cursor read the open `SKILL.md` format. Cursor walks `skills/` recursively and identifies a skill by its folder name; Claude Code reads the skill list in `.claude-plugin/plugin.json`.

## ✅ Decision

One `skills/` tree. Two thin manifests: `.claude-plugin/` (plugin + marketplace) and `.cursor-plugin/` (plugin + marketplace, for "From GitHub Repository"). `scripts/validate_skills.py` checks names are unique, every skill is listed, and both manifests share name and version.

## ⚖️ Consequences

Skill names must be unique across categories. Platform-specific behavior lives only in manifests and `docs/INSTALL.md`.
