# Object-oriented

Objects bundle state with the behavior that guards it, and collaborate by sending each other requests through interfaces.

## Core idea

A program is a set of objects, each with an identity, private state and operations. Callers ask an object to do something instead of reaching into its data, so the rules about that data live in one place. Polymorphism lets one request run different code depending on who receives it, so a new variant can arrive as a new class rather than a new branch in old code.

**Two kinds of inheritance.** *Design Patterns* by the Gang of Four (GoF: Gamma, Helm, Johnson and Vlissides) separates an object's *class* — how it is implemented — from its *type* — the set of requests it can answer. Class inheritance defines one implementation in terms of another; it shares code. Interface inheritance, or subtyping, only says that one object can be used where another is expected (*Design Patterns*, §1.6, p. 16–17). Kotlin and Java make the split explicit with `interface` and `class`: depend on the interface, and inherit an implementation only on purpose.

**Why composition comes first.** A subclass sees its parent's internals and breaks when they change, and the link between them is fixed at compile time. Composed objects meet only through interfaces and can be swapped at run time, which keeps each class small and encapsulated. Hence GoF's second principle, "Favor object composition over class inheritance" (p. 20), with delegation (p. 20–21) giving composition the reuse that inheritance promised. The principles in full: [Principles](principles.md).

Base definitions: [the paradigms overview](../../README.md#sources).

## Primitives

| Primitive | What it gives you |
|---|---|
| Object: identity, state, behavior | Something you hold a reference to, whose state changes only through its own operations |
| Class | The implementation: fields, constructors, method bodies |
| Interface (type) vs class (implementation) | A contract callers depend on, separate from any one implementation (GoF, p. 16–17) |
| Encapsulation | Invariants enforced in one place; callers can't put the object into an invalid state |
| Polymorphism and dynamic binding | The receiver's class, known only at run time, decides which code a call runs |
| Composition and delegation | Behavior assembled from parts held in fields, with requests forwarded to them; parts can be swapped at run time (GoF, p. 20) |

## Strengths and costs

| Strengths | Costs |
|---|---|
| Data and the rules guarding it live together | More types and indirection to navigate |
| New variants as new classes, not edits to old ones | Class hierarchies harden early and are costly to reshape |
| Interfaces give seams for tests and adapters | Shared mutable objects are hard to reason about across threads |
| Maps naturally onto domain concepts | Easy to over-design: one-implementation interfaces, patterns without a problem |

## Signals the code is in this style

- Classes with private fields and public methods that change them under rules.
- Interfaces with several implementations, passed in through constructors.
- Calls whose target is chosen at run time: `notifier.send(message)` where `notifier` is an interface.
- Class hierarchies, `abstract` classes, `override`.
- Pattern names in type names: `*Factory`, `*Strategy`, `*Adapter`, `*Decorator`.

## Common failure modes

- **Anemic model.** Domain classes are bags of getters and setters, and the rules live in `*Service` classes that pull data out, decide and push it back. Fix: move each rule into the object that owns the data — `order.cancel(reason)` instead of `orderService.cancel(order)` setting three fields.
- **God class.** One class with a dozen dependencies and methods spanning unrelated concerns; every change touches it. Fix: split by responsibility — the groups of fields used together point to the new classes.
- **Deep inheritance trees.** Four or more levels, where understanding one method means reading every ancestor and overrides call `super` in a fragile order. Fix: flatten; turn levels into composed collaborators, or into a sealed hierarchy of small cases.
- **Getters and setters for everything instead of behavior.** Every field exposed, so callers enforce the invariants — or forget to. Fix: replace sequences of setters with methods named after the intent (`account.freeze()`), and expose only what callers need to read.
- **Inheritance used for code reuse.** `class ReportMailer extends HttpClient` to borrow one method; the subclass inherits a whole interface it doesn't honor. Fix: hold the collaborator in a field and call the one method you need; inherit only to express a real subtype. Kotlin's `by` forwards every member of an interface, so use it only when the class should expose that whole interface.

## Review questions

1. Does each class own the rules for its own data, or do services manipulate it from outside?
2. Would every subclass work wherever its parent is expected (Liskov substitution, in [Principles](principles.md))?
3. Does inheritance express a subtype, or does it just borrow code that composition could provide?
4. Do callers depend on interfaces, and does each interface earn its place — several implementations, a test seam, a layer boundary?
5. Can the public API put the object into an invalid state?
6. Is each design pattern solving a problem this code actually has? See [Pattern misuse](pattern-misuse.md).
7. Which [code smells](code-smells.md) does the change add or remove?

## Languages

| Language | Support |
|---|---|
| Kotlin | Classes and members final by default, `open` to allow overriding; interfaces with default method bodies; `data` classes; `sealed` classes for closed hierarchies (sealed interfaces since Kotlin 1.5); `object` for singletons and companion objects; class delegation with `by` (*Kotlin in Action*, ch. 4, §4.1–4.4) |
| Java | Classes, open unless `final`; interfaces with `default` methods (Java 8); records (Java 16); sealed classes and interfaces (Java 17) |

Version detection and what each language offers: [`languages/README.md`](../../../languages/README.md).

## Branches

- [Principles](principles.md) — GoF principles, the eight causes of redesign, SOLID
- [Code smells](code-smells.md) — Fowler's smells and object-oriented anti-patterns
- [Pattern misuse](pattern-misuse.md) — the right pattern for the wrong problem
- [Domain-driven design](domain-driven-design.md) — entities, value objects, aggregates, repositories
- 🔜 Design patterns (planned) — creational, structural, behavioral

Back to [imperative programming](../README.md).
