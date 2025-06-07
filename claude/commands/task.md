# Hierarchical Task Management System

A comprehensive three-tier task management system with persistent hierarchical storage in the `/tasks` directory. The system organizes work into **Plans** (large scale) → **Tasks** (medium scale) → **Subtasks** (small scale), with all items stored as markdown files and metadata tracked in JSON indices.

## Three-Tier Hierarchy

- **📋 Plans**: Large-scale initiatives (e.g., "voice-assistant-migration")
- **🔧 Tasks**: Medium-scale work items within plans (e.g., "setup-infrastructure")
- **✅ Subtasks**: Small, actionable items within tasks (e.g., "setup-monorepo")

## Available Commands

The hierarchical task system provides focused commands for managing all three levels:

### 📝 `/task-create` - Create plans, tasks, or subtasks

```bash
/task-create plan "plan-name" [--priority=high|medium|low] [--tags=tag1,tag2]
/task-create task "plan-name/task-name" [--priority=high|medium|low] [--tags=tag1,tag2]
/task-create subtask "plan-name/task-name/subtask-name" [--priority=high|medium|low] [--tags=tag1,tag2]
```

Creates hierarchical work items with appropriate templates and updates status indices.

### 🔄 `/task-update` - Update status or metadata at any level

```bash
/task-update "plan-name" --status=planning|in-progress|blocked|completed [--progress=0-100]
/task-update "plan-name/task-name" --status=planning|in-progress|blocked|completed [--progress=0-100]
/task-update "plan-name/task-name/subtask-name" --status=planning|in-progress|blocked|completed [--progress=0-100]
```

Updates status, progress, priority with automatic propagation up the hierarchy.

### 📋 `/task-list` - List and filter hierarchically

```bash
/task-list [--type=plans|tasks|subtasks|all] [--status=active|completed|all] [--priority=high|medium|low] [--tag=tagname]
/task-list --plan="plan-name"                    # Show all tasks/subtasks in plan
/task-list --task="plan-name/task-name"          # Show all subtasks in task
```

Displays hierarchical view with tree structure and filtering options.

### 👁️ `/task-show` - View details at any level

```bash
/task-show "plan-name"
/task-show "plan-name/task-name"
/task-show "plan-name/task-name/subtask-name"
```

Shows complete information including hierarchical context and progress history.

### ✍️ `/task-log` - Add progress entries at any level

```bash
/task-log "plan-name" "high-level milestone achieved"
/task-log "plan-name/task-name" "task progress update"
/task-log "plan-name/task-name/subtask-name" "specific work completed"
```

Appends timestamped progress updates with hierarchical context.

### 🔍 `/task-search` - Search across all levels

```bash
/task-search "search-term" [--type=plans|tasks|subtasks|all] [--in=title|content|tags|all] [--status=active|all]
```

Searches hierarchically across plans, tasks, and subtasks with highlighted results.

### 📦 `/task-archive` - Archive completed items

```bash
/task-archive "plan-name"                       # Archive entire completed plan
/task-archive "plan-name/task-name"             # Archive completed task
/task-archive --all-completed | --older-than=30d
```

Moves completed items to archive folders with hierarchical organization.

## Quick Start - Hierarchical Workflow

1. **Create a plan for your project**:
   ```bash
   /task-create plan "voice-assistant-migration" --priority=high --tags=project,migration
   ```

2. **Break down into major tasks**:
   ```bash
   /task-create task "voice-assistant-migration/setup-infrastructure" --priority=high --tags=setup
   /task-create task "voice-assistant-migration/build-features" --priority=medium --tags=features
   ```

3. **Create actionable subtasks**:
   ```bash
   /task-create subtask "voice-assistant-migration/setup-infrastructure/setup-monorepo" --priority=high
   /task-create subtask "voice-assistant-migration/setup-infrastructure/configure-deployment" --priority=medium
   ```

4. **Work on subtasks and track progress**:
   ```bash
   /task-update "voice-assistant-migration/setup-infrastructure/setup-monorepo" --status=in-progress
   /task-log "voice-assistant-migration/setup-infrastructure/setup-monorepo" "Created monorepo structure"
   /task-update "voice-assistant-migration/setup-infrastructure/setup-monorepo" --status=completed
   ```

5. **View hierarchical progress**:
   ```bash
   /task-list --plan="voice-assistant-migration"  # See overall plan progress
   /task-list --task="voice-assistant-migration/setup-infrastructure"  # See task progress
   ```

6. **Complete and archive**:
   ```bash
   /task-update "voice-assistant-migration" --status=completed
   /task-archive "voice-assistant-migration"
   ```

## Hierarchical File Structure

```
/tasks/
├── status.json                           # Global plan index
├── voice-assistant-migration/            # Plan directory
│   ├── plan.md                          # Plan overview
│   ├── status.json                      # Plan-specific task/subtask index
│   ├── setup-infrastructure/            # Task directory
│   │   ├── task.md                     # Task overview
│   │   ├── setup-monorepo.md           # Subtask
│   │   └── configure-deployment.md     # Subtask
│   ├── build-features/
│   │   ├── task.md
│   │   ├── voice-ui-components.md
│   │   ├── audio-streaming.md
│   │   └── state-management.md
│   └── archive/                         # Plan-specific archives
│       └── 2025-01/
│           └── completed-task/
└── another-plan/                        # Another plan
    ├── plan.md
    ├── status.json
    └── [tasks and subtasks]
```

## File Formats by Level

### Plan Format (`/tasks/[plan-name]/plan.md`)

```markdown
# Plan: [Human Readable Title]

**Status**: planning|in-progress|blocked|completed
**Created**: YYYY-MM-DD
**Updated**: YYYY-MM-DD
**Priority**: high|medium|low
**Tags**: tag1, tag2

## Overview

High-level description of plan goals and scope

## Success Criteria

- [ ] Measurable outcomes
- [ ] Completion criteria

## Tasks

This plan contains the following tasks:

- See task directories for detailed breakdowns

## Dependencies & Constraints

External dependencies, timeline requirements

## Progress Log

### YYYY-MM-DDTHH:MM:SSZ

- Plan-level milestone entries
```

### Task Format (`/tasks/[plan]/[task]/task.md`)

```markdown
# Task: [Human Readable Title]

**Plan**: [plan-name]
**Status**: planning|in-progress|blocked|completed
**Created**: YYYY-MM-DD
**Updated**: YYYY-MM-DD
**Priority**: high|medium|low
**Tags**: tag1, tag2

## Context

Medium-scale description of task scope

## Subtasks

- [ ] List of subtask files in this directory

## Dependencies

Prerequisites from other tasks

## Progress Log

### YYYY-MM-DDTHH:MM:SSZ

- Task-level progress entries
```

### Subtask Format (`/tasks/[plan]/[task]/[subtask].md`)

```markdown
# Subtask: [Human Readable Title]

**Plan**: [plan-name]
**Task**: [task-name]
**Status**: planning|in-progress|blocked|completed
**Created**: YYYY-MM-DD
**Updated**: YYYY-MM-DD
**Priority**: high|medium|low
**Tags**: tag1, tag2

## Context

Specific, actionable work item description

## Action Items

- [ ] Concrete, verifiable steps
- [ ] Completable in single session

## Progress Log

### YYYY-MM-DDTHH:MM:SSZ

- Detailed implementation progress
```

## Hierarchical Status Indices

### Global Status (`/tasks/status.json`)

Tracks all plans and high-level statistics:

```json
{
  "version": "2.0",
  "lastUpdated": "ISO timestamp",
  "plans": {
    "voice-assistant-migration": {
      "title": "Voice Assistant Migration",
      "status": "in-progress",
      "priority": "high",
      "created": "2025-01-01",
      "updated": "2025-01-07",
      "tags": ["migration", "voice"],
      "progress": 45,
      "tasksCount": 3,
      "subtasksCount": 8
    }
  },
  "statistics": {
    "plans": {
      "total": 2,
      "active": 1,
      "completed": 1
    }
  }
}
```

### Plan Status (`/tasks/[plan-name]/status.json`)

Tracks tasks and subtasks within a plan:

```json
{
  "version": "2.0",
  "plan": "voice-assistant-migration",
  "lastUpdated": "ISO timestamp",
  "tasks": {
    "setup-infrastructure": {
      "title": "Setup Infrastructure",
      "status": "completed",
      "priority": "high",
      "progress": 100,
      "subtasksCount": 2
    }
  },
  "subtasks": {
    "setup-infrastructure/setup-monorepo": {
      "title": "Setup Monorepo",
      "task": "setup-infrastructure",
      "status": "completed",
      "priority": "high",
      "progress": 100
    }
  },
  "statistics": {
    "tasks": { "total": 3, "completed": 1 },
    "subtasks": { "total": 8, "completed": 3 }
  }
}
```

## Integration with TodoWrite

The hierarchical system automatically syncs with Claude's session todo list:

- **Plan-level todos**: High-level strategic items
- **Task-level todos**: Medium-scope work items
- **Subtask-level todos**: Specific actionable items

Progress flows upward: completing subtasks updates task progress, which updates plan progress, and all changes sync to TodoWrite for session tracking.

## Best Practices

1. **Hierarchical Naming**: Use descriptive, hyphenated names at each level
   - Plans: "voice-assistant-migration", "api-redesign-project"
   - Tasks: "setup-infrastructure", "build-core-features"
   - Subtasks: "setup-monorepo", "implement-authentication"

2. **Granularity**: Follow the three-tier structure
   - Plans: 2-6 months of work, strategic scope
   - Tasks: 1-4 weeks of work, feature/component scope
   - Subtasks: 1-3 days of work, specific actionable items

3. **Progress Tracking**: Update at the appropriate level
   - Subtask updates flow up to tasks and plans automatically
   - Use `/task-log` for detailed progress at each level

4. **Organization**: Use consistent tagging and dependencies
   - Tag by domain: backend, frontend, infrastructure
   - Mark dependencies between items clearly

5. **Archiving**: Archive completed items to maintain focus
   - Archive entire plans when projects complete
   - Keep active workspace clean and focused

## Common Hierarchical Workflows

### Large Project Workflow

```bash
# 1. Create the project plan
/task-create plan "api-redesign" --priority=high --tags=project,api

# 2. Break into major phases
/task-create task "api-redesign/design-phase" --priority=high --tags=design
/task-create task "api-redesign/implementation" --priority=high --tags=development
/task-create task "api-redesign/migration" --priority=medium --tags=migration

# 3. Create specific subtasks
/task-create subtask "api-redesign/design-phase/api-specification" --priority=high
/task-create subtask "api-redesign/design-phase/database-schema" --priority=high
/task-create subtask "api-redesign/implementation/user-endpoints" --priority=high
/task-create subtask "api-redesign/implementation/auth-system" --priority=medium

# 4. Work through subtasks
/task-update "api-redesign/design-phase/api-specification" --status=in-progress
/task-log "api-redesign/design-phase/api-specification" "Completed user endpoints spec"
/task-update "api-redesign/design-phase/api-specification" --status=completed

# 5. Monitor overall progress
/task-list --plan="api-redesign"  # See hierarchical progress
```

### Bug Fix as Subtask

```bash
# Add bug fix as subtask to existing maintenance task
/task-create subtask "maintenance/bug-fixes/fix-login-issue" --priority=high --tags=bug,auth
/task-update "maintenance/bug-fixes/fix-login-issue" --status=in-progress
/task-log "maintenance/bug-fixes/fix-login-issue" "Reproduced issue, identified root cause"
/task-update "maintenance/bug-fixes/fix-login-issue" --status=completed
```

### Multi-Agent Collaboration

```bash
# Agent A works on infrastructure
/task-list --task="api-redesign/implementation" 
/task-update "api-redesign/implementation/auth-system" --status=in-progress

# Agent B works on features in parallel
/task-update "api-redesign/implementation/user-endpoints" --status=in-progress

# Both agents can see overall plan progress
/task-list --plan="api-redesign"
```

## Integration with Plan Framework

Use `/plan [project-description]` to automatically analyze a codebase and create a hierarchical plan with integrated task structure. This provides seamless integration between high-level planning and detailed task execution.

For detailed help on any command, simply run the command without arguments or refer to the individual command files in `claude/commands/`.
