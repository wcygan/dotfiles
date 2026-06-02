# Issue #59902: The estrows is wrong for inner operator of index join

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/59902
- Status: closed
- Type: type/bug
- Created At: 2025-03-05T02:49:08Z
- Closed At: 2025-03-25T13:26:12Z
- Labels: affects-8.5, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- create table t1(a int primary key, b int); create table t2(a int, b int, key idx(a)); set tidb_enable_inl_join_inner_multi_pattern=on; explain select t1.b,(select count(*) from t2 where t2.a=t1.a) as a from t1 where t1.a=1;

## Linked PRs
- Fix PR #60071: planner: fix wrong HashAgg estrows for inner operator of index join
  URL: https://github.com/pingcap/tidb/pull/60071
  State: closed
  Merged At: 2025-03-25T13:26:11Z
  Changed Files Count: 6
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/issuetest/BUILD.bazel
  - pkg/planner/core/issuetest/planner_issue_test.go
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/r/planner/core/indexjoin.result
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? in the , we forget to transfer the parents stats by the child stats.
- Fix PR #60336: planner: fix wrong HashAgg estrows for inner operator of index join (#60071)
  URL: https://github.com/pingcap/tidb/pull/60336
  State: closed
  Merged At: 2025-04-16T16:36:22Z
  Changed Files Count: 6
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/issuetest/BUILD.bazel
  - pkg/planner/core/issuetest/planner_issue_test.go
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/r/planner/core/indexjoin.result
  PR Summary: This is an automated cherry-pick of #60071 What problem does this PR solve? Problem Summary: What changed and how does it work? in the , we forget to transfer the parents stats by the child stats.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
