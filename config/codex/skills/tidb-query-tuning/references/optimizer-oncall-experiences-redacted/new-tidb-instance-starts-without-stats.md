# New TiDB Instance Starts Without Stats

## User Symptom
- A newly scaled-out TiDB instance is healthy enough to serve traffic, but it has no usable stats and may choose bad plans.

## Investigation Signals
- `stats_meta` or related `stats_xxx` data is missing on the new node.
- TiDB logs show `Out of Memory Quota`, `SortAndSpillDiskAction`, or `Incorrect time value` during stats initialization.
- The issue often appears during `initStatsBuckets`.

## Workaround
- Temporarily increase `tidb_mem_quota_query` during instance startup so stats initialization can finish.
- If invalid historical time values block stats loading, use a compatible SQL mode such as `ALLOW_INVALID_DATES` long enough to load the old stats.
- After the instance is warm, restore the normal operational settings.

## Fixed Version
- Invalid time-value loading was fixed in `v6.5.11`.

## Public References
- https://github.com/pingcap/tidb/issues/56480
