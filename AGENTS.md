# Notes for agents working on this repo

- This repo **is** a set of agent skills. Skills live in `skills/<category>/<skill>/SKILL.md`; templates in `templates/<category>/<lang>/`.
- `templates/` and `skills/foundations/cloud-workspace/scripts/` are the source of truth. The copies under `skills/career-management/*/assets` and `.../scripts` are generated: edit the source, then run `python3 scripts/sync_skill_assets.py`.
- After any change run `make check` (lint, sync, validation, parity, tests, dry run, sheets, leak check). All must pass.
- Tests mirror the source tree: `scripts/x.py` → `tests/scripts/test_x.py`; a skill → `tests/skills/<category>/<skill>/test_skill.py`. Every test has a level marker (unit/contract/e2e/libreoffice). See `docs/TESTING.md`.
- English and pt-BR templates must keep the same structure and placeholders.
- Never add real people, employers, internal tool names, level/band schemes or company values to anything in this repo. Examples are fictional.
- Vocabulary: see `GLOSSARY.md`.
