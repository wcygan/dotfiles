Create a new task with persistent storage in the `/tasks` directory.

Usage: `/task-create "task-name" [--priority=high|medium|low] [--tags=tag1,tag2]`

Arguments: $ARGUMENTS

## Instructions

1. **Parse the arguments** to extract:
   - Task name (required, first argument)
   - Priority flag (optional, defaults to "medium")
   - Tags flag (optional, comma-separated)

2. **Validate the task name**:
   - Convert to lowercase, hyphenated format (e.g., "Implement Auth" → "implement-auth")
   - Ensure it contains only alphanumeric characters and hyphens
   - Check that it doesn't already exist in `/tasks/`

3. **Create the directory structure** if needed:
   ```bash
   mkdir -p tasks/archive/$(date +%Y-%m)
   ```

4. **Create the task markdown file** at `/tasks/[task-name].md`:
   ```markdown
   # Task: [Human Readable Title]

   **Status**: planning
   **Created**: [ISO date YYYY-MM-DD]
   **Updated**: [ISO date YYYY-MM-DD]
   **Priority**: [priority]
   **Tags**: [comma-separated tags]

   ## Context

   [Describe the background, requirements, and constraints]

   ## Plan

   - [ ] Break down the task into specific action items
   - [ ] Each item should be independently verifiable
   - [ ] Include acceptance criteria

   ## Progress Log

   ### [ISO datetime]

   - Task created

   ## Resources

   - [Add relevant documentation links]
   - [Reference any related tasks or issues]
   ```

5. **Update or create `/tasks/status.json`**:
   - If file doesn't exist, create with initial structure
   - Add the new task entry
   - Update statistics
   - Format:
   ```json
   {
     "version": "1.0",
     "lastUpdated": "[ISO timestamp]",
     "tasks": {
       "[task-name]": {
         "title": "[Human Readable Title]",
         "status": "planning",
         "priority": "[priority]",
         "created": "[ISO date]",
         "updated": "[ISO date]",
         "tags": ["tag1", "tag2"],
         "progress": 0
       }
     },
     "statistics": {
       "total": 1,
       "active": 1,
       "completed": 0,
       "archived": 0,
       "byStatus": {
         "planning": 1
       },
       "byPriority": {
         "[priority]": 1
       }
     }
   }
   ```

6. **Add to TodoWrite** for session tracking:
   - Create a todo item with the task name
   - Set status as "pending"
   - Use the same priority as the task

7. **Provide confirmation** with next steps:
   ```
   ✓ Created task: [task-name]

   Next steps:
   - Edit /tasks/[task-name].md to add context and plan
   - Use /task-update to change status
   - Use /task-log to add progress entries
   ```

## Error Handling

- If task name already exists, suggest using /task-update instead
- If invalid characters in name, show the sanitized version and ask for confirmation
- If directory creation fails, check permissions
