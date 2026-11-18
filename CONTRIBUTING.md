# Contributing

Thanks for helping. These skills stay **small, composable and usable without AI**. Before opening a PR, read this page.

## Ground rules

1. **No employer traces.** Examples use fictional people, companies and products only. No internal tool names, performance-system names, level/band schemes, org units or company values. The leak check (`scripts/check_leaks.py`) runs on every PR.
2. **Every template works by hand.** If a step needs an agent, it isn't a template.
3. **Every section has a tip.** ℹ️ what it is, 💡 how to use, ✍️ a practical example (see `skills/foundations/doc-templates/SKILL.md`).
4. **English and Brazilian Portuguese stay in sync.** Same headings, tables, callouts and placeholders (`scripts/check_parity.py`).
5. **Foundations are built once.** Platform code, tip rules, discipline vocabulary and user defaults live in `skills/foundations/`. A category never re-implements them.

## Local checks

```bash
python3 -m pip install -r requirements.txt
scripts/build.sh            # sync assets, validate skills, parity, dry run, build dist/, leak check
```

For the leak check to cover employer terms locally, keep a denylist at `~/.config/zeevolution/denylist.txt` (one term per line). It never goes into the repo.

## Adding a category

A category groups skills for one aspect of a technologist's work. Add one only when a practice is repeated often enough to be worth packaging.

1. `skills/<category>/README.md` and its skills: one **`<something>-toolkit`** user-invoked skill that sets up the category's documents, then working skills on top.
2. `templates/<category>/<lang>/` if it produces documents (`en` and `pt-BR`), plus `*.sheet.yaml` / `*.strings.yaml` for spreadsheets.
3. Add each skill folder to `.claude-plugin/plugin.json` → `skills`.
4. A row in the README "Reference" section, and a page under `docs/<category>/`.
5. If the skills bundle templates, extend `scripts/sync_skill_assets.py`.

Use `cloud-workspace` to create files, `doc-templates` for placeholders and tips, `disciplines` for wording. Never write a new platform adapter inside a category.

## Skill format

- Folder name = `name` in the `SKILL.md` frontmatter (lowercase, hyphens). Names are unique across categories.
- `description` says what the skill does **and when to use it**.
- User-invoked skills set `disable-model-invocation: true`.
- Keep `SKILL.md` focused; move detail to sibling `.md` files the skill links to.

## Versioning

Bump the version in **both** `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json` (`scripts/validate_skills.py` checks they match) and add a CHANGELOG entry that says, per document, what changed — manual users rely on it.
