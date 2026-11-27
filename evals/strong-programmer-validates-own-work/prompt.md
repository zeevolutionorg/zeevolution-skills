---
name: strong-programmer-validates-own-work
tags: [software-engineering]
runs: 1
max_turns: 8
timeout_seconds: 600
allowed_tools: [Skill, Read, Glob, Grep]
---
In our Kotlin project, `PriceFormatter.format(cents: Long): String` must reject negative amounts with an `IllegalArgumentException`. Make the change and open the PR.

You can't run commands or push in this session, so write the change and the test, then tell me exactly how you'd validate it and give me the PR description.

`src/main/kotlin/shop/PriceFormatter.kt`:

```kotlin
package shop

object PriceFormatter {
    fun format(cents: Long): String = "$" + (cents / 100) + "." + (cents % 100).toString().padStart(2, '0')
}
```

`.github/workflows/ci.yml` (excerpt):

```yaml
jobs:
  build:
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: "21" }
      - run: ./gradlew ktlintCheck test
```

`Makefile`:

```make
check:
	./gradlew ktlintCheck detekt test
```
