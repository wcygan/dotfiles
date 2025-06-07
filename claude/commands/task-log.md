Add a progress log entry to a subtask.

Usage: `/task-log "project-name/001-subtask" "progress update message"`

Arguments: $ARGUMENTS

## Instructions

1. **Parse arguments**:
   - Path to subtask (required, first argument in format "project/index-subtask")
   - Log message (required, remaining arguments)
   - If only path provided, prompt for message

2. **Validate subtask exists**:
   - Check `/tasks/{project-name}/{index}-{subtask}.md` exists
   - If not found, suggest similar subtasks or /task-create

3. **Read current subtask file**:
   - Load the markdown file
   - Locate the "Notes" section

4. **Add new log entry**:
   - Append to the "## Notes" section
   - Format:
   ```markdown
   ### [ISO datetime with timezone]

   - [Log message]
   ```
   - Preserve existing entries (prepend new ones)

5. **Update metadata**:
   - In the markdown header, update the "Updated" date to current timestamp

6. **Smart suggestions based on content**:
   - If message contains "completed", "done", "finished":
     - Suggest: "Update status to completed? /task-update '{project}/{subtask}' --status=completed"
   - If message contains "blocked", "waiting", "stuck":
     - Suggest: "Note: Consider updating priority if this blocks other work"
   - If message indicates significant progress:
     - Suggest: "Great progress! Update status with /task-update if needed"

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
   ✓ Added progress log to: {project}/{subtask}

   Latest entry:
   "[First 100 chars of message]..."

   Subtask last updated: [relative time]
   View full subtask: /task-show "{project}/{subtask}"
   ```

## Examples

```bash
# Simple progress update
/task-log "agentic-cli/001-core-development" "Set up basic CLI structure with Cliffy"

# Milestone with suggestion
/task-log "agentic-cli/002-build-system" "Milestone: Completed build script for all platforms"
> Suggestion: Update status to completed? /task-update "agentic-cli/002-build-system" --status=completed

# Blocker notification
/task-log "auth-system/003-oauth-integration" "Blocked by: Waiting for OAuth provider credentials"
> Note: Consider updating priority if this blocks other work

# Multiple updates
/task-log "api-refactor/001-endpoint-design" "Designed new REST endpoints
Created OpenAPI spec
Ready for implementation"
```
