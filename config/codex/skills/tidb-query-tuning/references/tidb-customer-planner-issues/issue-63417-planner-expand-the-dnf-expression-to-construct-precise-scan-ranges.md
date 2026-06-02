# Issue #63417: planner: expand the DNF expression to construct precise scan ranges

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/63417
- Status: open
- Type: type/enhancement
- Created At: 2025-09-09T03:21:38Z
- Labels: plan-rewrite, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- In the case above, we can only use the first 2 columns in the index to construct the scan ranges: . Actually we can expand and rewrite the DNF with this formula: . Then we'll get a precise and better key scan range:

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
