# 🤝 Contributing

Thanks for helping! These skills stay **small, composable and usable without AI**. Please read this page before opening a pull request.

> [!TIP]
> zeevolution-skills is a **library of categories**. 🌱 Career management is the first; new categories are welcome — see [🗂️ Adding a category](#️-adding-a-category).

## 📑 Contents

- [📜 Ground rules](#-ground-rules)
- [🔁 Your workflow](#-your-workflow)
- [🧪 Local checks](#-local-checks)
- [🧱 Skill format](#-skill-format)
- [🗂️ Adding a category](#️-adding-a-category)
- [🏷️ Versioning](#️-versioning)
- [✅ Pull request checklist](#-pull-request-checklist)

---

## 📜 Ground rules

| # | Rule | Enforced by |
|---|---|---|
| 1 | 🕵️ **No employer traces.** Fictional people, companies and products only. No internal tool names, performance-system names, level/band schemes, org units or company values. | Review. `scripts/check_leaks.py` rejects personal emails, non-public URLs and document metadata |
| 2 | ✋ **Every template works by hand.** If a step needs an agent, it isn't a template. | Review + Manual Kit build |
| 3 | 💡 **Every section has a tip:** ℹ️ what it is, 💡 how to use, ✍️ a practical example ([doc-templates](skills/foundations/doc-templates/SKILL.md)). | `tests/templates/…/test_documents.py` |
| 4 | 🌎 **English and Brazilian Portuguese stay in sync:** same headings, tables, callouts and placeholders. | `scripts/check_parity.py` |
| 5 | 🧱 **Foundations are built once.** Platform code, tip rules, discipline vocabulary and user defaults live in `skills/foundations/`. A category never re-implements them. | Review |

## 🔁 Your workflow

1. 🌿 Branch from `main`.
2. ✏️ Change the **sources**: `templates/` and `skills/foundations/cloud-workspace/scripts/`. Never edit the bundled copies under `skills/career-management/*/assets` or `*/scripts` by hand.
3. 🔄 Run `python3 scripts/sync_skill_assets.py` to refresh the bundled copies.
4. 🧪 Add or update the test at the **mirrored path** under `tests/`.
5. ✅ Run `make check`.
6. 📬 Open the PR.

## 🧪 Local checks

```bash
make install   # dev dependencies + pre-commit hooks
make check     # the same stages CI runs: lint, consistency, tests, e2e, sheets, leak check
```

> [!TIP]
> Tests mirror the repository layout (`scripts/x.py` → `tests/scripts/test_x.py`). See [docs/TESTING.md](docs/TESTING.md) for test levels, the CI/CD sequence and the tools.

## 🧱 Skill format

- 📁 Folder name = `name` in the `SKILL.md` frontmatter (lowercase, hyphens). Names are unique across categories.
- 📝 `description` says what the skill does **and when to use it**.
- ⌨️ User-invoked skills set `disable-model-invocation: true`.
- ✂️ Keep `SKILL.md` focused; move detail to sibling `.md` files the skill links to.
- 🧪 Every skill has `tests/skills/<category>/<skill>/test_skill.py`.

## 🗂️ Adding a category

A category groups skills for one aspect of a technologist's work. Add one only when a practice is repeated often enough to be worth packaging.

| Step | Add |
|---|---|
| 1️⃣ | `skills/<category>/README.md` and its skills. If the category sets up a whole set of documents, give it one **`<something>-toolkit`** user-invoked skill, with working skills on top; standalone skills are fine too (see `software-engineering`) |
| 2️⃣ | A contract test per skill at `tests/skills/<category>/<skill>/test_skill.py`, and `tests/.../scripts/test_<name>.py` for any script |
| 3️⃣ | `templates/<category>/<lang>/` if it produces documents (`en` and `pt-BR`), plus `*.sheet.yaml` / `*.strings.yaml` for spreadsheets, and `tests/templates/<category>/` |
| 4️⃣ | Each skill folder in `.claude-plugin/plugin.json` → `skills` |
| 5️⃣ | A row in the README "Skills reference" and a page under `docs/<category>/` |
| 6️⃣ | If the skills bundle templates, extend `scripts/sync_skill_assets.py` |

> [!IMPORTANT]
> Use `cloud-workspace` to create files, `doc-templates` for placeholders and tips, `disciplines` for wording. Never write a new platform adapter inside a category.

## 🏷️ Versioning

- 🔢 Bump the version in **both** `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json` — `scripts/validate_skills.py` checks they match, and the release workflow checks they match the tag.
- 📝 Add a CHANGELOG entry that says, **per document**, what changed — manual users rely on it.

## ✅ Pull request checklist

The [PR template](.github/pull_request_template.md) asks for:

- [ ] `make check` passes locally
- [ ] English and Portuguese templates changed together
- [ ] New script → new test at the mirrored path
- [ ] New skill → contract test + entry in `.claude-plugin/plugin.json`
- [ ] Document changed → CHANGELOG entry per document
- [ ] Only fictional people, companies and products
