# Issue #63075: `select 1 from dual` can't hit instance level plan cache

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/63075
- Status: closed
- Type: type/bug
- Created At: 2025-08-19T17:12:42Z
- Closed At: 2025-08-28T01:51:37Z
- Labels: affects-8.5, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #63198: planner: implement func CloneForPlanCache() for PhysicalTableDual
  URL: https://github.com/pingcap/tidb/pull/63198
  State: closed
  Merged At: 2025-08-27T15:50:55Z
  Changed Files Count: 3
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/instanceplancache/BUILD.bazel
  - pkg/planner/core/casetest/instanceplancache/others_test.go
  - pkg/planner/core/operator/physicalop/physical_table_dual.go
  PR Summary: What problem does this PR solve? Problem Summary: “select 1 from dual” can't hit instance level plan cache because CloneForPlanCache() is not implemented for PhysicalTableDual. What changed and how does it work? I implemented func CloneForPlanCache() for PhysicalTableDual.
- Fix PR #63472: planner: use generator to implement the PhysicalTableDual's CloneForPlanCache
  URL: https://github.com/pingcap/tidb/pull/63472
  State: closed
  Merged At: 2025-09-11T13:12:13Z
  Changed Files Count: 3
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/generator/plan_cache/plan_clone_generator.go
  - pkg/planner/core/operator/physicalop/physical_table_dual.go
  - pkg/planner/core/operator/physicalop/plan_clone_generated.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? use generator to implement the PhysicalTableDual's CloneForPlanCache
- Fix PR #63518: planner: implement func CloneForPlanCache() for PhysicalTableDual (#63198)
  URL: https://github.com/pingcap/tidb/pull/63518
  State: closed
  Merged At: 2025-09-17T19:45:59Z
  Changed Files Count: 4
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/instanceplancache/BUILD.bazel
  - pkg/planner/core/casetest/instanceplancache/others_test.go
  - pkg/planner/core/generator/plan_cache/plan_clone_generator.go
  - pkg/planner/core/plan_clone_generated.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #63547: planner: implement func CloneForPlanCache() for PhysicalTableDual (#63198)
  URL: https://github.com/pingcap/tidb/pull/63547
  State: closed
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/instanceplancache/BUILD.bazel
  - pkg/planner/core/casetest/instanceplancache/others_test.go
  - pkg/planner/core/operator/physicalop/physical_table_dual.go
  PR Summary: This is an automated cherry-pick of #63198 What problem does this PR solve? Problem Summary: “select 1 from dual” can't hit instance level plan cache because CloneForPlanCache() is not implemented for PhysicalTableDual. What changed and how does it work?
- Fix PR #63548: planner: use generator to implement the PhysicalTableDual's CloneForPlanCache (#63472)
  URL: https://github.com/pingcap/tidb/pull/63548
  State: closed
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/generator/plan_cache/plan_clone_generator.go
  - pkg/planner/core/operator/physicalop/physical_table_dual.go
  - pkg/planner/core/plan_clone_generated.go
  PR Summary: This is an automated cherry-pick of #63472 What problem does this PR solve? Problem Summary: What changed and how does it work? use generator to implement the PhysicalTableDual's CloneForPlanCache

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
