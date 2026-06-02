# Reading EXPLAIN ANALYZE Output

`EXPLAIN ANALYZE` is the primary tool for understanding how TiDB actually executes a query. It runs the query and reports actual row counts, execution time, and memory usage for each operator.

## Syntax

```sql
-- Basic (text format):
EXPLAIN ANALYZE SELECT ...;

-- Structured JSON format (better for programmatic analysis):
EXPLAIN FORMAT = "tidb_json" SELECT ...;

-- Estimate only (does NOT execute the query):
EXPLAIN SELECT ...;
```

**Use `EXPLAIN ANALYZE` for tuning.** Plain `EXPLAIN` shows estimates only, which may be wrong.

## Key columns in EXPLAIN ANALYZE output

| Column | Meaning |
|--------|---------|
| `id` | Operator name and position in the tree |
| `estRows` | Estimated row count from optimizer statistics |
| `actRows` | Actual row count observed during execution |
| `task` | Where the operator runs: `root` (TiDB), `cop[tikv]` (TiKV coprocessor), `cop[tiflash]` (TiFlash) |
| `access object` | Table, index, or partition being accessed |
| `execution info` | Wall time, loops, memory, disk usage, concurrency |
| `operator info` | Filter conditions, join keys, sort keys |

## What to look for

### 1. estRows vs actRows divergence

Large differences indicate stale or inaccurate statistics.

```
estRows: 100    actRows: 500000   ← Stats are wrong!
```

**Action:** Run `ANALYZE TABLE <table>;` (or with `ALL COLUMNS` if `@@tidb_analyze_column_options` is not `ALL`) and re-check.

### 2. Expensive operators (by wall time)

Look at `execution info` for `time:` values. The operator with the longest time is the bottleneck.

```
execution info: time:2.5s, loops:1, ...   ← This is the bottleneck
```

### 3. Full table scans on large tables

```
TableFullScan   table:orders   actRows:10000000
```

**Action:** Add an index or use a hint to force an index scan.

### 4. Hash join with large build side

```
HashJoin         actRows:50000
├── Build        actRows:5000000   ← Build side is huge
└── Probe        actRows:50000
```

**Action:** Consider `INL_JOIN` if the build side has an index, or `LEADING` to swap build/probe sides.

### 5. `IndexJoin` or `IndexHashJoin` using the wrong probe index

```
IndexJoin / IndexHashJoin
└── Probe child uses index:idx_filter_only
```

The join algorithm may be reasonable, but the probe-side `access object` can still be wrong.

**Action:** Compare candidate probe indexes with `USE_INDEX` / `IGNORE_INDEX`, then stabilize the better path with a SQL binding or hint.

### 6. Unnecessary Sort operators

```
Sort             actRows:1000000
└── TableFullScan
```

If there's an index that provides the sort order, use `ORDER_INDEX` to eliminate the Sort.

### 7. Apply operator (correlated subquery)

```
Apply            actRows:1000
├── Outer        actRows:1000
└── Inner        actRows:1000   (executed 1000 times)
```

This means correlated execution. If `actRows` on the outer side is small, this is fine. If large, consider letting TiDB decorrelate (remove `NO_DECORRELATE`) or adding an index on the inner side.

## Operator reference

### Scan operators

| Operator | Meaning |
|----------|---------|
| `TableFullScan` | Full table scan — reads every row |
| `TableRangeScan` | Scans a range of the primary key |
| `IndexRangeScan` | Scans a range of an index |
| `IndexFullScan` | Scans the entire index |
| `IndexLookUp` | Two-phase: index scan → table lookup for remaining columns |

### Join operators

| Operator | Meaning |
|----------|---------|
| `HashJoin` | Hash join (look for Build and Probe children) |
| `IndexJoin` | Index nested loop join |
| `IndexHashJoin` | Index hash join with indexed probe side |
| `MergeJoin` | Sort-merge join |
| `Apply` | Correlated subquery execution (per-row) |

### Aggregation operators

| Operator | Meaning |
|----------|---------|
| `HashAgg` | Hash-based aggregation |
| `StreamAgg` | Stream aggregation (requires sorted input) |

### Other operators

| Operator | Meaning |
|----------|---------|
| `Sort` | Sorts rows (expensive for large datasets) |
| `TopN` | Sort + limit combined (more efficient than separate Sort + Limit) |
| `Selection` | Filters rows (WHERE conditions not pushed to scan) |
| `Projection` | Computes output columns |
| `Limit` | Returns only N rows |

## Diagnostic workflow

```
1. Run EXPLAIN ANALYZE
2. Find the operator with the highest wall time
3. Check estRows vs actRows for that operator and its children
   ├── Big divergence → ANALYZE TABLE <table>; (or with ALL COLUMNS), then re-run
   └── Stats are fine → Operator choice is the problem
4. Identify the pattern:
   ├── Full scan → Add index or USE_INDEX hint
   ├── Wrong join strategy → HASH_JOIN / INL_JOIN hint
   ├── Right join strategy but wrong probe index → Compare USE_INDEX candidates and bind the winner
   ├── Wrong join order → LEADING hint
   ├── Expensive correlated subquery → Check NO_DECORRELATE guidance
   └── Unnecessary Sort → ORDER_INDEX hint or add sorted index
5. Apply fix and re-run EXPLAIN ANALYZE to verify
```
