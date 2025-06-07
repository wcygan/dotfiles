List plans, tasks, and subtasks with hierarchical filtering and sorting options.

Usage:

- `/task-list [--type=plans|tasks|subtasks|all] [--status=active|completed|all] [--priority=high|medium|low] [--tag=tagname] [--plan=plan-name] [--task=task-name] [--sort=updated|created|priority]`
- `/task-list --plan=plan-name` (show all tasks/subtasks in a plan)
- `/task-list --task=plan-name/task-name` (show all subtasks in a task)

Arguments: $ARGUMENTS

## Instructions

1. **Parse filter arguments**:
   - Type filter (default: "all" = plans, tasks, subtasks)
   - Status filter (default: "active" = planning, in-progress, blocked)
   - Priority filter (optional)
   - Tag filter (optional)
   - Plan filter (optional, shows tasks/subtasks within plan)
   - Task filter (optional, shows subtasks within task)
   - Sort order (default: "updated" descending)

2. **Load hierarchical data**:
   - Read global `/tasks/status.json` for plans overview
   - If plan filter specified, read `/tasks/[plan-name]/status.json`
   - If no plans exist, show message: "No plans found. Create one with /task-create plan"

3. **Apply hierarchical filters**:
   - Type filtering:
     - "plans": show only plans
     - "tasks": show only tasks (optionally filtered by plan)
     - "subtasks": show only subtasks (optionally filtered by plan/task)
     - "all": show all levels with indentation
   - Status filtering:
     - "active": planning, in-progress, blocked
     - "completed": completed only
     - "all": all statuses
   - Priority: exact match if specified
   - Tag: items containing the specified tag
   - Plan/Task: hierarchical scoping

4. **Sort results hierarchically**:
   - Maintain parent-child relationships in display
   - Within each level:
     - By updated date (most recent first)
     - By created date
     - By priority (high → medium → low)
     - Then alphabetically by name

5. **Display hierarchical formatted table**:

   **All Types View**:
   ```
   Plans, Tasks & Subtasks (showing X of Y total)

   Name                          Type      Status        Priority   Progress   Updated      Tags
   ─────────────────────────────────────────────────────────────────────────────────────────────────
   📋 voice-assistant-migration   plan      in-progress   high       45%        2025-01-07   migration, voice
   ├── 🔧 setup-infrastructure    task      completed     high       100%       2025-01-06   infrastructure
   │   ├── setup-monorepo         subtask   completed     high       100%       2025-01-05   monorepo
   │   └── setup-deployment       subtask   completed     medium     100%       2025-01-06   deployment
   ├── 🎨 build-features          task      in-progress   medium     25%        2025-01-07   features
   │   ├── voice-ui-components    subtask   completed     medium     100%       2025-01-06   ui, voice
   │   ├── audio-streaming        subtask   in-progress   high       50%        2025-01-07   audio, streaming
   │   └── state-management       subtask   planning      medium     0%         2025-01-05   state
   ```

   **Plan-Specific View** (`--plan=voice-assistant-migration`):
   ```
   Tasks in plan: voice-assistant-migration (showing X of Y total)

   Task                     Status        Priority   Progress   Subtasks   Updated      Tags
   ─────────────────────────────────────────────────────────────────────────────────────────
   🔧 setup-infrastructure  completed     high       100%       2/2        2025-01-06   infrastructure
   🎨 build-features        in-progress   medium     25%        1/3        2025-01-07   features
   🚀 optimize-production   planning      low        0%         0/2        2025-01-05   production
   ```

6. **Show hierarchical summary statistics**:
   ```
   Summary:
   Plans:
   - Active: 2 (planning: 1, in-progress: 1)
   - Completed: 1

   Tasks (across all plans):
   - Active: 5 (planning: 2, in-progress: 2, blocked: 1)
   - Completed: 3

   Subtasks (across all tasks):
   - Active: 8 (planning: 3, in-progress: 4, blocked: 1)
   - Completed: 12

   By Priority: high: 6, medium: 8, low: 4
   ```

7. **Provide helpful next actions**:
   - If no plans: "Create your first plan with /task-create plan \"plan-name\""
   - If filtered results empty: "No items match your filters. Try /task-list --status=all --type=all"
   - If many completed: "Archive completed items with /task-archive"
   - If viewing plan with no tasks: "Add tasks with /task-create task \"plan-name/task-name\""
   - If viewing task with no subtasks: "Add subtasks with /task-create subtask \"plan-name/task-name/subtask-name\""

## Display Formatting

- Use hierarchical icons:
  - 📋 Plans
  - 🔧 Tasks (can also use context-specific icons)
  - ✓ Completed items
  - ⏸️ Blocked items
- Use tree structure with indentation:
  - ├── for tasks under plans
  - │ ├── for subtasks under tasks
  - └── for last items in each level
- Use color coding if supported:
  - 🔴 high priority
  - 🟡 medium priority
  - 🟢 low priority
- Truncate long names to fit terminal width
- Show relative dates for recent updates (e.g., "2 days ago")
- Highlight items updated today

## Quick Filters

Suggest common hierarchical filters at the bottom:

```
Quick filters:
- Active plans: /task-list --type=plans --status=active
- High priority items: /task-list --status=active --priority=high
- Specific plan: /task-list --plan=voice-assistant-migration
- Specific task: /task-list --task=voice-assistant-migration/build-features
- Recently updated: /task-list --sort=updated
- By tag: /task-list --tag=backend
- All subtasks: /task-list --type=subtasks
```
