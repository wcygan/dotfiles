Display detailed information about a specific task.

Usage: `/task-show "task-name"`

Arguments: $ARGUMENTS

## Instructions

1. **Parse the task name** from arguments
   - Extract and validate the task name
   - Convert to lowercase, hyphenated format if needed

2. **Check task existence**:
   - Look for `/tasks/[task-name].md`
   - If not found, check `/tasks/status.json` for similar names
   - Suggest alternatives if exact match not found

3. **Read and display the task file**:
   - Load the complete markdown file
   - Display with syntax highlighting if available
   - Show the full content including:
     - Header metadata
     - Context section
     - Plan with checkboxes
     - Complete progress log
     - Resources

4. **Enhance with additional metadata** from status.json:
   - Show calculated metrics:
     - Days since creation
     - Days since last update
     - Estimated completion (based on progress rate)
   - Related tasks (by shared tags)
   - Task dependencies if any

5. **Display format**:
   ```
   ════════════════════════════════════════════════════════════════
   TASK: Upgrade Storage
   ════════════════════════════════════════════════════════════════

   Status: in-progress (25%)
   Priority: high
   Created: 5 days ago (2025-01-06)
   Updated: 2 days ago (2025-01-07)
   Tags: hardware, infrastructure

   ─────────────────────────────────────────────────────────────────
   [Full markdown content]
   ─────────────────────────────────────────────────────────────────

   Related Tasks:
   - setup-monitoring (infrastructure)
   - backup-automation (infrastructure)

   Next Actions:
   - Add progress: /task-log "upgrade-storage" "your update"
   - Update status: /task-update "upgrade-storage" --status=completed
   ```

6. **Provide contextual suggestions**:
   - If planning: "Ready to start? Use /task-update --status=in-progress"
   - If blocked: "Add details about the blocker with /task-log"
   - If high progress: "Nearly done! Remember to update status when complete"
   - If old task: "This task hasn't been updated in X days"

## Error Handling

- If task not found, show list of all available tasks
- Suggest using /task-list to browse tasks
- Handle archived tasks by checking archive directories
