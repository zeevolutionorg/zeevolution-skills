# Languages

Each language supports one or more approaches. Detect the language **and its version** before suggesting anything: a feature the project can't compile is not a fix.

| Language | Approaches | Version from | Details |
|---|---|---|---|
| Kotlin | Object-oriented, functional, procedural, parallel (coroutines) | The Kotlin Gradle or Maven plugin; `jvmToolchain` | [Kotlin](kotlin/README.md) |
| Java | Object-oriented, procedural, functional (since Java 8), parallel | `release` or the toolchain in Gradle or Maven | [Java](java/README.md) |

## Detecting the version

1. Read the build files: `build.gradle.kts` / `build.gradle`, `settings.gradle.kts`, `gradle/libs.versions.toml`, `pom.xml`.
2. Check the toolchain and target as well as the compiler. Compare per axis — the language version for syntax, the JDK version for APIs: on each axis, the lower one decides what you may suggest.
3. Look at the CI setup steps (`actions/setup-java`, Docker base images) when the build files don't say.
4. If you still can't tell, say so in the report and keep suggestions to what the oldest plausible version supports.

For a language not listed here, apply the same steps with that ecosystem's build files, and list the language under **Not covered yet**.
