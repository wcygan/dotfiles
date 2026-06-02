# Stale Stats After Bulk Data Change

## User Symptom
- A query suddenly switches to a bad index or a much heavier plan.
- TiKV CPU rises after rapid inserts, deletes, or major data distribution changes.

## Investigation Signals
- `EXPLAIN ANALYZE` shows `estRows` far away from `actRows`.
- `show stats_meta` shows stale `update_time`, large `modify_count`, or a delayed analyze cycle.
- The plan becomes normal again right after manual analyze or after scheduled analyze finally runs.

## Workaround
- Run manual `ANALYZE` on the affected table or partition.
- Check whether auto analyze thresholds or modification ratios delayed refresh too long.
- If the workload changed together with schema or index design, verify the new predicates still match the intended index.

## Fixed Version
- No single fix version. This is a recurring operational pattern around stale or delayed statistics.
