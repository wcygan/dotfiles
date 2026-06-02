# Issue #58016: planner: TiDB server can't start due to loading binding panic

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/58016
- Status: closed
- Type: type/bug
- Created At: 2024-12-05T11:45:15Z
- Closed At: 2024-12-05T13:57:49Z
- Labels: affects-4.0, affects-5.4, affects-6.1, affects-6.5, affects-7.1, affects-7.5, affects-8.1, affects-8.5, epic/sql-plan-management, impact/panic, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- It can't restart. Since when starting, TiDB has to load all bindings into memory, but TiDB has no protective measure for panic, which causes TiDB to be unable to restart successfully.

## Linked PRs
- Fix PR #58017: planner: handle panic when loading bindings at startup
  URL: https://github.com/pingcap/tidb/pull/58017
  State: closed
  Merged At: 2024-12-05T13:57:47Z
  Changed Files Count: 2
  Main Modules: pkg/bindinfo
  Sample Changed Files:
  - pkg/bindinfo/BUILD.bazel
  - pkg/bindinfo/binding.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: handle panic when loading bindings at startup What changed and how does it work? planner: handle panic when loading bindings at startup
- Fix PR #58035: planner: handle panic when loading bindings at startup (#58017)
  URL: https://github.com/pingcap/tidb/pull/58035
  State: closed
  Merged At: 2024-12-09T07:41:06Z
  Changed Files Count: 2
  Main Modules: pkg/bindinfo
  Sample Changed Files:
  - pkg/bindinfo/BUILD.bazel
  - pkg/bindinfo/binding.go
  PR Summary: This is an automated cherry-pick of #58017 What problem does this PR solve? Problem Summary: planner: handle panic when loading bindings at startup What changed and how does it work? planner: handle panic when loading bindings at startup
- Fix PR #58169: planner: handle panic when loading bindings at startup (#58017)
  URL: https://github.com/pingcap/tidb/pull/58169
  State: closed
  Merged At: 2024-12-12T11:55:07Z
  Changed Files Count: 2
  Main Modules: pkg/bindinfo
  Sample Changed Files:
  - pkg/bindinfo/BUILD.bazel
  - pkg/bindinfo/bind_record.go
  PR Summary: This is an automated cherry-pick of #58017 What problem does this PR solve? Problem Summary: planner: handle panic when loading bindings at startup What changed and how does it work? planner: handle panic when loading bindings at startup
- Fix PR #58170: planner: handle panic when loading bindings at startup (#58017)
  URL: https://github.com/pingcap/tidb/pull/58170
  State: open
  Merged At: not merged
  Changed Files Count: 2
  Main Modules: pkg/bindinfo
  Sample Changed Files:
  - pkg/bindinfo/BUILD.bazel
  - pkg/bindinfo/binding.go
  PR Summary: This is an automated cherry-pick of #58017 What problem does this PR solve? Problem Summary: planner: handle panic when loading bindings at startup What changed and how does it work? planner: handle panic when loading bindings at startup
- Fix PR #59062: planner: handle panic when loading bindings at startup (#58017)
  URL: https://github.com/pingcap/tidb/pull/59062
  State: closed
  Merged At: 2025-02-08T07:38:55Z
  Changed Files Count: 3
  Main Modules: .bazelversion, bindinfo/BUILD.bazel, bindinfo/bind_record.go
  Sample Changed Files:
  - .bazelversion
  - bindinfo/BUILD.bazel
  - bindinfo/bind_record.go
  PR Summary: This is an automated cherry-pick of #58017 What problem does this PR solve? Problem Summary: planner: handle panic when loading bindings at startup What changed and how does it work? planner: handle panic when loading bindings at startup

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
