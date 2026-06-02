# Issue #60985: TiDB panic when using plan replayer dump with a table using foreign keys

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/60985
- Status: closed
- Type: type/bug
- Created At: 2025-05-07T03:19:32Z
- Closed At: 2025-05-07T09:07:38Z
- Labels: affects-7.5, affects-8.1, affects-8.5, impact/panic, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #60987: domain: fix the issue where defining FKs in a circular manner causes an infinite loop
  URL: https://github.com/pingcap/tidb/pull/60987
  State: closed
  Merged At: 2025-05-07T09:07:37Z
  Changed Files Count: 2
  Main Modules: pkg/domain, pkg/server
  Sample Changed Files:
  - pkg/domain/plan_replayer_dump.go
  - pkg/server/handler/optimizor/plan_replayer_test.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? Foreign keys cannot form a cycle during the table definition phase. However, it is possible to disable FK checks to force a cycle. When traversing the definitions, we need to skip parts that have already been traversed to avoid an infinite loop
- Fix PR #60998: domain: fix the issue where defining FKs in a circular manner causes an infinite loop (#60987)
  URL: https://github.com/pingcap/tidb/pull/60998
  State: closed
  Merged At: 2025-07-08T10:30:12Z
  Changed Files Count: 2
  Main Modules: pkg/domain, pkg/server
  Sample Changed Files:
  - pkg/domain/plan_replayer_dump.go
  - pkg/server/handler/optimizor/plan_replayer_test.go
  PR Summary: This is an automated cherry-pick of #60987 What problem does this PR solve? Problem Summary: What changed and how does it work? Foreign keys cannot form a cycle during the table definition phase. However, it is possible to disable FK checks to force a cycle. When traversing the definitions, we need to skip parts that have already been traversed to avoid an infinite loop
- Fix PR #60999: domain: fix the issue where defining FKs in a circular manner causes an infinite loop (#60987)
  URL: https://github.com/pingcap/tidb/pull/60999
  State: open
  Merged At: not merged
  Changed Files Count: 2
  Main Modules: pkg/domain, pkg/server
  Sample Changed Files:
  - pkg/domain/plan_replayer_dump.go
  - pkg/server/handler/optimizor/plan_replayer_test.go
  PR Summary: This is an automated cherry-pick of #60987 What problem does this PR solve? Problem Summary: What changed and how does it work? Foreign keys cannot form a cycle during the table definition phase. However, it is possible to disable FK checks to force a cycle. When traversing the definitions, we need to skip parts that have already been traversed to avoid an infinite loop
- Fix PR #61000: domain: fix the issue where defining FKs in a circular manner causes an infinite loop (#60987)
  URL: https://github.com/pingcap/tidb/pull/61000
  State: closed
  Merged At: 2025-06-30T04:06:33Z
  Changed Files Count: 2
  Main Modules: pkg/domain, pkg/server
  Sample Changed Files:
  - pkg/domain/plan_replayer_dump.go
  - pkg/server/handler/optimizor/plan_replayer_test.go
  PR Summary: This is an automated cherry-pick of #60987 What problem does this PR solve? Problem Summary: What changed and how does it work? Foreign keys cannot form a cycle during the table definition phase. However, it is possible to disable FK checks to force a cycle. When traversing the definitions, we need to skip parts that have already been traversed to avoid an infinite loop
- Related PR #61028: domain: fix the issue where defining FKs in a circular manner causes …
  URL: https://github.com/pingcap/tidb/pull/61028
  State: closed
  Merged At: not merged
  Changed Files Count: 2
  Main Modules: pkg/domain, pkg/server
  Sample Changed Files:
  - pkg/domain/plan_replayer_dump.go
  - pkg/server/handler/optimizor/plan_replayer_test.go
  PR Summary: …an infinite loop (#60987) close pingcap/tidb#60985 What problem does this PR solve? Problem Summary: What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
