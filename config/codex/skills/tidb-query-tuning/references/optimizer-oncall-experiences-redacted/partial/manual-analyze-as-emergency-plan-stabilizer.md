# Manual Analyze as Emergency Plan Stabilizer

## Status
- Partial
- Confidence: Medium

## User Symptom
- A query suddenly switches to a much heavier plan after recent data churn.
- TiKV CPU rises and `EXPLAIN ANALYZE` shows a large `estRows` vs `actRows` gap.

## When To Use
- `show stats_meta` is clearly stale or `modify_count` is high.
- The bad plan appears after bulk insert, delete, or obvious data distribution change.
- Manual `ANALYZE` on the table or partition is operationally affordable.

## When Not To Use
- `estRows` is already close to `actRows`, which suggests the main problem is not stale stats.
- The incident is primarily an engine-choice, binding, or plan-cache problem.
- The cluster is already resource-starved and an immediate analyze is likely to worsen the outage.

## Risks
- Analyze itself can be expensive, time out, or even trigger more pressure.
- On very large or skewed tables, a manual analyze may take much longer than expected.

## Missing Evidence
- The handbook contains many successful manual-analyze recoveries, but most do not spell out the hard threshold for when analyze is the right first action versus when it is only incidental.
