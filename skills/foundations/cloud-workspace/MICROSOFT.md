# Adapter — Microsoft 365

## What you need

A tool that can create files in OneDrive or SharePoint:

- **Claude app / Desktop / Cowork:** a Microsoft 365 connector **with write access**.
- **Claude Code / Cursor:** a Microsoft 365 / OneDrive / SharePoint MCP server that can upload files.

Many Microsoft 365 integrations are read-only. **Check that an upload or create operation exists before you start.** If none exists, use the Files adapter ([FILES.md](FILES.md)) and give the user the upload steps below. This fallback is the expected path for v0.1.

## Steps (when a write-capable tool exists)

1. **Folder:** create `Career Hub — <name>` inside the user's root folder (OneDrive or a SharePoint document library).
2. **Documents:** render each template to `.docx` (`scripts/render_doc.py`) and upload it. Word for the web and desktop open `.docx` natively; nothing to convert.
3. **Spreadsheet:** build the `.xlsx` (`scripts/build_sheet.py`) and upload it. Excel opens it with every dropdown, formula, color and chart working.
4. **Links:** collect each file's sharing/open URL (`webUrl`) and follow the linking order in [SKILL.md](SKILL.md).
5. **Hub last:** re-render the hub `.docx` with all links and upload it, replacing the empty placeholder.

## Fallback: Files + upload steps for the user

When there's no write-capable tool:

1. Build the bundle with the Files adapter.
2. Tell the user, in their language:
   - "In OneDrive or SharePoint: **+ Add new › Folder** → `Career Hub — <name>`."
   - "Open the folder and **Upload › Files**: select every file from the bundle."
   - "Open `🚀 Career Hub` and replace each file name in the documents table with the file's link (select the file › **Copy link**)."

## Manual equivalent

See `docs/MANUAL.md` → Path 2 (Microsoft 365).
