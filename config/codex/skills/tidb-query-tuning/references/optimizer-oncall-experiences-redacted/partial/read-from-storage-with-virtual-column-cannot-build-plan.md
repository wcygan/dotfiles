# `read_from_storage` With a Virtual Column Cannot Build a Physical Plan

## Status
- Partial
- Confidence: Medium

## User Symptom
- A query using `read_from_storage(...)` fails with a `can't find physical plan` style error.

## Likely Oncall Signals
- The query references a virtual column.
- The failure only appears when the storage-engine hint is added.
- Affected versions include `v7.5.6` according to the handbook.

## Missing Oncall Signals
- The handbook does not preserve a representative failing SQL shape or the exact planner warning text.

## Fixed Version
- `v8.1.2`

## Public References
- https://github.com/pingcap/tidb/pull/48041
