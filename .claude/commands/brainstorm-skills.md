---
description: Brainstorm useful skills that can be created for a project based on codebase analysis
---

Brainstorm useful Claude Code skills for this project. Focus area (if provided): $ARGUMENTS

## Your Task

Analyze the current project and brainstorm skills that would meaningfully improve the developer workflow. Skills are Claude Code's extensibility mechanism — reusable instructions that Claude can invoke automatically or that users trigger with `/skill-name`.

## Step 1: Understand the Project

Before brainstorming, gather context:

1. **Read CLAUDE.md** (project root and `.claude/` directory) for conventions, tech stack, and workflows
2. **Scan project structure** — look at top-level files (`package.json`, `flake.nix`, `Cargo.toml`, `pyproject.toml`, `Makefile`, `justfile`, `Dockerfile`, etc.) to understand the tech stack
3. **Check existing skills** — read `.claude/skills/*/SKILL.md` to avoid duplicating what's already there
4. **Check existing commands** — read `.claude/commands/*.md` to understand current slash commands
5. **Identify pain points** — look at CI configs, test directories, scripts, and common patterns that suggest repetitive workflows

If the user provided a focus area via `$ARGUMENTS`, prioritize brainstorming in that domain.

## Step 2: Brainstorm Skills

For each skill idea, provide:

### Skill Template

```
### <Skill Name> (`/skill-name`)
**Type:** [Reference | Task | Background Knowledge]
**Invocation:** [User-only | Claude-only | Both]
**Why:** <1-2 sentences on the problem this solves>
**What it does:** <Brief description of behavior>
**Trigger keywords:** <When Claude should auto-activate>
**Complexity:** [Simple | Advanced (needs scripts/templates)]
```

### Categories to Consider

Brainstorm across these categories, selecting only the ones relevant to this project:

1. **Code Generation** — scaffolding components, endpoints, modules following project patterns
2. **Testing** — generating tests, running test suites, coverage analysis, test data generation
3. **Code Review** — project-specific review criteria, style enforcement, anti-pattern detection
4. **Deployment & CI** — deploy workflows, CI debugging, release management
5. **Documentation** — generating docs, updating changelogs, API documentation
6. **Debugging** — project-specific debugging workflows, log analysis, error investigation
7. **Refactoring** — project-specific refactoring patterns, migration helpers
8. **DevOps & Infrastructure** — container management, environment setup, config management
9. **Dependency Management** — updating deps, auditing, compatibility checks
10. **Project-Specific Workflows** — unique workflows specific to this codebase's domain

### Quality Filters

Only suggest skills that:
- **Solve a real, recurring need** — not hypothetical one-off tasks
- **Benefit from Claude's capabilities** — code reading, multi-file analysis, generation
- **Aren't already covered** — check existing skills and commands first
- **Are specific enough** — "help with code" is not a skill; "generate fish shell function with tests" is

## Step 3: Present Results

Use the AskUserQuestion tool to let the user select which skills interest them. Present the top 5-8 most impactful ideas grouped by category.

**Question format:** "Which of these skills would you like to create?" with multi-select enabled.

Include a brief rationale for your top 3 picks based on what you observed in the codebase (e.g., "I noticed you have 15 fish functions but no automated way to scaffold new ones with tests").

## Step 4: Flesh Out Selected Skills

For each skill the user selects:

1. **Draft the full SKILL.md** content including frontmatter, description, and instructions
2. **Identify if it needs supporting files** (scripts, templates, reference docs)
3. **Determine the right scope:**
   - Project skill (`.claude/skills/`) — specific to this codebase
   - Global skill (`config/claude/skills/` in dotfiles, or `~/.claude/skills/`) — useful across all projects
4. **Show the user** the draft and ask for feedback before creating files

### Skill Authoring Best Practices

When drafting skills, follow these guidelines from the official documentation:

- **Descriptions matter most** — Claude uses the description to decide when to auto-activate. Include keywords users would naturally say.
- **Keep SKILL.md under 500 lines** — move detailed reference to separate files
- **Use `disable-model-invocation: true`** for task skills with side effects (deploy, commit, send messages)
- **Use `user-invocable: false`** for background knowledge (conventions, domain context)
- **Use `context: fork`** for heavy research/analysis that benefits from isolation
- **Use `allowed-tools`** to restrict permissions for safety
- **Use `$ARGUMENTS`** for skills that take parameters
- **Use `!`command`` syntax** to inject dynamic context (e.g., git status, file listings)

## If No Focus Area Was Provided

If `$ARGUMENTS` is empty, ask the user what area they'd like to focus on using AskUserQuestion:

- **Development workflow** — code generation, testing, debugging
- **DevOps & infrastructure** — CI/CD, deployment, environment management
- **Code quality** — reviews, refactoring, documentation
- **Let me analyze and suggest** — you'll scan the project and recommend
