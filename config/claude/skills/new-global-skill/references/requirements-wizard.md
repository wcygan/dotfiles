---
title: Requirements Wizard
description: AskUserQuestion workflow for gathering global skill creation requirements
tags: [requirements, wizard, questions]
---

# Requirements Wizard

Use the AskUserQuestion tool to ask these four questions before creating any skill files.
Invoke all four questions in a single AskUserQuestion call.

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

## After Gathering Answers

1. Map capability to suggested name (see naming-and-descriptions.md for name table)
2. Apply invocation frontmatter:
   - "User-invoked only" → add `disable-model-invocation: true`
   - "Claude auto-invoked" → add `user-invocable: false`
   - "Both" → no invocation flags needed
3. Select matching template from skill-templates.md
4. If "Restricted" was chosen, apply allowed-tools from file-structure-and-tools.md
5. If "Advanced" was chosen, plan reference files alongside SKILL.md
6. Proceed to file creation only after all four answers are collected
