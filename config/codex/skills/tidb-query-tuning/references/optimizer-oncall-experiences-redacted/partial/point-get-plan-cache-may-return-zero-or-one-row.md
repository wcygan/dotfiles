# Point Get Plan Cache May Return Zero or One Row

## Status
- Partial
- Confidence: Low

## User Symptom
- The same point-get query under plan cache sometimes returns the expected single row and sometimes does not.

## Likely Oncall Signals
- The query is a point-get shape and uses plan cache.
- The application side insists the same key should always return one row.
- Metadata lock is already enabled, so the old obvious explanation may not apply.

## Missing Oncall Signals
- The handbook explicitly says the issue is still unrevealed.
- There is no stable reproduction recipe or decisive monitoring/log signature yet.

## Public References
- https://github.com/pingcap/tidb/issues/64351
