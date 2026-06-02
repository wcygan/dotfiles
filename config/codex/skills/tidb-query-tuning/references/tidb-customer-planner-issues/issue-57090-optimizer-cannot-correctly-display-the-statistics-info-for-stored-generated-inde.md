# Issue #57090: Optimizer cannot correctly display the statistics info for "stored generated indexes" in the operator info

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/57090
- Status: closed
- Type: type/bug
- Created At: 2024-11-04T03:41:11Z
- Closed At: 2025-10-16T07:17:00Z
- Labels: affects-5.4, affects-6.1, affects-6.5, affects-7.1, affects-7.5, affects-8.1, affects-8.5, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Create a database and a table: 2. Load the stats json for the table: [business_db.event_log.json]() 3. explain analyze the query:

## Linked PRs
- Fix PR #63961: planner: fix uninitialized stats for expression index
  URL: https://github.com/pingcap/tidb/pull/63961
  State: closed
  Merged At: 2025-10-16T07:16:59Z
  Changed Files Count: 3
  Main Modules: pkg/planner
  Sample Changed Files:
  - pkg/planner/cardinality/BUILD.bazel
  - pkg/planner/cardinality/selectivity.go
  - pkg/planner/cardinality/selectivity_test.go
  PR Summary: What problem does this PR solve? Problem Summary: For the following case, the explain analyze output shows  for that expression index(), which is confusing. For expression index , there will be both original column stats and index stats when [calculating selectivity](). Check the following debug output, you can see the column stats is  and the index stats is ready. So for expression index, should use index stats and its column stats.
- Fix PR #64779: planner: fix uninitialized stats for expression index (#63961)
  URL: https://github.com/pingcap/tidb/pull/64779
  State: closed
  Merged At: 2025-12-14T10:59:58Z
  Changed Files Count: 3
  Main Modules: pkg/planner
  Sample Changed Files:
  - pkg/planner/cardinality/BUILD.bazel
  - pkg/planner/cardinality/selectivity.go
  - pkg/planner/cardinality/selectivity_test.go
  PR Summary: This is an automated cherry-pick of #63961 What problem does this PR solve? Problem Summary: For the following case, the explain analyze output shows  for that expression index(), which is confusing. For expression index , there will be both original column stats and index stats when [calculating selectivity]().

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
