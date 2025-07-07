---
allowed-tools: Read, Write, Edit, Bash(deno run:*), Bash(git add:*), Bash(git commit:*), Bash(git status:*), TodoWrite
description: Systematically improve slash commands using robust task management
---

## Context

- Session ID: !`gdate +%s%N`
- Task status: !`deno run --allow-read --allow-write notes/improve-slash-commands/task-manager.ts status`
- Claim result: !`deno run --allow-read --allow-write notes/improve-slash-commands/task-manager.ts claim`

## Your task

PROCEDURE improve_next_command():

STEP 1: Process claimed task from Context

IF Claim result contains "No claimable commands available":

- Report "✅ All commands completed or actively being worked on by other agents"
- EXIT gracefully

ELSE:

- Extract COMMAND_ID and SESSION_ID from Claim result output
- Extract FILEPATH from Claim result output
- Continue to STEP 2 with claimed command

STEP 2: Analyze current command

- Read the command file at FILEPATH
- Extract COMMAND_ID and SESSION_ID from Claim result for later use
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

STEP 5: Mark task as completed using task manager

- Create improvement list based on changes made:
  - frontMatterAdded/Updated
  - dynamicContextAdded
  - programmaticStructureAdded
  - stateManagementAdded
  - extendedThinkingAdded
  - subAgentPatternsAdded

- COMPLETE_RESULT: !`deno run --allow-read --allow-write notes/improve-slash-commands/task-manager.ts complete --command-id COMMAND_ID --session-id SESSION_ID --improvement frontMatterAdded --improvement dynamicContextAdded`

IF COMPLETE_RESULT indicates failure:

- Report error and EXIT gracefully

STEP 6: ATOMIC commit of both files

- CRITICAL: Stage BOTH command file AND progress.json together
- git add FILEPATH notes/improve-slash-commands/progress.json
- git commit -m "improve(commands): enhance {command-name} with best practices"
- NEVER commit these files separately

STEP 7: Report completion status

- Show: "✅ Improved {command-name} ({completed}/{total} completed)"
- Display key improvements made in this session
- Show coordination status:
  - "📊 Available commands: {available-count}"
  - "🔄 Commands in-progress by other agents: {in-progress-count}"
  - "🎯 Session: {session-id} (single command focus)"
- IF all completed:
  - Generate final summary report: "🎉 All 159 commands improved!"
  - Display comprehensive workflow TLDR
  - Show improvement statistics from progress.json
- ELSE:
  - Show graceful completion: "✅ Single command improved - workflow ready for next agent"
  - Display session summary
  - Note: "Other agents can continue with remaining {available-count} commands"

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

### Deno-Based Task Management System

This command now uses a robust Deno-based task management system for safe parallel execution:

1. **Launch Multiple Sessions** (each works on exactly one command):
   ```bash
   # Terminal 1
   claude code
   > /improve-slash-commands
   # Claims command 029, works on it, completes it, exits

   # Terminal 2  
   claude code
   > /improve-slash-commands
   # Claims command 030, works on it, completes it, exits

   # Terminal 3
   claude code
   > /improve-slash-commands  
   # Claims command 031, works on it, completes it, exits
   ```

2. **True Atomic Claiming**:
   - File-based locking using Deno's exclusive write operations
   - Each agent claims exactly ONE command per session
   - Conflict detection ensures no double-claiming
   - Automatic cleanup of stale claims (>10 minutes)

3. **Robust Task Manager Features**:
   - Claims older than 10 minutes automatically become reclaimable
   - Graceful handling of crashed or disconnected agents
   - Comprehensive error handling and validation
   - Status reporting and progress tracking

4. **Task Manager Commands**:
   ```bash
   # Claim next available task
   deno run --allow-read --allow-write task-manager.ts claim

   # Mark task as completed
   deno run --allow-read --allow-write task-manager.ts complete \
     --command-id ID --session-id SESSION \
     --improvement frontMatterAdded --improvement dynamicContextAdded

   # Check status
   deno run --allow-read --allow-write task-manager.ts status

   # Clean up stale claims
   deno run --allow-read --allow-write task-manager.ts cleanup
   ```

### Coordination Best Practices

- **Single Command Focus**: Each agent works on exactly one command per session
- **Atomic Operations**: File-based locking prevents race conditions and conflicts
- **Graceful Exits**: Agents exit cleanly when no claimable commands exist
- **Conflict Resilience**: Failed claims result in clean exit, not retry loops
- **Progress Visibility**: Real-time status through task manager
- **No Coordination Overhead**: Zero manual coordination required between agents

### Example Progress.json Entry with Claim

```json
{
  "id": "042",
  "name": "generate-unit-tests",
  "filepath": "claude/commands/test/generate/generate-unit-tests.md",
  "namespace": "test/generate",
  "status": "in-progress",
  "claimedBy": {
    "sessionId": "17517032988071830001a2b3c",
    "timestamp": 1751703298
  },
  "lastModified": "2025-07-05T15:30:00Z"
}
```
