# Stats Version and Analyze Configuration

Statistics collection quality is not only about whether `ANALYZE` runs. The stats version, column coverage, partition behavior, and column-type exclusions all shape plan quality and resource usage.

## Prefer stats version 2

TiDB historically had two stats systems:

- stats v1
- stats v2

Stats v1 is no longer maintained. Since v6.5, the default has moved to stats v2 and new deployments should stay there unless debugging a specific regression.

### Why stats v2 is preferred

- Better estimation on large tables and skewed data
- Better handling of out-of-range predicates
- Faster analyze because table and index sampling is more efficient
- Lower collection overhead because not every older stats structure is required

## `tidb_analyze_version`

Use:

```sql
SELECT @@tidb_analyze_version;
SET GLOBAL tidb_analyze_version = 2;
```

Operational rule:

- Keep the cluster on a consistent stats version as much as possible
- Mixed-version stats across tables and indexes make diagnosis harder and can create temporary plan instability during migrations

## When migrating old stats to v2

The safest pattern is:

1. Switch the analyze version
2. Re-analyze the tables that matter
3. Validate plan quality on critical SQL

Avoid partial migrations of only a few hot tables unless you have a clear reason to do so.

## Column coverage policy

### `tidb_analyze_column_options`

This variable controls how much column-level stats `ANALYZE` collects.

Main choices:

- `PREDICATE`: collect only predicate columns
- `ALL`: collect all columns

Use `ALL` when:

- The workload is analytical
- Query shapes vary a lot
- Non-predicate columns still influence plan quality or resource usage indirectly

Use `PREDICATE` when:

- The workload is strongly OLTP-oriented
- You need to cut analyze overhead
- Plan regressions are not caused by missing column coverage

For OLAP-heavy workloads, `PREDICATE` can reduce stats completeness enough to hurt plan quality.

## OOM-oriented configuration

### Partitioned-table global stats

Partitioned-table analyze can cause large memory spikes when global stats merge is expensive.

Preferred mitigation:

- Enable `tidb_enable_async_merge_global_stats` on supporting versions

### `tidb_enable_historical_stats`

Disable it unless you specifically need historical stats snapshots and have validated the memory cost.

Why:

- Historical stats can add meaningful TiDB memory pressure
- Older implementations were especially risky on tables with many stats objects or partitions

### `tidb_analyze_skip_column_types`

Use this to skip stats collection for low-value, memory-heavy column types such as:

- `json`
- `blob`
- `mediumblob`
- `longblob`
- `text`
- `mediumtext`
- `longtext`

This is appropriate when:

- These columns are large
- They are not useful for predicate estimation
- Analyze or memory usage is unstable because of them

## Sampling and build concurrency

### `tidb_build_sampling_stats_concurrency`

Use it to accelerate column sampling for wide tables.

### `tidb_auto_build_stats_concurrency`

Use it to accelerate stats building, especially on partition-heavy workloads.

Do not tune them in isolation. Their combined effect can exceed what the host CPU can handle.

## Version-sensitive guidance

- v6.5+: stats v2 should be the default path
- v7.5+: async global-stats merge is a key tool for partitioned-table analyze
- v8.5+: concurrent auto analyze makes throughput tuning more practical, but only if TiDB and TiKV still have capacity

## Practical checklist

Use this order:

1. Confirm the cluster is on stats v2
2. Decide whether `ALL` or `PREDICATE` fits the workload
3. Disable or limit memory-heavy stats features unless they are truly needed
4. Exclude large low-value column types from analyze
5. Tune sampling/build concurrency only after the policy choices above are correct

## Common anti-patterns

- Leaving the cluster on old stats behavior after upgrade because "nothing broke yet"
- Using `PREDICATE` for OLAP workloads and then debugging bad plans as if they were optimizer bugs
- Increasing analyze concurrency before excluding memory-heavy column types
- Turning on historical stats without a concrete operational need
