# Issue #67409: planner: white-list based Plan Cache strategy

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67409
- Status: closed
- Type: type/enhancement
- Created At: 2026-03-30T06:27:47Z
- Closed At: 2026-04-08T21:36:11Z
- Labels: epic/plan-cache, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- Then, for these scenarios, we can: 1) / , 2) then use to identify top highly-frequent queries in this workload, 3) add these highly-frequent queries into the white-list.

## Linked PRs
- Fix PR #67535: planner: support use_plan_cache hint and binding under hint_only plan cache strategy
  URL: https://github.com/pingcap/tidb/pull/67535
  State: closed
  Merged At: 2026-04-08T21:36:10Z
  Changed Files Count: 11
  Main Modules: pkg/session, pkg/planner/core, pkg/util, tests/integrationtest, pkg/parser, pkg/planner
  Sample Changed Files:
  - pkg/parser/ast/misc.go
  - pkg/planner/core/plan_cache.go
  - pkg/planner/core/plan_cache_utils.go
  - pkg/planner/optimize.go
  - pkg/sessionctx/vardef/tidb_vars.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/sysvar.go
  - pkg/util/hint/hint.go
  - pkg/util/hint/hint_processor.go
  - tests/integrationtest/r/planner/core/plan_cache.result
  - tests/integrationtest/t/planner/core/plan_cache.test
  PR Summary: What problem does this PR solve? Problem Summary: planner: support use_plan_cache hint and binding under hint_only plan cache strategy What changed and how does it work? Added new system variable : (default): keep current behavior

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
