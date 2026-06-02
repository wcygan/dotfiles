# Issue #55803: query results of information_schema.tables not accurate

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/55803
- Status: closed
- Type: type/bug
- Created At: 2024-09-02T12:59:50Z
- Closed At: 2025-03-02T08:37:52Z
- Labels: affects-8.1, affects-8.5, component/statistics, report/customer, severity/major, sig/planner, type/bug, type/regression

## Customer-Facing Phenomenon
- The query results not accurate, there is no max_data_length . and some tables has no results. Also, run the query multple times, result might be different.

## Linked PRs
- Related PR #55789: DO NOT MERGE debug: add more logs
  URL: https://github.com/pingcap/tidb/pull/55789
  State: closed
  Merged At: not merged
  Changed Files Count: 1
  Main Modules: pkg/statistics
  Sample Changed Files:
  - pkg/statistics/handle/cache/stats_table_row_cache.go
  PR Summary: DO NOT MERGE THIS PR.
- Related PR #56287: statistics: Remove the ineffective dirty IDs from the row count cache
  URL: https://github.com/pingcap/tidb/pull/56287
  State: closed
  Merged At: 2025-03-02T08:37:51Z
  Changed Files Count: 10
  Main Modules: pkg/statistics, pkg/executor
  Sample Changed Files:
  - pkg/executor/infoschema_reader.go
  - pkg/statistics/handle/cache/stats_table_row_cache.go
  - pkg/statistics/handle/history/BUILD.bazel
  - pkg/statistics/handle/history/history_stats.go
  - pkg/statistics/handle/lockstats/BUILD.bazel
  - pkg/statistics/handle/lockstats/unlock_stats.go
  - pkg/statistics/handle/storage/BUILD.bazel
  - pkg/statistics/handle/storage/gc.go
  - pkg/statistics/handle/storage/save.go
  - pkg/statistics/handle/storage/update.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? As I mentioned in the issue  the main problem is that  anciently updates the modify_time even when the dirty tables have not been updated. But as @time-and-fate mentioned, the maintenance of the dirty table follows a best-effort approach, so it would be better to delete it entirely.
- Related PR #59854: statistics: Remove the ineffective dirty IDs from the row count cache (#56287)
  URL: https://github.com/pingcap/tidb/pull/59854
  State: open
  Merged At: not merged
  Changed Files Count: 10
  Main Modules: pkg/statistics, executor/infoschema_reader.go
  Sample Changed Files:
  - executor/infoschema_reader.go
  - pkg/statistics/handle/cache/stats_table_row_cache.go
  - pkg/statistics/handle/history/BUILD.bazel
  - pkg/statistics/handle/history/history_stats.go
  - pkg/statistics/handle/lockstats/BUILD.bazel
  - pkg/statistics/handle/lockstats/unlock_stats.go
  - pkg/statistics/handle/storage/BUILD.bazel
  - pkg/statistics/handle/storage/gc.go
  - pkg/statistics/handle/storage/save.go
  - pkg/statistics/handle/storage/update.go
  PR Summary: This is an automated cherry-pick of #56287 What problem does this PR solve? Problem Summary: What changed and how does it work? As I mentioned in the issue  the main problem is that  anciently updates the modify_time even when the dirty tables have not been updated.
- Related PR #59855: statistics: Remove the ineffective dirty IDs from the row count cache (#56287)
  URL: https://github.com/pingcap/tidb/pull/59855
  State: open
  Merged At: not merged
  Changed Files Count: 10
  Main Modules: pkg/statistics, pkg/executor
  Sample Changed Files:
  - pkg/executor/infoschema_reader.go
  - pkg/statistics/handle/cache/stats_table_row_cache.go
  - pkg/statistics/handle/history/BUILD.bazel
  - pkg/statistics/handle/history/history_stats.go
  - pkg/statistics/handle/lockstats/BUILD.bazel
  - pkg/statistics/handle/lockstats/unlock_stats.go
  - pkg/statistics/handle/storage/BUILD.bazel
  - pkg/statistics/handle/storage/gc.go
  - pkg/statistics/handle/storage/save.go
  - pkg/statistics/handle/storage/update.go
  PR Summary: This is an automated cherry-pick of #56287 What problem does this PR solve? Problem Summary: What changed and how does it work? As I mentioned in the issue  the main problem is that  anciently updates the modify_time even when the dirty tables have not been updated.
- Related PR #59862: statistics: Remove the ineffective dirty IDs from the row count cache (#56287)
  URL: https://github.com/pingcap/tidb/pull/59862
  State: closed
  Merged At: 2025-04-17T03:32:21Z
  Changed Files Count: 9
  Main Modules: pkg/statistics, pkg/executor
  Sample Changed Files:
  - pkg/executor/infoschema_reader.go
  - pkg/statistics/handle/cache/stats_table_row_cache.go
  - pkg/statistics/handle/history/BUILD.bazel
  - pkg/statistics/handle/history/history_stats.go
  - pkg/statistics/handle/lockstats/BUILD.bazel
  - pkg/statistics/handle/lockstats/unlock_stats.go
  - pkg/statistics/handle/storage/gc.go
  - pkg/statistics/handle/storage/save.go
  - pkg/statistics/handle/storage/update.go
  PR Summary: This is an automated cherry-pick of #56287 What problem does this PR solve? Problem Summary: What changed and how does it work? As I mentioned in the issue  the main problem is that  anciently updates the modify_time even when the dirty tables have not been updated.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
