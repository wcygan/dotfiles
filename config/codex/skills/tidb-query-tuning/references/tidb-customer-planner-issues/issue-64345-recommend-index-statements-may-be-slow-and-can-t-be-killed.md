# Issue #64345: `Recommend Index` statements may be slow and can't be killed

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/64345
- Status: open
- Type: type/enhancement
- Created At: 2025-11-07T08:39:42Z
- Labels: affects-8.5, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- What's worse, during this process, there is no checkpoint for the timeout option or signal, so the user is not able to it, and the timeout option is also ineffective.

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
