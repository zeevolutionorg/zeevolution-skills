# Installation

Pick **one** install per machine. Then run `/setup-zeevolution-skills` once.

## Claude Code

```text
/plugin marketplace add zeevolution/zeevolution-skills
/plugin install zeevolution-skills@zeevolution
```

The plugin includes every skill. Update with `/plugin marketplace update zeevolution`.

**To create documents in Google:** configure a Google Drive MCP server in Claude Code. **In Microsoft 365:** a OneDrive/SharePoint MCP server that can upload files. Without either, the skills use the **Files fallback** (below).

## Claude app, Claude Desktop, Cowork

1. Download the `.skill` files from the latest [Release](https://github.com/zeevolution/zeevolution-skills/releases) (or `zeevolution-skills-all-skills.zip`, which contains all of them).
2. In the app's settings, open **Skills** (under Capabilities) and upload each `.skill` file. `career-hub-toolkit.skill` works on its own; adding all six gives the agent the shared rules too.
3. Enable the **Google Drive** connector to create documents in Google. For Microsoft 365, enable a connector that can **write** to OneDrive/SharePoint; read-only connectors fall back to files.

## Cursor

Cursor reads the same `SKILL.md` files.

- **Option A — GitHub import:** open **Customize**, choose **From GitHub Repository**, enter `zeevolution/zeevolution-skills`, then **Install** (user or project scope). The repo ships `.cursor-plugin/marketplace.json` for this.
- **Option B — command line:** `npx skills@latest add zeevolution/zeevolution-skills -a cursor`
- **Option C — manual:** copy the `skills/` folder into `~/.cursor/skills/` (all projects) or `.cursor/skills/` (one project). Category folders are fine; Cursor finds every `SKILL.md`.
- **Teams:** an admin can import the repo as a team marketplace (Dashboard → Plugins & MCPs) and set the plugin to Default Off or Default On.

Run a skill by typing `/` in Agent chat and picking it. User-invoked skills (`/setup-zeevolution-skills`, `/career-hub-toolkit`) only run when you type them.

**To create documents:** add a Google Drive or Microsoft 365 MCP server in Cursor's MCP settings; otherwise the Files fallback is used (Cursor runs the scripts locally).

**Duplicates:** Cursor also loads skills from `~/.claude/skills/`. If you copied these skills there for Claude Code, don't install them for Cursor too.

## Other agents

```bash
npx skills@latest add zeevolution/zeevolution-skills -a <agent>
```

## Files fallback — requirements

When no Drive / OneDrive tool can write, skills create real `.docx` and `.xlsx` files locally. Needs:

```bash
python3 -m pip install -r requirements.txt   # openpyxl, python-docx, pyyaml
```

The files open in Word and Excel, and convert to Google Docs / Sheets when uploaded to Drive (**Settings › Convert uploads**, or right-click › **Open with**).

## Manual fallback — no requirements

If the agent has no connector, can't write files or can't run Python, the skills give you **filled-in Markdown documents** (as files, or one code block per document in the chat) and a **HOW-TO-PASTE** guide for Google Docs, Word, Notion and Confluence. You can also ask for this directly: "just give me the documents to paste".

## Without AI

No install needed: download a Manual Kit from the Releases page and follow [MANUAL.md](MANUAL.md).
