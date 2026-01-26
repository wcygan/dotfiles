---
allowed-tools: AskUserQuestion, Read, Glob, Grep, Write, Edit
description: Initialize a ralph loop with spec, implementation plan, prompt, and orchestrator
---

You are initializing a **ralph loop** workflow for autonomous development. This involves creating four files that work together:

1. `SPEC.md` - Detailed specification from user interview
2. `IMPLEMENTATION_PLAN.md` - Structured task breakdown with checkboxes
3. `PROMPT.md` - Meta-prompt that drives each loop iteration
4. `ralph.sh` - Bash orchestrator script

---

# Phase 1: Deep Interview

**Your goal is to fully understand what the user wants to build before writing anything.**

Use `AskUserQuestion` to interview the user. Cover these areas thoroughly:

## Core Understanding
- What is being built? (elevator pitch)
- What problem does it solve?
- Who is the target user/consumer?
- What does "done" look like?

## Technical Scope
- What's the tech stack? (languages, frameworks, databases)
- Are there existing codebases/files to integrate with?
- What are the hard constraints? (performance, compatibility, dependencies)
- What's explicitly out of scope?

## Architecture & Design
- High-level component structure
- Data models and relationships
- External integrations (APIs, services)
- Key technical decisions already made

## User Experience (if applicable)
- User workflows and journeys
- UI/UX requirements or preferences
- Error handling and edge cases
- Accessibility considerations

## Quality & Testing
- What constitutes "working"? (acceptance criteria)
- Testing strategy preferences
- Performance requirements
- Security considerations

## Risks & Unknowns
- What are you uncertain about?
- What could go wrong?
- Dependencies on external factors
- Areas needing research/spikes

**Interview rules:**
- Ask one question at a time
- Go deep on answers - follow up on interesting threads
- Don't ask obvious questions that can be inferred
- Challenge assumptions constructively
- Continue until you have comprehensive understanding
- Confirm understanding before moving to Phase 2

---

# Phase 2: Generate SPEC.md

Once the interview is complete, synthesize everything into `SPEC.md`:

```markdown
# Project Specification: {Project Name}

## Overview
{One paragraph summary of what this is and why it exists}

## Goals
{Bulleted list of what success looks like}

## Non-Goals
{Explicitly out of scope items}

## Technical Stack
{Languages, frameworks, tools, and why}

## Architecture
{Component breakdown, data flow, key abstractions}

## Data Models
{Core entities and relationships}

## User Workflows
{Step-by-step flows for key user journeys}

## API / Interface Design
{Endpoints, commands, or interface contracts}

## Acceptance Criteria
{Specific, testable conditions for "done"}

## Open Questions
{Remaining uncertainties to resolve during implementation}

## Decisions Log
{Key architectural decisions made and rationale}
```

Write this to `SPEC.md` in the current directory.

---

# Phase 3: Generate IMPLEMENTATION_PLAN.md

Break the spec into an ordered, actionable task list:

```markdown
# Implementation Plan

**Generated from:** SPEC.md  
**Status:** In Progress  
**Last Updated:** {timestamp}

## Phase 1: Foundation
- [ ] Task 1 description
- [ ] Task 2 description
- [ ] ...

## Phase 2: Core Features
- [ ] Task description
- [ ] ...

## Phase 3: Integration
- [ ] ...

## Phase 4: Polish & Testing
- [ ] ...

## Phase 5: Documentation
- [ ] ...

---

## Task Guidelines

Each task should be:
- **Atomic**: Completable in one focused session
- **Testable**: Has clear verification criteria
- **Independent**: Minimal dependencies on incomplete tasks

## Progress Tracking

Format: `- [x]` = complete, `- [ ]` = pending, `- [>]` = in progress
```

**Task sizing guidance:**
- Each task should be 15-60 minutes of work
- If a task feels too big, break it down
- Include setup/scaffolding tasks early
- Include test tasks alongside implementation
- End with documentation and cleanup tasks

Write this to `IMPLEMENTATION_PLAN.md` in the current directory.

---

# Phase 4: Generate PROMPT.md

Create the meta-prompt that drives each loop iteration:

```markdown
# Ralph Loop Prompt

You are operating in an autonomous development loop. Your job is to make incremental progress on the implementation plan.

## Context Files
- `SPEC.md` - The full project specification (read for context)
- `IMPLEMENTATION_PLAN.md` - Task list with completion status (read and update)

## Your Mission (Single Iteration)

### Step 1: Orient
1. Read `SPEC.md` to understand the project
2. Read `IMPLEMENTATION_PLAN.md` to find current progress
3. Identify the next incomplete task (first `- [ ]` item)

### Step 2: Execute
1. Implement the task completely
2. Write or update tests to verify the implementation
3. Run tests to confirm they pass
4. Commit changes with a descriptive message

### Step 3: Update State
1. Mark the completed task as `- [x]` in `IMPLEMENTATION_PLAN.md`
2. Update the "Last Updated" timestamp
3. If you discovered new tasks, add them in the appropriate phase

### Step 4: Exit
**Important:** After completing ONE task, exit immediately.

The loop will restart you with fresh context. Do not attempt multiple tasks.

---

## Rules

1. **One task per iteration** - Complete one checkbox, then exit
2. **Always test** - No task is done without verification
3. **Always commit** - Each task = one atomic commit
4. **Update the plan** - Mark completion before exiting
5. **Don't gold-plate** - Do what the task says, no more
6. **Ask if stuck** - If a task is unclear, add a question to SPEC.md and exit

## Exit Conditions

Exit with success message after:
- Completing and committing one task
- Updating IMPLEMENTATION_PLAN.md

Exit with blocker message if:
- All tasks are complete (plan is done!)
- You encounter an unresolvable issue
- A task requires clarification from the user

## Completion Detection

When all tasks show `- [x]`, output:
```
🎉 RALPH_COMPLETE: All tasks finished. Review the implementation.
```
```

Write this to `PROMPT.md` in the current directory.

---

# Phase 5: Generate ralph.sh

Create the orchestrator script with sane, documented defaults:

```bash
#!/usr/bin/env bash
#
# Ralph Loop Orchestrator
# Autonomous development loop driver for Claude-based workflows
#
# Usage: ./ralph.sh [OPTIONS]
#
# Options:
#   --max-iterations N    Maximum loop iterations (default: 50)
#   --delay N             Seconds between iterations (default: 2)
#   --pause               Pause for confirmation between iterations
#   --log FILE            Log output to file (default: ralph.log)
#   --no-log              Disable logging

#   -h, --help            Show this help message
#
# Exit Codes:
#   0 - All tasks completed successfully (RALPH_COMPLETE)
#   1 - Blocker encountered or max iterations reached
#   130 - Interrupted by user (Ctrl+C)

# ============================================================================
# SHELL OPTIONS (Safety First)
# ============================================================================
set -e          # Exit immediately on command failure
set -u          # Treat unset variables as errors
set -o pipefail # Pipeline fails if any command fails
# Note: We intentionally don't use 'set -x' by default (too verbose)

# ============================================================================
# DEFAULT CONFIGURATION
# These values are chosen for safety and typical use cases.
# Override via command-line flags.
# ============================================================================

# MAX_ITERATIONS: Prevents runaway loops. 50 is enough for most projects
# while providing a safety net. A typical task takes 1-5 minutes, so 50
# iterations = 50-250 minutes of autonomous work maximum.
MAX_ITERATIONS=50

# DELAY_SECONDS: Cooldown between iterations. Prevents API rate limiting
# and gives the filesystem time to sync.
DELAY_SECONDS=2

# PAUSE_BETWEEN: When true, requires human confirmation between iterations.
# Defaults to false for autonomous operation, but recommended for first runs.
PAUSE_BETWEEN=false

# LOG_FILE: Where to write iteration output for later review.
# Set to empty string to disable logging.
LOG_FILE="ralph.log"

# PROMPT_FILE: The instruction file for Claude. Must exist.
PROMPT_FILE="PROMPT.md"

# PLAN_FILE: Implementation plan to check for completion status.
PLAN_FILE="IMPLEMENTATION_PLAN.md"

# ============================================================================
# INTERNAL STATE
# ============================================================================
ITERATION=0
SCRIPT_NAME="$(basename "$0")"
START_TIME="$(date +%s)"

# ============================================================================
# FUNCTIONS
# ============================================================================

usage() {
    sed -n '2,/^$/p' "$0" | grep '^#' | sed 's/^# \?//'
    exit 0
}

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
    echo "$msg"
    if [[ -n "$LOG_FILE" ]]; then
        echo "$msg" >> "$LOG_FILE"
    fi
}

die() {
    log "ERROR: $*"
    exit 1
}

cleanup() {
    local exit_code=$?
    local elapsed=$(($(date +%s) - START_TIME))
    log ""
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log "Ralph loop terminated after $ITERATION iterations (${elapsed}s elapsed)"
    if [[ $exit_code -eq 130 ]]; then
        log "Interrupted by user (Ctrl+C)"
    fi
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit $exit_code
}

preflight_check() {
    # Verify required files exist
    if [[ ! -f "$PROMPT_FILE" ]]; then
        die "Missing $PROMPT_FILE - run ralph initialization first"
    fi
    if [[ ! -f "$PLAN_FILE" ]]; then
        die "Missing $PLAN_FILE - run ralph initialization first"
    fi
    
    # Verify claude CLI is available
    if ! command -v claude &>/dev/null; then
        die "Claude CLI not found. Install from: https://github.com/anthropics/claude-code"
    fi
    
    # Warn about dangerous permissions mode
    log "⚠️  Running with --dangerously-skip-permissions"
    log "   This grants Claude full system access. Use in sandboxed environments only."
}

show_config() {
    log "Configuration:"
    log "  Max iterations:  $MAX_ITERATIONS"
    log "  Delay:           ${DELAY_SECONDS}s"
    log "  Pause mode:      $PAUSE_BETWEEN"
    log "  Log file:        ${LOG_FILE:-"(disabled)"}"
    log "  Prompt file:     $PROMPT_FILE"
    log "  Plan file:       $PLAN_FILE"
    log ""
}

# ============================================================================
# ARGUMENT PARSING
# ============================================================================

while [[ $# -gt 0 ]]; do
    case $1 in
        --max-iterations)
            [[ -n "${2:-}" ]] || die "--max-iterations requires a number"
            MAX_ITERATIONS="$2"
            shift 2
            ;;
        --delay)
            [[ -n "${2:-}" ]] || die "--delay requires a number"
            DELAY_SECONDS="$2"
            shift 2
            ;;
        --pause)
            PAUSE_BETWEEN=true
            shift
            ;;
        --log)
            [[ -n "${2:-}" ]] || die "--log requires a filename"
            LOG_FILE="$2"
            shift 2
            ;;
        --no-log)
            LOG_FILE=""
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            die "Unknown option: $1 (use --help for usage)"
            ;;
    esac
done

# ============================================================================
# MAIN EXECUTION
# ============================================================================

# Set up signal handlers for clean shutdown
trap cleanup EXIT
trap 'exit 130' INT TERM

# Initialize log file with header
if [[ -n "$LOG_FILE" ]]; then
    {
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Ralph Loop Started: $(date)"
        echo "Working Directory: $(pwd)"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    } >> "$LOG_FILE"
fi

log "🔄 Starting Ralph Loop"
show_config
preflight_check

log ""

while [[ $ITERATION -lt $MAX_ITERATIONS ]]; do
    ITERATION=$((ITERATION + 1))
    
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log "📍 Iteration $ITERATION / $MAX_ITERATIONS"
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Log the input (prompt being sent to Claude)
    PROMPT_CONTENT=$(cat "$PROMPT_FILE")
    if [[ -n "$LOG_FILE" ]]; then
        {
            echo ""
            echo "┌─ INPUT TO CLAUDE ─────────────────────────────────────────────"
            echo "$PROMPT_CONTENT"
            echo "└────────────────────────────────────────────────────────────────"
            echo ""
        } >> "$LOG_FILE"
    fi
    
    # Run Claude with the prompt, capturing output
    # The || true prevents set -e from exiting on non-zero Claude exit
    OUTPUT=$(echo "$PROMPT_CONTENT" | claude --dangerously-skip-permissions 2>&1) || true
    
    # Display output to terminal
    echo "$OUTPUT"
    
    # Log the output from Claude
    if [[ -n "$LOG_FILE" ]]; then
        {
            echo "┌─ OUTPUT FROM CLAUDE ──────────────────────────────────────────"
            echo "$OUTPUT"
            echo "└────────────────────────────────────────────────────────────────"
            echo ""
        } >> "$LOG_FILE"
    fi
    
    # Check for completion signal
    if echo "$OUTPUT" | grep -q "RALPH_COMPLETE"; then
        log ""
        log "✅ Ralph loop completed successfully!"
        log "   All tasks in $PLAN_FILE are done."
        exit 0
    fi
    
    # Check for blocker signal
    if echo "$OUTPUT" | grep -q "RALPH_BLOCKED"; then
        log ""
        log "⚠️  Ralph encountered a blocker."
        log "   Review the output above and $PLAN_FILE, then restart."
        exit 1
    fi
    
    # Optional pause for human review
    if [[ "$PAUSE_BETWEEN" == true ]]; then
        log ""
        read -r -p "Press Enter to continue (or Ctrl+C to stop)..."
    fi
    
    # Delay between iterations (skip on last iteration or if very short)
    if [[ $ITERATION -lt $MAX_ITERATIONS && $DELAY_SECONDS -gt 0 ]]; then
        sleep "$DELAY_SECONDS"
    fi
done

log ""
log "⚠️  Reached maximum iterations ($MAX_ITERATIONS)"
log "   Review progress in $PLAN_FILE and restart if needed."
exit 1
```

Write this to `ralph.sh` and make it executable with `chmod +x ralph.sh`.

---

# Execution

1. **Start the interview** - Begin asking questions immediately
2. **Be thorough** - Don't rush; good specs prevent bad loops
3. **Confirm before generating** - Summarize understanding and get approval
4. **Generate all four files** - Create them in order
5. **Provide instructions** - Tell user how to start the loop

After creating all files, output:

```
✅ Ralph loop initialized!

Files created:
  - SPEC.md (project specification)
  - IMPLEMENTATION_PLAN.md (task breakdown)
  - PROMPT.md (loop instruction set)
  - ralph.sh (orchestrator script)

To start the loop:
  chmod +x ralph.sh
  ./ralph.sh

Options:
  ./ralph.sh --help                # Show all options
  ./ralph.sh --max-iterations 25   # Limit iterations (default: 50)
  ./ralph.sh --delay 5             # Seconds between iterations (default: 2)
  ./ralph.sh --pause               # Pause for confirmation between iterations
  ./ralph.sh --log output.log      # Custom log file (default: ralph.log)
  ./ralph.sh --no-log              # Disable logging

⚠️  Recommended: Run in a sandbox (Docker/VM) since this uses --dangerously-skip-permissions
💡 First run: Use --pause to review each iteration before continuing
```

---

**Begin the interview now. Ask your first question.**