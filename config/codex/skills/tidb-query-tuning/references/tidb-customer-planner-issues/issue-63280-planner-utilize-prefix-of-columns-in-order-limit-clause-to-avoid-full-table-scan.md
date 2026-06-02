# Issue #63280: planner: utilize prefix of columns in order-limit clause to avoid full table scan in join queries

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/63280
- Status: closed
- Type: type/enhancement
- Created At: 2025-08-29T08:26:17Z
- Closed At: 2026-02-28T10:32:40Z
- Labels: affects-8.5, plan-rewrite, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- But actually, we could first use some prefix columns of order-limit clause to avoid full table scan, and then order the final results by 2 columns at the end, which is like:

## Linked PRs
- Fix PR #65314: session: Add a new session variable to control the prefix index optimization for ORDER BY ... LIMIT queries
  URL: https://github.com/pingcap/tidb/pull/65314
  State: closed
  Merged At: 2025-12-31T12:48:45Z
  Changed Files Count: 14
  Main Modules: pkg/session, build/nogo_config.json, pkg/planner/core
  Sample Changed Files:
  - build/nogo_config.json
  - pkg/planner/core/hint_test.go
  - pkg/sessionctx/vardef/tidb_vars.go
  - pkg/sessionctx/variable/BUILD.bazel
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/sysvar.go
  - pkg/sessionctx/variable/sysvar_test.go
  - pkg/sessionctx/variable/tests/BUILD.bazel
  - pkg/sessionctx/variable/tests/main_test.go
  - pkg/sessionctx/variable/tests/session_test.go
  - pkg/sessionctx/variable/tests/slowlog/BUILD.bazel
  - pkg/sessionctx/variable/tests/slowlog/main_test.go
  - pkg/sessionctx/variable/tests/slowlog/slow_log_test.go
  - pkg/sessionctx/variable/tests/variable_test.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? 1. Added a new session variable tidb_opt_partial_ordered_index_for_topn to control prefix index optimization for ORDER BY ... LIMIT queries. 2. This is a global | session variable
- Related PR #65533: planner: add the prefix index as candidate for topn optimization
  URL: https://github.com/pingcap/tidb/pull/65533
  State: closed
  Merged At: 2026-01-17T14:41:29Z
  Changed Files Count: 5
  Main Modules: pkg/planner/core, pkg/planner
  Sample Changed Files:
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/operator/logicalop/logical_projection.go
  - pkg/planner/core/operator/physicalop/physical_topn.go
  - pkg/planner/core/util.go
  - pkg/planner/property/physical_property.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? The planner part 1 of the partial order by enhancement 1. The new physical property

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
