Archive completed projects or subtasks to keep the active list manageable.

Usage: `/task-archive "project-name" | "project/subtask" | --all-completed`

Arguments: $ARGUMENTS

## Instructions

1. **Parse archive arguments**:
   - Project name to archive entire project, OR
   - Project/subtask path to archive single subtask, OR
   - `--all-completed` flag to archive all completed items

2. **Validate before archiving**:
   - For projects: verify all subtasks are completed
   - For subtasks: verify subtask is completed
   - For bulk operations: show preview and ask for confirmation
   - Warn if trying to archive active items

3. **Create archive structure**:
   ```
   /tasks/archive/YYYY-MM/{project-name}/
   /tasks/archive/YYYY-MM/{project-name}/README.md
   /tasks/archive/YYYY-MM/{project-name}/001-subtask.md
   ```
   - Use completion date for YYYY-MM
   - Preserve project structure in archive

4. **Archive process**:
   - For projects: Move entire project directory to archive
   - For subtasks: Move individual .md file to archive project dir
   - Update global /tasks/plan.md to mark project as archived
   - Remove from TodoWrite if present

5. **Create archive summary** in `/tasks/archive/YYYY-MM/summary.md`:
   ```markdown
   # Archive Summary - YYYY-MM

   ## Archived Projects (X total)

   ### {Project Name}

   - Status: completed
   - Archived: YYYY-MM-DD
   - Subtasks: X completed
   - Duration: X days (created → completed)

   [Repeat for each archived project]

   ## Statistics

   - Projects completed: X
   - Total subtasks: Y
   - Average project duration: X days
   ```

6. **Display confirmation**:
   ```
   ✓ Archived successfully:

   Project: {project-name}
   Moved to: /tasks/archive/YYYY-MM/{project-name}/

   Archive summary:
   - Total archived this session: X projects
   - Active projects remaining: Y

   To view archived project: ls /tasks/archive/YYYY-MM/{project-name}/
   To restore: mv /tasks/archive/YYYY-MM/{project-name} /tasks/
   ```

7. **Bulk archive preview**:
   ```
   Projects to be archived:

   ✓ auth-system        (completed 5 days ago, 4/4 subtasks)
   ✓ api-refactor       (completed 10 days ago, 6/6 subtasks)

   Total: 2 projects (10 subtasks)
   Continue? (yes/no)
   ```

8. **Restore capability**:
   - Document how to restore: move file back and update status.json
   - Consider adding `/task-restore` command if needed

## Archive Strategies

1. **Archive completed project**:
   ```bash
   # Archive entire project when all subtasks complete
   /task-archive "auth-system"
   ```

2. **Archive single subtask**:
   ```bash
   # Archive individual completed subtask
   /task-archive "auth-system/003-oauth-integration"
   ```

3. **Bulk archive**:
   ```bash
   # Archive all completed projects
   /task-archive --all-completed
   ```

## Error Handling

- Prevent archiving projects with incomplete subtasks
- Prevent archiving active subtasks (pending, in-progress)
- Create archive directories as needed
- Handle file move failures gracefully
- Update global plan.md appropriately
- Provide rollback instructions if needed

## Archive Search

After archiving, projects can still be found with:

- `/task-search "term"` (searches archived items too)
- Browse archive: `ls /tasks/archive/`
