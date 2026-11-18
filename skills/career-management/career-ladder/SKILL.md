---
name: career-ladder
description: Get a career ladder into the standard shape used by zeevolution-skills (levels x pillars with expectations). Maps a ladder the user pastes, links or uploads; or falls back to the original generic ladder, clearly marked as generic. Use whenever a career document needs current/next level expectations.
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
Options: Paste the text · Share a link to a doc · Upload a file · No ladder, use the generic one. Default: generic.

### If the user provides a ladder

1. Read it (pasted text, the linked document through the workspace tools, or the uploaded file).
2. Find the **pillars** (also called dimensions, competencies, areas, axes) and the **levels** (also called bands, grades, steps, titles).
3. For each level × pillar, write the expectation **in the ladder's own words**: shorten to one or two sentences if it's long, but don't reinterpret it.
4. If the ladder has more than 6 pillars, group related ones and tell the user which you grouped. If it has more than 10 levels, keep the 10 closest to the person's current level.
5. If a cell is missing in the source, leave it empty; don't invent it.

**L2** — "Here's how I mapped it: {n} levels × {m} pillars ({pillar names}). Does this look right?"
Options: Looks right · Fix pillars · Fix levels. On a fix, ask what to change, apply it, and ask L2 again.

### If there's no ladder

**L3** — "I'll use a generic ladder with 4 pillars (Impact, Craft, Direction, Collaboration & Leadership). It's marked as generic so you can replace it at the next Career Check. OK?"
Options: OK · Let me share a ladder instead.

Use `assets/generic-ladder.<lang>.yaml` (`en` or `pt-BR`). The human-readable version is [GENERIC-LADDER.md](GENERIC-LADDER.md). Then:

- Set `ladder_source` to "Generic ladder" (localized). The documents and the spreadsheet show a banner asking to replace it later.
- Map the person's level to the closest generic stage only if the user agrees; otherwise ask: "Which of these stages is closest to the current level: Learning, Contributing, Owning, Leading, Shaping?"

## Feeding the documents

- **Ladder Assessment sheet:** pass the YAML with `--ladder` to `build_sheet.py`; it fills the 🪜 Ladder tab and the expectations update automatically by level.
- **Growth Plan, Performance Review, Evidence Doc, Onboarding Plan:** copy the current and next level expectations into the "Level" / "What the level expects" sections.
