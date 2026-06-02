# Case: Use TiFlash or MPP for Large Join

## Symptom

- Query is dominated by large join cost.
- `EXPLAIN ANALYZE` shows join operators consuming most time with large input rows.

## Required Inputs

- Original SQL.
- `EXPLAIN ANALYZE` output.
- Related table schema and existing indexes.
- TiFlash replica status for involved large tables.

## Plan Signature

- Bottleneck operator is `HashJoin`/`MergeJoin` over large row sets.
- Current plan runs mostly on TiKV path.
- No practical index path to transform this into an efficient `IndexJoin`.

## Diagnosis

- This is a plan-selection problem for large join workloads.
- If index design cannot realistically produce a good `IndexJoin`, prefer TiFlash/MPP path.

## Suggestions (Strict Order)

1. Binding or hints first.
   - Guide user to force TiFlash storage and MPP plan where suitable.
   - Example hints:
     - `/*+ READ_FROM_STORAGE(TIFLASH[t1, t2]) */`
     - `/*+ HASH_JOIN(t1, t2) */` (when needed to stabilize join shape)
   - Use SQL binding if hint effect should be persistent.
2. Add new index.
   - Recommend new indexes only if they can materially change join access into a better `IndexJoin`.
   - If large full/near-full joins remain unavoidable, do not force index creation.
3. Rewrite query.
   - Push highly selective filters before join.
   - Reduce join input columns and rows.
   - Break complex joins into staged subqueries when it lowers data volume.

## Example

- Query pattern:
  - `SELECT /* complex join */ ... FROM t1 JOIN t2 ON ... WHERE ...`
- Situation:
  - Join processes tens of millions of rows.
  - Existing indexes cannot produce a stable, fast `IndexJoin`.
- Action:
  - Prefer TiFlash/MPP path via hint/binding before new index design.

## Verification

- Re-run `EXPLAIN ANALYZE`.
- Confirm join-heavy operators move to TiFlash/MPP path and total latency improves.
- Validate that regression risk is acceptable for similar queries.
