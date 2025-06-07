List tasks with filtering and sorting options.

Usage: `/task-list [--status=active|completed|all] [--priority=high|medium|low] [--tag=tagname] [--sort=updated|created|priority]`

Arguments: $ARGUMENTS

## Instructions

1. **Parse filter arguments**:
   - Status filter (default: "active" = planning, in-progress, blocked)
   - Priority filter (optional)
   - Tag filter (optional)
   - Sort order (default: "updated" descending)

2. **Load task data**:
   - Read `/tasks/status.json`
   - If file doesn't exist, show message: "No tasks found. Create one with /task-create"

3. **Apply filters**:
   - Status filtering:
     - "active": planning, in-progress, blocked
     - "completed": completed only
     - "all": all tasks
   - Priority: exact match if specified
   - Tag: tasks containing the specified tag

4. **Sort results**:
   - By updated date (most recent first)
   - By created date
   - By priority (high → medium → low)
   - Then alphabetically by task name

5. **Display formatted table**:
   ```
   Tasks (showing X of Y total)

   Name                Status        Priority   Progress   Updated      Tags
   ─────────────────────────────────────────────────────────────────────────
   upgrade-storage     in-progress   high       25%        2025-01-07   hardware, infrastructure
   implement-auth      planning      medium     0%         2025-01-05   security, backend
   optimize-ci         blocked       low        10%        2025-01-04   devops
   ```

6. **Show summary statistics**:
   ```
   Summary:
   - Active: 3 (planning: 1, in-progress: 1, blocked: 1)
   - Completed: 2
   - By Priority: high: 1, medium: 2, low: 2
   ```

7. **Provide helpful next actions**:
   - If no tasks: "Create your first task with /task-create"
   - If filtered results empty: "No tasks match your filters. Try /task-list --status=all"
   - If many completed: "Archive completed tasks with /task-archive"

## Display Formatting

- Use color coding if supported:
  - 🔴 high priority
  - 🟡 medium priority
  - 🟢 low priority
  - ⏸️ blocked status
  - ✅ completed status
- Truncate long task names to fit terminal width
- Show relative dates for recent updates (e.g., "2 days ago")
- Highlight tasks updated today

## Quick Filters

Suggest common filters at the bottom:

```
Quick filters:
- High priority active: /task-list --status=active --priority=high
- Recently updated: /task-list --sort=updated
- By tag: /task-list --tag=backend
```
