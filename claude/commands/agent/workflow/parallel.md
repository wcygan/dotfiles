Set up parallel development workflow:

1. Analyze current repository state:
   - List current git worktrees with `git worktree list`
   - Check current branch and uncommitted changes
   - Identify independent features that could be developed in parallel

2. Suggest parallel development opportunities:
   - Identify independent tasks that won't conflict
   - Group related changes that should stay together
   - Consider file dependencies and potential merge conflicts

3. Create worktree setup commands:
   ```bash
   # Example worktrees for independent features
   git worktree add ../$PROJECT-feature-auth feature-auth
   git worktree add ../$PROJECT-feature-api feature-api
   git worktree add ../$PROJECT-feature-db feature-db
   ```

4. Provide Claude launch instructions:
   ```bash
   # Terminal 1: Authentication feature
   cd ../$PROJECT-feature-auth && claude

   # Terminal 2: API endpoints
   cd ../$PROJECT-feature-api && claude

   # Terminal 3: Database migrations
   cd ../$PROJECT-feature-db && claude
   ```

5. Set up coordination:
   - Get project name: `PROJECT=$(basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $PWD)`
   - Create project-specific coordination directory: `mkdir -p /tmp/$PROJECT`
   - Create coordination file at `/tmp/$PROJECT/claude-tasks.md` with:
     - Task assignments for each worktree
     - Dependencies between tasks
     - Progress tracking template
     - Communication guidelines
   - Display the coordination path clearly: "Coordination file: /tmp/$PROJECT/claude-tasks.md"

6. Best practices for parallel work:
   - Keep worktrees focused on single features
   - Use consistent naming conventions
   - Regularly sync with main branch
   - Clean up completed worktrees: `git worktree remove ../$PROJECT-feature-name`
   - Consider separate worktrees for:
     - Backend API development
     - Frontend changes
     - Database schema updates
     - Infrastructure/deployment changes
     - Documentation updates

Focus on maximizing parallel efficiency while avoiding conflicts.
