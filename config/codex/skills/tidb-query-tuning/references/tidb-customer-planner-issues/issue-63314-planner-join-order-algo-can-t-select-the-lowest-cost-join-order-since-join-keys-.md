# Issue #63314: planner: join order algo can't select the lowest cost join order since join keys are eliminated by constant propagation

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/63314
- Status: closed
- Type: type/enhancement
- Created At: 2025-09-01T10:46:40Z
- Closed At: 2025-09-10T02:07:49Z
- Labels: affects-8.5, planner/join-order, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- The best join order is , but the optimizer can't select it:

## Linked PRs
- Fix PR #63375: planner: keep join keys for join optimization in constant propagation
  URL: https://github.com/pingcap/tidb/pull/63375
  State: closed
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: pkg/planner/core, pkg/expression
  Sample Changed Files:
  - pkg/expression/constant_propagation.go
  - pkg/planner/core/casetest/join/BUILD.bazel
  - pkg/planner/core/casetest/join/join_test.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: keep join keys for join optimization in constant propagation What changed and how does it work?
- Fix PR #63385: planner: refactoring, use the special function to propagate constant for Joins
  URL: https://github.com/pingcap/tidb/pull/63385
  State: closed
  Merged At: not merged
  Changed Files Count: 4
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/operator/logicalop/logical_join.go
  - pkg/planner/core/rule/rule_init.go
  - pkg/planner/core/rule/rule_predicate_simplification.go
  - pkg/planner/core/rule/util/misc.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: refactoring, use the special function to propagate constant for Joins What changed and how does it work? planner: refactoring, use the special function to propagate constant for Joins
- Fix PR #63388: planner: refactor some code related to constant propagation for join
  URL: https://github.com/pingcap/tidb/pull/63388
  State: closed
  Merged At: 2025-09-05T12:55:36Z
  Changed Files Count: 7
  Main Modules: pkg/planner/core, pkg/expression, pkg/planner
  Sample Changed Files:
  - pkg/expression/constant_propagation.go
  - pkg/expression/constant_test.go
  - pkg/planner/cascades/old/transformation_rules.go
  - pkg/planner/core/operator/logicalop/logical_join.go
  - pkg/planner/core/rule/rule_init.go
  - pkg/planner/core/rule/rule_predicate_simplification.go
  - pkg/planner/core/rule/util/misc.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: refactor some code related to constant propagation for join What changed and how does it work? just refactor, no logical change
- Fix PR #63404: planner: keep join keys for join optimization in constant propagation | tidb-test=pr/2600
  URL: https://github.com/pingcap/tidb/pull/63404
  State: closed
  Merged At: 2025-09-10T02:07:48Z
  Changed Files Count: 12
  Main Modules: pkg/planner/core, pkg/session, pkg/expression, pkg/bindinfo, pkg/planner
  Sample Changed Files:
  - pkg/bindinfo/binding_plan_generation.go
  - pkg/expression/constant_propagation.go
  - pkg/expression/constant_test.go
  - pkg/planner/cascades/old/transformation_rules.go
  - pkg/planner/core/casetest/join/BUILD.bazel
  - pkg/planner/core/casetest/join/join_test.go
  - pkg/planner/core/operator/logicalop/logical_join.go
  - pkg/planner/core/rule/rule_predicate_simplification.go
  - pkg/sessionctx/vardef/tidb_vars.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/setvar_affect.go
  - pkg/sessionctx/variable/sysvar.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: keep join keys for join optimization in constant propagation What changed and how does it work?
- Fix PR #63470: planner: always keep join keys by default | tidb-test=pr/2602 
  URL: https://github.com/pingcap/tidb/pull/63470
  State: closed
  Merged At: 2025-09-12T05:01:52Z
  Changed Files Count: 19
  Main Modules: tests/integrationtest, pkg/planner/core, pkg/executor, pkg/session
  Sample Changed Files:
  - pkg/executor/explainfor_test.go
  - pkg/executor/prepared_test.go
  - pkg/executor/testdata/prepare_suite_out.json
  - pkg/planner/core/casetest/dag/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/dag/testdata/plan_suite_xut.json
  - pkg/planner/core/casetest/partition/testdata/partition_pruner_out.json
  - pkg/planner/core/casetest/partition/testdata/partition_pruner_xut.json
  - pkg/planner/core/issuetest/planner_issue_test.go
  - pkg/planner/core/testdata/plan_suite_unexported_out.json
  - pkg/sessionctx/vardef/tidb_vars.go
  - tests/integrationtest/r/agg_predicate_pushdown.result
  - tests/integrationtest/r/collation_misc_enabled.result
  - tests/integrationtest/r/executor/explain.result
  - tests/integrationtest/r/executor/explainfor.result
  - tests/integrationtest/r/executor/merge_join.result
  - tests/integrationtest/r/executor/point_get.result
  - tests/integrationtest/r/explain_foreign_key.result
  - tests/integrationtest/r/expression/issues.result
  - tests/integrationtest/r/planner/core/rule_constant_propagation.result
  PR Summary: What problem does this PR solve? Problem Summary: planner: always keep join keys by default What changed and how does it work? I went through all changes and all seem excepted and have the same situation. Before we can only choose  since there is no join key, while after this PR we can have more join choices like MergeJoin and IndexJoin because we can only choose them if we have join keys:
- Fix PR #64798: planner: refactor some code related to constant propagation for join (#63388)
  URL: https://github.com/pingcap/tidb/pull/64798
  State: closed
  Merged At: not merged
  Changed Files Count: 7
  Main Modules: pkg/planner/core, pkg/expression, pkg/planner
  Sample Changed Files:
  - pkg/expression/constant_propagation.go
  - pkg/expression/constant_test.go
  - pkg/planner/cascades/transformation_rules.go
  - pkg/planner/core/operator/logicalop/logical_join.go
  - pkg/planner/core/rule/rule_init.go
  - pkg/planner/core/rule/util/misc.go
  - pkg/planner/core/rule_predicate_simplification.go
  PR Summary: This is an automated cherry-pick of #63388 What problem does this PR solve? Problem Summary: planner: refactor some code related to constant propagation for join What changed and how does it work? just refactor, no logical change
- Fix PR #64799: planner: keep join keys for join optimization in constant propagation | tidb-test=pr/2600 (#63404)
  URL: https://github.com/pingcap/tidb/pull/64799
  State: open
  Merged At: not merged
  Changed Files Count: 12
  Main Modules: pkg/planner/core, pkg/session, pkg/expression, pkg/bindinfo, pkg/planner
  Sample Changed Files:
  - pkg/bindinfo/binding_plan_generation.go
  - pkg/expression/constant_propagation.go
  - pkg/expression/constant_test.go
  - pkg/planner/cascades/transformation_rules.go
  - pkg/planner/core/casetest/join/BUILD.bazel
  - pkg/planner/core/casetest/join/join_test.go
  - pkg/planner/core/operator/logicalop/logical_join.go
  - pkg/planner/core/rule/rule_predicate_simplification.go
  - pkg/sessionctx/vardef/tidb_vars.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/setvar_affect.go
  - pkg/sessionctx/variable/sysvar.go
  PR Summary: This is an automated cherry-pick of #63404 What problem does this PR solve? Problem Summary: planner: keep join keys for join optimization in constant propagation What changed and how does it work?
- Fix PR #64800: planner: always keep join keys by default | tidb-test=pr/2602  (#63470)
  URL: https://github.com/pingcap/tidb/pull/64800
  State: open
  Merged At: not merged
  Changed Files Count: 19
  Main Modules: tests/integrationtest, pkg/planner/core, pkg/executor, pkg/session
  Sample Changed Files:
  - pkg/executor/explainfor_test.go
  - pkg/executor/prepared_test.go
  - pkg/executor/testdata/prepare_suite_out.json
  - pkg/planner/core/casetest/dag/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/dag/testdata/plan_suite_xut.json
  - pkg/planner/core/casetest/partition/testdata/partition_pruner_out.json
  - pkg/planner/core/casetest/partition/testdata/partition_pruner_xut.json
  - pkg/planner/core/issuetest/planner_issue_test.go
  - pkg/planner/core/testdata/plan_suite_unexported_out.json
  - pkg/sessionctx/vardef/tidb_vars.go
  - tests/integrationtest/r/agg_predicate_pushdown.result
  - tests/integrationtest/r/collation_misc_enabled.result
  - tests/integrationtest/r/executor/explain.result
  - tests/integrationtest/r/executor/explainfor.result
  - tests/integrationtest/r/executor/merge_join.result
  - tests/integrationtest/r/executor/point_get.result
  - tests/integrationtest/r/explain_foreign_key.result
  - tests/integrationtest/r/expression/issues.result
  - tests/integrationtest/r/planner/core/rule_constant_propagation.result
  PR Summary: This is an automated cherry-pick of #63470 What problem does this PR solve? Problem Summary: planner: always keep join keys by default What changed and how does it work? I went through all changes and all seem excepted and have the same situation.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
