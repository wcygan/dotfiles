---
description: Generate handoff summary for transitioning to new agent or session
---

Create a comprehensive handoff summary of the current session.

**Handoff structure:**

## Context Summary
- What was the original request/goal?
- What phase of work are we in? (planning/implementation/testing/review)

## Progress Report
- ✅ **Completed**: Tasks finished successfully
- 🚧 **In Progress**: Current work state
- ⏸️ **Blocked**: Issues preventing progress
- 📋 **Pending**: Queued tasks

## Technical State
- Files modified (list with brief change description)
- Git status (branch, commits, staged changes)
- Tests status (passing/failing)
- Dependencies added/changed

## Key Decisions
- Architectural choices made
- Trade-offs considered
- Approaches rejected (and why)

## Next Steps
1. Immediate next action (most critical)
2. Subsequent tasks (ordered by priority)
3. Open questions needing user input

## Handoff Prompt
Generate a ready-to-use prompt for the next agent:

"""
You are continuing work on [project/task]. Previous agent context:

**Objective**: [original goal]

**Current state**: [where we are now]

**What's done**: [completed work]

**What's next**: [immediate action needed]

**Important context**: [key decisions, constraints, patterns discovered]

Please continue by [specific next step].
"""

**Style**: Be concise but complete. The next agent should understand the situation without re-reading the entire thread.
