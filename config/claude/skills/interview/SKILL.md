---
name: interview
description: Conduct an in-depth requirements interview to flesh out a plan or spec file. Ask non-obvious questions about technical implementation, UI & UX, tradeoffs, and concerns — then write the finalized spec back to the file. Use when you need to flesh out requirements, refine a spec, clarify a plan, or gather details before implementation. Keywords: interview, spec, plan, requirements, flesh out, questions, clarify spec, requirements gathering.
disable-model-invocation: true
argument-hint: [plan-file]
allowed-tools: AskUserQuestion, Read, Glob, Grep, Write, Edit
---

# Interview: Spec & Plan Refinement

Conduct an in-depth interview to flesh out a plan or specification, then write the finalized spec back to the file.

## Workflow

### 1. Load Context

If `$ARGUMENTS` references a file, read it to understand the current plan:

```
Read $ARGUMENTS
```

If no argument was provided, ask the user what topic or file they want to flesh out before proceeding.

### 2. Interview

Using the `AskUserQuestion` tool, conduct a thorough, non-obvious interview. Cover angles such as:

- **Technical implementation**: architecture decisions, data models, API design, performance requirements, edge cases, failure modes
- **UI & UX**: user flows, interaction patterns, error states, onboarding, accessibility
- **Tradeoffs**: build vs. buy, consistency vs. flexibility, simplicity vs. power, short-term vs. long-term
- **Concerns**: security, scalability, maintainability, cost, operational burden
- **Constraints**: timelines, team capabilities, external dependencies, non-negotiables
- **Success criteria**: how do we know it's done? what does "working" look like? what's out of scope?

**Rules:**
- Ask questions that expose hidden assumptions — not obvious ones
- Continue interviewing until the spec is complete; don't stop after a single round
- Each subsequent round should go deeper or cover an uncovered angle
- Surface contradictions and ambiguities in the existing plan and resolve them

### 3. Write the Spec

Once the interview is complete, write the finalized, detailed spec back to `$ARGUMENTS` (or ask for a filename if no argument was given).

Incorporate all decisions made during the interview. The output should be a complete, actionable spec — not just a summary of answers.
