# Issue #54064: IndexMergeJoin get different result when using different charset

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/54064
- Status: closed
- Type: type/bug
- Created At: 2024-06-17T17:25:26Z
- Closed At: 2024-07-25T07:48:06Z
- Labels: affects-5.4, affects-6.1, affects-6.5, affects-7.1, affects-7.5, affects-8.1, affects-8.2, impact/wrong-result, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Related PR #54249: planner, executor: fix index lookup join's inner index order should should be correctly mapped to join keys
  URL: https://github.com/pingcap/tidb/pull/54249
  State: closed
  Merged At: not merged
  Changed Files Count: 5
  Main Modules: pkg/executor, pkg/planner/core
  Sample Changed Files:
  - pkg/executor/builder.go
  - pkg/executor/join/index_lookup_merge_join.go
  - pkg/executor/test/jointest/join_test.go
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/physical_plans.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #54681: planner: deprecate index lookup merge join.
  URL: https://github.com/pingcap/tidb/pull/54681
  State: closed
  Merged At: 2024-07-25T07:48:05Z
  Changed Files Count: 21
  Main Modules: tests/integrationtest, pkg/executor, pkg/planner/core, pkg/util
  Sample Changed Files:
  - pkg/executor/join/index_lookup_merge_join.go
  - pkg/executor/join/index_lookup_merge_join_test.go
  - pkg/executor/partition_table_test.go
  - pkg/executor/test/jointest/hashjoin/hash_join_test.go
  - pkg/executor/test/jointest/join_test.go
  - pkg/planner/core/casetest/physicalplantest/physical_plan_test.go
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/util/hint/hint.go
  - tests/integrationtest/r/executor/index_lookup_join.result
  - tests/integrationtest/r/executor/index_lookup_merge_join.result
  - tests/integrationtest/r/executor/jointest/hash_join.result
  - tests/integrationtest/r/executor/write.result
  - tests/integrationtest/r/expression/charset_and_collation.result
  - tests/integrationtest/r/expression/issues.result
  - tests/integrationtest/r/planner/core/casetest/hint/hint.result
  - tests/integrationtest/r/planner/core/casetest/index/index.result
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  - tests/integrationtest/r/planner/core/integration.result
  - tests/integrationtest/r/planner/core/physical_plan.result
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #54904: planner: deprecate index lookup merge join. (#54681)
  URL: https://github.com/pingcap/tidb/pull/54904
  State: closed
  Merged At: not merged
  Changed Files Count: 21
  Main Modules: tests/integrationtest, pkg/executor, pkg/planner/core, pkg/util
  Sample Changed Files:
  - pkg/executor/index_lookup_merge_join.go
  - pkg/executor/join/index_lookup_merge_join_test.go
  - pkg/executor/partition_table_test.go
  - pkg/executor/test/jointest/hashjoin/hash_join_test.go
  - pkg/executor/test/jointest/join_test.go
  - pkg/planner/core/casetest/physicalplantest/physical_plan_test.go
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/util/hint/hint.go
  - tests/integrationtest/r/executor/index_lookup_join.result
  - tests/integrationtest/r/executor/index_lookup_merge_join.result
  - tests/integrationtest/r/executor/jointest/hash_join.result
  - tests/integrationtest/r/executor/write.result
  - tests/integrationtest/r/expression/charset_and_collation.result
  - tests/integrationtest/r/expression/issues.result
  - tests/integrationtest/r/planner/core/casetest/hint/hint.result
  - tests/integrationtest/r/planner/core/casetest/index/index.result
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  - tests/integrationtest/r/planner/core/integration.result
  - tests/integrationtest/r/planner/core/physical_plan.result
  PR Summary: This is an automated cherry-pick of #54681 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #54934: planner: deprecate index lookup merge join. (#54681)
  URL: https://github.com/pingcap/tidb/pull/54934
  State: closed
  Merged At: not merged
  Changed Files Count: 21
  Main Modules: tests/integrationtest, pkg/executor, pkg/planner/core, executor/index_lookup_merge_join.go, executor/partition_table_test.go, pkg/util
  Sample Changed Files:
  - executor/index_lookup_merge_join.go
  - executor/partition_table_test.go
  - pkg/executor/join/index_lookup_merge_join_test.go
  - pkg/executor/test/jointest/hashjoin/hash_join_test.go
  - pkg/executor/test/jointest/join_test.go
  - pkg/planner/core/casetest/physicalplantest/physical_plan_test.go
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/util/hint/hint.go
  - tests/integrationtest/r/executor/index_lookup_join.result
  - tests/integrationtest/r/executor/index_lookup_merge_join.result
  - tests/integrationtest/r/executor/jointest/hash_join.result
  - tests/integrationtest/r/executor/write.result
  - tests/integrationtest/r/expression/charset_and_collation.result
  - tests/integrationtest/r/expression/issues.result
  - tests/integrationtest/r/planner/core/casetest/hint/hint.result
  - tests/integrationtest/r/planner/core/casetest/index/index.result
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  - tests/integrationtest/r/planner/core/integration.result
  - tests/integrationtest/r/planner/core/physical_plan.result
  PR Summary: This is an automated cherry-pick of #54681 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #54950: planner: deprecate index lookup merge join. (#54681)
  URL: https://github.com/pingcap/tidb/pull/54950
  State: closed
  Merged At: not merged
  Changed Files Count: 21
  Main Modules: tests/integrationtest, pkg/executor, pkg/planner/core, pkg/util
  Sample Changed Files:
  - pkg/executor/index_lookup_merge_join.go
  - pkg/executor/index_lookup_merge_join_test.go
  - pkg/executor/partition_table_test.go
  - pkg/executor/test/jointest/hashjoin/hash_join_test.go
  - pkg/executor/test/jointest/join_test.go
  - pkg/planner/core/casetest/physicalplantest/physical_plan_test.go
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/util/hint/hint.go
  - tests/integrationtest/r/executor/index_lookup_join.result
  - tests/integrationtest/r/executor/index_lookup_merge_join.result
  - tests/integrationtest/r/executor/jointest/hash_join.result
  - tests/integrationtest/r/executor/write.result
  - tests/integrationtest/r/expression/charset_and_collation.result
  - tests/integrationtest/r/expression/issues.result
  - tests/integrationtest/r/planner/core/casetest/hint/hint.result
  - tests/integrationtest/r/planner/core/casetest/index/index.result
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  - tests/integrationtest/r/planner/core/integration.result
  - tests/integrationtest/r/planner/core/physical_plan.result
  PR Summary: This is an automated cherry-pick of #54681 What problem does this PR solve? Problem Summary: What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
