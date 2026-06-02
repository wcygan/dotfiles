# Issue #63602: statement with scalar subquery result wrong

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/63602
- Status: closed
- Type: type/bug
- Created At: 2025-09-18T08:21:32Z
- Closed At: 2025-09-23T07:52:17Z
- Labels: affects-8.5, contribution, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #63637: planner: refactor outer to inner join | tidb-test=pr/2612
  URL: https://github.com/pingcap/tidb/pull/63637
  State: closed
  Merged At: 2025-09-23T07:52:16Z
  Changed Files Count: 9
  Main Modules: pkg/planner/core, pkg/executor
  Sample Changed Files:
  - pkg/executor/test/indexmergereadtest/index_merge_reader_test.go
  - pkg/planner/core/casetest/parallelapply/parallel_apply_test.go
  - pkg/planner/core/casetest/rule/BUILD.bazel
  - pkg/planner/core/casetest/rule/rule_outer2inner_test.go
  - pkg/planner/core/casetest/rule/testdata/outer2inner_out.json
  - pkg/planner/core/casetest/rule/testdata/outer2inner_xut.json
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/operator/logicalop/BUILD.bazel
  - pkg/planner/core/operator/logicalop/logical_join.go
  PR Summary: What problem does this PR solve? close #61327 Problem Summary: What changed and how does it work? revert #52941 , Our  has problems and it will get wrong transfer.
- Related PR #63688: planner: refactor outer to inner join | tidb-test=pr/2614 
  URL: https://github.com/pingcap/tidb/pull/63688
  State: closed
  Merged At: 2025-09-24T16:32:19Z
  Changed Files Count: 11
  Main Modules: pkg/planner/core, tests/integrationtest, pkg/executor, pkg/session
  Sample Changed Files:
  - pkg/executor/test/indexmergereadtest/index_merge_reader_test.go
  - pkg/planner/core/casetest/parallelapply/parallel_apply_test.go
  - pkg/planner/core/casetest/rule/BUILD.bazel
  - pkg/planner/core/casetest/rule/rule_outer2inner_test.go
  - pkg/planner/core/casetest/rule/testdata/outer2inner_out.json
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/operator/logicalop/BUILD.bazel
  - pkg/planner/core/operator/logicalop/logical_join.go
  - pkg/session/main_test.go
  - tests/integrationtest/r/planner/core/rule_outer2inner.result
  - tests/integrationtest/t/planner/core/rule_outer2inner.test
  PR Summary: This is an automated cherry-pick of #63637 What problem does this PR solve? Problem Summary: What changed and how does it work? revert #52941 , Our  has problems and it will get wrong transfer.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
