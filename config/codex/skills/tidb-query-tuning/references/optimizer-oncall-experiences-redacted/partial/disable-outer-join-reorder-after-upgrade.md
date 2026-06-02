# Disable Outer Join Reorder After Upgrade

## Status
- Partial
- Confidence: Medium

## User Symptom
- A query changes plan after upgrade and loses the previous join order or index join opportunity.

## When To Use
- The main visible difference is join order.
- The regression appeared only after upgrade.
- Session-level validation with `set @@tidb_enable_outer_join_reorder = off` recovers the expected plan.

## When Not To Use
- The incident includes wrong results, executor build errors, or signs of a deeper rewrite bug.
- The old plan was never actually good; the upgrade only made an old schema or index problem visible.
- You have not compared the before/after join tree carefully.

## Risks
- Turning the flag off is a workload-wide optimizer behavior change if applied globally.
- It may restore one SQL while regressing others that benefit from reorder.

## Missing Evidence
- The handbook records multiple recoveries with this flag, but the safe rollout boundary is still workload-dependent rather than sharply defined.
