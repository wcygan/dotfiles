---
allowed-tools: WebSearch, WebFetch, Write, Bash(gdate:*)
description: Perform fast web research with structured analysis and result synthesis
---

## Context

- Session ID: !`gdate +%s%N`
- Research query: $ARGUMENTS
- Results directory: /tmp/research-results-$SESSION_ID/
- Current timestamp: !`gdate '+%Y-%m-%d %H:%M:%S'`
- Working directory: !`pwd`

## Your Task

Execute a systematic web research workflow for the query: "$ARGUMENTS"

STEP 1: Initialize Research Session

- Create session state file: /tmp/research-state-$SESSION_ID.json
- Initialize results directory: /tmp/research-results-$SESSION_ID/
- Log research parameters and timestamp

STEP 2: Primary Web Search

- Execute WebSearch with query: "$ARGUMENTS"
- Analyze search results for relevance and authority
- Identify top 3-5 most relevant sources
- Filter for development-related, current, and authoritative content

STEP 3: Content Extraction

FOR EACH selected source:

- Use WebFetch to extract detailed content
- Focus on technical documentation, best practices, and current information
- Save individual source analysis to /tmp/research-results-$SESSION_ID/source-N.md
- Rate content quality and relevance (1-10 scale)

STEP 4: Synthesis and Analysis

- Combine findings from all sources
- Identify common patterns and recommendations
- Highlight conflicting information or outdated practices
- Create comprehensive summary with actionable insights

STEP 5: Structured Output

Generate final research report containing:

- Executive summary (2-3 sentences)
- Key findings (bulleted list)
- Recommended actions or next steps
- Source quality assessment
- Confidence level in findings

STEP 6: Session Cleanup

- Save final report to /tmp/research-results-$SESSION_ID/final-report.md
- Update session state with completion status
- Provide file locations for future reference

## Error Handling

TRY:

- Execute primary research workflow
  CATCH (WebSearch failures):
- Log error and attempt alternative search terms
- Provide partial results if any sources were successfully fetched
  CATCH (WebFetch failures):
- Skip failed sources and continue with available content
- Note limitations in final report
  FINALLY:
- Ensure session state is updated
- Clean up temporary files if requested

## Quality Assurance

- Verify all sources are accessible and current
- Cross-reference information across multiple sources
- Flag potentially outdated or unreliable information
- Provide confidence indicators for each finding

## Research Examples

**Technology Research:**

- "Next.js 15 new features" → Focus on official docs, release notes, migration guides
- "Python asyncio best practices 2024" → Prioritize recent articles, official Python docs
- "Docker security vulnerabilities" → Emphasize security advisories, CVE databases

**Development Focus:**

- Prioritize official documentation over blog posts
- Favor recent content (last 12 months) for rapidly evolving technologies
- Include practical examples and implementation guidance
- Verify information against multiple authoritative sources
