# Statistics Health and Auto Analyze

Statistics health determines whether the optimizer sees the real data distribution. When statistics go stale, TiDB can pick the wrong join order, the wrong access path, or the wrong execution engine even if the SQL itself did not change.

This guide focuses on keeping `AUTO ANALYZE` ahead of statistics decay without overloading TiDB or TiKV.

## What "healthy stats" means operationally

`AUTO ANALYZE` is healthy when it can refresh statistics at least as fast as tables become stale.

Treat the following as the primary signals:

- `Statistics -> Stats Healthy Distribution`
- `Statistics -> Auto Analyze Duration`
- `Statistics -> Auto Analyze Query Per Minute`
- TiDB CPU and memory usage
- TiKV read pressure during analyze windows

In practice:

- Most relevant tables should stay in the high-health buckets (`[80, 100]`).
- The unhealthy bucket should not show a persistent backlog.
- `AUTO ANALYZE` throughput should not spend long periods at zero when there are stale tables waiting.

## Diagnostic workflow

### 1. Check whether stats are actually decaying faster than TiDB can repair them

Start with:

```sql
SHOW STATS_HEALTHY;
SHOW ANALYZE STATUS;
```

Then compare the dashboard trends:

- If the unhealthy range keeps growing for days, `AUTO ANALYZE` is not keeping up.
- If `Auto Analyze Query Per Minute` frequently drops to zero while stale tables still exist, the trigger threshold may be too conservative.
- If `Auto Analyze Duration` P95 is high, analyze work is too slow and needs capacity or concurrency tuning.

### 2. Decide whether the bottleneck is triggering or execution

Use this split:

- **Too few analyze tasks start**: lower `tidb_auto_analyze_ratio`
- **Tasks start but finish too slowly**: tune analyze concurrency, scan concurrency, or partition/global-stats behavior
- **Tasks are slow only for partitioned tables**: inspect partition merge behavior
- **Analyze harms business traffic**: isolate the stats owner and add TiKV rate limiting before increasing concurrency

## Primary tuning levers

### `tidb_auto_analyze_ratio`

Controls when a table becomes eligible for `AUTO ANALYZE`.

- Lower value: refresh stats earlier, more frequent analyze
- Higher value: fewer analyze tasks, higher risk of stale stats

Use a lower ratio only when:

- Analyze duration is already acceptable
- TiDB and TiKV still have headroom
- The unhealthy bucket is rising because analyze is triggered too late, not because tasks are too slow

### `tidb_auto_analyze_concurrency` (v8.5+)

Controls how many analyze jobs can run at the same time.

Use it when:

- `AUTO ANALYZE` is clearly throughput-limited
- TiDB CPU is not saturated
- TiKV read pressure is controlled

Do not increase it blindly. If possible, dedicate one or more TiDB nodes to stats work first.

### `tidb_auto_build_stats_concurrency`

Controls parallel stats building. This is especially useful for partitioned tables because multiple partitions can be analyzed in parallel.

Increase it when:

- Partition tables dominate the backlog
- TiDB CPU is still underutilized

### `tidb_build_sampling_stats_concurrency`

Controls concurrent column sampling.

Increase it when:

- Wide tables are slow to analyze
- Column sampling, not partition fan-out, is the bottleneck

### Effective concurrency rule

Treat these parameters as multiplicative, not independent:

- `tidb_auto_build_stats_concurrency`
- `tidb_build_sampling_stats_concurrency`
- `tidb_auto_analyze_concurrency` (v8.5+)

Keep the effective concurrency within what the TiDB CPU can sustain. Overdriving them creates contention and can make analyze slower, not faster.

## Partitioned tables

Partitioned tables often dominate stats maintenance cost.

### `tidb_auto_analyze_partition_batch_size`

Increase it when TiDB repeatedly performs many small partition analyze batches and global stats merge becomes the long pole.

### `tidb_enable_async_merge_global_stats`

Enable this on versions that support it when global stats merge is slow or memory-heavy.

Use it when:

- `SHOW ANALYZE STATUS` shows long-running `merge global stats`
- Partitioned-table analyze causes memory spikes

### `tidb_merge_partition_stats_concurrency`

Increase it when the bottleneck is merging global partition stats rather than scanning base data.

## Scan concurrency and TiKV protection

### `tidb_analyze_distsql_scan_concurrency`

This controls the scan concurrency used by analyze.

Increase it when:

- Analyze is scan-bound
- TiKV still has spare read bandwidth

### `tidb_sysproc_scan_concurrency`

Tune this carefully in large clusters, especially after scale-out.

General rule:

- Do not set it higher than the practical TiKV fan-out your cluster can absorb
- Add TiKV background read rate limiting before raising it

### TiKV guardrail

Before increasing analyze scan concurrency, rate-limit background reads in TiKV. Otherwise analyze can steal too much read bandwidth from business traffic.

## Stats-owner isolation

### `tidb_enable_stats_owner`

Use dedicated TiDB nodes for stats ownership when available.

This is valuable when:

- Analyze work competes with latency-sensitive SQL
- You want to raise analyze concurrency safely
- You need predictable operational isolation

Do not disable stats ownership on every TiDB node. That is effectively equivalent to disabling cluster-wide auto analyze execution.

## Common failure patterns

### Backlog grows, but query-per-minute is often zero

Likely cause:

- `tidb_auto_analyze_ratio` is too high

Action:

1. Lower `tidb_auto_analyze_ratio` gradually
2. Watch the unhealthy bucket trend
3. Confirm TiDB and TiKV still have headroom

### Backlog grows and duration P95 is high

Likely cause:

- Analyze is under-provisioned or blocked on partition/global-stats work

Action:

1. Inspect `SHOW ANALYZE STATUS`
2. Tune partition/global-stats settings first for partition-heavy workloads
3. Increase analyze/build/sampling concurrency gradually
4. Verify TiKV read pressure remains acceptable

### Analyze hurts online traffic

Likely cause:

- Too much scan concurrency or too many parallel jobs without isolation

Action:

1. Add TiKV background read rate limiting
2. Move stats ownership to dedicated TiDB nodes if possible
3. Reduce analyze concurrency if TiKV or business latency regresses

## Recommended operating discipline

- Change one variable at a time.
- Use dashboard trends, not single snapshots, to judge improvement.
- For partition-heavy clusters, inspect global-stats merge explicitly.
- Prefer dedicated stats-owner TiDB nodes before aggressive concurrency increases.
- Re-check query plans after major stats tuning changes because plan choices can legitimately change.
