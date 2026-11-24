# 📝 Changelog

Each release lists, **per document**, what changed — so people using the templates by hand can update their master copy.

> [!NOTE]
> Hubs already in use are never changed by a release. Only new copies pick up the changes.

## 📑 Contents

- [🏷️ 0.1.0 — 2026-11-23](#️-010--2026-11-23)
  - [✨ Added — skills](#-added--skills)
  - [🔌 Added — delivery and quality](#-added--delivery-and-quality)
  - [📄 Added — documents (career-management)](#-added--documents-career-management)

---

## 🏷️ 0.1.0 — 2026-11-23

First release.

### ✨ Added — skills

- `career-management/career-hub-toolkit` — one command to build a career hub (self mode and lead mode; English and Brazilian Portuguese; Google Workspace, Microsoft 365 or files).
- `career-management/career-ladder` — map a company career ladder into levels × pillars. Pillar names are filled in after the documents are generated.
- `foundations/setup-zeevolution-skills`, `foundations/cloud-workspace`, `foundations/doc-templates`, `foundations/disciplines`.
- **New category — software engineering:** `software-engineering/create-adr` (Architecture Decision Records: compress a spec + plan, from merged PRs, interview, or supersede) and `software-engineering/service-handoff` (service-ownership handoff with interview, repo evaluation, observability baseline and checklists).

### 🔌 Added — delivery and quality

- **Manual fallback**: with no connector, no filesystem or no Python, `/career-hub-toolkit` delivers filled-in Markdown documents plus a HOW-TO-PASTE guide (Google Docs, Word, Notion, Confluence) — as files or in the chat.
- `cloud-workspace/scripts/make_bundle.py` renders a whole hub (Files or Manual) in one command; `templates/career-management/bundle.yaml` lists the documents.
- Test suite mirroring the repository (unit, contract, e2e, LibreOffice formula tests), staged CI, nightly and release workflows, pre-commit.
- Manual Kit file names omit characters Windows cannot store. The 1:1 notes file is `01 - 🎶 1-1 Notes` in English and `01 - 🎶 Notas de 1-1` in Portuguese. The title inside the document stays "1:1".

### 📄 Added — documents (career-management)

- `00 Career Hub` — central page; "meet every two weeks" block; one "Development plan: Growth or Focus" row.
- `01 1:1 Notes` — Working Agreement, bi-weekly 1:1 with SBI status lines, quarterly Career Check with follow-up, Review Conversation.
- `02 Growth Plan` — self-analysis and three moves with rules; alternative to the Focus Plan.
- `03 Brag Document` — goals, quarterly self-assessment, work log.
- `04 Focus Plan` — two-quarter plan; alternative to the Growth Plan.
- `05 Ladder Assessment` — automated spreadsheet (dropdowns, expectations by level, gap and readiness, chart, history) plus a text fallback.
- `06 Performance Review`, `07 Evidence Doc`, `08 Onboarding Plan 30/60/90`.
