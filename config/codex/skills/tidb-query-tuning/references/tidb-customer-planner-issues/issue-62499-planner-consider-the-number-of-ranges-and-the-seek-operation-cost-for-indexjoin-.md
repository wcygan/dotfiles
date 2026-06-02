# Issue #62499: planner: consider the number of ranges and the seek operation cost for IndexJoin in cost model

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/62499
- Status: closed
- Type: type/enhancement
- Created At: 2025-07-18T09:16:33Z
- Closed At: 2025-09-23T03:45:09Z
- Labels: affects-8.5, epic/cost-model, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- IndexJoin's cost evaluation and even the index choosing should care about the number of ranges which could affect the seek operation in storage.

## Linked PRs
- Fix PR #63488: planner: consider seek operation cost in cost model for Index and Table Range Scans
  URL: https://github.com/pingcap/tidb/pull/63488
  State: closed
  Merged At: not merged
  Changed Files Count: 2
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/plan_cost_ver2.go
  - pkg/planner/core/plan_cost_ver2_test.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: consider seek operation cost in cost model for Index and Table Range Scans What changed and how does it work? Please see #63487 for more information.
- Fix PR #63568: planner: consider magnified seeking cost in IndexJoin
  URL: https://github.com/pingcap/tidb/pull/63568
  State: closed
  Merged At: 2025-09-23T03:45:08Z
  Changed Files Count: 1
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/plan_cost_ver2.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: consider magnified seeking cost in IndexJoin What changed and how does it work? Our current cost model doesn't consider the cost of seeking operation, which is usually cased by IN predicate like . In most cases its cost could be negligible, but if its under , its cost could be magnified by the  significantly (depending on the number of build rows), please see an simplified and concrete case here:
- Fix PR #64775: planner: consider magnified seeking cost in IndexJoin (#63568)
  URL: https://github.com/pingcap/tidb/pull/64775
  State: closed
  Merged At: 2025-12-15T02:59:33Z
  Changed Files Count: 1
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/plan_cost_ver2.go
  PR Summary: This is an automated cherry-pick of #63568 What problem does this PR solve? Problem Summary: planner: consider magnified seeking cost in IndexJoin What changed and how does it work? Our current cost model doesn't consider the cost of seeking operation, which is usually cased by IN predicate like .
- Related PR #65465: planner: consider seek cost in range construction
  URL: https://github.com/pingcap/tidb/pull/65465
  State: open
  Merged At: not merged
  Changed Files Count: 4
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/cost/factors_thresholds.go
  - pkg/planner/core/integration_test.go
  - pkg/planner/core/stats.go
  - tests/integrationtest/r/planner/core/grouped_ranges_order_by.result
  PR Summary: What problem does this PR solve? Problem Summary: The current optimizer cost model only takes seek cost into account for index joins. See #62499 for the fix for index join. However, the optimizer still selects the incorrect index on index range scan or table range scan operations. What changed and how does it work? It is not enough to simply account for the cost of seeks in the cost planning phase. It is sometimes better to only use a subset of the columns from the index and perform the selection afterwards (e.g. given an index abc, scan all entries under a = 1 and then perform a selection on b in (...) rather than doing a scan on every combination of (a = 1, b in (...)). To address this, when constructing the ranges for an index, we evaluate every possible set of ranges after the equality
- Related PR #66386: planner: consider seek cost in skyline pruning
  URL: https://github.com/pingcap/tidb/pull/66386
  State: open
  Merged At: not merged
  Changed Files Count: 6
  Main Modules: pkg/planner/core, pkg/planner, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/cost/factors_thresholds.go
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/integration_test.go
  - pkg/planner/core/stats.go
  - pkg/planner/util/fixcontrol/get.go
  - tests/integrationtest/r/planner/core/grouped_ranges_order_by.result
  PR Summary: What problem does this PR solve? Problem Summary: The current optimizer cost model only takes seek cost into account for index joins. See  for the fix for index join. However, the optimizer still selects the incorrect index on index range scan or table range scan operations. added support for IN-List match pruning to partially address this issue by allowing construction of ranges based on a prefix of an index. What changed and how does it work? This PR modifies the skyline pruning calculation to take into account seek cost when pruning indexes. This effectively allows comparison of seek costs between 2 paths to heuristically choose the better one prior to cost calculation.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
