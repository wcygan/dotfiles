Generate a Zed task configuration for: $ARGUMENTS

Create a task definition for .zed/tasks.json following Zed's task specification:
https://zed.dev/docs/tasks

Requirements:

1. Parse the user's task description to determine:
   - Task label (descriptive name)
   - Command to execute
   - Working directory (default to $ZED_WORKTREE_ROOT)
   - Whether it needs a new terminal
   - Whether concurrent runs are allowed
   - When to reveal the terminal (always/never/on_error)

2. Use appropriate Zed variables:
   - $ZED_FILE - current file path
   - $ZED_WORKTREE_ROOT - project root
   - $ZED_COLUMN - cursor column
   - $ZED_ROW - cursor row

3. Output a properly formatted JSON task configuration that can be added to .zed/tasks.json

4. If .zed/tasks.json doesn't exist, create it with the task
   If it exists, show how to add the task to the existing array

5. For common task types, suggest appropriate configurations:
   - Test runners (with file-specific tests)
   - Build commands
   - Linters/formatters
   - Development servers
   - Script runners

Example output format:

```json
{
  "label": "Run tests",
  "command": "deno test",
  "cwd": "$ZED_WORKTREE_ROOT",
  "use_new_terminal": false,
  "allow_concurrent_runs": false,
  "reveal": "always"
}
```

Provide clear instructions on how to use the generated task in Zed.
