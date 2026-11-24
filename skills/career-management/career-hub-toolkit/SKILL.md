---
name: career-hub-toolkit
description: One command to build a complete career-management hub - a Career Hub page plus 1:1 Notes, Growth Plan (PDI) or Focus Plan, Brag Document, an automated Ladder Assessment spreadsheet, Performance Review, and optional Evidence Doc and 30/60/90 Onboarding Plan - in Google Workspace, Microsoft 365, as .docx/.xlsx files, or as ready-to-paste Markdown when no connector is available. Works for your own career (self mode) or for someone you lead (lead mode), in English or Brazilian Portuguese.
disable-model-invocation: true
---

# /career-hub-toolkit

Builds a career-management hub for one person, in one go. The **Career Hub** document is the central piece: it lists and links every other document and recommends a **bi-weekly 1:1** to follow them.

```text
/career-hub-toolkit me                                    # self mode: your own career
/career-hub-toolkit Ana Souza, Data Scientist L3, google   # lead mode: someone you lead
```

This skill uses: **cloud-workspace** (create files), **doc-templates** (placeholders and tips), **disciplines** (wording), **career-ladder** (levels × pillars). If those skills aren't installed, everything needed is bundled here under `assets/` and `scripts/`.

## Step 1 — Defaults and arguments

1. Load saved defaults from `/setup-zeevolution-skills` (see that skill for where they're stored). If none exist, run its questions first (S1–S6), or ask only S3 and S5 if the user wants to go fast.
2. Parse the command arguments: `me` → self mode; a name → lead mode; also pick up role, discipline, level and platform words (`google`, `microsoft`, `files`) when present.

## Step 2 — Ask only what's missing

Use the exact questions in [INTERVIEW.md](INTERVIEW.md), sections B, C and D, in the user's language. Skip anything already known. Check for an existing hub for this person **before** the confirmation (question F2).

## Step 3 — Resolve the ladder

Run the **career-ladder** skill (or follow it from `../career-ladder/SKILL.md`). If the user shares a company ladder, map it to YAML and note `ladder_source`. If they don't, leave the pillar rows blank: names differ by company and are filled in after the documents are generated. Do not copy the sample ladder's pillar names into the person's documents.

## Step 4 — Decide the document set

| # | Document | Self mode | Lead mode |
|---|---|---|---|
| 00 | 🚀 Career Hub | ✅ | ✅ |
| 01 | 🎶 1:1 Notes | ✅ (with your manager or mentor) | ✅ |
| 02 | 🌱 Growth Plan | ✅ *(alternative to 04)* | ✅ *(alternative to 04)* |
| 03 | 😎 Brag Document | ✅ | ✅ |
| 04 | 🧭 Focus Plan | ✅ *(alternative to 02)* | ✅ *(alternative to 02)* |
| 05 | 🪜 Ladder Assessment (spreadsheet) | ✅ | ✅ |
| 06 | 📝 Performance Review | — (offer it for a self-review) | ✅ |
| 07 | 🔎 Evidence Doc | — | only if T8 = Yes |
| 08 | 🛬 Onboarding Plan | — | only if T7 = Yes |

**02 and 04 are always both created.** They're alternatives: the person and the leader choose one together in a bi-weekly or Career Check. Both documents open with a banner saying so, and the Hub has a single "Development plan: Growth **or** Focus" row. **Never choose for them.**

For documents not created, set their `doc_link_…` to empty and change their Hub row status to "Not in use".

## Step 5 — Confirm

Show the summary and ask the question in INTERVIEW.md section E. **Nothing is created before "Create".**

## Step 6 — Build the context

Write `context.json` (in a temporary location):

```json
{
  "person_name": "Ana Souza",
  "leader_name": "<user's name, or in self mode the manager/mentor name>",
  "role": "Data Scientist", "discipline": "Data Science",
  "level": "L3", "next_level": "L4",
  "start_date": "2026-11-18", "created_date": "2026-11-18",
  "next_meeting_date": "2026-12-02",
  "cycle": "2027 H1",
  "ladder_source": "Company ladder",
  "ladder_source_label": "Company ladder",
  "lang": "en",
  "doc_link_hub": "", "doc_link_one_on_one": "", "doc_link_growth_plan": "",
  "doc_link_focus_plan": "", "doc_link_brag": "", "doc_link_ladder": "",
  "doc_link_review": "", "doc_link_evidence": "", "doc_link_onboarding": ""
}
```

- Dates in the user's locale format inside documents (e.g. `Dec 2, 2026` / `2 dez. 2026`).
- `cycle`: the current half (`2027 H1` / `2027 S1`) unless the user said otherwise.
- `ladder_source` / `ladder_source_label`: localized "Company ladder" / "Generic ladder" (pt-BR: "Trilha da empresa" / "Trilha genérica").
- Self mode: apply the self-mode wording rules from **doc-templates** to the rendered copies.

## Step 7 — Create the files

Follow **cloud-workspace** (or the copies in `scripts/`), with the adapter for the chosen platform. **If that platform's connector / MCP server isn't available or can't write, say so in one line and go down the fallback order:**

1. **Connector / MCP** (Google or Microsoft) → the steps below.
2. **Files** — the agent can write files and run Python → `.docx` / `.xlsx` bundle, same steps with relative file links.
3. **Manual** — anything else (no connector, no filesystem or no Python) → **filled-in Markdown to copy and paste**; see "Manual mode" below.

**Shortcut when Python is available** (Files and Manual): one command renders the whole bundle, links included, hub last:

```bash
python3 scripts/make_bundle.py --bundle assets/templates/bundle.yaml --templates assets/templates \
  --lang <lang> --mode <self|lead> --format <files|manual> --context context.json \
  --ladder <ladder.yaml> --include <evidence,onboarding> \
  --paste-guide assets/paste-guide.<lang>.md --out "<folder>"
```

Connector / Files steps:

1. Create the folder: `Career Hub — {person_name}` (pt-BR: `Hub de Carreira — {person_name}`) in the root folder.
2. **Reserve the Hub:** create it empty to get its link → `doc_link_hub`.
3. Render and create documents 01–04 and 06–08 from `assets/templates/<lang>/NN-*.md` with `scripts/render_doc.py`. Collect each link into the context.
4. Build the Ladder Assessment with `scripts/build_sheet.py`:

   ```bash
   python3 scripts/build_sheet.py \
     --spec assets/templates/05-ladder-assessment.sheet.yaml \
     --strings assets/templates/<lang>/05-ladder-assessment.strings.yaml \
     --ladder <ladder.yaml> --context context.json --out "05 - 🪜 Ladder Assessment.xlsx"
   ```

   Upload/convert it as a spreadsheet (Google Sheets or Excel). Collect its link.
5. **Fill the Hub last** from `assets/templates/<lang>/00-career-hub.md` with every link, replacing the reserved empty Hub.
6. Check: no `{{` left in any created document; every link opens.

File names inside the folder (keep the number prefix so they sort):

| # | English | Português (Brasil) |
|---|---|---|
| 00 | 🚀 Career Hub | 🚀 Hub de Carreira |
| 01 | 🎶 1:1 Notes | 🎶 Notas de 1:1 |
| 02 | 🌱 Growth Plan | 🌱 PDI |
| 03 | 😎 Brag Document | 😎 Brag Document |
| 04 | 🧭 Focus Plan | 🧭 Plano de Foco |
| 05 | 🪜 Ladder Assessment | 🪜 Avaliação de Trilha |
| 06 | 📝 Performance Review | 📝 Avaliação de Desempenho |
| 07 | 🔎 Evidence Doc | 🔎 Documento de Evidências |
| 08 | 🛬 Onboarding Plan | 🛬 Plano de Onboarding |

### Manual mode (no connector available)

Same documents, same order, same interview — only the delivery changes ([cloud-workspace › MANUAL.md](../../foundations/cloud-workspace/MANUAL.md)):

1. Fill every placeholder in `assets/templates/<lang>/NN-*.md` (plain text replacement is enough). Use each document's **file name** as its link, e.g. `doc_link_one_on_one` → `01 - 🎶 1-1 Notes.md`. A colon in "1:1" is written as a hyphen in the file name so the file can be saved on Windows.
2. Fill `assets/paste-guide.<lang>.md` with `{{folder_name}}` = `Career Hub — {person_name}` and `{{doc_list}}` = a numbered list of the documents, the Hub first.
3. **Can write files:** create the folder with `HOW-TO-PASTE.md` plus one `.md` per document (`00 - 🚀 Career Hub.md`, …). **Chat only:** send the paste guide first, then **one fenced ```markdown block per document**, each titled with its file name.
4. Spreadsheet: if Python is available build the `.xlsx` anyway; otherwise include the filled text fallback (`05-…md`) and point to the Manual Kit spreadsheet in the repository Releases.
5. Then report back as below (instead of a Hub link: "start with `00 - 🚀 Career Hub`").

## Step 8 — Report back

Keep it short:

1. **The Hub link** — the only link you give; everything else is reachable from it. (Manual mode: where the files are, or "the documents are above", and to start with the Hub and the paste guide.)
2. What still needs filling after generation (e.g. "career ladder pillars — replace with your company's", "role left blank").
3. **The rhythm:** "The Hub recommends a **bi-weekly 1:1** to follow up on these documents." If the agent has calendar tools, ask question F1 (offer to create the recurring event with the Hub linked). Never book without a yes.
4. **First actions:** run the Working Agreement in the first 1:1; schedule the Career Check; choose together between the Growth Plan and the Focus Plan.

## Rules

- Personal data: the documents are about a real person. Write only to the user's own workspace; don't keep `context.json` after the run; don't share files unless asked. In lead mode, remind the user to share the folder only with the person.
- Never invent ladder content, levels or evidence. Leave a field empty rather than guess.
- Never overwrite an existing hub (question F2 decides).
- If a platform tool fails halfway, stop, list what was created, and offer to finish with the Files adapter.
