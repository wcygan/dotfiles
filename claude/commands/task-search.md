Search through tasks by name, content, tags, or status.

Usage: `/task-search "search-term" [--in=title|content|tags|all] [--status=active|completed|all]`

Arguments: $ARGUMENTS

## Instructions

1. **Parse search arguments**:
   - Search term (required)
   - Search scope (default: "all")
     - title: Task names only
     - content: Task file contents
     - tags: Tag matches only
     - all: Everything
   - Status filter (default: "all")

2. **Perform the search**:
   - **Title search**: Check task names in status.json
   - **Tag search**: Match against tags array in status.json
   - **Content search**: Read each .md file and search within
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

   1. upgrade-storage (high priority, in-progress)
      📁 /tasks/upgrade-storage.md
      📅 Updated: 2 days ago
      🏷️ Tags: hardware, infrastructure
      
      Context match:
      "...need to upgrade from 512GB to 2TB NVMe SSD..."

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   2. backup-automation (medium priority, planning)
      📁 /tasks/backup-automation.md
      📅 Updated: 5 days ago
      🏷️ Tags: infrastructure, automation
      
      Title match: Contains "backup"
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
   - View task: /task-show "[task-name]"
   - Update: /task-update "[task-name]" --status=...
   - Add log: /task-log "[task-name]" "message"
   ```

## Search Examples

```bash
# Search everywhere for "auth"
/task-search "auth"

# Search only in task titles
/task-search "storage" --in=title

# Search for a specific tag
/task-search "backend" --in=tags

# Search only active tasks
/task-search "implement" --status=active

# Complex search
/task-search "database migration" --in=content --status=active
```

## Performance Optimization

- Cache file contents during search session
- Limit context display to avoid overwhelming output
- For large task sets (>50), paginate results
- Index frequently searched terms in status.json
