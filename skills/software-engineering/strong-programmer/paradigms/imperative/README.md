# Imperative programming

Tell the machine *how*: a sequence of statements that change the program's state, one step at a time.

## Core idea

The program is a list of commands. Variables hold state; each statement reads or changes it; control flow — sequence, selection, iteration — decides what runs next. It is close to how the hardware works, which makes it predictable to trace and easy to make fast, and also easy to tangle as state spreads.

## Primitives

| Primitive | What it is |
|---|---|
| Variable and assignment | Named, mutable state |
| Sequence | Statements run in order |
| Selection | `if` / `switch` / `when` |
| Iteration | `for` / `while` loops |
| Procedure call | Named, reusable steps with parameters and a return value |

## Approaches

| Approach | What it adds | Status |
|---|---|---|
| Procedural | Programs as procedures over shared data; top-down decomposition | 🔜 |
| Object-oriented | Objects bundle state with behavior; encapsulation, polymorphism, composition | 🔜 |
| Parallel | Several steps run at the same time, split across threads, cores or machines | 🔜 |

Back to [the paradigms](../README.md).
