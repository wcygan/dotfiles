# Issue #67854: planner: avoid materializing IN (SELECT DISTINCT ...) subqueries when semi-join is possible

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67854
- Status: open
- Type: type/compatibility
- Created At: 2026-04-17T10:16:29Z
- Labels: affects-8.5, component/executor, report/customer, sig/planner, type/compatibility, type/performance

## Customer-Facing Phenomenon
- TiDB materializes/deduplicates the subquery result with aggregation before evaluating the  predicate. In the observed case, the inner table statistics are large enough that this produces a plan with  over a  of the inner table. Observed impact from the production-like case: | Query shape | Plan shape | Observed memory | | --- | --- | --- |

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
