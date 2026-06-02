# Cost Model V1 Picks the Wrong Engine

## User Symptom
- A query that used to run on TiFlash suddenly runs on TiKV and becomes much slower.
- TiKV CPU rises sharply because the new path triggers heavy scan or lookup work.

## Investigation Signals
- `EXPLAIN ANALYZE` shows `estRows` close to `actRows`, so the main problem is probably not stale stats.
- `EXPLAIN FORMAT='verbose'` or reproduced plans show the engine choice is driven by cost model behavior.
- Slow query history or clinic confirms the optimizer, not a manual binding, selected the worse engine.

## Workaround
- Prefer cost model v2 on supported releases.
- If switching cost model globally is too risky, bind or hint the intended engine for the problematic SQL and monitor the fallout.

## Fixed Version
- The handbook treats cost model v2 as the practical fix path on supported versions rather than a one-off patch.
