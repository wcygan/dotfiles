# Session Variables for Query Tuning

TiDB provides session and global variables that influence optimizer behavior. These are useful for workload-wide tuning (as opposed to per-query hints).

## Syntax

```sql
-- Session scope (current connection only):
SET tidb_variable_name = value;

-- Global scope (all new connections):
SET GLOBAL tidb_variable_name = value;

-- Check current value:
SELECT @@tidb_variable_name;
```

## Key optimizer variables

### Join and execution strategy

| Variable | Default | Effect |
|----------|---------|--------|
| `tidb_opt_prefer_range_scan` | OFF | When ON, prefer range scans over full table scans even if cost estimate favors the scan. Useful when stats underestimate filter selectivity. |
| `tidb_opt_enable_hash_join` | ON | Master switch for hash join. Set OFF to disable hash joins entirely (rarely needed). |
| `tidb_index_join_batch_size` | 25000 | Batch size for index join outer side. Increasing may help throughput; decreasing reduces memory. |
| `tidb_hash_join_concurrency` | 5 | Number of concurrent hash join workers. Increase for CPU-rich environments with large hash joins. |

### Subquery and rewrite behavior

| Variable | Default | Effect |
|----------|---------|--------|
| `tidb_opt_insubq_to_join_and_agg` | ON | Controls whether IN subqueries are rewritten to joins with aggregation. Disable if the rewrite produces worse plans. |
| `tidb_opt_derive_topn` | ON | Derives TopN through outer joins and projections. Usually beneficial. |
| `tidb_opt_enable_late_materialization` | ON | Delays column reads until after filtering. Helps when many rows are filtered out early. |

### Cost model tuning

| Variable | Default | Effect |
|----------|---------|--------|
| `tidb_cost_model_version` | 2 | Cost model version. Version 2 (TiDB 6.2+) is more accurate. Use version 2 unless debugging specific regressions. |
| `tidb_opt_seek_factor` | 20 | Cost factor for random I/O seeks. Higher values make the optimizer prefer sequential scans over index lookups. |

### Statistics behavior

| Variable | Default | Effect |
|----------|---------|--------|
| `tidb_auto_analyze_ratio` | 0.5 | Threshold of modified rows before auto-ANALYZE triggers. Lower values keep stats fresher but increase analyze frequency. |
| `tidb_stats_load_sync_wait` | 100 (ms) | Wait time for synchronous stats loading during plan optimization. If stats loading is slow, increase this. |
| `tidb_enable_pseudo_for_outdated_stats` | OFF | When ON, uses pseudo statistics for tables with outdated stats. Keep OFF (default) to get warnings about stale stats instead of silently bad plans. |

### Memory and resource limits

| Variable | Default | Effect |
|----------|---------|--------|
| `tidb_mem_quota_query` | 1 GB | Memory limit per query. Queries exceeding this are cancelled or spill to disk (depending on the operator). |
| `tidb_max_chunk_size` | 1024 | Max rows per chunk during execution. Larger values improve throughput but use more memory. |
| `tidb_distsql_scan_concurrency` | 15 | Concurrency for distributed scan (TiKV coprocessor requests). Increase for scan-heavy analytical queries. |

### TiFlash and MPP

| Variable | Default | Effect |
|----------|---------|--------|
| `tidb_enforce_mpp` | OFF | When ON, forces all supported queries to use MPP execution on TiFlash. Use when you know TiFlash is the right engine. |
| `tidb_allow_mpp` | ON | Master switch for MPP. Must be ON for any TiFlash MPP execution. |
| `tidb_isolation_read_engines` | tikv,tiflash,tidb | Controls which storage engines are used. Set to `tiflash` to force TiFlash reads; `tikv` to force TiKV reads. |

## Common tuning scenarios

### Force all reads from TiFlash for an analytical session

```sql
SET tidb_isolation_read_engines = 'tiflash';
SET tidb_enforce_mpp = ON;
```

### Increase concurrency for a batch job

```sql
SET tidb_distsql_scan_concurrency = 30;
SET tidb_hash_join_concurrency = 8;
SET tidb_index_join_batch_size = 50000;
```

### Debug a plan regression after stats change

```sql
-- Check stats health first
SHOW STATS_HEALTHY WHERE Db_name = 'mydb';

-- If stats are stale, refresh
ANALYZE TABLE mydb.mytable; (or ALL COLUMNS if @@tidb_analyze_column_options != 'ALL')

-- If plan is still bad, check cost model
SELECT @@tidb_cost_model_version;
SET tidb_cost_model_version = 2;
```

## General guidance

- Prefer per-query hints over session variables when the fix is query-specific.
- Session variables affect all queries in the connection — use with care in connection-pooled environments.
- Global variable changes take effect for new connections only, not existing ones.
- Document any non-default variable settings in application configuration so they survive restarts.
