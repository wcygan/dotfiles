Update task status, progress, or other metadata.

Usage: `/task-update "task-name" --status=planning|in-progress|blocked|completed [--progress=0-100] [--priority=high|medium|low]`

Arguments: $ARGUMENTS

## Instructions

1. **Parse the arguments**:
   - Task name (required, first argument)
   - Status flag (required)
   - Progress flag (optional, 0-100)
   - Priority flag (optional)

2. **Validate inputs**:
   - Check task exists in `/tasks/status.json`
   - Validate status is one of: planning, in-progress, blocked, completed
   - Ensure progress is between 0-100
   - If task doesn't exist, suggest using /task-create

3. **Read current task state**:
   - Load `/tasks/status.json`
   - Get current task metadata

4. **Update the markdown file header**:
   - Read `/tasks/[task-name].md`
   - Update the header section with new values:
     - Status
     - Updated timestamp
     - Priority (if changed)
     - Add completion date if status is "completed"

5. **Update status.json**:
   ```json
   {
     "tasks": {
       "[task-name]": {
         "status": "[new-status]",
         "updated": "[ISO date]",
         "progress": [progress],
         "priority": "[priority]",
         "completed": "[ISO date]"  // only if status=completed
       }
     }
   }
   ```
   - Recalculate statistics (byStatus, byPriority counts)

6. **Sync with TodoWrite**:
   - If status = "planning", "in-progress", or "blocked":
     - Ensure task is in todo list
     - Update todo status to "in_progress" if task status is "in-progress"
   - If status = "completed":
     - Mark todo as completed
     - Remove from active todo list

7. **Add automatic progress log entry** if significant change:
   ```markdown
   ### [ISO datetime]

   - Status changed from [old] to [new]
   - Progress updated to [progress]%
   ```

8. **Provide status summary**:
   ```
   ✓ Updated task: [task-name]

   Status: [old-status] → [new-status]
   Progress: [old]% → [new]%

   [If completed]
   Consider archiving with: /task-archive "[task-name]"
   ```

## Special Handling

- **Completed tasks**: Add completion timestamp, suggest archiving
- **Blocked tasks**: Prompt to add a progress log explaining the blocker
- **Progress milestones**: Auto-log at 25%, 50%, 75%, 100%
- **Status regression**: Warn if moving from completed back to active
