# Issue #62975: Make it possible to push Agg down cross UnionScan

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/62975
- Status: open
- Type: type/enhancement
- Created At: 2025-08-13T12:03:37Z
- Labels: affects-8.5, report/customer, sig/planner, sig/transaction, type/enhancement

## Customer-Facing Phenomenon
- As you can see, when there're dirty writes, the can not be pushed down to the coprocessor side. So the computation is left to the TiDB side. Compared with the normal execution without dirty writes, it's much slower.

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
