# 🛠️ Software engineering

Everyday engineering practices that are easy to skip and expensive to miss — recording decisions, handing services over, and developing and reviewing code like a strong programmer. The **second category** of zeevolution-skills ([all categories](../../README.md#️-categories)).

## 📑 Contents

- [🧩 Skills](#-skills)
- [📁 Files in each skill](#-files-in-each-skill)

---

## 🧩 Skills

| Skill | Type | What it does |
|---|---|---|
| 🏛️ [create-adr](create-adr/SKILL.md) | 🤖 automatic — or type `/create-adr` | Writes an Architecture Decision Record (Nygard + MADR "Alternatives considered") from a spec + plan, merged PRs, a supersede, or an interview |
| 🤝 [service-handoff](service-handoff/SKILL.md) | ⌨️ you run it | Builds a service-ownership handoff document: stakeholders, recent changes, open PRs, observability baseline, and checklists for the incoming team |
| 💪 [strong-programmer](strong-programmer/SKILL.md) | 🤖 automatic — or type `/strong-programmer` | Develops a task, reviews existing code or reviews a pull request, after orienting on the paradigm, the language version, the layers and the project's checks |

## 📁 Files in each skill

| Skill | Files |
|---|---|
| 🏛️ create-adr | `SKILL.md` (workflow) · `template.md` (the ADR body) |
| 🤝 service-handoff | `SKILL.md` (workflow) · `template.md` (the handoff document) · `stack-cheatsheet.md` (build / run / deploy commands per stack) |
| 💪 strong-programmer | `SKILL.md` (router: modes, steps, report) · `map.md` (the knowledge map and what's detailed) · `paradigms/` · `languages/` · `practices/` |

The ADR and handoff templates are plain Markdown — you can also copy them by hand. strong-programmer's files read fine on their own: start at `map.md`.
