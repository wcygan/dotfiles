# Case: Use Covering Index for `WHERE ... ORDER BY ...`

## Symptom

- Query has selective filters plus sorting, for example `WHERE a = ? AND b = ? ORDER BY c`.
- Plan shows extra sort cost or double-read lookup cost.

## Required Inputs

- Original SQL.
- `EXPLAIN ANALYZE` output.
- Related table schema and existing indexes.

## Plan Signature

- Filter columns and order-by columns are not aligned in one good index.
- Plan may include `Sort` on filtered rows or `IndexLookUp` with extra table reads.
- Bottleneck operator is sort-heavy or lookup-heavy.

## Diagnosis

- This is a potential plan/access-path problem.
- A covering index that matches filter prefix and order key can reduce lookup and sort overhead.

## Suggestions (Strict Order)

1. Binding or hints first.
   - If a suitable existing index already exists, guide user to force it with hints/bindings first.
2. Add new index.
   - Consider index like `idx(a, b, c)` for query shape `WHERE a = ? AND b = ? ORDER BY c`.
   - Ensure no duplicated index recommendation (left-prefix duplicates).
3. Rewrite query.
   - Reduce selected columns and simplify ordering requirements when possible.

## Example

- Query:
  - `SELECT c FROM t WHERE a = ? AND b = ? ORDER BY c;`
- Better index candidate:
  - `idx(a, b, c)`
- Why:
  - `a, b` support filtering.
  - `c` supports ordered access and can help avoid extra sort.
  - When selected columns are covered, it can also avoid double-read lookup.

## Verification

- Re-run `EXPLAIN ANALYZE`.
- Confirm reduced sort/lookup cost and lower total latency.
- Confirm no duplicated-index recommendation is introduced.
