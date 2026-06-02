# Issue #56603: Parsing CTE error with "doesn't yet support 'ORDER BY / LIMIT / SELECT DISTINCT in recursive query block"

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/56603
- Status: closed
- Type: type/bug
- Created At: 2024-10-12T05:39:52Z
- Closed At: 2024-10-15T11:02:29Z
- Labels: affects-6.5, affects-7.1, affects-7.5, affects-8.1, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- ERROR 1235 (42000): This version of TiDB doesn't yet support 'ORDER BY / LIMIT / SELECT DISTINCT in recursive query block of Common Table Expression'

## Linked PRs
- Fix PR #56609: planner, CTE, view: Fix default inline CTE which contains orderby/limit/distinct and inside of view | tidb-test=pr/2415
  URL: https://github.com/pingcap/tidb/pull/56609
  State: closed
  Merged At: 2024-10-15T11:02:28Z
  Changed Files Count: 14
  Main Modules: pkg/planner/core, pkg/planner, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/flatplan/testdata/flat_plan_suite_out.json
  - pkg/planner/core/casetest/hint/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/planstats/BUILD.bazel
  - pkg/planner/core/casetest/planstats/plan_stats_test.go
  - pkg/planner/core/casetest/planstats/testdata/plan_stats_suite_in.json
  - pkg/planner/core/casetest/planstats/testdata/plan_stats_suite_out.json
  - pkg/planner/core/casetest/rule/testdata/outer2inner_in.json
  - pkg/planner/core/casetest/rule/testdata/outer2inner_out.json
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/planbuilder.go
  - pkg/planner/indexadvisor/BUILD.bazel
  - pkg/planner/indexadvisor/indexadvisor_test.go
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/t/planner/core/casetest/physicalplantest/physical_plan.test
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? 1. If the CTE contain orderby/limit/distinct and CTE is referenced by another CTE recursive part, it cannot be inlined . Related issue #56603 2. If the CTE inside of view, the consumerCount of CTE cannot be updated because the view skip the preprocessor phase in during optimizer, it also cannot judge the inline or not. So the CTE inside of view will always be not inlined. Related issue  #56582
- Fix PR #56666: planner, CTE, view: Fix default inline CTE which contains orderby/limit/distinct and inside of view | tidb-test=e1d0c1e615f749e7139f5be95bc4a2b8cedb7380 (#56609)
  URL: https://github.com/pingcap/tidb/pull/56666
  State: closed
  Merged At: 2024-10-16T06:25:29Z
  Changed Files Count: 8
  Main Modules: planner/core
  Sample Changed Files:
  - planner/core/logical_plan_builder.go
  - planner/core/physical_plan_test.go
  - planner/core/plan_stats_test.go
  - planner/core/planbuilder.go
  - planner/core/testdata/flat_plan_suite_out.json
  - planner/core/testdata/integration_suite_out.json
  - planner/core/testdata/plan_suite_in.json
  - planner/core/testdata/plan_suite_out.json
  PR Summary: This is an automated cherry-pick of #56609 What problem does this PR solve? Problem Summary: What changed and how does it work? 1. If the CTE contain orderby/limit/distinct and CTE is referenced by another CTE recursive part, it cannot be inlined . Related issue #56603
- Fix PR #56670: planner, CTE, view: Fix default inline CTE which contains orderby/limit/distinct and inside of view | tidb-test=pr/2418
  URL: https://github.com/pingcap/tidb/pull/56670
  State: closed
  Merged At: 2024-12-23T04:08:45Z
  Changed Files Count: 8
  Main Modules: planner/core
  Sample Changed Files:
  - planner/core/logical_plan_builder.go
  - planner/core/physical_plan_test.go
  - planner/core/plan_stats_test.go
  - planner/core/planbuilder.go
  - planner/core/testdata/flat_plan_suite_out.json
  - planner/core/testdata/integration_suite_out.json
  - planner/core/testdata/plan_suite_in.json
  - planner/core/testdata/plan_suite_out.json
  PR Summary: This is an automated cherry-pick of #56609 What problem does this PR solve? Problem Summary: What changed and how does it work? 1. If the CTE contain orderby/limit/distinct and CTE is referenced by another CTE recursive part, it cannot be inlined . Related issue #56603
- Fix PR #56694: planner, CTE, view: Fix default inline CTE which contains orderby/limit/distinct and inside of view | tidb-test=pr/2415 (#56609)
  URL: https://github.com/pingcap/tidb/pull/56694
  State: open
  Merged At: not merged
  Changed Files Count: 14
  Main Modules: pkg/planner/core, pkg/planner, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/flatplan/testdata/flat_plan_suite_out.json
  - pkg/planner/core/casetest/hint/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/planstats/BUILD.bazel
  - pkg/planner/core/casetest/planstats/plan_stats_test.go
  - pkg/planner/core/casetest/planstats/testdata/plan_stats_suite_in.json
  - pkg/planner/core/casetest/planstats/testdata/plan_stats_suite_out.json
  - pkg/planner/core/casetest/rule/testdata/outer2inner_in.json
  - pkg/planner/core/casetest/rule/testdata/outer2inner_out.json
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/planbuilder.go
  - pkg/planner/indexadvisor/BUILD.bazel
  - pkg/planner/indexadvisor/indexadvisor_test.go
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/t/planner/core/casetest/physicalplantest/physical_plan.test
  PR Summary: This is an automated cherry-pick of #56609 What problem does this PR solve? Problem Summary: What changed and how does it work? 1. If the CTE contain orderby/limit/distinct and CTE is referenced by another CTE recursive part, it cannot be inlined . Related issue #56603
- Fix PR #56695: planner, CTE, view: Fix default inline CTE which contains orderby/limit/distinct and inside of view | tidb-test=pr/2438 (#56609)
  URL: https://github.com/pingcap/tidb/pull/56695
  State: closed
  Merged At: 2024-12-04T03:17:47Z
  Changed Files Count: 11
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/flatplan/testdata/flat_plan_suite_out.json
  - pkg/planner/core/casetest/hint/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/physicalplantest/physical_plan_test.go
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_in.json
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/planstats/BUILD.bazel
  - pkg/planner/core/casetest/planstats/plan_stats_test.go
  - pkg/planner/core/casetest/planstats/testdata/plan_stats_suite_in.json
  - pkg/planner/core/casetest/planstats/testdata/plan_stats_suite_out.json
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/planbuilder.go
  PR Summary: This is an automated cherry-pick of #56609 What problem does this PR solve? Problem Summary: What changed and how does it work? 1. If the CTE contain orderby/limit/distinct and CTE is referenced by another CTE recursive part, it cannot be inlined . Related issue #56603
- Fix PR #56696: planner, CTE, view: Fix default inline CTE which contains orderby/limit/distinct and inside of view | tidb-test=pr/2422 (#56609)
  URL: https://github.com/pingcap/tidb/pull/56696
  State: closed
  Merged At: 2024-11-07T08:45:26Z
  Changed Files Count: 8
  Main Modules: planner/core
  Sample Changed Files:
  - planner/core/casetest/physical_plan_test.go
  - planner/core/casetest/testdata/flat_plan_suite_out.json
  - planner/core/casetest/testdata/integration_suite_out.json
  - planner/core/casetest/testdata/plan_suite_in.json
  - planner/core/casetest/testdata/plan_suite_out.json
  - planner/core/logical_plan_builder.go
  - planner/core/plan_stats_test.go
  - planner/core/planbuilder.go
  PR Summary: This is an automated cherry-pick of #56609 What problem does this PR solve? Problem Summary: What changed and how does it work? 1. If the CTE contain orderby/limit/distinct and CTE is referenced by another CTE recursive part, it cannot be inlined . Related issue #56603
- Fix PR #58314: planner, CTE, view: Fix default inline CTE which contains orderby/limit/distinct and inside of view | tidb-test=e1d0c1e615f749e7139f5be95bc4a2b8cedb7380
  URL: https://github.com/pingcap/tidb/pull/58314
  State: closed
  Merged At: 2024-12-17T04:03:00Z
  Changed Files Count: 8
  Main Modules: planner/core
  Sample Changed Files:
  - planner/core/logical_plan_builder.go
  - planner/core/physical_plan_test.go
  - planner/core/plan_stats_test.go
  - planner/core/planbuilder.go
  - planner/core/testdata/flat_plan_suite_out.json
  - planner/core/testdata/integration_suite_out.json
  - planner/core/testdata/plan_suite_in.json
  - planner/core/testdata/plan_suite_out.json
  PR Summary: This is an automated cherry-pick of #56609 What problem does this PR solve? Problem Summary: What changed and how does it work? 1. If the CTE contain orderby/limit/distinct and CTE is referenced by another CTE recursive part, it cannot be inlined . Related issue #56603

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
