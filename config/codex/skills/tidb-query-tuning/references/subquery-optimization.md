# Subquery Optimization

TiDB's optimizer decorrelates correlated subqueries by default, transforming them into joins. This is usually beneficial but not always. Especially in OLTP workloads. Understanding when to override this behavior is key to tuning subquery performance.

## How TiDB handles subqueries

1. **Decorrelation (default):** TiDB rewrites correlated subqueries (EXISTS, IN, scalar) into semi-joins, anti-semi-joins, or left outer joins. This allows the join to be executed with hash join or index join strategies.

2. **Correlated execution:** The subquery executes once per outer row. This is the fallback when decorrelation is disabled or not possible.

## NO_DECORRELATE

### Hint syntax

Place `NO_DECORRELATE()` inside the subquery's SELECT:

```sql
SELECT *
FROM orders o
WHERE EXISTS (
  SELECT /*+ NO_DECORRELATE() */ 1
  FROM returns r
  WHERE r.order_id = o.id
);
```

The hint applies to EXISTS, IN, and scalar correlated subqueries. TiDB will issue a warning if used on a subquery with no correlated columns (since there is nothing to decorrelate).

**Important:** When `NO_DECORRELATE()` is used on an EXISTS subquery, TiDB automatically injects a `LIMIT 1` into the subquery for early exit — it only needs to find one matching row per outer row.

### Session variable: `tidb_opt_enable_no_decorrelate_in_select`

| Property | Value |
|----------|-------|
| Scope | GLOBAL, SESSION |
| Default | OFF |
| Effect | Automatically applies NO_DECORRELATE behavior to correlated subqueries **in the SELECT list** (scalar subqueries) |

```sql
-- Enable for the session:
SET @@session.tidb_opt_enable_no_decorrelate_in_select = ON;

-- Enable globally:
SET GLOBAL tidb_opt_enable_no_decorrelate_in_select = ON;
```

**What this variable does:** Correlated subqueries in the SELECT list (scalar subqueries) are automatically kept as correlated execution (Apply) instead of being decorrelated into a left outer join. This also enables outer join elimination rules that can remove unnecessary Apply operators when the subquery result is not needed.

**When to use:**
- Your workload has many scalar subqueries in the SELECT list that are well-indexed on the correlation columns.
- The outer queries are generally selective.
- You want a session-wide or global policy rather than adding hints to every query.

**When NOT to use:**
- The SELECT-list subqueries reference large tables without indexes on the correlation columns — correlated execution will be slow.
- The outer queries return many rows — each row triggers a subquery probe.

**Note:** This variable only affects subqueries in the SELECT list. It does NOT affect EXISTS/IN subqueries in the WHERE clause — use the `NO_DECORRELATE()` hint directly for those.

### When to use NO_DECORRELATE

Use `NO_DECORRELATE()` (via hint or variable) when **all** of these are true:

- The **outer query is selective** — it produces few rows (after WHERE filtering), so the subquery executes only a small number of times.
- The **subquery has a good index** on the correlation column(s) — each correlated probe is a fast index lookup.
- The **inner table is large** — decorrelation would build a large hash table or produce a large semi-join build side.

In this scenario, correlated execution does N fast index lookups (where N is small), while decorrelation builds an expensive hash table over the entire inner table.

### When NOT to use NO_DECORRELATE

- The **outer query returns many rows** — correlated execution means many subquery probes, which is slow.
- The **subquery lacks indexes** on the correlation predicate — each probe is a full scan.
- The **inner table is small** — decorrelation into a hash join is cheap and often faster.

### Example: well-indexed EXISTS with selective outer query

```sql
-- Outer query filters orders to a small set; subquery probes returns by indexed order_id.
-- Decorrelation would hash-join the entire returns table. Correlated execution is cheaper.
SELECT *
FROM orders o
WHERE o.status = 'disputed'
  AND o.created_at > '2024-01-01'
  AND EXISTS (
    SELECT /*+ NO_DECORRELATE() */ 1
    FROM returns r
    WHERE r.order_id = o.id
      AND r.reason = 'defective'
  );
```

**Prerequisite:** An index on `returns(order_id, reason)` or at minimum `returns(order_id)`.

### Example: scalar subquery in SELECT list

```sql
-- With variable: automatically keeps the correlated scalar subquery as Apply
SET @@session.tidb_opt_enable_no_decorrelate_in_select = ON;

SELECT
  o.id,
  o.total,
  (SELECT MAX(r.created_at) FROM returns r WHERE r.order_id = o.id) AS last_return_date
FROM orders o
WHERE o.status = 'disputed';

-- Or with hint (works regardless of variable):
SELECT
  o.id,
  o.total,
  (SELECT /*+ NO_DECORRELATE() */ MAX(r.created_at) FROM returns r WHERE r.order_id = o.id) AS last_return_date
FROM orders o
WHERE o.status = 'disputed';
```

### Diagnostic: comparing with and without

```sql
-- Without hint (default decorrelation):
EXPLAIN ANALYZE
SELECT * FROM orders o
WHERE o.status = 'disputed'
  AND EXISTS (SELECT 1 FROM returns r WHERE r.order_id = o.id);

-- With hint (correlated execution):
EXPLAIN ANALYZE
SELECT * FROM orders o
WHERE o.status = 'disputed'
  AND EXISTS (SELECT /*+ NO_DECORRELATE() */ 1 FROM returns r WHERE r.order_id = o.id);
```

Compare total execution time and the operator tree. Look for:
- **With decorrelation:** `HashJoin` + `TableFullScan` on returns → expensive if returns is large.
- **With NO_DECORRELATE:** `Apply` + `IndexLookUp` on returns → cheap if outer rows are few. Note the automatic `Limit` operator inside the Apply for EXISTS subqueries.

## SEMI_JOIN_REWRITE

### What it does

Rewrites a semi-join into an inner join with aggregation (GROUP BY on the join keys). This transformation is:

```
-- Before (semi-join):
SELECT * FROM t WHERE EXISTS (SELECT 1 FROM s WHERE s.a = t.a);

-- After (inner join + dedup):
SELECT * FROM t JOIN (SELECT a FROM s GROUP BY a) s ON t.a = s.a;
```

The aggregation deduplicates the inner side on the join keys, converting the semi-join into a regular inner join. This unlocks additional join strategies and optimizations that may not be available for semi-joins.

### Hint syntax

Place `SEMI_JOIN_REWRITE()` inside the EXISTS subquery:

```sql
SELECT *
FROM orders o
WHERE EXISTS (
  SELECT /*+ SEMI_JOIN_REWRITE() */ 1
  FROM returns r
  WHERE r.order_id = o.id
);
```

### Session variable: `tidb_opt_enable_semi_join_rewrite`

| Property | Value |
|----------|-------|
| Scope | GLOBAL, SESSION |
| Default | OFF |
| Effect | Automatically applies SEMI_JOIN_REWRITE for all eligible semi-joins |

```sql
SET @@session.tidb_opt_enable_semi_join_rewrite = ON;
```

### When to use SEMI_JOIN_REWRITE

- The semi-join execution is slow (e.g., hash semi-join with a large build side).
- The inner side has **few duplicates on the join key** — the GROUP BY dedup cost is low.
- The rewritten inner join can use a better join strategy (e.g., index join) that wasn't available for the semi-join.

### When NOT to use SEMI_JOIN_REWRITE

- The inner side has **many duplicates on the join key** — the GROUP BY aggregation becomes expensive.
- The semi-join is already fast (hash semi-join with a small build side).
- The subquery is correlated (Apply) — SEMI_JOIN_REWRITE only works on **non-correlated** semi-joins (i.e., after decorrelation).

### Limitations

- **Only works for SemiJoin**, not LeftOuterSemiJoin. TiDB will warn: `SEMI_JOIN_REWRITE() is inapplicable for LeftOuterSemiJoin.`
- **Cannot have left conditions or other conditions** — only equal conditions on the join keys are supported.
- **Conflicts with NO_DECORRELATE:** If both hints are specified on the same subquery, TiDB disables both and warns: `NO_DECORRELATE() and SEMI_JOIN_REWRITE() are in conflict. Both will be ineffective.` This makes sense because NO_DECORRELATE keeps the subquery correlated (Apply), while SEMI_JOIN_REWRITE requires a decorrelated semi-join to rewrite.

### Example

```sql
-- The inner side (returns) has unique order_id values, so GROUP BY is cheap.
-- Rewriting to inner join allows the optimizer to use index join on orders.
SELECT *
FROM orders o
WHERE EXISTS (
  SELECT /*+ SEMI_JOIN_REWRITE() */ 1
  FROM returns r
  WHERE r.order_id = o.id
);

-- Equivalent rewritten plan:
-- SELECT * FROM orders o JOIN (SELECT order_id FROM returns GROUP BY order_id) r ON o.id = r.order_id;
```

## Semi-join patterns

When TiDB decorrelates an EXISTS subquery, it typically creates a **semi-join**. The execution strategy for the semi-join matters:

| Strategy | When it works well |
|----------|-------------------|
| Hash semi-join | Inner side fits in memory; no useful index on join key |
| Index semi-join (INL_JOIN) | Inner side has index on join key; outer side is moderate |
| Merge semi-join | Both sides sorted on join key |

You can combine hints:

```sql
-- Force index join for the semi-join after decorrelation
SELECT /*+ INL_JOIN(r) */ *
FROM orders o
WHERE EXISTS (SELECT 1 FROM returns r WHERE r.order_id = o.id);
```

## NOT EXISTS / NOT IN (anti-semi-join)

TiDB converts `NOT EXISTS` and `NOT IN` into anti-semi-joins. The same principles apply:
- Check whether decorrelation helps or hurts.
- `NO_DECORRELATE()` works for `NOT EXISTS` subqueries too.

**Caution with NOT IN:** `NOT IN` has NULL-handling semantics that can prevent optimization. Prefer `NOT EXISTS` when possible, as it avoids NULL edge cases and gives the optimizer more freedom.

## Decision flowchart

```
Is the subquery correlated?
├── NO  → TiDB handles it as an uncorrelated subquery (executed once). TiDB does not currently correlate an uncorrelated subquery. If performance is sub-optimal, a rewrite or other tuning options may be needed.
└── YES → Continue below.

Where is the subquery?
├── SELECT list (scalar subquery)
│   └── Is the outer query selective AND subquery well-indexed?
│       ├── YES → SET tidb_opt_enable_no_decorrelate_in_select = ON
│       │         (or use NO_DECORRELATE() hint on the subquery)
│       └── NO  → Let TiDB decorrelate (default).
│
└── WHERE clause (EXISTS / IN / NOT EXISTS / NOT IN)
    └── Is the outer query selective (few rows after filtering)?
        ├── YES → Does the subquery have a good index on correlation columns?
        │         ├── YES → Try NO_DECORRELATE(). Verify with EXPLAIN ANALYZE.
        │         └── NO  → Let TiDB decorrelate (default). Consider adding an index.
        └── NO  → Let TiDB decorrelate (default).
                  └── Is the semi-join strategy optimal?
                      ├── YES → Done.
                      ├── NO, and inner side has few duplicates on join key
                      │   → Try SEMI_JOIN_REWRITE() to convert to inner join + dedup.
                      └── NO  → Try INL_JOIN / HASH_JOIN hints on the semi-join tables.
```

## Summary: hints vs variables

| Mechanism | Scope | Applies to | Default |
|-----------|-------|------------|---------|
| `/*+ NO_DECORRELATE() */` | Per-subquery (hint) | EXISTS, IN, scalar subqueries in WHERE or SELECT | — |
| `tidb_opt_enable_no_decorrelate_in_select` | Session / Global | Scalar subqueries in the SELECT list only | OFF |
| `/*+ SEMI_JOIN_REWRITE() */` | Per-subquery (hint) | EXISTS subqueries (non-correlated semi-joins only) | — |
| `tidb_opt_enable_semi_join_rewrite` | Session / Global | All eligible semi-joins | OFF |

**Key rule:** `NO_DECORRELATE` and `SEMI_JOIN_REWRITE` are mutually exclusive on the same subquery. NO_DECORRELATE keeps the subquery correlated; SEMI_JOIN_REWRITE requires it to be decorrelated first. Specifying both cancels both.
