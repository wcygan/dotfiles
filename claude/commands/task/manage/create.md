Create a new project task or subtask following the simplified structure.

Usage:

- `/task-create project "project-name" [--description="description"]`
- `/task-create subtask "project-name" "subtask-title" [--priority=high|medium|low]`

Arguments: $ARGUMENTS

## Instructions

1. **Parse the arguments** to extract:
   - Type: project or subtask (required, first argument)
   - Project name: hyphenated lowercase (required, second argument)
   - For subtasks: title (required, third argument)
   - Optional flags: description, priority

2. **Validate inputs**:
   - Convert project names to lowercase, hyphenated format
   - Ensure names contain only alphanumeric characters and hyphens
   - For subtasks, ensure parent project exists

3. **Create the structure** based on type:

   **For Projects**:
   ```bash
   # Create project directory
   mkdir -p /tasks/{project-name}
   ```

   Create `/tasks/{project-name}/README.md`:
   ```markdown
   # Project: {Human Readable Title}

   **Status**: planning
   **Created**: {ISO date}
   **Updated**: {ISO date}

   ## Overview

   {description or placeholder}

   ## Tasks

   - [ ] 001-{first-subtask}.md - Description pending

   ## Progress

   - Total subtasks: 0
   - Completed: 0
   - Progress: 0%
   ```

   **For Subtasks**:
   - Find the next available index number (001, 002, etc.)
   - Create `/tasks/{project-name}/{index}-{hyphenated-title}.md`:

   ```markdown
   # {index}: {Human Readable Title}

   **Status**: pending
   **Created**: {ISO date}
   **Priority**: {priority}

   ## Description

   {Auto-generated or provided description}

   ## Action Items

   - [ ] Define specific implementation steps
   - [ ] Add acceptance criteria

   ## Notes

   {Empty section for implementation notes}
   ```

4. **Update the project README.md**:
   - Add the new subtask to the Tasks list
   - Update the progress statistics
   - Sort tasks by index number

5. **Update global plan.md if needed**:
   - For new projects, add entry under "Active Projects"
   - Include brief description and status

6. **Provide confirmation**:

   **For Projects**:
   ```
   ✓ Created project: {project-name}

   Location: /tasks/{project-name}/

   Next steps:
   - Edit /tasks/{project-name}/README.md to add details
   - Create subtasks with: /task-create subtask "{project-name}" "task title"
   ```

   **For Subtasks**:
   ```
   ✓ Created subtask: {index}-{title}

   Location: /tasks/{project-name}/{index}-{title}.md

   Next steps:
   - Edit the file to add specific action items
   - Update status with: /task-update
   ```

## Examples

Create a new project:

```
/task-create project "authentication-system" --description="Implement OAuth2 authentication"
```

Add subtasks to the project:

```
/task-create subtask "authentication-system" "setup database schema"
/task-create subtask "authentication-system" "implement jwt tokens"
/task-create subtask "authentication-system" "create login endpoints"
```

## Error Handling

- If project already exists, show current tasks and suggest adding subtasks
- If subtask title is too long, suggest a shorter version
- Ensure consistent index numbering (pad with zeros: 001, 002, etc.)
