# Task Management System

A comprehensive task management system with persistent storage in the `/tasks` directory. Tasks are stored as markdown files with metadata tracked in a JSON index for quick searching and filtering.

## Available Commands

The task management system is split into focused commands for better usability:

### 📝 `/task-create` - Create a new task

```bash
/task-create "task-name" [--priority=high|medium|low] [--tags=tag1,tag2]
```

Creates a new task with markdown template and adds to status index.

### 🔄 `/task-update` - Update task status or metadata

```bash
/task-update "task-name" --status=planning|in-progress|blocked|completed [--progress=0-100]
```

Updates task status, progress, priority, or other metadata.

### 📋 `/task-list` - List and filter tasks

```bash
/task-list [--status=active|completed|all] [--priority=high|medium|low] [--tag=tagname]
```

Displays tasks in a formatted table with filtering options.

### 👁️ `/task-show` - View task details

```bash
/task-show "task-name"
```

Shows complete task information including progress history.

### ✍️ `/task-log` - Add progress entries

```bash
/task-log "task-name" "progress update message"
```

Appends timestamped progress updates to task history.

### 🔍 `/task-search` - Search across tasks

```bash
/task-search "search-term" [--in=title|content|tags|all] [--status=active|all]
```

Searches task names, contents, and tags with highlighted results.

### 📦 `/task-archive` - Archive completed tasks

```bash
/task-archive "task-name" | --all-completed | --older-than=30d
```

Moves completed tasks to archive folders organized by date.

## Quick Start

1. **Create your first task**:
   ```bash
   /task-create "implement-feature-x" --priority=high --tags=backend,api
   ```

2. **Add context and planning**:
   ```bash
   /task-show "implement-feature-x"
   # Then edit the markdown file to add details
   ```

3. **Track progress**:
   ```bash
   /task-log "implement-feature-x" "Completed database schema design"
   /task-update "implement-feature-x" --status=in-progress --progress=25
   ```

4. **View active tasks**:
   ```bash
   /task-list --status=active
   ```

5. **Complete and archive**:
   ```bash
   /task-update "implement-feature-x" --status=completed
   /task-archive "implement-feature-x"
   ```

## File Structure

```
/tasks/
├── status.json              # Task index and metadata
├── implement-auth.md        # Individual task file
├── upgrade-storage.md       # Individual task file
└── archive/                 # Completed tasks
    └── 2025-01/
        ├── summary.md       # Monthly archive summary
        └── old-task.md      # Archived task
```

## Task File Format

Each task is stored as a markdown file with structured metadata:

```markdown
# Task: [Human Readable Title]

**Status**: planning|in-progress|blocked|completed
**Created**: YYYY-MM-DD
**Updated**: YYYY-MM-DD
**Priority**: high|medium|low
**Tags**: tag1, tag2

## Context

Background information and requirements

## Plan

- [ ] Specific action items
- [ ] Broken down into steps

## Progress Log

### YYYY-MM-DDTHH:MM:SSZ

- Progress entries in reverse chronological order

## Resources

- Relevant links and references
```

## Status Index (status.json)

The JSON index enables quick filtering and statistics:

```json
{
  "version": "1.0",
  "lastUpdated": "ISO timestamp",
  "tasks": {
    "task-name": {
      "title": "Human Readable Title",
      "status": "current status",
      "priority": "priority level",
      "created": "creation date",
      "updated": "last update",
      "tags": ["tags"],
      "progress": 0-100
    }
  },
  "statistics": {
    "total": 10,
    "active": 6,
    "completed": 4,
    "byStatus": {...},
    "byPriority": {...}
  }
}
```

## Integration with TodoWrite

Active tasks (planning, in-progress, blocked) are automatically synced with the Claude session's todo list for easy tracking within the current context.

## Best Practices

1. **Naming**: Use descriptive, hyphenated names (e.g., "implement-user-auth")
2. **Progress**: Update regularly with `/task-log` for accountability
3. **Archiving**: Monthly cleanup keeps active list focused
4. **Tags**: Use consistent tags for better organization
5. **Planning**: Break down tasks into verifiable action items

## Common Workflows

### Bug Fix Workflow

```bash
/task-create "fix-login-bug" --priority=high --tags=bug,auth
/task-log "fix-login-bug" "Reproduced issue in test environment"
/task-update "fix-login-bug" --status=in-progress
/task-log "fix-login-bug" "Fixed: Added null check for user session"
/task-update "fix-login-bug" --status=completed --progress=100
/task-archive "fix-login-bug"
```

### Feature Development

```bash
/task-create "add-export-feature" --priority=medium --tags=feature,backend
/task-update "add-export-feature" --status=in-progress
/task-log "add-export-feature" "Milestone: CSV export working (50%)"
/task-update "add-export-feature" --progress=50
/task-log "add-export-feature" "Added PDF export support"
/task-update "add-export-feature" --status=completed --progress=100
```

### Blocked Task

```bash
/task-log "deploy-prod" "Blocked: Waiting for security team approval"
/task-update "deploy-prod" --status=blocked
# Later...
/task-log "deploy-prod" "Received approval, proceeding with deployment"
/task-update "deploy-prod" --status=in-progress
```

For detailed help on any command, simply run the command without arguments or refer to the individual command files in `claude/commands/`.
