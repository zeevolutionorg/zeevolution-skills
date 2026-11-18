# Manual usage — no AI needed

Build a complete Career Hub by hand in **about 20–30 minutes**, in Google Workspace or Microsoft 365. Once you keep a master copy, each new person takes **about 10 minutes**.

[Português (Brasil)](MANUAL.pt-BR.md)

## 1. Download the Manual Kit

From the latest [Release](https://github.com/zeevolution/zeevolution-skills/releases), download `career-management-kit-en.zip` (or `-pt-BR`) and unzip it.

| Folder | What's inside | Use it for |
|---|---|---|
| `markdown/` | The templates as `.md` text | Google Docs (paste or import), Notion, Confluence, Obsidian |
| `word/` | The same templates as `.docx` | Word / OneDrive / SharePoint, or upload to Google Drive |
| `sheets/` | `05 - 🪜 Ladder Assessment.xlsx`, the designed spreadsheet | Excel or Google Sheets. **Never re-create it from text.** |
| `START-HERE.pdf` | One page with these steps | Everyone |

**Which documents to copy**

- **Your own career (self mode):** 00 Career Hub, 01 1:1 Notes, 02 Growth Plan **and** 04 Focus Plan (copy both; choose one later), 03 Brag Document, 05 Ladder Assessment.
- **Someone you lead (lead mode):** 00 to 06. Add **07 Evidence Doc** only if a level is at risk, and **08 Onboarding Plan** only for someone new to the team.

> The **Growth Plan** and the **Focus Plan** are alternatives: you'll use one, not both. Both start with a banner explaining this; choose together in the first 1:1 or Career Check.

## 2. Path 1 — Google Workspace (Docs, Sheets, Drive)

1. **Create the folder.** In Google Drive: **New › New folder** → `Career Hub — <Person name>`. In lead mode, share it only with the person.
2. **Create the documents.** Pick one way:
   - **Upload (fastest):** drag every file from `word/` into the folder. Right-click each file › **Open with › Google Docs**, then **File › Save as Google Docs**, and delete the uploaded original. Tip: turn on Drive **Settings › Convert uploads** and every upload becomes a Google Doc automatically.
   - **Copy and paste:** in any Google Doc, turn on **Tools › Preferences › Enable Markdown** (once). Create a blank document, open the `.md` file in a text editor (or on GitHub with the **Raw** button), copy everything, then right-click in the doc › **Paste from Markdown**. Rename the document to match the file name.
3. **Create the Ladder Assessment.** Upload `sheets/05 - 🪜 Ladder Assessment.xlsx`, then right-click › **Open with › Google Sheets** (or let Convert uploads do it). Dropdowns, formulas and colors come along. Fill **only the yellow cells**.
4. **Replace the placeholders.** In each document: **Edit › Find and replace** (Ctrl/Cmd + Shift + H). Replace each of: `{{person_name}}`, `{{leader_name}}`, `{{role}}`, `{{discipline}}`, `{{level}}`, `{{next_level}}`, `{{start_date}}`, `{{next_meeting_date}}`, `{{cycle}}`, `{{ladder_source}}`. Finish by searching `{{` to make sure nothing is left (the `{{doc_link_…}}` ones are handled in the next step).
5. **Link everything from the Hub.** Open each document, **Share › Copy link**, and put the link on its row in the Career Hub's documents table (select the document name › Insert link). In every document, point the **← Back to Career Hub** link at the Hub.
6. **Choose the career ladder.** Have your company's? Paste it into the spreadsheet's **🪜 Ladder** tab (levels down column A, pillars across row 4) and set **Career ladder** to *Company ladder* on the Assessment tab. Don't have one? Keep the generic ladder; the banner reminds you to revisit it at the next Career Check.
7. **Book the bi-weekly.** In Google Calendar, create a recurring 1:1 **every 2 weeks** with the Hub link in the description, as the Hub's top block recommends.

## 3. Path 2 — Microsoft 365 (Word, Excel, OneDrive / SharePoint)

1. **Create the folder.** In OneDrive or SharePoint: **+ Add new › Folder** → `Career Hub — <Person name>`. In lead mode, share it only with the person.
2. **Create the documents.** Upload every file from `word/` (drag and drop, or **Upload › Files**). They open directly in Word for the web or desktop; nothing to convert. Use the `.docx` files, not the `.md` ones: Word's Markdown support is still partial.
3. **Create the Ladder Assessment.** Upload `sheets/05 - 🪜 Ladder Assessment.xlsx`. It opens in Excel with everything working. Fill **only the yellow cells**.
4. **Replace the placeholders.** In each document: **Home › Replace** (Ctrl + H, or Cmd + Shift + H on Mac). Same list as in Google step 4, then search `{{` to check nothing is left.
5. **Link everything from the Hub.** In OneDrive, select each file › **Copy link**, then put it on its row in the Career Hub table. Point each document's **← Back to Career Hub** link at the Hub.
6. **Choose the career ladder.** Same as Google step 6, in Excel's **🪜 Ladder** tab.
7. **Book the bi-weekly.** In Outlook, create a recurring 1:1 **every 2 weeks** with the Hub link in the body.

## 4. Path 3 — Other tools (Notion, Confluence, Obsidian, plain files)

Import or paste the `.md` files directly; most of these tools read Markdown. Keep the `.xlsx` in a shared drive and link it from the Hub. Steps 4–7 (placeholders, links, ladder, bi-weekly) are the same.

## 5. Make it reusable: a master copy

1. Follow Path 1 or 2 once **without** replacing the placeholders. Name the folder `Career Hub — TEMPLATE`.
2. For each new person: **Google:** right-click each file › **Make a copy** into the new folder. **Microsoft:** select the files › **Copy to** › the new folder.
3. Then do only steps 4–7 — about 10 minutes per person.

## 6. Keeping your copies up to date

Templates improve over time. [CHANGELOG.md](../CHANGELOG.md) lists, for each release, which documents changed and how, so you can update your master copy by hand. Hubs already in use are never affected.

## 7. After the hub exists

The **Career Hub** is the central page. Every two weeks:

1. Open the Hub and walk the status table.
2. Run the 1:1 in the 1:1 Notes (reflection → feedback → actions).
3. Update one development document (the chosen plan, the Brag, or the Ladder Assessment).
4. Update statuses and "last reviewed" dates in the Hub.

Once a quarter, the first bi-weekly is the **Career Check**. Once a cycle, review the Ladder Assessment and the Performance Review together.
