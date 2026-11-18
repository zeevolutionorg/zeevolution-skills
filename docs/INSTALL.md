# 📦 Installation

Install **zeevolution-skills** in your agent, then run `/setup-zeevolution-skills` once.

> [!IMPORTANT]
> **Pick one install per machine.** Cursor also loads skills from `~/.claude/skills/`, so installing the same skills twice shows every skill twice.

## 📑 Contents

- [🗺️ Which install is for me?](#️-which-install-is-for-me)
- [🟠 Claude Code](#-claude-code)
- [🟠 Claude app, Desktop and Cowork](#-claude-app-desktop-and-cowork)
- [⚫ Cursor](#-cursor)
- [🧩 Other agents](#-other-agents)
- [🔌 Creating documents: connectors and fallbacks](#-creating-documents-connectors-and-fallbacks)
- [⚙️ After installing](#️-after-installing)
- [🛟 Troubleshooting](#-troubleshooting)

---

## 🗺️ Which install is for me?

| You use | Go to | Updates |
|---|---|---|
| Claude in the terminal | [🟠 Claude Code](#-claude-code) | Automatic via the marketplace |
| Claude in the browser, desktop app or Cowork | [🟠 Claude app](#-claude-app-desktop-and-cowork) | Re-upload new `.skill` files |
| Cursor (IDE, Agent window, CLI) | [⚫ Cursor](#-cursor) | Automatic with GitHub import |
| Codex, Copilot, Windsurf, OpenCode… | [🧩 Other agents](#-other-agents) | `npx skills update` |
| No AI at all | [✋ MANUAL.md](MANUAL.md) | Download the new Manual Kit |

## 🟠 Claude Code

```text
/plugin marketplace add zeevolution/zeevolution-skills
/plugin install zeevolution-skills@zeevolution
```

- ✅ The plugin includes every skill.
- 🔄 Update with `/plugin marketplace update zeevolution`.

## 🟠 Claude app, Desktop and Cowork

1. ⬇️ Download the `.skill` files from the latest [Release](https://github.com/zeevolution/zeevolution-skills/releases) — or `zeevolution-skills-all-skills.zip`, which contains all of them.
2. ⬆️ In the app's settings, open **Skills** (under Capabilities) and upload each `.skill` file.
3. 🔌 Enable the **Google Drive** connector to create documents in Google. For Microsoft 365, enable a connector that can **write** to OneDrive or SharePoint.

> [!TIP]
> `career-hub-toolkit.skill` works on its own. Adding all six gives the agent the shared rules too.

## ⚫ Cursor

Cursor reads the same `SKILL.md` files. Choose one option:

| Option | How | Best for |
|---|---|---|
| **A · GitHub import** | **Customize** → **From GitHub Repository** → `zeevolution/zeevolution-skills` → **Install** (user or project scope) | Most people — updates automatically |
| **B · Command line** | `npx skills@latest add zeevolution/zeevolution-skills -a cursor` | Editable copies in your project |
| **C · Manual** | Copy `skills/` into `~/.cursor/skills/` (all projects) or `.cursor/skills/` (one project) | Offline or locked-down machines |
| **D · Team** | An admin imports the repo as a team marketplace (**Dashboard → Plugins & MCPs**) and sets it to *Default Off* or *Default On* | Teams and Enterprise plans |

- ⌨️ Run a skill by typing `/` in Agent chat and picking it.
- 🔒 User-invoked skills (`/setup-zeevolution-skills`, `/career-hub-toolkit`) only run when you type them.

## 🧩 Other agents

```bash
npx skills@latest add zeevolution/zeevolution-skills -a <agent>
```

## 🔌 Creating documents: connectors and fallbacks

The skills always end with something usable, in this order:

| # | Path | Needs | Result |
|---|---|---|---|
| 1 | 🔗 **Connector / MCP** | A Google Drive or Microsoft 365 tool that can **write** (connector in the Claude app; MCP server in Claude Code or Cursor) | Documents created in your workspace |
| 2 | 📁 **Files** | A filesystem + Python with `openpyxl`, `python-docx`, `pyyaml` | `.docx` / `.xlsx` that open in Word and Excel and convert to Google Docs / Sheets on upload |
| 3 | 📋 **Manual** | Nothing | Filled-in Markdown documents + a **HOW-TO-PASTE** guide, as files or one code block per document in the chat |

**📁 Files requirements**

```bash
python3 -m pip install -r requirements.txt   # openpyxl, python-docx, pyyaml
```

> [!NOTE]
> On Google Drive, turn on **Settings › Convert uploads** (or right-click › **Open with**) so uploaded files become Google Docs and Sheets.

**📋 Manual on purpose:** you can always ask for it — *"just give me the documents to paste"*.

## ⚙️ After installing

1. Run **`/setup-zeevolution-skills`** once (six quick questions, saved for next time).
2. Run **`/career-hub-toolkit me`** or **`/career-hub-toolkit <name>`**.
3. Open the **Career Hub** and book a **bi-weekly 1:1** with it in the invite.

## 🛟 Troubleshooting

| Symptom | Fix |
|---|---|
| 👯 Every skill appears twice | You installed twice (e.g. Claude Code copy in `~/.claude/skills/` + Cursor plugin). Remove one. |
| 🚫 "No Google Drive tool" | Enable the connector (Claude app) or add a Google Drive MCP server (Claude Code / Cursor). Meanwhile the skill falls back to Files or Manual. |
| 📖 Microsoft connector is read-only | Expected for many connectors in v0.1: the Files fallback gives you `.docx` / `.xlsx` to upload. |
| 🐍 `ModuleNotFoundError: openpyxl` | `python3 -m pip install -r requirements.txt`, or let the skill use the Manual fallback. |
| ⌨️ `/career-hub-toolkit` doesn't appear | Restart the agent after installing; in Cursor check **Customize → Skills**. |
