# Issue #51116: planner: the optimizer can't produce an optimal plan for queries with sub-queries in select list since it always decorrelate sub-queries

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/51116
- Status: closed
- Type: type/unknown
- Created At: 2024-02-18T08:46:57Z
- Closed At: 2025-09-03T18:34:01Z
- Labels: affects-8.5, report/customer, severity/moderate, sig/planner

## Customer-Facing Phenomenon
- A better plan could be (how Oracle executes it):

## Linked PRs
- Fix PR #63204: planner: Add variable for no_decorrelate in select list
  URL: https://github.com/pingcap/tidb/pull/63204
  State: closed
  Merged At: 2025-09-03T18:34:00Z
  Changed Files Count: 9
  Main Modules: pkg/session, pkg/planner/core, pkg/bindinfo
  Sample Changed Files:
  - pkg/bindinfo/binding_plan_generation.go
  - pkg/bindinfo/binding_plan_generation_test.go
  - pkg/planner/core/expression_rewriter.go
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/planbuilder.go
  - pkg/sessionctx/vardef/tidb_vars.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/setvar_affect.go
  - pkg/sessionctx/variable/sysvar.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? Customer requirement to allow decorrelation of subqueries in the select list. Added a variable to control this behavior.
- Fix PR #63273: planner: no_decorrelate triggered by cost factors
  URL: https://github.com/pingcap/tidb/pull/63273
  State: closed
  Merged At: not merged
  Changed Files Count: 1
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/expression_rewriter.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? Prototype PR for test scenario. Not planned for integration into master branch. The planned PR for master branch is:
- Fix PR #63287: planner: allow correlated exists subqueries to early-out | tidb-test=pr/2593
  URL: https://github.com/pingcap/tidb/pull/63287
  State: closed
  Merged At: 2025-09-10T20:50:27Z
  Changed Files Count: 4
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/expression_rewriter.go
  - pkg/planner/core/logical_plans_test.go
  - tests/integrationtest/r/cte.result
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? Enhancement to add LIMIT 1 to EXISTS correlated subqueries (where NO_DECORRELATE hint exists) if no existing LIMIT applies within the subquery.
- Fix PR #63541: planner: Add variable for no_decorrelate in select list (#63204)
  URL: https://github.com/pingcap/tidb/pull/63541
  State: closed
  Merged At: 2025-09-22T03:46:24Z
  Changed Files Count: 7
  Main Modules: pkg/session, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/expression_rewriter.go
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/planbuilder.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/setvar_affect.go
  - pkg/sessionctx/variable/sysvar.go
  - pkg/sessionctx/variable/tidb_vars.go
  PR Summary: This is an automated cherry-pick of #63204 What problem does this PR solve? Problem Summary: What changed and how does it work? Customer requirement to allow decorrelation of subqueries in the select list. Added a variable to control this behavior.
- Fix PR #63634: planner: allow correlated exists subqueries to early-out (#63287) | tidb-test=pr/2611
  URL: https://github.com/pingcap/tidb/pull/63634
  State: closed
  Merged At: 2025-09-23T01:12:22Z
  Changed Files Count: 3
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/expression_rewriter.go
  - tests/integrationtest/r/cte.result
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  PR Summary: This is an automated cherry-pick of #63287 What problem does this PR solve? Problem Summary: What changed and how does it work? Enhancement to add LIMIT 1 to EXISTS correlated subqueries (where NO_DECORRELATE hint exists) if no existing LIMIT applies within the subquery.
- Related PR #67693: [Do Not Merge/ POC only] planner: support rewrite join to apply rule
  URL: https://github.com/pingcap/tidb/pull/67693
  State: closed
  Merged At: not merged
  Changed Files Count: 12
  Main Modules: pkg/parser, pkg/planner/core, tests/integrationtest, pkg/executor, pkg/util
  Sample Changed Files:
  - pkg/executor/adapter.go
  - pkg/parser/hintparser.go
  - pkg/parser/hintparser.y
  - pkg/parser/hintparser_test.go
  - pkg/parser/misc.go
  - pkg/planner/core/optimizer.go
  - pkg/planner/core/planbuilder.go
  - pkg/planner/core/rule/logical_rules.go
  - pkg/planner/core/rule_join_to_apply.go
  - pkg/util/hint/hint.go
  - tests/integrationtest/r/planner/core/casetest/hint/join_to_apply.result
  - tests/integrationtest/t/planner/core/casetest/hint/join_to_apply.test
  PR Summary: What problem does this PR solve? Problem Summary: support rewrite join to apply rule What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
