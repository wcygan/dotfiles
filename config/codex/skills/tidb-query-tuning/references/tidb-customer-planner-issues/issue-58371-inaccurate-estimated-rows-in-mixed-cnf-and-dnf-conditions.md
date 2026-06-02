# Issue #58371: Inaccurate estimated rows in mixed CNF and DNF conditions

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/58371
- Status: open
- Type: type/bug
- Created At: 2024-12-18T06:33:43Z
- Labels: affects-6.5, affects-7.1, affects-7.5, affects-8.1, affects-8.5, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- The total selectivity is the product of the selectivities of the two CNF items, then the estRows equals , but the ranges  for the column id can probably be merged.

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
