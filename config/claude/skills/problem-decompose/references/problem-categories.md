---
title: Problem Categories
description: Taxonomy of problem types to help agents calibrate their analysis
tags: [taxonomy, categories, problem-types, calibration]
---

# Problem Categories

Use this taxonomy to classify problems during the framing step. The category influences which analysis frameworks to apply and what questions each agent should prioritize.

## Algorithmic Problems

Problems where the core challenge is choosing the right algorithm or data structure.

### Subtypes

| Subtype | Signals | Agent Focus |
|---------|---------|-------------|
| **Sorting / Ordering** | "arrange", "rank", "sort", "top-k" | Input Explorer: stability, pre-sortedness. Constraints: in-place? |
| **Searching / Lookup** | "find", "search", "contains", "exists" | Input Explorer: distribution, frequency. Constraints: precomputation ok? |
| **Graph / Tree** | "connected", "path", "cycle", "traverse" | Input Explorer: density, directedness. Constraints: memory for adjacency? |
| **Dynamic Programming** | "optimal", "minimize", "maximize", overlapping subproblems | Input Explorer: state space size. Constraints: space for memoization? |
| **String Processing** | "parse", "match", "pattern", "transform" | Input Explorer: character set, string lengths. Constraints: regex available? |
| **Numerical / Math** | "calculate", "approximate", "precision" | Input Explorer: range, precision needs. Constraints: floating point ok? |

### Key Questions for Algorithmic Problems
- What is the input size range? (determines viable complexity classes)
- Is preprocessing/precomputation allowed?
- Is an approximate answer acceptable?
- Can we trade space for time?

---

## Systems Design Problems

Problems where the core challenge is architecture, component interaction, and operational concerns.

### Subtypes

| Subtype | Signals | Agent Focus |
|---------|---------|-------------|
| **Data Pipeline** | "ingest", "transform", "ETL", "stream" | Input Explorer: throughput, schema variability. Constraints: latency budget. |
| **API Design** | "endpoint", "interface", "contract" | Goal Analyst: consumer UX. Constraints: backward compatibility. |
| **Storage / Persistence** | "store", "retrieve", "query", "index" | Input Explorer: read/write ratio, access patterns. Constraints: consistency model. |
| **Distributed Systems** | "scale", "replicate", "partition", "consensus" | Constraints Mapper: CAP trade-offs, network assumptions. |
| **Real-time / Event-driven** | "event", "webhook", "pub/sub", "notify" | Input Explorer: event volume, ordering requirements. Constraints: delivery guarantees. |
| **Auth / Security** | "authenticate", "authorize", "encrypt" | Constraints Mapper: compliance requirements. Goal Analyst: threat model. |

### Key Questions for Systems Design Problems
- What are the availability and consistency requirements?
- What is the expected load? (QPS, concurrent users, data volume)
- What existing systems must this integrate with?
- What is the operational team's capacity?

---

## Data Processing Problems

Problems centered on transforming, aggregating, or analyzing data.

### Subtypes

| Subtype | Signals | Agent Focus |
|---------|---------|-------------|
| **Batch Processing** | "bulk", "nightly", "report", "aggregate" | Input Explorer: data volume, freshness requirements. |
| **Stream Processing** | "real-time", "continuous", "window" | Input Explorer: arrival rate, ordering guarantees. Constraints: latency. |
| **Data Modeling** | "schema", "relationship", "normalize" | Goal Analyst: query patterns. Constraints: evolution/migration. |
| **Transformation** | "convert", "map", "reshape", "enrich" | Input Explorer: format variability, error rates. |

### Key Questions for Data Processing Problems
- What is the data volume and velocity?
- Is exactly-once processing required?
- What is the freshness requirement? (seconds, minutes, hours)
- How does the schema evolve over time?

---

## Concurrency Problems

Problems involving parallel execution, synchronization, or shared state.

### Subtypes

| Subtype | Signals | Agent Focus |
|---------|---------|-------------|
| **Synchronization** | "lock", "mutex", "race condition", "deadlock" | Input Explorer: contention patterns. Constraints: lock granularity. |
| **Parallelism** | "parallel", "concurrent", "thread pool" | Constraints Mapper: core count, memory per thread. |
| **Async Coordination** | "async", "await", "future", "channel" | Input Explorer: fan-out/fan-in patterns. Goal Analyst: cancellation semantics. |

### Key Questions for Concurrency Problems
- What is shared and what is isolated?
- What ordering guarantees are needed?
- What happens on failure of one concurrent unit?
- Is the bottleneck CPU, I/O, or contention?

---

## Optimization Problems

Problems where the goal is improving performance, cost, or resource usage.

### Subtypes

| Subtype | Signals | Agent Focus |
|---------|---------|-------------|
| **Latency Optimization** | "slow", "latency", "p99", "response time" | Input Explorer: hot paths, call frequency. Constraints: target latency. |
| **Throughput Optimization** | "throughput", "QPS", "batch size" | Constraints Mapper: resource ceilings. |
| **Cost Optimization** | "cost", "budget", "expensive", "reduce" | Constraints Mapper: cost drivers. Goal Analyst: acceptable trade-offs. |
| **Resource Optimization** | "memory", "CPU", "disk", "bandwidth" | Input Explorer: resource usage profiles. Constraints: hard limits. |

### Key Questions for Optimization Problems
- What is the current performance? (baseline measurement)
- What is the target? (quantified)
- Where is the bottleneck? (profiling data)
- What are we willing to sacrifice for the improvement?

---

## How Agents Use This Taxonomy

1. **During framing**: Classify the problem into 1-2 categories. Most real problems span categories.
2. **Input Explorer**: Use the "Key Questions" and "Agent Focus" columns for the relevant categories to guide investigation.
3. **Goal Analyst**: Use the category to identify which quality attributes matter most by default.
4. **Constraints Mapper**: Use the category to know which constraint dimensions to investigate thoroughly.
5. **Approach Generator**: Use the category to select appropriate algorithm families, design patterns, or architectural styles to propose.
