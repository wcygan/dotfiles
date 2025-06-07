# Integrated Planning and Multi-Agent Workflow

## TL;DR - Quick Start

Want to parallelize development work across multiple Claude agents? Here's how:

```bash
# 1. Create a plan with tasks
/plan-multi-agent "Build my awesome feature"

# 2. Set up parallel environment
/parallel-enhanced

# 3. Launch agents in separate terminals
deno task agent  # Terminal 1
deno task agent  # Terminal 2  
deno task agent  # Terminal 3

# That's it! Each agent will:
# - Automatically claim tasks
# - Complete them independently
# - Claim more until done
# - Exit when no work remains
```

**Key Commands for Agents:**

- `deno task claim-task` - Claim next available task
- `/agent-complete [agent-id]` - Clean up when done

**Monitor Progress:**

- `cat .claude-agents/task-registry.json | jq '.agents'` - See active agents
- `/task-list --status=all` - View all tasks and their status

---

## Full Guide

This guide demonstrates how the Planning Framework and Multi-Agent Workflows work together as a unified system for managing complex development projects.

## Overview

The integrated system combines hierarchical task management with multi-agent coordination, creating a seamless workflow where planning naturally flows into parallel execution with automatic progress tracking and dependency management.

## Key Concepts

### Unified Coordination Model

Instead of separate coordination files in `/tmp`, agent assignments and coordination are stored directly in the task hierarchy:

```
/tasks/project-name/
├── plan.md                    # Project overview
├── status.json               # Includes agent coordination
├── coordination.md           # Agent assignments and dependencies
├── agents/                   # Agent configurations
│   ├── agent-a.json
│   ├── agent-b.json
│   └── agent-c.json
└── tasks/                    # Hierarchical task structure
```

### Agent-Aware Task Hierarchy

Tasks now include agent assignment metadata:

```json
{
  "task": "setup-foundation/project-structure",
  "status": "in-progress",
  "assigned": "agent-a",
  "startTime": "2025-01-07T10:00:00Z",
  "dependencies": []
}
```

## Integrated Workflow

### Step 1: Create Multi-Agent Plan

```bash
/plan-multi-agent "Implement voice assistant migration"
```

This single command:

- Analyzes the codebase
- Creates hierarchical task structure
- Assigns agents to tasks based on dependencies
- Sets up coordination metadata
- Prepares worktree configurations

### Step 2: Initialize Parallel Environment

```bash
/parallel-enhanced
```

This command:

- Reads agent assignments from the plan
- Creates git worktrees for each agent
- Generates agent-specific launch commands
- Sets up dependency tracking

### Step 3: Agent Initialization

Each agent starts their session:

```bash
# In their respective worktree
claude
> /agent-init agent-a
> /task-list --mine
```

This automatically:

- Sets agent identity for the session
- Loads assigned tasks into TodoWrite
- Shows dependencies and blockers
- Enables progress synchronization

### Step 4: Coordinated Execution

Agents work independently while the system manages coordination:

```bash
# Agent A works on foundation
/task-update "project/setup-foundation/project-structure" --status=in-progress
# Progress automatically syncs to status.json

# Agent B can see Agent A's progress
/agent-status --all
# Shows real-time progress across all agents

# Agent C waits for dependencies
/task-list --mine
# Shows blocked tasks with completion estimates
```

## Command Reference

### Planning Commands

- `/plan-multi-agent [description]` - Create plan with agent assignments
- `/task-create plan|task|subtask [path]` - Create hierarchical work items
- `/task-list --plan=[name]` - View plan hierarchy with progress

### Agent Commands

- `/agent-init [agent-id]` - Initialize agent session
- `/agent-assign [task] [agent]` - Assign tasks to agents
- `/agent-status [--all]` - View agent progress and dependencies
- `/agent-complete [agent-id]` - Finalize agent work

### Coordination Commands

- `/parallel-enhanced` - Set up worktrees from plan
- `/join-status --point=[name]` - Check join point readiness
- `/task-dependencies [task]` - View task dependency graph

## Example: Full Project Flow

### 1. Initial Planning

```bash
# Create the multi-agent plan
/plan-multi-agent "Build new authentication system"

# This creates:
# - /tasks/auth-system/plan.md
# - Three agents: agent-infra, agent-api, agent-ui
# - Task assignments based on architecture
```

### 2. Parallel Setup

```bash
# Set up parallel development
/parallel-enhanced

# Output:
# Created worktree: ../auth-system-infra (agent-infra)
# Created worktree: ../auth-system-api (agent-api)
# Created worktree: ../auth-system-ui (agent-ui)
#
# Launch commands:
# Terminal 1: cd ../auth-system-infra && claude
# Terminal 2: cd ../auth-system-api && claude
# Terminal 3: cd ../auth-system-ui && claude
```

### 3. Agent Work

**Terminal 1 - Infrastructure Agent:**

```bash
cd ../auth-system-infra && claude
> /agent-init agent-infra
> /task-list --mine

# Shows:
# - setup-database-schema (ready)
# - configure-auth-service (ready)
# - deploy-infrastructure (blocked by other tasks)

> /task-update "auth-system/infrastructure/setup-database-schema" --status=in-progress
```

**Terminal 2 - API Agent:**

```bash
cd ../auth-system-api && claude  
> /agent-init agent-api
> /task-list --mine

# Shows:
# - implement-auth-endpoints (blocked by database-schema)
# - create-user-models (ready)
# - add-jwt-handling (blocked by auth-endpoints)
```

**Terminal 3 - UI Agent:**

```bash
cd ../auth-system-ui && claude
> /agent-init agent-ui  
> /task-list --mine

# Shows:
# - create-login-form (ready)
# - implement-user-dashboard (blocked by api)
```

### 4. Progress Monitoring

Any agent can check overall progress:

```bash
/agent-status --all

# Multi-Agent Progress:
# agent-infra: 1/3 tasks (33%) - working on database-schema
# agent-api: 0/3 tasks (0%) - blocked, waiting for infra
# agent-ui: 1/2 tasks (50%) - working on login-form
#
# Critical path: database-schema → auth-endpoints → jwt-handling
```

### 5. Dependency Resolution

As tasks complete, blocked work automatically becomes available:

```bash
# Agent-infra completes database schema
/task-update "auth-system/infrastructure/setup-database-schema" --status=completed

# Agent-api immediately sees the task is unblocked
/task-list --mine
# implement-auth-endpoints is now marked as "ready"
```

### 6. Join Points

When parallel work needs to merge:

```bash
/join-status --point=integration

# Join Point Status: integration
# Required: infrastructure ✅, api-core ✅, ui-basics ⏳
# 
# Ready in: ~30 minutes (ui-basics 80% complete)
```

## Benefits of Integration

### 1. Single Source of Truth

- No duplicate coordination files
- Task hierarchy serves as both plan and assignment
- Progress automatically flows through the system

### 2. Reduced Complexity

- Fewer commands to remember
- Automatic dependency tracking
- No manual status synchronization

### 3. Better Visibility

- Real-time progress across all agents
- Clear dependency chains
- Accurate time estimates

### 4. Improved Coordination

- Automatic notification when blocked tasks clear
- System-enforced join points
- Conflict prevention through task assignment

### 5. Seamless Workflow

- Planning flows directly into execution
- Agent setup is automated
- Progress tracking is built-in

## Best Practices

### 1. Plan First

Always create a plan before parallelizing:

```bash
/plan-multi-agent "Project description"
/parallel-enhanced  # Uses the plan
```

### 2. Initialize Agents

Each agent should initialize at session start:

```bash
/agent-init [agent-id]
```

### 3. Update Progress Frequently

Keep tasks updated for accurate coordination:

```bash
/task-update "[task]" --status=in-progress
/task-log "[task]" "Completed API design"
```

### 4. Monitor Dependencies

Regularly check for unblocked work:

```bash
/task-list --mine --show-dependencies
/agent-status
```

### 5. Clean Up After Completion

```bash
/agent-complete agent-a  # Finalizes work
git worktree remove ../project-feature
```

## Migration from Separate Systems

If you have existing projects using the old separate systems:

### Old Way

```bash
# Separate planning and coordination
/plan "Build feature"
/coordinate  # Manual setup in /tmp
/parallel    # Manual worktree creation
# Manual status tracking in /tmp files
```

### New Way

```bash
# Integrated planning and coordination
/plan-multi-agent "Build feature"
/parallel-enhanced  # Automatic from plan
# Automatic status tracking in task hierarchy
```

## Troubleshooting

### Agent Can't Find Tasks

```bash
# Ensure agent is initialized
/agent-init [agent-id]

# Check task assignments
/task-list --assigned=[agent-id]
```

### Dependencies Not Updating

```bash
# Force status refresh
/task-update --recalculate-progress

# Check dependency chain
/task-dependencies [blocked-task]
```

### Worktree Conflicts

```bash
# List all worktrees
git worktree list

# Clean up old worktrees
git worktree prune
```

## Deno-Based Work-Stealing Implementation

The system uses a Deno TypeScript launch script for cross-platform compatibility and robust task management:

### Key Features

1. **Atomic Task Claims**: Agents use file locking on `/tasks/[project]/status.json` to prevent conflicts
2. **Fresh Reads**: Always reads latest status before claiming to ensure consistency
3. **Main Registry Updates**: Updates both local tracking and main status.json
4. **Detailed Diagnostics**: Shows why tasks are unavailable (claimed, blocked, etc.)

### Usage

```bash
# After setting up with /parallel-enhanced
deno task agent  # Launches an intelligent work-stealing agent
```

Each agent:

- Generates a unique ID automatically
- Claims one task at a time from the pool
- Updates status.json atomically
- Continues until no work remains
- Shows detailed reasons if blocked

### Task Recovery

If an agent crashes, its claimed tasks can be recovered by:

1. Running `/task-list --status=all` to see claimed tasks
2. Manually unclaiming with `/task-update [task] --unclaim`
3. Or waiting for timeout-based recovery (future feature)

## Summary

The integrated Planning and Multi-Agent system provides a powerful, unified approach to managing complex development projects. By combining hierarchical task management with intelligent agent coordination, teams can work more efficiently with better visibility and automatic dependency management.

Key takeaways:

- Use `/plan-multi-agent` to create agent-aware plans
- Use `/parallel-enhanced` for automatic worktree setup and Deno script
- Launch agents with `deno task agent` for work-stealing behavior
- Let the system handle coordination through the task hierarchy
- Monitor progress with `/agent-status`
