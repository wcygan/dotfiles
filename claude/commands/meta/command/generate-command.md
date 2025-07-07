---
allowed-tools: Read, Write, Bash(mkdir:*), Bash(fd:*), Bash(ls:*), Bash(git:*), Bash(gdate:*)
description: Interactive generator for project-level slash commands with best practices validation
---

## Context

- Session ID: !`gdate +%s%N`
- Current directory: !`pwd`
- Existing .claude directory: !`ls -la .claude 2>/dev/null || echo "No .claude directory found"`
- Current command structure: !`fd "\.md$" .claude/commands 2>/dev/null | head -5 || echo "No existing commands"`
- Git status: !`git status --porcelain 2>/dev/null | head -3 || echo "Not a git repository"`
- Project type indicators: !`fd "(package\.json|deno\.json|Cargo\.toml|go\.mod|pom\.xml)" . -d 2 | head -3`

## Your Task

STEP 1: Initialize command generation session and analyze project context

- CREATE session state file: `/tmp/generate-command-state-$SESSION_ID.json`
- ANALYZE existing .claude/commands structure from Context
- IDENTIFY project patterns and common workflows
- DETERMINE recommended command categories based on project type

STEP 2: Interactive command specification gathering

TRY:

- PROMPT user for command requirements using intelligent project-based suggestions:

**Command Specification Questions:**

1. **Command Purpose**: What specific task should this command automate?

   Examples based on detected project type:
   - Deno projects: "test-single", "build-deploy", "format-check"
   - Rust projects: "cargo-audit", "benchmark-performance", "docker-build"
   - Go projects: "generate-mocks", "run-integration-tests", "profile-memory"
   - Multi-language: "sync-dependencies", "security-scan", "generate-docs"

2. **Command Name**: What should the slash command be called?
   - Must be kebab-case (e.g., "audit-security", "fix-issue")
   - Will be accessible as `/project:command-name`

3. **Parameters Needed**: Does the command need user input?
   - None: Simple execution commands
   - Single: Use `$ARGUMENTS` token
   - Multiple: Design structured input pattern

4. **Command Complexity Level**:
   - **Simple**: Single-step operation, no state management
   - **Interactive**: Requires user confirmation or multi-phase execution
   - **Complex**: Needs state management, error handling, resumability
   - **Analysis**: Benefits from extended thinking or sub-agents

5. **Tools Required**: What operations will the command perform?
   - File operations: Read, Write, Edit, MultiEdit
   - Shell commands: Bash with specific tool restrictions
   - External APIs: WebFetch, WebSearch
   - Sub-processes: Task (for sub-agent delegation)

CATCH (user_input_incomplete):

- SAVE partial input to session state
- PROVIDE examples and suggestions
- CONTINUE gathering missing information

STEP 3: Generate command file with best practices validation

**Command Generation Process:**

IF command_complexity == "simple":

- GENERATE basic command structure:
  ```yaml
  ---
  allowed-tools: [detected_tools]
  description: [user_provided_purpose]
  ---

  ## Context

  - Session ID: !`gdate +%s%N`
  [context_commands_based_on_purpose]

  ## Your task

  [user_specified_task_converted_to_steps]
  ```

IF command_complexity == "interactive":

- GENERATE command with checkpoint pattern:
  - Session state management
  - User confirmation points
  - Resume capability

IF command_complexity == "complex":

- GENERATE command with full state management:
  - `/tmp/command-state-$SESSION_ID.json` pattern
  - TRY/CATCH blocks for error handling
  - STEP-based execution with validation

IF command_complexity == "analysis":

- INCLUDE extended thinking recommendations:
  - "think hard" prompts for complex decisions
  - Sub-agent delegation patterns for parallel research
  - Token-efficient context management

**Best Practices Validation:**

FOR EACH generated command:

- VALIDATE front matter completeness
- ENSURE session ID in Context section
- VERIFY all bash commands are safe and tested
- CHECK programmatic structure (STEP/IF/FOR patterns)
- CONFIRM error handling for risky operations
- TEST command follows gold standard (/commit pattern)

STEP 4: Create command directory structure and file

```bash
# Ensure .claude/commands directory exists
IF [ ! -d ".claude/commands" ]; then
  mkdir -p .claude/commands
  echo "Created .claude/commands directory"
fi

# Determine command file path
command_file=".claude/commands/${command_name}.md"

# Check for existing command
IF [ -f "$command_file" ]; then
  echo "⚠️ Command $command_name already exists"
  PROMPT user for overwrite confirmation
fi
```

STEP 5: Write and validate generated command

- WRITE command file to determined path
- VALIDATE generated command syntax
- TEST all bash commands in Context section for compatibility
- VERIFY command follows established patterns

STEP 6: Commit new command to version control

IF git repository detected:

```bash
# Stage the new command
git add .claude/commands/${command_name}.md

# Create descriptive commit message
git commit -m "feat: add /project:${command_name} command

Adds interactive command for ${command_purpose}.
Includes proper front matter, dynamic context, and error handling."

echo "✅ Command committed to version control"
```

STEP 7: Provide usage instructions and next steps

- DISPLAY command usage: `/project:${command_name}`
- SHOW command file location for editing
- SUGGEST testing the command before team distribution
- RECOMMEND documenting the command in project README if applicable

FINALLY:

- CLEAN UP session state file
- REPORT successful command generation
- PROVIDE command testing instructions

**Example Command Patterns by Type:**

1. **Git/GitHub Operations**: Follow `/commit` gold standard pattern
2. **Code Analysis**: Include sub-agent delegation for large codebases
3. **Build/Deploy**: Add state management for multi-step processes
4. **Testing**: Include parallel execution for performance
5. **Documentation**: Use extended thinking for comprehensive coverage

**Advanced Features to Consider:**

- **Sub-Agent Integration**: For complex analysis or parallel research tasks
- **Extended Thinking**: For architectural decisions or deep analysis
- **State Management**: For resumable workflows and error recovery
- **Dynamic Context**: For real-time project state awareness
- **Security Validation**: Ensure minimal tool permissions and safe operations
