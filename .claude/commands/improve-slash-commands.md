---
allowed-tools: Read, Write, Bash(jq:*), Bash(gdate:*), Bash(fd:*), Bash(deno fmt:*), Bash(git add:*), Bash(git commit:*), Bash(git status:*), TodoWrite
description: Systematically improve slash commands one at a time
---

## Context

- Session ID: !`gdate +%s%N`
- Progress file: @notes/improve-slash-commands/progress.json
- Total commands: !`fd '\.md$' claude/commands | wc -l`
- Completed count: !`jq -r '.completed // 0' notes/improve-slash-commands/progress.json 2>/dev/null || echo 0`
- In-progress count: !`jq -r '[.commands[]? | select(.status == "in-progress")] | length' notes/improve-slash-commands/progress.json 2>/dev/null || echo 0`
- My claimed command: !`jq -r --arg sid "$(gdate +%s%N)" '.commands[]? | select(.status == "in-progress" and .claimedBy.sessionId == $sid) | .filepath // "none"' notes/improve-slash-commands/progress.json 2>/dev/null || echo "none"`
- Next pending: !`jq -r '.commands[]? | select(.status == "pending") | .filepath' notes/improve-slash-commands/progress.json 2>/dev/null | head -1 || echo "none"`
- Stale claims (>10min): !`jq -r --arg now "$(gdate -u +%s)" '[.commands[]? | select(.status == "in-progress" and (($now | tonumber) - (.claimedBy.timestamp // 0 | tonumber) > 600))] | length' notes/improve-slash-commands/progress.json 2>/dev/null || echo 0`

## Your task

PROCEDURE improve_next_command():

STEP 1: Claim a task atomically

- Load current progress.json state
- Check for MY existing claim (sessionId matches):
  - IF I have an existing claim: Resume work on that command
  - ELSE: Proceed to claim a new task

- Find claimable commands:
  - Pending commands (status == "pending")
  - Stale claims (status == "in-progress" AND timestamp > 10 minutes old)

- IF no claimable commands exist:
  - Report "All commands are being worked on or completed"
  - Exit gracefully

- IMMEDIATELY claim the first available command:
  - Read current progress.json
  - Update the selected command entry with:
    ```json
    {
      "status": "in-progress",
      "claimedBy": {
        "sessionId": "<session-id-from-context>",
        "timestamp": <unix-timestamp-seconds>
      },
      "lastModified": "<ISO-8601-timestamp>"
    }
    ```
  - Write updated progress.json atomically
  - Verify claim was successful by re-reading
  - IF claim failed (someone else claimed it): Try next available command

STEP 2: Analyze current command

- Read the command file
- Identify current structure
- FOR complex commands: Use "think hard" to deeply analyze optimization opportunities
- Determine improvement needs based on best practices:

* Has proper YAML front matter?
* Has appropriate allowed-tools?
* Has concise description?
* Uses dynamic context (!`command`)?
* Has programmatic structure?
* Uses proper state management?
* Could benefit from extended thinking capabilities?

STEP 3: Apply improvements systematically

- Add/update front matter:

* Extract allowed-tools from command usage patterns
* Tools to look for: Read, Write, Edit, MultiEdit, Bash, Task, Agent
* Write concise, action-oriented description

- Add dynamic context section if beneficial:

* CRITICAL: Include Session ID: !`gdate +%s%N` for EVERY command
* Git commands need: status, diff, branch, log
* File operations need: directory listings, file checks
* Analysis commands need: code search, structure discovery

- Test ALL bash commands in Context section:

* Test each command individually for compatibility
* Handle shell quoting issues (avoid != in jq, proper escaping)
* Provide fallback values: !`command || echo "fallback"`
* Verify proper output before including

- Restructure task definition:

* Convert casual language to STEP-based structure
* Add IF/ELSE for conditional logic
* Add FOR EACH for iterations
* Add TRY/CATCH for error-prone operations

- Add state management for complex workflows:

* Session IDs: !`gdate +%s%N` (NEVER hard-code - always use dynamic generation)
* State files: /tmp/{command}-state-!`gdate +%s%N`.json
* Checkpoints for resumability

STEP 4: Validate and format

- Ensure YAML front matter is valid
- Verify all bash commands in allowed-tools
- Run: deno fmt {filepath}
- Confirm improvements follow best practices

STEP 5: Update progress BEFORE committing

- Mark command as "completed" in progress.json
- Clear the claimedBy field (set to null)
- Record improvements made:

* frontMatterAdded/Updated
* dynamicContextAdded
* programmaticStructureAdded
* stateManagementAdded

- Update lastModified timestamp
- Increment completed count

STEP 6: ATOMIC commit of both files

- CRITICAL: Stage BOTH command file AND progress.json together
- git add {filepath} notes/improve-slash-commands/progress.json
- git commit -m "improve(commands): enhance {command-name} with best practices"
- NEVER commit these files separately

STEP 7: Report status

- Show: "✓ Improved {command-name} ({completed}/{total} completed)"
- Display key improvements made
- Show parallel work status:
  - "Currently {in-progress-count} commands being worked on by other agents"
  - "Session ID: {session-id}"
- IF all completed:
  - Generate final summary report
  - Display comprehensive TLDR
- ELSE:
  - Show next command: "Next: {next-command-name}"
  - Display session TLDR

STEP 8: TLDR the diff

- Show concise summary of actual changes made to the command file
- Focus on the key transformations:
  - "Added YAML front matter with tools: X, Y, Z"
  - "Introduced dynamic context for real-time git status"
  - "Converted to STEP-based execution with error handling"
  - "Added session-based state management"
- Example: "Transformed casual instructions → programmatic STEP structure with FOR loops, added !`git status` context injection, implemented /tmp/$SESSION_ID state files"

## Best Practices Reference

1. **Security First**:
   - Minimal allowed-tools (only what's actually used)
   - Read-only commands for context gathering
   - Never allow dangerous operations without constraints

2. **Deterministic Behavior**:
   - Same inputs must produce same outputs
   - Avoid randomness or ambiguous instructions
   - Use explicit control flow

3. **State Management**:
   - MANDATORY: Session ID in EVERY command's Context section using !`gdate +%s%N`
   - **NEVER hard-code session IDs** - always use dynamic bash commands
   - Unique session files with nanosecond timestamps
   - Checkpoint capabilities for long operations
   - Clean up temp files in FINALLY blocks

4. **Clear Structure**:
   - STEP-based execution flow
   - Programmatic constructs (IF/ELSE, FOR EACH, TRY/CATCH)
   - No conversational language

5. **Token Efficiency**:
   - Reference files with @ instead of embedding
   - Use precise tools (jq for JSON, rg for search, fd for file finding)
   - Batch related operations

6. **Testing Requirements**:
   - Test EVERY bash command before including in Context
   - Handle shell quoting and special characters properly
   - Always provide fallback values for commands that might fail
   - Verify output format matches expectations

7. **Atomic Commits**:
   - ALWAYS commit command file and progress.json together
   - Never split progress tracking from actual changes
   - Ensures consistency and rollback safety

## Extended Thinking for Command Optimization

### When to Use Extended Thinking

Use "think hard" or deeper thinking modes when improving commands that involve:

1. **Complex Logic Flow**:
   - Multi-phase workflows with dependencies
   - State machines with multiple transitions
   - Nested conditional logic requiring careful analysis

2. **Architecture Decisions**:
   - Choosing between sub-agent vs sequential execution
   - Designing optimal state management strategies
   - Determining appropriate error handling patterns

3. **Performance Optimization**:
   - Analyzing token usage patterns
   - Identifying opportunities for parallel execution
   - Optimizing context window usage

4. **Security Analysis**:
   - Evaluating allowed-tools permissions
   - Identifying potential security vulnerabilities
   - Designing safe command patterns

### How to Apply Extended Thinking

- Add thinking triggers in command descriptions:
  ```yaml
  description: Complex analysis requiring deep architectural thinking
  ```

- Include thinking prompts in task definitions:
  ```markdown
  ## Your task

  Think deeply about the optimal approach for this multi-phase workflow.
  Consider performance, security, and maintainability tradeoffs.
  ```

- For analysis commands, suggest thinking intensifiers:
  ```markdown
  STEP 1: Initial analysis

  - think hard about potential edge cases
  - think harder about security implications
  ```

### Extended Thinking Patterns

1. **Research Commands** - Enable deeper analysis:
   ```markdown
   Use extended thinking to thoroughly explore all aspects of $ARGUMENTS
   ```

2. **Debugging Commands** - Complex problem solving:
   ```markdown
   Think deeply about root causes and systematic debugging approaches
   ```

3. **Architecture Commands** - Design decisions:
   ```markdown
   Think harder about system design tradeoffs and long-term maintainability
   ```

## Improvement Patterns

### Pattern 1: Simple Command Enhancement

Before: Casual description of what command does
After: Front matter + structured steps + clear output

### Pattern 2: Git/GitHub Commands

Add context section with:

- Current status: !`git status`
- Recent changes: !`git diff HEAD`
- Branch info: !`git branch --show-current`

### Pattern 3: Code Generation Commands

Add:

- Framework detection logic
- Template selection based on context
- Validation steps

### Pattern 4: Analysis Commands

Consider adding sub-agent delegation for:

- Large-scale code analysis
- Multi-aspect exploration
- Parallel research tasks

### Pattern 5: Long-Running Operations

Add state management:

- Checkpoint after each major step
- Resume capability from checkpoints
- Progress tracking in state file

## Critical Testing Checklist

Before marking ANY command as improved:

- [ ] Session ID included in Context section: !`gdate +%s%N`
- [ ] **CRITICAL**: Session ID uses !`gdate +%s%N` - NEVER hard-code session IDs
- [ ] All bash commands tested individually for output
- [ ] Shell quoting issues resolved (no unescaped !, proper quotes)
- [ ] Fallback values provided for all dynamic commands
- [ ] Command file and progress.json staged together
- [ ] Atomic commit includes both files
- [ ] No separate commits for progress tracking
- [ ] Extended thinking considered for complex commands

### Common Bash Command Issues to Test

1. **jq expressions**: Avoid != operator, use proper escaping
2. **Git commands**: Test with actual repository state
3. **kubectl/docker**: Handle connection failures gracefully
4. **File operations**: Provide defaults for missing files
5. **Command substitution**: Watch for special characters

Example safe pattern:

```bash
!`command 2>/dev/null || echo "default value"`
```

## Concurrent Execution Pattern

### Enabling Parallel Agent Work

This command supports multiple agents working in parallel on different commands:

1. **Launch Multiple Sessions**:
   ```bash
   # Terminal 1
   claude code
   > /improve-slash-commands

   # Terminal 2
   claude code
   > /improve-slash-commands

   # Terminal 3
   claude code
   > /improve-slash-commands
   ```

2. **Automatic Task Distribution**:
   - Each agent claims tasks atomically at startup
   - No two agents will work on the same command
   - Agents automatically skip already-claimed tasks
   - Session IDs ensure unique identification

3. **Stale Claim Recovery**:
   - If an agent crashes or disconnects
   - Claims older than 10 minutes are considered stale
   - Other agents can reclaim stale tasks automatically

4. **Progress Tracking**:
   - Context section shows in-progress count
   - Each agent sees which commands are being worked on
   - Completed count updates in real-time

### Coordination Best Practices

- **Atomic Commits**: Each agent commits their command file + progress.json together
- **No Manual Coordination**: The claiming mechanism handles all coordination
- **Graceful Completion**: Agents exit when no more tasks are available
- **Progress Visibility**: Use `jq '.commands[] | select(.status == "in-progress")' notes/improve-slash-commands/progress.json` to see active work

### Example Progress.json Entry with Claim

```json
{
  "id": "042",
  "name": "generate-unit-tests",
  "filepath": "claude/commands/test/generate/generate-unit-tests.md",
  "namespace": "test/generate",
  "status": "in-progress",
  "claimedBy": {
    "sessionId": "1751703298807183000",
    "timestamp": 1751703298
  },
  "lastModified": "2025-07-05T15:30:00Z"
}
```
