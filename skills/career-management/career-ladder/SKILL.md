---
name: career-ladder
description: Get a career ladder into the standard shape used by zeevolution-skills (levels x pillars with expectations). Maps a ladder the user pastes, links or uploads. Pillar names differ by company and are filled in after the documents are generated. Use whenever a career document needs current/next level expectations.
---

# Career ladder

A career ladder is **optional**. Every career document works without one; with one, expectations become specific to the user's company.

## Output shape

Always produce this YAML (same shape as `assets/generic-ladder.<lang>.yaml`):

```yaml
source: company        # or: generic
pillars:               # 3 to 6, in the company's order
  - name: "…"
    meaning: "one sentence"
levels:                # 2 to 10, from most junior to most senior
  - name: "…"          # the company's own level name, e.g. "L3", "Senior", "Designer II"
    expectations:      # one per pillar, same order as pillars
      - "…"
```

Save it next to the person's documents only if the user wants (it's the company's content, it stays in the user's workspace). **Never** write a user's ladder into this repository.

## Flow (exact questions)

Ask in the user's language. Wording for pt-BR is in `../career-hub-toolkit/INTERVIEW.md` (section D).

**L1** — "Do you have a career ladder for this role?"
Options: Paste the text · Share a link to a doc · Upload a file · No ladder yet. Default: No ladder yet.

### If the user provides a ladder

1. Read it (pasted text, the linked document through the workspace tools, or the uploaded file).
2. Find the **pillars** (also called dimensions, competencies, areas, axes) and the **levels** (also called bands, grades, steps, titles).
3. For each level × pillar, write the expectation **in the ladder's own words**: shorten to one or two sentences if it's long, but don't reinterpret it.
4. If the ladder has more than 6 pillars, group related ones and tell the user which you grouped. If it has more than 10 levels, keep the 10 closest to the person's current level.
5. If a cell is missing in the source, leave it empty; don't invent it.

**L2** — "Here's how I mapped it: {n} levels × {m} pillars ({pillar names}). Does this look right?"
Options: Looks right · Fix pillars · Fix levels. On a fix, ask what to change, apply it, and ask L2 again.

### If there's no ladder

**L3** — "Pillars differ by company, so I won't fill them in. After the documents are generated, replace the pillar rows with your company's career ladder. OK?"
Options: OK · Let me share a ladder instead.

Do not copy pillar names into the person's documents. `assets/generic-ladder.<lang>.yaml` and [GENERIC-LADDER.md](GENERIC-LADDER.md) only show the levels × pillars shape. Then:

- Leave the pillar rows blank. Set `ladder_source` to "Generic ladder" (localized) so the spreadsheet banner asks to replace it after the documents are generated.
- Do not pass that sample ladder to `build_sheet.py`.

## Feeding the documents

- **Company ladder:** pass the YAML with `--ladder` to `build_sheet.py`; it fills the 🪜 Ladder tab and the expectations update automatically by level. Copy the current and next level expectations into the Growth Plan, Performance Review, Evidence Doc and Onboarding Plan.
- **No company ladder yet:** leave those sections blank. The documents say to replace the pillars after they are generated.
