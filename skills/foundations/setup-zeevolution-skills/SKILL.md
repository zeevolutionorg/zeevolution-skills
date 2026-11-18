---
name: setup-zeevolution-skills
description: One-time setup for zeevolution-skills. Asks six questions (name, discipline, where to create documents, folder, language, default career ladder) and saves the answers so every other skill stops asking them. Run once per user, or again to change defaults.
disable-model-invocation: true
---

# Setup — zeevolution-skills

Run once. Saves defaults that every zeevolution skill reads before asking anything.

## 1. Detect what's available

Before asking, check the session's tools:

- **Google:** any Google Drive / Docs / Sheets tool (connector or MCP server) that can create files.
- **Microsoft:** any OneDrive / SharePoint / Word / Excel tool that can create files.
- **Files:** a filesystem plus Python (`python3` with `openpyxl`, `python-docx`, `pyyaml`). If those packages are missing, install them (`pip install openpyxl python-docx pyyaml`).
- **Manual:** always available — filled-in Markdown the user copies and pastes into Google Docs or Word.

Use the result as the default for question S3. Never claim a platform works if its tool isn't there.

## 2. Ask the questions (exact wording)

Ask in the user's language (English or Brazilian Portuguese). Use the agent's question tool when it has one, in **two batches** (S1–S3, then S4–S6). Every question has a default; "Not sure" means the default.

| # | Question | Options | Default |
|---|---|---|---|
| S1 | "What's your name, as it should appear in the documents?" | Free text | — (required) |
| S2 | "What's your discipline?" | Engineering · Data Science · Design · Product Management · Other (type it) | Engineering |
| S3 | "Where should documents be created?" | Google Workspace (Docs/Sheets/Drive) · Microsoft 365 (Word/Excel/OneDrive) · Files I upload myself (.docx/.xlsx) · Markdown I copy and paste myself | Detected in step 1; Files if the agent can write files and run Python, otherwise Markdown |
| S4 | "In which folder should new documents go? Paste a folder link or name, or leave empty to create 'zeevolution-skills' at the root." | Free text / link | Create `zeevolution-skills/` |
| S5 | "Which language should documents use?" | English · Português (Brasil) | Language of the conversation |
| S6 | "Does your company have a career ladder you'd like to reuse by default? (You can still change it per person.)" | Yes, I'll share it now · Not now · We don't have one | Not now |

pt-BR wording for each question lives in `../../career-management/career-hub-toolkit/INTERVIEW.md` (section A).

If S6 = "Yes", run the **career-ladder** skill now and save the resulting ladder as the default.

## 3. Save the defaults

Save this object (JSON):

```json
{
  "user_name": "…",
  "discipline": "Engineering",
  "platform": "google | microsoft | files | manual",
  "root_folder": "link or name",
  "lang": "en | pt-BR",
  "default_ladder": null,
  "saved_at": "YYYY-MM-DD"
}
```

Where to save, first option that works:

1. **Filesystem available:** `~/.config/zeevolution-skills/config.json` (create the folder). Save a default ladder next to it as `ladder.yaml`.
2. **Cloud only:** a small document named `⚙️ zeevolution-skills settings` inside the root folder, containing the JSON in a code block.
3. **Agent memory**, if the agent has a memory feature.
4. Otherwise, tell the user the settings can't be saved here and will be asked again next time.

## 4. Confirm

Show the saved values in one short table and say where they were saved. Then suggest the next step: `/career-hub-toolkit me` (your own career) or `/career-hub-toolkit <name>` (someone you lead).

## Rules

- Never store anything about other people here. Only the user's own defaults.
- Never send these settings anywhere except the user's own filesystem, workspace or agent memory.
