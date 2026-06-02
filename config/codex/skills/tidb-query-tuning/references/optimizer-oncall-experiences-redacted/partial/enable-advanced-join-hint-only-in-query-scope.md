# Enable Advanced Join Hint Only in Query Scope

## Status
- Partial
- Confidence: Medium

## User Symptom
- `leading()` appears ineffective when it is used together with a join-method hint such as `inl_join`.

## When To Use
- The cluster originated from an older release line where `tidb_opt_advanced_join_hint` remains off.
- The query needs both join order control and join method control.
- A local `set_var(tidb_opt_advanced_join_hint=1)` hint restores the intended behavior.

## When Not To Use
- You are considering enabling the variable globally without workload review.
- The query already behaves correctly with simpler hints.

## Risks
- Global enablement is a real behavior change and can alter historical hint semantics.

## Missing Evidence
- The handbook clearly describes the mechanism but not a broader rollout playbook, so this remains a local workaround pattern rather than a mature SOP.
