Add a progress log entry to an existing task.

Usage: `/task-log "task-name" "progress update message"`

Arguments: $ARGUMENTS

## Instructions

1. **Parse arguments**:
   - Task name (required, first argument)
   - Log message (required, remaining arguments)
   - If only task name provided, prompt for message

2. **Validate task exists**:
   - Check `/tasks/[task-name].md` exists
   - If not found, suggest similar tasks or /task-create

3. **Read current task file**:
   - Load the markdown file
   - Locate the "Progress Log" section

4. **Add new log entry**:
   - Insert after the "## Progress Log" header
   - Format:
   ```markdown
   ### [ISO datetime with timezone]

   - [Log message]
   ```
   - Preserve existing entries (prepend new ones)

5. **Update metadata**:
   - In the markdown header, update the "Updated" date
   - In `/tasks/status.json`, update the "updated" timestamp

6. **Smart suggestions based on content**:
   - If message contains "completed", "done", "finished":
     - Suggest: "Update status to completed? /task-update '[task-name]' --status=completed"
   - If message contains "blocked", "waiting", "stuck":
     - Suggest: "Mark as blocked? /task-update '[task-name]' --status=blocked"
   - If message indicates progress:
     - Suggest: "Update progress? /task-update '[task-name]' --progress=X"

7. **Special log entry types** (auto-detect from message):
   - **Milestone**: If message starts with "Milestone:" or contains percentage
   - **Blocker**: If message contains "blocked by" or "waiting for"
   - **Decision**: If message starts with "Decided:" or "Decision:"
   - Format these specially:
   ```markdown
   ### 2025-01-07T14:30:00Z

   - 🎯 **Milestone**: Completed phase 1 (25% overall progress)

   ### 2025-01-07T15:00:00Z

   - 🚧 **Blocker**: Waiting for API credentials from vendor

   ### 2025-01-07T16:00:00Z

   - 📋 **Decision**: Using PostgreSQL instead of MySQL for better performance
   ```

8. **Batch logging** (if multiple updates):
   - Support multiline messages
   - Format as bullet points under single timestamp:
   ```markdown
   ### 2025-01-07T14:30:00Z

   - Reviewed storage options
   - Selected Samsung 990 Pro based on benchmarks
   - Ordered from vendor (arrival in 2 days)
   ```

9. **Provide confirmation**:
   ```
   ✓ Added progress log to: [task-name]

   Latest entry:
   "[First 100 chars of message]..."

   Task last updated: [relative time]
   View full task: /task-show "[task-name]"
   ```

## Examples

```bash
# Simple progress update
/task-log "upgrade-storage" "Ordered new SSD, arriving Thursday"

# Milestone with suggestion
/task-log "implement-auth" "Milestone: Completed user registration flow (50% done)"
> Suggestion: Update progress with /task-update "implement-auth" --progress=50

# Blocker notification
/task-log "deploy-prod" "Blocked by: Waiting for security review approval"
> Suggestion: Mark as blocked with /task-update "deploy-prod" --status=blocked

# Multiple updates
/task-log "refactor-api" "Completed endpoint refactoring
Improved response time by 40%
Ready for code review"
```
