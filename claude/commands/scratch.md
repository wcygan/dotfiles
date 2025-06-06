Set up inter-Claude communication:

1. Create structured scratchpad directories:
   ```bash
   # Get project name from repository
   PROJECT_NAME=$(basename $(git rev-parse --show-toplevel))
   mkdir -p /tmp/$PROJECT_NAME/claude-scratch/{tasks,reviews,notes,status}
   ```

2. Initialize communication files:
   - `/tmp/$PROJECT_NAME/claude-scratch/tasks.md` - Task assignments
   - `/tmp/$PROJECT_NAME/claude-scratch/reviews.md` - Code review feedback
   - `/tmp/$PROJECT_NAME/claude-scratch/notes.md` - General communication
   - `/tmp/$PROJECT_NAME/claude-scratch/status.json` - Progress tracking

3. Set up file templates:
   ```bash
   # Initialize templates
   echo "# Claude Instance Tasks" > /tmp/$PROJECT_NAME/claude-scratch/tasks.md
   echo '{}' | jq '.instances = {} | .sharedData = {}' > /tmp/$PROJECT_NAME/claude-scratch/status.json
   ```

   **tasks.md template:**
   ```markdown
   # Claude Instance Tasks

   ## Instance: main

   - [ ] Task 1: Description
   - [ ] Task 2: Description

   ## Instance: feature-a

   - [ ] Task 1: Description
   ```

   **status.json template:**
   ```json
   {
     "instances": {
       "main": {
         "status": "active",
         "currentTask": "Task 1",
         "lastUpdate": "timestamp"
       }
     },
     "sharedData": {}
   }
   ```

4. Create monitoring script:
   ```typescript
   // scripts/monitor-claude-scratch.ts
   import { watch } from "@std/fs";

   // Get project name from current directory or command line
   const projectName = Deno.args[0] || Deno.cwd().split("/").pop();
   const scratchPath = `/tmp/${projectName}/claude-scratch`;

   const watcher = watch(scratchPath);

   console.log(`Monitoring Claude scratchpad for ${projectName}...`);

   for await (const event of watcher) {
     if (event.kind === "modify") {
       console.log(`[${new Date().toISOString()}] ${event.paths[0]} updated`);

       // Read and display relevant changes
       if (event.paths[0].includes("status.json")) {
         const status = JSON.parse(await Deno.readTextFile(event.paths[0]));
         console.log("Current status:", status);
       }
     }
   }
   ```

5. Communication protocols:
   - Use markdown headers for instance identification
   - Timestamp all entries
   - Use consistent formatting for parsability
   - Lock files during writes to prevent conflicts

6. Usage instructions:
   ```bash
   # Get project name
   PROJECT_NAME=$(basename $(git rev-parse --show-toplevel))

   # Instance 1: Write task
   echo "## Instance: main\n- [ ] Implement new feature" >> /tmp/$PROJECT_NAME/claude-scratch/tasks.md

   # Instance 2: Read tasks
   cat /tmp/$PROJECT_NAME/claude-scratch/tasks.md | grep "Instance: feature"

   # Update status
   deno eval "
     const projectName = '$PROJECT_NAME';
     const statusPath = '/tmp/' + projectName + '/claude-scratch/status.json';
     const status = JSON.parse(await Deno.readTextFile(statusPath));
     status.instances.main.currentTask = 'Task 2';
     await Deno.writeTextFile(statusPath, JSON.stringify(status, null, 2));
   "
   ```

7. Best practices:
   - Clear scratchpad after session completion
   - Use instance names that match worktree names
   - Include task dependencies in communications
   - Regular status updates for long-running tasks
