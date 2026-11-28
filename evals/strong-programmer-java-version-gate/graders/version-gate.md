---
type: llm
---
The review states the project is on Java 8 before suggesting anything. None of its fixes use `var`, records, sealed types, switch expressions, pattern matching for `instanceof` or `switch`, text blocks, `List.of`, `Stream.toList()` or other post-Java-8 APIs. Its suggestions work on Java 8, for example: private final fields with an immutable class or constructor, `java.time.Instant`/`LocalDateTime` instead of `java.util.Date`, streams with `distinct()` and `Collectors.toList()` (or a `LinkedHashSet`) for `carriers`, polymorphism (a method on a common event type) instead of the `instanceof` chain. If it mentions newer features, it labels them as needing a JDK upgrade and does not present them as fixes.
