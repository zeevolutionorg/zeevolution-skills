---
name: strong-programmer-java-version-gate
tags: [software-engineering]
runs: 1
max_turns: 6
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob, Grep]
---
Can you review this and suggest how to modernize it?

`pom.xml` (excerpt):

```xml
<properties>
  <maven.compiler.source>1.8</maven.compiler.source>
  <maven.compiler.target>1.8</maven.compiler.target>
</properties>
```

`ShipmentReport.java`:

```java
public class ShipmentReport {
    public String id;
    public String carrier;
    public java.util.Date shippedAt;

    public static String describe(Object event) {
        if (event instanceof Delivered) {
            Delivered d = (Delivered) event;
            return "Delivered to " + d.getRecipient();
        } else if (event instanceof Lost) {
            Lost l = (Lost) event;
            return "Lost: " + l.getReason();
        } else {
            return "Unknown";
        }
    }

    public static java.util.List<String> carriers(java.util.List<ShipmentReport> reports) {
        java.util.List<String> result = new java.util.ArrayList<String>();
        for (ShipmentReport r : reports) {
            if (r.carrier != null && !result.contains(r.carrier)) {
                result.add(r.carrier);
            }
        }
        return result;
    }

    public static final String QUERY =
        "SELECT id, carrier, shipped_at\n" +
        "FROM shipments\n" +
        "WHERE shipped_at > ?";
}
```
