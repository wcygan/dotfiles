# Improving Slash Commands

We will improve all slash commmands under /claude/commands to follow the new best practices:

````bash
TL;DR: Best Practices for Prompts/Slash Commands in CLAUDE.md

🎯 Core Philosophy

- Think "Program" not "Conversation" - Treat prompts as executable specifications with deterministic behavior
- LLMs as Slow Computers - Program them with natural language using familiar constructs (loops, conditionals, state)

🔒 Security & Permissions

- Minimal allowed-tools - Only allow necessary commands
- Read-only for context - Example: Use status/log/diff commands for gathering info in the /commit command
- Scoped permissions - Explicitly define command scopes (e.g., Bash(git status:*))

📝 Command Structure

1. Front Matter - Clear allowed-tools and description
2. Dynamic Context - Use ! for bash execution (dynamic context injection), @ for file inclusion
3. Clear Task Definition - Specific, actionable instructions with examples
4. Organized Namespacing - Follow directory structure (claude/commands/git/pr/pr-create.md)

💾 State Management

- Unique temp files - Use nanosecond timestamps: /tmp/state-$(gdate +%s%N).json
- Session isolation - Each session gets unique IDs to prevent conflicts
- Checkpoint/resume - Save progress for long operations
- Serialize to disk - Minimize context window usage

🚀 Programming Patterns

- Sequential Steps - STEP 1:, STEP 2:, etc.
- Conditionals - IF/ELSE logic for different scenarios
- Loops - FOR EACH for iterating over items
- Error Handling - TRY/CATCH/FINALLY blocks
- State Machines - Track workflow phases with transitions

🤖 Sub-Agent Usage

- When to use: Large-scale analysis, parallel research, multi-aspect tasks
- When NOT to use: Sequential operations, simple tasks, state modifications
- Let Claude manage - Don't specify parallelism levels
- Clear boundaries - Each agent has independent scope
- Up to 10 parallel - System queues additional tasks

🎨 Design Principles

1. Minimize Non-Determinism - Goal: Same inputs → same outputs
2. Modular - Break into reusable components
3. Human checkpoints - AWAIT approval for critical operations
4. Token efficient - Reference files, use precise tools (jq (json query / processor — essential for working with JSON files), rg (recursively search directories for regex pattern), fd (find files according to patterns))
5. Error resilient - Handle partial failures gracefully

🛠️ Integration Features

- Arguments - $ARGUMENTS for user input
- Extended thinking - Combine with "think harder" for complex analysis
- File references - @path/to/file for content inclusion
- Dynamic context - !command`` for real-time data

📊 Performance Tips

- Batch operations - Multiple tool calls in single response
- Structured output - Use JSON/Markdown for aggregation
- Clean up - Remove temp files after completion
- Context preservation - Main agent synthesizes sub-agent findings

The /commit command (file: claude/commands/git/commit/commit.md) serves as the gold standard example, demonstrating all these best practices in action.

## Critical Testing Requirements

### Session ID Requirement
**EVERY command MUST include a SESSION_ID in the context section:**
```yaml
## Context
- Session ID: !`gdate +%s%N`
````

This ensures:

- Unique temporary files for each invocation
- No conflicts between concurrent sessions
- Clean state isolation

### Bash Command Testing

**EVERY bash command in the Context section MUST be tested for compatibility:**

1. Test each command individually before including
2. Handle shell quoting issues properly:
   - Avoid `!=` in jq expressions when passed through shell
   - Use proper escaping for quotes within quotes
   - Test with actual kubectl/docker/git environments

3. Common pitfalls to avoid:
   - Shell interpretation of `!` character
   - Nested quotes in jq expressions
   - Special characters in command substitution

4. Always provide fallback values:
   ```bash
   !`command || echo "fallback value"`
   ```

### Testing Checklist

Before marking a command as improved:

- [ ] All bash commands in Context section tested individually
- [ ] Session ID generation verified with `gdate +%s%N`
- [ ] Error handling for missing tools/connections
- [ ] Proper quoting and escaping verified
- [ ] Fallback values provided for all commands

## Atomic Commit Workflow

### CRITICAL: Always Commit progress.json Changes Atomically

**When improving commands, you MUST commit progress.json updates together with the command file changes:**

1. **Stage Both Files Together:**
   ```bash
   git add claude/commands/path/to/command.md notes/improve-slash-commands/progress.json
   ```

2. **Single Atomic Commit:**
   ```bash
   git commit -m "improve(commands): enhance {command-name} with best practices"
   ```

3. **Never Commit Separately:**
   - ❌ DON'T: Commit command file first, then progress.json later
   - ❌ DON'T: Update progress.json without committing the improved command
   - ✅ DO: Always stage and commit both files in a single atomic operation

### Why This Matters

- **Consistency**: The progress tracking stays in sync with actual improvements
- **Rollback Safety**: If a commit needs to be reverted, both files revert together
- **Clear History**: Each commit shows exactly what was improved and tracks it
- **Prevents Drift**: Avoids progress.json showing work that wasn't actually committed

### Example Workflow

```bash
# After improving a command
git add claude/commands/kubernetes/k8s-debug.md
git add notes/improve-slash-commands/progress.json

# Commit both atomically
git commit -m "improve(commands): enhance k8s-debug with best practices"
```

```
```
