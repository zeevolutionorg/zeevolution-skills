# Programming paradigms

A paradigm is a way of structuring computation. Two families cover the code you will meet:

| | Imperative | Declarative |
|---|---|---|
| You write | *How* — the steps, in order | *What* — the result you want |
| State | Changed in place, step by step | Avoided, or hidden behind the runtime |
| Control flow | Explicit: sequence, branches, loops | Implicit: the engine, evaluator or planner decides |
| Approaches | [Procedural, object-oriented, parallel](imperative/README.md) | [Logic, functional, database](declarative/README.md) |

## Which approach is this code in?

Name the approach before judging the code: a loop is fine in procedural code and a smell in a stream pipeline; a mutable field is normal in an object and a bug in a pure function.

| If you see | It's mostly |
|---|---|
| Top-level functions over shared data structures, step-by-step mutation, `static` utility classes | [Procedural](imperative/procedural.md) |
| Classes that bundle data with behavior, interfaces, polymorphic calls, injected collaborators | [Object-oriented](imperative/object-oriented/README.md) |
| Threads, executors, coroutines, `async`/`await`, locks, atomics, parallel streams, channels | [Parallel](imperative/parallel.md) |
| Facts and rules, unification, a rules engine or policy language (Prolog, Datalog, Drools, Rego) | [Logic](declarative/logic.md) |
| Pure functions, immutable values, `map`/`filter`/`fold`, functions passed as values, sealed results instead of exceptions | [Functional](declarative/functional.md) |
| SQL, query builders, ORM criteria, set operations instead of loops over rows | [Database](declarative/database.md) |

Real code mixes approaches — a Kotlin service can be object-oriented at the top, functional in its pipelines and database-driven in its repositories. Name the dominant approach per area, and judge each area by its own standards.

## Sources

- [Introduction of Programming Paradigms — GeeksforGeeks](https://www.geeksforgeeks.org/system-design/introduction-of-programming-paradigms/)
