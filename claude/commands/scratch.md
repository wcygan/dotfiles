Set up inter-Claude communication:

1. Create structured scratchpad directories:
   ```bash
   mkdir -p /tmp/claude-scratch/{tasks,reviews,notes,status}
   ```

2. Initialize communication files:
   - `/tmp/claude-scratch/tasks.md` - Task assignments
   - `/tmp/claude-scratch/reviews.md` - Code review feedback
   - `/tmp/claude-scratch/notes.md` - General communication
   - `/tmp/claude-scratch/status.json` - Progress tracking

3. Set up file templates:
   
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
   
   const watcher = watch("/tmp/claude-scratch");
   
   console.log("Monitoring Claude scratchpad...");
   
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
   # Instance 1: Write task
   echo "## Instance: main\n- [ ] Implement new feature" >> /tmp/claude-scratch/tasks.md
   
   # Instance 2: Read tasks
   cat /tmp/claude-scratch/tasks.md | grep "Instance: feature"
   
   # Update status
   deno eval "
     const status = JSON.parse(await Deno.readTextFile('/tmp/claude-scratch/status.json'));
     status.instances.main.currentTask = 'Task 2';
     await Deno.writeTextFile('/tmp/claude-scratch/status.json', JSON.stringify(status, null, 2));
   "
   ```

7. Best practices:
   - Clear scratchpad after session completion
   - Use instance names that match worktree names
   - Include task dependencies in communications
   - Regular status updates for long-running tasks