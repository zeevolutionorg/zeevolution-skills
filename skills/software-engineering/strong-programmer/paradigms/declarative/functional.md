# Functional

Programs built from functions that compute values from values, without changing anything else along the way.

## Core idea

A function's result depends only on its arguments, and calling it changes nothing outside it. Data is immutable: to "change" a value you build a new one. Functions are values too — passed in, returned, combined — so behavior is assembled from small pieces instead of written as a sequence of mutations. Effects such as I/O, time, randomness and the database don't go away; they move to the edges, and the core between them becomes easy to test and safe to run in parallel.

In Kotlin and Java the style rarely shapes a whole program; it governs collection pipelines, domain calculations and result types inside object-oriented code.

Base definitions: [the paradigms overview](../README.md#sources).

## Primitives

| Primitive | What it gives you |
|---|---|
| Pure function | Same input, same output, no side effects — tested with plain asserts, safe to cache and to run in parallel |
| Immutable value | Nobody can change it under you, so it can be shared freely across threads |
| First-class and higher-order functions | Functions passed and returned like data: `filter`, `map`, a `(Order) -> Boolean` parameter |
| Composition | Larger functions made by chaining smaller ones: `andThen`, `compose`, a `map` / `filter` pipeline |
| Referential transparency | A call can be replaced by its result without changing behavior, which makes refactoring safe |
| Algebraic data types (sealed + data/records) | A closed set of cases, each with its own data: a `sealed interface Payment` whose cases are `data class`es or `record`s |
| Pattern matching | Branch on which case a value is and unpack it, with the compiler checking that every case is handled — in Kotlin for `when` expressions over sealed and enum types (for `when` statements only since Kotlin 1.7, a warning in 1.6), in Java with pattern matching for `switch` (Java 21) |
| Folds and recursion | Iteration as a reduction over a structure: `fold`, `reduce`, collectors, `tailrec` in Kotlin |
| Laziness | Work done only when a result is needed: Kotlin's `Sequence`, Java streams, `lazy {}` |
| Effects at the edges | A pure core that decides, wrapped in a thin shell that reads input and carries out the effects |

## Strengths and costs

| Strengths | Costs |
|---|---|
| Pure code is trivial to test and to reason about locally | Effects still exist, and threading them through takes design |
| Immutable values make concurrency much safer | Copying instead of mutating costs allocations in hot paths |
| Sealed types make every case explicit and compiler-checked | Dense pipelines and function composition can be hard to read and to debug |
| Small functions compose and get reused | Deep recursion can overflow the JVM stack; there is no general tail-call optimization |

## Signals the code is in this style

- Chains of `map`, `filter`, `flatMap`, `fold`, `groupBy`, or streams ending in `collect`.
- `val`, read-only collections, records, `copy(...)` to derive a changed value.
- Functions taking or returning lambdas; `java.util.function` types in signatures.
- `sealed` hierarchies matched with `when` or `switch` instead of exceptions or type codes.

## Common failure modes

- **Side effects inside lambdas.** `orders.forEach { total += it.amount }`, or a `map` that saves each element: the pipeline looks pure but isn't, and parallel streams or lazy sequences run the effect out of order, more than once, or not at all. Fix: compute with `sumOf`, `fold` or a collector, and keep effects in one explicit loop or terminal step.
- **Pipelines too long to read.** Fifteen chained calls with nested lambdas and `it` hiding an outer `it`. Fix: name the intermediate values, extract steps into named functions, and accept a plain loop when it reads better.
- **`Optional` / nullable chains hiding errors.** `findUser(id)?.account?.limit ?: 0` or `.map(...).orElse(null)` turns "not found", "not set" and "failed" into one silent default. Fix: give the outcomes a type — a sealed result — or fail loudly where a missing value is a bug; keep `Optional` for return values, not fields or parameters.
- **Exceptions as control flow.** An expected outcome such as insufficient funds thrown through pure code and caught layers above. Fix: return a sealed result (`Approved` / `Rejected`) and keep exceptions for bugs and infrastructure failures.
- **Point-free code nobody can follow.** Method references, `andThen` / `compose` and curried helpers chained so that no argument is ever named. Fix: name the arguments and the steps; being clever is not the goal.

## Review questions

1. Which functions are pure, and where do the effects happen — is that boundary visible?
2. Can any lambda here change state outside itself?
3. Do values stay unchanged once built, including collections handed to callers?
4. Does each `when` / `switch` over a sealed type cover every case, without an `else` / `default` that would hide a new one?
5. Do absent values and expected failures have types, or do they hide in nulls, empty `Optional`s and exceptions?
6. Would a named function or a plain loop read better than this chain?
7. Is laziness intended — is each `Sequence` or stream consumed once, before its resources close?

## Languages

| Language | Support |
|---|---|
| Kotlin | Lambdas and function types (*Kotlin in Action*, ch. 5 and §8.1); collection operations; sequences for lazy pipelines (§5.3); `sealed` classes with `when` (sealed interfaces since Kotlin 1.5; exhaustiveness checked for `when` expressions, and for `when` statements only since Kotlin 1.7); `val`, `data` classes and read-only collection interfaces — read-only, not immutable: another reference may still change the list; `tailrec` |
| Java | Lambdas, method references, `java.util.function`, streams and `Optional` (Java 8); records (Java 16); sealed classes and interfaces (Java 17); pattern matching for `switch` and record patterns (Java 21) |

Version detection and what each language offers: [`languages/README.md`](../../languages/README.md).

## Branches

None yet.

Back to [declarative programming](README.md).
