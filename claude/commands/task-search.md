Search through projects and subtasks by name or content.

Usage: `/task-search "search-term" [--in=name|content|all] [--status=active|completed|all]`

Arguments: $ARGUMENTS

## Instructions

1. **Parse search arguments**:
   - Search term (required)
   - Search scope (default: "all")
     - name: Project/subtask names only
     - content: File contents
     - all: Everything
   - Status filter (default: "all")

2. **Perform the search**:
   - **Name search**: Check project directories and subtask filenames
   - **Content search**: Read README.md and subtask .md files
   - Search in `/tasks/` directory structure
   - Use case-insensitive matching
   - Support partial matches

3. **Rank results by relevance**:
   - Exact matches first
   - Title matches before content matches
   - Recent tasks before older ones
   - Active tasks before completed ones

4. **Display search results**:
   ```
   Search results for: "[search-term]" (found X matches)

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   1. agentic-workflow-cli/001-core-cli-development (pending, high)
      📁 /tasks/agentic-workflow-cli/001-core-cli-development.md
      📅 Updated: 2 days ago
      
      Context match:
      "...develop the core CLI structure and commands..."

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   2. agentic-workflow-cli (project, planning)
      📁 /tasks/agentic-workflow-cli/README.md
      📅 Updated: 2 days ago
      
      Project match: Contains "cli" in name
   ```

5. **Search highlighting**:
   - Highlight matching terms in results
   - Show context around matches (±2 lines)
   - Indicate match type (title/content/tag)

6. **Advanced search features**:
   - Support AND operations: "auth AND security"
   - Support OR operations: "auth OR login"
   - Support phrase search: "\"user authentication\""
   - Support exclusions: "security -testing"

7. **Empty results handling**:
   ```
   No tasks found matching "[search-term]"

   Suggestions:
   - Try a broader search term
   - Check spelling
   - Browse all tasks: /task-list
   - Search in different scope: /task-search "[term]" --in=content
   ```

8. **Quick actions for results**:
   ```
   Actions:
   - View project: /task-show "project-name"
   - View subtask: /task-show "project/001-subtask"
   - Update: /task-update "project/001-subtask" --status=...
   - Add log: /task-log "project/001-subtask" "message"
   ```

## Search Examples

```bash
# Search everywhere for "cli"
/task-search "cli"

# Search only in names
/task-search "core" --in=name

# Search only active items
/task-search "implement" --status=active

# Complex search
/task-search "build system" --in=content --status=active
```

## Performance Optimization

- Cache file contents during search session
- Limit context display to avoid overwhelming output
- For large task sets (>50), paginate results
- Index frequently searched terms in status.json
