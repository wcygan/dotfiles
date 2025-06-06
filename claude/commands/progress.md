# progress

Track development progress with timestamped entries

## Usage

Record progress updates with automatic timestamp generation and organization by date. The agent will handle file creation using shell commands.

## Examples

```bash
# Record a new feature
/progress "Implemented user authentication with JWT tokens"

# Record debugging work
/progress "Fixed memory leak in WebSocket connection handler"

# Record refactoring
/progress "Refactored database connection pool for better performance"

# View today's progress
/progress --today

# View progress for a specific date
/progress --date 2025-06-06

# View all progress entries
/progress --all
```

## Implementation

The agent will:

1. **For recording progress**:
   - Run `date` to get current timestamp
   - Create directory structure: `./progress/YYYY-MM-DD/` (in project root)
   - Create file: `YYYY-MM-DD-HH:MM:SS-TIMEZONE.md`
   - Write progress entry with markdown formatting

2. **For viewing progress**:
   - Use `ls`, `cat`, and `find` commands to retrieve entries
   - Format output appropriately based on the flag used

## Directory Structure

```
./progress/
├── 2025-06-06/
│   ├── 2025-06-06-10:30:45-CDT.md
│   ├── 2025-06-06-14:22:10-CDT.md
│   └── 2025-06-06-16:45:33-CDT.md
├── 2025-06-07/
│   └── 2025-06-07-09:15:22-CDT.md
```

## File Format

Each progress file contains:

```markdown
# Progress Update

**Date**: 2025-06-06
**Time**: 10:30:45 CDT

## Summary

[User's progress message]

---
```

## Features

- Automatic timestamp generation using shell `date` command
- Organized by date in subdirectories
- Simple markdown format for each entry
- Easy retrieval by date or all entries
- Human-readable file naming convention
- No external dependencies - pure shell operations
