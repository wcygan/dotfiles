# ORDER BY LIMIT Picks the Ordering Index

## User Symptom
- A query with `WHERE` and `ORDER BY ... LIMIT` chooses the ordering index and becomes much slower.
- Index lookup count becomes very large, or the path degenerates into an index full scan.

## Investigation Signals
- The estimated row count on the ordering index is much smaller than the actual row count.
- The query shape has a real tradeoff between a filtering index and an ordering index.
- In some incidents, a temporary selectivity collapse to zero also pushed the plan toward the ordering index.

## Workaround
- On supported versions, tune `tidb_opt_ordering_index_selectivity_threshold` and related ordering-index knobs.
- On older releases, prefer SPM or explicit hints.
- If stale stats are involved, run manual analyze first before changing heuristics.

## Fixed Version
- This is mostly mitigated by configuration and SPM rather than a single universal fix.
