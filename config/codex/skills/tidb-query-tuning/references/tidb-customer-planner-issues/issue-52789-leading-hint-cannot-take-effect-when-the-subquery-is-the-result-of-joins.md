# Issue #52789: LEADING hint cannot take effect when the subquery is the result of joins.

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/52789
- Status: open
- Type: type/enhancement
- Created At: 2024-04-22T03:17:55Z
- Labels: affects-7.1, affects-7.5, affects-8.1, affects-8.5, epic/hint, epic/sql-plan-management, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- For the SQL , we cannot use the LEADING hint to control the join order between the main query and the in subquery.

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
