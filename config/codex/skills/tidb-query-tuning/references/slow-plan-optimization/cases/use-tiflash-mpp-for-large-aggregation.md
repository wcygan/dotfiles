# Case: Use TiFlash or MPP for Large Aggregation

## Symptom

- Query is dominated by aggregation cost on large scanned data.
- `EXPLAIN ANALYZE` shows `HashAgg`/`StreamAgg` with high time and large input rows.

## Required Inputs

- Original SQL.
- `EXPLAIN ANALYZE` output.
- Related table schema and existing indexes.
- TiFlash replica status for involved large tables.

## Plan Signature

- Bottleneck operator is large-scale `HashAgg`/`StreamAgg`.
- Plan is mainly on TiKV path.
- No practical index path to turn this into an efficient selective scan plus `StreamAgg`.

## Diagnosis

- This is a plan-selection opportunity for large aggregation workloads.
- If index optimization cannot materially reduce scanned rows or enforce cheap ordered aggregation, prefer TiFlash/MPP path.

## Suggestions (Strict Order)

1. Binding or hints first.
   - Guide user to force TiFlash storage and MPP plan where suitable.
   - Example hint:
     - `/*+ READ_FROM_STORAGE(TIFLASH[t]) */`
   - Use SQL binding for stable reuse.
2. Add new index.
   - Recommend indexes only if they can materially improve selectivity or support better ordered aggregation.
   - If workload is large analytical aggregation, prioritize TiFlash/MPP over index expansion.
3. Rewrite query.
   - Push filters before aggregation.
   - Pre-aggregate in subqueries when it reduces rows early.
   - Remove unnecessary selected columns.

## Example

- Query pattern:
  - `SELECT k, SUM(v) FROM t WHERE dt >= ? AND dt < ? GROUP BY k;`
- Situation:
  - Very large scan and heavy aggregation.
  - Existing indexes cannot make aggregation cheap enough.
- Action:
  - Prefer TiFlash/MPP via hint/binding before new index proposals.

## Verification

- Re-run `EXPLAIN ANALYZE`.
- Confirm aggregation-heavy operators move to TiFlash/MPP path and latency improves.
- Confirm result correctness and acceptable resource usage.
