# Issue #53236: Failed to execute SQL, but succeed in mysql:v8.0

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/53236
- Status: closed
- Type: type/bug
- Created At: 2024-05-13T13:21:01Z
- Closed At: 2024-05-14T14:17:44Z
- Labels: affects-5.4, affects-6.1, affects-6.5, affects-7.1, affects-7.5, affects-8.1, compatibility-mysql80, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #53268: planner: UPDATE's select plan's output col IDs should be stable
  URL: https://github.com/pingcap/tidb/pull/53268
  State: closed
  Merged At: 2024-05-14T14:17:43Z
  Changed Files Count: 12
  Main Modules: tests/integrationtest, pkg/expression, pkg/planner/core, pkg/session, build/BUILD.bazel
  Sample Changed Files:
  - build/BUILD.bazel
  - pkg/expression/BUILD.bazel
  - pkg/expression/util.go
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/rule_eliminate_projection.go
  - pkg/sessionctx/stmtctx/BUILD.bazel
  - pkg/sessionctx/stmtctx/stmtctx.go
  - tests/integrationtest/r/planner/core/casetest/integration.result
  - tests/integrationtest/r/planner/core/cbo.result
  - tests/integrationtest/r/planner/core/issuetest/planner_issue.result
  - tests/integrationtest/r/planner/core/rule_constant_propagation.result
  - tests/integrationtest/t/planner/core/issuetest/planner_issue.test
  PR Summary: What problem does this PR solve? Problem Summary: The output UniqueIDs in the UPDATE's SELECT plan should remain unchanged after the optimization. What changed and how does it work?
- Fix PR #53273: planner: UPDATE's select plan's output col IDs should be stable (#53268)
  URL: https://github.com/pingcap/tidb/pull/53273
  State: closed
  Merged At: 2024-05-15T02:08:42Z
  Changed Files Count: 11
  Main Modules: tests/integrationtest, pkg/expression, pkg/planner/core, pkg/session
  Sample Changed Files:
  - pkg/expression/BUILD.bazel
  - pkg/expression/util.go
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/rule_eliminate_projection.go
  - pkg/sessionctx/stmtctx/BUILD.bazel
  - pkg/sessionctx/stmtctx/stmtctx.go
  - tests/integrationtest/r/planner/core/casetest/integration.result
  - tests/integrationtest/r/planner/core/cbo.result
  - tests/integrationtest/r/planner/core/issuetest/planner_issue.result
  - tests/integrationtest/r/planner/core/rule_constant_propagation.result
  - tests/integrationtest/t/planner/core/issuetest/planner_issue.test
  PR Summary: This is an automated cherry-pick of #53268 What problem does this PR solve? Problem Summary: The output UniqueIDs in the UPDATE's SELECT plan should remain unchanged after the optimization. What changed and how does it work?
- Fix PR #53274: planner: UPDATE's select plan's output col IDs should be stable (#53268)
  URL: https://github.com/pingcap/tidb/pull/53274
  State: closed
  Merged At: 2024-05-29T02:23:50Z
  Changed Files Count: 26
  Main Modules: pkg/planner/core, tests/integrationtest, pkg/util, pkg/expression, pkg/planner, pkg/session
  Sample Changed Files:
  - build/BUILD.bazel
  - pkg/expression/BUILD.bazel
  - pkg/expression/grouping_sets.go
  - pkg/expression/util.go
  - pkg/planner/core/BUILD.bazel
  - pkg/planner/core/collect_column_stats_usage.go
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/logical_plans.go
  - pkg/planner/core/plan_stats.go
  - pkg/planner/core/recheck_cte.go
  - pkg/planner/core/rule_aggregation_skew_rewrite.go
  - pkg/planner/core/rule_eliminate_projection.go
  - pkg/planner/funcdep/BUILD.bazel
  - pkg/planner/funcdep/fd_graph.go
  - pkg/planner/funcdep/fd_graph_test.go
  - pkg/sessionctx/stmtctx/BUILD.bazel
  - pkg/sessionctx/stmtctx/stmtctx.go
  - pkg/util/intset/BUILD.bazel
  - pkg/util/intset/fast_int_set.go
  - pkg/util/intset/fast_int_set_bench_test.go
  PR Summary: This is an automated cherry-pick of #53268 What problem does this PR solve? Problem Summary: The output UniqueIDs in the UPDATE's SELECT plan should remain unchanged after the optimization. What changed and how does it work?
- Fix PR #53275: planner: UPDATE's select plan's output col IDs should be stable (#53268)
  URL: https://github.com/pingcap/tidb/pull/53275
  State: closed
  Merged At: 2024-11-11T13:37:47Z
  Changed Files Count: 12
  Main Modules: planner/core, util/intset, sessionctx/stmtctx, expression/BUILD.bazel, expression/util.go
  Sample Changed Files:
  - expression/BUILD.bazel
  - expression/util.go
  - planner/core/issuetest/BUILD.bazel
  - planner/core/issuetest/planner_issue_test.go
  - planner/core/logical_plan_builder.go
  - planner/core/rule_eliminate_projection.go
  - sessionctx/stmtctx/BUILD.bazel
  - sessionctx/stmtctx/stmtctx.go
  - util/intset/BUILD.bazel
  - util/intset/fast_int_set.go
  - util/intset/fast_int_set_bench_test.go
  - util/intset/fast_int_set_test.go
  PR Summary: This is an automated cherry-pick of #53268 What problem does this PR solve? Problem Summary: The output UniqueIDs in the UPDATE's SELECT plan should remain unchanged after the optimization. What changed and how does it work?
- Fix PR #53276: planner: UPDATE's select plan's output col IDs should be stable (#53268)
  URL: https://github.com/pingcap/tidb/pull/53276
  State: closed
  Merged At: 2024-06-10T02:10:34Z
  Changed Files Count: 9
  Main Modules: planner/core, cmd/explaintest, sessionctx/stmtctx, expression/BUILD.bazel, expression/util.go
  Sample Changed Files:
  - cmd/explaintest/r/planner_issue.result
  - cmd/explaintest/t/planner_issue.test
  - expression/BUILD.bazel
  - expression/util.go
  - planner/core/issuetest/planner_issue_test.go
  - planner/core/logical_plan_builder.go
  - planner/core/rule_eliminate_projection.go
  - sessionctx/stmtctx/BUILD.bazel
  - sessionctx/stmtctx/stmtctx.go
  PR Summary: This is an automated cherry-pick of #53268 What problem does this PR solve? Problem Summary: The output UniqueIDs in the UPDATE's SELECT plan should remain unchanged after the optimization. What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
