# `REGEXP` or `RLIKE` on `information_schema` Can Be Wrong

## Status
- Partial
- Confidence: Medium

## User Symptom
- A query against certain `information_schema` tables returns wrong results when filtered with `REGEXP` or `RLIKE`.

## Likely Oncall Signals
- The incorrect result only appears on system tables in `information_schema`.
- Equivalent filters behave more like `LIKE` than true regex matching.
- The bug is very old, so it may surface during compatibility validation rather than after a recent regression.

## Missing Oncall Signals
- The handbook does not record which exact system tables are known to be affected or a fastest differential query to confirm the bug.

## Public References
- https://github.com/pingcap/tidb/issues/64249
