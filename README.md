<div align="center">

<p align="center">
  <img src="assets/logo.svg" alt="zeevolution-skills logo: a Z drawn as a rising staircase between code brackets" width="112" height="112">
</p>

<h1 align="center">Skills for Technologists</h1>

**zeevolution-skills** · small, composable agent skills for engineers, data scientists, designers and product managers

*Built from my experience leading and growing technologists.*

[![License: MIT](assets/badges/license-mit.svg)](LICENSE)
[![Claude skills](assets/badges/claude.svg)](docs/INSTALL.md#-claude-code)
[![Cursor skills](assets/badges/cursor.svg)](docs/INSTALL.md#-cursor)
[![Docs: EN and pt-BR](assets/badges/docs-languages.svg)](docs/README.md)
<!-- Add once the repo is public:
[![CI](https://github.com/zeevolution/zeevolution-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/zeevolution/zeevolution-skills/actions/workflows/ci.yml)
-->

</div>

> [!TIP]
> **A growing library, organized by category.** Each category packages one area of a technologist's work into skills you can run with an agent — or copy by hand. **🌱 Career management** is the first category, available now. **More categories are on the way.**

---

## 📑 Contents

- [🧭 How the library is organized](#-how-the-library-is-organized)
- [✨ What every skill gives you](#-what-every-skill-gives-you)
- [🚀 Quick start](#-quick-start)
- [📦 Install](#-install)
- [🔌 No connector? Still works](#-no-connector-still-works)
- [🗂️ Categories](#️-categories)
  - [🌱 Career management](#-career-management)
  - [🔭 Coming soon](#-coming-soon)
  - [🧱 Foundations](#-foundations)
- [✋ Without AI](#-without-ai)
- [✅ Quality](#-quality)
- [📚 Documentation](#-documentation)
- [⚖️ License](#️-license)

---

## 🧭 How the library is organized

```text
zeevolution-skills
├── 🌱 career-management     ← available now
├── 🔭 …next category        ← coming soon
├── 🔭 …and more             ← coming soon
└── 🧱 foundations           ← shared by every category: setup, documents, sheets, languages, disciplines
```

| Category | What it covers | Status |
|---|---|---|
| 🌱 **[Career management](#-career-management)** | Managing a career — your own, or the people you lead | ✅ **Available** (v0.1) |
| 🔭 **[More categories](#-coming-soon)** | Other aspects of a technologist's work | ⏳ **Coming soon** |
| 🧱 **[Foundations](#-foundations)** | Shared building blocks every category uses | ✅ Available |

Every category follows the same pattern: **one `*-toolkit` skill** that sets up its documents in one command, then **working skills** on top — all built on the same foundations.

## ✨ What every skill gives you

| | |
|---|---|
| 🤖 **Claude and Cursor** | Same skill files, two install paths, plus any agent that reads `SKILL.md` |
| ✋ **Works without AI** | Every document ships as a template you can copy into Google Docs or Word |
| 🔌 **Always delivers** | Connector → files → Markdown to paste: you always end with something usable |
| 🧭 **Self-explanatory documents** | Every section says *what it is*, *how to use it*, and shows a practical *example* |
| 🎨 **Any discipline** | Wording and examples for engineering, data science, design and product |
| 🌎 **Two languages** | English and Brazilian Portuguese, kept structurally identical by CI |

## 🚀 Quick start

1. 📦 **Install** in your agent — see [📦 Install](#-install).
2. ⚙️ **Set up once** — run **`/setup-zeevolution-skills`**: your name, discipline, where documents go and language. Every category reuses these answers.
3. 🗂️ **Pick a category and run its toolkit** — today that's **🌱 career management**: `/career-hub-toolkit me` for your own career, or `/career-hub-toolkit Ana Souza, Data Scientist L3` for someone you lead.

## 📦 Install

| You use | Install | 📄 Google docs need | 📄 Microsoft 365 docs need |
|---|---|---|---|
| 🟠 **Claude Code** | `/plugin marketplace add zeevolution/zeevolution-skills` then `/plugin install zeevolution-skills@zeevolution` | A Google Drive MCP server | A Microsoft 365 MCP server that can write |
| 🟠 **Claude app / Desktop / Cowork** | Download the `.skill` files from [Releases](https://github.com/zeevolution/zeevolution-skills/releases) and add them in the app's Skills settings | Google Drive connector | Microsoft 365 connector with write access |
| ⚫ **Cursor** | Customize → **From GitHub Repository** → `zeevolution/zeevolution-skills`, or `npx skills@latest add zeevolution/zeevolution-skills -a cursor` | A Google Drive MCP server | A Microsoft 365 MCP server |
| 🧩 **Other agents** | `npx skills@latest add zeevolution/zeevolution-skills -a <agent>` | Agent-specific | Agent-specific |
| ✋ **No AI** | Download a category's Manual Kit from [Releases](https://github.com/zeevolution/zeevolution-skills/releases) | — | — |

> [!IMPORTANT]
> **Pick one install per machine.** Cursor also reads `~/.claude/skills/`, so installing the same skills twice shows every skill twice. One install brings **every category** — new ones arrive with updates.

➡️ Step-by-step for every agent: **[docs/INSTALL.md](docs/INSTALL.md)**

## 🔌 No connector? Still works

Every skill that creates documents ends with something you can use, in this order:

| # | Path | When | You get |
|---|---|---|---|
| 1 | 🔗 **Connector / MCP** | A Google or Microsoft tool that can write | Documents created directly in your workspace |
| 2 | 📁 **Files** | The agent can write files and run Python | Real `.docx` / `.xlsx` that open in Word and Excel and convert to Google Docs / Sheets on upload |
| 3 | 📋 **Manual** | Anything else — needs nothing | Filled-in **Markdown** documents + a **HOW-TO-PASTE** guide for Google Docs, Word, Notion or Confluence, as files or straight in the chat |

## 🗂️ Categories

> [!NOTE]
> **User-invoked** skills (⌨️) run only when you type them — they orchestrate. **Model-invoked** skills (🤖) can also be picked up by the agent when the task fits — they hold reusable rules.

### 🌱 Career management

> ✅ **Available now** · managing a career — your own (**self mode**) or someone you lead (**lead mode**)

**What you get:** one command, `/career-hub-toolkit`, builds a full **career hub** — Career Hub, 1:1 Notes, Growth Plan *or* Focus Plan, Brag Document, an automated Ladder Assessment spreadsheet, Performance Review, and optional Evidence Doc and 30/60/90 Onboarding Plan. The **Career Hub** is the central page, and a **bi-weekly 1:1** keeps everything moving.

| Skill | Type | What it does |
|---|---|---|
| 🚀 [career-hub-toolkit](skills/career-management/career-hub-toolkit/SKILL.md) | ⌨️ user | One command builds the Career Hub and every career document, in self or lead mode |
| 🪜 [career-ladder](skills/career-management/career-ladder/SKILL.md) | 🤖 model | Maps a company career ladder into levels × pillars, or falls back to the generic ladder |

<details>
<summary>💡 <b>Why this category exists</b></summary>

- 📉 **Careers get managed in bursts.** Most career conversations happen once a year, the week before reviews. **✅ The fix:** one Career Hub page that links everything, a bi-weekly 1:1 that walks it for ten minutes, specific feedback (**SBI**), growth tied to **real upcoming work** (an "arena"), and evidence logged as it happens (the **Brag Document**).
- 📄 **Templates nobody understands don't get used.** **✅ The fix:** every section says *what it is*, *how to use it*, and shows a practical *example*.
- 🪜 **Every company's ladder is different.** **✅ The fix:** the career ladder is **optional** — share yours and it's mapped to levels × pillars, or use a generic one, clearly marked.

</details>

📘 **Docs:** [what the toolkit creates and asks](docs/career-management/career-hub-toolkit.md) · ✋ [manual guide](docs/MANUAL.md) · [guia em português](docs/MANUAL.pt-BR.md)

### 🔭 Coming soon

> ⏳ **More categories are on the way.**

Career management is the first of several categories. New ones are added when a practice proves worth packaging — each with its own `*-toolkit` skill, its own templates and a Manual Kit, built on the same foundations.

| | |
|---|---|
| 👀 **Follow along** | Watch the repository's releases and the [CHANGELOG](CHANGELOG.md) |
| 💬 **Suggest one** | Open an issue with the **Idea** template: tell us the practice you repeat and how you do it today |
| 🛠️ **Build one** | [CONTRIBUTING → Adding a category](CONTRIBUTING.md#️-adding-a-category) |

### 🧱 Foundations

> ✅ **Available** · shared building blocks every category uses — new categories get them for free

| Skill | Type | What it does |
|---|---|---|
| ⚙️ [setup-zeevolution-skills](skills/foundations/setup-zeevolution-skills/SKILL.md) | ⌨️ user | One-time setup: name, discipline, platform, folder, language, default ladder |
| ☁️ [cloud-workspace](skills/foundations/cloud-workspace/SKILL.md) | 🤖 model | Creates and links documents and spreadsheets in Google, Microsoft 365, as files, or as Markdown to paste |
| 📝 [doc-templates](skills/foundations/doc-templates/SKILL.md) | 🤖 model | Placeholders, the "what / how / example" tip anatomy, self vs lead wording, languages |
| 🎨 [disciplines](skills/foundations/disciplines/SKILL.md) | 🤖 model | Vocabulary and examples for engineering, data science, design and product |

## ✋ Without AI

Every category ships a **Manual Kit** per language in each release: its templates as Markdown and Word files, its spreadsheets, and a one-page START-HERE.

| Category | Kit | First time | Guides |
|---|---|---|---|
| 🌱 Career management | `career-management-kit-en.zip` · `career-management-kit-pt-BR.zip` | ⏱️ 20–30 min (≈10 min per next person) | [English](docs/MANUAL.md) · [Português](docs/MANUAL.pt-BR.md) |
| 🔭 Next categories | ⏳ coming soon | — | — |

## ✅ Quality

Every pull request runs lint, consistency checks, ~390 unit / contract / e2e tests that mirror the repo layout, real spreadsheet formula recalculation, a leak check and a secret scan — and, on demand, behavioral evals of the skills. New categories plug into the same pipeline. ➡️ [docs/TESTING.md](docs/TESTING.md)

## 📚 Documentation

➡️ Full map: **[docs/README.md](docs/README.md)**

| Group | Docs |
|---|---|
| 🚦 **Getting started** | 📦 [Install](docs/INSTALL.md) · 📖 [Glossary](GLOSSARY.md) |
| 🌱 **Career management** | 🚀 [career-hub-toolkit](docs/career-management/career-hub-toolkit.md) · ✋ [Manual](docs/MANUAL.md) · [pt-BR](docs/MANUAL.pt-BR.md) |
| 🔭 **Next categories** | ⏳ Coming soon |
| 🧱 **Foundations** | 🧩 [Foundations docs](docs/foundations/README.md) |
| 🛠️ **Contributing & internals** | 🤝 [Contributing](CONTRIBUTING.md) · 🧪 [Testing](docs/TESTING.md) · 🏛️ [Decisions](docs/adr/README.md) · 🎯 [Evals](evals/README.md) · 📝 [Changelog](CHANGELOG.md) · 🙏 [Credits](CREDITS.md) |

## ⚖️ License

[MIT](LICENSE) — skills, scripts and templates. Use them, adapt them, make them yours. 💙
