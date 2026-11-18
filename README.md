# Skills for Technologists

**zeevolution-skills** — small, composable agent skills for engineers, data scientists, designers and product managers. Built from my experience leading and growing technologists.

They work in **Claude** and **Cursor** (and other agents that read `SKILL.md`), and every document they create also works **without any AI**: copy the templates into Google Docs or Word and go.

> **First up: career management.** `/career-hub-toolkit` builds a complete career hub — for your own career or for someone you lead — in Google Workspace, Microsoft 365 or as `.docx`/`.xlsx` files, in English or Brazilian Portuguese.

---

## Requirements

| You use | Install | To create docs in Google | To create docs in Microsoft 365 |
|---|---|---|---|
| **Claude Code** | `/plugin marketplace add zeevolution/zeevolution-skills` then `/plugin install zeevolution-skills@zeevolution` | A Google Drive MCP server | A Microsoft 365 MCP server that can write, **or** the Files fallback |
| **Claude app / Desktop / Cowork** | Download the `.skill` files from [Releases](https://github.com/zeevolution/zeevolution-skills/releases) and add them in the app's Skills settings | Google Drive connector enabled | Microsoft 365 connector with write access, **or** the Files fallback |
| **Cursor** | Customize → **From GitHub Repository** → `zeevolution/zeevolution-skills` → Install. Or `npx skills@latest add zeevolution/zeevolution-skills -a cursor` | A Google Drive MCP server, **or** the Files fallback | A Microsoft 365 MCP server, **or** the Files fallback |
| **Other agents** | `npx skills@latest add zeevolution/zeevolution-skills -a <agent>` | Agent-specific | Agent-specific |
| **No AI** | Download a Manual Kit from [Releases](https://github.com/zeevolution/zeevolution-skills/releases) and follow [docs/MANUAL.md](docs/MANUAL.md) | — | — |

**No connector? Still works.** The skills always end with something usable, in this order:

1. **Connector / MCP server** (Google or Microsoft) → documents created directly in your workspace.
2. **Files fallback** → real `.docx` / `.xlsx` files, when the agent can write files and run Python (`openpyxl`, `python-docx`, `pyyaml`). They open in Word and Excel and convert to Google Docs / Sheets on upload.
3. **Manual fallback** → filled-in **Markdown documents** plus a **HOW-TO-PASTE** guide, as files or straight in the chat, for you to paste into Google Docs ("Paste from Markdown"), Word, Notion or Confluence. Needs nothing at all.

**Pick one install per machine.** Cursor also reads `~/.claude/skills/`; installing the same skills twice shows every skill twice.

Full details: [docs/INSTALL.md](docs/INSTALL.md).

## Quick start

1. Run **`/setup-zeevolution-skills`** once: your name, discipline, where documents go, language, and (optionally) your company's career ladder.
2. Run **`/career-hub-toolkit me`** for your own career, or **`/career-hub-toolkit Ana Souza, Data Scientist L3`** for someone you lead.
3. Open the **Career Hub** link it gives you. Book a **bi-weekly 1:1** with the Hub in the invite — that's the rhythm the whole toolkit is built around.

## Why these skills exist

### Careers get managed in bursts

Most career conversations happen once a year, the week before reviews. Evidence is rebuilt from memory, feedback is generic, and the plan written in January is forgotten by March.

**The fix** is a small, steady rhythm: one **Career Hub** page that links everything, and a **bi-weekly 1:1** where you walk it for ten minutes. Feedback is specific (**SBI**: situation, behavior, impact), growth is tied to **real upcoming work** (an "arena"), and evidence is logged as it happens (the **Brag Document**).

### Templates nobody understands don't get used

A blank "Development Plan" template with five headings gets left blank.

**The fix:** every section of every document says **what it is, how to use it, and shows a practical example** — from engineering, data science, design and product. Someone who never saw the toolkit can open any document and know what to do.

### Every company's ladder is different

**The fix:** the career ladder is **optional**. Share yours (paste, link or upload) and the skill maps it to levels × pillars. Don't have one? A generic, discipline-neutral ladder is used and clearly marked, so you can replace it at the next Career Check.

## Reference

Skills split on one axis: **user-invoked** skills run only when you type them (they orchestrate); **model-invoked** skills can also be picked up by the agent when the task fits (they hold reusable rules).

### Career management

**User-invoked**

- **[career-hub-toolkit](skills/career-management/career-hub-toolkit/SKILL.md)** — One command to build a career hub: Career Hub, 1:1 Notes, Growth Plan *or* Focus Plan, Brag Document, an automated Ladder Assessment spreadsheet, Performance Review, and optional Evidence Doc and 30/60/90 Onboarding Plan. Self mode or lead mode.

**Model-invoked**

- **[career-ladder](skills/career-management/career-ladder/SKILL.md)** — Map a company career ladder into levels × pillars, or fall back to the generic ladder.

### Foundations

Shared building blocks every category uses.

**User-invoked**

- **[setup-zeevolution-skills](skills/foundations/setup-zeevolution-skills/SKILL.md)** — One-time setup: name, discipline, platform, folder, language, default ladder.

**Model-invoked**

- **[cloud-workspace](skills/foundations/cloud-workspace/SKILL.md)** — Create and link documents and spreadsheets in Google Workspace, Microsoft 365 or as files.
- **[doc-templates](skills/foundations/doc-templates/SKILL.md)** — Placeholders, the "what / how / example" tip anatomy, self vs lead wording, languages.
- **[disciplines](skills/foundations/disciplines/SKILL.md)** — Vocabulary and examples for engineering, data science, design and product.

More categories will come as real, repeated practices prove worth packaging. See [CONTRIBUTING.md](CONTRIBUTING.md) for how a category is added.

## Without AI

Every release ships a **Manual Kit** per language (`career-management-kit-en.zip`, `career-management-kit-pt-BR.zip`) with the templates as Markdown and Word files, the Ladder Assessment spreadsheet, and a one-page START-HERE. Creating a hub by hand takes about 20–30 minutes, and about 10 minutes per person once you keep a master copy. Step-by-step guides for Google and Microsoft: [docs/MANUAL.md](docs/MANUAL.md) · [Português](docs/MANUAL.pt-BR.md).

## Quality

Every pull request runs lint, consistency checks, ~390 unit/contract/e2e tests (mirroring the repo layout), real spreadsheet formula recalculation, a leak check and secret scan — and, on demand, behavioral evals of the skills. See [docs/TESTING.md](docs/TESTING.md).

## License

[MIT](LICENSE) — skills, scripts and templates. Use them, adapt them, make them yours.
