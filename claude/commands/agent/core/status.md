Show comprehensive status for agents in multi-agent workflows:

## Usage

```bash
/agent-status [options]
```

## Examples

```bash
# Show current agent's status
/agent-status

# Show specific agent's status
/agent-status --agent=agent-a

# Show all agents in project
/agent-status --all

# Show dependencies and blockers
/agent-status --show-dependencies

# Compact view for monitoring
/agent-status --compact
```

## Display Information

### Current Agent View

```
Agent Status: agent-a (claude-foundation)
═══════════════════════════════════════════

Worktree: ../project-foundation
Branch: feature/setup-foundation
Started: 2025-01-07 10:00 AM
Elapsed: 2 hours 15 minutes

## Assigned Tasks (2 total)

✅ setup-foundation/project-structure 
   Status: completed
   Duration: 45 minutes

⚡ setup-foundation/dependency-setup
   Status: in-progress (75%)
   Started: 1 hour ago
   
⏸️ setup-foundation/ci-pipeline
   Status: pending
   Blocked by: dependency-setup

## Progress Summary

Tasks: 1/3 completed (33%)
Subtasks: 4/8 completed (50%)
Estimated remaining: 2 hours

## Current Blockers

None

## Blocking Others

- testing-suite/* (agent-c) - waiting for all setup-foundation tasks
```

### All Agents View

```
Multi-Agent Coordination Status
═══════════════════════════════════════════

Project: voice-assistant-migration
Agents: 3 active, 0 idle
Overall Progress: 45%

## Agent Summary

### 🟢 agent-a (claude-foundation)
Worktree: ../project-foundation
Tasks: 1/3 completed
Status: Working on dependency-setup
Time: 2h 15m

### 🟢 agent-b (claude-features)  
Worktree: ../project-features
Tasks: 2/4 completed
Status: Working on api-implementation
Time: 2h 30m

### 🟡 agent-c (claude-testing)
Worktree: ../project-testing
Tasks: 0/2 completed
Status: Blocked - waiting for agent-a, agent-b
Time: 0h 15m

## Join Points

❌ integration - Not ready
   Required: setup-foundation ✅, core-features ⏳
   
❌ final-testing - Not ready  
   Required: integration ❌

## Critical Path

1. dependency-setup (agent-a) - 30 min remaining
2. api-implementation (agent-b) - 1 hour remaining  
3. integration join point
4. unit-tests (agent-c) - 2 hours estimated
```

### Dependency View

```
/agent-status --show-dependencies

Dependency Graph
═══════════════════════════════════════════

setup-foundation/
├─ project-structure ✅
├─ dependency-setup ⚡ (75%)
└─ ci-pipeline ⏸️

    ↓ blocks

testing-suite/
├─ unit-tests ⏸️ (blocked)
└─ integration-tests ⏸️ (blocked)

core-features/
├─ api-implementation ⚡ (60%)
└─ database-schema ✅

    ↓ blocks
    
testing-suite/
└─ integration-tests ⏸️ (blocked)

Legend: ✅ complete, ⚡ in-progress, ⏸️ blocked/pending
```

### Compact Monitoring View

```
/agent-status --compact

agent-a  [██████████░░░░░] 66%  setup-foundation    ⚡ dependency-setup
agent-b  [████████░░░░░░░] 50%  core-features       ⚡ api-implementation  
agent-c  [░░░░░░░░░░░░░░░] 0%   testing-suite       ⏸️ blocked by a,b
```

## Implementation Details

1. **Agent Identity Detection**:
   ```bash
   # Check for agent initialization
   if [ -f ".claude-agent" ]; then
     AGENT_ID=$(cat .claude-agent)
   else
     echo "No agent initialized. Run: /agent-init [agent-id]"
   fi
   ```

2. **Progress Calculation**:
   - Read from task hierarchy status.json
   - Calculate completion percentages
   - Estimate remaining time based on task metadata

3. **Dependency Analysis**:
   - Parse task dependencies
   - Check completion status
   - Identify blocking chains

4. **Real-time Updates**:
   - Poll status.json for changes
   - Highlight recently updated tasks
   - Show time since last activity

## Advanced Features

### Historical View

```bash
/agent-status --history

Agent Activity Log (agent-a)
═══════════════════════════════════════════

10:00 AM - Started session
10:15 AM - Started: project-structure
10:45 AM - Completed: project-structure
11:00 AM - Started: dependency-setup
12:15 PM - Progress: dependency-setup (50%)
1:15 PM  - Progress: dependency-setup (75%)
```

### Performance Metrics

```bash
/agent-status --metrics

Agent Performance Metrics
═══════════════════════════════════════════

## Velocity
- Tasks/hour: 0.5
- Subtasks/hour: 2.0
- Lines changed/hour: 150

## Quality
- Tests written: 12
- Test coverage: 85%
- Lint issues: 0

## Comparison
- vs. agent-b: 20% faster
- vs. average: 10% faster
```

### Export Status

```bash
# Export for external monitoring
/agent-status --export=json > status.json

# Export for PR description
/agent-status --export=markdown > pr-status.md
```

## Integration Features

1. **Auto-refresh Mode**:
   ```bash
   /agent-status --watch
   # Updates every 30 seconds
   ```

2. **Slack/Discord Integration**:
   ```bash
   /agent-status --notify-on-unblock
   # Notifies when blocked tasks become available
   ```

3. **CI/CD Integration**:
   - Status endpoints for build systems
   - Progress webhooks
   - Completion triggers

## Benefits

1. **Real-time Visibility**: See what every agent is doing
2. **Dependency Tracking**: Know what's blocking progress
3. **Progress Monitoring**: Track velocity and estimates
4. **Coordination**: Identify when agents need to sync
5. **Performance**: Measure and improve agent efficiency
