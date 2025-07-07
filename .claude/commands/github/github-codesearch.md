---
allowed-tools: WebFetch
description: Search GitHub for code using GitHub's search API (requires authentication)
---

## Context

- Session ID: !`gdate +%s%N`
- Search query: $ARGUMENTS
- Current directory: !`pwd`

## Your task

Search GitHub for code using the provided query and display the results in a formatted, readable way.

Steps:

1. Validate that a search query was provided
2. Make a request to GitHub's search API using the query
3. Parse and format the search results
4. Display the results with:
   - Repository name and description
   - File path and relevant code snippet
   - Direct link to the file on GitHub
   - Total number of results found

API endpoint: https://api.github.com/search/code?q={query}

Example queries:

- `path:**/*.rs` - Search for Rust files
- `language:javascript react` - Search for JavaScript files containing "react"
- `extension:md documentation` - Search for Markdown files containing "documentation"
- `filename:package.json` - Search for package.json files

Handle errors gracefully:

- If no query provided, show usage examples
- If authentication required (401 error):
  - Explain that GitHub code search requires authentication
  - Provide instructions on setting up GitHub token or using GitHub CLI
  - Suggest alternative: use repository search instead
- If API rate limit exceeded, inform user to try again later
- If no results found, suggest refining the search query
- If API error occurs, display the error message

**Authentication Options:**

1. Use GitHub CLI: `gh auth login` (recommended)
2. Set GitHub token in environment variable
3. Use repository search as fallback (no authentication required)

Format output as:

```
🔍 GitHub Code Search Results for: {query}

Found {total_count} results:

📁 {repository_name} - {repository_description}
📄 {file_path}
🔗 {html_url}

{code_snippet}

---
```

Limit display to first 10 results for readability.
