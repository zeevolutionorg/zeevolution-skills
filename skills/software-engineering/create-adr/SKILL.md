---
name: create-adr
description: Author or compress Architecture Decision Records (ADRs) using the Nygard ADR Markdown template extended with MADR's "Alternatives considered" section. Use when the user asks to create an ADR, compress a `.specify` spec + plan into an ADR, supersede an existing ADR, summarize a merged PR / stack of PRs as an ADR, or mentions "ADR", "architecture decision record", "decision log", or "compress spec to ADR". Always asks the engineer first for (1) the input mode and (2) the destination folder; never assumes a default location.
---

# create-adr

Produce a single, durable **Architecture Decision Record** in the chosen folder, following:

- **Base structure:** [Nygard ADR — Markdown rendering](https://github.com/architecture-decision-record/architecture-decision-record/blob/main/architecture-decision-record.github.io/src/content/locales/en-us/templates/decision-record-template-by-michael-nygard.md) (Title, Status, Context, Decision, Consequences).
- **Alternatives considered:** [MADR 4.0.0 — full template](https://github.com/adr/madr/blob/4.0.0/template/adr-template.md?plain=1).
- **Catalogue:** [adr.github.io/adr-templates](https://adr.github.io/adr-templates/) (browse if a future ADR needs a different shape, e.g. Y-Statement).

The fully rendered template lives in [`template.md`](template.md) next to this file — read it when generating the ADR body.

## Hard rules

1. **Always ask, never guess.** Ask the **input mode** and the **destination folder** before touching any file. Use the agent's question tool if it has one (e.g. Claude's question dialog, Cursor's ask-questions tool); otherwise ask conversationally.
2. **No silent deletes.** In `compress` mode, list the source files you will delete and ask for confirmation before doing it.
3. **mkdocs.yaml is optional.** Only update it after the file is written and the user confirms.
4. **Stay self-contained.** Once written, the ADR must not link to files that the same flow is about to delete; inline whatever is necessary (esp. `Alternatives considered`).
5. **Defer implementation to code.** An ADR records the **why**, not the **how**. Concrete wiring (Spring beans, exception classes, HTTP statuses, config keys, IRSA scoping, test names) lives in code; the ADR should name **at most one or two anchor classes** that lead the reader into the right place — the rest is a one-line pointer back to the code and the **Related artifacts** PRs.
6. **Respect the size budget.** See [§ Size budget](#size-budget) below. If you exceed it, cut implementation detail first — never cut Context, Alternatives, or Consequences.

## Size budget

ADRs are read by humans (often years later, often during incidents). Long ADRs go unread.

| Slice | Target | Soft cap | Action if exceeded |
|-------|--------|----------|---------------------|
| **Narrative body** (Context + Alternatives + Decision + Consequences + References + Changelog, excluding tables) | ~1500 tokens | **2000 tokens** | Cut implementation detail; replace bullet lists describing code mechanics with a one-line pointer + 1–2 anchor class names. |
| **Reference tables** (Related artifacts, Supported regions, Mitigations matrix) | as needed | — | Tables are reference data; don't trim for budget — trim for relevance. |
| **Whole file** | ~2500 tokens | **4000 tokens** | If both the narrative and tables push past 4000 tokens, split: keep the ADR focused on the decision, and move overflow into a sibling doc (e.g. `<NNN>-multi-region-storage-runbook.md`) referenced from the ADR. |

Use `wc -c <file> | awk '{print $1/4}'` for a quick approximate token count (≈ 4 chars/token).

### The "anchor classes" pattern

When the Decision touches code, name only the **1–2 classes that anchor the design** — typically:

- the request/DTO that carries the new option (write path), and
- the persisted column / domain entity that materialises it (read path).

**Good — names anchors, leaves the rest to code:**

> We make the file-storage adapter region-aware by routing every object-storage operation through clients keyed by `Region`, with the region read from:
>
> - **`UploadRequest.region`** on **writes**, and
> - the persisted **`StoredFile.region`** column on **reads**.
>
> Concrete wiring (dependency-injection setup, the `region` metric tag, the `UnsupportedRegionException`, startup validation, cloud permission scoping, local emulator parity) — read the code; the PRs in **Related artifacts** link the exact diffs.

**Bad — restates code as prose:**

> 1. Add a `StorageProperties` config class with a `Map<Region, RegionConfig>`...
> 2. `RegionClientsConfig` produces three clients keyed by `Region`...
> 3. `BlobStorageAdapter` swaps three singletons for three maps...
> 4. ... (10 bullets total)

If you find yourself listing more than 2–3 class names, or writing bullets that describe how the code is structured, cut them. Code is the source of truth for the "how".

## Workflow

Create a task list (the agent's to-do / task tool, if it has one) with one item per phase and update it as you go:

```text
1. Pick input mode (compress | from-pr | free-prompt | supersede)
2. Pick destination folder + ADR number
3. Gather mode-specific inputs
4. Draft and write the ADR
5. Mode-specific cleanup
6. (Optional) Update mkdocs.yaml
7. Summarize and hand off
```

### Phase 1 — Pick input mode

Ask the engineer which form they want, presenting **all** four modes:

| Mode | Use when |
|------|----------|
| **`compress`** | An existing `.specify/specs/<name>.md` + `.specify/plans/<name>.md` pair represents work that has now shipped. Skill compresses both into one ADR and deletes the sources. |
| **`from-pr`** | A merged PR (or stack) represents the decision. Skill fetches metadata via `gh pr view`, summarises the decision, and includes the PRs in a **Related artifacts** table. |
| **`free-prompt`** | No spec/plan/PR exists yet — the engineer wants to dictate Context / Decision / Consequences interactively. |
| **`supersede`** | Replaces an existing ADR. Creates the new ADR and flips the previous one's **Status** to `Superseded by ADR-NNN`. |

### Phase 2 — Pick destination folder + ADR number

Ask the engineer for the destination folder. **Never assume.** Helpful suggestions (offer, don't dictate):

- **Monorepos:** a per-service folder is common, e.g. `docs/<service>/adrs/` or `services/<service>/docs/adr/`. Look for existing ADR folders first (see [§ Discovering repo conventions](#discovering-repo-conventions-helper-checklist)).
- **Other repos:** `docs/adr/` is the most common; some teams use `architecture/decisions/` (adr-tools default).
- **If the folder doesn't exist:** offer to scaffold it with a short `README.md`: what ADRs are, the template used (Nygard + MADR "Alternatives considered"), the lifecycle (Proposed → Accepted → Superseded), and a table listing each ADR.

Then determine the next number:

- List `*.md` files in the folder.
- Detect the highest `NNN-` or `NNNN-` prefix.
- Use the same width (3-digit if the folder uses 3, 4-digit if 4). Default to **3-digit zero-padded** for new folders.
- Confirm with the engineer: `Next ADR will be NNN-<kebab-slug>.md — confirm or override.`

### Phase 3 — Mode-specific input gathering

#### `compress`

1. Ask which spec + plan files to compress (offer a picker showing `.specify/specs/*.md` and `.specify/plans/*.md` that exist).
2. Read both files in full.
3. Extract: problem, constraints, chosen approach, alternatives, consequences, validation/rollout, file change inventory (used for "Related artifacts").
4. Surface anything the spec mentions about **other repos** (Terraform / k8s manifests / IRSA) so the Related artifacts table can be cross-repo.

#### `from-pr`

1. Ask for one or more PR numbers / URLs.
2. For each, run `gh pr view <num> --repo <owner>/<repo> --json title,body,mergedAt,mergeCommit,url,headRefName,baseRefName`.
3. Read PR bodies to extract decision rationale; treat each PR as a candidate row in the **Related artifacts** table (sorted by `mergedAt`).
4. If `gh search prs --owner <owner> --merged "<feature keyword>"` returns related PRs in **other repos**, ask whether to include them.

#### `free-prompt`

Ask, **one question per message**, for:

1. Title (imperative, short).
2. Date decided / date in production (offer "use today" or detect via `git log -1 --format=%cI`).
3. Deciders / Consulted.
4. Context — what problem, what constraints (no longer than ~200 words).
5. Alternatives considered (at least 2 rejected options with pros/cons).
6. Decision — what we chose and why.
7. Consequences — positive, negative, neutral, risks + mitigations.
8. Related artifacts (PRs / runbooks / dashboards).

#### `supersede`

1. Ask which ADR is being superseded (file path).
2. Read it; carry forward Context and the now-obsolete Decision into the new ADR's Context section as "Prior state".
3. The new ADR's Status header should say `Accepted — supersedes ADR-<old>`. A later cleanup step will edit the old ADR.

### Phase 4 — Draft and write

1. Read [`template.md`](template.md) for the exact section ordering and field labels.
2. Render the ADR with:
   - `Status: Accepted — implemented and rolled out to production.` if applicable, or `Status: Proposed` / `Status: Accepted` per context.
   - **`Date in production (approx.)`** — when uncertain, use the merge timestamp of the decisive commit (`git log -1 --format=%cI <commit>`); explicitly note that it's an approximation and how to refine it.
   - **`Related artifacts`** table sorted in **infrastructure-first** rollout order (deployments → infrastructure → app code).
   - **`Alternatives considered`** with at least 2 rejected options, each with Pros / Cons.
   - **`Consequences`** split into Positive / Negative / Mitigations / Neutral.
   - **Decision section follows the [anchor-classes pattern](#the-anchor-classes-pattern):** name at most 1–2 classes that anchor the design (typically the write-path DTO and the read-path persisted column/entity). Everything else collapses into a one-line pointer to the code + the **Related artifacts** PRs.
3. Inline anything that the `compress` step is about to delete (do not leave `[link to spec]` references pointing at soon-to-be-deleted files).
4. Write the file to the destination chosen in Phase 2. If the agent can't write files (chat-only app), deliver the ADR as one fenced ```markdown block and say which path it should be saved to. Write the ADR in the language the repo's existing ADRs use (default: the user's language).
5. After writing, do a quick **self-review pass**:
   - **Token check:** `wc -c <file> | awk '{print $1/4}'`. If narrative body is over 2000 tokens (or whole file over 4000), cut implementation detail per the [§ Size budget](#size-budget) — never cut Context, Alternatives, or Consequences.
   - **Anchor-classes check:** count class/file names referenced in the Decision section. More than 2–3 means you're restating code as prose; collapse the list and add `(read the code; the PRs in Related artifacts link the exact diffs)`.
   - **No-dangling-links check:** every relative link resolves; no `[link to spec]` to files the `compress` step is about to delete.
   - **No-TODO check:** no `<…>`, `TBD`, or `TODO` placeholders left.
   - **Decision clarity check:** the Decision can be paraphrased in one sentence by someone reading only that section. If not, rewrite.

### Phase 5 — Mode-specific cleanup

#### `compress`

1. **Confirm** with the engineer: "I'm about to delete `<spec.md>` and `<plan.md>`. Proceed?"
2. On approval, delete the spec/plan files.
3. Update their parent index READMEs (if they exist):
   - `.specify/specs/README.md` and `.specify/plans/README.md` → replace the deleted file's row in the `Documents` table with a `Former → Superseded by` row pointing at the new ADR. Keep the folder's structure description intact (so it stays ready for future initiatives).
4. Search the repo (`rg` / Grep) for any other file referencing the deleted paths; offer to update them to point at the new ADR.

#### `supersede`

1. Edit the old ADR's frontmatter / header `Status` to `Superseded by ADR-<NNN>` and link to the new file.
2. Append a one-line **Superseded by** entry under the old ADR's `Changelog / Metadata` section (if present).

#### `from-pr` and `free-prompt`

No automatic cleanup; just remind the engineer to commit.

### Phase 6 — (Optional) Update mkdocs.yaml

1. Look for `mkdocs.yaml` (or `mkdocs.yml`) at the **repo root first**, then at the **app root** (e.g. `applications/<svc>/mkdocs.yaml`).
2. Skip this phase silently if no mkdocs file exists. **Ask** the engineer whether to proceed if one does.
3. If proceeding:
   - Locate the app's `nav` block.
   - Find an existing `- ADRs:` subsection. If present, **append** the new entry under it (mirroring nearby siblings, e.g. `- NNN - <Title>: <service>/adrs/<file>.md`).
   - If absent, **insert** an `ADRs:` group with `Overview: …/adrs/README.md` first, then the new ADR.
   - **Indentation matters.** Match the surrounding indentation exactly; copy a neighbouring block as a template if unsure.
4. Run `mkdocs build --strict` (or the repo's equivalent) if available; otherwise print a "you may want to verify" note.

### Phase 7 — Summarize and hand off

Print a final summary:

```text
ADR written:    <path>
Mode:           <mode>
Number:         <NNN>
Deleted:        <list or "none">
mkdocs.yaml:    <updated | skipped | n/a>
Old ADR(s) superseded: <list or "none">
Related artifacts: <count>
```

Then suggest a commit message in the repo's existing style (look at recent commits with `git log --oneline -5`) — usually:

```text
docs(<scope>): add ADR <NNN> for <topic>
```

If the repo has its own PR-creation command or skill, mention it as the next step. Do **not** open the PR automatically.

## Discovering repo conventions (helper checklist)

When working in an unfamiliar repo:

- `find <repo-root> -type d \( -iname adr -o -iname adrs -o -iname decisions \) -not -path '*/node_modules/*'` — locate existing ADR folders.
- `cat <one-existing-adr.md>` — match the numbering width, frontmatter shape, and header style.
- `ls -la <adr-folder>/` and `cat <adr-folder>/README.md` — pick up any README format conventions.
- `git log --oneline -5 -- docs/` — match commit-message style.

## Tooling references

- [`adr.github.io/adr-templates`](https://adr.github.io/adr-templates/) — canonical catalogue (Nygard, MADR, Y-Statement, others).
- [`adr/madr`](https://github.com/adr/madr) — MADR templates and rationale.
- [`architecture-decision-record/architecture-decision-record`](https://github.com/architecture-decision-record/architecture-decision-record) — Nygard Markdown rendering used as the base.

## Anti-patterns to avoid

- **Inventing a default folder.** Always ask. Common conventions are suggestions, not defaults.
- **Linking from the new ADR to files the same flow is about to delete.** Inline the content instead.
- **Re-numbering existing ADRs** to fix gaps. Numbers are monotonically increasing and immutable.
- **Picking a non-Nygard/MADR template** without telling the engineer. If the conversation suggests Y-Statement or ISO/IEC/IEEE 42010, surface that explicitly and confirm.
- **Auto-pushing or auto-PRing.** This skill writes files and leaves the engineer to commit / push / open the PR with their usual flow.
- **Restating code as prose.** A long "Concretely:" list of beans, configs, exceptions, and HTTP status codes belongs in the code (and the PR diffs), not in the ADR. Name 1–2 anchor classes, point at the PRs, stop.
- **Letting the ADR grow past 4000 tokens.** Long ADRs go unread. If you hit the cap, cut implementation detail first; if the decision truly needs more room, split into a sibling document (e.g. `<NNN>-…-runbook.md`).
