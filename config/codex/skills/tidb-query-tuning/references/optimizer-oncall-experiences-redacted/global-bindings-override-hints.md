# Global Bindings Override Hints

## User Symptom
- A query keeps using the bound plan even after adding `FORCE INDEX`, `IGNORE_INDEX`, or other hints.
- Dropping a session binding does not change the plan.

## Investigation Signals
- The unexpected plan persists only in environments where a global binding exists.
- Plan replayer or isolated reproduction may not show the global binding, which makes frontline debugging confusing.

## Workaround
- For session-level validation, disable baselines in that session:
  `set @@session.tidb_enable_plan_baselines = 0;`
- Check whether a global binding matches the query before trusting hint tests.
- Remove or adjust the global binding if the binding itself is stale.

## Fixed Version
- No code fix was identified in the handbook. This is mostly expected behavior plus an operational pitfall.
