Complete an agent's work session with proper cleanup and integration:

## Usage

```bash
/agent-complete [agent-id] [options]
```

## Examples

```bash
# Complete current agent's work
/agent-complete

# Complete specific agent
/agent-complete agent-a

# Complete with automatic PR creation
/agent-complete agent-a --create-pr

# Complete without removing worktree (for review)
/agent-complete agent-a --keep-worktree
```

## Completion Process

1. **Validate Agent State**:
   ```bash
   # Check all assigned tasks are complete or handed off
   INCOMPLETE=$(jq -r '.assignedTasks[] | select(.status != "completed")' \
                /tasks/$PROJECT/agents/$AGENT.json)

   if [ -n "$INCOMPLETE" ]; then
     echo "Warning: Agent has incomplete tasks:"
     echo "$INCOMPLETE"
     echo "Continue anyway? (y/n)"
   fi
   ```

2. **Create Pull Request**:
   ```bash
   # Gather completed work
   COMPLETED_TASKS=$(jq -r '.assignedTasks[] | select(.status == "completed")' \
                    /tasks/$PROJECT/agents/$AGENT.json)

   # Generate PR body
   PR_BODY="## Completed Tasks

   $(echo "$COMPLETED_TASKS" | sed 's/^/- /')

   ## Summary
   Agent: $AGENT
   Branch: $BRANCH
   Duration: $(calculate_duration)
   Tasks Completed: $(count_completed)
   "

   # Create PR
   gh pr create --title "[$AGENT] ${TASK_GROUP} Implementation" \
                --body "$PR_BODY" \
                --base main \
                --head $BRANCH
   ```

3. **Update Task Status**:
   ```bash
   # Mark all completed tasks as merged
   for TASK in $COMPLETED_TASKS; do
     /task-update "$TASK" --status=merged --merged-by="$AGENT"
   done

   # Update agent status
   jq '.status = "completed"' /tasks/$PROJECT/agents/$AGENT.json > tmp.json
   mv tmp.json /tasks/$PROJECT/agents/$AGENT.json
   ```

4. **Clean Up Worktree**:
   ```bash
   # Get worktree info
   WORKTREE=$(jq -r '.worktree' /tasks/$PROJECT/agents/$AGENT.json)
   BRANCH=$(jq -r '.branch' /tasks/$PROJECT/agents/$AGENT.json)

   # Ensure we're not in the worktree being removed
   CURRENT_DIR=$(pwd)
   if [[ "$CURRENT_DIR" == "$WORKTREE"* ]]; then
     echo "Switching to main worktree before cleanup..."
     cd $(git worktree list | grep "(bare)" | awk '{print $1}' | head -1)
   fi

   # Remove worktree
   echo "Removing worktree: $WORKTREE"
   git worktree remove "$WORKTREE" --force

   # Prune worktree list
   git worktree prune
   ```

5. **Archive or Delete Branch**:
   ```bash
   # If PR was merged, delete branch
   PR_STATUS=$(gh pr view $BRANCH --json state -q .state)

   if [ "$PR_STATUS" = "MERGED" ]; then
     echo "Deleting merged branch: $BRANCH"
     git branch -d $BRANCH
   else
     echo "Branch $BRANCH kept for pending PR"
   fi
   ```

6. **Update Coordination Status**:
   ```bash
   # Remove agent from active coordination
   jq "del(.coordination.agents[\"$AGENT\"])" \
      /tasks/$PROJECT/status.json > tmp.json
   mv tmp.json /tasks/$PROJECT/status.json

   # Add to completed agents list
   jq ".coordination.completedAgents += [\"$AGENT\"]" \
      /tasks/$PROJECT/status.json > tmp.json
   mv tmp.json /tasks/$PROJECT/status.json
   ```

## Completion Report

```
Agent Completion Summary
═══════════════════════════════════════════

Agent: agent-a (claude-foundation)
Status: Successfully Completed

## Work Summary
- Total Tasks: 5
- Completed: 5
- Handed Off: 0
- Duration: 4 hours 32 minutes

## Pull Request
- PR #123: [agent-a] Foundation Setup
- Status: Open
- URL: https://github.com/org/repo/pull/123

## Cleanup Actions
✓ Tasks marked as merged
✓ Agent status updated
✓ Worktree removed: ../project-foundation
✓ Coordination status updated

## Next Steps
- Review and merge PR #123
- Agent agent-c can now start testing tasks
```

## Advanced Options

### Partial Completion

```bash
# Hand off remaining tasks to another agent
/agent-complete agent-a --handoff=agent-d

# This will:
# - Transfer incomplete tasks to agent-d
# - Update dependencies
# - Preserve work history
```

### Abandoned Worktree Recovery

```bash
# List all worktrees to find abandoned ones
git worktree list

# Clean up abandoned worktree
/agent-complete --cleanup-worktree="../abandoned-worktree"
```

### Batch Completion

```bash
# Complete multiple agents after integration
/agent-complete agent-a agent-b agent-c --after-integration
```

## Safety Features

1. **Pre-completion Checks**:
   - Verify no uncommitted changes
   - Check for incomplete tasks
   - Validate PR creation eligibility

2. **Rollback Support**:
   - Keep branch until PR is merged
   - Archive agent configuration
   - Maintain task history

3. **Conflict Prevention**:
   - Check if worktree is in use
   - Verify branch status before deletion
   - Update dependencies atomically

## Integration with Other Commands

- Updates task status visible in `/task-list`
- Removes agent from `/agent-status --all`
- Triggers dependency updates for blocked agents
- Creates PR visible in git workflow

## Best Practices

1. **Complete all tasks** before running agent-complete
2. **Create PR** to preserve work history
3. **Check dependencies** to ensure no blocking
4. **Clean session** with no uncommitted changes
5. **Document handoffs** if transferring work
