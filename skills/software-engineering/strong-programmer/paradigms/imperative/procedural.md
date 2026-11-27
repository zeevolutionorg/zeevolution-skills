# Procedural

Programs as procedures that call each other and work on data kept outside them.

## Core idea

Start from the whole task and break it down: the task becomes a few procedures, each of those becomes smaller ones, until every step is simple enough to write directly. Data sits in plain structures that procedures receive, read and change; behavior and data stay apart. It is the shortest path from a list of steps to working code, and it stays easy to follow while procedures are short and little state is shared.

In Kotlin and Java it shows up as top-level functions, `static` helpers, scripts and batch jobs — and inside the body of almost every method, since object-oriented code is procedural within its methods.

Base definitions: [the paradigms overview](../README.md#sources).

## Primitives

| Primitive | What it gives you |
|---|---|
| Procedure or function | A named step with one job, callable from many places |
| Parameters and return values | An explicit contract: what the step needs and what it produces |
| Local vs shared state | Locals live and die with one call and are safe; shared state (globals, `static` fields, singletons) is visible to every caller, and that is where the bugs hide |
| Records and structs | Related values grouped under one name: a Kotlin `data class`, a Java `record` (Java 16) or a class with only fields |
| Modules | A file, package or utility class that groups related procedures and hides its helpers |
| Top-down decomposition | A big task turned into a call tree you can read from the top |

## Strengths and costs

| Strengths | Costs |
|---|---|
| Reads in the order it runs | Data drifts away from the rules about it; every caller must know and repeat them |
| Little ceremony: no types to design up front | Shared mutable state couples procedures that never call each other |
| Easy to trace and debug one step at a time | Variation piles up as flags and `if`s |
| Fits scripts, batch jobs, algorithms and glue code | No natural seam to swap a behavior in tests |

## Signals the code is in this style

- Functions that take a data structure, change it and return nothing, or return the same structure.
- `*Utils` / `*Helper` classes with only `static` methods (Java), or files of top-level functions (Kotlin).
- Records or data classes without behavior, handed along a chain of functions.
- Long bodies split into numbered steps or blocks separated by comments.
- A `switch` / `when` on a type code that decides what to do.

## Common failure modes

- **Global mutable state.** A mutable `static` map, a `var` in a Kotlin `object` or companion, or a settable singleton, read and written from many functions: results depend on call order and tests leak into each other. Fix: pass the state in and return the new state, or give it one owner with a narrow interface.
- **Long functions.** One function fetches, validates, computes and saves, reusing locals across the sections. Fix: extract each section into a function whose parameters show what it needs (Fowler, *Refactoring*, 2nd ed., ch. 3, "Long Function").
- **Flag arguments.** `exportReport(report, true, false)`: booleans that pick a branch inside the callee, unreadable at the call site. Fix: split into functions with telling names (`exportSummary`, `exportDetailed`), or pass an enum when the options are many.
- **Data passed around in clumps.** The same values (`street`, `city`, `postcode`, `country`) travel together through many signatures and get reordered by mistake. Fix: introduce a record or data class and pass that.
- **Copy-paste variants.** `feeForStudents` and `feeForSeniors` share twenty lines and differ in two. Fix: extract the shared steps and pass the difference as a parameter or a function.

## Review questions

1. Can each function be described in one sentence without "and"?
2. Is each piece of shared mutable state necessary, and does exactly one place change it?
3. Do the parameters tell the whole story, or does the function also read globals, statics or the clock?
4. Are booleans or type codes selecting behavior that should be separate functions?
5. Do the same values travel together often enough to deserve a type?
6. Is there duplicated logic that differs only in a value or one step?
7. Would a test have to reset static state between cases?

## Languages

| Language | Support |
|---|---|
| Kotlin | Top-level functions and properties, no wrapper class needed (*Kotlin in Action*, §3.2.3); `private` keeps them in their file and `internal` in their module; `const val` for constants; `@file:JvmName` names the class Java callers see |
| Java | `static` methods in a `final` utility class with a `private` constructor; `static` imports; records (Java 16) for plain data |

Version detection and what each language offers: [`languages/README.md`](../../languages/README.md).

## Branches

None yet.

Back to [imperative programming](README.md).
