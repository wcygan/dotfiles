# Issue #54022: TiDB memory leak after meets the `fail to get stats version for this histogram`

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/54022
- Status: closed
- Type: type/bug
- Created At: 2024-06-14T03:54:53Z
- Closed At: 2024-06-20T04:31:06Z
- Labels: affects-6.5, affects-7.1, affects-7.5, impact/leak, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- ![img_v3_02bq_c13de680-8d76-4927-8f90-70d0f55d1e5g]() ![img_v3_02bq_3ff29c9b-d5c3-40a1-b8d6-48242f5e8aag]() ![img_v3_02bq_1278b481-a16b-4a56-ab13-5f86d68d0abg]()

## Linked PRs
- Related PR #54060: statistics: do not load unnecessary index statistics
  URL: https://github.com/pingcap/tidb/pull/54060
  State: closed
  Merged At: 2024-06-18T08:23:47Z
  Changed Files Count: 4
  Main Modules: pkg/statistics, tests/realtikvtest
  Sample Changed Files:
  - pkg/statistics/handle/handle_hist.go
  - pkg/statistics/handle/storage/read.go
  - tests/realtikvtest/statisticstest/BUILD.bazel
  - tests/realtikvtest/statisticstest/statistics_test.go
  PR Summary: What problem does this PR solve? Problem Summary: See more at the issue. A quick summary: If you have  enabled, it will trigger some async stats load for some tables. If there tables histogram isn't in the system, it would cause some problems when we try to load it.
- Related PR #54087: statistics: do not load unnecessary index statistics (#54060)
  URL: https://github.com/pingcap/tidb/pull/54087
  State: closed
  Merged At: 2024-11-11T10:54:30Z
  Changed Files Count: 2
  Main Modules: statistics/handle
  Sample Changed Files:
  - statistics/handle/handle.go
  - statistics/handle/handle_hist.go
  PR Summary: This is an automated cherry-pick of #54060 What problem does this PR solve? Problem Summary: See more at the issue. A quick summary:
- Related PR #54137: statistics: add a testcase for issue 54022
  URL: https://github.com/pingcap/tidb/pull/54137
  State: closed
  Merged At: 2024-07-05T09:38:34Z
  Changed Files Count: 2
  Main Modules: tests/realtikvtest
  Sample Changed Files:
  - tests/realtikvtest/statisticstest/BUILD.bazel
  - tests/realtikvtest/statisticstest/statistics_test.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? Added a test case for the issue 54022 to make sure we don't have this bug on master.
- Related PR #54476: statistics: add a testcase for issue 54022 (#54137)
  URL: https://github.com/pingcap/tidb/pull/54476
  State: closed
  Merged At: not merged
  Changed Files Count: 2
  Main Modules: tests/realtikvtest
  Sample Changed Files:
  - tests/realtikvtest/statisticstest/BUILD.bazel
  - tests/realtikvtest/statisticstest/statistics_test.go
  PR Summary: This is an automated cherry-pick of #54137 What problem does this PR solve? Problem Summary: What changed and how does it work? Added a test case for the issue 54022 to make sure we don't have this bug on master.
- Related PR #54477: statistics: add a testcase for issue 54022 (#54137)
  URL: https://github.com/pingcap/tidb/pull/54477
  State: closed
  Merged At: not merged
  Changed Files Count: 2
  Main Modules: tests/realtikvtest
  Sample Changed Files:
  - tests/realtikvtest/statisticstest/BUILD.bazel
  - tests/realtikvtest/statisticstest/statistics_test.go
  PR Summary: This is an automated cherry-pick of #54137 What problem does this PR solve? Problem Summary: What changed and how does it work? Added a test case for the issue 54022 to make sure we don't have this bug on master.
- Fix PR #59522: statistics: release session met error to avoid possible leak
  URL: https://github.com/pingcap/tidb/pull/59522
  State: closed
  Merged At: not merged
  Changed Files Count: 7
  Main Modules: pkg/statistics, pkg/domain, pkg/server, pkg/testkit, pkg/util
  Sample Changed Files:
  - pkg/domain/infosync/info.go
  - pkg/server/server.go
  - pkg/statistics/handle/util/BUILD.bazel
  - pkg/statistics/handle/util/util.go
  - pkg/statistics/handle/util/util_test.go
  - pkg/testkit/mocksessionmanager.go
  - pkg/util/processinfo.go
  PR Summary: What problem does this PR solve? Problem Summary: We should release the session pool after abandoning it. What changed and how does it work?
- Related PR #59649: statistics: do not load unnecessary index statistics (#54060)
  URL: https://github.com/pingcap/tidb/pull/59649
  State: closed
  Merged At: 2025-02-24T11:43:19Z
  Changed Files Count: 2
  Main Modules: statistics/handle
  Sample Changed Files:
  - statistics/handle/handle.go
  - statistics/handle/handle_hist.go
  PR Summary: This is an automated cherry-pick of #54060 What problem does this PR solve? Problem Summary: See more at the issue. A quick summary:
- Related PR #59720: statistics: add a testcase for issue 54022 (#54137)
  URL: https://github.com/pingcap/tidb/pull/59720
  State: closed
  Merged At: not merged
  Changed Files Count: 2
  Main Modules: tests/realtikvtest
  Sample Changed Files:
  - tests/realtikvtest/statisticstest/BUILD.bazel
  - tests/realtikvtest/statisticstest/statistics_test.go
  PR Summary: This is an automated cherry-pick of #54137 What problem does this PR solve? Problem Summary: What changed and how does it work? Added a test case for the issue 54022 to make sure we don't have this bug on master.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
