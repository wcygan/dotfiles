# Issue #56683: the pushed operator should scale with regions & index lookup will issue too much cop tasks.

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/56683
- Status: open
- Type: type/enhancement
- Created At: 2024-10-16T09:01:43Z
- Labels: affects-7.5, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- * the pushed operator's cost should multiple region num? * we should make a trade-off between row count est and cop task number, especially for index lookup. * a kind of regionScan(distinguished from rowIDScan and FullScan) should be tested after discussion with @chenshuang

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
