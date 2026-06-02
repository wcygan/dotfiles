# Index Selection

Good index design is the single highest-impact tuning lever. TiDB's optimizer uses cost-based index selection, but it can choose poorly when stats are stale or cardinality is misestimated.

## Index hints

### USE_INDEX

Force the optimizer to use a specific index:

```sql
SELECT /*+ USE_INDEX(t, idx_status_created) */ *
FROM orders t
WHERE t.status = 'pending' AND t.created_at > '2024-01-01';
```

### IGNORE_INDEX

Prevent use of a specific index (useful for testing whether a different index or table scan is faster):

```sql
SELECT /*+ IGNORE_INDEX(t, idx_old) */ *
FROM orders t
WHERE t.status = 'pending';
```

### USE_INDEX_MERGE

Combine multiple indexes when a query filters on columns covered by different indexes:

```sql
-- Uses both idx_status and idx_region, merges results
SELECT /*+ USE_INDEX_MERGE(t, idx_status, idx_region) */ *
FROM orders t
WHERE t.status = 'pending' OR t.region = 'us-east';
```

Index merge is particularly useful for OR conditions that span different indexes.

### ORDER_INDEX / NO_ORDER_INDEX

Control whether the optimizer uses an index to provide sort order:

```sql
-- Force ordered scan: avoid a Sort operator by reading from index in order
SELECT /*+ ORDER_INDEX(t, idx_created) */ *
FROM orders t
ORDER BY t.created_at DESC
LIMIT 20;

-- Prevent ordered scan: if the optimizer incorrectly chooses a slow ordered scan
SELECT /*+ NO_ORDER_INDEX(t, idx_created) */ *
FROM orders t
WHERE t.status = 'pending'
ORDER BY t.created_at DESC
LIMIT 20;
```

## Composite index design

### Leftmost prefix rule

TiDB (like MySQL) can only use a composite index from the leftmost column onward. An index on `(a, b, c)` supports:
- Queries filtering on `a`
- Queries filtering on `a, b`
- Queries filtering on `a, b, c`
- But NOT queries filtering only on `b` or `c`

### Column ordering guidelines

1. **Equality columns first:** Columns in `=` conditions go leftmost.
2. **Range column last:** The column used in `>`, `<`, `BETWEEN`, or `LIKE 'prefix%'` goes after equality columns.
3. **High-selectivity columns first** (among equality columns): Reduces rows scanned early.

```sql
-- Query: WHERE status = 'active' AND region = 'us' AND created_at > '2024-01-01'
-- Best index: (status, region, created_at)
-- status and region are equality; created_at is range
```

### Covering indexes

If a query only needs columns in the index (plus the primary key), TiDB can serve it from the index alone without a table lookup:

```sql
-- If index is (status, created_at) and PK is id:
-- This query is "covered" — no table lookup needed
SELECT id, status, created_at FROM orders WHERE status = 'pending';
```

## Invisible indexes

Test the impact of dropping an index without actually dropping it:

```sql
-- Make index invisible (optimizer won't use it, but it's still maintained)
ALTER TABLE orders ALTER INDEX idx_old INVISIBLE;

-- Test queries... if performance is fine, drop it
DROP INDEX idx_old ON orders;

-- If queries regressed, make it visible again
ALTER TABLE orders ALTER INDEX idx_old VISIBLE;
```

## Diagnosing index selection issues

### Step 1: Check which index is used

```sql
EXPLAIN SELECT * FROM orders WHERE status = 'pending' AND region = 'us';
```

Look for `IndexRangeScan`, `IndexFullScan`, or `TableFullScan` in the plan.

### Step 2: Check index statistics

```sql
SHOW STATS_HEALTHY WHERE Table_name = 'orders';
SHOW INDEX FROM orders;
```

### Step 3: Compare index choices

```sql
-- Force each candidate index and compare EXPLAIN ANALYZE results
EXPLAIN ANALYZE SELECT /*+ USE_INDEX(orders, idx_status) */ * FROM orders WHERE ...;
EXPLAIN ANALYZE SELECT /*+ USE_INDEX(orders, idx_region) */ * FROM orders WHERE ...;
EXPLAIN ANALYZE SELECT /*+ USE_INDEX(orders, idx_status_region) */ * FROM orders WHERE ...;
```

## `IndexJoin` and `IndexHashJoin` probe-side index selection

For `IndexJoin` and `IndexHashJoin`, treat the inner/probe access path as an index-selection problem, not only a join-strategy problem.

- Match the join equality columns on the probe-side table first.
- Then prefer indexes that also absorb pushed `=` or `IN` filters.
- Prefer a more covering probe path when it can avoid `IndexLookUp` and extra `TableRowIDScan`.
- Compare existing candidates with `EXPLAIN ANALYZE` using `USE_INDEX` or `IGNORE_INDEX`.
- If an existing index is clearly better for this query shape, prefer a SQL binding or query hint before adding a new index.

Two common patterns:

- Query shape `t1.a = t2.a AND t2.b = 1 AND t2.d = 1`: if both `(a, b)` and `(a, b, c, d)` exist, the longer index can be the better probe path even though the join only uses `a`.
- Query shape `ab.col1 = mp.col2 AND ab.col2 = mp.col6`: an index starting with `(col2, col6)` can be a better probe path than an index that starts with local filter columns but does not match the full join-key prefix.

## Common pitfalls

- **Too many indexes:** Each index adds write overhead and storage. Only create indexes that serve real query patterns.
- **Redundant indexes:** Index `(a, b)` makes a standalone index on `(a)` redundant. Audit with `SHOW INDEX`.
- **Low-selectivity leading column:** An index on `(gender, user_id)` is almost useless if the first column has only 2-3 distinct values and queries don't always filter on it.
- **Stale stats on new indexes:** After creating an index, run `ANALYZE TABLE <table_name>;` (or with `ALL COLUMNS` if `@@tidb_analyze_column_options` is not `ALL`) to collect stats for it. Otherwise the optimizer may not pick it.
