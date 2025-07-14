Your goal is to generate concise, actionable TL;DR summaries with progressive disclosure for any content type.

Ask for the target content (file path, directory, or topic) if not provided.

## Requirements

- Create three levels of detail: 30-second, 2-minute, and 5-minute versions
- Focus on actionable insights and immediate next steps
- Adapt format based on content type (technical, documentation, project, or discussion)
- Use clear hierarchy with most important information first
- Include concrete next steps and critical warnings

## Context Files

Include relevant files from your project to understand the structure and content. Examples:

**Project Overview**: Include files that provide project context

- README.md
- package.json (Node.js projects)
- deno.json (Deno projects)
- Cargo.toml (Rust projects)
- go.mod (Go projects)

**Documentation**: Include files that contain the content to summarize

- docs/ directory
- src/ directory (for code analysis)
- Any specific files mentioned by the user

## Analysis Process

### Step 1: Content Analysis

Analyze the provided content to understand:

- **Content type**: File, directory, codebase, documentation, or discussion topic
- **Complexity level**: Simple, moderate, or complex
- **Target audience**: Technical, business, or mixed
- **Key information hierarchy**: Critical vs. supporting details

### Step 2: Strategy Selection

Based on content type, apply appropriate summarization approach:

- **Technical/Code**: Focus on functionality, architecture, and implementation
- **Documentation**: Extract key insights and actionable recommendations
- **Project/Feature**: Emphasize goals, status, risks, and next steps
- **Discussion/Meeting**: Highlight decisions, action items, and open questions

### Step 3: Progressive Disclosure Generation

Create three levels of detail:

1. **30-Second Version**: Absolute essentials only
2. **2-Minute Version**: Key points with minimal context
3. **5-Minute Version**: Complete overview with full details

## TL;DR Structure Requirements

### Standard Format

```markdown
# TL;DR: [Content Name]

## 🎯 30-Second Version

[One paragraph with absolute essentials]

## ⚡ 2-Minute Version

### Bottom Line

[1-2 sentences with most critical takeaway]

### Key Points

- [Most important fact/decision]
- [Second most important point]
- [Third critical element]

### Immediate Action

[Single most important next step]

## 📋 5-Minute Version

### Complete Overview

[Detailed analysis with full context]

### All Key Points

- [Comprehensive list of important facts]
- [Supporting details and context]
- [Constraints and dependencies]

### Next Steps

1. [Immediate action - what to do first]
2. [Follow-up action - what to do next]
3. [Future consideration - what to plan for]

### Critical Notes

- [Important warnings or constraints]
- [Key dependencies or requirements]
- [Risks or limitations to be aware of]

### Resources

- [Essential links or documents]
- [Key people to contact]
- [Tools or systems to use]
```

## Content-Specific Templates

### For Technical/Code Content

```markdown
# TL;DR: [Component/System]

## What It Does

[One sentence description of purpose]

## Key Components

- [Main module/service]: [What it handles]
- [Secondary component]: [Its role]
- [Integration point]: [How it connects]

## To Get Started

1. [Setup/installation step]
2. [Configuration requirement]
3. [First thing to run/test]

## Common Issues

- [Most frequent problem and fix]
- [Performance consideration]

## Who to Ask

- [Subject matter expert]
- [Documentation location]
```

### For Documentation Content

```markdown
# TL;DR: [Document Name]

## Main Message

[Core thesis or argument in one sentence]

## Key Takeaways

- [Most important insight]
- [Critical fact or data point]
- [Actionable recommendation]

## Implementation

1. [First step to apply this knowledge]
2. [How to measure success]

## Skip This If

- [When this doesn't apply]
- [Prerequisites not met]
```

### For Project/Feature Content

```markdown
# TL;DR: [Project Name]

## Goal

[What we're trying to achieve]

## Status

[Current phase and % complete]

## Key Risks

- [Biggest concern]
- [Timeline risk]

## Need From You

- [Specific ask or decision needed]
- [Resource requirement]

## Timeline

- [Key milestone dates]
```

## Quality Requirements

- **Brevity**: Maximum 5 bullet points per section
- **Actionability**: Focus on what to do, not just what to know
- **Hierarchy**: Most important information first
- **Clarity**: Use simple, direct language
- **Context**: Include just enough background for understanding

## Output Validation

Ensure the TL;DR:

- [ ] Can be read in specified time limits (30s/2min/5min)
- [ ] Includes concrete next steps
- [ ] Highlights biggest risks and concerns
- [ ] Provides contact info or resource references
- [ ] Uses bullet points and short sentences consistently
- [ ] Follows appropriate template for content type

#file:README.md #file:package.json #file:deno.json #file:docs/ #file:src/
