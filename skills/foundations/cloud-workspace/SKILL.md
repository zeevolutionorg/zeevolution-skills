---
name: cloud-workspace
description: Create folders, documents and spreadsheets in the user's workspace (Google Workspace, Microsoft 365, or local .docx/.xlsx files) from zeevolution-skills templates, and link them together. Use whenever a zeevolution skill needs to write documents or sheets for the user.
---

# Cloud workspace

Shared building block: turns rendered templates into real files in the user's workspace. Any skill that produces documents calls this instead of handling platforms itself.

## Pick the adapter

Use the platform saved by `setup-zeevolution-skills` (or the one the user named). Then confirm the tools are really there:

| Platform | Adapter | Needs |
|---|---|---|
| Google Workspace | [GOOGLE.md](GOOGLE.md) | A Google Drive tool that can create files (Claude connector or an MCP server in Claude Code / Cursor) |
| Microsoft 365 | [MICROSOFT.md](MICROSOFT.md) | A OneDrive / SharePoint tool that can create files |
| Files | [FILES.md](FILES.md) | A filesystem and `python3` with `openpyxl`, `python-docx`, `pyyaml` |

If the chosen platform's tool is missing or can't write, **say so in one line and fall back to Files**. Never pretend a file was created.

## Rendering (same for every adapter)

Templates are Markdown with `{{placeholders}}` (rules in the **doc-templates** skill). Spreadsheets are YAML sheet specs (see [SHEETS.md](SHEETS.md)).

```bash
# document → .docx (also .html or .md)
python3 scripts/render_doc.py --in TEMPLATE.md --out OUT.docx --context context.json

# sheet spec → formatted .xlsx
python3 scripts/build_sheet.py --spec SPEC.sheet.yaml --strings STRINGS.yaml \
  --ladder LADDER.yaml --context context.json --out OUT.xlsx
```

Paths are relative to this skill's folder (in Claude Code: `${CLAUDE_SKILL_DIR}/scripts/…`). Skills that bundle their own copy of these scripts (e.g. career-hub-toolkit) use their copy.

`context.json` holds the placeholder values. Unknown placeholders render empty; pass `--keep-missing` to keep them (manual kits).

## Linking documents together

Documents point to each other (a hub links to every doc; every doc links back to the hub). Links only exist after files are created, so:

1. **Reserve the hub first:** create the hub document empty to get its link.
2. **Create every other document** with the hub link in the context (`doc_link_hub`).
3. **Fill the hub last**, with all the links collected in step 2, by replacing the empty hub's content.

If the adapter can't update a document after creating it, create the other documents first (their back-link to the hub stays as plain text "← Back to Career Hub"), then create the hub with all links, and tell the user to paste the hub link into the back-links. Files adapter: link by relative file name.

## Folder and names

- One folder per subject, e.g. `Career Hub — Ana Souza`, inside the user's root folder.
- File names: the document title without the person's name, e.g. `🚀 Career Hub`, `🎶 1:1 Notes`, so the folder reads cleanly.
- If a folder with the same name already exists, **stop and ask** (add missing docs / create a new folder next to it / cancel). Never overwrite.

## Privacy

- Write only to the user's own workspace. Never upload content to any other service.
- Don't share files unless the user asks. In a people-leadership context, remind the user to share the folder only with the person concerned.
