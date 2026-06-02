# RC Plus Forced MPP on Batch Point Get Can Error

## Status
- Partial
- Confidence: Medium

## User Symptom
- An ordinary `SELECT` unexpectedly errors under `READ COMMITTED` when MPP is strongly forced.

## Likely Oncall Signals
- Transaction isolation is `RC`.
- The query shape needs batch point get or a similar point-access path.
- A TiFlash-forcing hint or binding is present.

## Missing Oncall Signals
- The handbook records the public issue and cause, but not the exact end-user error text or the fastest way to distinguish it from a normal `SELECT FOR UPDATE` restriction.

## Public References
- https://github.com/pingcap/tidb/issues/65059
