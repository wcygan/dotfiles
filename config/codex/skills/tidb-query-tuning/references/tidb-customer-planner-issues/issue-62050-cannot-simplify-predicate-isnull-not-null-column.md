# Issue #62050: cannot simplify predicate ```isnull(not null column)```

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/62050
- Status: closed
- Type: type/bug
- Created At: 2025-06-27T09:05:11Z
- Closed At: 2025-07-01T15:58:28Z
- Labels: affects-7.5, affects-8.1, affects-8.5, affects-9.0, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #62046: planner: constant folding to isnull(not null column) | tidb-test=pr/2544
  URL: https://github.com/pingcap/tidb/pull/62046
  State: closed
  Merged At: 2025-07-01T15:58:27Z
  Changed Files Count: 9
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/rule/BUILD.bazel
  - pkg/planner/core/casetest/rule/main_test.go
  - pkg/planner/core/casetest/rule/rule_predicate_simplification_test.go
  - pkg/planner/core/casetest/rule/testdata/predicate_simplification_in.json
  - pkg/planner/core/casetest/rule/testdata/predicate_simplification_out.json
  - pkg/planner/core/casetest/rule/testdata/predicate_simplification_xut.json
  - pkg/planner/core/constraint/BUILD.bazel
  - pkg/planner/core/constraint/exprs.go
  - pkg/planner/core/operator/logicalop/logical_join.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? When we process the outer join, we remove the not-null flag. However, during predicate pushdown, this causes the flag to differ from the original one, and as a result, predicate simplification cannot be performed when handling the data source.
- Fix PR #62160: planner: constant folding to isnull(not null column) | tidb-test=pr/2560
  URL: https://github.com/pingcap/tidb/pull/62160
  State: closed
  Merged At: 2025-07-16T01:17:18Z
  Changed Files Count: 6
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/BUILD.bazel
  - pkg/planner/core/casetest/rule/BUILD.bazel
  - pkg/planner/core/casetest/rule/rule_predicate_simplification_test.go
  - pkg/planner/core/constraint/BUILD.bazel
  - pkg/planner/core/constraint/exprs.go
  - pkg/planner/core/rule_predicate_push_down.go
  PR Summary: This is an automated cherry-pick of #62046 What problem does this PR solve? Problem Summary: What changed and how does it work? When we process the outer join, we remove the not-null flag. However, during predicate pushdown, this causes the flag to differ from the original one, and as a result, predicate simplification cannot be performed when handling the data source.
- Fix PR #62161: planner: constant folding to isnull(not null column) | tidb-test=pr/2569
  URL: https://github.com/pingcap/tidb/pull/62161
  State: closed
  Merged At: 2025-07-31T11:58:52Z
  Changed Files Count: 9
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/BUILD.bazel
  - pkg/planner/core/casetest/rule/BUILD.bazel
  - pkg/planner/core/casetest/rule/main_test.go
  - pkg/planner/core/casetest/rule/rule_predicate_simplification_test.go
  - pkg/planner/core/casetest/rule/testdata/predicate_simplification_in.json
  - pkg/planner/core/casetest/rule/testdata/predicate_simplification_out.json
  - pkg/planner/core/constraint/BUILD.bazel
  - pkg/planner/core/constraint/exprs.go
  - pkg/planner/core/rule_predicate_push_down.go
  PR Summary: This is an automated cherry-pick of #62046 What problem does this PR solve? Problem Summary: What changed and how does it work? When we process the outer join, we remove the not-null flag. However, during predicate pushdown, this causes the flag to differ from the original one, and as a result, predicate simplification cannot be performed when handling the data source.
- Fix PR #62163: planner: constant folding to isnull(not null column) | tidb-test=pr/2559
  URL: https://github.com/pingcap/tidb/pull/62163
  State: closed
  Merged At: 2025-07-12T10:17:06Z
  Changed Files Count: 8
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/rule/BUILD.bazel
  - pkg/planner/core/casetest/rule/main_test.go
  - pkg/planner/core/casetest/rule/rule_predicate_simplification_test.go
  - pkg/planner/core/casetest/rule/testdata/predicate_simplification_in.json
  - pkg/planner/core/casetest/rule/testdata/predicate_simplification_out.json
  - pkg/planner/core/constraint/BUILD.bazel
  - pkg/planner/core/constraint/exprs.go
  - pkg/planner/core/operator/logicalop/logical_join.go
  PR Summary: This is an automated cherry-pick of #62046 What problem does this PR solve? Problem Summary: What changed and how does it work? When we process the outer join, we remove the not-null flag. However, during predicate pushdown, this causes the flag to differ from the original one, and as a result, predicate simplification cannot be performed when handling the data source.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
