# Kotlin

## Approaches supported

| Approach | How Kotlin supports it |
|---|---|
| Object-oriented | Classes final by default, interfaces with default methods, `data`, `sealed`, `object`, delegation with `by` |
| Functional | Lambdas, function types, extension functions, read-only collection interfaces, sequences |
| Procedural | Top-level functions and properties, no class required |
| Parallel | Coroutines, structured concurrency and `Flow` from the `kotlinx.coroutines` library, plus the JVM's threads and executors |

Details for object-oriented code: [idioms, pitfalls and patterns](object-oriented.md). What each version added: [Kotlin features by version](versions.md).

## Detecting the version

| Where | What to read |
|---|---|
| `build.gradle.kts` / `build.gradle` | `kotlin("jvm") version "x.y.z"` or `id("org.jetbrains.kotlin.jvm") version "x.y.z"` (Groovy: `id 'org.jetbrains.kotlin.jvm' version 'x.y.z'`); the `android` and `multiplatform` plugin ids carry the version the same way |
| `gradle/libs.versions.toml`, `gradle.properties`, `buildSrc` / `build-logic` | `kotlin = "x.y.z"` in the catalog (used through `alias(libs.plugins.…)`), a `kotlinVersion` property, or the version in a convention plugin |
| `pom.xml` | `<kotlin.version>` and the `kotlin-maven-plugin` |
| Compiler options | `languageVersion` / `apiVersion` — when set, they cap the features you may use |
| JVM target | `jvmToolchain(N)` or `jvmTarget` — treat it as the cap for Java APIs; `jvmTarget` alone won't stop the compiler from accepting newer ones |
| Coroutines | The `org.jetbrains.kotlinx:kotlinx-coroutines-core` version |

## Sources

- *Kotlin in Action*, 1st edition — Dmitry Jemerov and Svetlana Isakova (Manning): the language's idioms, up to Kotlin 1.0
- [What's new in Kotlin](https://kotlinlang.org/docs/whatsnew.html) and [Kotlin releases](https://kotlinlang.org/docs/releases.html): what each later version added
