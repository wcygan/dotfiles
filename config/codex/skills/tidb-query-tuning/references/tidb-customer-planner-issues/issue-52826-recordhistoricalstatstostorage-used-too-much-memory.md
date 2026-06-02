# Issue #52826: `RecordHistoricalStatsToStorage` used too much memory

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/52826
- Status: open
- Type: type/enhancement
- Created At: 2024-04-23T03:08:38Z
- Labels: affects-7.5, component/statistics, report/customer, severity/moderate, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- <img width="1824" alt="image" src=" It seems that there are many long insert internal SQL statements in the session pool of the domain, and it appears that they have not been cleaned up properly.

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
