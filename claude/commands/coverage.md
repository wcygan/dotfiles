# /coverage

Comprehensive code coverage analysis, reporting, and improvement automation with intelligent gap identification and test generation suggestions.

## Usage

```
/coverage [analyze|report|improve|enforce] [--threshold=80] [--format=html,json,lcov]
```

## Parameters

- `analyze` - Analyze current coverage and identify gaps (default)
- `report` - Generate comprehensive coverage reports
- `improve` - Suggest specific improvements to increase coverage
- `enforce` - Set up coverage enforcement in CI/CD
- `--threshold` - Coverage percentage threshold (default: 80%)
- `--format` - Output formats: html, json, lcov, cobertura, text

## Context Intelligence

### Framework and Tool Detection

**Language-Specific Coverage Tools:**

```bash
# Detect project type and configure appropriate coverage tools
detect_coverage_tools() {
  if [ -f "deno.json" ]; then
    LANGUAGE="deno"
    COVERAGE_TOOL="built-in"
    COVERAGE_CMD="deno test --coverage=coverage"
    REPORT_CMD="deno coverage coverage --html"
  elif [ -f "Cargo.toml" ]; then
    LANGUAGE="rust"
    COVERAGE_TOOL="tarpaulin"
    COVERAGE_CMD="cargo tarpaulin --out Html --out Xml"
    REPORT_CMD="open tarpaulin-report.html"
  elif [ -f "go.mod" ]; then
    LANGUAGE="go"
    COVERAGE_TOOL="built-in"
    COVERAGE_CMD="go test -coverprofile=coverage.out ./..."
    REPORT_CMD="go tool cover -html=coverage.out -o coverage.html"
  elif [ -f "package.json" ]; then
    # Detect Node.js testing framework
    if jq -e '.devDependencies.jest' package.json > /dev/null; then
      LANGUAGE="node"
      COVERAGE_TOOL="jest"
      COVERAGE_CMD="jest --coverage"
    elif jq -e '.devDependencies.vitest' package.json > /dev/null; then
      LANGUAGE="node"
      COVERAGE_TOOL="vitest"
      COVERAGE_CMD="vitest --coverage"
    elif jq -e '.devDependencies.c8' package.json > /dev/null; then
      LANGUAGE="node"
      COVERAGE_TOOL="c8"
      COVERAGE_CMD="c8 npm test"
    fi
  elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
    LANGUAGE="python"
    COVERAGE_TOOL="coverage.py"
    COVERAGE_CMD="coverage run -m pytest && coverage report"
    REPORT_CMD="coverage html"
  fi
  
  echo "Detected: $LANGUAGE with $COVERAGE_TOOL"
}
```

### Existing Coverage Configuration

**Check for Existing Coverage Setup:**

```bash
# Analyze existing coverage configuration
analyze_existing_coverage() {
  echo "🔍 Analyzing existing coverage setup..."
  
  case $LANGUAGE in
    "deno")
      if jq -e '.tasks.coverage' deno.json > /dev/null; then
        echo "✅ Deno coverage task found"
        jq '.tasks.coverage' deno.json
      else
        echo "❌ No coverage task in deno.json"
      fi
      ;;
    "rust")
      if grep -q "tarpaulin" Cargo.toml; then
        echo "✅ Tarpaulin configured in Cargo.toml"
      else
        echo "❌ No tarpaulin configuration found"
      fi
      ;;
    "node")
      if jq -e '.jest.collectCoverage' package.json > /dev/null; then
        echo "✅ Jest coverage configured"
        jq '.jest.collectCoverage' package.json
      elif jq -e '.scripts | to_entries[] | select(.value | contains("coverage"))' package.json > /dev/null; then
        echo "✅ Coverage script found"
        jq '.scripts | to_entries[] | select(.value | contains("coverage"))' package.json
      else
        echo "❌ No coverage configuration found"
      fi
      ;;
  esac
}
```

## Coverage Analysis

### 1. Comprehensive Coverage Metrics

**Multi-Dimensional Coverage Analysis:**

```typescript
// Generated coverage analyzer
interface CoverageMetrics {
  lines: CoverageData;
  branches: CoverageData;
  functions: CoverageData;
  statements: CoverageData;
}

interface CoverageData {
  total: number;
  covered: number;
  percentage: number;
  uncovered: Array<{
    file: string;
    lines: number[];
    complexity?: number;
    importance?: "critical" | "high" | "medium" | "low";
  }>;
}

interface FileAnalysis {
  file: string;
  coverage: CoverageMetrics;
  complexity: number;
  testComplexityRatio: number;
  riskScore: number;
  suggestions: CoverageSuggestion[];
}

interface CoverageSuggestion {
  type: "add_test" | "refactor" | "split_function" | "mock_dependency";
  description: string;
  effort: "low" | "medium" | "high";
  impact: "low" | "medium" | "high";
  codeExample?: string;
}

export class CoverageAnalyzer {
  async analyzeCoverage(coverageFile: string): Promise<FileAnalysis[]> {
    const coverageData = await this.parseCoverageFile(coverageFile);
    const sourceFiles = await this.getSourceFiles();

    return Promise.all(
      sourceFiles.map(async (file) => {
        const fileCoverage = coverageData.files[file];
        const complexity = await this.calculateComplexity(file);
        const testFiles = await this.findTestFiles(file);

        return {
          file,
          coverage: fileCoverage,
          complexity,
          testComplexityRatio: this.calculateTestComplexityRatio(file, testFiles),
          riskScore: this.calculateRiskScore(fileCoverage, complexity),
          suggestions: await this.generateSuggestions(file, fileCoverage, complexity),
        };
      }),
    );
  }

  private calculateRiskScore(coverage: CoverageMetrics, complexity: number): number {
    const coverageWeight = (100 - coverage.lines.percentage) * 0.4;
    const branchWeight = (100 - coverage.branches.percentage) * 0.3;
    const complexityWeight = Math.min(complexity / 10, 10) * 0.3;

    return Math.round(coverageWeight + branchWeight + complexityWeight);
  }

  private async generateSuggestions(
    file: string,
    coverage: CoverageMetrics,
    complexity: number,
  ): Promise<CoverageSuggestion[]> {
    const suggestions: CoverageSuggestion[] = [];

    // Low coverage suggestions
    if (coverage.lines.percentage < 70) {
      suggestions.push({
        type: "add_test",
        description: `Add tests for uncovered lines: ${
          coverage.lines.uncovered.map((u) => u.lines).flat().slice(0, 5).join(", ")
        }`,
        effort: coverage.lines.uncovered.length > 20 ? "high" : "medium",
        impact: "high",
        codeExample: await this.generateTestExample(file, coverage.lines.uncovered[0]),
      });
    }

    // High complexity suggestions
    if (complexity > 15) {
      suggestions.push({
        type: "refactor",
        description: "Consider breaking down complex functions for better testability",
        effort: "high",
        impact: "medium",
      });
    }

    // Branch coverage suggestions
    if (coverage.branches.percentage < coverage.lines.percentage - 20) {
      suggestions.push({
        type: "add_test",
        description: "Add tests for uncovered conditional branches",
        effort: "medium",
        impact: "high",
      });
    }

    return suggestions;
  }
}
```

### 2. Intelligent Gap Identification

**Critical Path Analysis:**

```bash
# Identify critical uncovered code paths
analyze_critical_gaps() {
  echo "🎯 Identifying critical coverage gaps..."
  
  # Find uncovered public APIs
  case $LANGUAGE in
    "typescript"|"javascript")
      rg "^export\s+(function|class|const)" --type ts --type js | \
        while read -r line; do
          file=$(echo "$line" | cut -d: -f1)
          func=$(echo "$line" | cut -d: -f2- | rg -o "(function|class|const)\s+\w+" | cut -d' ' -f2)
          
          # Check if this export is covered
          if ! rg -q "$func" "$(dirname "$file")/test/" 2>/dev/null; then
            echo "❌ Uncovered public API: $func in $file"
          fi
        done
      ;;
    "rust")
      rg "^pub\s+(fn|struct|enum)" --type rust | \
        while read -r line; do
          file=$(echo "$line" | cut -d: -f1)
          item=$(echo "$line" | cut -d: -f2- | rg -o "(fn|struct|enum)\s+\w+" | cut -d' ' -f2)
          
          # Check if this public item has tests
          if ! rg -q "$item" "${file%/*}/test/" 2>/dev/null && ! rg -q "#\[test\]" "$file"; then
            echo "❌ Uncovered public item: $item in $file"
          fi
        done
      ;;
    "go")
      rg "^func\s+[A-Z]" --type go | \
        while read -r line; do
          file=$(echo "$line" | cut -d: -f1)
          func=$(echo "$line" | cut -d: -f2- | rg -o "func\s+\w+" | cut -d' ' -f2)
          
          # Check if this public function has tests
          test_file="${file%.*}_test.go"
          if [ -f "$test_file" ] && ! rg -q "Test$func\|$func" "$test_file"; then
            echo "❌ Uncovered public function: $func in $file"
          fi
        done
      ;;
  esac
}

# Analyze error handling coverage
analyze_error_coverage() {
  echo "🚨 Analyzing error handling coverage..."
  
  # Find error handling patterns that might be uncovered
  rg "(throw|panic|error|Error|except|raise)" --type "$LANGUAGE" | \
    head -20 | \
    while read -r line; do
      file=$(echo "$line" | cut -d: -f1)
      line_num=$(echo "$line" | cut -d: -f2)
      echo "Check error handling coverage: $file:$line_num"
    done
}
```

### 3. Coverage Quality Assessment

**Test Quality vs Coverage Analysis:**

```typescript
// Generated test quality analyzer
interface TestQualityMetrics {
  testFilesCoverage: number;
  assertionDensity: number;
  mockUsage: number;
  edgeCaseCoverage: number;
  performanceTestCoverage: number;
}

export class TestQualityAnalyzer {
  async analyzeTestQuality(testFiles: string[]): Promise<TestQualityMetrics> {
    const analyses = await Promise.all(
      testFiles.map((file) => this.analyzeTestFile(file)),
    );

    return {
      testFilesCoverage: this.calculateTestFilesCoverage(analyses),
      assertionDensity: this.calculateAssertionDensity(analyses),
      mockUsage: this.calculateMockUsage(analyses),
      edgeCaseCoverage: this.calculateEdgeCaseCoverage(analyses),
      performanceTestCoverage: this.calculatePerformanceTestCoverage(analyses),
    };
  }

  private async analyzeTestFile(file: string): Promise<any> {
    const content = await Deno.readTextFile(file);

    // Count assertions
    const assertions = (content.match(/assert|expect|should/g) || []).length;

    // Count mocks/stubs
    const mocks = (content.match(/mock|stub|spy|fake/gi) || []).length;

    // Count edge case patterns
    const edgeCases =
      (content.match(/edge|boundary|null|undefined|empty|zero|negative/gi) || []).length;

    // Count performance tests
    const performanceTests = (content.match(/benchmark|performance|timeout|slow/gi) || []).length;

    const testCases = (content.match(/test\(|it\(|Deno\.test/g) || []).length;

    return {
      file,
      assertions,
      mocks,
      edgeCases,
      performanceTests,
      testCases,
      assertionDensity: testCases > 0 ? assertions / testCases : 0,
    };
  }
}
```

## Coverage Reporting

### 1. Multi-Format Report Generation

**Language-Specific Report Generation:**

**Deno Coverage Setup:**

```typescript
// Generated Deno coverage configuration
export async function generateCoverageReport(format: string[] = ["html", "json"]) {
  console.log("🔄 Generating Deno coverage report...");

  // Run tests with coverage
  const testResult = await new Deno.Command("deno", {
    args: ["test", "--allow-all", "--coverage=coverage"],
    stdout: "piped",
    stderr: "piped",
  }).output();

  if (!testResult.success) {
    console.error("❌ Tests failed");
    return;
  }

  // Generate reports in requested formats
  for (const fmt of format) {
    switch (fmt) {
      case "html":
        await new Deno.Command("deno", {
          args: ["coverage", "coverage", "--html"],
        }).output();
        console.log("📊 HTML report: coverage/html/index.html");
        break;

      case "json":
        await new Deno.Command("deno", {
          args: ["coverage", "coverage", "--output=coverage.json"],
        }).output();
        console.log("📄 JSON report: coverage.json");
        break;

      case "lcov":
        await new Deno.Command("deno", {
          args: ["coverage", "coverage", "--lcov", "--output=coverage.lcov"],
        }).output();
        console.log("📄 LCOV report: coverage.lcov");
        break;
    }
  }
}
```

**Rust Coverage Setup:**

```bash
# Generated Rust coverage configuration
setup_rust_coverage() {
  echo "🦀 Setting up Rust coverage with tarpaulin..."
  
  # Add tarpaulin to dev dependencies if not present
  if ! grep -q "cargo-tarpaulin" Cargo.toml; then
    echo "Adding tarpaulin to Cargo.toml..."
    cat >> Cargo.toml << 'EOF'

# Coverage analysis
[package.metadata.tarpaulin]
exclude = ["tests/*"]
exclude-files = ["src/bin/*"]
timeout = 120
EOF
  fi
  
  # Install tarpaulin if not available
  if ! command -v cargo-tarpaulin &> /dev/null; then
    cargo install cargo-tarpaulin
  fi
  
  # Generate coverage report
  cargo tarpaulin \
    --out Html \
    --out Xml \
    --out Json \
    --output-dir coverage \
    --exclude-files src/main.rs \
    --timeout 120
    
  echo "📊 Coverage reports generated in coverage/"
}
```

**Go Coverage Enhancement:**

```bash
# Generated Go coverage tooling
setup_go_coverage() {
  echo "🐹 Setting up enhanced Go coverage..."
  
  # Run tests with coverage
  go test -coverprofile=coverage.out -covermode=atomic ./...
  
  # Generate HTML report
  go tool cover -html=coverage.out -o coverage.html
  
  # Generate function-level coverage
  go tool cover -func=coverage.out > coverage-functions.txt
  
  # Calculate coverage by package
  go test -coverprofile=coverage.out ./... | tee coverage-summary.txt
  
  # Generate JSON report for CI integration
  go run << 'EOF'
package main

import (
    "encoding/json"
    "fmt"
    "os/exec"
    "strings"
)

func main() {
    cmd := exec.Command("go", "tool", "cover", "-func=coverage.out")
    output, _ := cmd.Output()
    
    lines := strings.Split(string(output), "\n")
    totalLine := lines[len(lines)-2]
    
    parts := strings.Fields(totalLine)
    coverage := strings.TrimSuffix(parts[len(parts)-1], "%")
    
    result := map[string]interface{}{
        "coverage": coverage,
        "timestamp": "$(date -Iseconds)",
        "format": "go-cover"
    }
    
    json, _ := json.MarshalIndent(result, "", "  ")
    fmt.Println(string(json))
}
EOF
}
```

### 2. Advanced Reporting Features

**Interactive Coverage Dashboard:**

```typescript
// Generated interactive coverage dashboard
export class CoverageDashboard {
  generateInteractiveReport(analyses: FileAnalysis[]): string {
    const totalCoverage = this.calculateOverallCoverage(analyses);
    const riskFiles = analyses.filter((a) => a.riskScore > 7).sort((a, b) =>
      b.riskScore - a.riskScore
    );
    const improvementOpportunities = this.identifyImprovementOpportunities(analyses);

    return `
<!DOCTYPE html>
<html>
<head>
    <title>Code Coverage Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .dashboard { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .card { background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric { font-size: 2em; font-weight: bold; color: #2563eb; }
        .risk-high { color: #dc2626; }
        .risk-medium { color: #ea580c; }
        .risk-low { color: #16a34a; }
        .progress-bar { width: 100%; height: 20px; background: #e5e7eb; border-radius: 10px; overflow: hidden; }
        .progress-fill { height: 100%; background: #10b981; transition: width 0.3s; }
    </style>
</head>
<body>
    <h1>Code Coverage Dashboard</h1>
    
    <div class="dashboard">
        <div class="card">
            <h2>Overall Coverage</h2>
            <div class="metric">${totalCoverage.lines.toFixed(1)}%</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${totalCoverage.lines}%"></div>
            </div>
            <p>Lines: ${totalCoverage.lines.toFixed(1)}% | Branches: ${
      totalCoverage.branches.toFixed(1)
    }% | Functions: ${totalCoverage.functions.toFixed(1)}%</p>
        </div>
        
        <div class="card">
            <h2>Risk Assessment</h2>
            <canvas id="riskChart" width="400" height="200"></canvas>
        </div>
        
        <div class="card">
            <h2>High Risk Files</h2>
            <ul>
                ${
      riskFiles.slice(0, 10).map((file) => `
                    <li class="risk-${
        file.riskScore > 8 ? "high" : file.riskScore > 5 ? "medium" : "low"
      }">
                        ${file.file} (Risk: ${file.riskScore}, Coverage: ${
        file.coverage.lines.percentage.toFixed(1)
      }%)
                    </li>
                `).join("")
    }
            </ul>
        </div>
        
        <div class="card">
            <h2>Improvement Opportunities</h2>
            <ul>
                ${
      improvementOpportunities.slice(0, 5).map((opp) => `
                    <li>${opp.description} (Impact: ${opp.impact}, Effort: ${opp.effort})</li>
                `).join("")
    }
            </ul>
        </div>
    </div>
    
    <script>
        // Generate risk distribution chart
        const ctx = document.getElementById('riskChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Low Risk', 'Medium Risk', 'High Risk'],
                datasets: [{
                    data: [
                        ${analyses.filter((a) => a.riskScore <= 3).length},
                        ${analyses.filter((a) => a.riskScore > 3 && a.riskScore <= 7).length},
                        ${analyses.filter((a) => a.riskScore > 7).length}
                    ],
                    backgroundColor: ['#16a34a', '#ea580c', '#dc2626']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    </script>
</body>
</html>`;
  }
}
```

## Coverage Improvement Automation

### 1. Intelligent Test Generation

**Coverage-Driven Test Generation:**

```typescript
// Generated coverage improvement automation
export class CoverageImprover {
  async generateTestsForUncoveredCode(file: string, uncoveredLines: number[]): Promise<string[]> {
    const sourceCode = await Deno.readTextFile(file);
    const ast = this.parseAST(sourceCode);
    const suggestions: string[] = [];

    for (const lineNum of uncoveredLines) {
      const node = this.findNodeAtLine(ast, lineNum);

      if (node) {
        switch (node.type) {
          case "FunctionDeclaration":
            suggestions.push(this.generateFunctionTest(node));
            break;
          case "IfStatement":
            suggestions.push(this.generateBranchTest(node));
            break;
          case "TryStatement":
            suggestions.push(this.generateErrorTest(node));
            break;
          case "ReturnStatement":
            suggestions.push(this.generateReturnValueTest(node));
            break;
        }
      }
    }

    return suggestions;
  }

  private generateFunctionTest(node: any): string {
    const functionName = node.id.name;
    const params = node.params.map((p: any) => p.name);

    return `
Deno.test("${functionName} - basic functionality", async () => {
  // TODO: Add appropriate test inputs
  const result = await ${functionName}(${params.map((p) => `/* ${p} */`).join(", ")});
  
  // TODO: Add assertions
  assertEquals(typeof result, "expected_type");
});

Deno.test("${functionName} - edge cases", async () => {
  // TODO: Test edge cases like null, undefined, empty values
  ${
      params.length > 0
        ? `
  await assertRejects(
    () => ${functionName}(${params.map(() => "null").join(", ")}),
    Error
  );`
        : ""
    }
});`;
  }

  private generateBranchTest(node: any): string {
    return `
// TODO: Add tests for both branches of the conditional
Deno.test("condition true branch", () => {
  // Test when condition is true
});

Deno.test("condition false branch", () => {
  // Test when condition is false
});`;
  }
}
```

### 2. Coverage Enforcement

**CI/CD Coverage Gates:**

```yaml
# Generated coverage enforcement workflow
name: Coverage Enforcement

on: [push, pull_request]

jobs:
  coverage:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup environment
        run: |
          # Setup based on detected language
          case "$(detect_language.sh)" in
            "deno")
              curl -fsSL https://deno.land/install.sh | sh
              echo "$HOME/.deno/bin" >> $GITHUB_PATH
              ;;
            "rust")
              rustup update stable
              cargo install cargo-tarpaulin
              ;;
            "go")
              # Go is pre-installed
              ;;
          esac

      - name: Run tests with coverage
        run: |
          case "$(detect_language.sh)" in
            "deno")
              deno task test
              deno coverage coverage --json > coverage.json
              ;;
            "rust")
              cargo tarpaulin --out Json --output-dir coverage
              ;;
            "go")
              go test -coverprofile=coverage.out ./...
              go tool cover -func=coverage.out -o coverage.txt
              ;;
          esac

      - name: Check coverage threshold
        run: |
          THRESHOLD=${COVERAGE_THRESHOLD:-80}
          CURRENT=$(extract_coverage_percentage.sh)

          if (( $(echo "$CURRENT < $THRESHOLD" | bc -l) )); then
            echo "❌ Coverage $CURRENT% is below threshold $THRESHOLD%"
            exit 1
          else
            echo "✅ Coverage $CURRENT% meets threshold $THRESHOLD%"
          fi

      - name: Comment coverage on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const coverage = require('./coverage.json');
            const comment = `
            ## 📊 Coverage Report

            | Metric | Coverage | Change |
            |--------|----------|---------|
            | Lines | ${coverage.lines}% | +2.3% |
            | Branches | ${coverage.branches}% | +1.1% |
            | Functions | ${coverage.functions}% | +0.8% |

            ${coverage.lines < 80 ? '⚠️ Coverage below 80% threshold' : '✅ Coverage meets requirements'}
            `;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

### 3. Progressive Coverage Improvement

**Coverage Ratcheting System:**

```typescript
// Generated coverage ratcheting system
interface CoverageHistory {
  timestamp: string;
  commit: string;
  coverage: CoverageMetrics;
  threshold: number;
}

export class CoverageRatchet {
  private historyFile = "coverage-history.json";

  async updateCoverageHistory(current: CoverageMetrics): Promise<void> {
    const history = await this.loadHistory();
    const commit = await this.getCurrentCommit();

    const entry: CoverageHistory = {
      timestamp: new Date().toISOString(),
      commit,
      coverage: current,
      threshold: this.calculateNewThreshold(history, current),
    };

    history.push(entry);

    // Keep only last 100 entries
    if (history.length > 100) {
      history.splice(0, history.length - 100);
    }

    await Deno.writeTextFile(this.historyFile, JSON.stringify(history, null, 2));

    console.log(
      `📈 Coverage: ${current.lines.percentage.toFixed(1)}% (threshold: ${entry.threshold}%)`,
    );
  }

  private calculateNewThreshold(history: CoverageHistory[], current: CoverageMetrics): number {
    if (history.length === 0) return 70; // Starting threshold

    const lastEntry = history[history.length - 1];
    const trend = this.calculateTrend(history.slice(-10));

    // Increase threshold if coverage is consistently improving
    if (trend > 0 && current.lines.percentage > lastEntry.threshold + 2) {
      return Math.min(current.lines.percentage - 1, 95);
    }

    // Maintain current threshold if stable
    return lastEntry.threshold;
  }

  async checkCoverageRegression(): Promise<boolean> {
    const history = await this.loadHistory();
    if (history.length === 0) return true;

    const lastEntry = history[history.length - 1];
    const currentCoverage = await this.getCurrentCoverage();

    if (currentCoverage.lines.percentage < lastEntry.threshold) {
      console.error(
        `❌ Coverage regression: ${
          currentCoverage.lines.percentage.toFixed(1)
        }% < ${lastEntry.threshold}%`,
      );

      // Suggest specific improvements
      await this.suggestImprovements(currentCoverage, lastEntry.coverage);

      return false;
    }

    return true;
  }
}
```

## Integration and Output

### Integration with Other Commands

- Use with `/test-gen` to generate tests for uncovered code
- Combine with `/flaky-fix` to ensure coverage improvements don't introduce flaky tests
- Integrate with `/ci-gen` for automated coverage enforcement
- Use with `/benchmark` to track coverage impact on performance

### Generated Outputs

1. **Coverage Reports**: Multi-format reports (HTML, JSON, LCOV, Cobertura)
2. **Gap Analysis**: Detailed uncovered code analysis with priorities
3. **Test Suggestions**: Specific test cases to improve coverage
4. **CI Integration**: Automated coverage enforcement workflows
5. **Interactive Dashboard**: Real-time coverage monitoring and trends
6. **Ratcheting System**: Progressive coverage improvement tracking
