---
description: Execute tasks incrementally with tests, ensuring perpetually green builds
---

Execute the current task using incremental development methodology with continuous testing.

**CORE PRINCIPLE: Every step must leave the codebase in a working, tested state.**

## Incremental Execution Loop

For each feature/task, follow this cycle:

1. **Verify green build** - Run existing tests to confirm starting point
2. **Implement smallest next increment** - One function, one endpoint, one behavior
3. **Write test for new code** - Lock down the new behavior immediately
4. **Run new test** - Verify it passes (fix code if needed)
5. **Run full test suite** - Ensure nothing broke
6. **Commit atomically** - One logical change + its tests
7. **Repeat** - Move to next increment

## When Faced with Multiple Tasks

**NEVER attempt multiple tasks in parallel.**

Instead:
1. **Choose ONE task** from the list
2. **Complete it fully** (implement + test + verify)
3. **Commit the completed task**
4. **Move to next task**

Example:
- ✅ Implement Task 2.1 (REST API) → test → commit
- ✅ Then implement Task 2.2 (WebSocket) → test → commit
- ✅ Then implement Task 2.3 (PubSub) → test → commit

**NOT:**
- ❌ Start all three tasks at once
- ❌ Write all code then add tests
- ❌ Commit without green builds

## Task Breakdown Strategy

If a task feels too large, break it down further:

**Example: "REST API for rooms"**
1. Create route handler stub + test for 404
2. Implement `POST /rooms` + test for successful creation
3. Add JWT validation middleware + test for auth failure
4. Implement `GET /rooms` + test for listing
5. Add error cases + tests

Each step = working code + passing tests + commit.

## Execution Checklist

Before starting:
- [ ] Current test suite is green
- [ ] Task is small enough (if not, break down)
- [ ] You know what test to write first

For each increment:
- [ ] Implement minimal code
- [ ] Write test(s) for new code
- [ ] New test passes
- [ ] Full test suite passes
- [ ] Code formatted/linted
- [ ] Ready to commit

After completing task:
- [ ] All tests green
- [ ] Feature fully tested
- [ ] Committed atomically
- [ ] Ready for next task

## Test-First Mindset

**Always write the test that would fail without your code, then make it pass.**

```
1. Write test → RED (test fails, feature doesn't exist)
2. Implement feature → GREEN (test passes)
3. Verify suite → GREEN (nothing broke)
4. Commit
```

## Emergency Recovery

If you find yourself with:
- Failing tests you can't fix quickly
- Multiple half-finished features
- Uncommitted changes spanning multiple tasks

**STOP. Rollback to last green commit and restart incrementally.**

## Output Format

When executing incrementally, report:

```
🔍 Current state: [test status]
📋 Selected task: [specific task from list]
✏️  Implementing: [specific increment]
🧪 Writing test: [test description]
✅ Test result: [pass/fail]
🏃 Full suite: [pass/fail]
💾 Commit: [commit message]
```

## Remember

- **Small steps are fast steps** - Less debugging, faster progress
- **Tests make progress permanent** - Can't accidentally break working code
- **Green builds enable confidence** - Always safe to deploy/share
- **Atomic commits enable rollback** - Easy to undo if needed

**Never commit unless: tests pass, code formatted, change is atomic.**
