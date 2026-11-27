# Knowledge map

What `strong-programmer` knows and how deep. Open a node only when the task needs it.

**Status:** ✅ detailed · 🌱 fundamentals only · 🔜 planned (no file yet — work from general knowledge and say so in the report) · — not applicable

## Paradigms and approaches

- 🌱 [Programming paradigms](paradigms/README.md) — imperative vs declarative, and how to tell which approach code is written in
  - 🌱 [Imperative](paradigms/imperative/README.md) — say *how*, step by step, changing state
    - 🔜 Procedural
    - 🔜 Object-oriented
      - 🔜 Principles: GoF principles, SOLID
      - 🔜 Code smells
      - 🔜 Pattern misuse
      - 🔜 Domain-driven design building blocks
      - 🔜 Design patterns: creational, structural, behavioral
    - 🔜 Parallel
  - 🌱 [Declarative](paradigms/declarative/README.md) — say *what* you want; the runtime decides how
    - 🔜 Logic
    - 🔜 Functional
    - 🔜 Database

## Languages

- 🌱 [Language registry and version detection](languages/README.md)

| Language | Procedural | Object-oriented | Parallel | Logic | Functional | Database |
|---|---|---|---|---|---|---|
| 🌱 [Kotlin](languages/kotlin/README.md) | 🌱 | 🌱 | 🌱 | — | 🌱 | — |
| 🌱 [Java](languages/java/README.md) | 🌱 | 🌱 | 🌱 | — | 🌱 | — |

## Practices (any paradigm)

- ✅ [Pull requests](practices/pull-requests.md) — size, stacking, drafts, descriptions, reviewing
- ✅ [Validating your work](practices/validating-work.md) — run what CI runs, follow the PR's checks
- 🔜 Tidy First — small structural changes before, after, or instead of a behavior change
- 🔜 Layers and hexagonal architecture — the application core, ports and adapters, the dependency rule
