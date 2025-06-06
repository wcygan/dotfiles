Analyze the codebase and create a comprehensive PLAN.md for $ARGUMENTS:

1. **Codebase Analysis**:
   - Search for existing documentation (README.md, CONTRIBUTING.md, docs/)
   - Identify project structure and key components
   - Analyze package files (package.json, go.mod, Cargo.toml, etc.)
   - Review recent commits and open issues/PRs
   - Examine test coverage and CI/CD configuration
   - Identify architectural patterns and conventions

2. **Create PLAN.md Structure**:
   - Generate a structured markdown file at project root
   - Include project overview and current state assessment
   - Break down work into discrete, actionable tasks
   - Identify parallelizable tasks and dependencies
   - Define clear join points for multi-agent coordination
   - Estimate complexity and effort for each task

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

4. **PLAN.md Template**:
   ```markdown
   # Project Plan: [Project Name]
   
   ## Overview
   Brief description of project goals and current state
   
   ## Task Breakdown
   
   ### Phase 1: Parallel Tasks
   Tasks that can be executed simultaneously by multiple agents
   
   #### Task 1.1: [Task Name]
   - **Description**: What needs to be done
   - **Files**: Specific files/directories to modify
   - **Dependencies**: None (can run in parallel)
   - **Estimated Time**: X hours
   - **Agent Assignment**: Agent A
   
   #### Task 1.2: [Task Name]
   - **Description**: What needs to be done
   - **Files**: Specific files/directories to modify
   - **Dependencies**: None (can run in parallel)
   - **Estimated Time**: X hours
   - **Agent Assignment**: Agent B
   
   ### Phase 2: Join Point
   - Merge parallel work from Phase 1
   - Run integration tests
   - Resolve any conflicts
   
   ### Phase 3: Sequential Tasks
   Tasks that must be completed in order
   
   #### Task 3.1: [Task Name]
   - **Description**: What needs to be done
   - **Dependencies**: Phase 2 completion
   - **Estimated Time**: X hours
   
   ## Execution Strategy
   
   ### Multi-Agent Setup
   ```bash
   # Terminal 1 - Agent A
   git worktree add /tmp/agent-a-work feature/agent-a
   cd /tmp/agent-a-work
   # Work on Task 1.1
   
   # Terminal 2 - Agent B  
   git worktree add /tmp/agent-b-work feature/agent-b
   cd /tmp/agent-b-work
   # Work on Task 1.2
   ```
   
   ### Coordination Points
   1. Daily sync at specific times
   2. Shared status file: `/tmp/project-status.md`
   3. Communication through PR comments
   
   ## Success Criteria
   - [ ] All tests passing
   - [ ] Documentation updated
   - [ ] Code review completed
   - [ ] Performance benchmarks met
   ```

5. **Advanced Planning Features**:
   - **Dependency Graph**: Visualize task dependencies
   - **Risk Assessment**: Identify potential blockers
   - **Resource Allocation**: Optimal agent/task assignment
   - **Progress Tracking**: Integration with todo lists
   - **Rollback Strategy**: Plan for failure scenarios

6. **Integration with Todo System**:
   ```typescript
   // Auto-generate todos from PLAN.md
   const tasks = parsePlanFile('./PLAN.md');
   tasks.forEach(task => {
     createTodo({
       content: task.description,
       status: 'pending',
       priority: task.priority,
       assignee: task.agent
     });
   });
   ```

7. **Monitoring and Updates**:
   - Regular plan reviews and updates
   - Progress visualization
   - Blocker identification and resolution
   - Dynamic re-planning based on progress

What specific aspects of the project should the plan focus on analyzing?