# Issue #50012: Multi-statements `prefetchPointPlanKeys` panic

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/50012
- Status: closed
- Type: type/bug
- Created At: 2024-01-03T06:12:49Z
- Closed At: 2024-01-03T12:59:04Z
- Labels: affects-6.5, affects-7.1, affects-7.2, affects-7.3, affects-7.4, affects-7.5, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #50037: server: fix decode issue for prefetch point plan index keys
  URL: https://github.com/pingcap/tidb/pull/50037
  State: closed
  Merged At: 2024-01-03T12:59:03Z
  Changed Files Count: 3
  Main Modules: pkg/server
  Sample Changed Files:
  - pkg/server/BUILD.bazel
  - pkg/server/conn.go
  - pkg/server/internal/testserverclient/server_client.go
  PR Summary: What problem does this PR solve? Problem Summary: The second parameter of  indicates whether index KVs belong to a clustered-index table. Previously, it was always , causing decoding error and panic. What changed and how does it work? Set the parameter properly.
- Fix PR #50046: server: fix decode issue for prefetch point plan index keys (#50037)
  URL: https://github.com/pingcap/tidb/pull/50046
  State: closed
  Merged At: 2024-01-23T15:03:21Z
  Changed Files Count: 3
  Main Modules: server/BUILD.bazel, server/conn.go, server/server_test.go
  Sample Changed Files:
  - server/BUILD.bazel
  - server/conn.go
  - server/server_test.go
  PR Summary: This is an automated cherry-pick of #50037 What problem does this PR solve? Problem Summary: The second parameter of  indicates whether index KVs belong to a clustered-index table. Previously, it was always , causing decoding error and panic. What changed and how does it work?
- Fix PR #50047: server: fix decode issue for prefetch point plan index keys (#50037)
  URL: https://github.com/pingcap/tidb/pull/50047
  State: closed
  Merged At: 2024-02-27T12:04:59Z
  Changed Files Count: 3
  Main Modules: server/BUILD.bazel, server/conn.go, server/server_test.go
  Sample Changed Files:
  - server/BUILD.bazel
  - server/conn.go
  - server/server_test.go
  PR Summary: This is an automated cherry-pick of #50037 What problem does this PR solve? Problem Summary: The second parameter of  indicates whether index KVs belong to a clustered-index table. Previously, it was always , causing decoding error and panic. What changed and how does it work?
- Fix PR #50048: server: fix decode issue for prefetch point plan index keys (#50037)
  URL: https://github.com/pingcap/tidb/pull/50048
  State: closed
  Merged At: 2024-02-18T08:48:00Z
  Changed Files Count: 3
  Main Modules: pkg/server
  Sample Changed Files:
  - pkg/server/BUILD.bazel
  - pkg/server/conn.go
  - pkg/server/internal/testserverclient/server_client.go
  PR Summary: This is an automated cherry-pick of #50037 What problem does this PR solve? Problem Summary: The second parameter of  indicates whether index KVs belong to a clustered-index table. Previously, it was always , causing decoding error and panic. What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
