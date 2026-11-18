# 🏛️ ADR 0001 — Bundle templates and scripts inside the skills that use them

> [!NOTE]
> **Status:** ✅ accepted

## 📑 Contents

- [🧭 Context](#-context)
- [✅ Decision](#-decision)
- [⚖️ Consequences](#️-consequences)

---

## 🧭 Context

People install skills in different ways: the whole Claude Code plugin, a Cursor GitHub import, `npx skills` picking individual skills, or one `.skill` file uploaded to the Claude app. A skill that reads `../../templates/` breaks in the last two cases.

## ✅ Decision

`templates/` and `skills/foundations/cloud-workspace/scripts/` stay the single source of truth. `scripts/sync_skill_assets.py` copies what each skill needs into its own `assets/` and `scripts/` folders, and CI fails if the copies drift (`--check`).

## ⚖️ Consequences

Some files exist twice in git. Editing a copy instead of the source is caught by CI.
