# Issue #64643: planner: `READ_FROM_STORAGE` hint table alias matching problem when using crossdb bindings

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/64643
- Status: closed
- Type: type/bug
- Created At: 2025-11-24T07:25:48Z
- Closed At: 2025-12-08T06:23:27Z
- Labels: affects-8.5, component/spm, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #64644: planner: fix the issue that `READ_FROM_STORAGE` hint doesn't consider cross-db binding
  URL: https://github.com/pingcap/tidb/pull/64644
  State: closed
  Merged At: 2025-11-24T12:45:26Z
  Changed Files Count: 3
  Main Modules: pkg/bindinfo, pkg/util
  Sample Changed Files:
  - pkg/bindinfo/tests/BUILD.bazel
  - pkg/bindinfo/tests/cross_db_binding_test.go
  - pkg/util/hint/hint.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: fix the issue that  hint doesn't consider cross-db binding What changed and how does it work? The database name might be "*" for cross-db bindings, we need to consider this case when matching tables for  hint.
- Fix PR #64653: planner: fix the issue that `READ_FROM_STORAGE` hint doesn't consider cross-db binding (#64644)
  URL: https://github.com/pingcap/tidb/pull/64653
  State: closed
  Merged At: 2025-12-15T14:05:56Z
  Changed Files Count: 2
  Main Modules: pkg/bindinfo, pkg/util
  Sample Changed Files:
  - pkg/bindinfo/fuzzy_binding_test.go
  - pkg/util/hint/hint.go
  PR Summary: This is an automated cherry-pick of #64644 What problem does this PR solve? Problem Summary: planner: fix the issue that  hint doesn't consider cross-db binding What changed and how does it work? The database name might be "*" for cross-db bindings, we need to consider this case when matching tables for  hint.
- Related PR #64689: planner: pick #64622 #63519 #63962 #64644 #64501 | tidb-test=pr/2634
  URL: https://github.com/pingcap/tidb/pull/64689
  State: closed
  Merged At: 2025-11-27T05:26:14Z
  Changed Files Count: 13
  Main Modules: pkg/statistics, pkg/planner/core, pkg/bindinfo, pkg/domain, pkg/util
  Sample Changed Files:
  - pkg/bindinfo/fuzzy_binding_test.go
  - pkg/domain/domain.go
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/index_join_path.go
  - pkg/planner/core/integration_test.go
  - pkg/statistics/handle/bootstrap.go
  - pkg/statistics/handle/storage/read.go
  - pkg/statistics/handle/syncload/stats_syncload.go
  - pkg/statistics/handle/usage/BUILD.bazel
  - pkg/statistics/handle/usage/session_stats_collect.go
  - pkg/statistics/handle/usage/session_stats_collect_test.go
  - pkg/statistics/table.go
  - pkg/util/hint/hint.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
