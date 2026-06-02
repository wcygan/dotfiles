# Case: Use TiFlash to Speed Up Large Scan

## Symptom

- Query scans a large table and runs slowly.
- `EXPLAIN ANALYZE` shows large scan/aggregation operators dominating total time.

## Required Inputs

- Original SQL.
- `EXPLAIN ANALYZE` output.
- Related table schema and whether TiFlash replica is available for involved tables.

## Plan Signature

- Bottleneck is large scan plus heavy compute (`TableFullScan`, `HashAgg`, `Sort`, or join over large input).
- Row count is large, so this is not a small-row non-plan case.
- Plan is using TiKV path while workload is analytical/scan-heavy.

## Diagnosis

- This is a plan-selection opportunity when TiFlash is available but not chosen.
- Goal is to route large scan/compute to TiFlash.

## Suggestions (Strict Order)

1. Binding or hints first.
   - Guide user to force TiFlash with hints/bindings before schema changes.
   - Example hint: `/*+ READ_FROM_STORAGE(TIFLASH[t]) */`.
2. Add new index.
   - Only suggest index if query is actually selective and index can reduce scanned rows materially.
   - For true large analytical scans, index may not be the best next step.
3. Rewrite query.
   - Push down filters earlier and reduce scanned columns where possible.
   - Use pre-aggregation/query decomposition when it reduces scanned data.

## Example

- Query pattern:
  - `SELECT d, SUM(m) FROM t WHERE dt >= ? AND dt < ? GROUP BY d;`
- Situation:
  - Plan performs large TiKV scan with expensive aggregation.
  - TiFlash replica exists for `t` but is not selected.
- Action:
  - Try `/*+ READ_FROM_STORAGE(TIFLASH[t]) */` via direct hint or SQL binding.

## Verification

- Re-run `EXPLAIN ANALYZE`.
- Confirm scan/agg operators run on TiFlash path and end-to-end latency improves.
- If improvement is unstable, keep binding and document fallback behavior.
