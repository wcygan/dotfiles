Display detailed information about a project or subtask.

Usage:

- `/task-show "project-name"` (show project overview with all subtasks)
- `/task-show "project-name/001-subtask"` (show specific subtask details)

Arguments: $ARGUMENTS

## Instructions

1. **Parse the path** from arguments:
   - Extract and validate the path
   - Determine if showing project or subtask
   - Convert to lowercase, hyphenated format if needed

2. **Check existence**:
   - For projects: Look for `/tasks/{project-name}/README.md`
   - For subtasks: Look for `/tasks/{project-name}/{index}-{subtask}.md`
   - If not found, suggest alternatives

3. **Display Project Overview** (if showing project):
   ```
   ════════════════════════════════════════════════════════════════
   PROJECT: {Project Name}
   ════════════════════════════════════════════════════════════════

   Status: {status}
   Created: {date}
   Updated: {date}
   Progress: X/Y subtasks completed (Z%)

   ─────────────────────────────────────────────────────────────────
   [Project README.md content]
   ─────────────────────────────────────────────────────────────────

   Subtasks:
   ┌─────┬──────────────────────────┬────────────┬──────────┬─────────┐
   │ #   │ Title                    │ Status     │ Priority │ Updated │
   ├─────┼──────────────────────────┼────────────┼──────────┼─────────┤
   │ 001 │ core-development        │ pending    │ high     │ 1d ago  │
   │ 002 │ build-distribution      │ pending    │ medium   │ 1d ago  │
   │ 003 │ documentation           │ pending    │ medium   │ 1d ago  │
   └─────┴──────────────────────────┴────────────┴──────────┴─────────┘

   Next Actions:
   - Start a subtask: /task-update "{project}/001-core-development" --status=in-progress
   - Add subtask: /task-create subtask "{project}" "new task"
   - View subtask: /task-show "{project}/001-core-development"
   ```

4. **Display Subtask Details** (if showing subtask):
   ```
   ════════════════════════════════════════════════════════════════
   SUBTASK: 001 - {Subtask Title}
   Project: {project-name}
   ════════════════════════════════════════════════════════════════

   Status: {status}
   Priority: {priority}
   Created: {date}
   Updated: {date}

   ─────────────────────────────────────────────────────────────────
   [Full subtask markdown content]
   ─────────────────────────────────────────────────────────────────

   Other subtasks in this project:
   - 001-current-task.md (← you are here)
   - 002-next-task.md (pending)
   - 003-other-task.md (pending)

   Next Actions:
   - Update status: /task-update "{project}/001-subtask" --status=in-progress
   - View project: /task-show "{project}"
   - Next subtask: /task-show "{project}/002-next-task"
   ```

5. **Show related information**:
   - For projects: List all subtasks with status summary
   - For subtasks: Show sibling subtasks and project context
   - Calculate days since creation/update
   - Show progress visualization

6. **Provide contextual suggestions**:
   - If all pending: "Ready to start? Pick a high-priority subtask"
   - If some in-progress: "Continue work on in-progress tasks"
   - If mostly complete: "Nearly done! {X} subtasks remaining"
   - If stale: "This hasn't been updated in {X} days"

## Error Handling

- If not found, show available projects: "Project not found. Available projects:"
- For subtasks, show available subtasks in the project
- Suggest using /task-list to browse all projects
