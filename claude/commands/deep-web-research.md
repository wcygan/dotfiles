# Deep Web Research

Performs comprehensive web research with thorough analysis across multiple sources and perspectives.

## Usage

```bash
/deep-web-research <query>
```

## Description

This command performs an extensive web research session by:

1. Conducting multiple WebSearch queries with different angles and keywords
2. Fetching content from 8-12 diverse sources using WebFetch
3. Cross-referencing information across sources for accuracy
4. Analyzing trends, patterns, and conflicting viewpoints
5. Providing a comprehensive report with detailed findings and recommendations

Takes 3-5x longer than quick-web-research to ensure thorough coverage of the topic.

## Examples

```bash
/deep-web-research "Kubernetes security best practices enterprise deployment"
/deep-web-research "React vs Vue vs Angular 2024 comparison"
/deep-web-research "microservices architecture patterns pros cons"
```

## Implementation

The command will:

- Execute multiple WebSearch queries with varied keywords and perspectives
- Identify 8-12 high-quality sources across different types (docs, blogs, forums, papers)
- Use WebFetch to extract comprehensive content from each source
- Analyze information for:
  - Current best practices and emerging trends
  - Common pitfalls and lessons learned
  - Different implementation approaches
  - Community consensus vs. debates
- Cross-reference claims across sources for validation
- Synthesize findings into a detailed report with:
  - Executive summary
  - Key findings and insights
  - Recommended approaches
  - Potential risks and considerations
  - Further reading suggestions

Perfect for architectural decisions, technology evaluations, and deep technical research.
