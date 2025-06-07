Initialize an agent identity for the current Claude session and load assigned tasks:

## Usage

```bash
/agent-init [agent-id] [options]
```

## Examples

```bash
# Initialize as agent-a
/agent-init agent-a

# Initialize with custom name
/agent-init agent-b --name="claude-features"

# Initialize and show immediate tasks
/agent-init agent-c --show-tasks

# Re-initialize (switch agent identity)
/agent-init agent-d --force
```

## Initialization Process

1. **Set Agent Identity**:
   ```bash
   # Create agent identity file
   echo "agent-a" > .claude-agent

   # Set environment context
   export CLAUDE_AGENT_ID="agent-a"
   export CLAUDE_AGENT_NAME="claude-foundation"
   ```

2. **Load Agent Configuration**:
   ```json
   // From /tasks/[project]/agents/agent-a.json
   {
     "agentId": "agent-a",
     "name": "claude-foundation",
     "worktree": "../project-foundation",
     "branch": "feature/setup-foundation",
     "assignedTasks": [
       "project/setup-foundation/project-structure",
       "project/setup-foundation/dependency-setup"
     ],
     "startTime": "2025-01-07T10:00:00Z"
   }
   ```

3. **Verify Worktree Context**:
   ```bash
   # Confirm in correct worktree
   CURRENT_WORKTREE=$(git rev-parse --show-toplevel)
   EXPECTED_WORKTREE=$(realpath "../project-foundation")

   if [ "$CURRENT_WORKTREE" != "$EXPECTED_WORKTREE" ]; then
     echo "Warning: Not in expected worktree"
     echo "Expected: $EXPECTED_WORKTREE"
     echo "Current: $CURRENT_WORKTREE"
   fi
   ```

4. **Load Assigned Tasks**:
   ```bash
   # Automatically populate TodoWrite with assigned tasks
   TASKS=$(jq -r '.assignedTasks[]' /tasks/project/agents/agent-a.json)

   # Convert to TodoWrite format and load
   for TASK in $TASKS; do
     /task-to-todo "$TASK"
   done
   ```

5. **Display Initialization Summary**:

   ```
   Agent Initialized Successfully
   ═══════════════════════════════════════════

   Agent ID: agent-a
   Name: claude-foundation
   Worktree: ../project-foundation
   Branch: feature/setup-foundation

   ## Assigned Tasks (2)

   1. setup-foundation/project-structure
      Status: pending
      Priority: high
      Can start: immediately

   2. setup-foundation/dependency-setup  
      Status: pending
      Priority: high
      Can start: immediately

   ## Your Impact

   You block:
   - testing-suite/* (agent-c)

   You depend on:
   - None (can start all tasks)

   ## Quick Commands

   View your tasks: /task-list --mine
   Start a task: /task-update "[task]" --status=in-progress
   Check status: /agent-status

   Ready to begin! Use /task-list --mine to see your work.
   ```

## Advanced Features

### Dependency Checking

```bash
/agent-init agent-c --check-dependencies

# Output:
# Checking dependencies for agent-c...
# 
# ⚠️  Warning: Your tasks have unmet dependencies
# 
# testing-suite/unit-tests depends on:
# - setup-foundation/* (agent-a) - 50% complete
# - core-features/* (agent-b) - 30% complete
#
# You can monitor progress with: /agent-status --show-dependencies
```

### Task Preloading

```bash
/agent-init agent-a --preload-tasks

# This will:
# 1. Load all assigned tasks into TodoWrite
# 2. Set first available task as "next up"
# 3. Prepare any task-specific context
# 4. Check for recent updates from other agents
```

### Session Recovery

```bash
/agent-init --recover

# Detects previous agent session and:
# 1. Restores agent identity
# 2. Reloads in-progress tasks
# 3. Shows what changed since last session
# 4. Resumes where you left off
```

## Configuration Options

### Custom Agent Names

```bash
/agent-init agent-prod-1 --name="Production Deployment Agent"
```

### Temporary Agents

```bash
/agent-init agent-temp-fix --temporary
# No permanent files created
# Useful for hotfixes or quick tasks
```

### Read-Only Mode

```bash
/agent-init agent-reviewer --read-only
# Can view but not modify tasks
# Useful for code review agents
```

## Integration with Other Commands

After initialization:

- `/task-list --mine` - Shows only your assigned tasks
- `/task-update` - Automatically tags updates with agent ID
- `/agent-status` - Shows your specific status
- `/commit` - Includes agent ID in commit metadata

## Error Handling

### Already Initialized

```
Error: Agent already initialized as agent-b
Use --force to switch to agent-a
Warning: This will clear current agent context
```

### No Assignments

```
Warning: No tasks assigned to agent-d
Use /agent-assign to assign tasks
Or use /task-list --unassigned to see available work
```

### Wrong Worktree

```
Error: This worktree is configured for agent-b
You are trying to initialize as agent-a
Please cd to ../project-foundation first
```

## Best Practices

1. **Initialize immediately** when starting a session
2. **One agent per worktree** to avoid conflicts
3. **Check dependencies** before starting work
4. **Use consistent agent IDs** across sessions
5. **Clean up** with `/agent-complete` when done

## Benefits

1. **Context Loading**: Automatically loads relevant tasks
2. **Identity Management**: Clear ownership of work
3. **Dependency Awareness**: Know what blocks your work
4. **Progress Tracking**: All updates tagged with agent ID
5. **Session Continuity**: Easy to resume work
