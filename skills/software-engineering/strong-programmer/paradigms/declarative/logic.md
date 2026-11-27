# Logic

State facts and rules about the problem; an engine searches for the answers that follow from them.

## Core idea

A logic program is a knowledge base — facts that hold and rules that derive new facts — plus queries that ask what follows from them. The engine, not the programmer, decides the search: it matches a query against rules by unification and backtracks when a path fails. Prolog and Datalog are the classic languages. In Kotlin and Java systems the style appears as rules engines, policy languages and constraint solvers running beside ordinary code, and it is judged by how cleanly that boundary is drawn.

Base definitions: [the paradigms overview](../README.md#sources).

## Primitives

| Primitive | What it gives you |
|---|---|
| Fact | A statement taken as true: `owner(doc_17, user_42).` |
| Rule | A way to derive new facts from existing ones: `can_edit(U, D) :- owner(D, U).` |
| Query or goal | A question the engine answers by finding bindings that make it true: `?- can_edit(user_42, D).` |
| Unification | Two terms made equal by binding their variables — pattern matching that works in both directions |
| Backtracking and resolution | Resolution chains a goal back through rules to facts; when a branch fails, the engine undoes its bindings and tries the next rule |
| Closed-world assumption | Anything the knowledge base can't prove counts as false |
| Negation as failure | `not(P)` succeeds when `P` can't be proved, not when `P` is known false — so adding a fact can turn a yes into a no |

## Strengths and costs

| Strengths | Costs |
|---|---|
| Rules read close to the policy or regulation they encode | The order of execution is hidden; performance depends on the engine's search |
| A new rule can extend behavior without touching control flow | Interactions between many rules are hard to predict and debug |
| Decisions can be explained: which rules fired, and on which facts | Few developers know the style; tooling and tests are thinner than for ordinary code |
| Policies can change without a code release when rules are data | A rule change is a production change, and needs the same review and tests |

## Signals the code is in this style

- `.drl` files and calls like `insert` / `fireAllRules` (Drools); `.rego` files and calls to a policy engine; Datalog queries; constraint models handed to a solver.
- Code that gathers facts, hands them to an engine and reads decisions back.
- Rules carrying priority or salience attributes, or names numbered to force an order.
- Rules edited by domain experts rather than by the developers.

## Common failure modes

- **Rule explosion.** Hundreds of near-identical rules, one per combination of inputs, and nobody can say which one fires. Fix: derive intermediate facts that capture shared conditions, use decision tables for combinations, and delete rules no test exercises.
- **Hidden ordering between rules.** Results depend on priorities or file order, so adding a rule changes unrelated outcomes. Fix: make rules independent of each other; where order is real, model it as explicit phases (agenda groups, separate policies) and test it.
- **Imperative steps encoded as rules.** Rules set flags only so the next rule fires, simulating a loop or a workflow. Fix: keep sequences in code and give the engine only the decisions.
- **Rule sets without tests.** Rules change in a console or a config repository and ship without review, then break decisions in production. Fix: treat rules as code — versioned, reviewed, with example-based tests for every rule (Rego has `opa test`; Drools sessions run in JUnit).
- **Business logic split between rules and code with no clear owner.** Half a decision in the rules, half in an `if` in a service, each side assuming the other checked. Fix: choose one home per decision, put all of it there, and call it through one narrow interface.

## Review questions

1. Is the problem really rule-shaped — many independent conditions, changing often, owned by people outside the team — or would a `when` / `switch` or a lookup table do?
2. Does every rule have a test with an example input and the expected decision?
3. Does any outcome depend on rule order or priority, and is that intended and tested?
4. When no rule matches, is the result the safe default (usually deny)?
5. Is the engine behind one interface that the rest of the code, and its tests, can replace?
6. Who changes the rules, how are changes reviewed, and how are they rolled back?

## Languages

| Language | Support |
|---|---|
| Kotlin | No native support: call a rules engine (Drools, in-process on the JVM), a policy language (Rego, evaluated by Open Policy Agent, usually as a separate service), a Datalog engine or a constraint solver |
| Java | No native support either; the same engines and the same choice between in-process and remote |

Whatever the engine, call it through a narrow interface your code owns — `interface EditPolicy { fun canEdit(user: UserId, doc: DocId): Boolean }` — so callers don't depend on the engine's API and tests can swap it out.

Version detection and what each language offers: [`languages/README.md`](../../languages/README.md).

## Branches

None yet.

Back to [declarative programming](README.md).
