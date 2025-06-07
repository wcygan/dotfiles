Create a new task, subtask, or plan with hierarchical organization in the `/tasks` directory.

Usage:

- `/task-create plan "plan-name" [--priority=high|medium|low] [--tags=tag1,tag2]`
- `/task-create task "plan-name/task-name" [--priority=high|medium|low] [--tags=tag1,tag2]`
- `/task-create subtask "plan-name/task-name/subtask-name" [--priority=high|medium|low] [--tags=tag1,tag2]`

Arguments: $ARGUMENTS

## Instructions

1. **Parse the arguments** to extract:
   - Type: plan, task, or subtask (required, first argument)
   - Path: hierarchical path (required, second argument)
     - Plan: "plan-name"
     - Task: "plan-name/task-name"
     - Subtask: "plan-name/task-name/subtask-name"
   - Priority flag (optional, defaults to "medium")
   - Tags flag (optional, comma-separated)

2. **Validate the path and type**:
   - Convert all path components to lowercase, hyphenated format
   - Ensure paths contain only alphanumeric characters, hyphens, and forward slashes
   - Validate hierarchy:
     - Plan: Must not already exist in `/tasks/`
     - Task: Parent plan must exist
     - Subtask: Parent plan and task must exist
   - Check that the specific item doesn't already exist

3. **Create the directory structure** based on type:
   ```bash
   # For plans
   mkdir -p tasks/[plan-name]/archive/$(date +%Y-%m)

   # For tasks  
   mkdir -p tasks/[plan-name]/[task-name]

   # For subtasks (files only, no additional directories)
   # Subtasks are markdown files within task directories
   ```

4. **Create the appropriate markdown file** based on type:

   **For Plans** - `/tasks/[plan-name]/plan.md`:
   ```markdown
   # Plan: [Human Readable Title]

   **Status**: planning
   **Created**: [ISO date YYYY-MM-DD]
   **Updated**: [ISO date YYYY-MM-DD]
   **Priority**: [priority]
   **Tags**: [comma-separated tags]

   ## Overview

   [High-level description of the plan's goals and scope]

   ## Success Criteria

   - [ ] Define measurable outcomes
   - [ ] Set clear completion criteria

   ## Tasks

   This plan is broken down into the following tasks:

   - See task directories for detailed breakdowns

   ## Dependencies & Constraints

   [External dependencies, resource constraints, timeline requirements]

   ## Progress Log

   ### [ISO datetime]

   - Plan created

   ## Resources

   - [Strategic documentation links]
   - [Architecture decisions]
   ```

   **For Tasks** - `/tasks/[plan-name]/[task-name]/task.md`:
   ```markdown
   # Task: [Human Readable Title]

   **Plan**: [plan-name]
   **Status**: planning
   **Created**: [ISO date YYYY-MM-DD]
   **Updated**: [ISO date YYYY-MM-DD]
   **Priority**: [priority]
   **Tags**: [comma-separated tags]

   ## Context

   [Medium-scale description of what needs to be accomplished]

   ## Subtasks

   This task is broken down into the following subtasks:

   - [ ] [List of subtask files in this directory]

   ## Dependencies

   - Prerequisites from other tasks
   - Blocking relationships

   ## Progress Log

   ### [ISO datetime]

   - Task created

   ## Resources

   - [Task-specific documentation]
   - [Implementation references]
   ```

   **For Subtasks** - `/tasks/[plan-name]/[task-name]/[subtask-name].md`:
   ```markdown
   # Subtask: [Human Readable Title]

   **Plan**: [plan-name]
   **Task**: [task-name]
   **Status**: planning
   **Created**: [ISO date YYYY-MM-DD]
   **Updated**: [ISO date YYYY-MM-DD]
   **Priority**: [priority]
   **Tags**: [comma-separated tags]

   ## Context

   [Small-scale, specific work item description]

   ## Action Items

   - [ ] Concrete, verifiable steps
   - [ ] Each should be completable in a single session
   - [ ] Include acceptance criteria

   ## Progress Log

   ### [ISO datetime]

   - Subtask created

   ## Resources

   - [Implementation-specific links]
   - [Code references]
   ```

5. **Update hierarchical status files**:

   **Global Status** `/tasks/status.json`:
   - Tracks all plans and high-level statistics

   **Plan Status** `/tasks/[plan-name]/status.json`:
   - Tracks tasks and subtasks within the plan

   **Structure for global status.json**:
   ```json
   {
     "version": "2.0",
     "lastUpdated": "[ISO timestamp]",
     "plans": {
       "[plan-name]": {
         "title": "[Human Readable Title]",
         "status": "planning",
         "priority": "[priority]",
         "created": "[ISO date]",
         "updated": "[ISO date]",
         "tags": ["tag1", "tag2"],
         "progress": 0,
         "tasksCount": 0,
         "subtasksCount": 0
       }
     },
     "statistics": {
       "plans": {
         "total": 1,
         "active": 1,
         "completed": 0
       }
     }
   }
   ```

   **Structure for plan-specific status.json**:
   ```json
   {
     "version": "2.0",
     "plan": "[plan-name]",
     "lastUpdated": "[ISO timestamp]",
     "tasks": {
       "[task-name]": {
         "title": "[Human Readable Title]",
         "status": "planning",
         "priority": "[priority]",
         "created": "[ISO date]",
         "updated": "[ISO date]",
         "tags": ["tag1", "tag2"],
         "progress": 0,
         "subtasksCount": 0
       }
     },
     "subtasks": {
       "[task-name]/[subtask-name]": {
         "title": "[Human Readable Title]",
         "task": "[task-name]",
         "status": "planning",
         "priority": "[priority]",
         "created": "[ISO date]",
         "updated": "[ISO date]",
         "tags": ["tag1", "tag2"],
         "progress": 0
       }
     },
     "statistics": {
       "tasks": {
         "total": 1,
         "active": 1,
         "completed": 0
       },
       "subtasks": {
         "total": 1,
         "active": 1,
         "completed": 0
       }
     }
   }
   ```

6. **Add to TodoWrite** for session tracking:
   - For plans: Create todo with plan overview
   - For tasks: Create todo linking to parent plan
   - For subtasks: Create actionable todo item
   - Set status as "pending" and use same priority

7. **Provide confirmation** with type-specific next steps:

   **For Plans**:
   ```
   ✓ Created plan: [plan-name]

   Next steps:
   - Edit /tasks/[plan-name]/plan.md to define scope and success criteria
   - Create tasks with /task-create task "[plan-name]/task-name"
   - Use /task-list --plan=[plan-name] to view plan progress
   ```

   **For Tasks**:
   ```
   ✓ Created task: [plan-name]/[task-name]

   Next steps:
   - Edit /tasks/[plan-name]/[task-name]/task.md to add context
   - Create subtasks with /task-create subtask "[plan-name]/[task-name]/subtask-name"
   - Use /task-update to change status
   ```

   **For Subtasks**:
   ```
   ✓ Created subtask: [plan-name]/[task-name]/[subtask-name]

   Next steps:
   - Edit /tasks/[plan-name]/[task-name]/[subtask-name].md to add action items
   - Use /task-update to change status
   - Use /task-log to add progress entries
   ```

## Error Handling

- If item already exists, suggest using /task-update instead
- If parent doesn't exist (task without plan, subtask without task), provide creation guidance
- If invalid characters in path, show the sanitized version and ask for confirmation
- If directory creation fails, check permissions
- If attempting to create a task/subtask in a completed plan, warn about reactivation
