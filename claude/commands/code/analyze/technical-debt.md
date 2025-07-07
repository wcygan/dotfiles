---
allowed-tools: Read, Write, Bash(fd:*), Bash(rg:*), Bash(git:*), Bash(jq:*), Bash(gdate:*), Task
description: Comprehensive technical debt analysis with actionable remediation strategies
---

## Context

- Session ID: !`gdate +%s%N`
- Project root: !`pwd`
- Technology stack: !`fd "(Cargo\.toml|go\.mod|pom\.xml|deno\.json|package\.json)" . -d 2 | head -5 || echo "No technology files detected"`
- Project structure: !`fd . -t d -d 3 | head -10 || echo "No directories found"`
- Git status: !`git status --porcelain | head -5 || echo "Not a git repository"`
- Recent commits: !`git log --oneline -5 2>/dev/null || echo "No git history"`
- Current branch: !`git branch --show-current 2>/dev/null || echo "No git repository"`

## Your task

PROCEDURE comprehensive_technical_debt_analysis():

STEP 1: Environment Analysis and Session Setup

- Initialize session state file: /tmp/technical-debt-analysis-$SESSION_ID.json
- Detect project technology stack and create analysis matrix
- Identify available analysis tools based on detected technologies
- Set up analysis workspace and temporary directories
- Create progress tracking and checkpoint system

STEP 2: Parallel Technical Debt Analysis

Think deeply about optimal analysis strategy for this codebase.

Use 6 parallel agents to analyze different debt dimensions:

- **Agent 1: Code Quality and Complexity Analysis**
  - Cyclomatic complexity assessment using rg pattern matching
  - Function length analysis (>20 lines flagged)
  - Large file identification (>500 lines)
  - Code smell detection and anti-pattern identification

- **Agent 2: Dependency Health and Security Assessment**
  - Outdated dependency detection per technology stack
  - Security vulnerability scanning (cargo audit, govulncheck, etc.)
  - Unused dependency identification
  - License compliance verification

- **Agent 3: Performance Debt Identification**
  - Inefficient pattern detection (memory leaks, N+1 queries)
  - Resource management analysis (missing cleanup patterns)
  - Synchronous operations that could be async
  - Large allocation and performance bottleneck discovery

- **Agent 4: Test Coverage and Quality Evaluation**
  - Test coverage analysis per technology stack
  - Test quality assessment (flaky tests, missing assertions)
  - Test naming and structure evaluation
  - Missing test scenario identification

- **Agent 5: Documentation Gaps and Technical Writing Debt**
  - Public API documentation completeness
  - README and documentation currency assessment
  - Code comment debt (commented-out code, misleading comments)
  - Missing architectural documentation

- **Agent 6: Architecture Violations and Design Debt**
  - Circular dependency detection
  - Inappropriate dependency violations
  - High coupling indicator analysis
  - Feature flag sprawl assessment

Each agent works independently and generates structured findings.

STEP 3: Results Aggregation and Prioritization

- Collect findings from all analysis agents
- Create comprehensive debt assessment matrix
- Apply priority scoring (High/Medium/Low) based on:
  - Security impact and risk level
  - Performance impact on critical paths
  - Development velocity impact
  - Maintenance burden and complexity
- Generate quantified metrics and trend analysis

STEP 4: Remediation Roadmap Generation

IF critical security vulnerabilities found:

- Prioritize immediate security fixes in current sprint
- Document security remediation steps and verification

IF performance bottlenecks identified:

- Assess impact on user experience and system scalability
- Create performance improvement timeline

FOR EACH identified debt category:

- Estimate remediation effort (story points/hours)
- Identify dependencies and sequencing requirements
- Assign to appropriate timeline (immediate/short-term/long-term)

Create structured remediation plan:

```json
{
  "immediate_actions": [],
  "short_term_actions": [],
  "long_term_actions": [],
  "automation_opportunities": [],
  "prevention_strategies": []
}
```

STEP 5: State Management and Cleanup

TRY:

- Save comprehensive analysis results to state file
- Generate executive summary and detailed technical report
- Create automation setup recommendations (pre-commit hooks, CI integration)
- Update project-specific debt tracking if applicable

CATCH (analysis_complexity_overflow):

- Save partial results and current progress
- Create resumption plan for incomplete analysis areas
- Document analysis limitations and alternative approaches

FINALLY:

- Clean up temporary analysis files: /tmp/technical-debt-temp-$SESSION_ID-*
- Archive session artifacts for future comparison
- Update state file with completion status

## Analysis Commands Reference

### Modern Tool Usage Examples

**File Discovery (using fd instead of find):**

```bash
# Source files by language
fd "\.(rs|go|java|ts|js|py)$" src/

# Large files identification
fd "\.(rs|go|java|ts)$" . --exec wc -l {} \; | rg "^\s*[5-9][0-9]{2,}" | head -20

# Configuration files
fd "(config|\.env|\.yml|\.yaml|\.toml|\.json)$" . -d 3
```

**Code Pattern Analysis (using rg instead of grep):**

```bash
# Complexity indicators
rg "if|else|while|for|match|switch|case|catch|\?\?" --count-matches

# Anti-patterns
rg "unwrap\(\)|expect\(|panic!" --type rust -n
rg "interface\{\}" --type go -n
rg "instanceof|\.getClass\(\)" --type java -n

# Security patterns
rg "password.*=|secret.*=|key.*=|token.*=" -n
rg "eval\(|exec\(|system\(" -n
```

**Dependency Analysis:**

```bash
# Rust
cargo outdated --root-deps-only 2>/dev/null || echo "Cargo not available"
cargo audit 2>/dev/null || echo "cargo-audit not installed"

# Go
go list -u -m all 2>/dev/null | rg "\[" || echo "Go modules not available"
govulncheck ./... 2>/dev/null || echo "govulncheck not installed"

# Java Maven
./mvnw versions:display-dependency-updates 2>/dev/null || echo "Maven not available"

# Deno
deno info --json 2>/dev/null | jq '.modules[] | select(.specifier | startswith("http"))' 2>/dev/null || echo "Deno not available"
```

## State Management Schema

```json
{
  "sessionId": "$SESSION_ID",
  "timestamp": "ISO_8601_TIMESTAMP",
  "target": "$ARGUMENTS",
  "phase": "analysis_complete",
  "technology_stack": {
    "detected_languages": [],
    "build_tools": [],
    "frameworks": []
  },
  "analysis_results": {
    "code_quality": {
      "complexity_score": "number",
      "large_files_count": "number",
      "code_smells": []
    },
    "dependencies": {
      "outdated_count": "number",
      "vulnerabilities": [],
      "unused_dependencies": []
    },
    "performance": {
      "bottlenecks": [],
      "inefficient_patterns": [],
      "memory_issues": []
    },
    "testing": {
      "coverage_percentage": "number",
      "quality_issues": [],
      "missing_tests": []
    },
    "documentation": {
      "missing_docs": [],
      "outdated_docs": [],
      "comment_debt": []
    },
    "architecture": {
      "circular_dependencies": [],
      "coupling_issues": [],
      "design_violations": []
    }
  },
  "debt_priority_matrix": {
    "high_priority": [],
    "medium_priority": [],
    "low_priority": []
  },
  "remediation_roadmap": {
    "immediate_actions": [],
    "short_term_actions": [],
    "long_term_actions": []
  },
  "metrics": {
    "total_debt_score": "number",
    "trend_direction": "improving|stable|degrading",
    "technical_debt_ratio": "percentage"
  }
}
```

## Expected Deliverables

- Comprehensive technical debt assessment report with quantified metrics
- Prioritized remediation roadmap with effort estimates
- Security vulnerability analysis with immediate action items
- Dependency health report with update recommendations
- Code quality metrics with improvement opportunities
- Performance bottleneck identification with optimization strategies
- Test coverage gaps with testing strategy recommendations
- Documentation debt assessment with writing guidelines
- Architecture violation analysis with refactoring suggestions
- Automation setup guide for continuous debt monitoring
- CI/CD integration recommendations for debt prevention

## Automation Integration

- Pre-commit hooks for code quality enforcement
- CI pipeline checks for dependency security
- Regular dependency update automation
- Code quality gates for pull request approval
- Security scanning in deployment pipelines
- Technical debt tracking in project management tools
