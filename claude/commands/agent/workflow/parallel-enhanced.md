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

4. **Set Up Deno Task for Agent Launch**:

   ```bash
   # Ensure project has Deno configuration
   if [ ! -f "deno.json" ]; then
     echo "Creating deno.json for project..."
     cat > deno.json << 'EOF'
   ```

{
"version": "1.0.0",
"imports": {
"@std/path": "jsr:@std/path@^1.0.9",
"@std/fs": "jsr:@std/fs@^1.0.17",
"@std/fs/exists": "jsr:@std/fs@^1.0.17/exists",
"@std/fs/ensure-dir": "jsr:@std/fs@^1.0.17/ensure-dir"
},
"tasks": {
"agent": "deno run --allow-all scripts/launch-agent.ts"
}
}
EOF
else

# Add agent task to existing deno.json

if ! grep -q '"agent"' deno.json; then

# Use jq to add the task

jq '.tasks.agent = "deno run --allow-all scripts/launch-agent.ts"' deno.json > deno.json.tmp
mv deno.json.tmp deno.json
echo "✅ Added 'agent' task to deno.json"
fi
fi

# Create scripts directory if needed

mkdir -p scripts

# Copy launch-agent.ts from dotfiles if not present

if [ ! -f "scripts/launch-agent.ts" ]; then
DOTFILES_LAUNCH_SCRIPT="$(dirname $(git rev-parse --show-toplevel))/dotfiles/scripts/launch-agent.ts"
     if [ -f "$DOTFILES_LAUNCH_SCRIPT" ]; then
cp "$DOTFILES_LAUNCH_SCRIPT" scripts/launch-agent.ts
echo "✅ Copied launch-agent.ts to project"
else
echo "⚠️ Warning: launch-agent.ts not found in dotfiles"
echo " You'll need to copy it manually from the dotfiles repo"
fi
fi

# Create coordination directory

COORD_DIR=".claude-agents"
mkdir -p $COORD_DIR

# Add to .gitignore if not already there

if ! grep -q "^\.claude-agents/" .gitignore 2>/dev/null; then
echo ".claude-agents/" >> .gitignore
echo "✅ Added .claude-agents/ to .gitignore"
fi

echo "✅ Set up Deno-based agent launch system"

````
5. **Generate Simple Launch Instructions**:

```bash
echo ""
echo "=== Work-Stealing Agent Launch ==="
echo ""
echo "To launch agents, simply run:"
echo "  deno task agent"
echo ""
echo "Launch multiple agents in parallel:"
echo "  # Terminal 1"
echo "  deno task agent"
echo ""
echo "  # Terminal 2" 
echo "  deno task agent"
echo ""
echo "  # Terminal 3"
echo "  deno task agent"
echo ""
echo "Each agent will:"
echo "- Automatically claim an available task from /tasks/$PROJECT/status.json"
echo "- Update the main status.json atomically to prevent conflicts"
echo "- Work independently in its own worktree"
echo "- Complete tasks and claim new ones"
echo "- Always read fresh status to stay consistent with other agents"
echo "- Exit gracefully when no work remains"
```

6. **Work-Stealing Agent Behavior**:

The Deno launch script creates agents that:
- Generate unique IDs (timestamp + random)
- Read fresh status.json before each operation
- Atomically claim tasks using file locking on status.json
- Update both local registry and main status.json
- Skip tasks that are blocked by dependencies
- Show detailed reasons when no tasks available
- Clean up gracefully on exit

## Built-in Task Management Tools

The system includes atomic task claiming to ensure safe multi-agent coordination:

### How Task Claiming Works

Every agent gets:
1. Their first task pre-claimed automatically when launched
2. A simple command `deno task claim-task` to claim subsequent tasks
3. Atomic file locking to prevent conflicts
4. Clear feedback on task availability

### The claim-task Command

When agents run `deno task claim-task`, it:
- Reads the current task status atomically
- Finds the next available, unblocked task
- Claims it for the agent
- Shows what to work on next
- Or indicates if no tasks remain

This ensures:
- No race conditions between agents
- No double-claiming of tasks
- Clear audit trail in status.json
- Consistent behavior across all agents

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
deno task agent

# Terminal 2:
deno task agent

# Terminal 3:
deno task agent

# Each agent automatically:
# - Reads /tasks/[project]/status.json
# - Claims an available, unblocked task
# - Updates status.json with claim
# - Completes the task
# - Repeats until no tasks remain
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
deno task agent  # Agent 1
deno task agent  # Agent 2
deno task agent  # Agent 3
# Agents automatically claim and complete all tasks
```

## Work-Stealing Benefits

1. **Dynamic Scaling**: Launch more agents if needed mid-project
2. **Fault Tolerance**: Failed agents don't block progress
3. **No Coordination**: Agents self-organize via task claims
4. **Optimal Distribution**: Work naturally flows to available agents
5. **Simple Operation**: One script handles everything

This creates a truly autonomous multi-agent system where agents collaborate through the task queue!
````
