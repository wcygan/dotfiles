# Issue #60076: planner: keep redundant Join Key predicates when propagating EQ predicates

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/60076
- Status: closed
- Type: type/enhancement
- Created At: 2025-03-14T02:29:55Z
- Closed At: 2025-09-10T02:07:49Z
- Labels: planner/join-order, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- See the case below, before adding , the can work well, while after adding it, the can't work and there are multiple dangerous Cartesian Joins.

## Linked PRs
- Fix PR #62996: expression: avoid removing the equal condition when to propagte constant | tidb-test=pr/2581
  URL: https://github.com/pingcap/tidb/pull/62996
  State: closed
  Merged At: not merged
  Changed Files Count: 45
  Main Modules: pkg/planner/core, pkg/expression, tests/integrationtest, pkg/executor, pkg/planner, pkg/testkit
  Sample Changed Files:
  - pkg/executor/builder.go
  - pkg/executor/explainfor_test.go
  - pkg/executor/testdata/prepare_suite_out.json
  - pkg/expression/builtin_compare_test.go
  - pkg/expression/constant_propagation.go
  - pkg/expression/constant_test.go
  - pkg/expression/scalar_function.go
  - pkg/planner/cascades/old/transformation_rules.go
  - pkg/planner/core/casetest/dag/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/dag/testdata/plan_suite_xut.json
  - pkg/planner/core/casetest/partition/testdata/partition_pruner_out.json
  - pkg/planner/core/casetest/partition/testdata/partition_pruner_xut.json
  - pkg/planner/core/casetest/rule/rule_predicate_simplification_test.go
  - pkg/planner/core/casetest/rule/testdata/predicate_simplification_in.json
  - pkg/planner/core/casetest/rule/testdata/predicate_simplification_out.json
  - pkg/planner/core/casetest/rule/testdata/predicate_simplification_xut.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_xut.json
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/find_best_task.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? When we perform constant propagation, sometimes we remove the equal condition, which is actually very dangerous. So the fix is that if it detects that the condition being processed is an equal condition, then the new expression generated from this expression should be appended to the slices, not replaced.
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
- Related PR #63385: planner: refactoring, use the special function to propagate constant for Joins
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

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
