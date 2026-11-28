---
name: strong-programmer-orients-first
tags: [smoke, software-engineering]
runs: 1
max_turns: 6
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob, Grep]
---
Review this code from our billing service.

`build.gradle.kts` (excerpt):

```kotlin
plugins {
    kotlin("jvm") version "1.9.24"
}
kotlin {
    jvmToolchain(17)
}
```

`InvoiceService.kt`:

```kotlin
class InvoiceService private constructor() {
    companion object {
        private var instance: InvoiceService? = null
        fun getInstance(): InvoiceService {
            if (instance == null) instance = InvoiceService()
            return instance!!
        }
    }

    fun total(lines: List<Map<String, Any>>): Double {
        var sum = 0.0
        for (line in lines) {
            val price = line["price"] as Double
            val qty = line["qty"] as Int
            sum += price * qty
        }
        return sum
    }
}
```
