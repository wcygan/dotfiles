# Agentic CLI - Action Plan

## Executive Summary

This document outlines a comprehensive action plan for building `agentic-cli`, a Deno/TypeScript command-line tool that manages hierarchical task planning and autonomous agent coordination. The tool will compile to a standalone binary for cross-platform distribution.

## Project Overview

**Goal**: Create a CLI tool that enables multi-agent software development workflows through:

- Hierarchical task management (plans → tasks → subtasks) stored as JSON in git
- Autonomous agent launching with context-aware prompts
- Git worktree management for isolated agent workspaces
- Automated testing and merge conflict resolution guidance

## Architecture Design

### Core Components

```
agentic-cli/
├── src/
│   ├── cli.ts                 # Main entry point
│   ├── commands/
│   │   ├── plan.ts           # Plan management commands
│   │   ├── task.ts           # Task CRUD operations
│   │   ├── agent.ts          # Agent launching/management
│   │   ├── status.ts         # Progress monitoring
│   │   └── merge.ts          # Merge assistance
│   ├── core/
│   │   ├── task-manager.ts   # Task hierarchy logic
│   │   ├── agent-launcher.ts # Agent orchestration
│   │   ├── git-ops.ts        # Git worktree operations
│   │   └── storage.ts        # JSON persistence
│   ├── types/
│   │   ├── plan.ts           # Type definitions
│   │   ├── task.ts           # Task interfaces
│   │   └── agent.ts          # Agent types
│   └── utils/
│       ├── prompts.ts        # Prompt generation
│       ├── logger.ts         # Logging utilities
│       └── config.ts         # Configuration
├── tests/
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── e2e/                  # End-to-end tests
├── deno.json                 # Deno configuration
└── build.ts                  # Build script
```

### Data Model

```typescript
// Plan structure
interface Plan {
  id: string;
  name: string;
  description: string;
  status: "pending" | "active" | "completed";
  created: string;
  updated: string;
  tasks: string[]; // Task IDs
  metadata: Record<string, any>;
}

// Task structure
interface Task {
  id: string;
  planId: string;
  name: string;
  description: string;
  status: "pending" | "assigned" | "in-progress" | "completed";
  assignedTo?: string;
  subtasks: string[]; // Subtask IDs
  dependencies: string[];
  estimatedHours?: number;
  created: string;
  updated: string;
}

// Subtask structure
interface Subtask {
  id: string;
  taskId: string;
  name: string;
  description: string;
  status: "pending" | "in-progress" | "completed";
  assignedTo?: string;
  branch?: string;
  worktree?: string;
  testCommand?: string;
  completionCriteria: string[];
}
```

## Development Phases

### Phase 1: Core Task Management (Week 1)

**1.1 Project Setup**

- Initialize Deno project with TypeScript configuration
- Set up directory structure
- Configure linting, formatting, and git hooks
- Create basic CLI framework using Cliffy or custom parser

**1.2 Task Management Implementation**

```typescript
// Example commands to implement
agentic plan create "Build authentication system"
agentic task create --plan <id> "Implement JWT tokens"
agentic subtask create --task <id> "Write token generation logic"
agentic task list --status pending
agentic task assign <id> --agent "agent-1"
```

**1.3 JSON Storage Layer**

- Implement file-based storage in `.agentic/` directory
- Create atomic read/write operations
- Add git integration for automatic commits
- Implement data validation and migrations

### Phase 2: Agent Launch System (Week 2)

**2.1 Git Worktree Management**

```typescript
// Worktree creation logic
async function createAgentWorktree(subtask: Subtask): Promise<string> {
  const repoName = await getRepoName();
  const worktreePath = `~/tmp/${repoName}/${subtask.id}`;
  const branchName = `agent/${subtask.id}`;

  await git.createBranch(branchName);
  await git.addWorktree(worktreePath, branchName);

  return worktreePath;
}
```

**2.2 Context-Aware Prompt Generation**

```typescript
// Generate comprehensive agent prompt
function generateAgentPrompt(subtask: Subtask, context: Context): string {
  return `
You are an autonomous agent working on: ${subtask.name}

## Context
Repository: ${context.repoName}
Branch: ${subtask.branch}
Worktree: ${subtask.worktree}

## Task Details
${subtask.description}

## Completion Criteria
${subtask.completionCriteria.map((c) => `- ${c}`).join("\n")}

## Testing
After implementation, run: ${subtask.testCommand}
Ensure all tests pass before marking complete.

## Merge Process
1. Commit all changes with descriptive messages
2. Run: agentic task complete ${subtask.id}
3. If conflicts occur, run: agentic merge assist

## Available Commands
- agentic status - Check current progress
- agentic task update ${subtask.id} --status in-progress
- agentic help - Get assistance
`;
}
```

**2.3 Agent Launch Command**

```typescript
// Launch agent with context
agentic agent launch --subtask <id>
// This will:
// 1. Create worktree
// 2. Generate prompt
// 3. Execute: cd <worktree> && claude prompt "<generated-prompt>"
```

### Phase 3: Testing & Merge Support (Week 3)

**3.1 Test Integration**

```typescript
// Test configuration in subtasks
interface TestConfig {
  command: string; // e.g., "deno test"
  coverage?: boolean; // require coverage threshold
  preTest?: string[]; // setup commands
  postTest?: string[]; // cleanup commands
}
```

**3.2 Merge Conflict Resolution**

```typescript
// Merge assistance command
agentic merge assist --subtask <id>
// Provides:
// 1. Conflict detection
// 2. Resolution strategies
// 3. Test verification
// 4. Rollback options
```

**3.3 Completion Workflow**

```typescript
// Task completion flow
agentic task complete <id>
// 1. Run tests
// 2. Create PR or merge to main
// 3. Clean up worktree
// 4. Update task status
// 5. Notify other agents
```

## Testing Strategy

### Unit Tests

```typescript
// tests/unit/task-manager.test.ts
Deno.test("TaskManager creates tasks correctly", async () => {
  const manager = new TaskManager();
  const task = await manager.createTask({
    planId: "plan-1",
    name: "Test task",
    description: "Test description",
  });

  assertEquals(task.status, "pending");
  assert(task.id);
});
```

### Integration Tests

```typescript
// tests/integration/agent-launch.test.ts
Deno.test("Agent launch creates worktree and prompt", async () => {
  const subtask = await createTestSubtask();
  const result = await launchAgent(subtask.id);

  assert(await exists(result.worktreePath));
  assert(result.prompt.includes(subtask.name));
});
```

### End-to-End Tests

```typescript
// tests/e2e/full-workflow.test.ts
Deno.test("Complete workflow from plan to merge", async () => {
  // Create plan
  const plan = await cli("plan", "create", "Test plan");

  // Create task
  const task = await cli("task", "create", "--plan", plan.id, "Test task");

  // Launch agent
  const agent = await cli("agent", "launch", "--task", task.id);

  // Simulate work and completion
  await simulateAgentWork(agent);

  // Verify merge
  const status = await cli("status");
  assertEquals(status.tasks[0].status, "completed");
});
```

## Build & Distribution

### Compilation Script

```typescript
// build.ts
const targets = [
  "x86_64-pc-windows-msvc",
  "x86_64-apple-darwin",
  "x86_64-unknown-linux-gnu",
  "aarch64-apple-darwin",
];

for (const target of targets) {
  await Deno.run({
    cmd: [
      "deno",
      "compile",
      "--allow-read",
      "--allow-write",
      "--allow-run",
      "--allow-env",
      "--target",
      target,
      "--output",
      `dist/agentic-${target}`,
      "src/cli.ts",
    ],
  }).status();
}
```

### Installation Methods

1. **Direct Download**: GitHub releases with pre-compiled binaries
2. **Install Script**: `curl -fsSL https://agentic.dev/install.sh | sh`
3. **Package Managers**:
   - Homebrew: `brew install agentic-cli`
   - Cargo: `cargo install agentic-cli`
   - npm: `npm install -g agentic-cli`

## Command Reference

```bash
# Plan management
agentic plan create <name>
agentic plan list
agentic plan show <id>
agentic plan update <id> --status completed

# Task management
agentic task create --plan <plan-id> <name>
agentic task list [--status <status>]
agentic task assign <id> --agent <agent-id>
agentic task update <id> --status in-progress

# Subtask management
agentic subtask create --task <task-id> <name>
agentic subtask list --task <task-id>

# Agent operations
agentic agent launch --subtask <id>
agentic agent list --active
agentic agent status <id>

# Workflow commands
agentic status                    # Overall progress
agentic merge assist --subtask <id>
agentic task complete <id>

# Utility commands
agentic init                      # Initialize in current repo
agentic config set <key> <value>
agentic export --format json      # Export all data
```

## Configuration

### Global Config (`~/.agentic/config.json`)

```json
{
  "defaultEditor": "claude",
  "worktreeBase": "~/tmp",
  "autoCommit": true,
  "testTimeout": 300,
  "mergeStrategy": "interactive"
}
```

### Project Config (`.agentic/config.json`)

```json
{
  "projectName": "my-app",
  "testCommand": "deno test",
  "branches": {
    "main": "main",
    "feature": "feature/*"
  },
  "agents": {
    "maxConcurrent": 5,
    "defaultPromptTemplate": "default"
  }
}
```

## Security Considerations

1. **File Permissions**: Ensure `.agentic/` directory has appropriate permissions
2. **Git Integration**: Use SSH keys or tokens for git operations
3. **Agent Isolation**: Each agent works in isolated worktree
4. **Audit Logging**: Track all operations in `.agentic/audit.log`

## Success Metrics

1. **Functionality**: All core features working as specified
2. **Performance**: Task operations < 100ms, agent launch < 5s
3. **Reliability**: 99%+ success rate for git operations
4. **Usability**: Clear documentation and helpful error messages
5. **Portability**: Single binary < 25MB, works on all major platforms

## Timeline

- **Week 1**: Core task management and storage
- **Week 2**: Agent launching and git integration
- **Week 3**: Testing, merge support, and polish
- **Week 4**: Documentation, distribution, and release

## Next Steps

1. Set up project repository
2. Implement core task management
3. Create comprehensive test suite
4. Build agent launch system
5. Add merge conflict resolution
6. Create build pipeline
7. Write user documentation
8. Release v1.0.0

This action plan provides a clear roadmap for building a robust, tested, and user-friendly CLI tool for multi-agent development workflows.
