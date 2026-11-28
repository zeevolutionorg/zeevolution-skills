---
name: strong-programmer-review-habits
tags: [smoke, software-engineering]
runs: 1
max_turns: 6
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob, Grep]
---
Please review PR #482 "Payments: new retry engine, ledger export and admin screens" — I need to approve it today.

Diff stat: 41 files changed, 1,930 insertions(+), 512 deletions(-)

One excerpt from `PaymentClient.java` (the project builds with Java 17):

```java
private static final int Attempts_Max = 5;

public Receipt charge(Order order) {
    while (true) {
        try {
            return gateway.charge(order.total());
        } catch (Exception e) {
            // try again
        }
    }
}
```
