# 🛠️ Software engineering

> 🛠️ **Category: software engineering** · three skills: recording decisions, handing services over, developing and reviewing code. [All categories →](../README.md)

## 📑 Contents

- [🏛️ /create-adr](#️-create-adr)
- [🤝 /service-handoff](#-service-handoff)
- [💪 strong-programmer](#-strong-programmer)
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

## 💪 strong-programmer

Develops a task, reviews existing code or reviews a pull request — and orients itself before it judges or writes anything.

| | |
|---|---|
| 🧭 **Orients first** | Language and version, the paradigm and approach the code is written in, the layers, the project's checks and CI |
| 🔀 **Three modes** | `develop` · `review-code` · `review-pr` |
| 🗺️ **Knowledge map** | Paradigms → approaches → topics, with languages across them and practices for any paradigm ([map](../../skills/software-engineering/strong-programmer/map.md)) |
| 📏 **Pull-request habits** | Small, sliced, stacked at most 3 or 4 deep, opened as drafts, described for a reviewer with no context; reviews that block only on must-fix items |
| ✅ **Validates its own work** | Runs what CI runs, follows the PR's checks to green, and says what it couldn't run |

It steps in on its own when you ask for a review or an implementation. You can also call it:

```text
/strong-programmer review PR #123
```

### What it knows today

| Area | Status |
|---|---|
| Paradigms and the six approaches | 🌱 imperative and declarative overview, and how to recognize each approach; 🔜 each approach's fundamentals |
| Object-oriented: principles, smells, pattern misuse, DDD building blocks | 🔜 |
| Design patterns (the 23 GoF patterns) | 🔜 |
| Kotlin and Java | 🌱 the approaches each supports, and version detection |
| Pull requests, validating your work | ✅ |
| Tidy First | 🔜 short rule in the router |
| Layers and hexagonal architecture | 🔜 short rule in the router |

✅ detailed · 🌱 fundamentals only · 🔜 planned

In a 🔜 area the skill still works from general knowledge, and lists the area under **Not covered yet** in its report.

## ✋ Without AI

The templates are plain Markdown you can copy into your docs tool:

- 🏛️ [ADR template](../../skills/software-engineering/create-adr/template.md)
- 🤝 [Handoff template](../../skills/software-engineering/service-handoff/template.md) · [Stack cheat-sheet](../../skills/software-engineering/service-handoff/stack-cheatsheet.md)
- 💪 [strong-programmer knowledge map](../../skills/software-engineering/strong-programmer/map.md) — what the skill knows, with a link to every file
