Set up parallel development workflow integrated with planning framework:

1. **Check for Existing Plan**:
   ```bash
   # First, check if a plan exists in the task hierarchy
   PROJECT=$(basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $PWD)

   if [ -f "/tasks/$PROJECT/plan.md" ]; then
     echo "Found existing plan: /tasks/$PROJECT/plan.md"
     /task-list --plan="$PROJECT" --show-structure
   else
     echo "No plan found. Create one with: /plan-multi-agent [description]"
     exit 1
   fi
   ```

2. **Analyze Plan for Parallelization**:
   - Read plan's status.json for agent assignments
   - Identify tasks marked for parallel execution
   - Check dependency constraints
   - Determine optimal worktree structure

3. **Automatic Worktree Creation Based on Plan**:

   ```bash
   # Read agent assignments from plan
   AGENTS=$(jq -r '.coordination.agents | keys[]' /tasks/$PROJECT/status.json)

   for AGENT in $AGENTS; do
     WORKTREE=$(jq -r ".coordination.agents[\"$AGENT\"].worktree" /tasks/$PROJECT/status.json)
     BRANCH=$(jq -r ".coordination.agents[\"$AGENT\"].branch" /tasks/$PROJECT/status.json)
     
     echo "Setting up worktree for $AGENT:"
     
     # Check if worktree already exists
     if git worktree list | grep -q "$WORKTREE"; then
       echo "  Worktree already exists at $WORKTREE"
       continue
     fi
     
     # Create branch if it doesn't exist
     if ! git show-ref --verify --quiet "refs/heads/$BRANCH"; then
       echo "  Creating branch $BRANCH"
       git branch $BRANCH
     fi
     
     # Create worktree
     git worktree add $WORKTREE $BRANCH
     echo "  Created worktree at $WORKTREE on branch $BRANCH"
   done
   ```

4. **Create Work-Stealing Launch Script**:

   ```bash
   # Create coordination directory for this project
   COORD_DIR=".claude-agents"
   mkdir -p $COORD_DIR

   # Create atomic task registry
   cat > $COORD_DIR/task-registry.json << EOF
   {
     "version": "1.0",
     "lastUpdated": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
     "agents": {},
     "claimedTasks": {}
   }
   EOF

   # Create the launch script
   cat > $COORD_DIR/launch-agent.sh << 'SCRIPT'
   #!/bin/bash
   set -e

   # Project and coordination setup
   PROJECT=$(basename $(git rev-parse --show-toplevel))
   COORD_DIR=".claude-agents"
   REGISTRY="$COORD_DIR/task-registry.json"
   LOCK_FILE="$COORD_DIR/registry.lock"

   # Generate unique agent ID
   AGENT_ID="agent-$(date +%s)-$$"
   AGENT_NAME="claude-worker-$(shuf -i 1000-9999 -n 1)"

   # Function to acquire lock for atomic operations
   acquire_lock() {
     local timeout=30
     local elapsed=0
     while ! mkdir "$LOCK_FILE" 2>/dev/null; do
       sleep 0.1
       elapsed=$((elapsed + 1))
       if [ $elapsed -gt $((timeout * 10)) ]; then
         echo "Failed to acquire lock after ${timeout}s"
         exit 1
       fi
     done
   }

   release_lock() {
     rmdir "$LOCK_FILE" 2>/dev/null || true
   }

   # Function to claim next available task
   claim_next_task() {
     acquire_lock
     
     # Read current registry
     local registry=$(cat "$REGISTRY")
     
     # Find unclaimed, unblocked tasks
     local available_tasks=$(jq -r '
       .tasks 
       | to_entries[] 
       | select(.value.status == "pending" and 
                (.value.claimed == null or .value.claimed == false) and
                (.value.blockedBy == null or .value.blockedBy == []))
       | .key
     ' /tasks/$PROJECT/status.json 2>/dev/null | head -1)
     
     if [ -z "$available_tasks" ]; then
       release_lock
       return 1
     fi
     
     # Claim the task
     local task="$available_tasks"
     jq --arg agent "$AGENT_ID" --arg task "$task" '
       .agents[$agent] = {
         "name": env.AGENT_NAME,
         "startTime": now | todate,
         "currentTask": $task
       } |
       .claimedTasks[$task] = {
         "agent": $agent,
         "claimedAt": now | todate
       }
     ' <<< "$registry" > "$REGISTRY.tmp"
     
     mv "$REGISTRY.tmp" "$REGISTRY"
     release_lock
     
     echo "$task"
   }

   # Create worktree for this agent
   WORKTREE="../$PROJECT-$AGENT_ID"
   BRANCH="work/$AGENT_ID"

   echo "🚀 Launching $AGENT_NAME"
   echo "   ID: $AGENT_ID"
   echo "   Worktree: $WORKTREE"

   # Create branch and worktree
   git branch $BRANCH 2>/dev/null || true
   git worktree add "$WORKTREE" "$BRANCH"

   # Claim first task
   TASK=$(claim_next_task)

   if [ -z "$TASK" ]; then
     echo "❌ No available tasks found"
     echo ""
     echo "Possible reasons:"
     echo "- All tasks are already claimed by other agents"
     echo "- Remaining tasks are blocked by incomplete dependencies"
     echo "- All tasks are completed"
     echo ""
     echo "Run '/task-list --status=pending --show-dependencies' to see blocked tasks"
     git worktree remove "$WORKTREE" --force
     exit 0
   fi

   # Launch Claude with work-stealing prompt
   cd "$WORKTREE"

   PROMPT="You are $AGENT_NAME (ID: $AGENT_ID) working on project $PROJECT.
   ```

I've claimed the task: $TASK

First, initialize yourself as an agent and begin work:

1. Run: /agent-init $AGENT_ID --name='$AGENT_NAME'
2. Update the task status: /task-update '$TASK' --status=in-progress
3. Read the task details and complete it
4. When done, run: /task-update '$TASK' --status=completed

After completing this task:

1. Check for more available work with: /task-list --status=pending --unassigned
2. If tasks are available, claim the next one
3. If no tasks available, check blocked tasks and report why you're stopping
4. Clean up with: /agent-complete $AGENT_ID

Work in a focused, autonomous manner. Complete one task fully before moving to the next."

claude prompt "$PROMPT" --mode=interactive
SCRIPT

chmod +x $COORD_DIR/launch-agent.sh

# Add coordination directory to .gitignore if not already there

if ! grep -q "^\.claude-agents/" .gitignore 2>/dev/null; then
echo ".claude-agents/" >> .gitignore
echo "✅ Added .claude-agents/ to .gitignore"
fi

echo "✅ Created work-stealing launch script: $COORD_DIR/launch-agent.sh"

````
5. **Generate Simple Launch Instructions**:

```bash
echo ""
echo "=== Work-Stealing Agent Launch ==="
echo ""
echo "To launch agents, simply run:"
echo "  ./$COORD_DIR/launch-agent.sh"
echo ""
echo "Launch multiple agents in parallel:"
echo "  # Terminal 1"
echo "  ./$COORD_DIR/launch-agent.sh"
echo ""
echo "  # Terminal 2" 
echo "  ./$COORD_DIR/launch-agent.sh"
echo ""
echo "  # Terminal 3"
echo "  ./$COORD_DIR/launch-agent.sh"
echo ""
echo "Each agent will:"
echo "- Automatically claim an available task"
echo "- Work independently in its own worktree"
echo "- Complete tasks and claim new ones"
echo "- Exit gracefully when no work remains"
````

6. **Work-Stealing Agent Behavior**:

   The launch script creates agents that:
   - Automatically generate unique IDs
   - Atomically claim available tasks using file locking
   - Work independently without pre-assignment
   - Continue claiming tasks until none remain
   - Handle dependencies by skipping blocked tasks
   - Exit gracefully when blocked or complete

7. **Monitor Work-Stealing Progress**:

   ```bash
   # View active agents and their current tasks
   cat .claude-agents/task-registry.json | jq '.agents'

   # Output:
   # {
   #   "agent-1234-5678": {
   #     "name": "claude-worker-3421",
   #     "startTime": "2025-01-07T10:00:00Z",
   #     "currentTask": "setup-foundation/project-structure"
   #   },
   #   "agent-1234-5679": {
   #     "name": "claude-worker-8765",
   #     "startTime": "2025-01-07T10:00:15Z", 
   #     "currentTask": "core-features/api-implementation"
   #   }
   # }

   # Check which tasks are claimed
   cat .claude-agents/task-registry.json | jq '.claimedTasks'
   ```

8. **Advantages of Work-Stealing Approach**:

   - **No Manual Assignment**: Agents claim work dynamically
   - **Automatic Load Balancing**: Fast agents naturally take more tasks
   - **Resilient**: If an agent fails, uncompleted tasks become available
   - **Simple Launch**: One command starts any number of agents
   - **Zero Configuration**: No need to pre-assign tasks or create agent IDs

9. **Enhanced Parallel Workflow**:

   ```bash
   # Step 1: Create plan with tasks
   /plan-multi-agent "Implement new feature set"

   # Step 2: Set up parallel environment and launch script
   /parallel-enhanced

   # Step 3: Launch agents (as many as needed)
   # Terminal 1:
   ./.claude-agents/launch-agent.sh

   # Terminal 2:
   ./.claude-agents/launch-agent.sh

   # Terminal 3:
   ./.claude-agents/launch-agent.sh

   # Each agent automatically:
   # - Claims an available task
   # - Completes it
   # - Claims the next available task
   # - Exits when no tasks remain
   ```

10. **Join Point Management**:

    ```bash
    # Check if ready for join point
    /join-status --point="integration"

    # Output:
    # Join Point: integration
    # Status: Not Ready
    # 
    # Required Tasks:
    # ✓ setup-foundation/project-structure (agent-a) - completed
    # ✓ setup-foundation/dependency-setup (agent-a) - completed  
    # ⚡ core-features/api-implementation (agent-b) - in-progress (80%)
    # ⏸️ core-features/database-schema (agent-b) - pending
    #
    # Estimated ready: 2 hours
    ```

11. **Cleanup Integration**:

    ```bash
    # Clean up completed agent work
    /agent-complete agent-a

    # This will:
    # - Mark all agent-a tasks as reviewed
    # - Create PR from agent's branch
    # - Safely remove worktree
    # - Merge or archive branch
    # - Update coordination status

    # Full cleanup process:
    WORKTREE=$(jq -r '.coordination.agents["agent-a"].worktree' /tasks/$PROJECT/status.json)
    BRANCH=$(jq -r '.coordination.agents["agent-a"].branch' /tasks/$PROJECT/status.json)

    # Create PR
    gh pr create --title "Agent A: Foundation Setup Complete" \
                 --body "Completed tasks: setup-foundation/*" \
                 --base main --head $BRANCH

    # Remove worktree safely
    cd $MAIN_WORKTREE  # Return to main worktree first
    git worktree remove $WORKTREE --force

    # Clean up tracking
    git worktree prune
    ```

## Key Improvements

1. **Plan-Driven**: Reads from existing task hierarchy instead of manual setup
2. **Work-Stealing**: Agents dynamically claim tasks without pre-assignment
3. **One-Command Launch**: Simple script starts intelligent agents
4. **Atomic Operations**: File locking ensures no task conflicts
5. **Self-Managing**: Agents handle their own lifecycle and cleanup

## Usage Example

```bash
# Old workflow (manual coordination):
/plan "Build feature"
/coordinate  # Manually assign tasks
/parallel    # Manually set up worktrees
# Launch each agent with specific assignments

# New workflow (work-stealing):
/plan-multi-agent "Build feature"  # Creates plan with tasks
/parallel-enhanced                 # Creates launch script

# Launch as many agents as needed:
./.claude-agents/launch-agent.sh  # Agent 1
./.claude-agents/launch-agent.sh  # Agent 2
./.claude-agents/launch-agent.sh  # Agent 3
# Agents automatically claim and complete all tasks
```

## Work-Stealing Benefits

1. **Dynamic Scaling**: Launch more agents if needed mid-project
2. **Fault Tolerance**: Failed agents don't block progress
3. **No Coordination**: Agents self-organize via task claims
4. **Optimal Distribution**: Work naturally flows to available agents
5. **Simple Operation**: One script handles everything

This creates a truly autonomous multi-agent system where agents collaborate through the task queue!
