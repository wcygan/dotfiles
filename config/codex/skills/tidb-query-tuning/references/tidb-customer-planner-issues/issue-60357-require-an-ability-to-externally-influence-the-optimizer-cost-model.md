# Issue #60357: Require an ability to externally influence the optimizer cost model

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/60357
- Status: closed
- Type: type/enhancement
- Created At: 2025-04-02T00:50:13Z
- Closed At: 2025-04-10T21:56:34Z
- Labels: affects-8.5, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- The TiDB optimizer would benefit from having an ability to influence the optimizer's cost of each physical operator in a query plan. This could be used externally to influence query plans (by customers/users and also TiDB engineers), and could be used by TiDB engineers to test and adjust the optimizer's cost model.

## Linked PRs
- Fix PR #60333: planner: add optimizer cost factors
  URL: https://github.com/pingcap/tidb/pull/60333
  State: closed
  Merged At: 2025-04-10T21:56:33Z
  Changed Files Count: 9
  Main Modules: tests/integrationtest, pkg/session, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/plan_cost_ver2.go
  - pkg/planner/core/plan_cost_ver2_test.go
  - pkg/sessionctx/vardef/tidb_vars.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/sysvar.go
  - tests/integrationtest/r/executor/explain.result
  - tests/integrationtest/r/planner/core/cbo.result
  - tests/integrationtest/r/planner/core/plan_cache.result
  - tests/integrationtest/r/planner/core/plan_cost_ver2.result
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? Add a global variable "cost factor" to the more common optimizer physical operators. This allows an ability to externally control the optimizer's plan choice(s) - by either increasing the cost factor for one operation (to discourage that plan choice), or decreasing the cost factor of an operation (to encourage that plan choice).
- Fix PR #60512: planner: add optimizer cost factor tests
  URL: https://github.com/pingcap/tidb/pull/60512
  State: closed
  Merged At: 2025-04-14T03:55:06Z
  Changed Files Count: 1
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/plan_cost_ver2_test.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? Add testcases for recent optimizer cost factors.
- Fix PR #60558: planner: add hint support for optimizer cost factors
  URL: https://github.com/pingcap/tidb/pull/60558
  State: closed
  Merged At: 2025-04-16T04:27:58Z
  Changed Files Count: 4
  Main Modules: pkg/planner/core, pkg/session
  Sample Changed Files:
  - pkg/planner/core/casetest/hint/BUILD.bazel
  - pkg/planner/core/casetest/hint/hint_test.go
  - pkg/planner/core/plan_cost_ver2_test.go
  - pkg/sessionctx/variable/setvar_affect.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #61765: planner: add optimizer cost factors (#60333)
  URL: https://github.com/pingcap/tidb/pull/61765
  State: closed
  Merged At: 2025-06-25T15:23:21Z
  Changed Files Count: 9
  Main Modules: tests/integrationtest, pkg/session, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/plan_cost_ver2.go
  - pkg/planner/core/plan_cost_ver2_test.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/sysvar.go
  - pkg/sessionctx/variable/tidb_vars.go
  - tests/integrationtest/r/executor/explain.result
  - tests/integrationtest/r/planner/core/cbo.result
  - tests/integrationtest/r/planner/core/plan_cache.result
  - tests/integrationtest/r/planner/core/plan_cost_ver2.result
  PR Summary: This is an automated cherry-pick of #60333 What problem does this PR solve? Problem Summary: What changed and how does it work? Add a global variable "cost factor" to the more common optimizer physical operators. This allows an ability to externally control the optimizer's plan choice(s) - by either increasing the cost factor for one operation (to discourage that plan choice), or decreasing the cost factor of an operation (to encourage that plan choice).
- Fix PR #61903: planner: add optimizer cost factor tests (#60512)
  URL: https://github.com/pingcap/tidb/pull/61903
  State: closed
  Merged At: 2025-07-02T19:48:27Z
  Changed Files Count: 1
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/plan_cost_ver2_test.go
  PR Summary: This is an automated cherry-pick of #60512 What problem does this PR solve? Problem Summary: What changed and how does it work? Add testcases for recent optimizer cost factors.
- Fix PR #61904: planner: add hint support for optimizer cost factors (#60558)
  URL: https://github.com/pingcap/tidb/pull/61904
  State: closed
  Merged At: 2025-07-07T13:43:33Z
  Changed Files Count: 4
  Main Modules: pkg/planner/core, pkg/session
  Sample Changed Files:
  - pkg/planner/core/casetest/hint/BUILD.bazel
  - pkg/planner/core/casetest/hint/hint_test.go
  - pkg/planner/core/plan_cost_ver2_test.go
  - pkg/sessionctx/variable/setvar_affect.go
  PR Summary: This is an automated cherry-pick of #60558 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #64553: planner: add optimizer cost factors
  URL: https://github.com/pingcap/tidb/pull/64553
  State: closed
  Merged At: not merged
  Changed Files Count: 4
  Main Modules: pkg/session, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/plan_cost_ver2.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/sysvar.go
  - pkg/sessionctx/variable/tidb_vars.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #64564: planner: add optimizer cost factors | tidb-test=release-8.5-20250114-v8.5.0 
  URL: https://github.com/pingcap/tidb/pull/64564
  State: closed
  Merged At: 2025-11-19T15:38:41Z
  Changed Files Count: 9
  Main Modules: tests/integrationtest, pkg/session, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/plan_cost_ver2.go
  - pkg/planner/core/plan_cost_ver2_test.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/sysvar.go
  - pkg/sessionctx/variable/tidb_vars.go
  - tests/integrationtest/r/executor/explain.result
  - tests/integrationtest/r/planner/core/cbo.result
  - tests/integrationtest/r/planner/core/plan_cache.result
  - tests/integrationtest/r/planner/core/plan_cost_ver2.result
  PR Summary: What problem does this PR solve? Problem Summary: cherry pick  to v8.5.0 for hotfix What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
