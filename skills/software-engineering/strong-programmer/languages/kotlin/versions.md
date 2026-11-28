# Kotlin features by version

Suggest only what the project's version supports; see [the README](README.md) for detection. Upgrading Kotlin or `kotlinx.coroutines` is the team's decision, never a review fix: write every fix for the version the project runs today, and if a newer feature would help, mention it once, after those fixes, labelled with the version it needs. Rows tagged `kotlinx.coroutines` follow that library's version, not Kotlin's. Covers every release up to Kotlin 2.4.21, the latest stable one when this page was checked (November 2026).

| Feature | Since | Replaces or enables | Review note |
|---|---|---|---|
| Data classes: generated `equals`, `hashCode`, `toString`, `componentN` and `copy` | Kotlin 1.0 | Hand-written or IDE-generated value classes | Expect `val` properties only; a `var` in a data class used as a map key or set element breaks the container |
| Sealed classes, with every subclass nested inside the sealed class | Kotlin 1.0 | An open hierarchy plus an `else` branch nobody can test | Use `when` as an expression over it so the compiler checks every case |
| `object` declarations and companion objects | Kotlin 1.0 | Hand-written singletons; Java `static` members | A stateless `object` is fine; mutable state in one is global data |
| Class delegation with `by` | Kotlin 1.0 | Wrappers that forward every method by hand | Suggest it for decorators and wrappers that change only a few methods |
| Delegated properties: `by lazy`, `Delegates.observable` | Kotlin 1.0 | Hand-written lazy initialization, null checks and change callbacks | `lazy` is synchronized by default; another thread-safety mode needs a reason |
| Extension functions and properties | Kotlin 1.0 | Static `*Utils` classes | Resolved statically: a member with the same signature always wins |
| Top-level functions and properties | Kotlin 1.0 | Classes that exist only to hold static methods | Suggest them instead of an `object` with no state |
| `when` with smart casts after `is` | Kotlin 1.0 | `instanceof` checks followed by casts | Flag an explicit `as` right after an `is` check |
| Named and default arguments | Kotlin 1.0 | Telescoping constructors; builders for optional parameters | Suggest named arguments at call sites with several `Boolean` or same-typed parameters |
| Sealed subclasses anywhere at the top level of the same file; data classes extending other classes | Kotlin 1.1 | Subclasses nested inside the sealed class | Below 1.1, every subclass of a sealed class must be nested in it |
| Type aliases (`typealias`) | Kotlin 1.1 | Repeating long generic or function types | An alias is not a new type and catches no mix-ups; for that, use a value class (Kotlin 1.5) |
| Bound callable references (`cart::total`) | Kotlin 1.1 | A lambda that only calls one method on a captured object | Prefer the reference when it reads better than the lambda |
| `also`, `takeIf`, `takeUnless` | Kotlin 1.1 | Temporary variables for side effects and conditional values | Flag long chains of scope functions that hide control flow |
| `lateinit` on top-level properties and local variables; `::name.isInitialized` | Kotlin 1.2 | A nullable `var` read with `!!` | An `isInitialized` check in business code usually means the value belongs in the constructor |
| Coroutines stable: `suspend` functions, the `sequence {}` builder | Kotlin 1.3 | The experimental coroutines of 1.1–1.2; callbacks; hand-written iterators | Code still on the experimental coroutine package needs migrating, not mixing |
| `Result` and `runCatching` | Kotlin 1.3 | `try`/`catch` blocks that turn an exception into a value | In coroutines it also catches `CancellationException`: rethrow it |
| Capturing the `when` subject: `when (val reply = send()) { … }` | Kotlin 1.3 | A local declared just before the `when` | The variable's scope ends with the `when` |
| `CoroutineScope` and structured concurrency | kotlinx.coroutines 1.0 | Coroutines launched with no owner | Every launch belongs to a scope with a lifecycle; flag `GlobalScope` |
| `Flow`, the core cold-stream API | kotlinx.coroutines 1.3 | Callbacks, Rx streams, channels used as streams | Operators marked `@FlowPreview` or `@ExperimentalCoroutinesApi` are not stable |
| `fun interface`: SAM conversion for Kotlin interfaces | Kotlin 1.4 | Object expressions implementing a one-method Kotlin interface | A plain function type is enough when the role needs no name |
| Trailing commas | Kotlin 1.4 | Diff noise when a parameter is added or moved | Style only: leave it to the formatter |
| Named arguments mixed with positional ones | Kotlin 1.4 | Naming every argument after the first named one | Name just the argument that needs it, such as a `Boolean` in the middle of a call; below 1.4, every argument after a named one must be named too |
| Explicit API mode (`explicitApi()`) | Kotlin 1.4 | Library declarations public by accident | Suggest it for published library modules |
| `StateFlow` and `SharedFlow` | kotlinx.coroutines 1.4 | `ConflatedBroadcastChannel`, `BroadcastChannel`, hand-written listener lists | Expose the read-only `StateFlow`; keep the `MutableStateFlow` private |
| Value classes (`@JvmInline value class`) | Kotlin 1.5 | `inline class` (Alpha in 1.3); data class wrappers around one value | One underlying property; boxed when used as a generic or interface type |
| Sealed interfaces; sealed subclasses in any file of the same package and module | Kotlin 1.5 | Sealed classes forcing single inheritance; one large file per hierarchy | Below 1.5, use a `sealed class` in one file |
| `@JvmRecord` on data classes | Kotlin 1.5 | Java code that needs a real record from a Kotlin class | Needs JVM 16 bytecode and a class that extends nothing; only for Java interop |
| `GlobalScope` marked `@DelicateCoroutinesApi` | kotlinx.coroutines 1.5 | Silent use of `GlobalScope` | An opt-in on it is a finding unless the code says why |
| Warnings for non-exhaustive `when` statements over enum, sealed or `Boolean` subjects | Kotlin 1.6 | Silently skipped cases | Below 1.6, only `when` expressions are checked |
| `kotlin.time.Duration`; `buildList`, `buildMap`, `buildSet` | Kotlin 1.6 | `Long` millisecond parameters; a mutable collection built and then copied | Suggest `Duration` for timeouts and intervals |
| Non-exhaustive `when` statements over enum, sealed or `Boolean` subjects are errors | Kotlin 1.7 | Relying on reviewers to spot a missed case | Below 1.7, make the `when` an expression to get the check |
| Definitely non-nullable types `T & Any` | Kotlin 1.7 | Casts and `!!` when overriding Java generic methods | Mostly for Java interop and generic APIs |
| Opt-in requirements (`@RequiresOptIn`, `@OptIn`) stable | Kotlin 1.7 | The `-opt-in=kotlin.RequiresOptIn` compiler flag | Each `@OptIn` is a choice to depend on an unstable API: ask why |
| `data object` | Kotlin 1.9 | `object` with a hand-written `toString` inside sealed hierarchies | Suggest it for the stateless cases of a sealed type |
| `entries` on enum classes | Kotlin 1.9 | `values()`, which allocates a new array on every call | Suggest `entries` instead of `values()` |
| `..<` for open-ended ranges | Kotlin 1.9 | `until` | The operator is stable from 1.8, but on the standard types it needs `@OptIn(ExperimentalStdlibApi::class)` until 1.9 |
| Secondary constructors with bodies in value classes | Kotlin 1.9 | Factory functions only to validate a value class | Validation in `init` already works from 1.5 |
| K2 compiler; smarter smart casts: conditions stored in a local `val`, `is` checks joined with `or`, after `inline` lambdas | Kotlin 2.0 | Repeated checks and explicit casts | Below 2.0, keep casts the older compiler needs |
| `enumEntries<T>()` | Kotlin 2.0 | `enumValues<T>()` | Same reasoning as `entries` |
| Warning when a data class's `copy()` exposes a non-public constructor; `@ConsistentCopyVisibility` | Kotlin 2.0.20 | `copy()` staying callable when the constructor is private, which skips checks done only in a factory function such as a companion `of(…)` | Checks in `init` still run, since `copy()` calls the primary constructor. `copy()` will become as visible as the constructor; opt in now with the annotation |
| Exhaustive `when` on a type parameter with a sealed upper bound | Kotlin 2.1 | A redundant `else` branch | Drop the `else` once every case is covered |
| Guard conditions in a `when` with a subject: `when (payment) { is Card if payment.isExpired -> … }` | Kotlin 2.2 | Nested `if` inside a branch | Only in a `when` with a subject; preview in 2.1, behind a compiler flag |
| Non-local `break` and `continue` in lambdas passed to inline functions | Kotlin 2.2 | Rewriting `forEach` as a `for` loop only to break out | Preview in 2.1 |
| Multi-dollar string interpolation (`$$"""…"""`) | Kotlin 2.2 | `${'$'}` escapes in JSON and template strings | Preview in 2.1 |
| Interface functions compiled to JVM default methods by default (`-jvm-default`) | Kotlin 2.2 | Java implementers having to implement every method; the `-Xjvm-default` flag | Matters for Java callers and binary compatibility of libraries |
| Nested type aliases | Kotlin 2.3 | Top-level aliases used by one class | Beta in 2.2 |
| Data-flow-based exhaustiveness for `when` expressions | Kotlin 2.3 | `else -> throw` after an early return already ruled a case out | Experimental in 2.2.20 |
| `return` in expression bodies with an explicit return type | Kotlin 2.3 | Block bodies only to return early | The return type must be written out |
| `kotlin.time.Clock` and `kotlin.time.Instant` in the standard library | Kotlin 2.3 | Reading the system time deep inside logic; `kotlinx-datetime` only for instants | Inject a `Clock` so tests control time. Experimental in 2.1.20–2.2 (needs `@OptIn(ExperimentalTime::class)`): don't suggest it below 2.3; on the JVM, an injected `java.time.Clock` does the same job on any version |
| Context parameters: `context(audit: AuditLog) fun close(account: Account)` | Kotlin 2.4 | The experimental context receivers; a dependency threaded through every call | Not a substitute for a class's constructor dependencies; explicit context arguments and callable references to functions with context parameters are still experimental |
| Explicit backing fields: `val lines: List<Line> field = mutableListOf<Line>()` | Kotlin 2.4 | A private `_lines` property behind a public read-only one | Experimental in 2.3 |
| `kotlin.uuid.Uuid` in the common standard library | Kotlin 2.4 | `java.util.UUID` in multiplatform code; ids passed around as `String` | Wrap it in a value class per id (`@JvmInline value class OrderId(val value: Uuid)`). `Uuid.generateV4()` and `Uuid.generateV7()` are still experimental. Experimental since 2.0.20 (needs `@OptIn(ExperimentalUuidApi::class)`): don't suggest it below 2.4 |

## Not yet stable

Never suggest these as fixes; mention one only if the project already opts in.

- Collection literals (`[a, b]`), explicit context arguments, callable references to functions with context parameters, compile-time evaluation of more standard functions and the `@IntroducedAt` annotation: experimental in Kotlin 2.4.
- The unused return value checker and `@MustUseReturnValues`: experimental since Kotlin 2.3.
- Context-sensitive resolution: experimental since Kotlin 2.2.
- Custom contracts (`contract { … }` in your own functions): experimental since Kotlin 1.3.
- In `kotlinx.coroutines`, any API marked `@ExperimentalCoroutinesApi` or `@FlowPreview`.
