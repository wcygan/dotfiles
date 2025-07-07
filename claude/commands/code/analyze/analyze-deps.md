---
allowed-tools: Bash, Read, Write
description: Analyze project dependencies with security, performance, and maintenance insights
---

## Context

- Session ID: !`gdate +%s%N`
- Current directory: !`pwd`
- Project files: !`fd "(deno\.json|package\.json|Cargo\.toml|go\.mod|pom\.xml|requirements\.txt|composer\.json)" . -t f | head -10 || echo "No project files detected"`
- Directory structure: !`fd . -t d -d 2 | head -10 || echo "No directories found"`
- Git status: !`git status --porcelain | head -5 || echo "Not a git repository"`
- Current branch: !`git branch --show-current 2>/dev/null || echo "No git repository"`
- Lock files: !`fd "(package-lock\.json|yarn\.lock|Cargo\.lock|go\.sum|poetry\.lock|deno\.lock)" . -t f | head -5 || echo "No lock files found"`

## Your Task

Analyze project dependencies using modern tools. Analysis type: $ARGUMENTS (security, outdated, size, licenses, graph, or all - defaults to 'all')

STEP 1: Initialize Analysis Session

- Create session state file: /tmp/analyze-deps-$SESSION_ID.json
- Detect project type from Context section
- Parse analysis type from $ARGUMENTS (default: 'all')
- Initialize analysis results structure

STEP 2: Project Type Detection and Setup

IF project files include "deno.json":

- SET project_type = "deno"
- SET package_manager = "deno"
  ELSE IF project files include "package.json":
- SET project_type = "node"
- SET package_manager = "npm" OR "yarn" (detect from lock files)
  ELSE IF project files include "Cargo.toml":
- SET project_type = "rust"
- SET package_manager = "cargo"
  ELSE IF project files include "go.mod":
- SET project_type = "go"
- SET package_manager = "go"
  ELSE IF project files include "pom.xml":
- SET project_type = "java"
- SET package_manager = "maven"
  ELSE:
- SET project_type = "unknown"
- WARN: "No recognized project files found"

STEP 3: Security Analysis

IF analysis_type IN ['security', 'all']:

TRY:

CASE project_type:
WHEN "deno":

- Check for security advisories in JSR imports
- Analyze remote dependencies for known vulnerabilities
- Generate security report

  WHEN "rust":
  - Run: cargo audit --json (if available)
  - Parse security advisories
  - Check crates.io for vulnerability reports

  WHEN "node":
  - Run: npm audit --json OR yarn audit --json
  - Parse vulnerability data
  - Check for known problematic packages

  WHEN "go":
  - Run: go list -json -m all (check for known issues)
  - Check Go vulnerability database
  - Analyze module security status

CATCH (security_scan_failure):

- Log error to session state
- Continue with other analysis types
- Note: Manual security review recommended

STEP 4: Performance Analysis

IF analysis_type IN ['size', 'performance', 'all']:

TRY:

CASE project_type:
WHEN "deno":

- Analyze import map sizes
- Check for large remote dependencies
- Estimate bundle impact

  WHEN "rust":
  - Run: cargo tree --format "{p}" | head -20
  - Analyze compilation impact
  - Check for duplicate dependencies

  WHEN "node":
  - Calculate node_modules size
  - Analyze bundle size contributors
  - Check for large packages

  WHEN "go":
  - Run: go list -m all | head -20
  - Analyze module sizes
  - Check dependency depth

CATCH (performance_analysis_failure):

- Log error to session state
- Provide manual analysis guidance

STEP 5: Maintenance Analysis

IF analysis_type IN ['outdated', 'maintenance', 'all']:

TRY:

FOR EACH detected package manager:

- Check for outdated dependencies
- Analyze maintenance status
- Generate update recommendations
- Assess breaking change risks

CATCH (maintenance_check_failure):

- Log warning to session state
- Recommend manual dependency review

STEP 6: Generate Comprehensive Report

TRY:

- Compile all analysis results from session state
- Create dependency summary with counts and types
- Generate security risk assessment
- Provide maintenance recommendations
- Calculate dependency health score
- Save final report to session state

STEP 7: Present Results

- Display analysis summary in structured format
- Highlight critical security issues
- Show outdated dependency priorities
- Provide actionable next steps
- Save report to: /tmp/analyze-deps-report-$SESSION_ID.json

CATCH (report_generation_failure):

- Provide partial results
- Log error details
- Offer manual analysis steps

FINALLY:

- Update session state with completion status
- Clean up temporary analysis files
- Archive session data for future reference

## State Management

```json
// /tmp/analyze-deps-$SESSION_ID.json
{
  "sessionId": "$SESSION_ID",
  "timestamp": "ISO_8601_TIMESTAMP",
  "projectType": "detected_project_type",
  "analysisType": "$ARGUMENTS",
  "phase": "analysis_complete",
  "results": {
    "security": {
      "vulnerabilities": [],
      "riskLevel": "low|medium|high",
      "recommendations": []
    },
    "performance": {
      "bundleSize": "estimated_size",
      "dependencyCount": 0,
      "largestDependencies": []
    },
    "maintenance": {
      "outdatedCount": 0,
      "outdatedPackages": [],
      "updatePriority": "low|medium|high"
    }
  },
  "recommendations": [
    "Priority actions based on analysis"
  ],
  "healthScore": "0-100",
  "nextActions": [
    "Specific next steps for dependency management"
  ]
}
```

## Modern Tool Integration

- **fd**: Fast file discovery for project detection
- **rg**: Security pattern searching in lock files
- **jq**: JSON processing for package manager outputs
- **bat**: Syntax-highlighted output for better readability
- **Modern package managers**: Native audit and analysis commands

## Example Usage

```bash
# Complete dependency analysis
/analyze-deps

# Security-focused analysis only
/analyze-deps security

# Check for outdated packages
/analyze-deps outdated

# Bundle size and performance analysis
/analyze-deps size

# License compliance analysis
/analyze-deps licenses
```
