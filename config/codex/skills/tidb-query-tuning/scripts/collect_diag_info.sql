-- collect_diag_info.sql
-- Run this script to gather baseline metadata for query tuning.

-- 1. TiDB Version & Stats Config
SELECT tidb_version();
SELECT @@tidb_analyze_column_options;

-- 2. Slow Queries in the last hour
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

-- 3. Top Load SQLs
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

-- 4. Active Connections
SELECT
    user,
    host,
    db,
    command,
    time,
    state,
    info
FROM
    information_schema.processlist
WHERE
    command != 'Sleep'
ORDER BY
    time DESC;

-- 5. Hot Regions
SELECT
    db_name,
    table_name,
    type,
    flow_bytes,
    max_hot_degree
FROM
    information_schema.tidb_hot_regions
ORDER BY
    flow_bytes DESC
LIMIT 5;

-- 6. SQL Plan Bindings
SHOW GLOBAL BINDINGS;

-- 7. Statistics Healthy for all tables
SHOW STATS_HEALTHY;
