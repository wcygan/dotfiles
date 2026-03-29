---
title: Requirements Wizard
description: AskUserQuestion workflow for gathering global skill creation requirements
tags: [requirements, wizard, questions]
---

# Requirements Wizard

Use the AskUserQuestion tool to ask these five questions before creating any skill files.
Invoke all five questions in a single AskUserQuestion call.

## Question 1: Capability

```
What capability should this global skill provide?
Header: "Capability"
Options:
  - "Code Analysis"    / "Analyze code for patterns, quality, security issues"
  - "Test Generation"  / "Generate comprehensive test suites"
  - "Documentation"    / "Create docs, READMEs, API documentation"
  - "Data Processing"  / "Process files like PDFs, CSVs, JSON"
multiSelect: false
```

## Question 2: Invocation Mode

```
How should this skill be triggered?
Header: "Invocation"
Options:
  - "User-invoked only (/skill-name)"  / "Only activates when user types /skill-name"
  - "Claude auto-invoked"              / "Claude loads it automatically when relevant"
  - "Both (user + auto)"               / "User can call /skill-name and Claude can auto-trigger"
multiSelect: false
```

## Question 3: Scope

```
Skill scope — simple or advanced?
Header: "Complexity"
Options:
  - "Simple (single SKILL.md)"   / "Just instructions, no scripts or templates"
  - "Advanced (with resources)"  / "Include scripts, templates, or reference docs"
multiSelect: false
```

## Question 4: Tool Access

```
Should tools be restricted?
Header: "Tool Access"
Options:
  - "Full access"  / "Skill can use all available tools"
  - "Restricted"   / "Limit to specific tools (Read, Grep, etc.)"
multiSelect: false
```

## Question 5: Execution Context

```
Where should this skill execute?
Header: "Execution Context"
Options:
  - "Inline (main conversation)"  / "Runs in the current conversation context"
  - "Forked (isolated subagent)"  / "Runs in a separate subagent — no conversation history"
multiSelect: false
```

If "Forked" is chosen, ask a follow-up:

```
Which agent type for the forked skill?
Header: "Agent Type"
Options:
  - "Explore (read-only)"       / "Fast, read-only exploration — best for analysis tasks"
  - "General-purpose (default)" / "Full capabilities — use when skill spawns sub-agents or writes files"
multiSelect: false
```

## After Gathering Answers

1. Map capability to suggested name (see naming-and-descriptions.md for name table)
2. Apply invocation frontmatter:
   - "User-invoked only" → add `disable-model-invocation: true`
   - "Claude auto-invoked" → add `user-invocable: false`
   - "Both" → no invocation flags needed
3. Apply execution context frontmatter:
   - "Forked" → add `context: fork`
   - "Forked" + "Explore" → add `context: fork` and `agent: Explore`
   - "Forked" + "General-purpose" → add `context: fork` (no agent field needed)
   - "Inline" → no context field needed
4. Select matching template from skill-templates.md (use forked analysis template if forked)
5. If "Restricted" was chosen, apply allowed-tools from file-structure-and-tools.md
6. If "Advanced" was chosen, plan reference files alongside SKILL.md
7. If "Forked" was chosen, add `!`command`` blocks for injecting project state
8. Proceed to file creation only after all five answers are collected
