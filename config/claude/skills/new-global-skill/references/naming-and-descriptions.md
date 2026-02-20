---
title: Naming & Descriptions
description: Rules for global skill names and descriptions with good/bad examples
tags: [naming, descriptions, templates, examples]
---

# Naming & Descriptions

## Name Generation

Based on capability, suggest:

| Capability      | Suggested Name           |
|-----------------|--------------------------|
| Code Analysis   | `code-quality-analyzer`  |
| Test Generation | `test-suite-generator`   |
| Documentation   | `doc-generator`          |
| Data Processing | `data-processor`         |
| Custom          | descriptive kebab-case   |

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

✅ "Review code for security vulnerabilities, performance issues, and best practices. Use when reviewing PRs, auditing code, or checking for bugs. Keywords: review, security, audit, PR, code review"

## Bad Examples

❌ "Helps with documents" — too vague, no triggers, no keywords
❌ "Processes things" — no triggers, no subject matter
❌ "Does code stuff" — non-descriptive, won't match any user request

## Global Skill Note

Global skills run across all projects — descriptions should not mention project-specific
frameworks or assumptions. Prefer language like "any codebase", "projects using X",
or make mentions of tech stack conditional.
