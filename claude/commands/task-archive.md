Archive completed or cancelled tasks to keep the active list manageable.

Usage: `/task-archive "task-name" | --all-completed | --older-than=30d`

Arguments: $ARGUMENTS

## Instructions

1. **Parse archive arguments**:
   - Single task name, OR
   - `--all-completed` flag to archive all completed tasks, OR
   - `--older-than=Xd` to archive tasks not updated in X days

2. **Validate before archiving**:
   - For single task: verify it exists and is completed/cancelled
   - For bulk operations: show preview and ask for confirmation
   - Warn if trying to archive active tasks

3. **Create archive structure**:
   ```
   /tasks/archive/YYYY-MM/[task-name].md
   ```
   - Use task's completion date for YYYY-MM
   - If not completed, use last updated date

4. **Archive process for each task**:
   - Move the .md file to archive directory
   - Update status.json:
     - Add "archived": true flag
     - Add "archivedDate": "[ISO date]"
     - Keep entry for searchability
   - Update statistics in status.json
   - Remove from TodoWrite if present

5. **Create archive summary** in `/tasks/archive/YYYY-MM/summary.md`:
   ```markdown
   # Archive Summary - YYYY-MM

   ## Archived Tasks (X total)

   ### [Task Name]

   - Status: completed
   - Archived: YYYY-MM-DD
   - Duration: X days (created → completed)
   - Tags: [tags]

   [Repeat for each archived task]

   ## Statistics

   - Tasks completed: X
   - Average completion time: X days
   - Most used tags: [top 3 tags]
   ```

6. **Display confirmation**:
   ```
   ✓ Archived successfully:

   Task: [task-name]
   Moved to: /tasks/archive/YYYY-MM/[task-name].md

   Archive summary:
   - Total archived this session: X
   - Total in archive: Y
   - Active tasks remaining: Z

   To view archived task: cat /tasks/archive/YYYY-MM/[task-name].md
   To restore: mv /tasks/archive/YYYY-MM/[task-name].md /tasks/
   ```

7. **Bulk archive preview**:
   ```
   Tasks to be archived:

   ✓ implement-auth     (completed 5 days ago)
   ✓ fix-bug-123        (completed 10 days ago)
   ✓ update-deps        (completed 15 days ago)

   Total: 3 tasks
   Continue? (yes/no)
   ```

8. **Restore capability**:
   - Document how to restore: move file back and update status.json
   - Consider adding `/task-restore` command if needed

## Archive Strategies

1. **Monthly cleanup**:
   ```bash
   # Archive all completed tasks
   /task-archive --all-completed
   ```

2. **Stale task cleanup**:
   ```bash
   # Archive tasks not touched in 60 days
   /task-archive --older-than=60d
   ```

3. **Single task**:
   ```bash
   # Archive specific completed task
   /task-archive "implement-auth"
   ```

## Error Handling

- Prevent archiving active tasks (planning, in-progress, blocked)
- Create archive directories as needed
- Handle file move failures gracefully
- Maintain status.json integrity
- Provide rollback instructions if needed

## Archive Search

After archiving, tasks can still be found with:

- `/task-search "term"` (searches archived tasks too)
- `/task-list --status=all` (shows archived count)
