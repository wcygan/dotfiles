# Issue #67468: support join reorder for semi join

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67468
- Status: open
- Type: type/enhancement
- Created At: 2026-03-31T12:49:43Z
- Labels: report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- tidb generate the bad plan because we didn't support reorder semi join for now, we'd better support it. Because using hint is not suitable for all situations.

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
