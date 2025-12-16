---
description: Symlink AGENTS.md files to CLAUDE.md for Claude Code compatibility
---

Find all `AGENTS.md` files in the current project and create `CLAUDE.md` symlinks pointing to them (where CLAUDE.md doesn't already exist).

**Context**: Claude Code reads `CLAUDE.md` files for project context, but some projects use `AGENTS.md` (the agents.md specification). This command bridges the gap by symlinking them.

**Task**:

1. Use `fd AGENTS.md` to find all AGENTS.md files in the project
2. For each file found:
   - Check if `CLAUDE.md` already exists in the same directory
   - If it exists (file or symlink), skip and report
   - If it doesn't exist, create a symlink: `CLAUDE.md -> AGENTS.md`
3. Report results showing:
   - Files created (with path)
   - Files skipped (with reason)
   - Summary count

**Implementation**:

```bash
fd AGENTS.md | while read -r agents_file; do
  dir=$(dirname "$agents_file")
  claude_file="$dir/CLAUDE.md"
  
  if [ "$dir" = "." ]; then
    claude_file="CLAUDE.md"
  fi
  
  if [ -e "$claude_file" ]; then
    echo "SKIP: $claude_file (already exists)"
  else
    (cd "$dir" && ln -s AGENTS.md CLAUDE.md)
    echo "CREATED: $claude_file -> AGENTS.md"
  fi
done
```

**Output format**:
```
Linking AGENTS.md → CLAUDE.md...

SKIP: CLAUDE.md (already exists)
CREATED: backend/CLAUDE.md -> AGENTS.md
CREATED: frontend/CLAUDE.md -> AGENTS.md

Summary: 2 created, 1 skipped
```

Run the script and report results. Do not modify any existing files.
