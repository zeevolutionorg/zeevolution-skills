---
type: llm
---
Before any finding, the review states the language and version (Kotlin 1.9, JVM toolchain 17) and the approach the code is written in (an object-oriented class with a procedural loop inside). The review is organised as: verdict, what was checked, context, findings ordered by severity, Tidy First, not covered yet. Findings include the hand-written lazy singleton (not thread-safe; Kotlin's `object` declaration replaces it), `Double` for money, and the untyped `Map<String, Any>` lines with unchecked casts. Every suggested fix compiles on Kotlin 1.9.
