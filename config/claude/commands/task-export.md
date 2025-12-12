---
description: Export tasks to standalone markdown files with full context for delegation
---

Export the current task list (or user-provided tasks) into individual markdown files in `/tmp/claude-tasks/`.

**Input:** Either use the current todo list from this session, or the user will provide a list of tasks.

**For each task, create a file at:** `/tmp/claude-tasks/{timestamp}-{slug}.md`

**File structure for each task:**

```markdown
# Task: {Task Title}

## Objective
Clear one-sentence statement of what needs to be accomplished.

## Context
- **Project**: [project name/path if known]
- **Related files**: [key files involved]
- **Dependencies**: [what must exist/be done first]
- **Constraints**: [limitations, requirements, patterns to follow]

## Current State
Describe what exists now:
- Relevant code snippets or file contents
- Current behavior
- Why this task is needed

## Desired End State
Describe what should exist after completion:
- Expected behavior
- Success criteria
- How to verify completion

## Implementation Guidance
1. Step-by-step approach
2. Key decisions to make
3. Patterns to follow from existing code
4. Potential pitfalls to avoid

## Testing & Verification
- How to test the changes
- Commands to run
- Expected outputs

## References
- Related files: `file:line` format
- Documentation links
- Similar implementations in codebase
```

**Process:**

1. **Gather context**: For each task, analyze:
   - What files are involved
   - What code patterns exist
   - What the current state is
   - What success looks like

2. **Create directory**: `mkdir -p /tmp/claude-tasks`

3. **Generate files**: Create one `.md` file per task with full context

4. **Output summary**: List all created files with brief descriptions

**Naming convention:**
- Timestamp: `YYYYMMDD-HHMMSS`
- Slug: lowercase, hyphens, max 50 chars
- Example: `/tmp/claude-tasks/20241211-143022-add-user-auth.md`

**Style:**
- Be thorough - the file should be self-contained
- Include actual code snippets, not placeholders
- Specify exact file paths
- Make it actionable without additional context
- Assume the reader has no prior session context
