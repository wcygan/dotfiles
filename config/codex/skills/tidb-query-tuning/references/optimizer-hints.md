# Optimizer Hints

TiDB supports query-level optimizer hints using the `/*+ HINT() */` syntax placed immediately after `SELECT`, `UPDATE`, or `DELETE`.

## Syntax

```sql
SELECT /*+ HINT_NAME(arguments) */ ...
```

Multiple hints can be combined:

```sql
SELECT /*+ HASH_JOIN(t1, t2) NO_DECORRELATE() */ ...
```

## Hint Catalog

### Join strategy hints

| Hint | Effect | When to use |
|------|--------|-------------|
| `HASH_JOIN(t1, t2)` | Force hash join between named tables | Large table joins without useful indexes; both sides are large |
| `INL_JOIN(t)` | Force index nested loop join, `t` is the inner (probed) side | Inner table has a good index on the join key and is large; outer side is small |
| `INL_HASH_JOIN(t)` | Index join with hash join on the inner side | Similar to INL_JOIN but inner side needs hash matching |
| `MERGE_JOIN(t1, t2)` | Force sort-merge join | Both sides are already sorted on join key or can be cheaply sorted |
| `SHUFFLE_JOIN(t1, t2)` | Force shuffle hash join (MPP) | TiFlash queries where data needs redistributing across nodes |
| `BROADCAST_JOIN(t1, t2)` | Force broadcast join (MPP) | TiFlash queries where one side is small enough to broadcast |

### Join order hints

| Hint | Effect | When to use |
|------|--------|-------------|
| `LEADING(t1, t2, t3)` | Force join order; tables joined left to right | Optimizer picks a bad join order due to cardinality misestimation |
| `STRAIGHT_JOIN()` | Join tables in the order written in FROM clause | Quick override when you know the right order |

### Subquery hints

| Hint | Effect | When to use |
|------|--------|-------------|
| `NO_DECORRELATE()` | Keep correlated subquery as-is; do not flatten into a join | Subquery is well-indexed, outer query is selective. See `subquery-optimization.md` |
| `SEMI_JOIN_REWRITE()` | Rewrite semi-join to inner join with deduplication | When semi-join execution is slow and inner side has few duplicates |

### Index hints

| Hint | Effect | When to use |
|------|--------|-------------|
| `USE_INDEX(t, idx)` | Force use of a specific index | Optimizer picks wrong index or full table scan |
| `IGNORE_INDEX(t, idx)` | Prevent use of a specific index | A specific index produces a bad plan |
| `USE_INDEX_MERGE(t, idx1, idx2)` | Force index merge (combine multiple indexes) | Query filters on columns from different indexes |
| `ORDER_INDEX(t, idx)` | Force ordered scan on index | Need sorted results and the index provides the order |
| `NO_ORDER_INDEX(t, idx)` | Prevent ordered scan on index | Optimizer incorrectly prefers an ordered scan |

### Read strategy hints

| Hint | Effect | When to use |
|------|--------|-------------|
| `READ_FROM_STORAGE(TIKV[t])` | Force reading from TiKV (row store) | OLTP point lookups; avoid accidental TiFlash reads |
| `READ_FROM_STORAGE(TIFLASH[t])` | Force reading from TiFlash (columnar) | Analytical scans on large tables with TiFlash replicas |
| `USE_TOJA(TRUE)` | Enable outer join to anti/semi-join transformation | Specific outer join patterns that can be simplified |
| `USE_TOJA(FALSE)` | Disable the transformation | Transformation produces a worse plan |

### Aggregation hints

| Hint | Effect | When to use |
|------|--------|-------------|
| `HASH_AGG()` | Force hash aggregation | Large GROUP BY with many distinct values |
| `STREAM_AGG()` | Force stream aggregation | Data is already sorted on GROUP BY columns |
| `MPP_1PHASE_AGG()` | Force single-phase MPP aggregation | TiFlash; low cardinality GROUP BY |
| `MPP_2PHASE_AGG()` | Force two-phase MPP aggregation | TiFlash; high cardinality GROUP BY |

### Other hints

| Hint | Effect | When to use |
|------|--------|-------------|
| `MEMORY_QUOTA(N)` | Set per-query memory limit (e.g., `MEMORY_QUOTA(1 GB)`) | Prevent a single query from using too much memory |
| `MAX_EXECUTION_TIME(N)` | Set per-query timeout in milliseconds | Safety net for queries that might run too long |
| `RESOURCE_GROUP(name)` | Assign query to a resource group | Workload isolation |

## General guidance

- **Start without hints.** Fix stats and indexes first. Only add hints when the optimizer consistently picks a wrong plan.
- **Be specific.** Specify table names in hints to avoid ambiguity, especially in multi-join queries.
- **Document why.** Add a SQL comment explaining the reason for the hint so future maintainers don't remove it blindly.
- **Re-evaluate after upgrades.** Optimizer improvements in new TiDB versions may make existing hints unnecessary or counterproductive.
