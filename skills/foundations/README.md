# 🧱 Foundations

Shared building blocks used by every category. A category never re-implements these.

## 📑 Contents

- [🧩 Skills](#-skills)
- [🔌 Delivery paths](#-delivery-paths)
- [🛠️ Scripts](#️-scripts)

---

## 🧩 Skills

| Skill | Type | What it does |
|---|---|---|
| ⚙️ [setup-zeevolution-skills](setup-zeevolution-skills/SKILL.md) | ⌨️ user | One-time defaults: name, discipline, platform, folder, language, ladder |
| ☁️ [cloud-workspace](cloud-workspace/SKILL.md) | 🤖 model | Creates and links documents and spreadsheets; renders templates; builds sheets from specs |
| 📝 [doc-templates](doc-templates/SKILL.md) | 🤖 model | Placeholders, tip anatomy, self vs lead wording, languages |
| 🎨 [disciplines](disciplines/SKILL.md) | 🤖 model | Vocabulary and examples for engineering, data science, design, product |

## 🔌 Delivery paths

`cloud-workspace` always ends with something usable:

| # | Adapter | Guide |
|---|---|---|
| 1 | 🔗 Google Workspace / Microsoft 365 | [GOOGLE.md](cloud-workspace/GOOGLE.md) · [MICROSOFT.md](cloud-workspace/MICROSOFT.md) |
| 2 | 📁 Files (`.docx` / `.xlsx`) | [FILES.md](cloud-workspace/FILES.md) |
| 3 | 📋 Manual (Markdown to paste) | [MANUAL.md](cloud-workspace/MANUAL.md) |

## 🛠️ Scripts

| Script | Does |
|---|---|
| `render_doc.py` | Markdown template → `.docx`, `.html` or filled `.md` |
| `build_sheet.py` | Sheet spec (YAML) → formatted, automated `.xlsx` — see [SHEETS.md](cloud-workspace/SHEETS.md) |
| `make_bundle.py` | A whole document bundle (Files or Manual), links included, hub last |
