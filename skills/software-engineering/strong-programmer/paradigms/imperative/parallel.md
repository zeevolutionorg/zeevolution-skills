# Parallel

Several steps run at the same time — on threads, cores or machines — and the program must stay correct in whatever order they interleave.

## Core idea

Work is split into tasks that can run at once, either to finish sooner (parallelism: one computation spread over many cores) or to keep waiting work from holding up other work (concurrency: many requests in flight). Both share the hard part: tasks that touch the same mutable state must agree on who changes it and when the change becomes visible to the others. The safest designs share nothing, or share only immutable values, and hand data between tasks through well-defined channels.

Thread safety, visibility and executors follow Goetz et al., *Java Concurrency in Practice* (2006), cited below as *JCiP*. Base definitions: [the paradigms overview](../README.md#sources).

## Primitives

| Primitive | What it gives you |
|---|---|
| Thread or task | A unit of work that runs independently; tasks go to a pool or scheduler instead of owning a thread |
| Shared memory vs message passing | Tasks either touch the same objects, which needs synchronization, or exchange messages through queues and channels, so ownership moves with the message |
| Synchronization: locks and atomics | Mutual exclusion (`synchronized`, `ReentrantLock`, Kotlin's `Mutex`) or atomic updates of a single variable or map entry (`AtomicLong`, `LongAdder`, `ConcurrentHashMap.compute`) |
| Visibility and happens-before | The memory model's rule for when one thread sees another's writes: through locks, `volatile`, thread start and join, and the hand-offs in concurrent collections (*JCiP*, ch. 3 and 16) |
| Data vs task parallelism | One large dataset split across cores (parallel streams, chunks) vs different independent jobs run side by side |
| Futures | A handle to a result that isn't ready yet: `Future`, `CompletableFuture`, Kotlin's `Deferred` |
| Structured concurrency | Child tasks live inside a scope that waits for all of them, cancels them together and passes their failure up; nothing outlives the code that started it |

## Strengths and costs

| Strengths | Costs |
|---|---|
| Uses every core; cuts wall-clock time for CPU-bound work | Bugs depend on timing: rare, hard to reproduce, invisible to most unit tests |
| Overlaps waiting on I/O, so one slow call doesn't stall the rest | Coordination overhead can make small tasks slower than a plain loop |
| Isolates slow or failing work | Cancellation, timeouts and error propagation have to be designed in, not added later |

## Signals the code is in this style

- `ExecutorService`, `CompletableFuture`, `Thread`, `parallelStream()`, `synchronized`, `volatile`.
- `suspend` functions, `launch`, `async` / `await`, `coroutineScope`, `withContext`, `Flow`, `Channel`.
- Fields holding atomics, concurrent collections, locks or a `@Volatile` flag.
- Fan-out: a loop that starts one task per item, then joins the results.

## Common failure modes

- **Race conditions.** Check-then-act or read-modify-write on shared state from several threads: `if (!cache.containsKey(k)) cache.put(k, load(k))`, `count++` on a field. Fix: confine the state to one task, make it immutable, or make the compound step atomic — `ConcurrentHashMap.computeIfAbsent`, `AtomicLong.incrementAndGet`, one lock around both steps (*JCiP*, ch. 2).
- **Deadlock.** Two tasks take the same two locks in opposite order, or a task waits on a future that needs the lock it holds. Fix: one global lock order, no calls to unknown code while holding a lock, `tryLock` with a timeout (*JCiP*, ch. 10).
- **Blocking a thread the runtime shares.** `Thread.sleep`, JDBC or a blocking HTTP client on an event loop or on `Dispatchers.Default`; `runBlocking` called from inside a coroutine; blocking work in `CompletableFuture.supplyAsync` without an executor, which runs it on the shared `ForkJoinPool.commonPool()`. Fix: move blocking calls to a pool meant for them — `withContext(Dispatchers.IO)`, an executor passed explicitly, or virtual threads on Java 21.
- **Unbounded fan-out.** `ids.map { async { client.fetch(it) } }` over 50,000 ids opens 50,000 calls at once and exhausts connections. Fix: bound the calls in flight, not just the threads — a `Semaphore` (`semaphore.withPermit { client.fetch(it) }` in coroutines, `java.util.concurrent.Semaphore` around blocking calls), chunks processed one after another, or a `Flow` with `flatMapMerge(concurrency = n)` (an experimental API). `limitedParallelism(n)` (`kotlinx.coroutines` 1.6) and fixed-size executors cap threads: that bounds a blocking client, but a suspending client still has every call open at once.
- **Lost cancellation.** `GlobalScope.launch`, a hand-made `CoroutineScope(Job())` nobody cancels, or `CompletableFuture.cancel(true)`, which doesn't interrupt the running work: tasks keep going after the caller gave up. Fix: start work in a scope tied to the caller's lifetime, and pass timeouts down. In Java, keep the `Future` from `ExecutorService.submit` — its `cancel(true)` interrupts the worker — and check `Thread.currentThread().isInterrupted()` in long loops.
- **Swallowing `InterruptedException` / `CancellationException`.** `catch (e: Exception)` or `runCatching` around a suspending call eats the coroutine's cancellation; an empty `catch (InterruptedException e)` erases the thread's interrupt. Fix: rethrow `CancellationException`; for `InterruptedException`, rethrow it or call `Thread.currentThread().interrupt()` before returning (*JCiP*, ch. 7).
- **Pool starvation.** Tasks in a bounded pool block waiting for other tasks queued behind them in the same pool, or long blocking calls occupy every thread. Fix: separate pools for dependent stages and for blocking I/O; never wait on a future from inside the pool that has to complete it (*JCiP*, ch. 8).

## Review questions

1. What state do tasks share, and what makes every access to it safe?
2. Is each compound action — check-then-act, read-modify-write — atomic?
3. Can anything here block a thread the runtime shares: an event loop, a coroutine dispatcher, the common pool?
4. How many tasks can this start at once, and what bounds that number?
5. When the caller cancels or times out, does every child task stop?
6. Are `InterruptedException` and `CancellationException` rethrown or restored, never swallowed?
7. Does a test exercise the concurrent path, not only the sequential one?

## Languages

| Language | Support |
|---|---|
| Kotlin | Coroutines (Kotlin 1.3) with `kotlinx.coroutines`: `suspend`, `launch` / `async`, structured concurrency through `coroutineScope` and `supervisorScope`, `withContext` to change dispatcher, `Channel`, and `Flow` (stable since `kotlinx.coroutines` 1.3); everything Java has is available too |
| Java | `java.util.concurrent`: executors, locks, atomics, concurrent collections; `CompletableFuture` and parallel streams (Java 8); virtual threads (Java 21 — before Java 24, blocking inside `synchronized` pins the carrier thread). Structured concurrency (`StructuredTaskScope`) is a preview API — first previewed in Java 21, reshaped in Java 25: don't suggest it unless the project already enables preview features and builds on the exact JDK the code targets |

Version detection and what each language offers: [`languages/README.md`](../../languages/README.md).

## Branches

None yet.

Back to [imperative programming](README.md).
