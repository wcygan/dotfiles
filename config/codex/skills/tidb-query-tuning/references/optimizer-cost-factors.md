# Optimizer Cost Factors

TiDB provides a set of `tidb_opt_*_cost_factor` variables that act as multipliers on the cost model. Each variable controls the cost of a specific physical operator. By adjusting these multipliers you can **encourage** or **discourage** the optimizer from choosing particular operators without using hard-coded hints.

These cost factors were delivered to allow the EXPLAIN EXPLORE feature of TiDB to iterate through alternative cost factors and explore other viable query plans that may not have been chosen as the winning plan initially.

## How cost factors work

- Every cost factor **defaults to 1.0** (neutral — no adjustment).
- The factor is a **multiplier** on the operator's calculated cost:
  - **Lower than 1.0** (e.g., 0.5) → makes the operator **cheaper** → **encourages** the optimizer to choose it.
  - **Higher than 1.0** (e.g., 10 or 100) → makes the operator **more expensive** → **discourages** the optimizer from choosing it.
- The optimizer still uses cost-based selection — the factor biases the cost, it doesn't force or disable the operator entirely.

## Setting cost factors

Cost factors can be set at three scopes:

### Global (all new connections)

```sql
SET GLOBAL tidb_opt_hash_join_cost_factor = 10;
```

Use for cluster-wide tuning when a workload systematically benefits from avoiding (or favoring) a particular operator.

### Session (current connection only)

```sql
SET @@session.tidb_opt_table_full_scan_cost_factor = 100;
```

Use for a specific workload or batch job within a single connection.

### Per-query via SET_VAR hint

```sql
SELECT /*+ SET_VAR(tidb_opt_hash_join_cost_factor=100) */ *
FROM orders o JOIN customers c ON o.cust_id = c.id;
```

Use for surgical, per-query tuning — the most precise approach. The variable is set only for the duration of that single statement.

## Complete cost factor catalog

### Scan operators

| Variable | Operator affected | Use case |
|----------|-------------------|----------|
| `tidb_opt_table_full_scan_cost_factor` | TableFullScan | Increase to discourage full table scans; the optimizer will prefer index scans when available |
| `tidb_opt_table_range_scan_cost_factor` | TableRangeScan | Adjust cost of range scans on the primary key / clustered index |
| `tidb_opt_table_rowid_scan_cost_factor` | TableRowIDScan | Adjust cost of scanning by row ID (typically after an index lookup) |
| `tidb_opt_index_scan_cost_factor` | IndexScan (single index range scan) | Lower to encourage index scans; increase to push toward full scans or other indexes |
| `tidb_opt_table_tiflash_scan_cost_factor` | TiFlash table scan | Lower to encourage TiFlash reads for analytical queries; increase to prefer TiKV |

### Reader operators (TiDB ↔ storage layer)

| Variable | Operator affected | Use case |
|----------|-------------------|----------|
| `tidb_opt_table_reader_cost_factor` | TableReader (reads full rows from TiKV) | Adjust the cost of reading full table data from TiKV |
| `tidb_opt_index_reader_cost_factor` | IndexReader (reads from index only, no table lookup) | Adjust the cost of covering index reads |
| `tidb_opt_index_lookup_cost_factor` | IndexLookUp (index scan + table lookup) | Increase to discourage index lookups when the table lookup is expensive; lower to encourage them |
| `tidb_opt_index_merge_cost_factor` | IndexMerge (combines multiple indexes) | Lower to encourage index merge for OR conditions; increase if index merge is causing overhead |

### Join operators

| Variable | Operator affected | Use case |
|----------|-------------------|----------|
| `tidb_opt_hash_join_cost_factor` | HashJoin | Increase to discourage hash joins (e.g., when memory is constrained); lower to encourage them |
| `tidb_opt_index_join_cost_factor` | IndexJoin (index nested loop join) | Lower to encourage index joins when the inner side has a good index; increase if index join probes are expensive |
| `tidb_opt_merge_join_cost_factor` | MergeJoin | Lower to encourage merge joins when data is pre-sorted; increase to prefer hash or index joins |

### Aggregation operators

| Variable | Operator affected | Use case |
|----------|-------------------|----------|
| `tidb_opt_hash_agg_cost_factor` | HashAgg | Increase to discourage hash aggregation; lower to encourage it |
| `tidb_opt_stream_agg_cost_factor` | StreamAgg | Lower to encourage stream aggregation when data is sorted on the GROUP BY key |

### Other operators

| Variable | Operator affected | Use case |
|----------|-------------------|----------|
| `tidb_opt_sort_cost_factor` | Sort | Increase to discourage explicit sort operators (optimizer may prefer index-ordered reads instead) |
| `tidb_opt_topn_cost_factor` | TopN (sort + limit combined) | Adjust cost of TopN operations |
| `tidb_opt_limit_cost_factor` | Limit | Adjust cost of Limit operators |

## Practical examples

### Discourage full table scans, prefer index access

```sql
-- Session-wide: make full table scans 100x more expensive
SET @@session.tidb_opt_table_full_scan_cost_factor = 100;

-- Per-query alternative:
SELECT /*+ SET_VAR(tidb_opt_table_full_scan_cost_factor=100) */ *
FROM orders WHERE status = 'pending';
```

### Discourage hash join, encourage index join

When the inner table has a good index on the join key but the optimizer keeps choosing hash join:

```sql
SELECT /*+ SET_VAR(tidb_opt_hash_join_cost_factor=100) SET_VAR(tidb_opt_index_join_cost_factor=0.5) */ *
FROM orders o JOIN customers c ON o.cust_id = c.id
WHERE o.created_at > '2024-01-01';
```

### Encourage TiFlash for analytical queries

```sql
SELECT /*+ SET_VAR(tidb_opt_table_tiflash_scan_cost_factor=0.1) */
  region, SUM(amount)
FROM orders
GROUP BY region;
```

### Discourage sort operators (prefer index-ordered reads)

```sql
SET @@session.tidb_opt_sort_cost_factor = 50;

SELECT * FROM orders ORDER BY created_at DESC LIMIT 20;
-- Optimizer will now strongly prefer an index on created_at over a full scan + sort
```

### Combine multiple factors to reshape a complex query plan

```sql
-- Discourage full scans and hash joins; encourage index lookups
SELECT /*+
  SET_VAR(tidb_opt_table_full_scan_cost_factor=100)
  SET_VAR(tidb_opt_hash_join_cost_factor=50)
  SET_VAR(tidb_opt_index_lookup_cost_factor=0.5)
*/ *
FROM orders o
JOIN items i ON i.order_id = o.id
JOIN products p ON p.id = i.product_id
WHERE o.status = 'active';
```

## Cost factors vs hints

| Approach | Precision | Effect |
|----------|-----------|--------|
| **Hints** (e.g., `HASH_JOIN(t1, t2)`) | Forces a specific operator | Hard override — optimizer has no choice |
| **Cost factors** | Biases the cost model | Soft influence — optimizer still picks the cheapest plan, but costs are weighted differently |

**When to prefer cost factors over hints:**
- You want to **nudge** the optimizer without completely overriding it.
- The query has many joins or operators, and hinting each one is impractical.
- You want a **session-wide or global** policy (e.g., "always discourage full scans") rather than per-query tuning.
- You have a pure OLTP application and want to discourage OLAP style operations (table full scans, hash joins etc).
- You're unsure which specific operator is the problem — adjusting cost factors lets the optimizer re-evaluate the whole plan.

**When to prefer hints:**
- You know exactly which operator and which tables should use a specific strategy.
- You need to force a certain query join order or index choice
- Cost factor adjustments still don't produce the desired plan.

**What if the cost factor doesn't discourage the operator?:**
- It's possible that the desired operator isn't valid for this plan - for example, discouraging hash join won't impact a query that doesn't involve a join.
- There are logical rewrites in the optimizer that may disable some plan choices. An example is for correlated subqueries, if you're not seeing a desired index join it may be because the optimizer decorrelated the subquery, and the solution is either the NO_DECORRELATE() hint or for subqueries in the select list you can use the session/global variable tidb_opt_enable_no_decorrelate_in_select. 

## Diagnostic workflow

1. Run `EXPLAIN ANALYZE` on the slow query.
2. Identify the problematic operator (e.g., an unnecessary TableFullScan or HashJoin with a huge build side).
3. Increase the cost factor for the unwanted operator and/or decrease the factor for the preferred alternative.
4. Re-run `EXPLAIN ANALYZE` and compare execution time and plan shape.
5. If the plan improves, decide the right scope (per-query SET_VAR, session, or global).

## Cautions

- **Don't set extreme values globally without testing.** A global `tidb_opt_table_full_scan_cost_factor = 1000` will affect every query in the cluster, including those where a full scan is genuinely the best plan.
- **Prefer per-query SET_VAR for targeted tuning.** It's the safest scope — no side effects on other queries.
- **Cost factors don't disable operators.** Even at very high values, the optimizer may still choose the operator if there is no alternative. Use hints to truly force a choice.
- **Re-evaluate after stats refresh.** A bad plan caused by stale stats may resolve itself after `ANALYZE TABLE`, making the cost factor adjustment unnecessary.
- **Document non-default settings.** If you set cost factors at session or global scope, document the reason so future maintainers understand the intent.
