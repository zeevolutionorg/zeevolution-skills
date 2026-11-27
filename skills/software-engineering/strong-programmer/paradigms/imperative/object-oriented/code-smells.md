# Code smells

Surface signs that a design may be making change harder: Fowler and Beck's 24 smells, then the object-oriented anti-patterns that come up most in Kotlin and Java reviews.

## How to use this list

- **A smell is a hint, not a verdict.** It says where to look. Confirm the cost in *this* code before flagging: which change does it make harder, or which bug does it invite? If you can't name the cost, don't raise it.
- **Judge by the approach.** A loop is normal in procedural or performance-critical code; a data-only class is normal at a boundary. Name the approach first ([paradigms](../../README.md)).
- **Name the refactoring.** Use the catalog name (Extract Function, Move Function…) and say where it applies, so the author knows the move, not just the complaint.
- **One finding per smell instance**, with file and line.
- **Label by cost.** Style-level smells — naming, comments, small duplication — are `nit:`. A smell that makes the change in hand harder is a `suggestion:`. It is a blocker or a major only when it hides a bug or breaks an invariant, such as mutable state shared between threads.
- **Keep it structural.** Fixing a smell is a tidying: a separate commit from the behavior change, and often a separate PR.

## Smells

From Fowler, *Refactoring* (2nd ed.), ch. 3, in the book's order. Fixes are named after the book's catalog of refactorings, with a Kotlin or Java note where the language helps.

| Smell | Signals | Usual fix | Principle |
|---|---|---|---|
| Mysterious Name | You need the body to know what it does: `data`, `process()`, `handle2`, `tmp`, `Util`; a name that no longer matches the behavior | Change Function Declaration, Rename Variable, Rename Field | Clear intent |
| Duplicated Code | The same logic, or the same shape with small differences, in several places; a bug fix that has to be copied | Extract Function, Slide Statements, Pull Up Method | One source of truth |
| Long Function | You scroll to read it; comments label its blocks; deep nesting; many local variables | Extract Function, Replace Temp with Query, Decompose Conditional, Split Loop, Replace Function with Command | Single responsibility |
| Long Parameter List | Four or more parameters, several of the same type, or a flag that switches behavior; Kotlin named arguments make the call readable but don't cure it | Introduce Parameter Object, Preserve Whole Object, Replace Parameter with Query, Remove Flag Argument, Combine Functions into Class | Cohesion |
| Global Data | Mutable state in an `object`, a `companion object` or a `static` field, read and written from anywhere | Encapsulate Variable; inject the dependency instead | Encapsulation |
| Mutable Data | `var` or non-final fields changed from several places; collections shared and mutated; setters called long after construction | Encapsulate Variable, Split Variable, Separate Query from Modifier, Remove Setting Method, Change Reference to Value | Encapsulation |
| Divergent Change | One class edited for unrelated reasons: these methods change for a new database, those for a new tax rule | Split Phase, Extract Class, Move Function | Single responsibility |
| Shotgun Surgery | One change edits many classes a little each: a new field touches the DTO, the mapper, the entity, the validator and three services | Move Function, Move Field, Combine Functions into Class, Inline Class | Encapsulate the concept that varies |
| Feature Envy | A method that uses another object's getters more than its own fields: `order.customer.address.country` read to compute something the customer should know | Move Function, Extract Function | Tell, don't ask |
| Data Clumps | The same three or four values always travel together: `street, city, zip`; `amount, currency`; `from, to` | Extract Class, Introduce Parameter Object, Preserve Whole Object | Cohesion |
| Primitive Obsession | `String` for emails, ids and currency codes; `Long` for money; `Int` status codes; the same validation repeated wherever they are used | Replace Primitive with Object (a `data class`, a value class from Kotlin 1.5, or a record from Java 16 — see [value objects](domain-driven-design.md#building-blocks)), Replace Type Code with Subclasses | Value objects |
| Repeated Switches | The same `when` / `switch` on the same type code in several places, each needing an edit for a new case | Replace Conditional with Polymorphism. Or a sealed type the compiler checks for missing cases: Kotlin `when` expressions over a `sealed class` (`sealed interface` from Kotlin 1.5; `when` statements checked from 1.7), Java pattern matching for `switch` over a sealed type (Java 21). On older versions, keep the polymorphism | Open/closed |
| Loops | One `for` loop that filters, transforms and accumulates in a single body | Replace Loop with Pipeline: `filter` / `map` / `fold`, or streams (Java 8) | Declarative intent |
| Lazy Element | A class or function that doesn't earn its keep: a wrapper that only forwards, a hierarchy with one trivial subclass | Inline Function, Inline Class, Collapse Hierarchy | Simplicity |
| Speculative Generality | Hooks, parameters, abstract classes or type parameters "for later", with one user or used only by tests. A port the tests fake at a real boundary (a clock, a payment gateway) is not speculative | Collapse Hierarchy, Inline Function, Inline Class, Change Function Declaration, Remove Dead Code | Simplicity — see [overkill](pattern-misuse.md#overkill) |
| Temporary Field | A field set only in some situations and `null` or `lateinit` the rest of the time | Extract Class, Move Function, Introduce Special Case | Cohesion |
| Message Chains | `a.getB().getC().getD()`; `invoice.order.customer.account.email` | Hide Delegate, Extract Function, Move Function | Law of Demeter |
| Middle Man | A class whose methods mostly forward to one other object | Remove Middle Man, Inline Function, Replace Superclass with Delegate | Simplicity |
| Insider Trading | Two classes trading internals: one reads or writes the other's fields or depends on its call order; subclasses reaching into `protected` state | Move Function, Move Field, Hide Delegate, Replace Subclass with Delegate | Encapsulation |
| Large Class | Many fields and methods; groups of fields used by different groups of methods; a test that needs a huge setup | Extract Class, Extract Superclass, Replace Type Code with Subclasses | Single responsibility |
| Alternative Classes with Different Interfaces | Two classes doing the same job with different method names (`send` and `dispatch`), so callers can't swap them | Change Function Declaration, Move Function, Extract Superclass (or extract a shared interface) | Program to an interface |
| Data Class | Only fields and accessors, while the logic about that data lives in other classes; fine for DTOs at a boundary and for immutable values | Encapsulate Record, Remove Setting Method, Move Function, Split Phase | Tell, don't ask |
| Refused Bequest | A subclass that ignores what it inherits, or overrides it to throw `UnsupportedOperationException` | Push Down Method, Push Down Field, Replace Subclass with Delegate, Replace Superclass with Delegate | Liskov substitution |
| Comments | Comments that explain what confusing code does, or apologize for it; comments that say *why* are fine | Extract Function, Change Function Declaration, Introduce Assertion | Clear intent |

The principles behind the last column are in [principles](principles.md).

## Object-oriented anti-patterns

| Anti-pattern | Signals | Why it hurts | Fix |
|---|---|---|---|
| God class | One class (`OrderManager`, `ApplicationService`) that knows and does most of a module; thousands of lines; a dozen injected dependencies; most tickets touch it | Every change risks unrelated behavior; constant merge conflicts; it can't be tested in isolation | Extract Class by responsibility, moving behavior to the objects that own the data, one tidying at a time |
| Anemic domain model | Entities that are only getters and setters while `*Service` classes hold every rule about them | Rules are duplicated across services and drift apart; any caller can put the object in an invalid state | Move the rules into the entity or value object; keep services for operations that belong to no single object ([building blocks](domain-driven-design.md#building-blocks)) |
| Inheritance for reuse | `: BaseService()` or `extends AbstractController` to get helper methods; subclasses that callers couldn't substitute for the parent | Couples subclasses to the parent's internals; every change to the parent ripples down; behavior can't be swapped at run time | Compose: inject the helper or delegate to it (Kotlin `by`); keep inheritance for real subtypes |
| Singleton as global state | `object Settings { var … }` or `getInstance()` called deep inside business logic; tests that pass alone and fail together | A hidden dependency; mutable state shared across tests and threads; can't be replaced in a test | Create one instance at startup and inject it; make it immutable. A stateless Kotlin `object` is fine |
| Service locator | `ServiceLocator.get(PaymentGateway::class)` or `context.getBean(…)` inside business code | Dependencies don't show in the constructor; a missing one fails at run time, not at wiring time; tests must set up a global registry | Constructor injection; let the framework or the startup code do the wiring |
| Tell, don't ask violations | Callers read an object's state through getters to make a decision the object should make: `if (account.balance >= amount) account.balance -= amount` | The rule scatters across callers and drifts; the object can't protect its invariant | Move the decision into the object: `account.withdraw(amount)` |
| Boolean flag parameters | `send(message, true)`, `export(report, false, true)`; the body is `if (flag) … else …` | Call sites don't say what they do; one function doing two jobs | Remove Flag Argument: two named functions, or an enum; named arguments help reading but leave the double duty |

## Sources

- Martin Fowler, *Refactoring: Improving the Design of Existing Code*, 2nd ed. (2018), ch. 3 "Bad Smells in Code" (written with Kent Beck), and the book's catalog for the refactoring names
- Eric Evans, *Domain-Driven Design* (2003), ch. 5: services, and why domain behavior belongs in entities and value objects rather than being pulled out of them
- Gamma, Helm, Johnson and Vlissides, *Design Patterns* (1994), §1.6, p. 19–20: inheritance versus composition
