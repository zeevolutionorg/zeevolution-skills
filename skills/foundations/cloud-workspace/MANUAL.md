# Adapter — Manual (copy & paste)

The last fallback, and the one that always works: when the agent has **no Google / Microsoft connector or MCP server**, or **can't write files or run Python**, give the user **filled-in Markdown documents** and a **paste guide**. The user creates the documents in Google Docs or Word themselves, in about 15–20 minutes.

Use it also when the user asks for it ("just give me the files", "I'll paste them myself").

## Steps

1. **Tell the user why**, in one line: e.g. "There's no Google Drive tool in this session, so I'll prepare the documents for you to paste."
2. **Fill the placeholders** in each template (`{{person_name}}`, `{{leader_name}}`, `{{role}}`, …) with the values from the interview. Plain text replacement is enough; with Python available you can use `scripts/render_doc.py --in T.md --out OUT.md --context context.json`.
   - **Links** (`{{doc_link_…}}`): the documents don't exist yet, so leave each link as the **document's file name** (e.g. `01 - 🎶 1:1 Notes.md`). The paste guide tells the user to swap them for real links.
   - Leave nothing else as `{{…}}`. Unknown values become empty.
3. **Deliver the documents** — pick the first that works:
   - **Agent can write files:** one folder `Career Hub — <name>/` with one `.md` per document, numbered (`00 - 🚀 Career Hub.md`, `01 - 🎶 1:1 Notes.md`, …), plus `HOW-TO-PASTE.md` rendered from `assets/paste-guide.<lang>.md`. Zip it if the agent can.
   - **Chat only:** send each document as its **own fenced Markdown block** (` ```markdown `), one message per document, titled with its file name. Send the paste guide first.
4. **The spreadsheet (Ladder Assessment):**
   - If Python is available, also build the `.xlsx` with `scripts/build_sheet.py` (Files adapter) — it's the best version.
   - Otherwise include the **text fallback** (`05-ladder-assessment.md`, filled in) and tell the user they can download the ready-made spreadsheet from the repository's Releases (Manual Kit → `sheets/`).
5. **Give the paste guide** for the user's platform (from `assets/paste-guide.<lang>.md`), with the folder name and the document list filled in.
6. **End with the same report** as the other adapters: the rhythm (bi-weekly 1:1 with the Hub in the invite) and the first actions.

## Rules

- Same documents, same order, same rules as the other adapters — only the delivery changes.
- The Hub is still the central piece: put it first in the list and say "start with the Hub".
- Don't paste personal data anywhere else than the user's own chat or files.
- In chat, never merge two documents in one code block: the user copies them one at a time.
