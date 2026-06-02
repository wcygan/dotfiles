# Exchange Partition Can Duplicate `_tidb_rowid` and Skip Updates

## Status
- Partial
- Confidence: Medium

## User Symptom
- After `EXCHANGE PARTITION`, an `UPDATE` on a nonclustered primary-key table silently misses some rows.

## Likely Oncall Signals
- The affected table recently participated in `EXCHANGE PARTITION`.
- The table uses a nonclustered primary key.
- The missed rows are consistent with duplicated internal row IDs after the exchange.

## Missing Oncall Signals
- The handbook gives the root cause and fix PR, but does not provide a quick SQL-side integrity check to confirm the duplicate-rowid condition during incident handling.

## Fixed Version
- The handbook says the problem affects releases since `v6.5` and cites the fix PR.

## Public References
- https://github.com/pingcap/tidb/pull/65084
