Update plan, task, or subtask status, progress, or other metadata.

Usage:

- `/task-update "plan-name" --status=planning|in-progress|blocked|completed [--progress=0-100] [--priority=high|medium|low]`
- `/task-update "plan-name/task-name" --status=planning|in-progress|blocked|completed [--progress=0-100] [--priority=high|medium|low]`
- `/task-update "plan-name/task-name/subtask-name" --status=planning|in-progress|blocked|completed [--progress=0-100] [--priority=high|medium|low]`

Arguments: $ARGUMENTS

## Instructions

1. **Parse the arguments**:
   - Hierarchical path (required, first argument)
     - Plan: "plan-name"
     - Task: "plan-name/task-name"
     - Subtask: "plan-name/task-name/subtask-name"
   - Status flag (required)
   - Progress flag (optional, 0-100)
   - Priority flag (optional)

2. **Validate inputs**:
   - Parse path to determine type (plan/task/subtask)
   - Check item exists in appropriate location:
     - Plan: `/tasks/[plan-name]/plan.md` and global status.json
     - Task: `/tasks/[plan-name]/[task-name]/task.md` and plan status.json
     - Subtask: `/tasks/[plan-name]/[task-name]/[subtask-name].md` and plan status.json
   - Validate status is one of: planning, in-progress, blocked, completed
   - Ensure progress is between 0-100
   - If item doesn't exist, suggest using /task-create

3. **Read current hierarchical state**:
   - Load appropriate status.json file(s):
     - Plans: Load global `/tasks/status.json`
     - Tasks/Subtasks: Load `/tasks/[plan-name]/status.json`
   - Get current item metadata

4. **Update the appropriate markdown file header**:
   - Read the correct markdown file:
     - Plan: `/tasks/[plan-name]/plan.md`
     - Task: `/tasks/[plan-name]/[task-name]/task.md`
     - Subtask: `/tasks/[plan-name]/[task-name]/[subtask-name].md`
   - Update the header section with new values:
     - Status
     - Updated timestamp
     - Priority (if changed)
     - Add completion date if status is "completed"

5. **Update hierarchical status files**:

   **For Plans** (update global `/tasks/status.json`):
   ```json
   {
     "plans": {
       "[plan-name]": {
         "status": "[new-status]",
         "updated": "[ISO date]",
         "progress": [calculated-from-tasks],
         "priority": "[priority]",
         "completed": "[ISO date]"  // only if status=completed
       }
     }
   }
   ```

   **For Tasks/Subtasks** (update `/tasks/[plan-name]/status.json`):
   ```json
   {
     "tasks": {
       "[task-name]": {
         "status": "[new-status]",
         "progress": [calculated-from-subtasks]
       }
     },
     "subtasks": {
       "[task-name]/[subtask-name]": {
         "status": "[new-status]",
         "progress": [progress]
       }
     }
   }
   ```

   - Recalculate hierarchical statistics
   - Propagate progress changes upward through the hierarchy

6. **Sync with TodoWrite**:
   - Update corresponding todo item based on type:
     - Plans: Update high-level strategic todo
     - Tasks: Update medium-scope todo
     - Subtasks: Update specific action todo
   - If status = "planning", "in-progress", or "blocked":
     - Ensure item is in todo list
     - Update todo status to "in_progress" if item status is "in-progress"
   - If status = "completed":
     - Mark todo as completed
     - Check if parent items should be updated

7. **Add automatic progress log entry** with hierarchical context:
   ```markdown
   ### [ISO datetime]

   - Status changed from [old] to [new]
   - Progress updated to [progress]%
   - [For tasks/subtasks] Plan "[plan-name]" now at [plan-progress]%
   ```

8. **Provide hierarchical status summary**:

   **For Plans**:
   ```
   ✓ Updated plan: [plan-name]

   Status: [old-status] → [new-status]
   Progress: [old]% → [new]% (calculated from [X] tasks)

   [If completed]
   Consider archiving with: /task-archive "[plan-name]"
   ```

   **For Tasks**:
   ```
   ✓ Updated task: [plan-name]/[task-name]

   Status: [old-status] → [new-status]
   Progress: [old]% → [new]% (calculated from [X] subtasks)
   Plan impact: "[plan-name]" now at [plan-progress]%

   [If completed]
   Consider archiving with: /task-archive "[plan-name]/[task-name]"
   ```

   **For Subtasks**:
   ```
   ✓ Updated subtask: [plan-name]/[task-name]/[subtask-name]

   Status: [old-status] → [new-status]
   Progress: [old]% → [new]%
   Task impact: "[task-name]" now at [task-progress]%
   Plan impact: "[plan-name]" now at [plan-progress]%

   [If completed]
   Next: Work on other subtasks in this task
   ```

## Special Handling

- **Completed items**: Add completion timestamp, calculate parent progress
- **Blocked items**: Prompt to add a progress log explaining the blocker
- **Progress milestones**: Auto-log at 25%, 50%, 75%, 100%
- **Status regression**: Warn if moving from completed back to active
- **Hierarchical completion**:
  - If all subtasks completed → suggest completing task
  - If all tasks completed → suggest completing plan
- **Progress propagation**: Changes bubble up through plan → task → subtask hierarchy
