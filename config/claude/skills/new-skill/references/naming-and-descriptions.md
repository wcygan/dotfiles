---
title: Naming & Descriptions
description: Rules for skill names and descriptions with good/bad examples
tags: [naming, descriptions, templates, examples]
---

# Naming & Descriptions

## Name Generation

Based on capability, suggest:

| Capability    | Suggested Name           |
|---------------|--------------------------|
| Code Analysis | `code-quality-analyzer`  |
| Test Generation | `test-suite-generator` |
| Documentation | `doc-generator`          |
| Data Processing | `data-processor`       |
| Custom        | descriptive kebab-case   |

**Naming rules:**
- Lowercase letters, numbers, hyphens only
- Max 64 characters
- Descriptive (what it does, not how)
- Examples: `pdf-text-extractor`, `api-doc-generator`, `test-coverage-analyzer`

## Description Template

```
[Primary function]. [Secondary capabilities]. Use when [trigger scenarios]. Keywords: [comma-separated terms].
```

**Requirements:**
1. What it does (functionality)
2. When to use it (trigger conditions)
3. Trigger keywords (terms users might mention)
4. Max 1024 characters total

## Good Examples

✅ "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files, documents, or form processing. Keywords: PDF, extract, document, form, merge"

✅ "Generate comprehensive unit and integration tests with high coverage. Use when adding tests, improving coverage, or implementing TDD. Keywords: test, testing, coverage, unit test, integration test, TDD"

✅ "Analyze code for security vulnerabilities, performance issues, and maintainability problems. Use when reviewing code or conducting security audits. Keywords: security, vulnerability, code review, audit, performance"

## Bad Examples

❌ "Helps with documents" — too vague, no triggers, no keywords
❌ "Processes things" — no triggers, no subject matter
❌ "Does code stuff" — non-descriptive, won't match any user request

## Three Skill Patterns

Different patterns need different description styles:

### 1. Reference (inline, auto-invoked)

Background knowledge Claude applies automatically. Description should be broad and
keyword-rich so Claude picks it up in relevant contexts.

```
description: Work with GitHub from the command line using the GitHub CLI (gh). Use when managing repositories, pull requests, issues, releases, or any GitHub operations. Keywords: github, gh, pull request, PR, issue, release
```

**Style**: broad triggers, many keywords, no action verbs like "run" or "execute"

### 2. Task (user-invoked, inline)

Step-by-step workflows triggered with `/name`. Description should be specific about
what the workflow does end-to-end.

```
description: Analyze staged changes and create a well-crafted conventional commit. Use when committing code, writing commit messages, or preparing changes for review. Keywords: commit, git commit, staged changes
```

**Style**: specific workflow scope, outcome-focused, mention the trigger scenarios

### 3. Forked (subagent context)

Isolated analysis tasks. Description should emphasize the analysis output since the
user won't interact with the skill mid-run.

```
description: Deep analysis of project dependencies for outdated packages, security vulnerabilities, and license issues. Returns structured findings with severity levels. Keywords: dependency, audit, security, CVE, outdated
```

**Style**: emphasize output format, mention "returns" or "reports", note isolation won't interact
