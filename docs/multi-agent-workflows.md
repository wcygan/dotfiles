# Multi-Agent Workflows with Claude Code

This guide explains how to effectively use Claude Code's multi-agent capabilities for complex software development tasks, leveraging the custom commands in the `claude/commands/` directory.

## Overview

Multi-agent workflows allow you to parallelize development work across multiple Claude instances, each working in separate git worktrees. This approach maximizes efficiency while avoiding merge conflicts and enables tackling complex projects that would be too large for a single session.

## Key Commands for Multi-Agent Work

### 1. Planning Phase: `/plan`

The `/plan` command analyzes your codebase and creates a comprehensive `PLAN.md` file that:
- Breaks down work into discrete, actionable tasks
- Identifies which tasks can run in parallel vs sequentially
- Defines clear synchronization points
- Estimates complexity and assigns tasks to specific agents

**Usage:**
```bash
claude> /plan implement user authentication system
```

This generates a structured plan with:
- **Phase 1**: Parallel tasks (unit tests, documentation, independent modules)
- **Phase 2**: Join points for integration and conflict resolution
- **Phase 3**: Sequential tasks requiring ordered execution

### 2. Parallel Setup: `/parallel`

The `/parallel` command sets up multiple git worktrees and provides launch instructions for parallel Claude instances.

**Usage:**
```bash
claude> /parallel
```

This command will:
1. Analyze your repository for parallelization opportunities
2. Create separate worktrees for independent features
3. Generate launch commands for each Claude instance
4. Set up a coordination file at `/tmp/claude-tasks.md`

**Example output:**
```bash
# Terminal 1: Authentication feature
git worktree add ../myproject-auth feature-auth
cd ../myproject-auth && claude

# Terminal 2: API endpoints
git worktree add ../myproject-api feature-api
cd ../myproject-api && claude

# Terminal 3: Database migrations
git worktree add ../myproject-db feature-db
cd ../myproject-db && claude
```

### 3. Coordination: `/coordinate`

The `/coordinate` command creates a detailed coordination plan for multiple Claude instances, managing dependencies and communication.

**Usage:**
```bash
claude> /coordinate
```

This creates `/tmp/claude-coordination.md` with:
- Work stream definitions and assignments
- Task dependencies and priorities
- Communication channels (shared files for status updates)
- Synchronization points

## Best Practices for Multi-Agent Development

### 1. Task Decomposition
- **Independent tasks**: Frontend/backend separation, test suites, documentation
- **Minimize overlap**: Assign files/modules to single agents when possible
- **Clear boundaries**: Each agent should have a well-defined scope

### 2. Communication Patterns
- Use shared status files (`/tmp/claude-scratch/status.json`)
- Regular synchronization at defined join points
- PR comments for code-level communication

### 3. Workflow Example

Here's a typical multi-agent workflow for implementing a new feature:

```bash
# Step 1: Plan the work
claude> /plan implement shopping cart feature

# Step 2: Set up parallel development
claude> /parallel

# Step 3: Create coordination plan
claude> /coordinate

# Step 4: Launch agents in separate terminals
# Terminal 1:
cd ../myproject-frontend && claude
> Read /tmp/claude-coordination.md
> Work on frontend tasks from Stream A

# Terminal 2:
cd ../myproject-backend && claude
> Read /tmp/claude-coordination.md
> Work on backend tasks from Stream B

# Terminal 3:
cd ../myproject-tests && claude
> Read /tmp/claude-coordination.md
> Work on test tasks from Stream C
```

### 4. Synchronization Points

Define clear synchronization points in your plan:
1. **After parallel work**: Merge features and run integration tests
2. **Before deployment**: Final review and build verification
3. **At blockers**: When one stream needs results from another

### 5. Monitoring Progress

Track multi-agent progress using:
```bash
# Check coordination status
deno run --allow-read scripts/check-coordination-progress.ts

# View specific agent status
cat /tmp/claude-scratch/status.json | jq '.instances["claude-frontend"]'

# Monitor git worktree status
git worktree list
```

## Advanced Patterns

### 1. Pipeline Development
Use multiple agents in a pipeline where each completes a stage:
- Agent 1: Core implementation
- Agent 2: Tests and validation
- Agent 3: Documentation and examples

### 2. Feature Branch Strategy
Each agent works on a feature branch:
```bash
git worktree add ../project-auth feature/auth
git worktree add ../project-api feature/api
git worktree add ../project-ui feature/ui
```

### 3. Conflict Resolution
Plan for potential conflicts:
- Assign clear file ownership
- Use join points for integration
- Have a designated "integration agent" for final merging

## Common Pitfalls to Avoid

1. **File conflicts**: Don't have multiple agents editing the same files
2. **Dependency chains**: Minimize sequential dependencies between agents
3. **Communication gaps**: Ensure regular status updates via shared files
4. **Scope creep**: Keep each agent focused on their assigned tasks

## Cleanup

After completing multi-agent work:
```bash
# Remove completed worktrees
git worktree remove ../project-auth
git worktree remove ../project-api

# Clean up coordination files
rm -rf /tmp/claude-scratch
rm /tmp/claude-coordination.md
```

## Summary

Multi-agent workflows with Claude Code enable:
- **Parallel development** of independent features
- **Structured coordination** through planning and task assignment
- **Efficient progress** on complex projects
- **Clear communication** via shared status files

By combining `/plan`, `/parallel`, and `/coordinate` commands, you can tackle large-scale development tasks that would be impractical for a single Claude instance, while maintaining code quality and avoiding conflicts.