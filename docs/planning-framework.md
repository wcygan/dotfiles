# Planning Framework

A hierarchical task management system for organizing and executing complex projects with multi-agent coordination support.

## Overview

The Planning Framework provides a three-tier hierarchical structure for managing work at different scales, from strategic planning to tactical execution. It integrates seamlessly with Claude's task management commands and TodoWrite system for comprehensive project coordination.

## Three-Tier Hierarchy

### 📋 Plans (Large Scale)

- **Scope**: 2-6 months of work, strategic initiatives
- **Examples**: "voice-assistant-migration", "api-redesign-project"
- **Purpose**: High-level project coordination and progress tracking

### 🔧 Tasks (Medium Scale)

- **Scope**: 1-4 weeks of work, feature/component level
- **Examples**: "setup-infrastructure", "build-core-features"
- **Purpose**: Break down plans into manageable work units

### ✅ Subtasks (Small Scale)

- **Scope**: 1-3 days of work, specific actionable items
- **Examples**: "setup-monorepo", "implement-authentication"
- **Purpose**: Concrete, verifiable work items

## File Organization

```
/tasks/
├── status.json                           # Global plan index
├── voice-assistant-migration/            # Plan directory
│   ├── plan.md                          # Plan overview
│   ├── status.json                      # Plan-specific index
│   ├── setup-infrastructure/            # Task directory
│   │   ├── task.md                     # Task overview
│   │   ├── setup-monorepo.md           # Subtask
│   │   └── configure-deployment.md     # Subtask
│   └── build-features/
│       ├── task.md
│       ├── voice-ui-components.md
│       └── audio-streaming.md
```

## Core Commands

### Creating Hierarchical Work Items

```bash
# Create a plan
/task-create plan "voice-assistant-migration" --priority=high --tags=project,migration

# Create tasks within the plan
/task-create task "voice-assistant-migration/setup-infrastructure" --priority=high --tags=setup
/task-create task "voice-assistant-migration/build-features" --priority=medium --tags=features

# Create actionable subtasks
/task-create subtask "voice-assistant-migration/setup-infrastructure/setup-monorepo" --priority=high
/task-create subtask "voice-assistant-migration/build-features/voice-ui-components" --priority=medium
```

### Managing Progress

```bash
# Update status at any level
/task-update "voice-assistant-migration/setup-infrastructure/setup-monorepo" --status=completed
/task-update "voice-assistant-migration/setup-infrastructure" --status=in-progress

# View hierarchical progress
/task-list --plan="voice-assistant-migration"
/task-list --task="voice-assistant-migration/setup-infrastructure"

# Add progress logs
/task-log "voice-assistant-migration/setup-infrastructure/setup-monorepo" "Completed initial structure"
```

## Progress Propagation

The system automatically calculates progress up the hierarchy:

```
Subtask completion → Task progress → Plan progress → TodoWrite sync
```

- Completing subtasks updates parent task progress
- Completing tasks updates parent plan progress
- All changes sync with Claude's session todo list

## Multi-Agent Coordination

### Git Worktree Setup

```bash
# Agent A - Infrastructure work
git worktree add /tmp/agent-a-work feature/setup-infrastructure
cd /tmp/agent-a-work
/task-list --task="voice-assistant-migration/setup-infrastructure"

# Agent B - Feature development
git worktree add /tmp/agent-b-work feature/build-features
cd /tmp/agent-b-work  
/task-list --task="voice-assistant-migration/build-features"
```

### Coordination Points

- **Parallel Tasks**: Independent work streams that can run simultaneously
- **Join Points**: Synchronization points where parallel work merges
- **Status Files**: Shared progress tracking through JSON indices

## Integration with Plan Command

Use the `/plan` command to automatically analyze codebases and create hierarchical task structures:

```bash
/plan "Migrate voice assistant to new architecture"
```

This command will:

1. Analyze the codebase structure
2. Create a main plan with `/task-create plan`
3. Break down into logical tasks based on code organization
4. Suggest actionable subtasks for immediate execution

## File Formats

### Plan Format (`plan.md`)

```markdown
# Plan: Voice Assistant Migration

**Status**: in-progress
**Created**: 2025-01-07
**Updated**: 2025-01-07
**Priority**: high
**Tags**: migration, voice

## Overview

Migrate existing voice assistant to new microservices architecture

## Success Criteria

- [ ] Zero-downtime migration
- [ ] Performance improvements of 50%
- [ ] Full feature parity

## Tasks

- setup-infrastructure: Infrastructure preparation
- build-features: Core feature implementation

## Dependencies & Constraints

- Database migration must complete before feature rollout
- Security review required before production deployment
```

### Task Format (`task.md`)

```markdown
# Task: Setup Infrastructure

**Plan**: voice-assistant-migration
**Status**: in-progress
**Created**: 2025-01-07
**Updated**: 2025-01-07
**Priority**: high
**Tags**: infrastructure, setup

## Context

Prepare infrastructure components for voice assistant migration

## Subtasks

- [ ] setup-monorepo.md - Create monorepo structure
- [ ] configure-deployment.md - Set up deployment pipeline

## Dependencies

- None (can start immediately)
```

### Subtask Format (`subtask.md`)

```markdown
# Subtask: Setup Monorepo

**Plan**: voice-assistant-migration
**Task**: setup-infrastructure
**Status**: completed
**Created**: 2025-01-07
**Updated**: 2025-01-07
**Priority**: high
**Tags**: monorepo, structure

## Context

Create monorepo structure for voice assistant components

## Action Items

- [x] Initialize Nx workspace
- [x] Configure shared libraries
- [x] Set up build configuration

## Progress Log

### 2025-01-07T10:30:00Z

- Completed monorepo setup with Nx
- All tests passing
```

## Status Tracking

### Global Status (`/tasks/status.json`)

Tracks all plans and high-level statistics:

```json
{
  "version": "2.0",
  "lastUpdated": "2025-01-07T15:30:00Z",
  "plans": {
    "voice-assistant-migration": {
      "title": "Voice Assistant Migration",
      "status": "in-progress",
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

Tracks tasks and subtasks within a specific plan:

```json
{
  "version": "2.0",
  "plan": "voice-assistant-migration",
  "tasks": {
    "setup-infrastructure": {
      "status": "completed",
      "progress": 100,
      "subtasksCount": 2
    }
  },
  "subtasks": {
    "setup-infrastructure/setup-monorepo": {
      "task": "setup-infrastructure",
      "status": "completed",
      "progress": 100
    }
  }
}
```

## Best Practices

### Naming Conventions

- **Plans**: Use descriptive project names (`voice-assistant-migration`)
- **Tasks**: Use action-oriented names (`setup-infrastructure`, `build-features`)
- **Subtasks**: Use specific, actionable names (`setup-monorepo`, `implement-auth`)

### Granularity Guidelines

- **Plans**: Strategic scope, multiple months
- **Tasks**: Feature scope, 1-4 weeks
- **Subtasks**: Implementation scope, 1-3 days

### Progress Management

- Update subtasks frequently for accurate progress tracking
- Use `/task-log` for detailed progress notes
- Complete items promptly to maintain accurate hierarchy

### Tagging Strategy

Use consistent tags for filtering and organization:

- **Domain tags**: `backend`, `frontend`, `infrastructure`, `security`
- **Type tags**: `feature`, `bug`, `refactor`, `documentation`
- **Priority tags**: `critical`, `milestone`, `nice-to-have`

## Common Workflows

### Large Project Setup

```bash
# 1. Create project plan
/task-create plan "api-redesign" --priority=high --tags=project,api

# 2. Break into phases
/task-create task "api-redesign/design-phase" --priority=high --tags=design
/task-create task "api-redesign/implementation" --priority=high --tags=development

# 3. Create specific work items
/task-create subtask "api-redesign/design-phase/api-specification" --priority=high
/task-create subtask "api-redesign/implementation/user-endpoints" --priority=high

# 4. Track progress
/task-list --plan="api-redesign"
```

### Multi-Agent Collaboration

```bash
# Coordinate parallel work
/task-update "api-redesign/design-phase/api-specification" --status=in-progress  # Agent A
/task-update "api-redesign/implementation/user-endpoints" --status=in-progress   # Agent B

# Monitor overall progress
/task-list --plan="api-redesign"  # Shows work from both agents
```

### Completion and Archival

```bash
# Complete hierarchy bottom-up
/task-update "api-redesign/implementation/user-endpoints" --status=completed
/task-update "api-redesign/implementation" --status=completed
/task-update "api-redesign" --status=completed

# Archive completed work
/task-archive "api-redesign"
```

## Integration Points

### TodoWrite Synchronization

The framework automatically syncs with Claude's TodoWrite system:

- **Plan-level todos**: Strategic oversight items
- **Task-level todos**: Medium-scope coordination items
- **Subtask-level todos**: Specific actionable items

### Git Integration

- Use git worktrees for parallel agent work
- Branch naming aligns with task hierarchy
- Commit messages reference task paths

### CI/CD Integration

- Task completion can trigger automated builds
- Progress updates integrate with deployment pipelines
- Status tracking supports release management

## Future Enhancements

### Planned Features

- **Dependency graphing**: Visual task relationships
- **Time estimation**: Effort tracking and planning
- **Resource allocation**: Agent capacity management
- **Template system**: Reusable plan structures

### Migration Support

- **Flat-to-hierarchical conversion**: Migrate existing task lists
- **Import/export**: Share plans between projects
- **Backup/restore**: Preserve work history

## Troubleshooting

### Common Issues

- **Missing parent items**: Ensure plans exist before creating tasks
- **Progress inconsistency**: Use `/task-update` to recalculate hierarchy
- **Status conflicts**: Check for duplicate task names

### Recovery Procedures

- **Corrupted status files**: Regenerate from markdown files
- **Lost progress**: Recover from git history and logs
- **Sync issues**: Force TodoWrite refresh with status updates
