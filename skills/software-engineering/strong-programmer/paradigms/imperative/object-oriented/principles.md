# Object-oriented principles

The ideas the design patterns are built on, the changes that force a redesign, and SOLID. Use them to explain *why* a piece of object-oriented code is hard to change — not as rules to apply everywhere.

## GoF principles

The Gang of Four state these in §1.6 "How Design Patterns Solve Design Problems" and §1.7. They distinguish an object's *class* (how it is implemented) from its *type* (the requests it answers); class inheritance shares implementation, interface inheritance shares type (p. 17). Everything below follows from keeping the two apart.

- **Program to an interface, not an implementation** (p. 18). Declare fields, parameters and return types as the type the code needs, so clients don't know or care which class they hold. A class has to be named somewhere to create the object — keep that at the edges (the wiring code, a factory), not inside business logic.
  - In review: `private val orders: JdbcOrderRepository` in a domain service; `ArrayList<Order>` or `HashMap<…>` in a public signature; `new SmtpMailer()` inside a use case.
  - The type can be a Kotlin or Java `interface`, an abstract class or a function type. It does not mean every class needs an interface — see [pattern misuse](pattern-misuse.md#overkill).
- **Favor object composition over class inheritance** (p. 20). Inheritance is white-box reuse fixed at compile time: the subclass sees and depends on its parent's internals, so a change in the parent can break it (GoF quote the saying that "inheritance breaks encapsulation", p. 19). Composition is black-box: objects are used only through their interfaces and can be swapped at run time.
  - In review: `class AuditedOrderService : OrderService()` just to add logging; a `BaseService` that exists to share helpers; `protected` mutable fields; Kotlin classes made `open` only so subclasses can borrow their helper methods.
  - Kotlin classes are final unless marked `open` (*Kotlin in Action* §4.1.2), which nudges toward composition. Inheritance still fits a real is-a that callers can substitute (see Liskov below) and a sealed hierarchy of cases.
- **Delegation** (p. 20–21) is what lets composition match inheritance for reuse: the receiving object forwards requests to a delegate it holds — GoF's window *has* a rectangle instead of *being* one. Forwarding by hand is tedious in Java; in Kotlin, class delegation with `by` generates it (*Kotlin in Action* §4.3.3), so you write only the methods you change:

  ```kotlin
  class AuditedOrders(private val inner: OrderRepository, private val audit: AuditLog) : OrderRepository by inner {
      override fun save(order: Order) {
          audit.record("saved ${order.id}")
          inner.save(order)
      }
  }
  ```

  GoF add a caveat: the more the wiring is decided at run time, the harder the code is to follow, so delegate where it simplifies.
- **Encapsulate the concept that varies** (§1.7, p. 28–29). Find what changes — an algorithm, which class gets created, a platform, a policy — and put it behind a stable interface so the rest of the code doesn't change with it. Table 1.2 (p. 30) lists what each pattern lets you vary.
  - In review: the same `when (country)` or `switch (plan)` in three classes; adding a payment method means editing five files.
  - The corollary matters just as much: encapsulate what varies *now*. An abstraction over something that has never varied is cost without benefit.

## The eight causes of redesign

GoF §1.6, "Designing for change" (p. 24–25), lists eight common reasons a design has to be reworked, each with the patterns that guard against it. Read it backwards in a review: when the code shows the signal, ask whether that change is actually coming. If it is, the patterns are candidates to evaluate, not orders.

| Cause | What it looks like in code | Patterns that address it |
|---|---|---|
| Creating an object by naming its class | `PostgresClient()` or `new SmtpMailer()` constructed inside a domain class, so it can't be reconfigured or tested without editing it | Abstract Factory, Factory Method, Prototype |
| Dependence on specific operations | The caller hard-codes which handler serves a request: `if (type == "refund") refunds.handle(r) else if (…)`, repeated wherever the request is made | Chain of Responsibility, Command |
| Dependence on hardware and software platform | Business code imports `java.io.File`, a cloud vendor's SDK, `android.*` or shells out to OS commands | Abstract Factory, Bridge |
| Dependence on object representations or implementations | Callers know how another object is stored or located: they read its internal `Map`, its JSON layout, its table columns, or bypass its cache | Abstract Factory, Bridge, Memento, Proxy |
| Algorithmic dependencies | A pricing, ranking or parsing algorithm inlined in the class that uses it, so tuning it means editing and retesting the caller | Builder, Iterator, Strategy, Template Method, Visitor |
| Tight coupling | Classes that can't be instantiated or tested without each other; package cycles; one change ripples through many files | Abstract Factory, Bridge, Chain of Responsibility, Command, Facade, Mediator, Observer |
| Extending functionality by subclassing | One subclass per combination — `EmailNotifier`, `RetryingEmailNotifier`, `RetryingLoggingEmailNotifier` — or overriding one method forces overriding another | Bridge, Chain of Responsibility, Composite, Decorator, Observer, Strategy |
| Inability to alter classes conveniently | The class comes from a library or generated code, or changing it would touch every subclass | Adapter, Decorator, Visitor |

## SOLID

Robert C. Martin's five principles of class design, each with its own chapter in *Agile Software Development* (2002).

| Principle | Means | Violation signals | Usual fix |
|---|---|---|---|
| Single responsibility | A class has one reason to change: it serves one concern or one group of people asking for changes | It changes for unrelated tickets; it imports persistence, HTTP and formatting at once; its name needs "And" or "Manager"; its tests mock many unrelated things | Extract Class along the reasons to change; move each behavior next to the data it uses |
| Open/closed | New behavior arrives by adding code, not by editing code that already works | Every new case edits the same `when` / `switch` in several places; adding a provider means changing a core class | Polymorphism or a function parameter at the point that varies. When the set of cases is closed and the operations grow, a sealed type the compiler checks: Kotlin `when` expressions (`sealed interface` from 1.5; `when` statements checked from 1.7), Java pattern matching for `switch` (Java 21; sealed types from Java 17). On older versions, keep the polymorphism or a Visitor |
| Liskov substitution | A subtype works anywhere its base type is expected, without the caller knowing which one it has | Overrides that throw `UnsupportedOperationException` or do nothing; `is` / `instanceof` checks before a call; a subtype that demands more of its inputs or promises less of its results | Stop inheriting: split the hierarchy, compose instead, or separate the read-only and mutable interfaces |
| Interface segregation | Clients depend only on the methods they use | Implementations with empty or throwing methods; a test fake that stubs fifteen methods to use one; one interface serving unrelated callers | Split it into role interfaces, one per kind of client; a class can still implement several |
| Dependency inversion | High-level policy doesn't depend on low-level details; both depend on an abstraction that the policy side owns | Domain code imports JDBC, JPA, an HTTP client or framework types; the interface lives next to its only implementation in the infrastructure package; a rule can't be tested without a database | Define the interface in the domain, in its terms; implement it in an adapter; wire the two together at startup |

SOLID is a review lens, not a checklist to maximize. Applied to every class on every axis, it produces the [overkill](pattern-misuse.md#overkill) it was meant to prevent. Use it to name the principle behind a concrete cost you can point to in this code.

## Review questions

- What varies here, and does it vary today — or only in someone's plans?
- Who depends on whom? Does the domain import a database, HTTP or framework type?
- Can this rule be tested without the database, the network or the clock?
- For this ticket, which classes change — and does anything unrelated change with them?
- If one more case arrives (a payment method, a country, a report format), how many files do I edit?
- Is this inheritance a real is-a that callers can substitute, or a way to reuse code?
- Does each client use the whole interface it depends on?
- Is this abstraction paying for itself, or is it there "just in case"?

## Sources

- Erich Gamma, Richard Helm, Ralph Johnson and John Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software* (1994): §1.6 "How Design Patterns Solve Design Problems" — class versus interface inheritance (p. 17), programming to an interface (p. 18), inheritance versus composition (p. 18–20), delegation (p. 20–21), designing for change and the causes of redesign (p. 24–25); §1.7 "How to Select a Design Pattern" (p. 28–29) and Table 1.2 (p. 30)
- Robert C. Martin, *Agile Software Development: Principles, Patterns, and Practices* (2002): the chapters on the single-responsibility, open-closed, Liskov substitution, dependency-inversion and interface-segregation principles (ch. 8–12)
- Dmitry Jemerov and Svetlana Isakova, *Kotlin in Action*: §4.1.2 (final by default), §4.3.3 (class delegation with `by`)
