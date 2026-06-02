# Case: Fix Wrong Probe Index for `IndexJoin` or `IndexHashJoin`

## Symptom

- Query already uses `IndexJoin` or `IndexHashJoin`, but latency is still high.
- The inner/probe side uses an existing index that is not the best match for join keys, pushed filters, or covering columns.
- `EXPLAIN ANALYZE` often shows expensive `IndexLookUp`, extra `TableRowIDScan`, or residual probe-side filters.

## Required Inputs

- Original SQL.
- `EXPLAIN ANALYZE` output.
- Related table schema (`SHOW CREATE TABLE`) and existing indexes.

## Plan Signature

- Join operator is `IndexJoin` or `IndexHashJoin`.
- The join choice itself is reasonable, but the probe child uses the wrong `access object`.
- Another existing index would allow tighter join-key lookup, more pushed predicates, or a more covering probe path.

## Diagnosis

- Do not assume the probe index is correct just because TiDB picked an index-based join.
- Separate two questions:
  1. Is `IndexJoin` or `IndexHashJoin` the right join algorithm?
  2. Is the chosen probe index the right inner access path?
- If the join algorithm is reasonable but the inner index is not, treat this as an index-selection problem.

## Suggestions (Strict Order)

1. Binding or hints first.
   - Compare candidate probe indexes with `EXPLAIN ANALYZE`, for example `USE_INDEX(probe_table, idx_name)` or `IGNORE_INDEX(probe_table, idx_name)`.
   - If a better existing index wins, keep the join and stabilize it with `USE_INDEX(...)` plus a SQL binding or query hint.
2. Add new index.
   - Only if no existing probe-side index matches the join keys and selective filters well enough.
   - Prefer indexes that put join equality columns first, then additional `=` or `IN` filters, then range columns.
3. Rewrite query.
   - Rewrite only when hints/bindings and existing indexes still cannot produce a stable probe path.

## Example 1

- Inner table `t2` has `ab(a, b)` and `ac(a, b, c, d)`.
- Query shape:
  - `SELECT /*+ TIDB_INLJ(t2) */ t2.a FROM t1, t2 WHERE t1.a = t2.a AND t2.b = 1 AND t2.d = 1`
- Bad plan:
  - `IndexJoin` probes `t2` through `ab(a, b)` and leaves `d = 1` as a later residual filter plus table lookup.
- Better plan:
  - `USE_INDEX(t2, ac)` lets the probe side use `ac(a, b, c, d)`, keeping more work on the index path and reducing probe cost.
- Tuning takeaway:
  - The join algorithm was acceptable; the probe index was not.

## Example 2

- Probe table `mp` has `idx_1(col2, col6, col7)` and `idx_2(col3, col5, col6, col4)`.
- Query uses `IndexHashJoin` with join keys `ab.col1 = mp.col2` and `ab.col2 = mp.col6`, plus extra filters on `mp`.
- Bad plan:
  - Probe side uses `idx_2(col3, col5, col6, col4)`, which matches local filters but not the full join-key prefix.
- Better plan:
  - Probe side uses `idx_1(col2, col6, col7)` so the join lookup is driven by the join equalities first, with remaining filters applied later.
- Tuning takeaway:
  - `IndexHashJoin` can still need `USE_INDEX` or a binding to pick the right probe path.

## Verification

- Re-run `EXPLAIN ANALYZE` with each candidate probe index forced.
- Confirm lower probe-side time, fewer scanned rows, and less residual filtering or table lookup work.
- If the hinted plan is consistently better, create a SQL binding or keep the query hint with a short reason comment.
