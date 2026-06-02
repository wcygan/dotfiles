# Issue #60037: auto analyze merge global statistics failed  when some partition statistics are missing

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/60037
- Status: closed
- Type: type/bug
- Created At: 2025-03-12T10:08:36Z
- Closed At: 2025-03-13T04:29:03Z
- Labels: affects-6.5, affects-7.1, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- merge global stats failed

## Linked PRs
- Fix PR #60035: statistics: sync TiDBSkipMissingPartitionStats value in the auto analyze
  URL: https://github.com/pingcap/tidb/pull/60035
  State: closed
  Merged At: 2025-03-18T14:13:39Z
  Changed Files Count: 2
  Main Modules: statistics/handle
  Sample Changed Files:
  - statistics/handle/handle.go
  - statistics/handle/update_test.go
  PR Summary: …essionVar What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #60038: planner: add test cases for auto analyze's tidb_skip_missing_partition_stats
  URL: https://github.com/pingcap/tidb/pull/60038
  State: closed
  Merged At: 2025-03-13T04:29:02Z
  Changed Files Count: 2
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/tests/analyze/BUILD.bazel
  - pkg/planner/core/tests/analyze/analyze_test.go
  PR Summary: … What problem does this PR solve? Problem Summary: What changed and how does it work? add test cases for auto analyze's tidb_skip_missing_partition_stats
- Fix PR #60046: statistics: sync TiDBSkipMissingPartitionStats value in the auto analyze (#60038)
  URL: https://github.com/pingcap/tidb/pull/60046
  State: closed
  Merged At: 2025-04-25T08:17:38Z
  Changed Files Count: 2
  Main Modules: statistics/handle
  Sample Changed Files:
  - statistics/handle/updatetest/BUILD.bazel
  - statistics/handle/updatetest/update_test.go
  PR Summary: This is an automated cherry-pick of #60038 … What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #60049: planner: add test cases for auto analyze's tidb_skip_missing_partition_stats (#60038)
  URL: https://github.com/pingcap/tidb/pull/60049
  State: closed
  Merged At: not merged
  Changed Files Count: 2
  Main Modules: planner/core
  Sample Changed Files:
  - planner/core/tests/cte/BUILD.bazel
  - planner/core/tests/cte/main_test.go
  PR Summary: This is an automated cherry-pick of #60038 … What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #60270: statistics: sync TiDBSkipMissingPartitionStats value in the auto analyze | tidb-test=920d9bf1b1137cda1272bdd59ae527aee8067944
  URL: https://github.com/pingcap/tidb/pull/60270
  State: closed
  Merged At: 2025-03-27T02:58:12Z
  Changed Files Count: 2
  Main Modules: statistics/handle
  Sample Changed Files:
  - statistics/handle/handle.go
  - statistics/handle/update_test.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
