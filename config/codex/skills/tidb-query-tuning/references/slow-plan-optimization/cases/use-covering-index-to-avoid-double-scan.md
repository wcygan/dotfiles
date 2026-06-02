# Case: Use Covering Index to Avoid Double Scan

## Symptom

- Query is slow and plan shows `IndexLookUp`/double-read pattern.
- `EXPLAIN ANALYZE` shows high time in lookup/table-read side.

## Required Inputs

- Original SQL.
- `EXPLAIN ANALYZE` output.
- Related table schema (`SHOW CREATE TABLE`) and existing indexes.

## Plan Signature

- Bottleneck operator is `IndexLookUp` (or lookup-related path).
- Large gap between scanned rows and returned rows, with heavy table row fetch cost.
- Current index cannot cover all needed columns.

## Diagnosis

- This is usually a query plan problem (access path not ideal).
- Goal is to avoid table lookup by using a covering index when possible.

## Suggestions (Strict Order)

1. Binding or hints first.
   - If a better existing covering index already exists, guide user to force it by hint/binding first.
   - Example: `/*+ USE_INDEX(t, idx_a_b_c) */`.
2. Add new index.
   - Recommend a covering index only if no suitable existing index can cover predicates and required columns.
   - Avoid duplicated indexes: do not recommend a shorter prefix when a longer useful index already exists.
3. Rewrite query.
   - Reduce selected columns when possible to make existing index covering.

## Example

- Query:
  - `SELECT c FROM t WHERE a = ? AND b > ?;`
- Existing index:
  - `idx_a_b(a, b)` (not covering for selected column `c`)
- Better index candidate:
  - `idx_a_b_c(a, b, c)` (covering)
- Expected impact:
  - Shift from double-read lookup path toward index-only read path.

## Verification

- Re-run `EXPLAIN ANALYZE`.
- Confirm lower total time and lower lookup/table-read cost.
- Confirm no duplicated-index recommendation is introduced.
