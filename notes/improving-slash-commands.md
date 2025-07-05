# Improving Slash Commands

We will improve all slash commmands under /claude/commands to follow the new best practices:

```bash
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
4. Token efficient - Reference files, use precise tools (jq, rg)
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
```
