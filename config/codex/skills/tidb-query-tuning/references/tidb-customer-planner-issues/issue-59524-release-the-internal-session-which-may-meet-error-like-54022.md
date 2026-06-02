# Issue #59524: release the internal session which may meet error like #54022 

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/59524
- Status: closed
- Type: type/bug
- Created At: 2025-02-13T14:10:02Z
- Closed At: 2025-02-18T13:48:27Z
- Labels: affects-7.5, affects-8.1, affects-8.5, impact/leak, may-affects-5.4, may-affects-6.1, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- like the analysis in #54022, the internal session may not be released after it meets some error. the pull that intended to fix that issue only removed the error found in the issue. but the unrealised behavior is not changed.

## Linked PRs
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
- Fix PR #59546: statistics: add Destroy method and handle session recycling
  URL: https://github.com/pingcap/tidb/pull/59546
  State: closed
  Merged At: 2025-02-18T13:48:26Z
  Changed Files Count: 21
  Main Modules: pkg/statistics, pkg/bindinfo, pkg/util, pkg/domain, pkg/ddl, pkg/planner/core
  Sample Changed Files:
  - pkg/bindinfo/global_handle.go
  - pkg/bindinfo/global_handle_test.go
  - pkg/bindinfo/tests/cross_db_binding_test.go
  - pkg/ddl/notifier/testkit_test.go
  - pkg/domain/domain.go
  - pkg/domain/infosync/info.go
  - pkg/planner/core/rule_collect_plan_stats.go
  - pkg/server/server.go
  - pkg/statistics/handle/bootstrap.go
  - pkg/statistics/handle/handle.go
  - pkg/statistics/handle/lockstats/lock_stats.go
  - pkg/statistics/handle/storage/read.go
  - pkg/statistics/handle/syncload/stats_syncload.go
  - pkg/statistics/handle/util/BUILD.bazel
  - pkg/statistics/handle/util/pool.go
  - pkg/statistics/handle/util/util.go
  - pkg/statistics/handle/util/util_test.go
  - pkg/testkit/mocksessionmanager.go
  - pkg/util/processinfo.go
  - pkg/util/session_pool.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? ref This is an alternative API design to solve the problem. I believe explicitly using destroy instead of exposing implementation details is a better approach to fix it.
- Fix PR #59614: statistics: add Destroy method and handle session recycling (#59546)
  URL: https://github.com/pingcap/tidb/pull/59614
  State: closed
  Merged At: 2025-02-21T10:39:54Z
  Changed Files Count: 24
  Main Modules: pkg/statistics, pkg/util, pkg/bindinfo, pkg/domain, DEPS.bzl, go.mod
  Sample Changed Files:
  - DEPS.bzl
  - go.mod
  - go.sum
  - pkg/bindinfo/global_handle.go
  - pkg/bindinfo/global_handle_test.go
  - pkg/ddl/notifier/testkit_test.go
  - pkg/domain/domain.go
  - pkg/domain/infosync/info.go
  - pkg/planner/core/rule_collect_plan_stats.go
  - pkg/server/server.go
  - pkg/statistics/handle/bootstrap.go
  - pkg/statistics/handle/handle.go
  - pkg/statistics/handle/lockstats/lock_stats.go
  - pkg/statistics/handle/storage/read.go
  - pkg/statistics/handle/syncload/stats_syncload.go
  - pkg/statistics/handle/util/BUILD.bazel
  - pkg/statistics/handle/util/pool.go
  - pkg/statistics/handle/util/util.go
  - pkg/statistics/handle/util/util_test.go
  - pkg/testkit/mocksessionmanager.go
  PR Summary: This is an automated cherry-pick of #59546 What problem does this PR solve? Problem Summary: What changed and how does it work? ref
- Fix PR #59615: statistics: add Destroy method and handle session recycling (#59546)
  URL: https://github.com/pingcap/tidb/pull/59615
  State: closed
  Merged At: 2025-02-21T09:22:32Z
  Changed Files Count: 16
  Main Modules: pkg/statistics, pkg/domain, pkg/util, DEPS.bzl, go.mod, go.sum
  Sample Changed Files:
  - DEPS.bzl
  - go.mod
  - go.sum
  - pkg/domain/domain.go
  - pkg/domain/infosync/info.go
  - pkg/planner/core/plan_stats.go
  - pkg/server/server.go
  - pkg/statistics/handle/bootstrap.go
  - pkg/statistics/handle/handle_hist.go
  - pkg/statistics/handle/storage/read.go
  - pkg/statistics/handle/util/BUILD.bazel
  - pkg/statistics/handle/util/util.go
  - pkg/statistics/handle/util/util_test.go
  - pkg/testkit/mocksessionmanager.go
  - pkg/util/logutil/log.go
  - pkg/util/processinfo.go
  PR Summary: This is an automated cherry-pick of #59546 What problem does this PR solve? Problem Summary: What changed and how does it work? ref
- Fix PR #59616: statistics: add Destroy method and handle session recycling (#59546)
  URL: https://github.com/pingcap/tidb/pull/59616
  State: open
  Merged At: not merged
  Changed Files Count: 21
  Main Modules: pkg/statistics, pkg/bindinfo, pkg/domain, pkg/util, DEPS.bzl, go.mod
  Sample Changed Files:
  - DEPS.bzl
  - go.mod
  - go.sum
  - pkg/bindinfo/global_handle.go
  - pkg/bindinfo/util.go
  - pkg/domain/domain.go
  - pkg/domain/infosync/info.go
  - pkg/planner/core/rule_collect_plan_stats.go
  - pkg/server/server.go
  - pkg/statistics/handle/bootstrap.go
  - pkg/statistics/handle/handle.go
  - pkg/statistics/handle/lockstats/lock_stats.go
  - pkg/statistics/handle/storage/read.go
  - pkg/statistics/handle/syncload/stats_syncload.go
  - pkg/statistics/handle/util/BUILD.bazel
  - pkg/statistics/handle/util/pool.go
  - pkg/statistics/handle/util/util.go
  - pkg/statistics/handle/util/util_test.go
  - pkg/testkit/mocksessionmanager.go
  - pkg/util/logutil/log.go
  PR Summary: This is an automated cherry-pick of #59546 What problem does this PR solve? Problem Summary: What changed and how does it work? ref
- Fix PR #59634: statistics: add Destroy method and handle session recycling (#59546)
  URL: https://github.com/pingcap/tidb/pull/59634
  State: closed
  Merged At: 2025-02-19T06:52:10Z
  Changed Files Count: 12
  Main Modules: pkg/statistics, pkg/domain, pkg/planner/core, pkg/server, pkg/testkit, pkg/util
  Sample Changed Files:
  - pkg/domain/domain.go
  - pkg/domain/infosync/info.go
  - pkg/planner/core/plan_stats.go
  - pkg/server/server.go
  - pkg/statistics/handle/bootstrap.go
  - pkg/statistics/handle/handle_hist.go
  - pkg/statistics/handle/storage/read.go
  - pkg/statistics/handle/util/BUILD.bazel
  - pkg/statistics/handle/util/util.go
  - pkg/statistics/handle/util/util_test.go
  - pkg/testkit/mocksessionmanager.go
  - pkg/util/processinfo.go
  PR Summary: This is an automated cherry-pick of #59546 What problem does this PR solve? Problem Summary: What changed and how does it work? ref
- Fix PR #59670: statistics: add Destroy method and handle session recycling (#59546) (#59634)
  URL: https://github.com/pingcap/tidb/pull/59670
  State: closed
  Merged At: not merged
  Changed Files Count: 12
  Main Modules: pkg/statistics, domain/domain.go, domain/infosync, pkg/planner/core, server/server.go, statistics/handle
  Sample Changed Files:
  - domain/domain.go
  - domain/infosync/info.go
  - pkg/planner/core/plan_stats.go
  - pkg/statistics/handle/bootstrap.go
  - pkg/statistics/handle/storage/read.go
  - pkg/statistics/handle/util/BUILD.bazel
  - pkg/statistics/handle/util/util.go
  - pkg/statistics/handle/util/util_test.go
  - server/server.go
  - statistics/handle/handle_hist.go
  - testkit/mocksessionmanager.go
  - util/processinfo.go
  PR Summary: This is an automated cherry-pick of #59634 This is an automated cherry-pick of #59546 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #59671: statistics: add Destroy method and handle session recycling (#59546)
  URL: https://github.com/pingcap/tidb/pull/59671
  State: closed
  Merged At: not merged
  Changed Files Count: 21
  Main Modules: pkg/statistics, pkg/bindinfo, domain/infosync, domain/session_pool_test.go, pkg/ddl, pkg/domain
  Sample Changed Files:
  - domain/infosync/info.go
  - domain/session_pool_test.go
  - pkg/bindinfo/global_handle.go
  - pkg/bindinfo/global_handle_test.go
  - pkg/bindinfo/tests/cross_db_binding_test.go
  - pkg/ddl/notifier/testkit_test.go
  - pkg/domain/domain.go
  - pkg/planner/core/rule_collect_plan_stats.go
  - pkg/statistics/handle/bootstrap.go
  - pkg/statistics/handle/handle.go
  - pkg/statistics/handle/lockstats/lock_stats.go
  - pkg/statistics/handle/storage/read.go
  - pkg/statistics/handle/syncload/stats_syncload.go
  - pkg/statistics/handle/util/BUILD.bazel
  - pkg/statistics/handle/util/pool.go
  - pkg/statistics/handle/util/util.go
  - pkg/statistics/handle/util/util_test.go
  - pkg/util/session_pool.go
  - server/server.go
  - testkit/mocksessionmanager.go
  PR Summary: This is an automated cherry-pick of #59546 What problem does this PR solve? Problem Summary: What changed and how does it work? ref

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
