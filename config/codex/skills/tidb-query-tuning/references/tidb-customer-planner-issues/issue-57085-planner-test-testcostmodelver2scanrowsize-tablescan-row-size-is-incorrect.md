# Issue #57085: Planner: Test TestCostModelVer2ScanRowSize tablescan row size is incorrect

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/57085
- Status: closed
- Type: type/bug
- Created At: 2024-11-03T20:51:07Z
- Closed At: 2024-11-06T04:42:27Z
- Labels: affects-8.1, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- (scan(1000*logrowsize(80)*tikv_scan_factor(40.7) <--- 1000

## Linked PRs
- Fix PR #57086: planner: fix cost adjustment for high risk tablescan
  URL: https://github.com/pingcap/tidb/pull/57086
  State: closed
  Merged At: 2024-11-06T04:42:25Z
  Changed Files Count: 13
  Main Modules: tests/integrationtest, pkg/planner/core, pkg/planner
  Sample Changed Files:
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/core/casetest/binaryplan/testdata/binary_plan_suite_out.json
  - pkg/planner/core/casetest/dag/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/plan_cost_ver2.go
  - pkg/planner/core/plan_cost_ver2_test.go
  - tests/integrationtest/r/executor/chunk_reuse.result
  - tests/integrationtest/r/executor/explain.result
  - tests/integrationtest/r/planner/core/casetest/integration.result
  - tests/integrationtest/r/planner/core/cbo.result
  - tests/integrationtest/r/planner/core/integration.result
  - tests/integrationtest/r/planner/core/plan_cache.result
  - tests/integrationtest/r/planner/core/plan_cost_ver2.result
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? Code to provide a minimum cost to table scan - should use "max" rather than "min" to ensure that the minimum is actually applied. Current code will produce a lower cost for tablescans greater than 1000 rows that fit the other criteria for requiring a minimum cost to table scans.
- Fix PR #57190: planner: fix cost adjustment for high risk tablescan (#57086)
  URL: https://github.com/pingcap/tidb/pull/57190
  State: closed
  Merged At: 2024-11-07T03:37:55Z
  Changed Files Count: 13
  Main Modules: tests/integrationtest, pkg/planner/core, pkg/planner
  Sample Changed Files:
  - pkg/planner/cardinality/selectivity_test.go
  - pkg/planner/core/casetest/binaryplan/testdata/binary_plan_suite_out.json
  - pkg/planner/core/casetest/dag/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/plan_cost_ver2.go
  - pkg/planner/core/plan_cost_ver2_test.go
  - tests/integrationtest/r/executor/chunk_reuse.result
  - tests/integrationtest/r/executor/explain.result
  - tests/integrationtest/r/planner/core/casetest/integration.result
  - tests/integrationtest/r/planner/core/cbo.result
  - tests/integrationtest/r/planner/core/integration.result
  - tests/integrationtest/r/planner/core/plan_cache.result
  - tests/integrationtest/r/planner/core/plan_cost_ver2.result
  PR Summary: This is an automated cherry-pick of #57086 What problem does this PR solve? Problem Summary: What changed and how does it work? Code to provide a minimum cost to table scan - should use "max" rather than "min" to ensure that the minimum is actually applied. Current code will produce a lower cost for tablescans greater than 1000 rows that fit the other criteria for requiring a minimum cost to table scans.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
