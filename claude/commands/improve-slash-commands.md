---
allowed-tools: Task, Read, Write, Edit, Bash(git add:*, git commit:*, deno fmt:*), Glob
description: Systematically improve slash commands with best practices
---

## Context

- Session ID: !`gdate +%s%N`
- Progress file: @notes/improve-slash-commands/progress.json
- Total commands: 159
- Completed count: !`jq .completed notes/improve-slash-commands/progress.json`
- Current command: !`jq -r '.inProgress // "none"' notes/improve-slash-commands/progress.json`
- Next pending: !`jq -r '.commands[] | select(.status == "pending") | .filepath' notes/improve-slash-commands/progress.json | head -1`

## Your task

PROCEDURE improve_next_command():

STEP 1: Load progress state
- IF progress.json doesn't exist:
  - Initialize with all commands from fd scan
- IF no in-progress command exists:
  - Find next pending command
  - Mark as "in-progress" in progress.json
- ELSE:
  - Resume work on in-progress command

STEP 2: Analyze current command
- Read the command file
- Identify current structure
- Determine improvement needs based on best practices:
  * Has proper YAML front matter?
  * Has appropriate allowed-tools?
  * Has concise description?
  * Uses dynamic context (!`command`)?
  * Has programmatic structure?
  * Uses proper state management?

STEP 3: Apply improvements systematically
- Add/update front matter:
  * Extract allowed-tools from command usage patterns
  * Tools to look for: Read, Write, Edit, MultiEdit, Bash, Task, Agent
  * Write concise, action-oriented description
- Add dynamic context section if beneficial:
  * Git commands need: status, diff, branch, log
  * File operations need: directory listings, file checks
  * Analysis commands need: code search, structure discovery
- Restructure task definition:
  * Convert casual language to STEP-based structure
  * Add IF/ELSE for conditional logic
  * Add FOR EACH for iterations
  * Add TRY/CATCH for error-prone operations
- Add state management for complex workflows:
  * Session IDs: !`gdate +%s%N`
  * State files: /tmp/{command}-state-$SESSION_ID.json
  * Checkpoints for resumability

STEP 4: Validate and format
- Ensure YAML front matter is valid
- Verify all bash commands in allowed-tools
- Run: deno fmt {filepath}
- Confirm improvements follow best practices

STEP 5: Commit changes
- Stage: git add {filepath}
- Commit: git commit -m "improve(commands): enhance {command-name} with best practices"

STEP 6: Update progress
- Mark command as "completed" in progress.json
- Record improvements made:
  * frontMatterAdded/Updated
  * dynamicContextAdded
  * programmaticStructureAdded
  * stateManagementAdded
- Update lastModified timestamp
- Increment completed count

STEP 7: Stage and commit progress atomically
- Stage: git add notes/improve-slash-commands/progress.json
- Commit: git commit -m "docs(improve): update progress for {command-name}"

STEP 8: TLDR the diff
- Show concise summary of actual changes made to the command file
- Focus on the key transformations:
  * "Added YAML front matter with tools: X, Y, Z"
  * "Introduced dynamic context for real-time git status"
  * "Converted to STEP-based execution with error handling"
  * "Added session-based state management"
- Example: "Transformed casual instructions → programmatic STEP structure with FOR loops, added !`git status` context injection, implemented /tmp/$SESSION_ID state files"
- IF all completed:
  - Generate final summary report
- ELSE:
  - Show next command: "Next: {next-command-name}"

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
   - Unique session files with nanosecond timestamps
   - Checkpoint capabilities for long operations
   - Clean up temp files in FINALLY blocks

4. **Clear Structure**:
   - STEP-based execution flow
   - Programmatic constructs (IF/ELSE, FOR EACH, TRY/CATCH)
   - No conversational language

5. **Token Efficiency**:
   - Reference files with @ instead of embedding
   - Use precise tools (jq for JSON, rg for search)
   - Batch related operations

## Improvement Patterns

### Pattern 1: Simple Command Enhancement
Before: Casual description of what command does
After: Front matter + structured steps + clear output

### Pattern 2: Git/GitHub Commands
Add context section with:
- Current status: !`git status`
- Recent changes: !`git log --oneline -5`
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