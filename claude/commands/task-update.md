Update project or subtask status and metadata using the simplified structure.

Usage:

- `/task-update "project-name" --status=planning|in-progress|completed`
- `/task-update "project-name/001-subtask-name" --status=pending|in-progress|completed [--priority=high|medium|low]`

Arguments: $ARGUMENTS

## Instructions

1. **Parse the arguments**:
   - Path (required, first argument)
     - Project: "project-name"
     - Subtask: "project-name/001-subtask-name"
   - Status flag (required)
   - Priority flag (optional, for subtasks)

2. **Validate inputs**:
   - Parse path to determine type (project/subtask)
   - Check item exists in appropriate location:
     - Project: `/tasks/{project-name}/README.md`
     - Subtask: `/tasks/{project-name}/{index}-{subtask-name}.md`
   - Validate status based on type:
     - Projects: planning, in-progress, completed
     - Subtasks: pending, in-progress, completed
   - If item doesn't exist, suggest using /task-create

3. **Update the appropriate markdown file**:
   - Read the correct markdown file:
     - Project: `/tasks/{project-name}/README.md`
     - Subtask: `/tasks/{project-name}/{index}-{subtask-name}.md`
   - Update the header section with new values:
     - Status
     - Updated timestamp
     - Priority (if changed for subtasks)
     - Add completion date if status is "completed"

4. **For Projects** - Update README.md:
   ```markdown
   # Project: {Human Readable Title}

   **Status**: {new-status}
   **Created**: {ISO date}
   **Updated**: {new ISO date}
   **Completed**: {ISO date} // only if status=completed
   ```

   Also update the Tasks list to reflect subtask status changes:
   ```markdown
   ## Tasks

   - [x] 001-completed-subtask.md - Description ✓
   - [ ] 002-pending-subtask.md - Description
   - [~] 003-in-progress-subtask.md - Description (in progress)
   ```

5. **For Subtasks** - Update the subtask file:
   ```markdown
   # {index}: {Human Readable Title}

   **Status**: {new-status}
   **Created**: {ISO date}
   **Updated**: {new ISO date}
   **Priority**: {priority}
   **Completed**: {ISO date} // only if status=completed
   ```

6. **Calculate project progress**:
   - Count total subtasks in project
   - Count completed subtasks
   - Update Progress section in project README.md:
     ```markdown
     ## Progress

     - Total subtasks: X
     - Completed: Y
     - Progress: Z%
     ```

7. **Sync with TodoWrite** (if applicable):
   - If status = "pending" or "in-progress":
     - Ensure item is in todo list
     - Update todo status to "in_progress" if subtask status is "in-progress"
   - If status = "completed":
     - Mark todo as completed

8. **Add progress log entry**:
   Append to the Notes section of the file:
   ```markdown
   ## Notes

   ### {ISO datetime}

   - Status changed from {old} to {new}
   - {Additional context if provided}
   ```

9. **Provide status summary**:

   **For Projects**:
   ```
   ✓ Updated project: {project-name}

   Status: {old-status} → {new-status}
   Progress: Y/X subtasks completed (Z%)

   Next steps:
   - View subtasks: /task-list --project={project-name}
   - Update a subtask: /task-update "{project-name}/001-subtask"
   ```

   **For Subtasks**:
   ```
   ✓ Updated subtask: {index}-{subtask-name}

   Status: {old-status} → {new-status}
   Project impact: {project-name} now at Z% (Y/X completed)

   [If this completes all subtasks]
   All subtasks complete! Consider updating project status:
   /task-update "{project-name}" --status=completed
   ```

## Special Handling

- **Completed items**: Add completion timestamp
- **Status regression**: Warn if moving from completed back to pending/in-progress
- **Auto-completion**: If all subtasks completed, suggest completing the project
- **Global plan update**: When updating projects, also check if `/tasks/plan.md` needs updating
