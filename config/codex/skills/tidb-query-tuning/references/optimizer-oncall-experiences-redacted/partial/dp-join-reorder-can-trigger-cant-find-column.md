# DP Join Reorder Can Trigger `can't find column`

## Status
- Partial
- Confidence: Medium

## User Symptom
- A join query fails with a `can't find column` style error when DP join reorder is enabled.

## Likely Oncall Signals
- The failure is sensitive to join reorder settings such as `tidb_opt_join_reorder_threshold`.
- Disabling the relevant reorder behavior makes the query succeed.
- The problem appears during optimization or physical-plan generation rather than execution after a long runtime.

## Missing Oncall Signals
- The handbook cites the public issue but does not preserve a representative stack, exact error text variant, or minimal SQL shape.

## Public References
- https://github.com/pingcap/tidb/issues/63353
