# Issue #65489: Memory leak when `analyze table` is the last statement in a session

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/65489
- Status: closed
- Type: type/bug
- Created At: 2026-01-08T12:17:48Z
- Closed At: 2026-01-09T22:24:42Z
- Labels: affects-7.5, affects-8.1, affects-8.5, component/statistics, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- About 1GiB memory in .

## Linked PRs
- Fix PR #65492: session: fix memory leak when sessions close after ANALYZE statements
  URL: https://github.com/pingcap/tidb/pull/65492
  State: closed
  Merged At: 2026-01-09T22:24:41Z
  Changed Files Count: 3
  Main Modules: pkg/executor, pkg/session
  Sample Changed Files:
  - pkg/executor/test/analyzetest/memorycontrol/BUILD.bazel
  - pkg/executor/test/analyzetest/memorycontrol/memory_control_test.go
  - pkg/session/session.go
  PR Summary: What problem does this PR solve? Problem Summary: Short-lived sessions executing ANALYZE statements leak ~1GiB memory in  after 20k iterations. When ANALYZE statements are executed, the session's  is attached to . For sessions that close immediately after ANALYZE (common in connection pooling), the tracker remains attached, preventing garbage collection. What changed and how does it work? ANALYZE has a special memory tracking path where  is called.  keeps strong references to its children. When a session closes immediately after ANALYZE, the session-level  is not detached, so the global tracker retains the session, keeping  alive. **Changes:**
- Fix PR #65516: session: fix memory leak when sessions close after ANALYZE statements (#65492)
  URL: https://github.com/pingcap/tidb/pull/65516
  State: closed
  Merged At: 2026-01-13T01:50:14Z
  Changed Files Count: 3
  Main Modules: pkg/executor, pkg/session
  Sample Changed Files:
  - pkg/executor/test/analyzetest/memorycontrol/BUILD.bazel
  - pkg/executor/test/analyzetest/memorycontrol/memory_control_test.go
  - pkg/session/session.go
  PR Summary: This is an automated cherry-pick of #65492 What problem does this PR solve? Problem Summary: Short-lived sessions executing ANALYZE statements leak ~1GiB memory in  after 20k iterations. When ANALYZE statements are executed, the session's  is attached to . For sessions that close immediately after ANALYZE (common in connection pooling), the tracker remains attached, preventing garbage collection. What changed and how does it work? ANALYZE has a special memory tracking path where  is called.  keeps strong references to its children. When a session closes immediately after ANALYZE, the session-level  is not detached, so the global tracker retains the session, keeping  alive.
- Fix PR #65539: session: fix memory leak when sessions close after ANALYZE statements (#65492)  | tidb-test=86a1cff755f507d127f0bca7ff18e2f3b9537124
  URL: https://github.com/pingcap/tidb/pull/65539
  State: closed
  Merged At: 2026-01-13T05:25:26Z
  Changed Files Count: 3
  Main Modules: pkg/executor, pkg/session
  Sample Changed Files:
  - pkg/executor/test/analyzetest/memorycontrol/BUILD.bazel
  - pkg/executor/test/analyzetest/memorycontrol/memory_control_test.go
  - pkg/session/session.go
  PR Summary: This is an automated cherry-pick of #65492 What problem does this PR solve? Problem Summary: Short-lived sessions executing ANALYZE statements leak ~1GiB memory in  after 20k iterations. When ANALYZE statements are executed, the session's  is attached to . For sessions that close immediately after ANALYZE (common in connection pooling), the tracker remains attached, preventing garbage collection. What changed and how does it work? ANALYZE has a special memory tracking path where  is called.  keeps strong references to its children. When a session closes immediately after ANALYZE, the session-level  is not detached, so the global tracker retains the session, keeping  alive.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
