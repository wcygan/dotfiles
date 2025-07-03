# /flaky-fix

Detect, analyze, and fix flaky tests for $ARGUMENT using intelligent pattern recognition and automated stabilization techniques.

## Context Intelligence

### Test Framework Detection

**Identify Test Framework and History:**

```bash
# Detect testing framework and locate test files
if [ -f "deno.json" ]; then
  FRAMEWORK="deno"
  TEST_FILES=$(fd "test|spec" --extension ts --extension js)
elif [ -f "Cargo.toml" ]; then
  FRAMEWORK="rust"
  TEST_FILES=$(fd "_test\.rs$|tests/" --type f)
elif [ -f "go.mod" ]; then
  FRAMEWORK="go"
  TEST_FILES=$(fd "_test\.go$")
elif [ -f "package.json" ]; then
  FRAMEWORK="node"
  TEST_FILES=$(fd "(test|spec)\.(js|ts|jsx|tsx)$")
elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
  FRAMEWORK="python"
  TEST_FILES=$(fd "test_.*\.py$|.*_test\.py$")
else
  echo "Unknown testing framework"
  exit 1
fi
```

### CI/CD Integration Detection

**Extract Test Results from CI History:**

```bash
# GitHub Actions test results
if [ -d ".github/workflows" ]; then
  gh run list --limit 100 --json status,conclusion,createdAt,workflowName > ci_history.json
  
  # Extract failed test names from workflow logs
  for run_id in $(jq -r '.[] | select(.conclusion == "failure") | .databaseId' ci_history.json); do
    gh run view $run_id --log | rg "FAIL:|Error:|Failed:" > "failed_tests_${run_id}.log"
  done
fi

# GitLab CI results
if [ -f ".gitlab-ci.yml" ]; then
  # Extract from GitLab API if available
  curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "https://gitlab.com/api/v4/projects/$PROJECT_ID/pipelines?status=failed&per_page=100" \
    > gitlab_failures.json
fi
```

## Flaky Test Analysis

### 1. Pattern Recognition

**Test Failure Pattern Analysis:**

```bash
# Analyze test output patterns for common flaky indicators
analyze_flaky_patterns() {
  local test_logs="$1"
  
  echo "🔍 Analyzing flaky test patterns..."
  
  # Common flaky test indicators
  rg "TimeoutError|timeout|timed out" "$test_logs" --count --no-filename
  rg "Race condition|race|concurrent|parallel" "$test_logs" --count --no-filename
  rg "Network error|connection|ECONNREFUSED|502|503|504" "$test_logs" --count --no-filename
  rg "Random|Math\.random|uuid|timestamp" "$test_logs" --count --no-filename
  rg "Element not found|NoSuchElementException|element is not visible" "$test_logs" --count --no-filename
  rg "Database.*lock|deadlock|transaction" "$test_logs" --count --no-filename
  
  # Generate pattern report
  cat > flaky_patterns.json << EOF
{
  "timing_issues": $(rg "timeout|timed out|TimeoutError" "$test_logs" --count --no-filename || echo 0),
  "race_conditions": $(rg "race|concurrent|parallel" "$test_logs" --count --no-filename || echo 0),
  "network_issues": $(rg "Network error|connection|ECONNREFUSED" "$test_logs" --count --no-filename || echo 0),
  "randomness": $(rg "Random|Math\.random|uuid" "$test_logs" --count --no-filename || echo 0),
  "ui_timing": $(rg "Element not found|not visible" "$test_logs" --count --no-filename || echo 0),
  "database_issues": $(rg "Database.*lock|deadlock" "$test_logs" --count --no-filename || echo 0)
}
EOF
}
```

**Test Stability Score Calculation:**

```typescript
// Generated flaky test analyzer
interface TestRun {
  name: string;
  timestamp: string;
  status: "pass" | "fail" | "skip";
  duration: number;
  error?: string;
}

interface FlakeScore {
  testName: string;
  totalRuns: number;
  failures: number;
  flakeRate: number;
  avgDuration: number;
  patterns: string[];
  severity: "low" | "medium" | "high" | "critical";
}

export class FlakyTestAnalyzer {
  analyzeTestStability(testRuns: TestRun[], threshold = 3): FlakeScore[] {
    const testGroups = this.groupTestsByName(testRuns);

    return Object.entries(testGroups).map(([testName, runs]) => {
      const failures = runs.filter((r) => r.status === "fail").length;
      const totalRuns = runs.length;
      const flakeRate = failures / totalRuns;

      const avgDuration = runs.reduce((sum, r) => sum + r.duration, 0) / totalRuns;
      const patterns = this.detectPatterns(runs);

      return {
        testName,
        totalRuns,
        failures,
        flakeRate,
        avgDuration,
        patterns,
        severity: this.calculateSeverity(flakeRate, failures, threshold),
      };
    }).filter((score) => score.failures >= threshold);
  }

  private detectPatterns(runs: TestRun[]): string[] {
    const patterns: string[] = [];
    const failedRuns = runs.filter((r) => r.status === "fail");

    // Time-based patterns
    const durations = runs.map((r) => r.duration);
    const avgDuration = durations.reduce((a, b) => a + b, 0) / durations.length;
    const stdDev = Math.sqrt(
      durations.reduce((sq, n) => sq + Math.pow(n - avgDuration, 2), 0) / durations.length,
    );

    if (stdDev > avgDuration * 0.5) {
      patterns.push("inconsistent_timing");
    }

    // Error patterns
    const errorTypes = failedRuns.map((r) => this.categorizeError(r.error || ""));
    const uniqueErrors = [...new Set(errorTypes)];

    if (uniqueErrors.includes("timeout")) patterns.push("timeout_issues");
    if (uniqueErrors.includes("network")) patterns.push("network_dependency");
    if (uniqueErrors.includes("race")) patterns.push("race_condition");
    if (uniqueErrors.includes("ui_timing")) patterns.push("ui_synchronization");

    return patterns;
  }

  private categorizeError(error: string): string {
    if (/timeout|timed out/i.test(error)) return "timeout";
    if (/network|connection|refused/i.test(error)) return "network";
    if (/race|concurrent/i.test(error)) return "race";
    if (/element.*not.*found|not.*visible/i.test(error)) return "ui_timing";
    if (/random|uuid/i.test(error)) return "randomness";
    return "unknown";
  }

  private calculateSeverity(
    flakeRate: number,
    failures: number,
    threshold: number,
  ): "low" | "medium" | "high" | "critical" {
    if (flakeRate > 0.5 || failures > threshold * 3) return "critical";
    if (flakeRate > 0.3 || failures > threshold * 2) return "high";
    if (flakeRate > 0.1 || failures > threshold) return "medium";
    return "low";
  }
}
```

### 2. Test History Mining

**Git-Based Test History Analysis:**

```bash
# Extract test history from git commits
extract_test_history() {
  echo "📊 Extracting test history from git..."
  
  # Get commits that touched test files in last 30 days
  git log --since="30 days ago" --oneline --name-only | \
    rg "test|spec" | sort | uniq > recent_test_changes.txt
  
  # Find commits with test failures
  git log --since="30 days ago" --grep="test.*fail\|fix.*test\|flaky" \
    --oneline > test_failure_commits.txt
  
  # Extract CI failure patterns
  git log --since="30 days ago" --oneline \
    --grep="ci.*fail\|build.*fail\|pipeline.*fail" > ci_failure_commits.txt
}

# Analyze test file modification patterns
analyze_test_modifications() {
  echo "🔄 Analyzing test modification patterns..."
  
  # Tests that are frequently modified (potential maintenance issues)
  git log --since="30 days ago" --name-only --pretty=format: | \
    rg "test|spec" | sort | uniq -c | sort -nr | head -20 > frequently_modified_tests.txt
  
  # Tests that haven't been touched (potential maintenance debt)
  find tests/ -name "*.ts" -o -name "*.js" -o -name "*.rs" -o -name "*.go" -o -name "*.py" | \
    while read test_file; do
      last_modified=$(git log -1 --format="%ai" -- "$test_file" 2>/dev/null)
      if [ -n "$last_modified" ]; then
        echo "$last_modified $test_file"
      fi
    done | sort > test_last_modified.txt
}
```

## Automated Stabilization Techniques

### 1. Timeout and Retry Fixes

**Intelligent Timeout Adjustment:**

```typescript
// Generated timeout fixes for different frameworks

// Deno/JavaScript timeout improvements
export function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  baseDelay = 1000,
): Promise<T> {
  return new Promise(async (resolve, reject) => {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        const result = await fn();
        resolve(result);
        return;
      } catch (error) {
        if (attempt === maxRetries) {
          reject(error);
          return;
        }

        // Exponential backoff with jitter
        const delay = baseDelay * Math.pow(2, attempt - 1) + Math.random() * 1000;
        await new Promise((r) => setTimeout(r, delay));
      }
    }
  });
}

// Enhanced test wrapper with stability improvements
export function stabilizeTest(testFn: () => Promise<void>, options?: {
  retries?: number;
  timeout?: number;
  skipOnCI?: boolean;
}) {
  return async () => {
    const { retries = 3, timeout = 30000, skipOnCI = false } = options || {};

    if (skipOnCI && Deno.env.get("CI")) {
      console.log("⏭️  Skipping flaky test in CI environment");
      return;
    }

    const testWithTimeout = () =>
      Promise.race([
        testFn(),
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error(`Test timeout after ${timeout}ms`)), timeout)
        ),
      ]);

    return withRetry(testWithTimeout, retries);
  };
}
```

**Framework-Specific Stabilization:**

**Rust Test Stabilization:**

```rust
// Generated Rust test stability improvements
use std::time::{Duration, Instant};
use tokio::time::sleep;

pub async fn with_retry<F, Fut, T, E>(
    mut f: F,
    max_retries: usize,
    base_delay: Duration,
) -> Result<T, E>
where
    F: FnMut() -> Fut,
    Fut: std::future::Future<Output = Result<T, E>>,
    E: std::fmt::Debug,
{
    let mut last_error = None;
    
    for attempt in 1..=max_retries {
        match f().await {
            Ok(result) => return Ok(result),
            Err(e) => {
                last_error = Some(e);
                if attempt < max_retries {
                    let delay = base_delay * 2_u32.pow(attempt as u32 - 1);
                    sleep(delay).await;
                }
            }
        }
    }
    
    Err(last_error.unwrap())
}

// Macro for stable test execution
#[macro_export]
macro_rules! stable_test {
    ($name:ident, $body:expr) => {
        #[tokio::test]
        async fn $name() {
            const MAX_RETRIES: usize = 3;
            const BASE_DELAY: Duration = Duration::from_millis(100);
            
            with_retry(
                || async { $body.await },
                MAX_RETRIES,
                BASE_DELAY,
            )
            .await
            .expect("Test failed after retries");
        }
    };
}
```

### 2. Race Condition Fixes

**Synchronization Improvements:**

```typescript
// Generated synchronization utilities
export class TestSynchronizer {
  private static waitConditions: Map<string, () => Promise<boolean>> = new Map();

  static async waitFor(
    condition: () => Promise<boolean> | boolean,
    options: {
      timeout?: number;
      interval?: number;
      message?: string;
    } = {},
  ): Promise<void> {
    const { timeout = 10000, interval = 100, message = "Condition not met" } = options;
    const start = Date.now();

    while (Date.now() - start < timeout) {
      try {
        const result = await condition();
        if (result) return;
      } catch (error) {
        // Continue waiting on condition errors
      }

      await new Promise((resolve) => setTimeout(resolve, interval));
    }

    throw new Error(`${message} (timeout: ${timeout}ms)`);
  }

  static async waitForElement(selector: string, timeout = 10000): Promise<Element> {
    return this.waitFor(
      () => {
        const element = document.querySelector(selector);
        return Promise.resolve(!!element);
      },
      { timeout, message: `Element ${selector} not found` },
    ).then(() => document.querySelector(selector)!);
  }

  static async waitForApi(
    url: string,
    expectedStatus = 200,
    timeout = 10000,
  ): Promise<Response> {
    let lastResponse: Response | null = null;

    await this.waitFor(
      async () => {
        try {
          const response = await fetch(url);
          lastResponse = response;
          return response.status === expectedStatus;
        } catch {
          return false;
        }
      },
      { timeout, message: `API ${url} not ready` },
    );

    return lastResponse!;
  }
}
```

### 3. Test Isolation Improvements

**Database and State Reset:**

```typescript
// Generated test isolation utilities
export class TestIsolation {
  private static cleanupTasks: (() => Promise<void>)[] = [];

  static addCleanup(task: () => Promise<void>): void {
    this.cleanupTasks.push(task);
  }

  static async cleanup(): Promise<void> {
    for (const task of this.cleanupTasks) {
      try {
        await task();
      } catch (error) {
        console.warn("Cleanup task failed:", error);
      }
    }
    this.cleanupTasks.length = 0;
  }

  // Database isolation
  static async withTransaction<T>(
    db: Database,
    testFn: (tx: Transaction) => Promise<T>,
  ): Promise<T> {
    const tx = await db.transaction();
    try {
      const result = await testFn(tx);
      await tx.rollback(); // Always rollback in tests
      return result;
    } catch (error) {
      await tx.rollback();
      throw error;
    }
  }

  // HTTP service isolation
  static createIsolatedHttpClient(baseURL: string): HttpClient {
    const client = new HttpClient(baseURL);

    // Track requests for cleanup
    this.addCleanup(async () => {
      await client.cleanup?.();
    });

    return client;
  }
}
```

## Continuous Monitoring Setup

### 1. Test Metrics Collection

**CI/CD Integration for Flake Detection:**

```yaml
# Generated GitHub Actions workflow for flake monitoring
name: Flaky Test Monitor

on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]

jobs:
  analyze-flakes:
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Download test results
        uses: actions/github-script@v6
        with:
          script: |
            // Download artifacts from failed workflow
            const artifacts = await github.rest.actions.listWorkflowRunArtifacts({
              owner: context.repo.owner,
              repo: context.repo.repo,
              run_id: ${{ github.event.workflow_run.id }}
            });

            for (const artifact of artifacts.data.artifacts) {
              if (artifact.name.includes('test-results')) {
                // Process test results for flake analysis
              }
            }

      - name: Analyze flaky patterns
        run: |
          deno run --allow-all scripts/analyze-flakes.ts \
            --input test-results.json \
            --output flake-report.json \
            --threshold 3

      - name: Create issue for new flaky tests
        if: steps.analyze.outputs.new-flakes == 'true'
        uses: actions/github-script@v6
        with:
          script: |
            await github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'New Flaky Tests Detected',
              body: '...' // Include flake analysis
            });
```

### 2. Flake Alerting System

**Slack/Discord Integration:**

```typescript
// Generated flake notification system
interface FlakeAlert {
  testName: string;
  flakeRate: number;
  recentFailures: number;
  patterns: string[];
  suggestedFixes: string[];
}

export class FlakeNotifier {
  async sendAlert(alert: FlakeAlert): Promise<void> {
    const webhook = Deno.env.get("SLACK_WEBHOOK_URL");
    if (!webhook) return;

    const message = {
      text: `🚨 Flaky Test Alert: ${alert.testName}`,
      blocks: [
        {
          type: "section",
          text: {
            type: "mrkdwn",
            text: `*Flaky Test Detected*\n\n` +
              `• Test: \`${alert.testName}\`\n` +
              `• Flake Rate: ${(alert.flakeRate * 100).toFixed(1)}%\n` +
              `• Recent Failures: ${alert.recentFailures}`,
          },
        },
        {
          type: "section",
          text: {
            type: "mrkdwn",
            text: `*Detected Patterns:*\n${alert.patterns.map((p) => `• ${p}`).join("\n")}`,
          },
        },
        {
          type: "section",
          text: {
            type: "mrkdwn",
            text: `*Suggested Fixes:*\n${alert.suggestedFixes.map((f) => `• ${f}`).join("\n")}`,
          },
        },
      ],
    };

    await fetch(webhook, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(message),
    });
  }
}
```

## Report Generation

### Comprehensive Flake Analysis Report

**HTML Report Generation:**

```typescript
// Generated flake report generator
export class FlakeReporter {
  generateHTMLReport(flakeScores: FlakeScore[]): string {
    const criticalFlakes = flakeScores.filter((f) => f.severity === "critical");
    const highFlakes = flakeScores.filter((f) => f.severity === "high");

    return `
<!DOCTYPE html>
<html>
<head>
  <title>Flaky Test Analysis Report</title>
  <style>
    .critical { background-color: #ffe6e6; }
    .high { background-color: #fff2e6; }
    .medium { background-color: #fff9e6; }
    .chart { width: 100%; height: 300px; }
  </style>
</head>
<body>
  <h1>Flaky Test Analysis Report</h1>
  
  <div class="summary">
    <h2>Summary</h2>
    <ul>
      <li>Total Tests Analyzed: ${flakeScores.length}</li>
      <li>Critical Flaky Tests: ${criticalFlakes.length}</li>
      <li>High Priority Flaky Tests: ${highFlakes.length}</li>
    </ul>
  </div>
  
  <div class="details">
    <h2>Flaky Test Details</h2>
    <table>
      <thead>
        <tr>
          <th>Test Name</th>
          <th>Flake Rate</th>
          <th>Failures</th>
          <th>Patterns</th>
          <th>Severity</th>
        </tr>
      </thead>
      <tbody>
        ${
      flakeScores.map((score) => `
          <tr class="${score.severity}">
            <td>${score.testName}</td>
            <td>${(score.flakeRate * 100).toFixed(1)}%</td>
            <td>${score.failures}</td>
            <td>${score.patterns.join(", ")}</td>
            <td>${score.severity}</td>
          </tr>
        `).join("")
    }
      </tbody>
    </table>
  </div>
</body>
</html>`;
  }
}
```

## Integration with Other Commands

- Use with `/test-gen` to create stable tests from the start
- Combine with `/coverage` to ensure flake fixes don't reduce coverage
- Integrate with `/ci-gen` for automated flake detection in pipelines
- Use with `/monitor` to set up ongoing flake tracking

## Output

The command provides:

1. **Flake Analysis Report**: Detailed analysis of test stability patterns
2. **Automated Fixes**: Generated code improvements for common flake patterns
3. **Monitoring Setup**: Continuous flake detection and alerting
4. **Stability Utilities**: Reusable test stabilization functions
5. **CI Integration**: Automated flake tracking in development workflows
