---
allowed-tools: Read, Bash(git log:*), Bash(git diff:*), Bash(git branch:*), Bash(gh pr list:*), Bash(gh issue list:*), Bash(rg:*), Bash(fd:*), Bash(gdate:*), Bash(jq:*), Write
description: Generate comprehensive retrospective analysis with structured learning extraction and actionable improvements
---

## Context

- Session ID: !`gdate +%s%N 2>/dev/null || date +%s%N 2>/dev/null || echo "$(date +%s)$(jot -r 1 100000 999999 2>/dev/null || shuf -i 100000-999999 -n 1 2>/dev/null || echo $RANDOM$RANDOM)"`
- Reflection scope: $ARGUMENTS
- Current branch: !`git branch --show-current 2>/dev/null || echo "no-git-repo"`
- Recent commits (last 10): !`git log --oneline -10 --since="1 week ago" 2>/dev/null || echo "No recent commits found"`
- Recent PRs: !`gh pr list --state all --limit 5 --json number,title,state,createdAt 2>/dev/null | jq -r '.[] | "#\(.number): \(.title) [\(.state)]"' 2>/dev/null || echo "No PR data available"`
- Open issues: !`gh issue list --state open --limit 5 --json number,title,labels 2>/dev/null | jq -r '.[] | "#\(.number): \(.title)"' 2>/dev/null || echo "No issue data available"`
- Project structure: !`fd . -t f -d 2 | head -10 2>/dev/null || echo "Limited file discovery"`
- Code changes analysis: !`git diff --stat HEAD~5..HEAD 2>/dev/null || echo "No recent changes to analyze"`
- Test results: !`rg "test.*pass|fail|error" . --type log -A 1 -B 1 | head -10 2>/dev/null || echo "No test logs found"`

## Your Task

STEP 1: Initialize reflection session and analyze scope

- CREATE session state file: `/tmp/reflection-session-$SESSION_ID.json`
- DETERMINE reflection timeframe and boundaries
- ANALYZE available data sources from Context section
- IDENTIFY key stakeholders and objectives for the reflection period

STEP 2: Multi-dimensional analysis with systematic data gathering

TRY:

- EXTRACT quantitative metrics from git history and project data
- ANALYZE recent code changes, PR patterns, and issue resolution
- EXAMINE development velocity and quality indicators
- REVIEW decision points and architectural choices
- ASSESS team collaboration patterns and communication effectiveness

STEP 3: Generate structured retrospective analysis

**Reflection Analysis Framework:**

FOR EACH reflection dimension:

**1. Context Establishment (Session State: analyzing)**

```json
{
  "period_scope": "$ARGUMENTS or current session",
  "key_objectives": "extracted from git commits and PR descriptions",
  "stakeholders": "identified from git contributors and PR reviewers",
  "data_sources": ["git_history", "github_activity", "code_metrics", "test_results"]
}
```

**2. Success Pattern Recognition (Session State: extracting_positives)**

- ANALYZE successful implementations from git history
- IDENTIFY high-velocity periods and their characteristics
- EXTRACT effective collaboration patterns from PR reviews
- DOCUMENT technical achievements and breakthroughs
- RECOGNIZE process improvements that increased efficiency

**3. Challenge and Improvement Analysis (Session State: analyzing_challenges)**

- MAP technical debt accumulation patterns
- IDENTIFY bottlenecks in development workflow
- ANALYZE failed or reverted commits for learning opportunities
- REVIEW unresolved issues and their root causes
- ASSESS communication gaps from delayed PR reviews

**4. Learning Extraction (Session State: synthesizing_insights)**

- CORRELATE decisions with outcomes using git history
- EXTRACT architectural lessons from code evolution
- IDENTIFY skill development from commit complexity progression
- DOCUMENT domain knowledge gained through feature implementations
- SYNTHESIZE process discoveries from workflow patterns

**5. Decision Impact Assessment (Session State: evaluating_decisions)**

- REVIEW major architectural decisions from commit messages
- MEASURE outcomes against original objectives
- ANALYZE alternative paths considered but not taken
- ASSESS trade-offs made and their long-term impact
- DOCUMENT lessons for future decision-making

**6. Quantitative Analysis (Session State: measuring_metrics)**

IF data available:

- CALCULATE development velocity (commits per week, PR frequency)
- MEASURE code quality trends (test coverage changes, complexity metrics)
- ANALYZE collaboration health (review turnaround, contributor diversity)
- TRACK issue resolution patterns and cycle times

**7. Actionable Improvement Generation (Session State: generating_actions)**

- PRIORITIZE improvements by impact and effort
- CREATE SMART goals for next iteration
- DESIGN experiments to test process improvements
- PLAN technical debt reduction strategies
- SCHEDULE learning and skill development activities

STEP 4: Generate comprehensive retrospective document

CREATE structured reflection document with:

**📍 Executive Summary**

- Period analyzed and key metrics
- Top 3 successes and top 3 improvement areas
- Overall health assessment and trajectory

**✅ Achievements & Successes**

- Technical milestones with specific examples
- Process improvements with measurable impact
- Team collaboration highlights with evidence
- Individual growth demonstrations

**🔄 Areas for Improvement**

- Technical challenges with root cause analysis
- Process bottlenecks with proposed solutions
- Communication gaps with remediation strategies
- Resource optimization opportunities

**💡 Key Insights & Learnings**

- Technical patterns and architectural lessons
- Process discoveries and workflow optimizations
- Team dynamics evolution and collaboration patterns
- Domain knowledge expansion and user understanding

**🎯 Decision Analysis**

- Major decisions made with outcome assessment
- Trade-offs evaluated and their impact
- Alternative approaches considered
- Lessons for future decision-making

**📊 Quantitative Analysis**

- Development velocity trends
- Quality metrics evolution
- Collaboration health indicators
- Performance and efficiency measurements

**🚀 Action Plan**

- Immediate wins (next 1-2 weeks)
- Process improvements (next iteration)
- Technical improvements (next quarter)
- Learning and development goals

**🎉 Recognition & Celebrations**

- Individual contributions highlighted
- Team achievements acknowledged
- Problem-solving excellence recognized
- Growth milestones celebrated

STEP 5: Save reflection artifacts and state

- SAVE reflection document to `/tmp/reflection-output-$SESSION_ID.md`
- UPDATE session state with completion status
- CREATE follow-up action items for task tracking
- GENERATE summary for team sharing

CATCH (insufficient_data):

- DOCUMENT data limitations and gaps
- PROVIDE reflection based on available information
- SUGGEST additional data collection for future reflections
- OFFER alternative reflection approaches

FINALLY:

- CLEAN up temporary session files
- REPORT reflection completion status
- PROVIDE next steps for action item implementation

**Quality Standards:**

- Specific examples over generic observations
- Data-driven insights where possible
- Balanced perspective (positives and improvements)
- Forward-looking and actionable
- Growth-oriented rather than purely documentary
- Constructive and solution-focused approach
