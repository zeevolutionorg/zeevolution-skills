# Database

Describe the data you want as a set; the database's planner decides how to find it.

## Core idea

Data lives in relations — tables of rows with typed columns — and a query states which rows and columns are wanted, how tables relate, and how to group or order the result. The query planner picks the path: which index, which join algorithm, in what order. Code in this style works on whole sets at once and lets the schema's constraints guard the data, instead of fetching rows one at a time and checking them in application loops.

In Kotlin and Java services it lives at the edge of the application, in repositories and data-access adapters: SQL, query builders and ORM mappings.

Base definitions: [the paradigms overview](../README.md#sources).

## Primitives

| Primitive | What it gives you |
|---|---|
| Relation / table | A set of rows with one shape; no order unless a query asks for one |
| Keys and constraints | Identity and rules the database enforces for every writer: primary and foreign keys, `UNIQUE`, `NOT NULL`, `CHECK` |
| Set-based operations | One statement acts on every matching row: `UPDATE ... WHERE`, `INSERT ... SELECT`, `GROUP BY` |
| Declarative queries (SQL) | You state the result you want; the engine chooses the steps |
| Joins | Rows from several tables combined on matching keys, inside the database instead of in application maps |
| Transactions (ACID) | Changes that commit or roll back together, isolated from concurrent work at the level you choose |
| Indexes and the query planner | Fast lookups on chosen columns; the planner picks indexes and join order from statistics, and `EXPLAIN` shows what it chose |
| Normalization | Each fact stored once, so an update can't leave copies that disagree; denormalize only on purpose, for measured reads |

## Strengths and costs

| Strengths | Costs |
|---|---|
| One statement replaces a loop and many round trips | Performance depends on the planner, indexes and data volume — none of it visible in the code |
| Constraints protect the data from every writer, not only this service | SQL in strings is checked only at run time, unless a type-safe builder generates it |
| Transactions make a group of changes all-or-nothing | Rows aren't objects; ORMs hide the cost of the mapping until it shows up in production |
| Mature tools to explain and tune queries | Schema changes need migrations that work on live data |

## Signals the code is in this style

- SQL in strings or text blocks, `@Query`, jOOQ or Exposed DSL chains, JPA `@Entity` classes with `@OneToMany`.
- Repository interfaces and data-access adapters.
- Migration files (Flyway, Liquibase) next to the code.
- `@Transactional` on service methods.

## Common failure modes

- **N+1 queries.** Load 100 orders, then touch `order.items` on each and 100 more queries run — usually a lazy JPA association read in a loop or by a serializer. Fix: fetch what the use case needs in one query (`JOIN FETCH`, an entity graph, an explicit join, or one `WHERE id IN (...)` batch); count statements in tests with SQL logging on.
- **Looping over rows in application code.** `findAll()` followed by `filter` and `sum` in Kotlin, or one `UPDATE` per row in a loop. Fix: push filtering, aggregation and bulk changes into the query (`WHERE`, `SUM`, `UPDATE ... WHERE`), and page through large results.
- **Missing or unused indexes.** A query filters or joins on an unindexed column and slows down as the table grows; meanwhile indexes nobody uses tax every write. Fix: read `EXPLAIN` for new queries on large tables, index for the real `WHERE` / `JOIN` / `ORDER BY`, and drop indexes the database reports as unused.
- **Transactions spanning remote calls.** `@Transactional` around an HTTP call or a message publish holds locks and a connection while waiting, and the remote effect can't be rolled back. Fix: keep transactions short and local, call out before or after, and use an outbox table when a database change and a message must agree.
- **ORM entities leaking into the domain.** JPA entities — no-arg constructors, setters, lazy proxies — serve as the domain model and get returned from controllers, so lazy loading fires in the web layer. Fix: map entities to domain types inside the repository adapter and keep persistence annotations out of the core.
- **SQL built by string concatenation.** `"... WHERE name = '" + name + "'"` invites SQL injection and defeats plan reuse. Fix: bind every value as a parameter; when a column or sort direction must vary, pick it from an allowlist.

## Review questions

1. How many queries does this use case run, and does the number grow with the data?
2. Is filtering, aggregation or bulk change done in the database, or in an application loop?
3. Do new queries have indexes that match their `WHERE`, `JOIN` and `ORDER BY`, and was `EXPLAIN` checked on realistic data?
4. Where does each transaction start and end, and does anything remote happen inside it?
5. Is every value bound as a parameter?
6. Does the schema enforce the rules — keys, `NOT NULL`, `UNIQUE` — or only the code?
7. Do persistence types stay in the adapter, out of the domain and the API?
8. Will the migration work on a live table full of data: locks, backfill, rollback?

## Languages

| Language | Support |
|---|---|
| Kotlin | Exposed, a Kotlin SQL DSL with a lightweight DAO layer; every Java library below works from Kotlin too |
| Java | JDBC with `PreparedStatement`; JPA / Hibernate; jOOQ for type-safe SQL generated from the schema; Spring Data repositories; text blocks (Java 15) for readable SQL |

Whatever the library: parameterized queries, always — never concatenate values into SQL.

Version detection and what each language offers: [`languages/README.md`](../../languages/README.md).

## Branches

None yet.

Back to [declarative programming](README.md).
