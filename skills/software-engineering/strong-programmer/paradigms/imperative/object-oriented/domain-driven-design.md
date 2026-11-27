# Domain-driven design building blocks

Evans' building blocks for putting business rules into objects named after the business — entities, value objects, aggregates and repositories — plus two aggregate rules that Vaughn Vernon added later. Use them where the code has real rules to protect. A form that saves rows to one table doesn't need aggregates.

## Building blocks

| Block | What it is | Signs it's done well | Common mistakes |
|---|---|---|---|
| Entity | An object defined by its identity, which stays the same while its attributes change: an order is the same order after it ships. Two entities are equal when their ids are | The id exists from creation; `equals` / `hashCode` use the id only; state changes through named methods (`order.ship()`) that check the rules | Data-class equality over every field; an id generated only on save, so every new entity looks equal (all `null` ids); a public setter for every field; an entity for something that has no identity, such as an amount of money |
| Value object | Something that describes, with no identity of its own: `Money`, `EmailAddress`, `DateRange`. Immutable, equal when its values are equal, and it validates itself | It can't be built invalid; operations return new values (`total.plus(fee)`); it replaces bare primitives across signatures | Mutable fields; validation repeated in each service instead of in the value; `String` and `BigDecimal` passed around instead (Primitive Obsession); an id field on a value |
| Aggregate | A cluster of entities and values changed as one unit, with one root entity as the only way in. It is the consistency boundary: its invariants hold whenever a change completes | Every rule about the cluster is enforced by methods on the root. Later practice (Vernon): it stays small, one transaction changes one aggregate, and other aggregates are referenced by id | Outside code changing children directly (`order.lines.add(…)`); one transaction updating two aggregates; object references between aggregates (an ORM `@ManyToOne` to another root); huge aggregates loaded whole for every change |
| Repository | Collection-like access to aggregates: add, find by id or by domain criteria, remove — while storage stays hidden | One per aggregate root; an interface in domain terms (`findOverdue(asOf)`) that lives with the domain; it returns whole aggregates | One per table or per child entity; query builders, SQL fragments or ORM types in the interface; methods named after columns; returning rows or DTOs; business rules inside it |

Evans draws the aggregate boundary and lets objects inside it hold references to other roots; the one-aggregate-per-transaction and reference-by-id rules come from Vernon's *Implementing Domain-Driven Design* (2013), ch. 10. Evans also covers services and modules (ch. 5) and factories (ch. 6). Strategic design — bounded contexts, context maps, a shared language across teams — isn't covered yet.

## In Kotlin and Java

**Value objects.** In Kotlin, a `data class` with its checks in `init`; `copy()` goes through the primary constructor, so copies are checked too. For a single wrapped value, an `@JvmInline value class` (Kotlin 1.5) costs no allocation in most uses. In Java, a record with a compact constructor (Java 16); before that, a final class with final fields and `equals` / `hashCode` over all of them.

```kotlin
@JvmInline
value class EmailAddress(val value: String) {
    init { require('@' in value) { "not an email address: $value" } }
}

data class Money(val cents: Long, val currency: Currency) {
    operator fun plus(other: Money): Money {
        require(currency == other.currency) { "cannot add $currency and ${other.currency}" }
        return Money(cents + other.cents, currency)
    }
}
```

```java
public record DateRange(LocalDate start, LocalDate end) {
    public DateRange {
        Objects.requireNonNull(start);
        Objects.requireNonNull(end);
        if (end.isBefore(start)) throw new IllegalArgumentException("end before start");
    }

    public boolean contains(LocalDate day) {
        return !day.isBefore(start) && !day.isAfter(end);
    }
}
```

Watch `BigDecimal` inside a value object: its `equals` compares scale, so `1.0` and `1.00` are not equal. Normalize the scale on creation, or store minor units as above.

**Entities.** Write `equals` and `hashCode` over the id; don't use a `data class` or a record, whose generated equality covers every field. Assign the id when the object is created (a UUID, or one from a sequence) so equality holds before the first save. ORM entities have extra needs — a no-argument constructor, non-final classes (the `kotlin-jpa` and `kotlin-allopen` compiler plugins provide both in Kotlin) — so keep those details out of the domain class when you can.

**Aggregates.** No public setters. The root exposes methods that enforce the invariants and hands out copies of its children, so callers can't change them behind its back:

```kotlin
class Order(val id: OrderId) {
    private val _lines = mutableListOf<OrderLine>()
    val lines: List<OrderLine> get() = _lines.toList()
    var status = OrderStatus.OPEN
        private set

    fun add(line: OrderLine) {
        check(status == OrderStatus.OPEN) { "order $id is $status" }
        _lines += line
    }

    override fun equals(other: Any?) = other is Order && other.id == id
    override fun hashCode() = id.hashCode()
}
```

**Repositories.** The interface lives with the domain and speaks its language; the JPA or JDBC implementation lives outside it, and the domain never imports it. Extending a framework repository (`JpaRepository<OrderEntity, UUID>`) inside the domain leaks persistence into it — keep it behind your own interface. Where each piece goes is the subject of layers and hexagonal architecture, planned for a later version of this map.

```kotlin
interface OrderRepository {
    fun find(id: OrderId): Order?
    fun findOverdue(asOf: LocalDate): List<Order>
    fun save(order: Order)
}
```

## Review questions

- Is this a value or an entity? Would two of them with the same data be the same thing?
- What invariant does this aggregate protect — and can any code path change its children without going through the root?
- Does a transaction touch two aggregates? Should the second change happen afterwards, through an event or a job?
- Can this value object be constructed invalid, through a constructor, `copy()` or deserialization?
- Do the entity's `equals` and `hashCode` use the id only, and is the id set before the first save?
- Does the repository interface speak the domain's language, or SQL and the ORM's?
- Do the rules live in the objects, or in services that read their getters (an [anemic domain model](code-smells.md#object-oriented-anti-patterns))?
- Is this worth modeling at all, or is it a form over a table?

## Sources

- Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software* (2003), Part II "The Building Blocks of a Model-Driven Design": ch. 5 "A Model Expressed in Software" (entities, value objects, services, modules) and ch. 6 "The Life Cycle of a Domain Object" (aggregates, factories, repositories)
- Vaughn Vernon, *Implementing Domain-Driven Design* (2013), ch. 10 "Aggregates": change one aggregate per transaction, reference other aggregates by identity, keep aggregates small
- Language versions: value classes from *What's new in Kotlin* (1.5); records from the JEP index (JEP 395, Java 16)
