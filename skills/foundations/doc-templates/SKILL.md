---
name: doc-templates
description: Rules for zeevolution-skills document templates - placeholder syntax, the "What it is / How to use / Example" tip anatomy, self vs lead wording, language selection and how to render. Use when filling, writing or editing any zeevolution-skills template.
---

# Doc templates

Every zeevolution document template follows these rules, so a person who never saw the toolkit can open any document and know what to do.

## Markdown subset

Templates use only: headings `#`–`####`, paragraphs, `**bold**`, `*italic*`, `` `code` ``, `[links](url)`, bullet / numbered / checkbox (`- [ ]`) lists with 2-space nesting, pipe tables, `>` callouts, and `---` rules. This subset renders the same in Google Docs ("Paste from Markdown"), Word (via `.docx`), Notion and Confluence.

## Placeholders

`{{snake_case}}` only. Shared names (reuse them; don't invent synonyms):

| Placeholder | Meaning |
|---|---|
| `{{person_name}}` | The person the document is about |
| `{{leader_name}}` | Their leader / manager (self mode: the user's manager or mentor) |
| `{{role}}`, `{{discipline}}` | Role title and discipline |
| `{{level}}`, `{{next_level}}` | Current and next career level |
| `{{start_date}}`, `{{created_date}}` | When it starts / when the doc was generated |
| `{{next_meeting_date}}` | Next recurring meeting |
| `{{cycle}}` | Period, e.g. `2027 H1` |
| `{{ladder_source}}` | "Company ladder" or "Generic ladder" (localized) |
| `{{doc_link_<doc>}}` | Link to a sibling document: `hub`, `one_on_one`, `growth_plan`, `focus_plan`, `brag`, `ladder`, `review`, `evidence`, `onboarding` |

When rendering for a person, **every** placeholder must be filled or deliberately left empty. After rendering, search for `{{`: anything left is a bug, except in manual kits.

## Tip anatomy (callouts)

Callouts start with an emoji that sets their meaning and color:

| Emoji | Use | Rule |
|---|---|---|
| ℹ️ | **What this is** — at the top of every document: what, who fills it, when | Exactly one per document, right after the title |
| 💡 | **How to use** — under a section | Imperative, one to three sentences |
| ✍️ | **Example** — under a tip | Practical, fictional, labeled with a discipline: `Example (Design):` |
| 🗓️ | **Rhythm** — when to meet / review | Used in the hub |
| ⚠️ | **Banner** — something to decide or be careful about | e.g. "Choose one: Growth Plan or Focus Plan" |

Examples rotate across Engineering, Data Science, Design and Product. When rendering for one person, you **may** swap an example for one from their discipline using the **disciplines** skill, but never remove the tip itself.

## Self mode vs lead mode

Templates are written for **lead mode** (a leader and a person). In **self mode** (the user builds their own hub):

- `{{person_name}}` = the user; `{{leader_name}}` = their manager or mentor's name, or the user's own name if they have neither.
- Keep the structure. Where a sentence only makes sense for a leader writing about someone else, rephrase it in the first person ("I", "my manager"). Do this only in the rendered copy, never in the template files.
- In the hub's rhythm block, "Owner of the invite" is the user.

## Languages

Templates live in `templates/<category>/<lang>/` (`en`, `pt-BR`). Both versions must have the same headings, tables, callouts and placeholders. Pick the user's language from setup; otherwise the conversation's language.

## Rendering

Use the **cloud-workspace** skill's scripts (`render_doc.py` for documents, `build_sheet.py` for sheets). Don't hand-convert Markdown to another format.

## Writing new templates

1. Start with the title line (emoji + name + `— {{person_name}}`), then `[← Back to Career Hub]({{doc_link_hub}})` if it belongs to a hub, then the ℹ️ callout.
2. Every section a person must fill gets a 💡 and at least one ✍️.
3. Fictional people, companies and products only. No real employer names, internal tools or org units, ever.
4. Write the `en` and `pt-BR` versions together and run `scripts/check_parity.py`.
