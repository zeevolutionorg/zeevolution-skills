---
type: llm
---
The review names, with their usual fixes and the principle behind each: Repeated Switches on the order type (move the variation into the type: an enum or sealed hierarchy with behavior; open/closed), a Large Class doing pricing, persistence, mail, PDF and import (single responsibility: split by reason to change), a Data Class / anemic model with public mutable properties (move behavior next to the data; Mutable Data), Primitive Obsession for type and status (enum or sealed types) and `Double` for money. It flags the SQL built by string interpolation as a blocking injection risk. It does not propose speculative patterns (no Abstract Factory, Visitor or a strategy hierarchy beyond what the three order types need), and its fixes compile on Kotlin 1.9.
