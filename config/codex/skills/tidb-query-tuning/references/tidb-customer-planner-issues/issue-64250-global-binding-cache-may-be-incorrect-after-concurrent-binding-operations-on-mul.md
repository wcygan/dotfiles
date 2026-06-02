# Issue #64250: global binding cache may be incorrect after concurrent binding operations on multiple tidb nodes

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/64250
- Status: closed
- Type: type/bug
- Created At: 2025-11-03T14:54:59Z
- Closed At: 2025-11-07T10:33:16Z
- Labels: affects-7.5, affects-8.5, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- There are fewer than 200 bindings after creating, and some remaining bindings at last.

## Linked PRs
- Fix PR #64289: planner: tolerate reasonable time lag between different TiDB nodes when updating binding cache
  URL: https://github.com/pingcap/tidb/pull/64289
  State: closed
  Merged At: 2025-11-07T10:33:15Z
  Changed Files Count: 4
  Main Modules: pkg/bindinfo
  Sample Changed Files:
  - pkg/bindinfo/BUILD.bazel
  - pkg/bindinfo/binding_cache.go
  - pkg/bindinfo/binding_operator.go
  - pkg/bindinfo/binding_operator_test.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: tolerate reasonable time lag between different TiDB nodes when updating binding cache What changed and how does it work? When updating binding cache, TiDB doesn't consider time lag between different nodes, which could cause inconsistency on binding cache. See more info in #64250. Below is an simplified example, TiDB1's clock is consistent with the real time, while TiDB2's clock is 0.5s slower than the real time:
- Fix PR #64353: planner: tolerate reasonable time lag between different TiDB nodes when updating binding cache (#64289)
  URL: https://github.com/pingcap/tidb/pull/64353
  State: open
  Merged At: not merged
  Changed Files Count: 4
  Main Modules: pkg/bindinfo
  Sample Changed Files:
  - pkg/bindinfo/BUILD.bazel
  - pkg/bindinfo/binding_cache.go
  - pkg/bindinfo/binding_operator.go
  - pkg/bindinfo/binding_operator_test.go
  PR Summary: This is an automated cherry-pick of #64289 What problem does this PR solve? Problem Summary: planner: tolerate reasonable time lag between different TiDB nodes when updating binding cache What changed and how does it work? When updating binding cache, TiDB doesn't consider time lag between different nodes, which could cause inconsistency on binding cache. See more info in #64250.
- Fix PR #64354: planner: tolerate reasonable time lag between different TiDB nodes when updating binding cache (#64289)
  URL: https://github.com/pingcap/tidb/pull/64354
  State: closed
  Merged At: not merged
  Changed Files Count: 4
  Main Modules: pkg/bindinfo
  Sample Changed Files:
  - pkg/bindinfo/BUILD.bazel
  - pkg/bindinfo/binding_cache.go
  - pkg/bindinfo/binding_operator.go
  - pkg/bindinfo/binding_operator_test.go
  PR Summary: This is an automated cherry-pick of #64289 What problem does this PR solve? Problem Summary: planner: tolerate reasonable time lag between different TiDB nodes when updating binding cache What changed and how does it work? When updating binding cache, TiDB doesn't consider time lag between different nodes, which could cause inconsistency on binding cache. See more info in #64250.
- Fix PR #64355: planner: tolerate reasonable time lag between different TiDB nodes when updating binding cache (#64289) 
  URL: https://github.com/pingcap/tidb/pull/64355
  State: closed
  Merged At: 2025-11-10T06:37:08Z
  Changed Files Count: 5
  Main Modules: pkg/bindinfo, pkg/executor, build/nogo_config.json
  Sample Changed Files:
  - build/nogo_config.json
  - pkg/bindinfo/global_handle.go
  - pkg/bindinfo/global_handle_test.go
  - pkg/executor/test/showtest/main_test.go
  - pkg/executor/test/showtest/show_test.go
  PR Summary: This is an automated cherry-pick of #64289 What problem does this PR solve? Problem Summary: planner: tolerate reasonable time lag between different TiDB nodes when updating binding cache What changed and how does it work? When updating binding cache, TiDB doesn't consider time lag between different nodes, which could cause inconsistency on binding cache. See more info in #64250.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
