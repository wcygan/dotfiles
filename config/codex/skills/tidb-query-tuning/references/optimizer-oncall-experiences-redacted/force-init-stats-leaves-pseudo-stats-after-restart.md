# Force-Init Stats Leaves Pseudo Stats After Restart

## User Symptom
- After restart, queries keep using `stats:pseudo` for a long time and CPU rises because the wrong index is chosen.

## Investigation Signals
- The node starts with `force-init-stats=true` and `lite-init-stats=false`.
- `EXPLAIN` or `EXPLAIN ANALYZE` shows `stats:pseudo` on the chosen access path.
- There is no obvious sync-load error in logs, yet statistics still do not arrive for tens of minutes.
- Manual analyze immediately changes the plan and reduces the pressure.

## Workaround
- Run manual `ANALYZE` for the affected table or partition.
- Avoid routing full traffic to a freshly restarted node before stats warm-up is complete.

## Fixed Version
- The handbook points to follow-up fixes for missing table IDs during init and for sync-load starvation, but does not record a single release number.

## Public References
- https://github.com/pingcap/tidb/pull/58280
- https://github.com/pingcap/tidb/pull/58302
