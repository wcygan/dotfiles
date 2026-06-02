# Issue #62438: the same count tableRowIDScan may generate different cost evaluation

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/62438
- Status: closed
- Type: type/bug
- Created At: 2025-07-16T03:55:36Z
- Closed At: 2025-08-01T09:49:55Z
- Labels: affects-6.5, affects-7.1, affects-7.5, affects-8.1, affects-8.5, component/statistics, epic/cardinality-estimation, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- And you could tell from those explain above, for same count in the tableScan, but the cost formula will compute into a different row size like:  and  which is confusing

## Linked PRs
- Related PR #62537: planner: keep hist unchanged when deriving limit stats 
  URL: https://github.com/pingcap/tidb/pull/62537
  State: closed
  Merged At: 2025-08-01T09:49:54Z
  Changed Files Count: 19
  Main Modules: pkg/planner/core, tests/integrationtest, pkg/planner
  Sample Changed Files:
  - pkg/planner/core/casetest/cbotest/BUILD.bazel
  - pkg/planner/core/casetest/cbotest/cbo_test.go
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_in.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_xut.json
  - pkg/planner/core/casetest/cbotest/testdata/issue62438.json
  - pkg/planner/core/casetest/hint/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/hint/testdata/integration_suite_xut.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_xut.json
  - pkg/planner/core/casetest/vectorsearch/vector_index_test.go
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/integration_test.go
  - pkg/planner/core/plan_cost_ver2_test.go
  - pkg/planner/util/misc.go
  - tests/integrationtest/r/planner/core/casetest/integration.result
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/r/planner/core/plan_cache.result
  - tests/integrationtest/r/planner/core/plan_cost_ver2.result
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #62773: planner: keep hist unchanged when deriving limit stats  (#62537)
  URL: https://github.com/pingcap/tidb/pull/62773
  State: open
  Merged At: not merged
  Changed Files Count: 19
  Main Modules: pkg/planner/core, tests/integrationtest, pkg/planner
  Sample Changed Files:
  - pkg/planner/core/casetest/cbotest/BUILD.bazel
  - pkg/planner/core/casetest/cbotest/cbo_test.go
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_in.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_xut.json
  - pkg/planner/core/casetest/cbotest/testdata/issue62438.json
  - pkg/planner/core/casetest/hint/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/hint/testdata/integration_suite_xut.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_xut.json
  - pkg/planner/core/casetest/vectorsearch/vector_index_test.go
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/integration_test.go
  - pkg/planner/core/plan_cost_ver2_test.go
  - pkg/planner/util/misc.go
  - tests/integrationtest/r/planner/core/casetest/integration.result
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/r/planner/core/plan_cache.result
  - tests/integrationtest/r/planner/core/plan_cost_ver2.result
  PR Summary: This is an automated cherry-pick of #62537 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #62774: planner: keep hist unchanged when deriving limit stats  (#62537)
  URL: https://github.com/pingcap/tidb/pull/62774
  State: open
  Merged At: not merged
  Changed Files Count: 19
  Main Modules: pkg/planner/core, tests/integrationtest, pkg/planner
  Sample Changed Files:
  - pkg/planner/core/casetest/cbotest/BUILD.bazel
  - pkg/planner/core/casetest/cbotest/cbo_test.go
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_in.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_xut.json
  - pkg/planner/core/casetest/cbotest/testdata/issue62438.json
  - pkg/planner/core/casetest/hint/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/hint/testdata/integration_suite_xut.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_xut.json
  - pkg/planner/core/casetest/vectorsearch/vector_index_test.go
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/integration_test.go
  - pkg/planner/core/plan_cost_ver2_test.go
  - pkg/planner/util/misc.go
  - tests/integrationtest/r/planner/core/casetest/integration.result
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/r/planner/core/plan_cache.result
  - tests/integrationtest/r/planner/core/plan_cost_ver2.result
  PR Summary: This is an automated cherry-pick of #62537 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #63562: planner: keep hist unchanged when deriving limit stats  (#62537)
  URL: https://github.com/pingcap/tidb/pull/63562
  State: closed
  Merged At: 2025-09-20T23:11:01Z
  Changed Files Count: 15
  Main Modules: pkg/planner/core, tests/integrationtest, pkg/planner
  Sample Changed Files:
  - pkg/planner/core/casetest/cbotest/BUILD.bazel
  - pkg/planner/core/casetest/cbotest/cbo_test.go
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_in.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/issue62438.json
  - pkg/planner/core/casetest/dag/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/vectorsearch/vector_index_test.go
  - pkg/planner/core/plan_cost_ver2_test.go
  - pkg/planner/util/misc.go
  - tests/integrationtest/r/planner/core/casetest/integration.result
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/r/planner/core/plan_cache.result
  - tests/integrationtest/r/planner/core/plan_cost_ver2.result
  PR Summary: This is an automated cherry-pick of #62537 What problem does this PR solve? Problem Summary: What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
