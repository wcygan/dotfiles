# Issue #66658: planner: decrease concurrency / batch_size automatically for streaming plans with limit-clause

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/66658
- Status: open
- Type: type/enhancement
- Created At: 2026-03-03T10:48:48Z
- Labels: report/customer, sig/execution, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- We have a clause, but TiDB still scanned more than 390000+ rows. The root cause is that our default concurrency (5, 15) and batch-size (25000) is too large. We have to scan and process more rows before the plan is stopped by the limit-clause. This could waste some system resources, like CPU.

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
