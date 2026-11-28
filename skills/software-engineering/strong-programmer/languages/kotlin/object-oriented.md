# Kotlin for object-oriented code

What good object-oriented Kotlin looks like in review, the traps that come up most, and how the language absorbs the GoF patterns. Check the project's version first: the version each feature needs is in [Kotlin features by version](versions.md). The general rules — principles, smells, pattern fit — are in [object-oriented](../../paradigms/imperative/object-oriented/README.md). `KiA §` points to a section of *Kotlin in Action*, 1st edition, which covers Kotlin 1.0; later features cite their Kotlin version.

## Idioms that matter in review

- **Final by default, `open` on purpose** — classes and members are closed unless marked `open`. Expect `open` only on classes designed for extension, and only on the members meant to be overridden; an override that subclasses must not change again is `final override`. Flag `open` added "in case" and overrides of members never designed for it (KiA §4.1.2).
- **Narrowest visibility** — `private` first; `internal` for what the rest of the module uses but other modules must not; a `private` top-level declaration is private to its file. Flag public declarations nobody outside needs, especially in library modules, where explicit API mode (Kotlin 1.4) makes the choice visible (KiA §4.1.3).
- **Interfaces with default methods** — an interface can carry default bodies and abstract properties, but no state. Flag an abstract base class whose only job is to share a default method (KiA §4.1.1).
- **Nested by default, `inner` on purpose** — a nested class holds no reference to its outer instance; an `inner` one does. Flag `inner` when the body never touches the outer instance: it keeps the outer object alive for nothing (KiA §4.1.4).
- **Sealed hierarchies with exhaustive `when`** — a closed set of cases (payment methods, results, states) is a `sealed class`, or a `sealed interface` from Kotlin 1.5, matched with `when` used as an expression and no `else`. Adding a case then fails to compile wherever it isn't handled. Flag an `else` branch on a sealed subject — it switches the check off — and `String` or `Int` type codes where a sealed type fits (KiA §4.1.5, §2.3).

  ```kotlin
  sealed interface Payment                          // Kotlin 1.5; a sealed class before
  data class Card(val last4: String) : Payment
  data class BankTransfer(val iban: String) : Payment
  data object Cash : Payment                        // Kotlin 1.9; a plain object before

  fun feeInCents(payment: Payment): Int = when (payment) { // an expression: a new case won't compile until handled
      is Card -> 30
      is BankTransfer -> 0
      Cash -> 0
  }
  ```

- **Primary constructor and `init`** — dependencies and required state arrive through the primary constructor as `private val`; `init` validates with `require`. Prefer default arguments to secondary constructors. Flag dependencies set after construction and two-phase `setup()` methods (KiA §4.2.1, §4.2.2).
- **Properties, not getters and setters** — expose `val` properties; compute derived values in a custom getter; keep writes inside the class with `private set`; touch `field` only inside accessors. Flag Java-style `getTotal()` / `setTotal()` functions and public `var`s that let callers break an invariant (KiA §2.2.1–2.2.2, §4.2.3–4.2.5).
- **Data classes for values** — a `data class` with `val` properties gives equality by value, a readable `toString` and `copy`. Flag data classes for entities with identity (equality over every field is wrong for them), `var` properties, and properties declared in the body, which `equals` and `copy` ignore (KiA §4.3.1–4.3.2).
- **Delegation with `by` instead of inheritance** — `class AuditedRepository(private val inner: Repository) : Repository by inner` overrides only what it changes. Flag a subclass of a concrete class made only to tweak one method, and wrappers that forward every method by hand (KiA §4.3.3).
- **`object` for stateless singletons** — an `object` suits a stateless strategy, a comparator or a sealed case with no data. Anything with state, configuration or a test double is one instance created at startup and injected (KiA §4.4.1).
- **Companion objects as named factories** — a private constructor plus `companion object { fun of(…) }` when creation validates input, names a case or picks a subclass. Flag companions that collect unrelated helpers and constants (KiA §4.4.2–4.4.3).
- **Object expressions** — `object : Listener { … }` for a one-off implementation of several members; for a single-method Kotlin interface, a `fun interface` and a lambda (Kotlin 1.4) read better (KiA §4.4.4).
- **Extensions or members** — extensions add convenience to types you don't own or keep a class's core small. They can't reach `private` or `protected` members and are resolved statically, so they never behave polymorphically. Flag an extension where behavior must vary by subtype — that's a member — and extensions on your own class that need its internals (KiA §3.3, §3.3.4).
- **Top-level functions, not utility classes** — a stateless helper is a top-level function in a well-named file, not an `object` or a class of static methods (KiA §3.2.3).
- **Named and default arguments, not overloads or builders** — one constructor with defaults replaces telescoping constructors and most builders; named arguments make `Boolean` and same-typed parameters readable at the call site (KiA §3.2.1–3.2.2).
- **Absence in the type** — `T?` only where absence is a real case; `?.` and `?:` for defaults and early returns; smart casts after a check instead of casts (KiA §6.1, §2.3.5). Flag `!!` and nullable types for values that are always present.
- **Read-only collection types at boundaries** — expose `List`, `Set` and `Map`, keep the mutable type private. Read-only is not immutable: another reference may still change the list, so copy input you store (`toList()`) (KiA §6.3.2).
- **Delegated properties** — `by lazy` for expensive values not always needed; `Delegates.observable` to react to changes of one property; hand-written double-checked locking is a finding (KiA §7.5, §7.5.2–7.5.3).
- **`apply` and `with`** — `apply` configures an object right after creating it, typically a Java object with setters; `with` groups several calls on one object. Flag nested scope functions where `this` and `it` stop being obvious (KiA §5.5).
- **Function types and `inline`** — accept `(Order) -> Money` instead of declaring a one-method interface for a small role; mark a higher-order function `inline` when it takes lambdas and is called often. Flag `inline` on functions without lambda parameters (KiA §8.1, §8.2, §8.2.4).
- **Variance at API boundaries** — a parameter that only reads takes `List<Shape>`, not `MutableList<Shape>`; your own generic producers declare `out T`, consumers `in T`. Flag unchecked casts that work around missing variance (KiA §9.3).
- **Value classes for domain primitives** — `@JvmInline value class OrderId(val value: String)` (Kotlin 1.5) stops swapped arguments at compile time at no allocation cost in most uses; before 1.5, a small data class.

## Pitfalls

- **A `data class` with `var` properties used as a map key or in a set** — changing a property changes `hashCode`, and the entry is lost (KiA §4.3.2).
- **A JPA entity written as a `data class`** — generated `equals` and `hashCode` cover mutable fields and lazy relations, and `toString` can trigger lazy loading. Write identity-based equality by hand.
- **`copy()` is shallow and stays public** — a copied data class shares its mutable lists with the original. `copy()` also stays callable when the constructor is private, so it skips checks done only in a factory function such as a companion `of(…)`; checks in `init` still run, because `copy()` calls the primary constructor. Kotlin 2.0.20 warns, and `@ConsistentCopyVisibility` makes `copy()` as private as the constructor.
- **Arrays in a data class** — `equals` compares array references, not contents. Use a `List`.
- **`!!` instead of modelling absence** — each one is a possible `NullPointerException` the type system was meant to prevent (KiA §6.1.6).
- **Platform types from Java** — `String!` lets a Java `null` through until something dereferences it far from the cause (KiA §6.1.11). Declare the Kotlin type at the boundary.
- **`lateinit` hiding a missing constructor dependency** — fails at run time with `UninitializedPropertyAccessException` instead of at construction (KiA §6.1.8). Fine for test fixtures and framework-injected fields; not for domain objects.
- **An extension shadowed by a member** — a member with the same signature always wins, so the extension is silently never called (KiA §3.3.4).
- **Calling an `open` member from a constructor or `init`** — the subclass override runs before the subclass's properties are initialized and sees `null` even in non-null types.
- **Companion objects as a dumping ground** — constants, helpers and factories for unrelated concerns in one companion: the Kotlin form of a `*Utils` class.
- **`open` everywhere for frameworks** — Spring and other proxy-based frameworks need open classes; the `kotlin-spring` (all-open) compiler plugin opens the annotated ones, and `kotlin-jpa` (no-arg) adds the constructor JPA needs. Writing `open` by hand on every class and member is the wrong fix.
- **An `object` holding mutable global state** — shared across tests and threads, and impossible to replace in a test. Inject an instance instead.
- **Coroutines** — `GlobalScope.launch` with no owner to cancel it; blocking calls (`Thread.sleep`, JDBC, blocking HTTP) inside a coroutine without `withContext(Dispatchers.IO)`; `catch (e: Exception)` or `runCatching` around suspending calls that swallows `CancellationException` and keeps a cancelled coroutine running — rethrow it.

## Patterns the language absorbs

Where Kotlin offers nothing special, the pattern is still written with classes and interfaces, and the general [pattern misuse](../../paradigms/imperative/object-oriented/pattern-misuse.md) checks apply. On a version without the feature, the hand-written pattern is correct — don't flag it.

| Pattern | Kotlin feature | Since | Review note |
|---|---|---|---|
| Abstract Factory | Still a class-level design | — | Keep it when whole families of objects must vary together; with one family it's a constructor call. A one-method factory can be a function type |
| Builder | Named and default arguments; `copy()` on a data class for variants; `apply` to configure mutable objects (KiA §3.2.1–3.2.2, §4.3.2, §5.5.2) | Kotlin 1.0 | A builder for a few properties is overkill. Type-safe builders with lambdas with receivers suit nested structures (KiA §11.2). GoF's Builder — one process, several representations — is still classes |
| Factory Method | Factory functions in a `companion object`, or top-level functions (KiA §4.4.2) | Kotlin 1.0 | That's a named constructor. GoF's version, where a subclass decides the class, still needs classes |
| Prototype | `copy()` on a data class (KiA §4.3.2) | Kotlin 1.0 | Shallow: mutable properties stay shared with the original |
| Singleton | `object` declaration (KiA §4.4.1) | Kotlin 1.0 | Stateless only. With state or a test double, create one instance at startup and inject it. `data object` (Kotlin 1.9) when it gets printed |
| Adapter | Extension functions (KiA §3.3) | Kotlin 1.0 | For a different call shape only: an extension can't make a type implement an interface. That still takes a wrapper class, with `by` when most methods pass through |
| Bridge | Still a class-level design | — | Inject the implementor through the constructor; with one implementation, it's speculative |
| Composite | A sealed type with leaf and composite cases, operations as recursive `when` expressions (KiA §4.1.5) | Kotlin 1.0 | Keep the GoF interface when other modules add node types |
| Decorator | Class delegation with `by` (KiA §4.3.3) | Kotlin 1.0 | Override only the decorated methods. A decorator named `*Adapter` is misnamed |
| Facade | Still a class-level design | — | A facade that forwards one call per method is the Middle Man smell |
| Flyweight | `object` for shared stateless instances; enum entries; interned values | Kotlin 1.0 | Share immutable state only; a cache of mutable objects is not a flyweight |
| Proxy | `by lazy` for a virtual proxy (KiA §7.5.2); `by` delegation for access-control or logging proxies (KiA §4.3.3) | Kotlin 1.0 | A proxy keeps its subject's interface. Dynamic proxies still use `java.lang.reflect.Proxy` |
| Chain of Responsibility | A list of handler functions tried in order, such as `handlers.firstNotNullOfOrNull { it(request) }` | Kotlin 1.0; `firstNotNullOfOrNull` 1.5 | Keep handler classes when each one is configured separately or must pass the request on after acting, as filters and interceptors do |
| Command | A lambda of type `() -> Unit` (KiA §8.1); a `fun interface` when the role needs a name | Kotlin 1.0; `fun interface` 1.4 | Keep a class when the command needs undo, or must be logged, replayed or serialized |
| Interpreter | A sealed expression tree evaluated by a recursive `when` (KiA §4.1.5) | Kotlin 1.0 | For a small grammar only; a real language needs a parser |
| Iterator | Implement `Iterable` or `operator fun iterator()` (KiA §7.3.4); return a `Sequence` (KiA §5.3); build one with `sequence {}` | Kotlin 1.0; `sequence {}` 1.3 | Hand-written `hasNext` / `next` classes are rarely needed |
| Mediator | Still a class-level design | — | Inside one module, for calls that are synchronous, ordered and known, call directly |
| Memento | An immutable data class snapshot taken and restored by the originator (KiA §4.3.2) | Kotlin 1.0 | Nest the snapshot type in the originator and keep its members private |
| Observer | `Flow`; `StateFlow` and `SharedFlow`; `Delegates.observable` for one property (KiA §7.5.3) | kotlinx.coroutines 1.3; 1.4 for `StateFlow` and `SharedFlow` | A library: check its version, not Kotlin's. One known dependent is a direct call |
| State | A sealed type of states — data classes, plus `data object` from Kotlin 1.9 — with transitions as `when` expressions that return the next state (KiA §4.1.5) | Kotlin 1.0 | Move behavior into the state classes once the `when` branches grow |
| Strategy | Function types and lambdas (KiA §8.1); a `fun interface` when the role needs a name | Kotlin 1.0; `fun interface` 1.4 | One algorithm and no selection is a plain function |
| Template Method | A higher-order function that takes the varying step as a lambda (KiA §8.1.6) | Kotlin 1.0 | Mark it `inline` when it's called in hot paths (KiA §8.2) |
| Visitor | A sealed class (KiA §4.1.5) or `sealed interface`, matched with `when` used as an expression | Kotlin 1.0; `sealed interface` 1.5; `when` statements checked from 1.7 | Keep the GoF Visitor for many unrelated operations over a stable hierarchy you can't seal |

## Java interop

- **`@JvmStatic`, `@JvmField`** — without `@JvmStatic`, Java calls a companion function as `Money.Companion.of(…)`; with it, `Money.of(…)`. `@JvmField` exposes a property as a plain field. Both work in interface companions from Kotlin 1.3 (KiA §4.4.3, §10.1.2).
- **`@JvmOverloads`** — Java can't use default arguments; this generates the overloads (KiA §3.2.2).

  ```kotlin
  class Money private constructor(val cents: Long, val currency: String) {
      companion object {
          @JvmStatic
          @JvmOverloads
          fun of(cents: Long, currency: String = "EUR"): Money {
              require(cents >= 0) { "negative amount: $cents" }
              return Money(cents, currency)
          }
      }
  }
  // Java: Money.of(1500) and Money.of(1500, "USD")
  ```

- **`@JvmName`** — renames a generated method or file class, for example `@file:JvmName("Prices")`, or resolves signature clashes after type erasure (KiA §3.2.3, §10.1.2).
- **`@Throws`** — Kotlin has no checked exceptions. Without `@Throws(IOException::class)`, Java callers can't write a `catch` for the checked exception your function actually throws.
- **Platform types and nullability annotations** — Java types without annotations arrive as platform types (KiA §6.1.11); collections from Java too (KiA §6.3.4). Annotated Java (JSpecify, JetBrains, `javax.annotation`) gives real nullable or non-null types; JSpecify mismatches are errors from Kotlin 2.1. When writing Java that Kotlin calls, annotate it.
- **SAM conversion for Java interfaces** — pass a lambda wherever Java expects `Runnable`, `Comparator` or another single-method interface; a SAM constructor (`Runnable { … }`) makes the type explicit (KiA §5.4, §5.4.2).
- **Read-only collections are mutable from Java** — a `List` handed to Java code can be changed there, and Kotlin won't know. Pass a copy when it matters (KiA §6.3.3).
- **`internal` is public in bytecode** — Java code in another module can still use `internal` declarations. Only `internal` members of classes get mangled names, which makes such calls awkward, not impossible (KiA §4.1.3).
- **Interface default methods** — before Kotlin 2.2, default bodies compile into a `DefaultImpls` class unless the build sets `-Xjvm-default`, so Java classes implementing the interface must implement every method. From 2.2 they are JVM default methods.
- **Records** — `@JvmRecord data class` (Kotlin 1.5, JVM 16 bytecode) when Java code needs a real record; Java records are used from Kotlin like any class with properties.
