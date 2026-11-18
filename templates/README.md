# Templates

Source of truth for every document the skills create. Usable by hand: see [docs/MANUAL.md](../docs/MANUAL.md).

- `<category>/<lang>/NN-name.md` — documents (Markdown subset, `{{placeholders}}`, ℹ️ / 💡 / ✍️ tips).
- `<category>/*.sheet.yaml` — spreadsheet structure; `<category>/<lang>/*.strings.yaml` — its words.
- `career-management/<lang>/generic-ladder.yaml` — the generic career ladder.

Rules: `skills/foundations/doc-templates/SKILL.md`. Checks: `scripts/check_parity.py`.
