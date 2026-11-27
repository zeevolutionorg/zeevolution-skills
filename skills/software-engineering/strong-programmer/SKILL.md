---
name: strong-programmer
description: >-
  Strong-programmer knowledge for writing and reviewing code: programming paradigms and approaches,
  object-oriented design, design patterns and their misuse, Kotlin and Java idioms for the project's
  version, software layers and hexagonal architecture, pull-request habits, validating your own work,
  and Tidy First. Use when implementing or refactoring a task, opening or reviewing a pull request /
  diff, reviewing existing code, choosing between paradigms or patterns, questioning whether a pattern
  fits, deciding where code belongs, spotting code smells or SOLID violations, or deciding whether to
  tidy code before, after or instead of a change. Triggers: "review this PR", "code review",
  "implement", "refactor", "open a PR", "design pattern", "SOLID", "code smell", "architecture",
  "layers", "hexagonal", "ports and adapters", "Kotlin idiom", "Java version", "tidy first".
---

# strong-programmer

Understand what the code is before judging it, use the language version the project runs, keep changes reviewable, and prove the work before calling it done.

The knowledge is a tree: paradigm → approach → topic, with languages across it and practices that apply anywhere. [`map.md`](map.md) lists every node and its depth — ✅ detailed, 🌱 fundamentals, 🔜 planned. Open only what the task needs.

## Modes

| Mode | Use it for | You deliver |
|---|---|---|
| `develop` | Implementing, fixing or refactoring a task | The change in reviewable PRs, validated, with PR descriptions |
| `review-code` | Existing code: a file, a module, a repository | A review report with a health verdict |
| `review-pr` | A pull request or a diff | A review report with a verdict |

## Steps

1. **Pick the mode.** Infer it; ask only when genuinely unclear.
2. **Orient before judging.** Before any finding or new code, establish and state:
   - **Language and version**, from the build files ([`languages/README.md`](languages/README.md)). Never suggest a feature newer than the project's version.
   - **Paradigm and approach** ([`paradigms/README.md`](paradigms/README.md)). Code mixes approaches: name the dominant one per area and judge each area by its own standards.
   - **The project's checks and CI** ([`practices/validating-work.md`](practices/validating-work.md)).
   - **The layers**: where the application core is and which adapters surround it. Domain rules never import frameworks, databases or transport code; dependencies point toward the core.
   - **The codebase's conventions**: follow them unless they are the problem.
3. **Load the branch.** Open the matching map nodes. For a 🔜 node, use general knowledge and list it under **Not covered yet**.
4. **Tidy First.** Before changing behavior, ask whether a small structural tidying makes the change easier. Keep structure and behavior changes in separate commits and separate findings.
5. **Do the work.**
   - `develop`: slice the change into PR-sized steps ([`practices/pull-requests.md`](practices/pull-requests.md)); choose the approach that fits the problem; put new code in the right layer; use a pattern only when the problem matches its intent; use the detected version's idioms; write tests.
   - `review-pr`: size first — over 2,000 changed lines, ask for a split instead of skimming. Then bugs, design (including dependency direction) and tests before anything else; leave style to linters; check CI.
   - `review-code`: start where the risk is — entry points, the most-changed files, what the user named.
6. **Validate.** In `develop`, run what CI runs, locally, then follow your PR's checks to green; never report done on red or unverified checks. In reviews, report the CI status and run what you can; the author fixes their own PR. Say what couldn't run and why.
7. **Report.** Use the shapes below.

## Report

**Reviews**, in this order:

1. **Verdict** — `review-pr`: Approve, Request changes (only for must-fix items), or Request a split. `review-code`: overall health and the riskiest area.
2. **What I checked** — and what I didn't.
3. **Context** — language and version, approach, layers, checks and CI status.
4. **Findings** — blocker, major, minor (`suggestion:`), nit (`nit:`), most severe first; only blockers and majors are must-fix. Each with file and line, why it matters, the map node behind it, and a fix that works on the project's version.
5. **Tidy First** — tidyings worth doing first, after, later, or never.
6. **Not covered yet** — 🔜 nodes and unlisted languages this review touched.

**Develop:**

1. **The change** — sliced into PRs that each make sense alone.
2. **Design choices** — approach and patterns, with the map node behind each.
3. **Tidyings** — in their own commits.
4. **Validation** — commands run and results, CI status, what couldn't run here.
5. **PR description** — what changed, why, how you tested it, where to start reading. Open it as a draft.
6. **Not covered yet** — 🔜 nodes and unlisted languages this change touched.
