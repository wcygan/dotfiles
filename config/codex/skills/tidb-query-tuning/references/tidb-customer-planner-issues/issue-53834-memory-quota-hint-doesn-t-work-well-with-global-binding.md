# Issue #53834: `memory_quota` hint doesn't work well with global binding

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/53834
- Status: closed
- Type: type/bug
- Created At: 2024-06-05T08:58:17Z
- Closed At: 2024-06-18T11:02:48Z
- Labels: affects-5.4, affects-6.1, affects-6.5, affects-7.1, affects-7.5, affects-8.1, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Start the TiDB cluster: 2. Use sysbench to create a table and insert 100000 rows: 3. Try following SQLs: 4. Try this SQLs with hint:

## Linked PRs
- Fix PR #54048: planner: fix the issue that bindings with query-level hint can not take effect for replace statements
  URL: https://github.com/pingcap/tidb/pull/54048
  State: closed
  Merged At: 2024-06-18T05:19:17Z
  Changed Files Count: 4
  Main Modules: pkg/util, pkg/bindinfo, pkg/planner
  Sample Changed Files:
  - pkg/bindinfo/session_handle_test.go
  - pkg/planner/optimize.go
  - pkg/util/hint/hint.go
  - pkg/util/hint/hint_processor.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: fix the issue that bindings with query-level hint can not take effect for replace statements What changed and how does it work? planner: fix the issue that bindings with query-level hint can not take effect for replace statements
- Fix PR #54083: planner: fix the issue that statement-level hints in sub-queries of Insert/Replace can not take effect
  URL: https://github.com/pingcap/tidb/pull/54083
  State: closed
  Merged At: 2024-06-18T11:02:47Z
  Changed Files Count: 3
  Main Modules: pkg/bindinfo, pkg/session, pkg/util
  Sample Changed Files:
  - pkg/bindinfo/session_handle_test.go
  - pkg/session/test/session_test.go
  - pkg/util/hint/hint_processor.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: fix the issue that statement-level hints in sub-queries of Insert/Replace can not take effect What changed and how does it work?
- Fix PR #54092: planner: fix the issue that bindings with query-level hint can not take effect for replace statements (#54048)
  URL: https://github.com/pingcap/tidb/pull/54092
  State: closed
  Merged At: 2024-06-18T14:55:17Z
  Changed Files Count: 4
  Main Modules: bindinfo/session_handle_test.go, planner/optimize.go, session/session_test, util/hint
  Sample Changed Files:
  - bindinfo/session_handle_test.go
  - planner/optimize.go
  - session/session_test/session_test.go
  - util/hint/hint_processor.go
  PR Summary: This is an automated cherry-pick of #54048 What problem does this PR solve? Problem Summary: planner: fix the issue that bindings with query-level hint can not take effect for replace statements What changed and how does it work? planner: fix the issue that bindings with query-level hint can not take effect for replace statements
- Fix PR #54093: planner: fix the issue that statement-level hints in sub-queries of Insert/Replace can not take effect (#54083)
  URL: https://github.com/pingcap/tidb/pull/54093
  State: closed
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: bindinfo/session_handle_test.go, pkg/session, util/hint
  Sample Changed Files:
  - bindinfo/session_handle_test.go
  - pkg/session/test/session_test.go
  - util/hint/hint_processor.go
  PR Summary: This is an automated cherry-pick of #54083 What problem does this PR solve? Problem Summary: planner: fix the issue that statement-level hints in sub-queries of Insert/Replace can not take effect What changed and how does it work?
- Fix PR #54349: planner: fix the issue that bindings with query-level hint can not take effect for replace statements (#54048)
  URL: https://github.com/pingcap/tidb/pull/54349
  State: closed
  Merged At: 2024-07-15T09:35:59Z
  Changed Files Count: 4
  Main Modules: pkg/bindinfo, pkg/planner, pkg/util
  Sample Changed Files:
  - pkg/bindinfo/BUILD.bazel
  - pkg/bindinfo/session_handle_test.go
  - pkg/planner/optimize.go
  - pkg/util/hint/hint_processor.go
  PR Summary: This is an automated cherry-pick of #54048 What problem does this PR solve? Problem Summary: planner: fix the issue that bindings with query-level hint can not take effect for replace statements What changed and how does it work? planner: fix the issue that bindings with query-level hint can not take effect for replace statements
- Fix PR #54350: planner: fix the issue that statement-level hints in sub-queries of Insert/Replace can not take effect (#54083)
  URL: https://github.com/pingcap/tidb/pull/54350
  State: closed
  Merged At: 2024-07-15T12:17:58Z
  Changed Files Count: 3
  Main Modules: pkg/bindinfo, pkg/session, pkg/util
  Sample Changed Files:
  - pkg/bindinfo/session_handle_test.go
  - pkg/session/test/session_test.go
  - pkg/util/hint/hint_processor.go
  PR Summary: This is an automated cherry-pick of #54083 What problem does this PR solve? Problem Summary: planner: fix the issue that statement-level hints in sub-queries of Insert/Replace can not take effect What changed and how does it work?
- Fix PR #54948: planner: fix the issue that bindings with query-level hint can not take effect for replace statements (#54048)
  URL: https://github.com/pingcap/tidb/pull/54948
  State: closed
  Merged At: 2024-07-31T14:28:28Z
  Changed Files Count: 4
  Main Modules: pkg/util, pkg/bindinfo, pkg/planner
  Sample Changed Files:
  - pkg/bindinfo/session_handle_test.go
  - pkg/planner/optimize.go
  - pkg/util/hint/hint.go
  - pkg/util/hint/hint_processor.go
  PR Summary: This is an automated cherry-pick of #54048 What problem does this PR solve? Problem Summary: planner: fix the issue that bindings with query-level hint can not take effect for replace statements What changed and how does it work? planner: fix the issue that bindings with query-level hint can not take effect for replace statements
- Fix PR #54954: planner: fix the issue that statement-level hints in sub-queries of Insert/Replace can not take effect (#54083)
  URL: https://github.com/pingcap/tidb/pull/54954
  State: closed
  Merged At: 2024-08-01T13:28:20Z
  Changed Files Count: 3
  Main Modules: pkg/bindinfo, pkg/session, pkg/util
  Sample Changed Files:
  - pkg/bindinfo/session_handle_test.go
  - pkg/session/test/session_test.go
  - pkg/util/hint/hint_processor.go
  PR Summary: This is an automated cherry-pick of #54083 What problem does this PR solve? Problem Summary: planner: fix the issue that statement-level hints in sub-queries of Insert/Replace can not take effect What changed and how does it work?
- Fix PR #56894: planner: fix the issue that bindings with query-level hint can not take effect for replace statements (#54048)
  URL: https://github.com/pingcap/tidb/pull/56894
  State: closed
  Merged At: not merged
  Changed Files Count: 4
  Main Modules: bindinfo/session_handle_test.go, pkg/planner, pkg/util, util/hint
  Sample Changed Files:
  - bindinfo/session_handle_test.go
  - pkg/planner/optimize.go
  - pkg/util/hint/hint.go
  - util/hint/hint_processor.go
  PR Summary: This is an automated cherry-pick of #54048 What problem does this PR solve? Problem Summary: planner: fix the issue that bindings with query-level hint can not take effect for replace statements What changed and how does it work? planner: fix the issue that bindings with query-level hint can not take effect for replace statements
- Fix PR #56895: planner: fix the issue that statement-level hints in sub-queries of Insert/Replace can not take effect (#54083)
  URL: https://github.com/pingcap/tidb/pull/56895
  State: closed
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: bindinfo/session_handle_test.go, pkg/session, util/hint
  Sample Changed Files:
  - bindinfo/session_handle_test.go
  - pkg/session/test/session_test.go
  - util/hint/hint_processor.go
  PR Summary: This is an automated cherry-pick of #54083 What problem does this PR solve? Problem Summary: planner: fix the issue that statement-level hints in sub-queries of Insert/Replace can not take effect What changed and how does it work?
- Fix PR #57240: planner: fix the issue that bindings with query-level hint can not take effect for replace statements (#54048)
  URL: https://github.com/pingcap/tidb/pull/57240
  State: closed
  Merged At: 2024-11-08T11:13:38Z
  Changed Files Count: 4
  Main Modules: bindinfo/session_handle_test.go, planner/optimize.go, session/sessiontest, util/hint
  Sample Changed Files:
  - bindinfo/session_handle_test.go
  - planner/optimize.go
  - session/sessiontest/session_test.go
  - util/hint/hint_processor.go
  PR Summary: This is an automated cherry-pick of #54048 What problem does this PR solve? Problem Summary: planner: fix the issue that bindings with query-level hint can not take effect for replace statements What changed and how does it work? planner: fix the issue that bindings with query-level hint can not take effect for replace statements

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
