# Quick Web Research

Performs fast web research using WebSearch to find relevant information quickly.

## Usage

```bash
/quick-web-research <query>
```

## Description

This command performs a quick web research session by:

1. Using WebSearch to find relevant results for your query
2. Fetching content from the top 2-3 most relevant sources using WebFetch
3. Providing a concise summary of findings

Perfect for getting quick answers to development questions, finding current documentation, or checking the latest information on a topic.

## Examples

```bash
/quick-web-research "Next.js 15 new features"
/quick-web-research "Python asyncio best practices 2024"
/quick-web-research "Docker security vulnerabilities"
```

## Implementation

The command will:

- Execute a WebSearch with your query
- Identify the most relevant 2-3 results
- Use WebFetch to extract detailed content from those sources
- Synthesize findings into a concise, actionable summary
- Focus on development-related information and current best practices
