# Issue #54125: join reorder using greedy algorithm use wrong rule for the cost of limit operator

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/54125
- Status: open
- Type: type/enhancement
- Created At: 2024-06-19T15:49:55Z
- Labels: affects-6.5, epic/cardinality-estimation, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- I expect the join order for that query is: rel (limit20)  INNER JOIN rel LEFT JOIN info But the actual order is rel LEFT JOIN info INNER JOIN rel (limit 20)

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
