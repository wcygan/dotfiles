Begin working on the highest priority task identified by next-steps analysis or start a specific task.

## Usage

```bash
# Start working on the highest priority task from next-steps
/project:start

# Start working on a specific task
/project:start "implement user authentication"

# Start with focus on quick wins
/project:start --quick-wins

# Start but skip certain types of tasks
/project:start --skip=documentation
```

## Arguments

$ARGUMENTS

## Workflow

1. **Task Selection**:
   - If no arguments: Run next-steps analysis and pick the top priority task
   - If task specified: Find and start that specific task
   - If --quick-wins: Focus on tasks marked as "Quick" effort

2. **Pre-work Setup**:
   - Check current git status and branch
   - Set up any required environment
   - Run preliminary tests to ensure clean state
   - Use TodoWrite to track the active task

3. **Execution Process**:
   - Read all relevant files and context
   - Plan the implementation approach
   - Make incremental changes with verification
   - Run tests after each significant change
   - Commit completed work with clear messages

4. **Progress Tracking**:
   - Update task status in TodoWrite
   - Create progress entries if significant milestones reached
   - Note any blockers or issues discovered
   - Track follow-up tasks identified during work

5. **Completion**:
   - Run full test suite
   - Run lint and type checking
   - Stage and commit only modified files
   - Push changes to current branch
   - Mark task as completed in TodoWrite
   - Suggest next task to work on

## Integration with Next-Steps

This command is designed to work seamlessly with `/project:next-steps`:

```bash
# Typical workflow
/project:next-steps              # Analyze what needs to be done
/project:start                    # Begin the top priority task

# Or in one command with specific focus
/project:next-steps "performance"
/project:start "optimize database queries"
```

## Task Selection Priority

When no specific task is given, select based on:

1. **Blockers first**: Tasks blocking other work
2. **High priority**: Critical functionality or bugs
3. **Quick wins**: If --quick-wins flag is set
4. **Dependencies**: Tasks that enable other work
5. **User preference**: If specified in arguments

## Execution Principles

- **Incremental progress**: Make small, verifiable changes
- **Test frequently**: Verify work doesn't break existing functionality
- **Clear commits**: Each commit should have a clear purpose
- **Document decisions**: Note why certain approaches were chosen
- **Leave clean**: Code should be in working state if interrupted

## Exit Conditions

Work stops when:

- Task is completed successfully
- A blocker is encountered that requires user input
- Tests are failing and need investigation
- User interrupts with new instructions

## Example Flow

```bash
# Start working on highest priority task
/project:start

# Output:
Starting task: "Fix authentication token expiry"
- Priority: High
- Estimated effort: Moderate
- Current branch: main
- Running initial tests... ✓

Beginning implementation...
[... work progresses ...]

Task completed successfully!
- 5 files changed
- All tests passing
- 3 commits created
- Changes pushed to main

Suggested next task: "Add token refresh endpoint"
Run /project:start to continue with next task.
```
