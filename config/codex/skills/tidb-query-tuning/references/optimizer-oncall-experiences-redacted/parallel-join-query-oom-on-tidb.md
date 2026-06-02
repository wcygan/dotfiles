# Parallel Join Query OOM on TiDB

## User Symptom
- Running one complex query at moderate or high concurrency causes TiDB OOM or very high heap usage.
- Single-query latency may still look acceptable, but concurrency collapses the node.

## Investigation Signals
- The plan crosses TiFlash and TiKV and builds a large hash join on TiDB.
- `EXPLAIN ANALYZE` memory numbers are not reliable for this pattern.
- Grafana TiDB heap memory and TiFlash logs are more trustworthy than the plan output.

## Workaround
- Reduce rows as early as possible in the query shape.
- Move selective inner joins earlier.
- Rewrite the query so `TopN` can push down before the long chain of outer joins.
- If high concurrency is required, scale out TiDB or increase memory.

## Fixed Version
- No general product fix. This is mostly a query-shape and resource-sizing problem.
