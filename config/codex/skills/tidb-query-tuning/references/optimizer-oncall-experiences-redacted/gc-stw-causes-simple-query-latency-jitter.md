# GC STW Causes Simple Query Latency Jitter

## User Symptom
- Very simple queries such as `select ... limit 1` show noticeable latency jitter.
- The slowdown does not stay in one obvious execution stage.

## Investigation Signals
- Slow samples appear across parser, planner, and executor stages instead of one operator hotspot.
- Grafana shows high `GC STW Duration`.
- The pattern is more visible on TiDB nodes with very large schema or stats memory pressure.

## Workaround
- Increase `tidb_server_memory_limit_gc_trigger`.
- Increase `tidb_gogc_tuner_threshold`.
- Give TiDB more memory if the node is structurally memory-tight.

## Fixed Version
- No universal fix was recorded in the handbook.
