# Java

Covered from Java 8 onward, standard language and JDK features only.

## Approaches supported

| Approach | How Java supports it |
|---|---|
| Object-oriented | Classes, interfaces (default methods since Java 8), enums, records (Java 16), sealed types (Java 17) |
| Procedural | `static` methods and utility classes |
| Functional | Lambdas, method references, `java.util.function`, streams, `Optional` (all since Java 8) |
| Parallel | Threads, `java.util.concurrent`, `CompletableFuture` (Java 8), parallel streams, virtual threads (Java 21) |

Details for object-oriented code: [idioms, pitfalls and patterns](object-oriented.md). What each version added: [Java features by version](versions.md).

## Detecting the version

| Where | What to read |
|---|---|
| `build.gradle.kts` / `build.gradle` | `java { toolchain { languageVersion.set(JavaLanguageVersion.of(N)) } }`, `options.release`, `sourceCompatibility` / `targetCompatibility` |
| `pom.xml` | `<maven.compiler.release>`, `<maven.compiler.source>` / `<target>`, the `maven-compiler-plugin` `<release>`, or Spring Boot's `<java.version>` |
| Version files | `.java-version`, `.tool-versions`, `.sdkmanrc` |
| CI | `actions/setup-java` `java-version`, the Docker base image |
| Old projects | `1.8` means Java 8 |

Preview features (`--enable-preview`) don't count as available unless the project already enables them.

## Sources

- [Java SE documentation](https://docs.oracle.com/en/java/javase/) — the API docs for each release
- [JEP index](https://openjdk.org/jeps/0) — the release that delivered each language and JDK feature
