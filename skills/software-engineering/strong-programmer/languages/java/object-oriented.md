# Java for object-oriented code

What good object-oriented Java looks like in a review, what to flag, and which GoF patterns the language now covers. Every version tag comes from [Java features by version](versions.md): never suggest a feature above the project's version. Whether a pattern fits the problem at all is in [pattern misuse](../../paradigms/imperative/object-oriented/pattern-misuse.md).

## Idioms that matter in review

**Immutable classes with `final` fields** — expect `private final` fields set once in the constructor, no setters, and defensive copies of mutable inputs: `List.copyOf` (Java 10), or `Collections.unmodifiableList(new ArrayList<>(source))` on Java 8–9. Flag setters on value-like objects and getters that hand out an internal mutable collection.

**Records for value data (Java 16)** — expect a record for data identified by its values, with validation and copies in the compact constructor. Flag records with mutable components, records used as JPA entities (entities must not be final and need a no-argument constructor), and records grown into god objects with many unrelated methods.

```java
import java.util.List;
import java.util.Objects;

public record Order(String id, List<String> skus) {
    public Order {
        Objects.requireNonNull(id, "id");
        if (skus.isEmpty()) {
            throw new IllegalArgumentException("an order needs at least one item");
        }
        skus = List.copyOf(skus);
    }
}
```

**Sealed hierarchies (Java 17) with pattern matching for `switch` (Java 21)** — expect a closed set of cases as a `sealed` interface with one record or final class per case, matched in a `switch` with no `default`, so adding a case breaks the build where it must be handled. On Java 17–20, `sealed` closes the hierarchy but no `switch` over it is checked: keep a polymorphic method or a Visitor. Below Java 17, an abstract class with a package-private constructor closes the hierarchy to its package.

```java
sealed interface PaymentResult permits Approved, Declined {}

record Approved(String authorizationCode) implements PaymentResult {}

record Declined(int declineCode, boolean retryable) implements PaymentResult {}

final class CheckoutMessages {
    static String forCustomer(PaymentResult result) {
        return switch (result) {
            case Approved a -> "Payment approved (authorization " + a.authorizationCode() + ")";
            case Declined d when d.retryable() -> "Payment declined, please try again";
            case Declined d -> "Payment declined with code " + d.declineCode();
        };
    }
}
```

**Interfaces with default methods (Java 8) and private methods (Java 9)** — expect defaults that let a published interface grow without breaking implementers, and private methods that share code between them. Flag defaults that need state the interface can't hold, and interfaces used only to hold constants.

**Static factory methods over public constructors** — expect named creation where the name says something the constructor can't: `Money.ofCents(1250)`, `Order.draft(customerId)`, `List.of(...)` (Java 9). A factory can validate, cache, or return a subtype. Flag a factory that only calls `new` and adds no name, check or choice.

**Enums with behavior instead of type codes** — expect an `enum` whose constants carry their own data and behavior (fields, constant-specific methods, or a lambda per constant from Java 8), plus `EnumMap` and `EnumSet` for lookups. Flag `int` or `String` codes with the same `switch` repeated in several places.

**`equals`, `hashCode` and `toString` contracts** — expect `equals` and `hashCode` overridden together over the same fields (`Objects.equals` and `Objects.hash`, Java 7), or a record that generates all three (Java 16). Flag one without the other, equality over mutable fields of objects kept in hash-based collections, and `equals` on a non-final class that a subclass can break; make the class `final`.

**Composition over inheritance; classes `final` by default** — expect a class that is `final` unless it was designed for extension, and reuse through a field it delegates to. Flag subclassing a concrete class to reuse one method, and constructors that call overridable methods. From Java 25, a subclass constructor can validate and assign its own fields before `super(...)`.

**Constructor injection** — expect dependencies as `private final` fields passed through the constructor, so the object is complete once built and tests can pass fakes. Flag framework annotations on fields, setters used only for wiring, and static lookups of collaborators.

**`Optional` as a return type only (Java 8)** — expect `Optional<Customer> findById(...)` for a result that may be absent, consumed with `map`, `orElse` or `orElseThrow()` (Java 10). Flag `Optional` fields and parameters, `Optional` wrapping a collection (return an empty one), and `get()` without a check.

**Unmodifiable collections across boundaries** — expect returned collections to be unmodifiable: `List.of` (Java 9), `List.copyOf` (Java 10), `Stream.toList()` (Java 16), or `Collections.unmodifiableList(new ArrayList<>(items))` on Java 8. Flag getters that return the internal list callers can change.

**try-with-resources** — expect every `AutoCloseable` (streams, connections, locks wrapped in a resource) closed by `try (...)` (Java 7), naming an existing effectively final variable from Java 9. Flag `close()` calls in hand-written `finally` blocks.

**Checked and unchecked exceptions at boundaries** — expect checked exceptions only for conditions the caller can recover from, unchecked ones for programming errors, and low-level exceptions (`SQLException`, `IOException`) translated into the caller's terms at the layer boundary. Lambdas (Java 8) can't throw checked exceptions through the `java.util.function` interfaces, so wrap them where they cross. Flag `throws Exception`, empty `catch` blocks, and exceptions used for normal control flow.

**`var` only where the type is obvious (Java 10)** — expect `var` when the right-hand side names the type (`var orders = new ArrayList<Order>()`). Flag it where the reader must open another file to know the type (`var result = service.process(input)`).

## Pitfalls

- **Mutable objects as map keys or set members.** If a field used by `hashCode` changes after insertion, the entry can no longer be found. Keys must be immutable.
- **`Optional` fields and parameters.** `Optional` is not `Serializable`, adds a third state (`null`, empty, present) to every parameter, and its API note intends it mainly as a return type.
- **`equals` without `hashCode`.** Equal objects land in different hash buckets, so `HashSet` and `HashMap` keep duplicates and miss lookups.
- **Extending concrete classes.** A subclass depends on which of its parent's methods call which; a change in the parent breaks it silently. Prefer composition, or design the parent for extension and document its self-use.
- **`protected` fields.** They make every subclass part of the class's implementation; keep fields `private` and expose behavior.
- **Records with mutable components.** A record holding an `ArrayList` or an array is only shallowly immutable, and arrays compare by identity in the generated `equals`. Copy in the compact constructor, or use an unmodifiable type.
- **Java serialization of domain objects.** Deserialization of an ordinary class bypasses its constructors and their checks. Prefer an explicit format (JSON, Protocol Buffers) at boundaries; records are safer because deserialization goes through their canonical constructor.
- **Calling overridable methods from a constructor.** The subclass override runs before the subclass's fields are set and sees `null` or zero.
- **`==` on boxed numbers.** `Integer.valueOf` always caches -128 to 127, so `==` happens to work for small values and may fail outside that range. Use `equals`, or primitives.
- **`synchronized` around blocking calls on virtual threads, Java 21–23.** The virtual thread stays pinned to its platform thread for the whole call; suggest a `ReentrantLock` there. From Java 24 (JEP 491) this is no longer a problem.
- **`Date` and `Calendar` in new code.** Mutable and error-prone; use `java.time` (Java 8), converting at the edges with `Date.from(instant)` and `date.toInstant()` where an old API needs them.
- **Swallowing `InterruptedException`.** Catching it and carrying on loses the cancellation request. Restore the flag with `Thread.currentThread().interrupt()` or rethrow.
- **`Collections.unmodifiableList` taken for a copy.** It is a read-only view: changes to the backing list show through. Copy first, or use `List.copyOf` (Java 10).

## Patterns the language absorbs

Where Java gives you the pattern, the hand-written GoF structure is noise; on a version without the feature, the hand-written pattern is correct, as long as the problem calls for it ([pattern misuse](../../paradigms/imperative/object-oriented/pattern-misuse.md)). "Any" means every covered version (Java 8 and later).

| Pattern | Java feature | Since | Review note |
|---|---|---|---|
| Abstract Factory | Still a class-level design: an interface with one creation method per product, one implementation per family | Any | A dependency-injection configuration often plays this role; with one product and no family, a `Supplier<T>` (Java 8) is enough |
| Builder | A constructor or static factory methods for a few parts, or a record (Java 16); a fluent builder for many optional parts | Any; records Java 16 | Below Java 16, a constructor or a static factory is still the answer for two or three parts; a fluent builder earns its place only with many optional parts. GoF's Builder (p. 97) separates a construction process from its representations, a different idea from the fluent builder for optional parameters |
| Factory Method | Static factory methods as named constructors, like `List.of` (Java 9) | Any | GoF's Factory Method (p. 107) lets subclasses choose the class and still needs classes; a static factory is a named constructor |
| Prototype | A copy constructor, or a method returning a modified copy; records (Java 16) make both short | Any; records Java 16 | Below Java 16, a copy constructor or a `withX` method on a final class with final fields; on every version, prefer these to `Cloneable` and `clone()`, whose contract is easy to get wrong |
| Singleton | An `enum` with one constant, or the lazy holder idiom | Java 5 | Better still: one instance created at startup and injected; a static instance with mutable state is [Singleton as global state](../../paradigms/imperative/object-oriented/code-smells.md) |
| Adapter | No shortcut: a wrapper class implementing the target interface | Any | When the target is a functional interface, a method reference is the whole adapter (Java 8): `Supplier<Instant> now = clock::instant` |
| Bridge | Still a class-level design | Any | Two hierarchies that vary independently; check that both dimensions vary today |
| Composite | Still a class-level design; a sealed interface (Java 17) of records can model a closed tree | Any | Keep child management off the leaf type; recursive operations over a sealed tree read well as a `switch` (Java 21) |
| Decorator | No shortcut: implement the interface and forward every method by hand | Any | For a functional interface, a lambda that wraps the original is the decorator (Java 8); over a wide interface, ask whether a narrower one would do |
| Facade | Still a class-level design | Any | One entry point over a subsystem; a facade that forwards each call one to one is a Middle Man |
| Flyweight | `Integer.valueOf` caching and `String.intern`; for your own types, a static factory backed by a cache (`Map.computeIfAbsent`, Java 8) | Java 5 | Flyweights must be immutable; never compare them, or any boxed value, with `==` |
| Proxy | `java.lang.reflect.Proxy` for dynamic proxies of interfaces; for a virtual proxy, the holder idiom or a memoizing `Supplier` | Java 1.3 | No standard lazy value up to Java 25 (stable values are preview); a proxy keeps its subject's interface, and one that changes it is an Adapter |
| Chain of Responsibility | Still a class-level design; stateless handlers can be a list of lambdas tried in order (Java 8) | Any | Servlet filters and interceptors are this pattern; for a fixed, known sequence, direct calls are simpler |
| Command | `Runnable`, `Supplier`, `Callable` or your own functional interface, written as lambdas | Java 8 | Keep a class when the command needs undo, or must be logged, replayed or serialized |
| Interpreter | A sealed interface of records for the expression tree (Java 17), evaluated with a pattern-matching `switch` (Java 21) | Java 21 | Below Java 21, an `interpret` method on each node class; past a small grammar, a parser library |
| Iterator | `Iterable` for for-each; streams (Java 8) | Java 5 | Return a stream or an unmodifiable collection rather than exposing internals; hand-write an `Iterator` only for lazy traversal of your own structure |
| Mediator | Still a class-level design | Any | Inside one module, for calls that are synchronous, ordered and known, direct calls are simpler |
| Memento | An immutable snapshot class, or a record (Java 16) | Any; records Java 16 | Below Java 16, a small nested or package-private class with private final fields; record accessors are public, so nest the record or keep it package-private too, to keep the snapshot opaque to callers |
| Observer | `java.util.concurrent.Flow` for reactive streams, or a plain listener interface that takes lambdas | Java 9 | `java.util.Observable` is deprecated since Java 9; with one known listener, call it directly |
| State | A sealed interface with one record per state (Java 17), transitions in a `switch` (Java 21); or an enum with constant-specific behavior when states carry no data | Java 17 | Below Java 17, state classes behind an interface, or the enum |
| Strategy | A lambda for a functional interface such as `Comparator` or `Function` | Java 8 | Name your own functional interface when the role matters; one strategy with no selection is a plain method |
| Template Method | Pass the varying step as a lambda instead of subclassing | Java 8 | Keep the abstract class only when several steps vary together and subclasses are real subtypes |
| Visitor | Sealed types (Java 17) matched with pattern matching for `switch` (Java 21) | Java 21 | Below Java 21 no `switch` over the cases is checked, so the classic Visitor is right where exhaustiveness matters; it also stays right for hierarchies you can't seal |

Pattern pages are from Gamma, Helm, Johnson and Vlissides, *Design Patterns* (1994); versions are from the JEP index and the Java SE API docs, as listed in [Java features by version](versions.md).
