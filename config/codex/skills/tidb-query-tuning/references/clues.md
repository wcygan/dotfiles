# TiDB Query Tuning: Clue Collection

To effectively diagnose a performance issue, collect these clues from the system tables.

## 1. Top Slow Queries
Search the `SLOW_QUERY` table to find queries that exceeded the `slow-threshold`.

```sql
SELECT
    query,
    query_time,
    process_time,
    wait_time,
    mem_max,
    plan_digest,
    is_internal
FROM
    information_schema.slow_query
WHERE
    time > now() - INTERVAL 1 HOUR
ORDER BY
    query_time DESC
LIMIT 10;
```

## 2. Statements Summary
For historical aggregated statistics, use `STATEMENTS_SUMMARY`.

```sql
SELECT
    digest_text,
    sum_latency,
    avg_latency,
    exec_count,
    avg_mem,
    avg_processed_keys,
    avg_total_keys
FROM
    information_schema.statements_summary
WHERE
    digest_text IS NOT NULL
ORDER BY
    sum_latency DESC
LIMIT 10;
```

## 3. Statistics Health
Stale statistics are a primary cause of bad execution plans.

```sql
SHOW STATS_HEALTHY WHERE Table_name = 'your_table';
```
If `Healthy` < 60, run `ANALYZE TABLE <table_name>;`. (Note: use `ALL COLUMNS` if `@@tidb_analyze_column_options` is not `ALL`).

## 4. PLAN REPLAYER (On-site Info Export)
`PLAN REPLAYER` exports version, config, vars, schema, stats, and the execution plan into a ZIP file.

- **Export single SQL**:
  ```sql
  PLAN REPLAYER DUMP EXPLAIN ANALYZE SELECT * FROM your_table WHERE ...;
  ```
- **Download the ZIP**:
  Use the returned token and the TiDB status port:
  `curl http://{tidb-server-ip}:{status-port}/plan_replayer/dump/{token} > plan.zip`

## 5. TiDB HTTP API (Debug API)
TiDB servers expose an HTTP API (default port `10080`) for deeper diagnostics.

- **Dump Statistics**:
  `curl http://{tidb-server-ip}:10080/stats/dump/{db}/{table} > stats.json`
- **View Schema**:
  `curl http://{tidb-server-ip}:10080/schema/{db}/{table}`
- **Hot Regions**:
  `curl http://{tidb-server-ip}:10080/regions/hot`
- **Pprof (Profiling)**:
  `curl http://{tidb-server-ip}:10080/debug/pprof/profile?seconds=30 > cpu.pprof`
- **All Endpoints**:
  Check `curl http://{tidb-server-ip}:10080/debug/pprof/` for available profile types (heap, mutex, goroutine).

## 6. SQL Plan Bindings
Check if there are already bindings affecting the plan.

- **Show all bindings**:
  ```sql
  SHOW GLOBAL BINDINGS;
  ```
- **Check if last query used a binding**:
  ```sql
  SELECT @@last_plan_from_binding;
  ```
- **Verbose explain** (shows if a binding was used in warnings):
  ```sql
  EXPLAIN FORMAT = 'verbose' <sql_statement>;
  SHOW WARNINGS;
  ```

## 7. Resource Usage
Check for heavy scans or high backoff counts.

```sql
SELECT
    query,
    scan_objects,
    backoff_types,
    request_count
FROM
    information_schema.slow_query
WHERE
    query_time > 1
ORDER BY
    scan_objects DESC
LIMIT 5;
```

## 5. Metadata Collection
Always get these before proposing a fix:
- `SHOW CREATE TABLE <table_name>;`
- `SELECT tidb_version();`
- `SHOW SESSION VARIABLES LIKE '%concurrency%';`
