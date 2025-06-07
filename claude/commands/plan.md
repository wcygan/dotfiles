Analyze the codebase and create a comprehensive plan with integrated task management for $ARGUMENTS:

1. **Codebase Analysis**:
   - Search for existing documentation (README.md, CONTRIBUTING.md, docs/)
   - Identify project structure and key components
   - Analyze package files (package.json, go.mod, Cargo.toml, etc.)
   - Review recent commits and open issues/PRs
   - Examine test coverage and CI/CD configuration
   - Identify architectural patterns and conventions

2. **Create Plan with Integrated Task Framework**:
   - Generate plan using hierarchical task structure:
     - Create main plan with `/task-create plan "project-name"`
     - Break down into medium-scale tasks
     - Further decompose into actionable subtasks
   - Include project overview and current state assessment
   - Identify parallelizable tasks and dependencies
   - Define clear join points for multi-agent coordination
   - Estimate complexity and effort for each level

3. **Task Categorization**:
   - **Independent Tasks** (can run in parallel):
     - Unit test improvements
     - Documentation updates
     - Linting/formatting fixes
     - Independent feature modules
   - **Sequential Tasks** (must follow order):
     - Database migrations
     - API breaking changes
     - Build system updates
   - **Join Points** (synchronization required):
     - Integration testing after parallel work
     - Final build and deployment
     - Code review and merge

4. **Hierarchical Plan Creation Process**:

   **Step 1: Create the main plan**
   ```bash
   /task-create plan "[project-name]" --priority=high --tags=project,planning
   ```

   **Step 2: Break down into major tasks**
   ```bash
   /task-create task "[project-name]/setup-foundation" --priority=high --tags=setup,infrastructure
   /task-create task "[project-name]/core-features" --priority=high --tags=features,development
   /task-create task "[project-name]/optimization" --priority=medium --tags=performance,polish
   ```

   **Step 3: Create actionable subtasks**
   ```bash
   # Setup foundation subtasks
   /task-create subtask "[project-name]/setup-foundation/project-structure" --priority=high
   /task-create subtask "[project-name]/setup-foundation/dependency-setup" --priority=high
   /task-create subtask "[project-name]/setup-foundation/ci-pipeline" --priority=medium

   # Core features subtasks
   /task-create subtask "[project-name]/core-features/api-implementation" --priority=high
   /task-create subtask "[project-name]/core-features/database-schema" --priority=high
   /task-create subtask "[project-name]/core-features/authentication" --priority=medium
   ```

   **Step 4: Plan structure will be automatically organized as**:
   ```
   /tasks/[project-name]/
   ├── plan.md                           # High-level plan overview
   ├── status.json                       # Plan progress tracking
   ├── setup-foundation/
   │   ├── task.md                      # Task overview
   │   ├── project-structure.md         # Subtask details
   │   ├── dependency-setup.md          # Subtask details
   │   └── ci-pipeline.md              # Subtask details
   ├── core-features/
   │   ├── task.md
   │   ├── api-implementation.md
   │   ├── database-schema.md
   │   └── authentication.md
   └── optimization/
       ├── task.md
       └── [subtasks as created]
   ```

   **Step 5: Multi-Agent Coordination Setup**
   ```bash
   # Each agent works on different tasks using git worktrees
   # Agent A - Foundation work
   git worktree add /tmp/agent-a-work feature/setup-foundation
   cd /tmp/agent-a-work
   /task-list --task="[project-name]/setup-foundation"

   # Agent B - Core features
   git worktree add /tmp/agent-b-work feature/core-features  
   cd /tmp/agent-b-work
   /task-list --task="[project-name]/core-features"
   ```

5. **Advanced Planning Features with Task Integration**:
   - **Dependency Graph**: Use task dependencies to visualize relationships
   - **Risk Assessment**: Tag high-risk subtasks, track blockers
   - **Resource Allocation**: Assign agents to specific tasks/subtasks
   - **Progress Tracking**: Automatic progress aggregation from subtasks → tasks → plan
   - **Rollback Strategy**: Archive completed work, maintain plan structure

6. **Automatic Todo Integration**:

   **Plan Creation Automatically Syncs with TodoWrite**:
   - Plan-level todo: "Complete [project-name] plan"
   - Task-level todos: "Complete [task-name] in [project-name]"
   - Subtask-level todos: "[specific actionable item]"

   **Progress Flows Upward**:
   ```
   Subtask completed → Task progress updated → Plan progress updated → Todo progress updated
   ```

   **Use commands to manage**:
   ```bash
   /task-list --plan="[project-name]"     # See all plan items
   /task-update "[project-name]/task/subtask" --status=completed
   /task-list --status=active             # See what's left to do
   ```

7. **Monitoring and Updates with Task Framework**:
   - **Progress Visualization**: Use `/task-list --plan=[project-name]` for hierarchy view
   - **Blocker Management**: Use `/task-update --status=blocked` and `/task-log` for context
   - **Plan Reviews**: Regular `/task-list --status=all` to see completion status
   - **Dynamic Replanning**: Create new subtasks as needed, archive completed ones
   - **Statistics**: Automatic calculation of plan completion percentage

## Implementation Steps

1. **Analyze the codebase** to understand current state and requirements
2. **Create the main plan** with `/task-create plan "[project-name]"`
3. **Identify major phases** and create tasks for each
4. **Break down tasks** into specific, actionable subtasks
5. **Set up coordination** using git worktrees and task assignments
6. **Track progress** using the task command suite
7. **Coordinate completion** through join points and status updates

What specific aspects of the project should the plan focus on analyzing?
