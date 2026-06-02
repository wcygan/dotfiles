# Analyze Retry Stuck When Global Time Zone Differs

## Status
- Partial
- Confidence: Medium

## User Symptom
- A failed analyze job does not retry for an unexpectedly long time.

## Likely Oncall Signals
- Auto analyze for the same table appears stalled after one failure.
- Global `time_zone` differs from `SYSTEM`.
- No obvious new retry job is scheduled even though the table remains unhealthy.

## Missing Oncall Signals
- The handbook records the issue and public bug, but does not provide concrete log keywords or metric panels that confirm this path quickly.

## Public References
- https://github.com/pingcap/tidb/issues/65815
