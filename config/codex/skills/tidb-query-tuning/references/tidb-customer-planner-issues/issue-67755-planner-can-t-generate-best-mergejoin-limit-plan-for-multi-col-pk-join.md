# Issue #67755: planner: can't generate best MergeJoin+Limit Plan for multi-col PK join

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67755
- Status: open
- Type: type/enhancement
- Created At: 2026-04-14T07:23:52Z
- Labels: plan-rewrite, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- But TiDB now can only generate (incur a large sort) or (incur massive double-read requests). The reason why TiDB needs a for is that the primary key is , but the order property is , since the column is missing in the order-clause, TiDB added a sort at the end. But actually, is a fixed value in this SQL , so PK should be able to satisfy the .

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
