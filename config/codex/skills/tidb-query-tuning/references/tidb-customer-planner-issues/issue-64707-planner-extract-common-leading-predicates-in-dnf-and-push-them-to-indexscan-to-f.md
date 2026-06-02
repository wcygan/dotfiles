# Issue #64707: planner: extract common leading predicates in DNF and push them to IndexScan to filter out unnecessary data earlier

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/64707
- Status: open
- Type: type/enhancement
- Created At: 2025-11-27T06:51:48Z
- Labels: plan-rewrite, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- Actually, we could extract some common leading predicates from that DNF, for example and then push it into to filter our some unnecessary data earlier:

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
