# Notes for agents working on this repo

- This repo **is** a set of agent skills. Skills live in `skills/<category>/<skill>/SKILL.md`; templates in `templates/<category>/<lang>/`.
- `templates/` and `skills/foundations/cloud-workspace/scripts/` are the source of truth. The copies under `skills/career-management/*/assets` and `.../scripts` are generated: edit the source, then run `python3 scripts/sync_skill_assets.py`.
- After any change run `scripts/build.sh` (sync, validation, parity, dry run, build, leak check). All must pass.
- English and pt-BR templates must keep the same structure and placeholders.
- Never add real people, employers, internal tool names, level/band schemes or company values to anything in this repo. Examples are fictional.
- Vocabulary: see `GLOSSARY.md`.
