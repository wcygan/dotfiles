# Issue #64276: Planner: Incorrect estRows on Projection with PointGet

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/64276
- Status: open
- Type: type/bug
- Created At: 2025-11-05T01:52:36Z
- Labels: affects-8.5, report/customer, sig/planner, type/bug

## Customer-Facing Phenomenon
- When a parent LogicalProjection derives statistics, it copies the child’s RowCount in DeriveStats. Later in physical optimization, the plan may be rewritten by ConvertToPointGet, which updates the child’s stats.RowCount (e.g., to 1 for PointGet). However, the parent Projection’s previously copied RowCount is not refreshed, so its estRows becomes inconsistent with the child and remains significantly larger. This leads to wrong cost, sub-optimal plan choice, and misleading EXPLAIN output (parent shows thousands of rows while the child is Point_Get with 1 row).

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
