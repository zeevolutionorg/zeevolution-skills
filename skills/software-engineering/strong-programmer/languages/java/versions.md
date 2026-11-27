# Java features by version

Suggest only what the project's Java version supports; see [the README](README.md) for how to detect it. Moving to a newer JDK is the team's decision, never a review fix: lead with fixes that compile on the detected version, and if a newer feature would genuinely help, mention it once, after those fixes, naming the Java version it needs.

| Feature | Since | Replaces or enables | Review note |
|---|---|---|---|
| Lambdas and method references (JEP 126) | Java 8 | Anonymous inner classes that implement a one-method interface | Flag anonymous classes written for `Runnable`, `Comparator` or a listener; a method reference reads best when it names the operation |
| Standard functional interfaces in `java.util.function` (`Function`, `Supplier`, `Predicate`, `Consumer`) | Java 8 | A home-made one-method callback interface for every use | Reuse a standard interface for plumbing; a named interface is still right when the role deserves a name in the domain |
| Streams, `java.util.stream` (JEP 107) | Java 8 | Loops that filter, transform and collect by hand | Suggest a stream when the loop is a pipeline; keep the loop when the body has several side effects or throws checked exceptions |
| `Optional` | Java 8 | Returning `null` to mean "no result" | Its API note means it primarily for return types: flag `Optional` fields, parameters and collection elements, and `get()` without a check |
| Default and static methods in interfaces (JEP 126) | Java 8 | Abstract "base adapter" classes and `*Utils` classes beside an interface | Lets a published interface grow without breaking implementers; interfaces still hold no state, so stateful shared logic belongs in a class |
| Date and time API, `java.time` (JEP 150) | Java 8 | `java.util.Date`, `Calendar`, `SimpleDateFormat` | `Instant` for timestamps, `LocalDate` for calendar dates, an explicit `ZoneId` for zoned times, an injected `Clock` for tests; flag new `Date` code on every covered version |
| `CompletableFuture` | Java 8 | Blocking `Future.get()` chains and callback interfaces | The `*Async` methods without an executor run on the shared `ForkJoinPool.commonPool()`: ask for an explicit executor when the work blocks |
| `Map.getOrDefault`, `computeIfAbsent`, `merge` | Java 8 | `containsKey` / `get` / null check / `put` sequences for defaults, grouping and counting | `computeIfAbsent(key, k -> new ArrayList<>()).add(item)` to group, `merge(key, 1, Integer::sum)` to count; the mapping function must not modify the map |
| `Collection.removeIf` | Java 8 | An explicit `Iterator` loop calling `iterator.remove()` | `items.removeIf(Item::isExpired)`; flag `remove` called inside a for-each loop, which typically throws `ConcurrentModificationException` |
| Comparator factories: `Comparator.comparing`, `thenComparing`, `reversed` | Java 8 | Anonymous `Comparator` classes with a hand-written `compare` | `comparing(Invoice::dueDate).thenComparing(Invoice::number)`; flag `compare` methods that subtract `int`s, which overflow |
| `String.join` | Java 8 | `StringBuilder` loops that trim a trailing separator | `String.join(", ", names)`; inside a stream, `Collectors.joining(", ")` |
| Module system, JPMS (JEP 261) | Java 9 | The class path alone, where every public class is reachable | Optional for applications; don't ask for `module-info.java` unless the project already uses modules |
| Collection factories `List.of`, `Set.of`, `Map.of` (JEP 269) | Java 9 | `Arrays.asList`, `Collections.unmodifiableList(...)` wrappers, double-brace initialization | Unmodifiable, reject `null` elements, and `Set.of` / `Map.of` throw on duplicates; on Java 8, `Collections.unmodifiableList(Arrays.asList(...))` |
| Private methods in interfaces (JEP 213) | Java 9 | Code duplicated across default methods, or a public helper nobody should call | Share code between default methods; on Java 8, move the helper to a package-private class |
| try-with-resources on an effectively final variable (JEP 213) | Java 9 | Declaring a second variable only to put it in the `try` header | `try (connection) { ... }`; on Java 8 the resource must be declared in the header |
| Reactive-streams interfaces, `java.util.concurrent.Flow` (JEP 266) | Java 9 | `java.util.Observable`, deprecated since Java 9, and home-made publisher interfaces | For asynchronous streams with back-pressure, usually through a library that implements them; overkill for one synchronous listener |
| `Optional.ifPresentOrElse`, `or`, `stream` | Java 9 | `if (opt.isPresent()) ... else ...` blocks | On Java 8, `map(...).orElseGet(...)` when both branches produce a value; for side effects, a plain `if (opt.isPresent())` |
| `Stream.takeWhile` and `dropWhile` | Java 9 | A loop with `break` over ordered data | Only meaningful on ordered streams; on Java 8 keep the loop |
| `var` for local variables (JEP 286) | Java 10 | A long type written on both sides of `=` | Locals with an initializer and loop variables only, never fields, parameters or return types; suggest it where the right-hand side shows the type, flag it where the reader must guess |
| Unmodifiable copies `List.copyOf`, `Set.copyOf`, `Map.copyOf` | Java 10 | `Collections.unmodifiableList(new ArrayList<>(source))` for defensive copies | A real copy, not a view, and `null` elements are rejected; the Java 8–9 form above is still correct there |
| `Collectors.toUnmodifiableList`, `toUnmodifiableSet`, `toUnmodifiableMap` | Java 10 | `collectingAndThen(toList(), Collections::unmodifiableList)` | Throw on `null` elements; from Java 16, `Stream.toList()` is shorter for lists but accepts `null` elements |
| `Optional.orElseThrow()` without arguments | Java 10 | `Optional.get()` | Same behavior with an honest name, and the one `get()`'s own docs prefer; on Java 8–9, `orElseThrow(NoSuchElementException::new)` |
| `var` in lambda parameters (JEP 323) | Java 11 | Explicit parameter types written only to carry an annotation | Worth it only for annotations, as in `(@Nonnull var line) -> ...`; otherwise leave lambda parameters implicit |
| HTTP client, `java.net.http.HttpClient` (JEP 321) | Java 11 | `HttpURLConnection` | Build one client and reuse it (it is immutable); don't ask to replace the project's existing HTTP library in a review |
| `String.isBlank`, `strip`, `lines`, `repeat` | Java 11 | `trim().isEmpty()`, utility libraries for basic string work | `strip` removes Unicode white space, `trim` only characters up to U+0020 |
| `Files.readString` and `writeString` | Java 11 | `new String(Files.readAllBytes(path), UTF_8)` | Use UTF-8 unless told otherwise; on Java 8–10 keep the `readAllBytes` form with an explicit charset |
| `Predicate.not` | Java 11 | A lambda written only to negate a method reference | `filter(not(String::isBlank))` |
| `Optional.isEmpty` | Java 11 | `!opt.isPresent()` | Cosmetic: never a finding on its own |
| `Collectors.teeing` | Java 12 | Two passes over the data, or a mutable holder in a loop, to get two results | Combines two collectors in one pass, such as a count and a sum |
| `String.indent` and `transform` | Java 12 | Loops that prefix each line; nested static calls around a string | `indent` also normalizes line endings to `\n`; rarely worth a finding |
| Switch expressions and arrow labels (JEP 361) | Java 14 | `switch` statements that assign one variable in every `case`, with `break`s and fall-through bugs | Arrow labels never fall through; a `switch` expression must be exhaustive, and over an enum without `default` the compiler flags a missing constant; on Java 8–13, a `switch` statement or a map lookup |
| Helpful `NullPointerException` messages (JEP 358) | Java 14 | Splitting call chains over lines only to learn which call returned `null` | No code change; off by default in Java 14 (`-XX:+ShowCodeDetailsInExceptionMessages`), on by default from Java 15 |
| Text blocks (JEP 378) | Java 15 | String literals joined with `+` and `\n` for SQL, JSON or HTML | Incidental indentation is stripped; on Java 8–14 keep the concatenation or load a resource file |
| `String.formatted` | Java 15 | `String.format(template, args)` | Reads well right after a text block |
| Records (JEP 395) | Java 16 | Final classes with private final fields, a constructor, accessors, `equals`, `hashCode` and `toString`; Lombok `@Value` | Shallowly immutable: copy mutable components in the compact constructor (`List.copyOf`); can't extend a class; accessors are `total()`, not `getTotal()`; preview only in Java 14–15 |
| Pattern matching for `instanceof` (JEP 394) | Java 16 | `if (x instanceof Refund) { Refund r = (Refund) x; ... }` | Suggest `if (x instanceof Refund r)`; a chain of them over your own types still calls for polymorphism or a sealed type |
| `Stream.toList()` | Java 16 | `collect(Collectors.toList())` | Returns an unmodifiable list, while `Collectors.toList()` promises nothing about mutability: check that no caller adds to the result. Unlike `Collectors.toUnmodifiableList()`, it accepts `null` elements |
| Sealed classes and interfaces (JEP 409) | Java 17 | An abstract class with a package-private constructor to close a hierarchy | Each permitted subclass is `final`, `sealed` or `non-sealed`, in the same module (or package); exhaustiveness checks over them need pattern matching for `switch` (Java 21) |
| UTF-8 as the default charset (JEP 400) | Java 18 | Code that silently depended on the platform charset (`new FileReader(file)`, `getBytes()`) | Below Java 18, flag charset-less I/O and name the charset in a form that compiles on Java 8: `getBytes(StandardCharsets.UTF_8)`, `Files.newBufferedReader(path, StandardCharsets.UTF_8)`, `new InputStreamReader(in, StandardCharsets.UTF_8)`; the `FileReader` and `FileWriter` constructors that take a `Charset` need Java 11 |
| Virtual threads (JEP 444) | Java 21 | Large platform-thread pools sized for blocking I/O; reactive code adopted only to save threads | One virtual thread per task (`Executors.newVirtualThreadPerTaskExecutor()`); never pool them, and limit concurrency with a `Semaphore`; on Java 21–23, see the pinning row below |
| Pattern matching for `switch` (JEP 441) | Java 21 | `instanceof` chains; a Visitor over a hierarchy you own | Over a sealed type, leave out `default` so the compiler reports a missing case; `case null` handles `null`, otherwise the `switch` throws; preview only in Java 17–20 |
| Record patterns (JEP 440) | Java 21 | A type test followed by accessor calls | `case Approved(var authorizationCode) ->` takes the record apart; nest only as deep as stays readable |
| Sequenced collections (JEP 431) | Java 21 | `list.get(0)`, `list.get(list.size() - 1)`, iterating a `LinkedHashSet` to reach its last element | `getFirst()`, `getLast()`, and `reversed()`, which returns a view rather than a copy |
| Unnamed variables and patterns, `_` (JEP 456) | Java 22 | Names like `ignored` or `unused` in `catch` clauses, lambdas and patterns | Use `_` for a value that must be declared but is never read |
| Foreign Function and Memory API (JEP 454) | Java 22 | JNI glue code; off-heap memory through `sun.misc.Unsafe` | Rare in application code; suggest it only where JNI or `Unsafe` is already in use |
| Markdown documentation comments, `///` (JEP 467) | Java 23 | HTML-heavy Javadoc | Optional; don't convert existing Javadoc inside an unrelated change |
| Stream gatherers, `Stream.gather` (JEP 485) | Java 24 | Custom collectors or loops for windows, running totals and other stateful steps | `Gatherers.windowFixed`, `windowSliding`, `scan`, `fold`, `mapConcurrent`; plain `map` and `filter` stay as they are |
| `synchronized` no longer pins virtual threads (JEP 491) | Java 24 | Replacing `synchronized` with `ReentrantLock` only to avoid pinning | From Java 24, don't ask for that change; on Java 21–23, blocking I/O inside `synchronized` on a virtual thread holds the platform thread it runs on, so suggest a `ReentrantLock` there |
| Scoped values, `ScopedValue` (JEP 506) | Java 25 | `ThreadLocal` used to pass request context one way down a call chain | Immutable and bound for a bounded scope; keep `ThreadLocal` where code must change the value later |
| Module import declarations, `import module` (JEP 511) | Java 25 | Long lists of on-demand imports in scripts and prototypes | Fine in small programs; production code keeps explicit imports, since module imports can make simple names ambiguous |
| Compact source files and instance `main` methods (JEP 512) | Java 25 | `public static void main(String[] args)` ceremony in small tools and examples | Meant for scripts, examples and teaching; application entry points rarely need it |
| Flexible constructor bodies (JEP 513) | Java 25 | Static helper methods called inside the `super(...)` arguments only to validate them | Validate and assign fields before `super(...)` or `this(...)`, without touching `this`; below Java 25, validate in a static factory or a static helper |

## Not yet standard (up to Java 25)

Preview and incubator features need `--enable-preview` or `--add-modules` and can change between releases. Mention them only when the project already enables them, and never as a fix.

- **Structured concurrency** (`StructuredTaskScope`) — fifth preview in Java 25 (JEP 505).
- **Primitive types in patterns, `instanceof` and `switch`** — third preview in Java 25 (JEP 507).
- **Stable values** (`StableValue`) — preview in Java 25 (JEP 502); later previews renamed them lazy constants.
- **String templates** — previewed in Java 21 and 22, then withdrawn (JEP 465) and removed from JDK 23; no release has them.
- **Vector API** — incubating since Java 16; tenth incubator in Java 25 (JEP 508).

None of these became standard in JDK 26 or 27 either; check the [JDK project page](https://openjdk.org/projects/jdk/) of the exact release before treating any of them as available.
