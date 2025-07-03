# Scaffold Deno Script with Dax

## Description

Creates a new Deno script in the `/scripts` folder using Dax for cross-platform shell operations and adds it as a task in the project's `deno.json`.

## Usage

```
/scaffold-deno-script [script-name]
```

## What it does

1. Creates a new script file in the `/scripts` folder
2. Adds Dax dependency to project's `deno.json` if not already present
3. Adds a new task in `deno.json` to run the script
4. Creates a script demonstrating cross-platform shell operations
5. Includes examples of progress indicators and command execution
6. Runs the script to verify Dax functionality

## Example

```
/scaffold-deno-script cleanup-logs
```

This creates a new script at `/scripts/cleanup-logs.ts` and adds a `cleanup-logs` task to `deno.json`:

- Cross-platform shell command execution via Dax
- Modern TypeScript with JSR imports
- Progress indicators and async operations
- Error handling and proper exit codes
- File system operations and command output processing
- Template for building automation scripts
