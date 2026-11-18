# 🗂️ Templates

The source of truth for every document the skills create — also usable by hand: see [docs/MANUAL.md](../docs/MANUAL.md).

## 📑 Contents

- [📁 Layout](#-layout)
- [📏 Rules](#-rules)
- [✅ Checks](#-checks)

---

## 📁 Layout

| Path | What it is |
|---|---|
| 📝 `<category>/<lang>/NN-name.md` | Documents: Markdown subset, `{{placeholders}}`, ℹ️ / 💡 / ✍️ tips |
| 📊 `<category>/*.sheet.yaml` | Spreadsheet structure (language-neutral) |
| 🔤 `<category>/<lang>/*.strings.yaml` | The spreadsheet's words, per language |
| 📦 `<category>/bundle.yaml` | Which documents exist, their order, titles and modes |
| 🪜 `career-management/<lang>/generic-ladder.yaml` | The generic career ladder |

## 📏 Rules

Every template follows [doc-templates](../skills/foundations/doc-templates/SKILL.md): one ℹ️ "what this is" per document, 💡 "how to use" + ✍️ example per section, only known placeholders, fictional examples.

## ✅ Checks

| Check | Command |
|---|---|
| 🌎 English / Portuguese parity | `python3 scripts/check_parity.py` |
| 🧪 Template contracts | `python3 -m pytest tests/templates` |
