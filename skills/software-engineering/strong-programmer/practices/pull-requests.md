# Pull requests

Habits that get pull requests merged — and reviewed well. Use them in every mode: when you open a PR (`develop`), and when you review one (`review-pr`, and `review-code` when the fixes will become PRs).

## When you open one

| Habit | Rule of thumb |
|---|---|
| Keep fixes small | Under 200 changed lines |
| Slice features | 200–800 changed lines per PR, each slice making sense on its own |
| Split big changes | Anything over 1,500 changed lines is split before it's opened |
| Stack, but not too high | At most 3 or 4 stacked PRs; the upper ones stay in draft until the base is reviewed |
| Open as a draft | While you're still working; mark it ready when CI is green |
| Write for a reviewer with no context | The description says **what changed**, **why**, **how you tested it** and **where to start reading** |

Also:

- One concern per PR. Tidyings (structure) and behavior changes go in separate commits, ideally separate PRs.
- Generated files, lockfiles and renames inflate the count: say so in the description, so the reviewer knows what to skip.
- When a base PR changes, rebase the PRs above it and validate them again before pushing.

## When you review one

| Habit | Rule of thumb |
|---|---|
| Answer quickly | Within 8 business hours — or say on the PR when you will |
| Read for what matters first | Bugs, design and tests before naming and style; leave formatting to linters |
| Say what you checked | And what you didn't, so the author knows what is still unreviewed |
| Block only on must-fix | Request changes only for what must change; mark everything else `nit:` or `suggestion:` |
| Don't skim a huge PR | Over 2,000 changed lines, ask for a split instead of skimming |

## Applying it in each mode

| Mode | What to do |
|---|---|
| `develop` | Plan the slices before writing code; open each as a draft; write the description from the four parts; stack at most 3 or 4 |
| `review-pr` | Check the size first; then bugs, design and tests; label every finding; say what you checked; give a verdict |
| `review-code` | Group findings into PR-sized fixes the team could open, each within the size limits above |
