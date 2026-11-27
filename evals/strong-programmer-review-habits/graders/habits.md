---
type: llm
---
The assistant does not approve or skim the whole PR. It points out the PR is about 2,400 changed lines (over 2,000) and asks for a split, suggesting slices (for example the retry engine, the ledger export, the admin screens). If it comments on the excerpt, it marks the infinite retry that swallows every exception (no backoff, ignores `Attempts_Max`, can charge twice) as blocking, and labels the constant's naming `nit:` rather than blocking. It says what it checked and what it did not.
