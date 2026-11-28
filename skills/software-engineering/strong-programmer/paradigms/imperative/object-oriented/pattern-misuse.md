# Pattern misuse

A design pattern is a named solution to a recurring problem in a context. Applied to a different problem, it adds indirection and buys none of the flexibility it exists for. GoF warn about this themselves: patterns get their flexibility through extra levels of indirection, so apply one only when that flexibility is actually needed (§1.8, p. 31). Check the problem before you judge — or write — the implementation.

## The main check: is it the right problem?

1. **State the problem in one sentence without naming a pattern.** "After an order is saved, issue its invoice." If you can't, the pattern came first and the problem was fitted to it.
2. **Compare the sentence with the pattern's intent and applicability**, not with its class diagram. Each pattern lets one aspect vary (GoF Table 1.2, p. 30): Observer, *how many* objects depend on another; Strategy, *which* algorithm runs. If the sentence doesn't mention that aspect, it's the wrong pattern.
3. **The variation must exist now**: a second implementation in the code or in the ticket at hand, a choice made at run time, a fake the tests actually need. "We might need another one later" is not a variation.

When a pattern fails the check, the finding names the pattern, the problem sentence, the intent it doesn't match, and the simpler code.

**Example: Observer to call one known collaborator (Kotlin).**

```kotlin
interface OrderPlacedListener { fun onOrderPlaced(order: Order) }

class InvoiceIssuer(private val invoices: InvoiceRepository) : OrderPlacedListener {
    override fun onOrderPlaced(order: Order) {
        invoices.save(Invoice.forOrder(order))
    }
}

class OrderService(
    private val orders: OrderRepository,
    private val listeners: List<OrderPlacedListener>, // always exactly [InvoiceIssuer]
) {
    fun place(order: Order) {
        orders.save(order)
        listeners.forEach { it.onOrderPlaced(order) }
    }
}
```

The problem is "after an order is saved, issue its invoice": one dependent, known in advance, required — the order is not placed without its invoice. Observer's intent and applicability (p. 293–294) describe a one-to-many dependency where the subject notifies dependents without assuming who they are. Here the subject must know: the reader can't find from `OrderService` who issues invoices, the ordering is implicit, and a failing listener's effect on the order is unclear. Drop the listener interface, give `InvoiceIssuer` a method named for its job, and call it directly:

```kotlin
class OrderService(private val orders: OrderRepository, private val invoices: InvoiceIssuer) {
    fun place(order: Order) {
        orders.save(order)
        invoices.issueFor(order)
    }
}
```

Observer becomes right when there are several independent reactions — a confirmation email, an analytics event — that `OrderService` shouldn't know about and that must not fail the order.

**Example: Strategy with one implementation and no selection (Java).**

```java
public interface ShippingFeeStrategy {
    Money feeFor(Cart cart);
}

public final class DefaultShippingFeeStrategy implements ShippingFeeStrategy {
    @Override
    public Money feeFor(Cart cart) {
        return cart.total().isAtLeast(FREE_SHIPPING_FROM) ? Money.ZERO : FLAT_FEE;
    }
}
// Wired once at startup; nothing ever picks a different strategy.
```

The problem is "charge a flat fee below a threshold and nothing above it". Strategy's intent and applicability (p. 315–316) describe a family of interchangeable algorithms, with a class configured with one of them. There is one algorithm and no choice, so the interface is a name with nothing behind it. Make it a method on `Cart` or a small concrete `ShippingFee` class. When a second rule arrives — express delivery, a per-region fee — extracting the interface takes minutes.

An interface with one production implementation is still right at a boundary the tests must fake: a clock, a payment gateway, a message broker. That is a port, and its variation — production versus test — exists today.

## Overkill

| Signal | Simpler code | When the pattern earns its place |
|---|---|---|
| An interface with one implementation that will never vary (`OrderService` + `OrderServiceImpl`) | The class alone. Spring proxies classes for `@Transactional` without an interface; Kotlin needs the `kotlin-spring` compiler plugin to open them | A second implementation exists, or it's a boundary the tests fake |
| A factory that only calls a constructor | The constructor, or a named factory function that validates | Creation picks among classes, or hides an expensive or pooled setup |
| A builder for two or three required properties | Kotlin: a constructor with named arguments. Java: a constructor, a static factory or a record | Many optional parts, or construction in steps (GoF Builder, p. 97, separates a construction process from the representations it produces) |
| Layers that only forward: controller → facade → service → manager → repository for a CRUD form | Remove the pass-through layers (the Middle Man smell) | A layer holds a rule, a transaction or a boundary |
| An abstract base class for two subclasses that share one helper | A function, or a collaborator both use | The subclasses are real subtypes callers substitute |
| An event bus, mediator or chain inside one module for calls that are synchronous, ordered and known | Direct calls in sequence | Senders and receivers are independent and their number varies |
| A Visitor over a hierarchy with one operation, or one you own and could seal | A method on each class; or a sealed type matched with a Kotlin `when` expression (`sealed interface` from 1.5) or Java pattern matching for `switch` (Java 21), so the compiler catches a missed case | Many unrelated operations over a stable hierarchy you can't seal, or Java before 21, where no `switch` over the cases is checked |

The cost is the same each time: more types to read, "go to implementation" landing on an interface, deeper stack traces, and flexibility nobody uses.

## Absorbed by the language

Kotlin and modern Java build several patterns in. Where the language gives you the pattern, the hand-written GoF structure is noise. The reverse holds too: on a version without the feature, the hand-written pattern is correct — don't flag it.

| Pattern | Kotlin | Java |
|---|---|---|
| Singleton | `object` declaration (Kotlin 1.0, *Kotlin in Action* §4.4.1) | An `enum` with one constant (Java 5) or the lazy holder idiom; better, one instance created at startup and injected |
| Builder | Named and default arguments (Kotlin 1.0, §3.2.1–3.2.2); `copy()` on a `data class` for variants (§4.3.2) | Records (Java 16) plus static factory methods; keep a fluent builder for many optional parts |
| Factory Method (as a named constructor) | Factory functions in a `companion object` (Kotlin 1.0, §4.4.2) or top-level functions | Static factory methods (any version), like `List.of` (Java 9); GoF's version, where subclasses decide the class, still needs classes |
| Strategy | Function types and lambdas (Kotlin 1.0, §8.1); a `fun interface` when the role needs a name (Kotlin 1.4) | A lambda for a functional interface such as `Comparator` or `Function` (Java 8) |
| Command | A lambda of type `() -> Unit` (Kotlin 1.0); keep a class when the command needs undo, or must be logged, replayed or serialized | `Runnable`, `Supplier` or `Callable` written as lambdas (Java 8); the same caveat applies |
| Template Method | A higher-order function that takes the varying step as a lambda (Kotlin 1.0, §8.1) | Pass the step as a lambda instead of subclassing (Java 8) |
| Iterator | Implement `Iterable`, return a `Sequence` (Kotlin 1.0), or build one with `sequence {}` (Kotlin 1.3) | `Iterable` for for-each (Java 5); streams (Java 8) |
| Observer | `Flow` (stable in `kotlinx.coroutines` 1.3), `StateFlow` / `SharedFlow` (stable in 1.4) — a library: check its version, not Kotlin's | `java.util.concurrent.Flow` (Java 9) for reactive streams, or a plain listener interface; `java.util.Observable` is deprecated (Java 9) |
| Decorator | Class delegation with `by` (Kotlin 1.0, §4.3.3): override only what you decorate | No shortcut: forward every method by hand |
| Visitor (over types you own) | A `sealed class` with `when` used as an expression (Kotlin 1.0); `sealed interface` (Kotlin 1.5); `when` statements are checked too from Kotlin 1.7 | Sealed types (Java 17) with pattern matching for `switch` (Java 21) |
| Prototype | `copy()` on a `data class` (Kotlin 1.0, §4.3.2) | A copy constructor or a method returning a modified copy; records (Java 16) make it short |
| Proxy (virtual) | `by lazy` (Kotlin 1.0, §7.5.2) | No lazy shortcut: the holder idiom or a memoizing `Supplier`; `java.lang.reflect.Proxy` (Java 1.3) for dynamic proxies of interfaces |
| Adapter (simple) | Extension functions (Kotlin 1.0, §3.3) — for a different call shape only; they can't make a type implement an interface | No shortcut: a wrapper class |

Two names cover different ideas than GoF's. The fluent builder common in Java code exists for optional parameters; GoF's Builder (p. 97) is about one construction process producing different representations. A static or companion factory is a named constructor; GoF's Factory Method (p. 107) lets subclasses choose the class. Judge each against the problem it actually solves.

## Named like a pattern but isn't

A pattern's name in a class name is a promise to the reader. When the code doesn't keep it, rename the class or change the code.

| Name | What it really is | Honest name or fix |
|---|---|---|
| `*Factory` that only calls a constructor | A constructor with an extra hop | Delete it and call the constructor, or a factory function if it validates or names a case |
| `*Strategy` with one implementation and no selection | A plain class or function | Name it after what it computes (`ShippingFee`); add the interface when a second strategy and a selector exist |
| `*Adapter` that adds behavior — caching, retries, logging | A Decorator: same interface, extra behavior | `CachingRateProvider`, `RetryingPaymentGateway`; an Adapter converts one interface to another and adds nothing |
| `*Proxy` that changes the interface | An Adapter, or a Facade over several objects | Name it for what it does; a Proxy keeps its subject's interface and controls access to it |
| `*Repository` that exposes SQL, query builders or the ORM's session, or returns rows | A DAO or a query service | Keep the repository in domain terms — `findOverdue(asOf)`, aggregates in and out — and call the other thing `*Dao` or `*Queries` |
| `*Manager`, `*Helper`, `*Util` that hide a god class | A bag of unrelated responsibilities | Split it by responsibility and name each part for its job (`InvoiceNumbering`, `LateFeeCalculator`) |
| `*Builder` whose every property is required | A constructor | A constructor with named arguments (Kotlin) or a record (Java 16) |

## Wrong for the version

Never suggest a feature newer than the project's version. Detect it first ([language registry](../../../languages/README.md)); in Kotlin, `languageVersion` / `apiVersion` cap it too. A Java preview feature counts only if the project already enables `--enable-preview`.

| Don't suggest | It needs | Before that, suggest |
|---|---|---|
| `record` | Java 16 (preview in 14–15) — not on Java 11 | A final class with final fields and hand-written `equals` / `hashCode` / `toString`, or Lombok `@Value` if the project already uses Lombok |
| Pattern matching for `switch`, record patterns | Java 21 (only previews before) — not on Java 17 | `instanceof` with a pattern variable (Java 16), or a classic Visitor when exhaustiveness matters |
| `sealed` classes and interfaces in Java | Java 17 | An abstract class with a package-private constructor, which closes the hierarchy to its package |
| `sealed interface` in Kotlin | Kotlin 1.5 — not on Kotlin 1.4 | A `sealed class` (Kotlin 1.0) |
| Relying on the compiler to flag a non-exhaustive `when` statement over a sealed type, enum or `Boolean` | Kotlin 1.7 (a warning in 1.6) | Use `when` as an expression — assign or return it — which is checked on every version |
| `@JvmInline value class` | Kotlin 1.5 | A `data class` wrapper |
| `data object` | Kotlin 1.9 | A plain `object`, overriding `toString` if it is printed |
| `fun interface` | Kotlin 1.4 | A function type |

## How to check a pattern fits

1. Write the problem in one sentence without the pattern's name.
2. Match it to the pattern's intent and applicability (GoF §1.7, p. 28; Table 1.2, p. 30), and read the pattern's own Applicability section, not only its diagram.
3. Name the variation the pattern encapsulates and show it exists today: the second implementation, the run-time choice, the test that needs a fake.
4. Check the language doesn't already give it to you on the project's version ([absorbed by the language](#absorbed-by-the-language), [wrong for the version](#wrong-for-the-version)).
5. Weigh the pattern's Consequences section against the simplest code: the types it adds, the indirection a reader must follow, what it makes harder to test or debug.
6. Prefer the simplest design that passes the tests. In `develop`, say in the PR description what would justify the pattern later; in a review, write that trigger into the finding.
7. Label the finding by cost. It is a major — must-fix — only when the misuse hides a likely bug, as in the Observer example, where nobody can tell whether a failed invoice fails the order. Otherwise extra types and indirection are a `suggestion:`.

## Sources

- Gamma, Helm, Johnson and Vlissides, *Design Patterns* (1994): §1.7 "How to Select a Design Pattern" and §1.8 "How to Use a Design Pattern" (p. 28–31), Table 1.2 (p. 30), and each pattern's Intent, Applicability and Consequences sections — Builder (p. 97), Factory Method (p. 107), Observer (p. 293), Strategy (p. 315)
- Dmitry Jemerov and Svetlana Isakova, *Kotlin in Action*: §3.2.1–3.2.2 (named and default arguments), §3.3 (extension functions), §4.3.2 (data classes and `copy`), §4.3.3 (class delegation), §4.4.1 (object declarations), §4.4.2 (companion objects), §7.5.2 (`by lazy`), §8.1 (higher-order functions and function types)
- Java versions from the JEP index — records (JEP 395), sealed classes (JEP 409), pattern matching for `switch` (JEP 441), `java.util.concurrent.Flow` (JEP 266); Kotlin versions from *What's new in Kotlin*, and `kotlinx.coroutines` versions from its release notes (the first two are linked from the [Java](../../../languages/java/README.md) and [Kotlin](../../../languages/kotlin/README.md) pages)
