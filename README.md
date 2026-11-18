<div align="center">

# 🧰 Skills for Technologists

**zeevolution-skills** · small, composable agent skills for engineers, data scientists, designers and product managers

*Built from my experience leading and growing technologists.*

[![CI](https://github.com/zeevolution/zeevolution-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/zeevolution/zeevolution-skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Claude](https://img.shields.io/badge/Claude-skills-D97757)
![Cursor](https://img.shields.io/badge/Cursor-skills-111111)
![Languages](https://img.shields.io/badge/docs-EN%20%7C%20pt--BR-2ea44f)

</div>

> [!TIP]
> **First up: career management.** `/career-hub-toolkit` builds a complete career hub — for **your own career** or for **someone you lead** — in Google Workspace, Microsoft 365, as `.docx`/`.xlsx` files, or as Markdown to paste. In English or Brazilian Portuguese. And every document also works **without any AI**.

---

## 📑 Contents

- [✨ What you get](#-what-you-get)
- [🚀 Quick start](#-quick-start)
- [📦 Install](#-install)
- [🔌 No connector? Still works](#-no-connector-still-works)
- [💡 Why these skills exist](#-why-these-skills-exist)
- [🗂️ Skills reference](#️-skills-reference)
- [✋ Without AI](#-without-ai)
- [✅ Quality](#-quality)
- [📚 Documentation](#-documentation)
- [⚖️ License](#️-license)

---

## ✨ What you get

| | |
|---|---|
| 🚀 **One command, a full career hub** | Career Hub, 1:1 Notes, Growth Plan *or* Focus Plan, Brag Document, an automated Ladder Assessment spreadsheet, Performance Review, and optional Evidence Doc and 30/60/90 Onboarding Plan |
| 👤 **Self or lead mode** | Manage your own career, or the career of someone you lead |
| 🧭 **Self-explanatory documents** | Every section says *what it is*, *how to use it*, and shows a practical *example* |
| 🪜 **Your ladder, or ours** | Share your company's career ladder, or use a generic one clearly marked as such |
| 🌎 **Two languages** | English and Brazilian Portuguese, kept structurally identical by CI |
| 🤖 **Claude and Cursor** | Same skill files, two install paths, plus any agent that reads `SKILL.md` |

## 🚀 Quick start

1. ⚙️ **Set up once** — run **`/setup-zeevolution-skills`**: your name, discipline, where documents go, language and (optionally) your company's career ladder.
2. 🏗️ **Build a hub** — run **`/career-hub-toolkit me`** for your own career, or **`/career-hub-toolkit Ana Souza, Data Scientist L3`** for someone you lead.
3. 🗓️ **Start the rhythm** — open the **Career Hub** link and book a **bi-weekly 1:1** with the Hub in the invite. That's the rhythm the whole toolkit is built around.

## 📦 Install

| You use | Install | 📄 Google docs need | 📄 Microsoft 365 docs need |
|---|---|---|---|
| 🟠 **Claude Code** | `/plugin marketplace add zeevolution/zeevolution-skills` then `/plugin install zeevolution-skills@zeevolution` | A Google Drive MCP server | A Microsoft 365 MCP server that can write |
| 🟠 **Claude app / Desktop / Cowork** | Download the `.skill` files from [Releases](https://github.com/zeevolution/zeevolution-skills/releases) and add them in the app's Skills settings | Google Drive connector | Microsoft 365 connector with write access |
| ⚫ **Cursor** | Customize → **From GitHub Repository** → `zeevolution/zeevolution-skills`, or `npx skills@latest add zeevolution/zeevolution-skills -a cursor` | A Google Drive MCP server | A Microsoft 365 MCP server |
| 🧩 **Other agents** | `npx skills@latest add zeevolution/zeevolution-skills -a <agent>` | Agent-specific | Agent-specific |
| ✋ **No AI** | Download a Manual Kit from [Releases](https://github.com/zeevolution/zeevolution-skills/releases) | — | — |

> [!IMPORTANT]
> **Pick one install per machine.** Cursor also reads `~/.claude/skills/`, so installing the same skills twice shows every skill twice.

➡️ Step-by-step for every agent: **[docs/INSTALL.md](docs/INSTALL.md)**

## 🔌 No connector? Still works

The skills always end with something you can use, in this order:

| # | Path | When | You get |
|---|---|---|---|
| 1 | 🔗 **Connector / MCP** | A Google or Microsoft tool that can write | Documents created directly in your workspace |
| 2 | 📁 **Files** | The agent can write files and run Python | Real `.docx` / `.xlsx` that open in Word and Excel and convert to Google Docs / Sheets on upload |
| 3 | 📋 **Manual** | Anything else — needs nothing | Filled-in **Markdown** documents + a **HOW-TO-PASTE** guide for Google Docs, Word, Notion or Confluence, as files or straight in the chat |

## 💡 Why these skills exist

### 📉 Careers get managed in bursts

Most career conversations happen once a year, the week before reviews. Evidence is rebuilt from memory, feedback is generic, and the plan written in January is forgotten by March.

**✅ The fix:** a small, steady rhythm. One **Career Hub** page links everything, and a **bi-weekly 1:1** walks it for ten minutes. Feedback is specific (**SBI**: situation, behavior, impact), growth is tied to **real upcoming work** (an "arena"), and evidence is logged as it happens (the **Brag Document**).

### 📄 Templates nobody understands don't get used

A blank "Development Plan" template with five headings gets left blank.

**✅ The fix:** every section of every document says **what it is, how to use it, and shows a practical example** — from engineering, data science, design and product. Someone who never saw the toolkit can open any document and know what to do.

### 🪜 Every company's ladder is different

**✅ The fix:** the career ladder is **optional**. Share yours (paste, link or upload) and the skill maps it to levels × pillars. Don't have one? A generic, discipline-neutral ladder is used and clearly marked, so you can replace it at the next Career Check.

## 🗂️ Skills reference

> [!NOTE]
> **User-invoked** skills run only when you type them — they orchestrate. **Model-invoked** skills can also be picked up by the agent when the task fits — they hold reusable rules.

### 🌱 Career management

| Skill | Type | What it does |
|---|---|---|
| 🚀 [career-hub-toolkit](skills/career-management/career-hub-toolkit/SKILL.md) | ⌨️ user | One command builds the Career Hub and every career document, in self or lead mode |
| 🪜 [career-ladder](skills/career-management/career-ladder/SKILL.md) | 🤖 model | Maps a company career ladder into levels × pillars, or falls back to the generic ladder |

### 🧱 Foundations

Shared building blocks every category uses.

| Skill | Type | What it does |
|---|---|---|
| ⚙️ [setup-zeevolution-skills](skills/foundations/setup-zeevolution-skills/SKILL.md) | ⌨️ user | One-time setup: name, discipline, platform, folder, language, default ladder |
| ☁️ [cloud-workspace](skills/foundations/cloud-workspace/SKILL.md) | 🤖 model | Creates and links documents and spreadsheets in Google, Microsoft 365, as files, or as Markdown to paste |
| 📝 [doc-templates](skills/foundations/doc-templates/SKILL.md) | 🤖 model | Placeholders, the "what / how / example" tip anatomy, self vs lead wording, languages |
| 🎨 [disciplines](skills/foundations/disciplines/SKILL.md) | 🤖 model | Vocabulary and examples for engineering, data science, design and product |

🔭 More categories will come as real, repeated practices prove worth packaging — see [CONTRIBUTING.md](CONTRIBUTING.md#-adding-a-category).

## ✋ Without AI

Every release ships a **Manual Kit** per language with the templates as Markdown and Word files, the Ladder Assessment spreadsheet, and a one-page START-HERE.

| | |
|---|---|
| ⏱️ **First hub** | about 20–30 minutes |
| 🔁 **Each next person** | about 10 minutes, with a master copy |
| 📘 **Guides** | [English](docs/MANUAL.md) · [Português](docs/MANUAL.pt-BR.md) |

## ✅ Quality

Every pull request runs lint, consistency checks, ~390 unit / contract / e2e tests that mirror the repo layout, real spreadsheet formula recalculation, a leak check and a secret scan — and, on demand, behavioral evals of the skills. ➡️ [docs/TESTING.md](docs/TESTING.md)

## 📚 Documentation

| Doc | For |
|---|---|
| 📦 [INSTALL](docs/INSTALL.md) | Installing in Claude, Cursor or other agents |
| ✋ [MANUAL](docs/MANUAL.md) · [pt-BR](docs/MANUAL.pt-BR.md) | Building a hub by hand, no AI |
| 🚀 [career-hub-toolkit](docs/career-management/career-hub-toolkit.md) | What the toolkit creates and asks |
| 🧪 [TESTING](docs/TESTING.md) | Tests, CI/CD and tools |
| 🤝 [CONTRIBUTING](CONTRIBUTING.md) | Changing or adding skills |
| 📖 [GLOSSARY](GLOSSARY.md) | The shared vocabulary |
| 🙏 [CREDITS](CREDITS.md) | Ideas this builds on |
| 📝 [CHANGELOG](CHANGELOG.md) | What changed, per document |
| 🏛️ [Decisions](docs/adr/README.md) | Why the repo is shaped this way |
| 🎯 [Evals](evals/README.md) | Behavioral tests of the skills |

## ⚖️ License

[MIT](LICENSE) — skills, scripts and templates. Use them, adapt them, make them yours. 💙
