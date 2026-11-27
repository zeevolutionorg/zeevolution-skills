## What changed

-

## Why

-

## How I tested

<!-- Commands you ran and their results. Anything you could not run locally, and what covers it (usually CI). -->

-

## Where to start reading

-

## Checklist

- [ ] `make check` passes locally (lint incl. markdownlint, consistency, tests, e2e + dry run + build, sheets when LibreOffice is installed, leak check, secret scan when Go is installed)
- [ ] Size: under 200 changed lines for a fix, 200–800 for a feature slice; anything over 1,500 is split
- [ ] English and Portuguese templates changed together (parity check)
- [ ] New script → new test at the mirrored path under `tests/`
- [ ] New skill → `tests/skills/<category>/<skill>/test_skill.py` and an entry in `.claude-plugin/plugin.json`
- [ ] Changed a document? CHANGELOG says, per document, what changed (manual users rely on it)
- [ ] Only fictional people, companies and products
