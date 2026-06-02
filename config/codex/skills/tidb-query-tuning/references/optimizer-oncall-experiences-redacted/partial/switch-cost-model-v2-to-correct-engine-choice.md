# Switch Cost Model V2 to Correct Engine Choice

## Status
- Partial
- Confidence: Medium

## User Symptom
- The optimizer chooses TiKV instead of TiFlash, or chooses another clearly worse engine path, and overall latency or TiKV pressure rises.

## When To Use
- `EXPLAIN ANALYZE` shows `estRows` close to `actRows`, so stale stats are not the main suspect.
- The plan is chosen by the optimizer rather than by binding or manual hint.
- Evidence points to a cost-model v1 misjudgment instead of a missing index.

## When Not To Use
- The cluster cannot tolerate broad plan churn.
- The problem is isolated to one or two SQLs that can be safely controlled by binding or hint.
- There are still unresolved stats-quality problems.

## Risks
- Switching cost model is a workload-wide behavior change.
- After the switch, some unrelated SQLs may change plans and need follow-up bindings.

## Missing Evidence
- The handbook strongly suggests this workaround in several cases, but does not define a crisp decision tree for when the global switch is preferable to local binding.
