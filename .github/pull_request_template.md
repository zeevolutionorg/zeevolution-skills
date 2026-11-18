## What changed

-

## Checklist

- [ ] `make check` passes locally (lint, consistency, tests, dry run, build, leak check)
- [ ] English and Portuguese templates changed together (parity check)
- [ ] New script → new test at the mirrored path under `tests/`
- [ ] New skill → `tests/skills/<category>/<skill>/test_skill.py` and an entry in `.claude-plugin/plugin.json`
- [ ] Changed a document? CHANGELOG says, per document, what changed (manual users rely on it)
- [ ] Behavior change in a skill? Add or update a case in `evals/` and add the `run-evals` label
- [ ] Only fictional people, companies and products
