# 🛠️ Software engineering

> 🛠️ **Category: software engineering** · two skills for recording decisions and handing services over. [All categories →](../README.md)

## 📑 Contents

- [🏛️ /create-adr](#️-create-adr)
- [🤝 /service-handoff](#-service-handoff)
- [✋ Without AI](#-without-ai)

---

## 🏛️ /create-adr

Writes one durable **Architecture Decision Record** — the *why* behind a technical decision, readable years later.

| | |
|---|---|
| 📐 **Format** | Nygard (Title, Status, Context, Decision, Consequences) + MADR's **Alternatives considered** |
| 🔀 **Four ways in** | **compress** a shipped spec + plan · **from-pr** (one PR or a stack) · **free-prompt** (an interview) · **supersede** an older ADR |
| 💬 **Always asks first** | The input mode and the destination folder — it never guesses a location |
| ✂️ **Stays short** | Size budget (~2,500 tokens), names only 1–2 "anchor" classes, leaves the *how* to the code |
| 🧹 **Safe cleanup** | Asks before deleting compressed sources; optionally updates `mkdocs.yaml` |

```text
/create-adr
```

## 🤝 /service-handoff

Builds a **service-ownership handoff** — for a new team, or a fresh agent session — as a Markdown document with actionable checklists.

| | |
|---|---|
| 🧭 **Any scope** | One service, several services, or a whole domain across repos (backend, frontend, mobile, libraries, infra, alerts, data) |
| 💬 **Interviews you first** | Handoff type, outgoing and incoming owners, docs, decisions, risks, on-call, channels |
| 🔎 **Reads the repos** | Ownership files, recent changes (themed, not raw logs), open PRs — via local clones or the `gh` CLI |
| 📈 **Observability baseline** | Traffic, errors, latency, alerts and on-call — from observability tools when available, otherwise marked TBD |
| ✅ **Checklists** | Incoming-owner checklist, learning plan, per-repo ownership-transfer PRs |

```text
/service-handoff What will the next owner focus on?
```

> [!TIP]
> Want the handoff as a Google Doc or Word file? Ask for it — the skill hands the Markdown to **cloud-workspace**, which creates the document or falls back to a `.docx` / paste guide.

## ✋ Without AI

Both templates are plain Markdown you can copy into your docs tool:

- 🏛️ [ADR template](../../skills/software-engineering/create-adr/template.md)
- 🤝 [Handoff template](../../skills/software-engineering/service-handoff/template.md) · [Stack cheat-sheet](../../skills/software-engineering/service-handoff/stack-cheatsheet.md)
