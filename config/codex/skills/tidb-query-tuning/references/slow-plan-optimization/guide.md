# Slow Plan Optimization Sub-Module

This is a sub-module of `tidb-query-tuning`, not an independent skill entry point.

## Required Inputs

- Require the original SQL text (exact query sent to TiDB).
- Prefer real execution plans from `EXPLAIN ANALYZE` with runtime details (time cost, rows, loops, memory/disk when available).
- Ask whether the user can provide the related table schema (`SHOW CREATE TABLE` for involved tables).
- If the user only provides `EXPLAIN` (no runtime stats), ask for `EXPLAIN ANALYZE` before giving detailed optimization advice.
- Ask for missing required inputs before giving optimization advice.

## Workflow

- Confirm required inputs first (SQL, `EXPLAIN ANALYZE`, and schema if available).
- Identify the bottleneck operator in the execution plan first.
  - Define bottleneck operator as the operator that accounts for the largest time cost in the plan.
- If the bottleneck is `IndexJoin` or `IndexHashJoin`, inspect the inner/probe child before changing join strategy.
  - Separate "right join algorithm" from "right probe index".
  - Verify the probe-side `access object`, pushed predicates, and whether another existing index would give a tighter or more covering lookup path.
- Decide whether this is a query plan problem before proposing plan tuning.
  - If the bottleneck operator processes only a small number of rows but still takes a long time, treat it as likely not a query plan problem.
- If it is not a query plan problem, or there is no clear room for plan-side improvement, do not provide plan optimization suggestions.
  - Output a clear conclusion such as: "Can't improve this query from the plan perspective; this might be a <component> problem."
  - If plan is already optimal and bottleneck is at execution layer, suggest increasing execution engine concurrency as a possible non-plan solution.
- Use bottleneck-targeted methods first if and only if it is a query plan problem.
- Figure out optimization methods that directly target that bottleneck operator.
- Output suggestions in this strict order:
  1. Create SQL binding or add optimizer hints.
  2. Add new indexes.
  3. Rewrite the query.
- Re-run `EXPLAIN ANALYZE` to verify each applied change.

## Guardrails

- Keep recommendation priority fixed: binding/hints -> indexes -> query rewrite.
- Keep analysis priority fixed: identify bottleneck operator -> optimize bottleneck -> output suggestions.
- Keep diagnosis priority fixed: determine plan problem vs non-plan problem before plan changes.
- If diagnosis says non-plan problem, stop plan tuning and return only the non-plan conclusion.
- If diagnosis says execution-layer bottleneck with an already-optimal plan, allow concurrency tuning suggestion as non-plan guidance.
- For `IndexJoin` and `IndexHashJoin`, do not treat the join algorithm and the probe index as the same decision.
- Do not jump to index or SQL rewrite suggestions before considering binding/hints.
- Use runtime evidence from `EXPLAIN ANALYZE` to justify each recommendation.
- When recommending new indexes, avoid duplicated indexes.

## Index Recommendation Rules

- Treat indexes as duplicated when one index is a left-prefix of another index.
  - Example: `idx(a, b)` is duplicated by `idx(a, b, c)`.
- Prefer the longer duplicated index, because it can cover more predicates.
  - Example: `idx(a, b, c)` is better than `idx(a, b)` when both are candidates.
- If the plan is already using `idx(a, b, c)`, do not recommend `idx(a, b)` for queries like `WHERE a = ? AND b > ?`.
- If table schema already has `idx(a, b, c)`, do not recommend creating `idx(a, b)`.
- If there is an existing index that can cover more query predicates (especially `EQ`/`IN`) but the plan is not using it, treat this as a possible index-selection problem.
- For index-selection problems, guide the user to try optimizer hints/bindings first to force the better index choice.
  - Example: query `WHERE a = ? AND b = ? AND c > ? AND d = ?` uses `idx(a, c)`, but schema has `idx(a, b, d)`.
  - In this case, prefer guiding hint-based index selection before recommending new index creation.

## Non-Plan Cases

- `PointGet` or `BatchPointGet` as bottleneck usually means the plan is already optimal; suspect TiKV hotspot or storage-side latency.
- Exception: for non-clustered primary-key tables, `PointGet`/`BatchPointGet` can show double-read behavior (`num_rpc:2`). If workload is dominated by primary-key point lookups, consider clustered primary key table design to reduce RPCs.
- Small `IndexRangeScan`/`TableRangeScan` (for example ~100 rows) but long latency usually points to TiKV-side issues, not plan shape.
- Small-row `Hash`/`Agg`/`Sort` (for example ~1000 rows) but long latency is usually not a query plan problem.
- If plan is already optimal and bottleneck is execution-layer scheduling/compute, consider increasing execution engine concurrency.

## Useful References

- `cases/use-clustered-primary-key-for-pointget.md` - Use clustered primary key to reduce `PointGet`/`BatchPointGet` RPC count for primary-key point lookup workloads.
- `cases/use-covering-index-to-avoid-double-scan.md` - Use covering indexes to reduce index lookup double-read cost.
- `cases/use-tiflash-to-speed-up-large-scan.md` - Use TiFlash for large scan and analytical workloads.
- `cases/use-tiflash-mpp-for-large-join.md` - Use TiFlash or MPP for large joins when index-based join optimization is not feasible.
- `cases/use-tiflash-mpp-for-large-aggregation.md` - Use TiFlash or MPP for large aggregations when index-based StreamAgg optimization is not feasible.
- `cases/use-index-merge-for-dnf-predicates.md` - Consider IndexMerge for DNF predicates such as `a = ? OR b = ? OR c > ?`.
- `cases/use-covering-index-for-filter-and-order-by.md` - Use covering index to optimize `WHERE ... ORDER BY ...` patterns.
- `cases/use-correct-probe-index-for-index-join.md` - Validate whether `IndexJoin` or `IndexHashJoin` chose the right inner probe index before changing join strategy or adding indexes.
