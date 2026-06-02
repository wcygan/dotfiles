# Issue #65878: planner: plan-cache support queries with "int_col = str_val"

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/65878
- Status: open
- Type: type/enhancement
- Created At: 2026-01-28T09:51:56Z
- Labels: epic/plan-cache, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- According to [our official document](), if a query contains a predicate like "int_col = str_val", it can't hit the plan cache, please see the case below:

## Linked PRs
- Fix PR #66198: expression: skip refineArgs for comparisons when plan cache is active
  URL: https://github.com/pingcap/tidb/pull/66198
  State: closed
  Merged At: not merged
  Changed Files Count: 2
  Main Modules: pkg/expression, pkg/planner/core
  Sample Changed Files:
  - pkg/expression/builtin_compare.go
  - pkg/planner/core/casetest/plancache/plan_cache_suite_test.go
  PR Summary: What problem does this PR solve? Problem Summary: The  function in  tried to permit certain comparison argument refinements (e.g.  -> ) while marking the plan as uncacheable via . This unnecessarily prevented plan caching for queries with comparisons involving int, year, decimal, double, and datetime columns. What changed and how does it work? Removed the  function.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
