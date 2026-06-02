# Issue #50068: planner: set_var cannot take effect in UNION ALL statements

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/50068
- Status: closed
- Type: type/bug
- Created At: 2024-01-04T05:58:51Z
- Closed At: 2024-01-04T14:00:35Z
- Labels: affects-6.5, affects-7.1, affects-7.5, epic/hint, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- The second query's execution time exceeds the limitation. The reason is that UNION ALL's node is not considered when extracting statement hints: ![img_v3_026p_32b954e0-92b3-4a15-8aac-c847fca3026g]()

## Linked PRs
- Fix PR #50070: bindinfo: extract the table hint from the union statement
  URL: https://github.com/pingcap/tidb/pull/50070
  State: closed
  Merged At: 2024-01-04T14:00:34Z
  Changed Files Count: 2
  Main Modules: pkg/server, pkg/util
  Sample Changed Files:
  - pkg/server/conn_test.go
  - pkg/util/hint/hint_processor.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #50095: bindinfo: extract the table hint from the union statement (#50070)
  URL: https://github.com/pingcap/tidb/pull/50095
  State: closed
  Merged At: 2024-01-23T07:19:50Z
  Changed Files Count: 2
  Main Modules: server/conn_test.go, util/hint
  Sample Changed Files:
  - server/conn_test.go
  - util/hint/hint_processor.go
  PR Summary: This is an automated cherry-pick of #50070 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #50096: bindinfo: extract the table hint from the union statement (#50070)
  URL: https://github.com/pingcap/tidb/pull/50096
  State: closed
  Merged At: 2024-01-05T07:20:04Z
  Changed Files Count: 2
  Main Modules: pkg/server, pkg/util
  Sample Changed Files:
  - pkg/server/conn_test.go
  - pkg/util/hint/hint_processor.go
  PR Summary: This is an automated cherry-pick of #50070 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #50097: bindinfo: extract the table hint from the union statement (#50070)
  URL: https://github.com/pingcap/tidb/pull/50097
  State: closed
  Merged At: 2024-01-23T07:15:21Z
  Changed Files Count: 2
  Main Modules: server/conn_test.go, util/hint
  Sample Changed Files:
  - server/conn_test.go
  - util/hint/hint_processor.go
  PR Summary: This is an automated cherry-pick of #50070 What problem does this PR solve? Problem Summary: What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
