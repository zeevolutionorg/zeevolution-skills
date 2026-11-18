# 🎯 Behavioral evals

End-to-end checks of how an agent **behaves** with the skills — the part unit tests can't see.

## 📑 Contents

- [❓ What they check](#-what-they-check)
- [📁 Format](#-format)
- [▶️ Run them](#️-run-them)
- [💸 Cost and rules](#-cost-and-rules)

---

## ❓ What they check

| Case | Checks that the skill… | Tags |
|---|---|---|
| `career-hub-self-manual-en` | builds a self-mode hub as Markdown + paste guide and reports the bi-weekly rhythm | smoke |
| `career-hub-lead-files-ptbr` | builds a lead-mode hub as `.docx` / `.xlsx` in Portuguese, without the optional docs | — |
| `career-hub-asks-before-creating` | asks for missing information and creates nothing | smoke |
| `career-hub-no-connector-fallback` | says there's no Google tool and falls back instead of pretending | smoke |
| `create-adr-asks-first` | `create-adr` asks for the input mode and folder before writing | smoke |
| `service-handoff-interviews-first` | `/service-handoff` interviews the engineer before writing | — |

## 📁 Format

- 📝 `evals/<case>/prompt.md` — frontmatter (name, tags, runs, max_turns, timeout, allowed tools) + the prompt.
- ⚖️ `evals/<case>/graders/*.md` — `tool_used`, `file_exists`, `regex` or `llm` graders.
- 🧪 `tests/evals/test_cases.py` checks every case is well formed.

## ▶️ Run them

```bash
claude plugin eval . --trust-plugin --no-publish --tag smoke --runs 1 --threshold 0.75 --max-cost-usd 5 --json results.json
```

| Where | When |
|---|---|
| 🔀 Pull requests | Smoke cases, when the PR has the **`run-evals`** label |
| 🌙 Nightly | The full suite, 3 runs each |
| 💻 Locally | `make evals` |

## 💸 Cost and rules

- 💸 Each case is a real agent session (a fresh `claude -p`): keep cases short.
- 🕵️ Fictional people only — never real data.
- 🗃️ Results land in `evals/results/` (git-ignored).

> [!CAUTION]
> Verify the format against the official "Test plugins with evals" page for your Claude Code version before relying on a new grader type.
