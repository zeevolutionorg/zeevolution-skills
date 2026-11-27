# Knowledge map

What `strong-programmer` knows and how deep. Open a node only when the task needs it.

**Status:** ✅ detailed · 🌱 fundamentals only · 🔜 planned (no file yet — work from general knowledge and say so in the report) · — not applicable

## Paradigms and approaches

- 🌱 [Programming paradigms](paradigms/README.md) — imperative vs declarative, and how to tell which approach code is written in
  - 🌱 [Imperative](paradigms/imperative/README.md) — say *how*, step by step, changing state
    - 🌱 [Procedural](paradigms/imperative/procedural.md) — procedures over shared data
    - ✅ [Object-oriented](paradigms/imperative/object-oriented/README.md) — objects bundle state with behavior
      - ✅ [Principles: GoF principles, SOLID](paradigms/imperative/object-oriented/principles.md)
      - ✅ [Code smells and anti-patterns](paradigms/imperative/object-oriented/code-smells.md)
      - ✅ [Pattern misuse](paradigms/imperative/object-oriented/pattern-misuse.md) — the right pattern for the wrong problem
      - ✅ [Domain-driven design building blocks](paradigms/imperative/object-oriented/domain-driven-design.md)
      - 🔜 Design patterns: creational, structural, behavioral
    - 🌱 [Parallel](paradigms/imperative/parallel.md) — several steps at the same time
  - 🌱 [Declarative](paradigms/declarative/README.md) — say *what* you want; the runtime decides how
    - 🌱 [Logic](paradigms/declarative/logic.md) — facts and rules
    - 🌱 [Functional](paradigms/declarative/functional.md) — pure functions over immutable values
    - 🌱 [Database](paradigms/declarative/database.md) — set-based queries

## Languages

- 🌱 [Language registry and version detection](languages/README.md)
  - ✅ [Kotlin features by version](languages/kotlin/versions.md)
  - ✅ [Kotlin for object-oriented code](languages/kotlin/object-oriented.md)
  - ✅ [Java features by version](languages/java/versions.md)
  - ✅ [Java for object-oriented code](languages/java/object-oriented.md)

| Language | Procedural | Object-oriented | Parallel | Logic | Functional | Database |
|---|---|---|---|---|---|---|
| 🌱 [Kotlin](languages/kotlin/README.md) | 🌱 | ✅ | 🌱 | — | 🌱 | — |
| 🌱 [Java](languages/java/README.md) | 🌱 | ✅ | 🌱 | — | 🌱 | — |

## Practices (any paradigm)

- ✅ [Pull requests](practices/pull-requests.md) — size, stacking, drafts, descriptions, reviewing
- ✅ [Validating your work](practices/validating-work.md) — run what CI runs, follow the PR's checks
- 🔜 Tidy First — small structural changes before, after, or instead of a behavior change
- 🔜 Layers and hexagonal architecture — the application core, ports and adapters, the dependency rule
