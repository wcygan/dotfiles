Coordinate multiple Claude instances:

1. Analyze project and create coordination plan:
   - Identify major work streams
   - Determine dependencies between tasks
   - Estimate complexity and time for each task
   - Suggest optimal parallelization strategy

2. Create coordination file:
   - Get project name: `PROJECT=$(basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $PWD)`
   - Create project-specific directory: `mkdir -p /tmp/$PROJECT/claude-scratch`
   - Create `/tmp/$PROJECT/claude-coordination.md` with structure:
   ```markdown
   # Claude Multi-Instance Coordination Plan

   Generated: [timestamp]

   ## Work Streams

   ### Stream A: [Description]

   - Instance: claude-feature-a
   - Worktree: ../dotfiles-feature-a
   - Tasks:
     1. [ ] Task with specific scope
     2. [ ] Follow-up task
   - Dependencies: None
   - Priority: High

   ### Stream B: [Description]

   - Instance: claude-feature-b
   - Worktree: ../dotfiles-feature-b
   - Tasks:
     1. [ ] Task with specific scope
   - Dependencies: Stream A task 1
   - Priority: Medium

   ## Communication Channels

   - Tasks: /tmp/$PROJECT/claude-scratch/tasks.md
   - Reviews: /tmp/$PROJECT/claude-scratch/reviews.md
   - Status: /tmp/$PROJECT/claude-scratch/status.json

   ## Synchronization Points

   - [ ] After Stream A task 1: Sync with Stream B
   - [ ] Before final integration: All streams sync
   ```

3. Set up worktrees and provide commands:
   ```bash
   # Create worktrees
   git worktree add ../dotfiles-feature-a feature-a
   git worktree add ../dotfiles-feature-b feature-b

   # Launch Claude instances
   # Terminal 1:
   cd ../$PROJECT-feature-a && claude
   # > Read coordination plan at /tmp/$PROJECT/claude-coordination.md
   # > Focus on Stream A tasks

   # Terminal 2:
   cd ../$PROJECT-feature-b && claude
   # > Read coordination plan at /tmp/$PROJECT/claude-coordination.md
   # > Focus on Stream B tasks
   ```

4. Create progress checking script:
   ```typescript
   // scripts/check-coordination-progress.ts
   import { parse } from "@std/yaml";

   // Get project name from current directory
   const projectName = Deno.cwd().split("/").pop();

   // Read coordination plan
   const plan = await Deno.readTextFile(`/tmp/${projectName}/claude-coordination.md`);

   // Read current status
   const status = JSON.parse(
     await Deno.readTextFile(`/tmp/${projectName}/claude-scratch/status.json`),
   );

   // Display progress
   console.log("=== Coordination Progress ===");
   for (const [instance, data] of Object.entries(status.instances)) {
     console.log(`\n${instance}:`);
     console.log(`  Status: ${data.status}`);
     console.log(`  Current: ${data.currentTask}`);
     console.log(`  Updated: ${data.lastUpdate}`);
   }

   // Check dependencies
   console.log("\n=== Dependency Status ===");
   // Parse and check dependency completion
   ```

5. Instance naming conventions:
   - Use descriptive names: claude-auth, claude-ui, claude-tests
   - Match worktree names for clarity
   - Include in all communications

6. Task assignment best practices:
   - Keep related changes in same instance
   - Minimize file overlap between instances
   - Clear scope boundaries
   - Regular synchronization points

7. Monitoring and management:
   ```bash
   # Check overall progress
   deno run --allow-read scripts/check-coordination-progress.ts

   # View specific instance status
   PROJECT=$(basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $PWD)
   cat /tmp/$PROJECT/claude-scratch/status.json | jq '.instances["claude-feature-a"]'

   # Clean up completed work
   git worktree remove ../$PROJECT-feature-a
   rm -rf /tmp/$PROJECT  # After session complete
   ```

Use this for complex features requiring multiple parallel work streams.
