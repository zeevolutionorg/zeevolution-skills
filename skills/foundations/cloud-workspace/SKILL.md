---
name: cloud-workspace
description: Create folders, documents and spreadsheets in the user's workspace (Google Workspace, Microsoft 365, local .docx/.xlsx files, or filled-in Markdown to copy and paste when no connector is available) from zeevolution-skills templates, and link them together. Use whenever a zeevolution skill needs to write documents or sheets for the user.
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
| Manual (copy & paste) | [MANUAL.md](MANUAL.md) | Nothing. Works in every agent, even with no connector, no filesystem and no Python |

### Fallback order

Always end with something the user can use. Go down this list until one works, and **say in one line why you moved down**:

1. **Connector / MCP** for the chosen platform (Google or Microsoft) that can write.
2. **Files** — real `.docx` / `.xlsx`, if the agent can write files and run Python.
3. **Manual** — filled-in Markdown files (or Markdown in the chat, if there's no filesystem) plus a step-by-step paste guide for Google Docs or Word.

The user can also ask for **Manual** directly ("just give me the files to paste"). Never pretend a file was created.

## Rendering (same for every adapter)

Templates are Markdown with `{{placeholders}}` (rules in the **doc-templates** skill). Spreadsheets are YAML sheet specs (see [SHEETS.md](SHEETS.md)).

```bash
# document → .docx (also .html or .md)
python3 scripts/render_doc.py --in TEMPLATE.md --out OUT.docx --context context.json

# whole bundle (Files or Manual adapter): every document, links, hub last
python3 scripts/make_bundle.py --bundle BUNDLE.yaml --templates TEMPLATES_DIR --lang en \
  --mode lead --format files|manual --context context.json --out OUT_DIR

# sheet spec → formatted .xlsx
python3 scripts/build_sheet.py --spec SPEC.sheet.yaml --strings STRINGS.yaml \
  --ladder LADDER.yaml --context context.json --out OUT.xlsx
```

No Python? The **Manual** adapter fills placeholders by plain text replacement, which the agent can do itself.

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
