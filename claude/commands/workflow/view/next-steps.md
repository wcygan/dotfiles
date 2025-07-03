Analyze the current project state and recommend the next best tasks to work on, including potential follow-up actions.

## Analysis Process

1. **Project State Assessment**:
   - Check for existing PLAN.md or planning documents
   - Review recent git commits and branch activity
   - Analyze open TODO items using TodoRead
   - Check task management system at /tasks/ for active items
   - Review CI/CD status and test results
   - Identify any blocked or stalled work

2. **Priority Analysis**:
   - **Immediate blockers**: Issues preventing other work
   - **High-impact tasks**: Core functionality, critical bugs
   - **Quick wins**: Small tasks with immediate value
   - **Technical debt**: Refactoring or cleanup needs
   - **Documentation gaps**: Missing or outdated docs
   - **Test coverage**: Areas needing better testing

3. **Context Gathering**:
   - Check for incomplete work from previous sessions
   - Review any error logs or failing tests
   - Look for comments like TODO, FIXME, HACK
   - Analyze dependencies and their health
   - Check for security vulnerabilities

4. **Recommendation Format**:

   **Next Steps** (prioritized list):

   1. **[Task Name]** - Priority: High/Medium/Low
      - Why: Brief explanation of importance
      - What: Specific actions to take
      - Dependencies: What needs to be done first
      - Estimated effort: Quick/Moderate/Significant
      - Follow-up tasks:
        - Related task 1
        - Related task 2

   2. **[Next Task]** ...

   **Optional Parallel Work**:
   - Tasks that can be done simultaneously
   - Independent improvements

   **Future Considerations**:
   - Longer-term improvements
   - Architecture decisions needed
   - Process improvements

5. **Task Creation**:
   - For each recommended task, offer to create it in the task system
   - Suggest appropriate priorities and tags
   - Link related tasks for better tracking

## Usage Examples

```bash
# General next steps analysis
/project:next-steps

# Focus on specific area
/project:next-steps "focus on performance improvements"

# After completing a feature
/project:next-steps "just finished user auth, what's next?"

# When stuck or blocked
/project:next-steps "blocked on database migration"
```

## Arguments

$ARGUMENTS

## Implementation Notes

- Always check multiple sources of truth (git, todos, tasks, code)
- Consider both technical and project management perspectives
- Balance urgency vs importance
- Suggest concrete, actionable next steps
- Include rationale for prioritization
- Identify task dependencies and relationships
- Consider team/multi-agent coordination needs
