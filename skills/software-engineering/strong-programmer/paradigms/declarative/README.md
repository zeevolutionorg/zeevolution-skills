# Declarative programming

Tell the machine *what* you want; the language, engine or planner decides how to get it.

## Core idea

The program describes the result — an expression, a relation, a query, a set of rules — and leaves control flow to the runtime. There is less state to track and fewer orderings to get wrong, at the cost of trusting (and learning) what the runtime does underneath.

## Primitives

| Primitive | What it is |
|---|---|
| Expression | A value computed from other values, with no hidden effects |
| Binding | A name for a value that does not change |
| Relation or rule | A fact about the problem that the engine can use |
| Query | A description of the data wanted, not the steps to fetch it |
| Composition | Bigger descriptions built from smaller ones |

## Approaches

| Approach | What it adds | Status |
|---|---|---|
| Logic | Facts and rules; the engine searches for answers | 🔜 |
| Functional | Pure functions and immutable values; functions as values | 🔜 |
| Database | Set-based queries over data; the planner chooses how to run them | 🔜 |

Back to [the paradigms](../README.md).
