# Behavioral evals

End-to-end checks of how an agent **behaves** with the skills — the part unit tests can't see: does `/career-hub-toolkit` fire, ask before creating, fall back when there's no connector, and report the bi-weekly rhythm?

They run with `claude plugin eval` (each case is a fresh `claude -p` session). Format: `evals/<case>/prompt.md` (frontmatter + prompt) and `evals/<case>/graders/*.md` (`tool_used`, `file_exists`, `regex`, `llm`).

```bash
claude plugin eval . --trust-plugin --no-publish --tag smoke --runs 1 --threshold 0.75 --max-cost-usd 5 --json results.json
```

- `smoke` cases run on PRs that touch `skills/` or `templates/` (label `run-evals`), the full suite nightly.
- They cost real model usage: keep cases short and fictional. Never put real people's data here.
- Results land in `evals/results/` (git-ignored).

> Verify the format against the official "Test plugins with evals" page for your Claude Code version before relying on a new grader type.
