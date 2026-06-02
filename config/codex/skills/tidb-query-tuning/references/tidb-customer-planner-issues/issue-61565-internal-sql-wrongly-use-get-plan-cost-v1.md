# Issue #61565: internal SQL wrongly use get plan cost v1

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/61565
- Status: closed
- Type: type/bug
- Created At: 2025-06-06T11:12:24Z
- Closed At: 2025-06-10T05:22:29Z
- Labels: affects-6.5, affects-7.1, affects-7.5, affects-8.1, affects-8.5, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- When you enable the flame graph, you will find that some of the internal SQL stacks have stacks that call , which is clearly incorrect. ![Image]()

## Linked PRs
- Fix PR #61566: session: set right cost model version
  URL: https://github.com/pingcap/tidb/pull/61566
  State: closed
  Merged At: not merged
  Changed Files Count: 1
  Main Modules: pkg/session
  Sample Changed Files:
  - pkg/session/session.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #61608: planner: set the default of the tidb_cost_model_version correctly
  URL: https://github.com/pingcap/tidb/pull/61608
  State: closed
  Merged At: 2025-06-10T05:22:28Z
  Changed Files Count: 3
  Main Modules: pkg/planner/core, pkg/session, pkg/util
  Sample Changed Files:
  - pkg/planner/core/plan_cost_ver1.go
  - pkg/sessionctx/variable/session.go
  - pkg/util/mock/context.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? We don't set the default of the tidb_cost_model_version in the right place. so it led many problems in the internal SQL. The internal SQL will not use the cost model v2.
- Fix PR #61895: planner: set the default of the tidb_cost_model_version correctly (#61608)
  URL: https://github.com/pingcap/tidb/pull/61895
  State: closed
  Merged At: 2025-07-15T22:58:57Z
  Changed Files Count: 2
  Main Modules: pkg/planner/core, pkg/session
  Sample Changed Files:
  - pkg/planner/core/plan_cost_ver1.go
  - pkg/sessionctx/variable/session.go
  PR Summary: This is an automated cherry-pick of #61608 What problem does this PR solve? Problem Summary: What changed and how does it work? We don't set the default of the tidb_cost_model_version in the right place. so it led many problems in the internal SQL. The internal SQL will not use the cost model v2.
- Fix PR #61896: planner: set the default of the tidb_cost_model_version correctly (#61608)
  URL: https://github.com/pingcap/tidb/pull/61896
  State: open
  Merged At: not merged
  Changed Files Count: 2
  Main Modules: pkg/planner/core, pkg/session
  Sample Changed Files:
  - pkg/planner/core/plan_cost_ver1.go
  - pkg/sessionctx/variable/session.go
  PR Summary: This is an automated cherry-pick of #61608 What problem does this PR solve? Problem Summary: What changed and how does it work? We don't set the default of the tidb_cost_model_version in the right place. so it led many problems in the internal SQL. The internal SQL will not use the cost model v2.
- Fix PR #61897: planner: set the default of the tidb_cost_model_version correctly (#61608)
  URL: https://github.com/pingcap/tidb/pull/61897
  State: closed
  Merged At: 2025-07-09T16:05:03Z
  Changed Files Count: 3
  Main Modules: pkg/planner/core, pkg/session, pkg/util
  Sample Changed Files:
  - pkg/planner/core/plan_cost_ver1.go
  - pkg/sessionctx/variable/session.go
  - pkg/util/mock/context.go
  PR Summary: This is an automated cherry-pick of #61608 What problem does this PR solve? Problem Summary: What changed and how does it work? We don't set the default of the tidb_cost_model_version in the right place. so it led many problems in the internal SQL. The internal SQL will not use the cost model v2.
- Fix PR #62184: planner: set the default of the tidb_cost_model_version correctly (#61608)
  URL: https://github.com/pingcap/tidb/pull/62184
  State: closed
  Merged At: 2025-07-04T01:23:18Z
  Changed Files Count: 2
  Main Modules: pkg/planner/core, pkg/session
  Sample Changed Files:
  - pkg/planner/core/plan_cost_ver1.go
  - pkg/sessionctx/variable/session.go
  PR Summary: This is an automated cherry-pick of #61608 What problem does this PR solve? Problem Summary: What changed and how does it work? We don't set the default of the tidb_cost_model_version in the right place. so it led many problems in the internal SQL. The internal SQL will not use the cost model v2.
- Fix PR #63799: planner: set the default of the tidb_cost_model_version correctly (#61608) | tidb-test=release-8.5.3
  URL: https://github.com/pingcap/tidb/pull/63799
  State: closed
  Merged At: 2025-09-29T14:48:22Z
  Changed Files Count: 3
  Main Modules: pkg/planner/core, pkg/session, pkg/util
  Sample Changed Files:
  - pkg/planner/core/plan_cost_ver1.go
  - pkg/sessionctx/variable/session.go
  - pkg/util/mock/context.go
  PR Summary: This is an automated cherry-pick of #61608 What problem does this PR solve? Problem Summary: What changed and how does it work? We don't set the default of the tidb_cost_model_version in the right place. so it led many problems in the internal SQL. The internal SQL will not use the cost model v2.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
