---
name: strong-programmer-oo-smells
tags: [software-engineering]
runs: 1
max_turns: 6
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob, Grep]
---
Review this class. We're on Kotlin 1.9.

```kotlin
data class Order(var id: String, var type: String, var items: MutableList<Item>, var status: String)
data class Item(var sku: String, var price: Double, var qty: Int)

class OrderManager(private val db: Database, private val mailer: Mailer, private val pdf: PdfRenderer) {
    fun total(order: Order): Double {
        val base = order.items.sumOf { it.price * it.qty }
        return when (order.type) {
            "RETAIL" -> base
            "WHOLESALE" -> base * 0.9
            "STAFF" -> base * 0.7
            else -> base
        }
    }

    fun shippingCost(order: Order): Double = when (order.type) {
        "RETAIL" -> 9.9
        "WHOLESALE", "STAFF" -> 0.0
        else -> 9.9
    }

    fun canCancel(order: Order): Boolean = when (order.type) {
        "WHOLESALE" -> order.status == "NEW"
        else -> order.status == "NEW" || order.status == "PAID"
    }

    fun save(order: Order) = db.execute("insert into orders values ('${order.id}', '${order.type}', '${order.status}')")
    fun sendConfirmation(order: Order) = mailer.send(to = "orders@example.com", body = "Order ${order.id}: ${total(order)}")
    fun invoicePdf(order: Order): ByteArray = pdf.render(order.items.joinToString("\n") { "${it.sku} x${it.qty}" })
    fun importCsv(path: String): List<Order> = java.io.File(path).readLines().map { line ->
        val f = line.split(",")
        Order(f[0], f[1], mutableListOf(), "NEW")
    }
}
```
