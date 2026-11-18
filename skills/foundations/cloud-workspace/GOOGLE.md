# Adapter — Google Workspace

## What you need

A tool that can create files in Google Drive:

- **Claude app / Desktop / Cowork:** the Google Drive connector, enabled.
- **Claude Code / Cursor:** a Google Drive MCP server configured in the agent's MCP settings.

Tool names differ between connectors. Look for operations like *create file*, *create folder*, *upload*, *update file content*, *copy file*, *get link*.

## Steps

1. **Folder:** create `Career Hub — <name>` (or the subject folder) inside the user's root folder. Keep its id/link.
2. **Documents, preferred path — upload `.docx` with conversion:** render each template to `.docx` (`scripts/render_doc.py`) and upload it with the target type **Google Docs** (`application/vnd.google-apps.document`). Headings, tables, colored tip boxes and links survive the conversion.
3. **Documents, fallback path — HTML or Markdown:** if the tool can't upload binary files but can create a Google Doc from text, render to `.html` (best) or `.md` and create the doc from that content.
4. **Spreadsheet:** build the `.xlsx` (`scripts/build_sheet.py`) and upload it with the target type **Google Sheets** (`application/vnd.google-apps.spreadsheet`). Dropdowns, formulas, colors, frozen rows and the chart carry over. If the tool can only create empty sheets, upload the `.xlsx` as a file and tell the user to open it with **Open with › Google Sheets**.
5. **Links:** collect each file's `webViewLink` (or the equivalent "open" URL) and follow the linking order in [SKILL.md](SKILL.md).
6. **Hub last:** update the reserved hub doc's content with all links. If updating isn't possible, create the hub now and delete the empty placeholder (only if the tool can delete; otherwise tell the user).

## When there's no Google tool

Say so in one line and go down the fallback order in [SKILL.md](SKILL.md): **Files** (`.docx`/`.xlsx` to upload to Drive) if the agent can write files and run Python, otherwise **Manual** ([MANUAL.md](MANUAL.md)): filled-in Markdown plus the "Paste from Markdown" guide.

## Checks before reporting success

- Every file was actually created (you have an id or link for each).
- Opening the hub link shows real links, not `{{doc_link_…}}` text.
- Report only the hub link to the user, plus anything that fell back.

## Manual equivalent

See `docs/MANUAL.md` → Path 1 (Google).
