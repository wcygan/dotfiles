# Issue #62551: rollup will output more rows than expected

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/62551
- Status: closed
- Type: type/bug
- Created At: 2025-07-22T08:18:03Z
- Closed At: 2025-07-23T14:42:15Z
- Labels: affects-8.1, affects-8.5, impact/wrong-result, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Related PR #62558: planner: fix expand operator shouldn't keep child keys && fix grouping function forget to encode their func meta
  URL: https://github.com/pingcap/tidb/pull/62558
  State: closed
  Merged At: 2025-07-23T14:42:14Z
  Changed Files Count: 10
  Main Modules: pkg/planner/core, pkg/expression
  Sample Changed Files:
  - pkg/expression/builtin_grouping.go
  - pkg/expression/scalar_function.go
  - pkg/planner/core/explain.go
  - pkg/planner/core/operator/logicalop/logical_expand.go
  - pkg/planner/core/operator/logicalop/logicalop_test/BUILD.bazel
  - pkg/planner/core/operator/logicalop/logicalop_test/logical_operator_test.go
  - pkg/planner/core/operator/logicalop/logicalop_test/main_test.go
  - pkg/planner/core/operator/logicalop/logicalop_test/testdata/cascades_suite_in.json
  - pkg/planner/core/operator/logicalop/logicalop_test/testdata/cascades_suite_out.json
  - pkg/planner/core/operator/logicalop/logicalop_test/testdata/cascades_suite_xut.json
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? * previously, tidb use buildKeyInfo to derive unique key and pk for each logical operator. While for logical expand, if we use baseLogicalPlan's buildKeyInfo logic, it will derive and keep child unique key info. Since expand op will duplicate rows, we just keep it sample as setting it nil. * the second problem is that: expression hashcode will simply encode func name and return type for normal scalar function, while for grouping function, its function meta should also be taken into consideration. Otherwise, two different grouping function will be seen as a same one in predicateSimplication logic.
- Related PR #62588: planner: fix expand operator shouldn't keep child keys && fix grouping function forget to encode their func meta (#62558)
  URL: https://github.com/pingcap/tidb/pull/62588
  State: open
  Merged At: not merged
  Changed Files Count: 18
  Main Modules: pkg/planner/core, pkg/expression
  Sample Changed Files:
  - pkg/expression/builtin_grouping.go
  - pkg/expression/scalar_function.go
  - pkg/planner/core/explain.go
  - pkg/planner/core/operator/logicalop/logical_expand.go
  - pkg/planner/core/operator/logicalop/logicalop_test/BUILD.bazel
  - pkg/planner/core/operator/logicalop/logicalop_test/logical_operator_test.go
  - pkg/planner/core/operator/logicalop/logicalop_test/main_test.go
  - pkg/planner/core/testdata/cascades_suite_in.json
  - pkg/planner/core/testdata/cascades_suite_out.json
  - pkg/planner/core/testdata/cascades_suite_xut.json
  - pkg/planner/core/testdata/index_merge_suite_in.json
  - pkg/planner/core/testdata/index_merge_suite_out.json
  - pkg/planner/core/testdata/plan_cache_suite_in.json
  - pkg/planner/core/testdata/plan_cache_suite_out.json
  - pkg/planner/core/testdata/plan_suite_unexported_in.json
  - pkg/planner/core/testdata/plan_suite_unexported_out.json
  - pkg/planner/core/testdata/runtime_filter_generator_suite_in.json
  - pkg/planner/core/testdata/runtime_filter_generator_suite_out.json
  PR Summary: This is an automated cherry-pick of #62558 What problem does this PR solve? Problem Summary: What changed and how does it work? * previously, tidb use buildKeyInfo to derive unique key and pk for each logical operator. While for logical expand, if we use baseLogicalPlan's buildKeyInfo logic, it will derive and keep child unique key info. Since expand op will duplicate rows, we just keep it sample as setting it nil.
- Related PR #62589: planner: fix expand operator shouldn't keep child keys && fix grouping function forget to encode their func meta (#62558)
  URL: https://github.com/pingcap/tidb/pull/62589
  State: closed
  Merged At: 2025-07-29T07:11:16Z
  Changed Files Count: 11
  Main Modules: pkg/planner/core, pkg/expression
  Sample Changed Files:
  - pkg/expression/builtin_grouping.go
  - pkg/expression/expression.go
  - pkg/expression/scalar_function.go
  - pkg/expression/schema.go
  - pkg/planner/core/explain.go
  - pkg/planner/core/operator/logicalop/logical_expand.go
  - pkg/planner/core/operator/logicalop/logicalop_test/BUILD.bazel
  - pkg/planner/core/operator/logicalop/logicalop_test/logical_operator_test.go
  - pkg/planner/core/operator/logicalop/logicalop_test/main_test.go
  - pkg/planner/core/operator/logicalop/logicalop_test/testdata/cascades_suite_in.json
  - pkg/planner/core/operator/logicalop/logicalop_test/testdata/cascades_suite_out.json
  PR Summary: This is an automated cherry-pick of #62558 What problem does this PR solve? Problem Summary: What changed and how does it work? * previously, tidb use buildKeyInfo to derive unique key and pk for each logical operator. While for logical expand, if we use baseLogicalPlan's buildKeyInfo logic, it will derive and keep child unique key info. Since expand op will duplicate rows, we just keep it sample as setting it nil.
- Related PR #62595: planner: fix expand operator shouldn't keep child keys && fix grouping function forget to encode their func meta (#62558)
  URL: https://github.com/pingcap/tidb/pull/62595
  State: open
  Merged At: not merged
  Changed Files Count: 16
  Main Modules: pkg/planner/core, pkg/expression
  Sample Changed Files:
  - pkg/expression/builtin_grouping.go
  - pkg/expression/scalar_function.go
  - pkg/planner/core/explain.go
  - pkg/planner/core/operator/logicalop/logical_expand.go
  - pkg/planner/core/operator/logicalop/logicalop_test/BUILD.bazel
  - pkg/planner/core/operator/logicalop/logicalop_test/logical_operator_test.go
  - pkg/planner/core/operator/logicalop/logicalop_test/main_test.go
  - pkg/planner/core/testdata/cascades_suite_in.json
  - pkg/planner/core/testdata/cascades_suite_out.json
  - pkg/planner/core/testdata/cascades_suite_xut.json
  - pkg/planner/core/testdata/index_merge_suite_in.json
  - pkg/planner/core/testdata/index_merge_suite_out.json
  - pkg/planner/core/testdata/plan_suite_unexported_in.json
  - pkg/planner/core/testdata/plan_suite_unexported_out.json
  - pkg/planner/core/testdata/runtime_filter_generator_suite_in.json
  - pkg/planner/core/testdata/runtime_filter_generator_suite_out.json
  PR Summary: This is an automated cherry-pick of #62558 What problem does this PR solve? Problem Summary: What changed and how does it work? * previously, tidb use buildKeyInfo to derive unique key and pk for each logical operator. While for logical expand, if we use baseLogicalPlan's buildKeyInfo logic, it will derive and keep child unique key info. Since expand op will duplicate rows, we just keep it sample as setting it nil.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
