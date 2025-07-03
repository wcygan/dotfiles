Assign a task or set of tasks to a specific agent for multi-agent coordination:

## Usage

```bash
/agent-assign [task-path] [agent-id] [options]
```

## Examples

```bash
# Assign a single task
/agent-assign "project/setup-foundation" agent-a

# Assign all subtasks under a task
/agent-assign "project/core-features/*" agent-b

# Reassign a task from one agent to another
/agent-assign "project/testing-suite/unit-tests" agent-c --from=agent-b

# Assign with specific branch/worktree
/agent-assign "project/api-development" agent-d --branch=feature/api --worktree=../project-api
```

## Implementation Steps

1. **Validate Task Path**:
   - Check task exists in hierarchy
   - Verify task is not already assigned (unless --force)
   - Check for dependency conflicts

2. **Update Task Metadata**:
   ```bash
   # Add agent assignment to task
   /task-update "[task-path]" --assigned="[agent-id]"

   # Update plan's status.json
   {
     "coordination": {
       "agents": {
         "[agent-id]": {
           "assignedTasks": ["task-path", ...],
           "workload": 5  // number of assigned tasks
         }
       }
     }
   }
   ```

3. **Create/Update Agent Configuration**:
   ```json
   // In /tasks/[project]/agents/[agent-id].json
   {
     "agentId": "agent-a",
     "name": "claude-foundation",
     "worktree": "../project-foundation",
     "branch": "feature/setup-foundation",
     "assignedTasks": [
       "project/setup-foundation/project-structure",
       "project/setup-foundation/dependency-setup"
     ],
     "dependencies": {
       "blockedBy": [],
       "blocks": ["project/testing-suite"]
     },
     "status": "active",
     "lastUpdate": "2025-01-07T16:00:00Z"
   }
   ```

4. **Handle Dependencies**:
   - Check if assigned tasks have dependencies
   - Warn if dependencies assigned to different agents
   - Suggest optimal assignment order

5. **Worktree Setup** (if not exists):
   ```bash
   # Auto-create worktree for new agent
   if [ ! -d "$WORKTREE" ]; then
     git worktree add $WORKTREE $BRANCH
     echo "Created worktree: $WORKTREE on branch $BRANCH"
   fi
   ```

6. **Generate Agent Instructions**:
   ````markdown
   ## Agent Assignment Complete

   Agent: agent-a
   Assigned Tasks: 2
   Worktree: ../project-foundation
   Branch: feature/setup-foundation

   ### Launch Instructions:

   ```bash
   cd ../project-foundation && claude
   > /agent-init agent-a
   > /task-list --mine
   ```
   ````

   ### Assigned Tasks:
   - project/setup-foundation/project-structure (ready)
   - project/setup-foundation/dependency-setup (ready)

   ### This agent blocks:
   - project/testing-suite/* (agent-c)
   ```
   ```

## Advanced Features

### Workload Balancing

```bash
# Show current agent workloads
/agent-assign --show-workload

# Output:
# Agent Workload Summary:
# agent-a: 2 tasks (4 hours estimated)
# agent-b: 3 tasks (6 hours estimated)  
# agent-c: 1 task (2 hours estimated)
# 
# Unassigned tasks: 4

# Auto-balance unassigned tasks
/agent-assign --auto-balance
```

### Dependency-Aware Assignment

```bash
# Assign related tasks together
/agent-assign "project/api/*" agent-b --include-dependencies

# This assigns:
# - project/api/endpoints
# - project/api/authentication  
# - project/shared/models (dependency)
```

### Bulk Operations

```bash
# Assign by tags
/agent-assign --tag=frontend agent-ui
/agent-assign --tag=backend agent-api
/agent-assign --tag=testing agent-test

# Assign by priority
/agent-assign --priority=high agent-a --limit=3
```

## Integration with Other Commands

Works seamlessly with:

- `/plan-multi-agent` - Creates initial assignments
- `/task-create` - Can include --assigned flag
- `/agent-status` - Shows assigned work
- `/parallel-enhanced` - Uses assignments for setup

## Benefits

1. **Clear Ownership**: Every task has an assigned agent
2. **Dependency Management**: System prevents conflicting assignments
3. **Workload Visibility**: See distribution across agents
4. **Flexible Reassignment**: Move tasks between agents as needed
5. **Automatic Setup**: Worktrees created based on assignments
