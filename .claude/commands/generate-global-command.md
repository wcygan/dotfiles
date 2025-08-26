---
allowed-tools: Read, Write, Bash(mkdir:*), Bash(fd:*), Bash(eza:*), Bash(git:*), Bash(gdate:*)
description: Interactive generator for global Claude slash commands with namespace organization and best practices validation
---

## Context

- Session ID: !`gdate +%s%N`
- Current directory: !`pwd`
- Claude commands directory: !`eza -la . claude/commands 2>/dev/null | head -10 || echo "Not in dotfiles directory"`
- Existing namespaces: !`fd -t d -d 1 . claude/commands 2>/dev/null | sort || echo "claude/commands not found"`
- Total commands: !`fd "\.md$" claude/commands 2>/dev/null | wc -l || echo "0"`
- Git status: !`git status --porcelain 2>/dev/null | head -3 || echo "Not a git repository"`

## Your Task

STEP 1: Validate environment and analyze command structure

IF current directory is not dotfiles repository:
PRINT "Error: This command must be run from the dotfiles repository root"
EXIT

- CREATE session state file: `/tmp/generate-global-command-state-$SESSION_ID.json`
- ANALYZE namespace structure in claude/commands/
- IDENTIFY existing command patterns and conventions
- EXTRACT best practices from README.md

STEP 2: Interactive command specification gathering

**Command Specification Questions:**

1. **Command Purpose**: What specific task should this command automate?

   Examples by category:
   - **Agent**: Coordination patterns, personas, parallel execution
   - **Context**: Technology-specific knowledge loading
   - **Scaffold**: Project templates and boilerplate
   - **Git**: Version control workflows
   - **Test**: Testing strategies and generation
   - **Code**: Analysis, refactoring, migration
   - **Docs**: Documentation generation and management
   - **Security**: Auditing and vulnerability scanning
   - **Ops**: DevOps, monitoring, deployment

2. **Namespace Selection**: Which namespace should contain this command?

   Based on detected namespaces:
   - agent/ - Multi-agent coordination
   - analyze/ - Deep analysis and research
   - code/ - Code operations and transformations
   - context/ - Context loading for technologies
   - docs/ - Documentation tasks
   - git/ - Git and GitHub workflows
   - meta/ - Meta commands and utilities
   - ops/ - Operations and DevOps
   - scaffold/ - Project scaffolding
   - security/ - Security operations
   - task/ - Task management
   - test/ - Testing operations
   - tool/ - Tool-specific integrations
   - workflow/ - Workflow management

3. **Command Name**: What should the slash command be called?
   - Must be kebab-case (e.g., "analyze-performance", "generate-tests")
   - Will be accessible as `/command-name` globally
   - Should be descriptive and follow namespace conventions

4. **Command Complexity Level**:
   - **Simple**: Single-step operation, basic context
   - **Interactive**: Multi-phase with user checkpoints
   - **Complex**: State management, error handling, resumability
   - **Analysis**: Extended thinking or sub-agent delegation
   - **Workflow**: Multi-stage pipeline with coordination

5. **Dynamic Context Requirements**: What real-time information is needed?
   - File system state (fd, eza, rg commands)
   - Git repository state (status, diff, log)
   - Project configuration (reading config files)
   - System state (environment variables, timestamps)

6. **Tools Required**: What operations will the command perform?
   - File operations: Read, Write, Edit, MultiEdit
   - Shell commands: Bash with specific restrictions
   - Research: WebFetch, WebSearch
   - Parallel execution: Task (sub-agents)
   - AI capabilities: Extended thinking patterns

STEP 3: Generate command following gold standard patterns

**Command Template Selection:**

IF command_complexity == "simple":
USE basic template with dynamic context:

```yaml
---
allowed-tools: [minimal_required_tools]
description: [concise_purpose]
---

## Context

- Session ID: !`gdate +%s%N`
[relevant_dynamic_context]

## Your task

[clear_sequential_steps]
```

IF command_complexity == "interactive":
USE checkpoint pattern from /commit:

- Human-in-the-loop confirmations
- CHECKPOINT markers
- State preservation between phases

IF command_complexity == "complex":
USE programmatic pattern:

- STEP/IF/FOR/WHILE constructs
- TRY/CATCH error handling
- State management with unique files
- Resume capability

IF command_complexity == "analysis":
USE sub-agent pattern:

- Parallel agent delegation
- Research task distribution
- Synthesis in main agent
- Extended thinking prompts

IF command_complexity == "workflow":
USE pipeline pattern:

- Phase definitions
- State transitions
- Coordination points
- Progress tracking

**Best Practices Validation:**

FOR EACH generated command:

- ✓ Front matter with minimal allowed-tools
- ✓ Concise, actionable description
- ✓ Dynamic context with !` commands
- ✓ Unique session IDs for parallel safety
- ✓ Programmatic structure (not conversational)
- ✓ Error handling for risky operations
- ✓ Clear task definition with examples
- ✓ Follows namespace conventions

STEP 4: Determine file path and create directory structure

```bash
# Validate we're in dotfiles directory
IF [ ! -d "claude/commands" ]; then
  echo "Error: Must run from dotfiles repository root"
  EXIT 1
fi

# Create namespace directory if needed
namespace_dir="claude/commands/${selected_namespace}"
IF [ ! -d "$namespace_dir" ]; then
  mkdir -p "$namespace_dir"
  echo "Created namespace directory: $namespace_dir"
fi

# Determine command file path
# Add namespace prefix to filename for clarity
command_file="${namespace_dir}/${command_name}.md"

# Check for existing command
IF [ -f "$command_file" ]; then
  echo "⚠️ Command already exists at: $command_file"
  PROMPT "Overwrite existing command? (y/n)"
  IF response != "y"; then
    EXIT
  fi
fi
```

STEP 5: Write command with validation

- WRITE generated command to determined path
- VALIDATE all bash commands in Context section
- ENSURE command follows established patterns:
  - Gold standard: /commit pattern for Git operations
  - Sub-agent: /analyze-code-quality for parallel analysis
  - State management: Complex workflows with checkpoints
  - Extended thinking: Deep analysis tasks

STEP 6: Update namespace documentation if needed

IF new namespace created OR significant pattern introduced:

- CHECK for namespace README.md
- UPDATE with new command documentation
- DOCUMENT any new patterns introduced

STEP 7: Commit new command to version control

```bash
# Stage the new command
git add "claude/commands/${selected_namespace}/${command_name}.md"

# Create semantic commit message
git commit -m "feat(commands): add /${command_name} to ${selected_namespace} namespace

- Purpose: ${command_purpose}
- Complexity: ${command_complexity}
- Tools: ${allowed_tools}

Implements ${pattern_type} pattern with proper error handling and state management."

echo "✅ Command committed to version control"
```

STEP 8: Provide usage instructions and next steps

**Installation and Usage:**

```bash
# Install globally (from dotfiles root)
deno task install

# Command is now available as:
/${command_name}

# Edit if needed:
$EDITOR claude/commands/${selected_namespace}/${command_name}.md

# Test the command:
echo "Test with: /${command_name} [arguments]"
```

**Next Steps:**

- TEST command with various inputs
- DOCUMENT in project README if significant
- SHARE with team after validation
- CONSIDER creating related commands in same namespace

FINALLY:

- CLEAN UP session state file
- REPORT successful generation with file path
- SUGGEST testing strategies based on complexity

**Advanced Pattern Examples:**

1. **Sub-Agent Research** (analyze namespace):
   ```yaml
   ## Your task
   Use 5 parallel agents to analyze:
     - Agent 1: Architecture patterns
     - Agent 2: Security vulnerabilities
     - Agent 3: Performance bottlenecks
     - Agent 4: Code quality metrics
     - Agent 5: Documentation coverage
   ```

2. **State Machine** (workflow namespace):
   ```yaml
   ## State Definition
   - States: [initializing, analyzing, implementing, complete]
   - Current: !`jq .state < /tmp/state-$SESSION_ID.json`
   ```

3. **Pipeline Processing** (ops namespace):
   ```yaml
   Input: $ARGUMENTS
     |> Stage 1: Validate
     |> Stage 2: Process
     |> Stage 3: Deploy
   ```

4. **Extended Thinking** (analyze namespace):
   ```yaml
   Think deeply about the architectural implications...
   Consider edge cases and failure modes...
   ```

**Namespace-Specific Patterns:**

- **agent/**: Multi-agent coordination, personas
- **analyze/**: Extended thinking, deep research
- **code/**: AST manipulation, refactoring
- **context/**: Technology documentation loading
- **docs/**: Generation with templates
- **git/**: Commit, PR, and merge workflows
- **meta/**: Command and knowledge management
- **ops/**: CI/CD, deployment, monitoring
- **scaffold/**: Project initialization
- **security/**: Vulnerability scanning, auditing
- **test/**: Test generation, coverage analysis
- **tool/**: External tool integration
- **workflow/**: Complex multi-stage processes
