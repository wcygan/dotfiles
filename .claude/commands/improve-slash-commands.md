---
allowed-tools: Read, Write, Bash(jq:*), Bash(gdate:*), Bash(fd:*), Bash(deno fmt:*), Bash(git add:*), Bash(git commit:*), Bash(git status:*), TodoWrite
description: Systematically improve slash commands one at a time
---

## Context

- Session ID: !`gdate +%s%N`
- Progress file: @notes/improve-slash-commands/progress.json
- Total commands: !`fd '\.md$' claude/commands | wc -l`
- Completed count: !`jq -r '.completed // 0' notes/improve-slash-commands/progress.json 2>/dev/null || echo 0`
- Current command: !`jq -r '.commands[]? | select(.status == "in-progress") | .filepath // "none"' notes/improve-slash-commands/progress.json 2>/dev/null || echo "none"`
- Next pending: !`jq -r '.commands[]? | select(.status == "pending") | .filepath' notes/improve-slash-commands/progress.json 2>/dev/null | head -1 || echo "none"`

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

* Session IDs: !`gdate +%s%N`
* State files: /tmp/{command}-state-$SESSION_ID.json
* Checkpoints for resumability

STEP 4: Validate and format

- Ensure YAML front matter is valid
- Verify all bash commands in allowed-tools
- Run: deno fmt {filepath}
- Confirm improvements follow best practices

STEP 5: Update progress BEFORE committing

- Mark command as "completed" in progress.json
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
   - MANDATORY: Session ID in EVERY command's Context section
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
- [ ] All bash commands tested individually for output
- [ ] Shell quoting issues resolved (no unescaped !, proper quotes)
- [ ] Fallback values provided for all dynamic commands
- [ ] Command file and progress.json staged together
- [ ] Atomic commit includes both files
- [ ] No separate commits for progress tracking

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
