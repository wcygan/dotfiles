Analyze the codebase and create a comprehensive plan with integrated task management and multi-agent coordination for $ARGUMENTS:

1. **Codebase Analysis**:
   - Search for existing documentation (README.md, CONTRIBUTING.md, docs/)
   - Identify project structure and key components
   - Analyze package files (package.json, go.mod, Cargo.toml, etc.)
   - Review recent commits and open issues/PRs
   - Examine test coverage and CI/CD configuration
   - Identify architectural patterns and conventions

2. **Create Hierarchical Plan with Agent Assignments**:

   **Step 1: Create the main plan**
   ```bash
   /task-create plan "[project-name]" --priority=high --tags=project,multi-agent
   ```

   **Step 2: Break down into major tasks with agent considerations**
   ```bash
   /task-create task "[project-name]/setup-foundation" --priority=high --tags=setup,infrastructure,agent-a
   /task-create task "[project-name]/core-features" --priority=high --tags=features,development,agent-b
   /task-create task "[project-name]/testing-suite" --priority=high --tags=testing,quality,agent-c
   ```

   **Step 3: Create actionable subtasks with clear ownership**
   ```bash
   # Agent A - Foundation work
   /task-create subtask "[project-name]/setup-foundation/project-structure" --priority=high --assigned="agent-a"
   /task-create subtask "[project-name]/setup-foundation/dependency-setup" --priority=high --assigned="agent-a"

   # Agent B - Core features (parallel with A)
   /task-create subtask "[project-name]/core-features/api-implementation" --priority=high --assigned="agent-b"
   /task-create subtask "[project-name]/core-features/database-schema" --priority=high --assigned="agent-b"

   # Agent C - Testing (depends on A & B)
   /task-create subtask "[project-name]/testing-suite/unit-tests" --priority=high --assigned="agent-c"
   /task-create subtask "[project-name]/testing-suite/integration-tests" --priority=medium --assigned="agent-c"
   ```

3. **Generate Multi-Agent Coordination Structure**:

   **Enhanced Status.json with Agent Tracking**:
   ```json
   {
     "version": "3.0",
     "lastUpdated": "2025-01-07T15:30:00Z",
     "coordination": {
       "agents": {
         "agent-a": {
           "name": "claude-foundation",
           "worktree": "../project-foundation",
           "branch": "feature/setup-foundation",
           "assignedTasks": ["setup-foundation/*"],
           "status": "active"
         },
         "agent-b": {
           "name": "claude-features",
           "worktree": "../project-features",
           "branch": "feature/core-features",
           "assignedTasks": ["core-features/*"],
           "status": "active"
         }
       },
       "dependencies": {
         "testing-suite": ["setup-foundation", "core-features"]
       },
       "joinPoints": [
         {
           "phase": "integration",
           "requiredTasks": ["setup-foundation", "core-features"],
           "description": "Merge foundation and features before testing"
         }
       ]
     },
     "plans": {
       "[project-name]": {
         "title": "Project Implementation",
         "status": "in-progress",
         "progress": 0,
         "tasksCount": 3,
         "subtasksCount": 6,
         "agentAssignments": {
           "agent-a": ["setup-foundation"],
           "agent-b": ["core-features"],
           "agent-c": ["testing-suite"]
         }
       }
     }
   }
   ```

4. **Automatic Worktree and Launch Setup**:

   ```bash
   # Auto-generated worktree commands
   git worktree add ../project-foundation feature/setup-foundation
   git worktree add ../project-features feature/core-features
   git worktree add ../project-testing feature/testing-suite

   # Launch instructions with task context
   # Terminal 1 - Agent A:
   cd ../project-foundation && claude
   > /task-list --assigned="agent-a"
   > /agent-status

   # Terminal 2 - Agent B:
   cd ../project-features && claude
   > /task-list --assigned="agent-b"
   > /agent-status

   # Terminal 3 - Agent C:
   cd ../project-testing && claude
   > /task-list --assigned="agent-c" --wait-for="setup-foundation,core-features"
   > /agent-status
   ```

5. **Unified Coordination File**:

   Create `/tasks/[project-name]/coordination.md`:
   ```markdown
   # Multi-Agent Coordination Plan

   ## Agent Assignments

   ### Agent A - Foundation (claude-foundation)

   - Worktree: `../project-foundation`
   - Branch: `feature/setup-foundation`
   - Tasks: All items under `setup-foundation/`
   - Can start: Immediately

   ### Agent B - Features (claude-features)

   - Worktree: `../project-features`
   - Branch: `feature/core-features`
   - Tasks: All items under `core-features/`
   - Can start: Immediately (parallel with Agent A)

   ### Agent C - Testing (claude-testing)

   - Worktree: `../project-testing`
   - Branch: `feature/testing-suite`
   - Tasks: All items under `testing-suite/`
   - Can start: After Agent A & B reach join point

   ## Communication Protocol

   - Task updates: Use `/task-update` commands (auto-sync via status.json)
   - Blockers: Use `/task-log` to document issues
   - Progress: Check `/agent-status` for real-time view
   - Join points: System enforces dependencies automatically

   ## Dependency Graph
   ```
   setup-foundation ──┐
   ├──> testing-suite ──> final-integration
   core-features ─────┘
   ```
   ```

6. **Progress Monitoring Integration**:

   ```bash
   # Check overall plan progress with agent details
   /task-list --plan="[project-name]" --show-agents

   # Check specific agent progress
   /agent-status --agent="agent-a"

   # View dependency readiness
   /task-dependencies --task="testing-suite"

   # Monitor join point status
   /task-list --join-points --plan="[project-name]"
   ```

7. **Automatic Synchronization**:

   - Task completion automatically updates all status files
   - Agent progress visible to all other agents via status.json
   - Join points enforced through dependency tracking
   - No manual coordination files needed in /tmp

## Benefits of Integrated Approach

1. **Single Source of Truth**: Task hierarchy serves as both plan and coordination
2. **Automatic Progress Tracking**: No duplicate status updates needed
3. **Clear Agent Ownership**: Tasks assigned at creation time
4. **Dependency Management**: System enforces proper execution order
5. **Simplified Commands**: Agents just work on assigned tasks

Would you like me to create this plan with multi-agent coordination for your project?
