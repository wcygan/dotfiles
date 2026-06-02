# Case: Use IndexMerge for DNF Predicates

## Symptom

- Query has DNF predicates like `WHERE a = ? OR b = ? OR c > ?`.
- Current plan scans too many rows or falls back to table scan.

## Required Inputs

- Original SQL.
- `EXPLAIN ANALYZE` output.
- Related table schema and existing indexes.

## Plan Signature

- Predicate contains multiple `OR` branches.
- Single-index access path is not selective enough for all branches.
- Bottleneck operator is scan-heavy and row filtering happens late.

## Diagnosis

- This is a potential plan problem where IndexMerge can combine multiple index paths for DNF filters.
- Confirm each major `OR` branch has a usable index candidate.

## Suggestions (Strict Order)

1. Binding or hints first.
   - Guide user to try IndexMerge using hints/bindings first.
   - Example hint:
     - `/*+ USE_INDEX_MERGE(t, idx_a, idx_b, idx_c) */`
2. Add new index.
   - Add missing branch indexes only when an important `OR` branch has no usable index.
   - Avoid duplicated indexes (left-prefix duplicates).
3. Rewrite query.
   - Simplify DNF branches.
   - Remove redundant predicates.
   - Consider splitting into `UNION ALL` forms only when it is clearer and faster.

## Example

- Query:
  - `SELECT * FROM t WHERE a = ? OR b = ? OR c > ?;`
- Situation:
  - Existing plan does not use effective multi-index access.
  - Table has `idx_a(a)`, `idx_b(b)`, `idx_c(c)`.
- Action:
  - Try IndexMerge via hint/binding, then verify scan row reduction.

## Verification

- Re-run `EXPLAIN ANALYZE`.
- Confirm IndexMerge path is selected and total scanned rows/time decrease.
- Confirm no duplicated-index recommendation is introduced.
