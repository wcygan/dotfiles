# Issue #52650: Correlated subquery will block the join reorder and the correlated subquery should not be executed before joins

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/52650
- Status: open
- Type: type/enhancement
- Created At: 2024-04-16T15:41:16Z
- Labels: planner/join-order, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- The actual join group is (t, t2, t3, t4). But as you can see, the Apply is inserted and split the join group into two parts.

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
