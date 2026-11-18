# Adapter — Files (.docx / .xlsx bundle)

The universal fallback and the default in Cursor or Claude Code when no Drive / OneDrive tool is configured. It produces real files that open in Word and Excel and convert to Google Docs / Sheets on upload.

## What you need

- A filesystem the agent can write to.
- `python3` with `openpyxl`, `python-docx` and `pyyaml`. If missing: `pip install openpyxl python-docx pyyaml` (add `--break-system-packages` on systems that require it).
- **No filesystem, no Python, or the install fails?** Don't stop: use the **Manual** adapter ([MANUAL.md](MANUAL.md)) and give the user filled-in Markdown to paste.

## Steps

1. **Output folder:** `<root>/Career Hub — <name>/` where `<root>` is the saved root folder if it's a local path, otherwise the agent's working/output folder.
2. **Context:** write `context.json` with all placeholder values. For links, use **relative file names**, e.g. `"doc_link_hub": "00 - 🚀 Career Hub.docx"`.
3. **Documents:** `python3 scripts/render_doc.py --in <template>.md --out "<folder>/<NN - title>.docx" --context context.json` for each document.
4. **Spreadsheet:** `python3 scripts/build_sheet.py --spec <spec> --strings <strings> --ladder <ladder> --context context.json --out "<folder>/05 - 🪜 Ladder Assessment.xlsx"`.
5. **Hub last** (it links to all the others).
6. **Optional zip** for easy upload: `<folder>.zip`.
7. Delete `context.json` from the output folder when done (it contains personal data the user didn't ask to keep).

## What to tell the user

- Where the folder is, and that it holds N documents and one spreadsheet.
- **Google:** "Upload the folder to Drive. Turn on Drive **Settings › Convert uploads** first, or right-click each file › **Open with › Google Docs / Google Sheets**."
- **Microsoft:** "Upload the folder to OneDrive or SharePoint; the files open directly in Word and Excel."
- After uploading: "Open the Career Hub and replace each file name in the documents table with the file's link."
