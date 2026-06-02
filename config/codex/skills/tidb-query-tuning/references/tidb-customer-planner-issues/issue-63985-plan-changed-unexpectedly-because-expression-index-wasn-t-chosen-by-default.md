# Issue #63985: plan changed unexpectedly because expression index wasn't chosen by default

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/63985
- Status: closed
- Type: type/bug
- Created At: 2025-10-16T01:56:43Z
- Closed At: 2025-11-05T17:02:54Z
- Labels: affects-8.5, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- you can reproduce this problem using dataset as And I think this is introduced by recent commit between  be3ba74ef819842dae045121eec5f3f6f0aaf1a7 and 3e7f31765ebe78bea7e4fdbd762180e20ade300b

## Linked PRs
- Related PR #63961: planner: fix uninitialized stats for expression index
  URL: https://github.com/pingcap/tidb/pull/63961
  State: closed
  Merged At: 2025-10-16T07:16:59Z
  Changed Files Count: 3
  Main Modules: pkg/planner
  Sample Changed Files:
  - pkg/planner/cardinality/BUILD.bazel
  - pkg/planner/cardinality/selectivity.go
  - pkg/planner/cardinality/selectivity_test.go
  PR Summary: What problem does this PR solve? Problem Summary: For the following case, the explain analyze output shows  for that expression index(), which is confusing. For expression index , there will be both original column stats and index stats when [calculating selectivity](). Check the following debug output, you can see the column stats is  and the index stats is ready. So for expression index, should use index stats and its column stats.
- Fix PR #64151: planner: fix prefer task logic when enumerate physical limit/topn | tidb-test=pr/2622
  URL: https://github.com/pingcap/tidb/pull/64151
  State: closed
  Merged At: 2025-11-05T17:02:53Z
  Changed Files Count: 10
  Main Modules: pkg/planner/core, pkg/planner
  Sample Changed Files:
  - pkg/planner/cascades/memo/group_expr.go
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_xut.json
  - pkg/planner/core/casetest/dag/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/dag/testdata/plan_suite_xut.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_xut.json
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/operator/physicalop/physical_topn.go
  PR Summary: What problem does this PR solve? Problem Summary: check  for detail. What changed and how does it work? there will be two kinds of tasks: 1. hintTask: this task was chosen because of hint
- Fix PR #64307: planner: fix prefer task logic when enumerate physical limit/topn
  URL: https://github.com/pingcap/tidb/pull/64307
  State: closed
  Merged At: 2025-11-06T06:41:44Z
  Changed Files Count: 10
  Main Modules: pkg/planner/core, pkg/planner
  Sample Changed Files:
  - pkg/planner/cascades/memo/group_expr.go
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_xut.json
  - pkg/planner/core/casetest/dag/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/dag/testdata/plan_suite_xut.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_xut.json
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/operator/physicalop/physical_topn.go
  PR Summary: What problem does this PR solve? Problem Summary: this is for hotfix. cherry-pick  manually What changed and how does it work?
- Fix PR #65134: planner: fix prefer task logic when enumerate physical limit/topn | tidb-test=pr/2622 (#64151)
  URL: https://github.com/pingcap/tidb/pull/65134
  State: closed
  Merged At: not merged
  Changed Files Count: 10
  Main Modules: pkg/planner/core, pkg/planner
  Sample Changed Files:
  - pkg/planner/cascades/memo/group_expr.go
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_xut.json
  - pkg/planner/core/casetest/dag/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/dag/testdata/plan_suite_xut.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_xut.json
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/operator/physicalop/physical_topn.go
  PR Summary: This is an automated cherry-pick of #64151 What problem does this PR solve? Problem Summary: check  for detail. What changed and how does it work? there will be two kinds of tasks:

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
