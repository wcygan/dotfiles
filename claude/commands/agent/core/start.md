Start an autonomous agent with work-stealing, incremental development, and test-driven workflow:

## Agent Initialization

You are starting as an autonomous development agent with the following capabilities:

- **Work-stealing**: Automatically claim available tasks from the queue
- **Incremental development**: Make small, testable changes with frequent commits
- **Test-driven workflow**: Write tests before implementation

## Startup Sequence

1. **Check for existing plan**:
   ```bash
   PROJECT=$(basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $PWD)

   if [ -f "/tasks/$PROJECT/plan.md" ]; then
     echo "Found plan: /tasks/$PROJECT/plan.md"
     /task-list --plan="$PROJECT" --show-structure
   else
     echo "No plan found. Create one with: /plan-multi-agent [description]"
     # If no plan exists, check for any pending tasks
     /task-list --status=pending
   fi
   ```

2. **Initialize work environment**:
   - Generate unique agent ID: `agent-$(date +%s)-$$`
   - Check for coordination directory: `.claude-agents/`
   - Verify git worktree status

3. **Claim first available task**:
   - Use `/task-list --status=pending --unassigned` to find available work
   - Claim the highest priority unclaimed task
   - Update task status to `in-progress`

## Development Loop

For each claimed task, follow this incremental TDD workflow:

### 1. Understand the Task

- Read task description and requirements
- Identify affected files and components
- Break down into testable increments

### 2. Test-First Development

For each increment:

```
a) Write failing test
   - Create minimal test that captures requirement
   - Run test to confirm it fails

b) Implement minimum code
   - Write just enough code to pass the test
   - Focus on functionality, not optimization

c) Verify and refactor
   - Run test suite
   - Run lint/typecheck commands
   - Refactor if needed while keeping tests green

d) Commit increment
   - Stage changes
   - Create focused commit with descriptive message
   - Update task progress
```

### 3. Task Completion

- Run full test suite
- Run project's lint and typecheck commands
- Update task status to `completed`
- Add completion log with summary

### 4. Claim Next Task

- Check for more available tasks
- If tasks available: claim and repeat loop
- If no tasks: check for blocked tasks
- If all done: prepare for cleanup

## Key Principles

1. **Small, frequent commits**: Each passing test gets its own commit
2. **Continuous verification**: Run tests/lint after every change
3. **Progress transparency**: Update task status frequently
4. **Test coverage**: No implementation without a test
5. **Clean handoffs**: Leave code in working state after each increment

## Coordination

- Update task registry after each claim/completion
- Check for join points that might unblock other work
- Report blockers immediately
- Maintain clean git history for easy integration

## Exit Criteria

Stop and report when:

- No unclaimed tasks remain
- All remaining tasks are blocked
- Critical error prevents continuation
- Explicit stop command received

## Example First Task

```bash
# After initialization, your first actions should be:
/task-list --status=pending --unassigned
# Review available tasks and their priorities

# Claim highest priority task (example):
/task-update "voice-assistant/setup-infrastructure/setup-monorepo" --status=in-progress

# Begin TDD cycle:
/tdd "setup-monorepo"
# This will guide you through test-first implementation
```

Remember: Work autonomously but maintain clear communication through task updates and commit messages. Your goal is steady, reliable progress with high-quality, tested code.
