---
allowed-tools: Task, Read, Write, Edit, MultiEdit, Bash(fd:*), Bash(rg:*), Bash(bat:*), Bash(eza:*), Bash(jq:*), Bash(gdate:*), Bash(deno:*), Bash(cargo:*), Bash(go:*), Bash(mvn:*), Bash(npm:*), Bash(jest:*), Bash(vitest:*), Bash(coverage:*), Bash(tarpaulin:*)
description: Comprehensive code coverage orchestrator with intelligent gap analysis, multi-format reporting, and automated improvement recommendations
---

## Context

- Session ID: !`gdate +%s%N 2>/dev/null || date +%s%N 2>/dev/null || echo "$(date +%s)$(jot -r 1 100000 999999 2>/dev/null || shuf -i 100000-999999 -n 1 2>/dev/null || echo $RANDOM$RANDOM)"`
- Target project: $ARGUMENTS
- Current directory: !`pwd`
- Project structure: !`eza -la --tree --level=2 2>/dev/null | head -10 || fd . -t d -d 2 | head -8`
- Build files detected: !`fd "(package\.json|Cargo\.toml|go\.mod|deno\.json|pom\.xml|pyproject\.toml|requirements\.txt)" . -d 3 | head -8 || echo "No build files detected"`
- Existing coverage files: !`fd "(coverage|tarpaulin-report|coverage\.out|\.coverage)" . -d 3 | head -5 || echo "No coverage reports found"`
- Language detection: !`echo "Languages: $(fd "\.(js|ts|jsx|tsx)" . | head -1 >/dev/null && echo "JS/TS") $(fd "\.rs$" . | head -1 >/dev/null && echo "Rust") $(fd "\.go$" . | head -1 >/dev/null && echo "Go") $(fd "\.py$" . | head -1 >/dev/null && echo "Python") $(fd "\.java$" . | head -1 >/dev/null && echo "Java")"`
- Coverage tools status: !`echo "Tools: $(which jest >/dev/null && echo "jest✓") $(which vitest >/dev/null && echo "vitest✓") $(which cargo-tarpaulin >/dev/null && echo "tarpaulin✓") $(which go >/dev/null && echo "go✓") $(which coverage >/dev/null && echo "coverage.py✓")"`

## Your Task

- CREATE session state file: `/tmp/coverage-session-$SESSION_ID.json`
- ANALYZE project structure and technology stack from Context section
- DETECT coverage tools and existing configurations
- DETERMINE analysis complexity based on project size and language diversity

```bash
# Initialize coverage analysis session state
echo '{
  "sessionId": "'$SESSION_ID'",
  "targetProject": "'$ARGUMENTS'",
  "detectedLanguages": [],
  "coverageStrategy": "auto-detect",
  "analysisComplexity": "standard",
  "toolConfiguration": {}
}' > /tmp/coverage-session-$SESSION_ID.json
```

STEP 2: Intelligent technology stack detection and coverage tool configuration

TRY:

**Multi-Language Coverage Tool Detection:**

```bash
# Language-specific coverage configuration
configure_coverage_tools() {
  local project_languages=()
  local coverage_config={}
  
  # Deno/TypeScript projects
  if fd "deno\.json" . | head -1 >/dev/null; then
    echo "🦕 Deno project detected"
    project_languages+=("deno")
    DENO_CMD="deno test --allow-all --coverage=coverage"
    DENO_REPORT="deno coverage coverage --html"
  fi
  
  # Rust projects  
  if fd "Cargo\.toml" . | head -1 >/dev/null; then
    echo "🦀 Rust project detected"
    project_languages+=("rust")
    RUST_CMD="cargo tarpaulin --out Html --out Json --out Xml --output-dir coverage"
    RUST_INSTALL="cargo install cargo-tarpaulin"
  fi
  
  # Go projects
  if fd "go\.mod" . | head -1 >/dev/null; then
    echo "🐹 Go project detected"
    project_languages+=("go")
    GO_CMD="go test -coverprofile=coverage.out -covermode=atomic ./..."
    GO_REPORT="go tool cover -html=coverage.out -o coverage.html"
  fi
  
  # Node.js/JavaScript projects
  if fd "package\.json" . | head -1 >/dev/null; then
    echo "⚡ Node.js project detected"
    project_languages+=("node")
    
    # Detect testing framework
    if jq -e '.devDependencies.jest' package.json >/dev/null 2>&1; then
      NODE_TOOL="jest"
      NODE_CMD="jest --coverage --collectCoverageFrom='src/**/*.{js,ts,jsx,tsx}'"
    elif jq -e '.devDependencies.vitest' package.json >/dev/null 2>&1; then
      NODE_TOOL="vitest"  
      NODE_CMD="vitest --coverage"
    elif jq -e '.devDependencies.c8' package.json >/dev/null 2>&1; then
      NODE_TOOL="c8"
      NODE_CMD="c8 npm test"
    fi
  fi
  
  # Python projects
  if fd "(pyproject\.toml|requirements\.txt)" . | head -1 >/dev/null; then
    echo "🐍 Python project detected"
    project_languages+=("python")
    PYTHON_CMD="coverage run -m pytest && coverage report --format=json"
    PYTHON_REPORT="coverage html"
  fi
  
  # Java projects
  if fd "(pom\.xml|build\.gradle)" . | head -1 >/dev/null; then
    echo "☕ Java project detected"
    project_languages+=("java")
    if fd "pom\.xml" . | head -1 >/dev/null; then
      JAVA_CMD="mvn test jacoco:report"
    else
      JAVA_CMD="gradle test jacocoTestReport"
    fi
  fi
  
  echo "Detected languages: ${project_languages[@]}"
}
```

**Existing Coverage Analysis:**

```bash
# Analyze current coverage setup and reports
analyze_existing_coverage() {
  echo "🔍 Analyzing existing coverage setup..."
  
  # Check for existing coverage files and configurations
  for config_file in deno.json package.json Cargo.toml pyproject.toml pom.xml build.gradle; do
    if [ -f "$config_file" ]; then
      echo "📄 Found $config_file - checking coverage configuration"
      case "$config_file" in
        "deno.json")
          jq -e '.tasks.coverage // .tasks.test' "$config_file" >/dev/null 2>&1 && echo "✅ Coverage task configured" || echo "❌ No coverage task"
          ;;
        "package.json")  
          jq -e '.scripts | to_entries[] | select(.value | contains("coverage"))' "$config_file" >/dev/null 2>&1 && echo "✅ Coverage script found" || echo "❌ No coverage scripts"
          ;;
        "Cargo.toml")
          rg -q "(tarpaulin|cargo-tarpaulin)" "$config_file" && echo "✅ Tarpaulin configured" || echo "❌ No tarpaulin config"
          ;;
      esac
    fi
  done
  
  # Check for existing coverage reports
  existing_reports=$(fd "(coverage|tarpaulin-report|coverage\.out|\.coverage)" . -d 3)
  if [ -n "$existing_reports" ]; then
    echo "📊 Found existing coverage reports:"
    echo "$existing_reports" | head -5
  fi
}
```

CATCH (tool_detection_failed):

- LOG detection errors to session state
- PROVIDE manual configuration guidance
- SUGGEST tool installation steps

```bash
echo "⚠️ Coverage tool detection failed. Manual configuration may be required."
echo "Please verify that the following tools are installed:"
echo "  - For Deno: Built-in coverage support"
echo "  - For Rust: cargo install cargo-tarpaulin"
echo "  - For Go: Built-in coverage support"
echo "  - For Node.js: npm install --save-dev jest @vitest/ui or c8"
echo "  - For Python: pip install coverage pytest"
```

STEP 3: Comprehensive coverage analysis with parallel sub-agent coordination

IF project_complexity == "multi-language" OR codebase_size > 10000_lines:

LAUNCH parallel sub-agents for comprehensive coverage analysis:

- **Agent 1: Source Code Coverage Analysis**: Analyze primary source directories (src/, lib/, app/)
  - Focus: Function coverage, line coverage, branch coverage analysis
  - Tools: Language-specific coverage tools, complexity analysis
  - Output: Coverage metrics with gap identification and priority ranking

- **Agent 2: Test Code Quality Assessment**: Analyze test directories and test patterns
  - Focus: Test coverage quality, assertion patterns, mock usage, edge case coverage
  - Tools: Test file analysis, testing framework detection, quality metrics
  - Output: Test quality assessment with improvement recommendations

- **Agent 3: Critical Path Analysis**: Identify critical uncovered code paths
  - Focus: Public APIs, error handling, business logic, security-sensitive code
  - Tools: API discovery, error pattern analysis, critical function identification
  - Output: Prioritized list of critical coverage gaps

- **Agent 4: Performance Impact Analysis**: Assess coverage collection performance impact
  - Focus: Test execution time, coverage overhead, CI/CD pipeline impact
  - Tools: Benchmark analysis, performance monitoring, optimization opportunities
  - Output: Performance optimization recommendations

- **Agent 5: Integration & Reporting**: Generate comprehensive reports and integration strategies
  - Focus: Multi-format reporting, CI/CD integration, trend analysis
  - Tools: Report generation, dashboard creation, automation setup
  - Output: Complete coverage reporting solution with automation

**Sub-Agent Coordination:**

```bash
# Each agent reports findings to session state
echo "Parallel coverage analysis agents launched..."
echo "Results will be aggregated into comprehensive coverage report"
```

ELSE:

EXECUTE streamlined single-language coverage analysis:

```bash
# Single-language analysis workflow
echo "🔍 Executing streamlined coverage analysis for single-language project..."
```

STEP 4: Intelligent gap identification and critical path analysis

TRY:

**Critical Path Coverage Assessment:**

```bash
# Identify critical uncovered code paths using modern tools
analyze_critical_gaps() {
  echo "🎯 Identifying critical coverage gaps with priority ranking..."
  
  # Find uncovered public APIs by language
  case "$detected_language" in
    "typescript"|"javascript")
      echo "🔍 Analyzing TypeScript/JavaScript public APIs"
      rg "^export\s+(function|class|const|interface)" --type ts --type js src/ | \
        while IFS=: read -r file line_num content; do
          func_name=$(echo "$content" | rg -o "(function|class|const|interface)\s+\w+" | cut -d' ' -f2)
          # Check if this export is tested
          if ! rg -q "$func_name" tests/ test/ __tests__/ *.test.* *.spec.* 2>/dev/null; then
            echo "❌ CRITICAL: Uncovered public API: $func_name in $file:$line_num"
          fi
        done
      ;;
    "rust")
      echo "🔍 Analyzing Rust public items"
      rg "^pub\s+(fn|struct|enum|trait)" --type rust src/ | \
        while IFS=: read -r file line_num content; do
          item_name=$(echo "$content" | rg -o "(fn|struct|enum|trait)\s+\w+" | cut -d' ' -f2)
          # Check if this public item has tests
          if ! rg -q "$item_name" tests/ "${file%.*}_test.rs" 2>/dev/null && ! rg -q "#\[test\]" "$file"; then
            echo "❌ CRITICAL: Uncovered public item: $item_name in $file:$line_num"
          fi
        done
      ;;
    "go")
      echo "🔍 Analyzing Go public functions"
      rg "^func\s+[A-Z]" --type go . | \
        while IFS=: read -r file line_num content; do
          func_name=$(echo "$content" | rg -o "func\s+\w+" | cut -d' ' -f2)
          test_file="${file%.*}_test.go"
          if [ -f "$test_file" ] && ! rg -q "Test$func_name\|$func_name" "$test_file"; then
            echo "❌ CRITICAL: Uncovered public function: $func_name in $file:$line_num"
          fi
        done
      ;;
  esac
}

# Analyze error handling coverage
analyze_error_coverage() {
  echo "🚨 Analyzing error handling coverage..."
  
  # Find error handling patterns that might be uncovered
  rg "(throw|panic|error|Error|except|raise|Result<|Option<)" --type "$detected_language" src/ | \
    head -20 | \
    while IFS=: read -r file line_num content; do
      echo "🔍 Check error handling coverage: $file:$line_num"
      echo "    Pattern: $(echo "$content" | cut -c1-80)..."
    done
}

# Security-sensitive code analysis  
analyze_security_coverage() {
  echo "🔒 Analyzing security-sensitive code coverage..."
  
  # Find authentication, authorization, and security patterns
  security_patterns=(
    "auth" "login" "password" "token" "jwt" "session"
    "encrypt" "decrypt" "hash" "crypto" "security"
    "admin" "privilege" "permission" "role" "access"
  )
  
  for pattern in "${security_patterns[@]}"; do
    matches=$(rg -i "$pattern" --type "$detected_language" src/ | head -3)
    if [ -n "$matches" ]; then
      echo "🔒 Security pattern '$pattern' found - verify test coverage:"
      echo "$matches" | while IFS=: read -r file line_num content; do
        echo "    $file:$line_num"
      done
    fi
  done
}
```

**Performance-Critical Code Analysis:**

```bash
# Identify performance-critical functions that need coverage
analyze_performance_critical() {
  echo "⚡ Analyzing performance-critical code coverage..."
  
  performance_patterns=(
    "benchmark" "performance" "optimize" "cache" "async" "parallel" 
    "database" "query" "index" "sort" "search" "algorithm"
  )
  
  for pattern in "${performance_patterns[@]}"; do
    matches=$(rg -i "$pattern" --type "$detected_language" src/ | head -2)
    if [ -n "$matches" ]; then
      echo "⚡ Performance pattern '$pattern' - ensure adequate test coverage"
    fi
  done
}
```

STEP 5: Execute coverage collection with comprehensive reporting

**Language-Specific Coverage Execution:**

```bash
# Execute coverage based on detected project type
execute_coverage_collection() {
  echo "📊 Executing coverage collection for detected languages..."
  
  if [ -n "$DENO_CMD" ]; then
    echo "🦕 Running Deno coverage..."
    eval "$DENO_CMD"
    deno coverage coverage --html --output=coverage-html
    deno coverage coverage --json --output=coverage.json
  fi
  
  if [ -n "$RUST_CMD" ]; then
    echo "🦀 Running Rust coverage..."
    if ! command -v cargo-tarpaulin >/dev/null; then
      echo "Installing cargo-tarpaulin..."
      cargo install cargo-tarpaulin
    fi
    eval "$RUST_CMD"
  fi
  
  if [ -n "$GO_CMD" ]; then
    echo "🐹 Running Go coverage..."
    eval "$GO_CMD"
    eval "$GO_REPORT"
  fi
  
  if [ -n "$NODE_CMD" ]; then
    echo "⚡ Running Node.js coverage..."
    eval "$NODE_CMD"
  fi
  
  if [ -n "$PYTHON_CMD" ]; then
    echo "🐍 Running Python coverage..."
    eval "$PYTHON_CMD"
    eval "$PYTHON_REPORT"
  fi
  
  if [ -n "$JAVA_CMD" ]; then
    echo "☕ Running Java coverage..."
    eval "$JAVA_CMD"
  fi
}
```

CATCH (coverage_execution_failed):

- LOG execution errors to session state
- PROVIDE troubleshooting guidance
- SAVE partial results for manual analysis

```bash
echo "❌ Coverage execution failed. Troubleshooting steps:"
echo "  1. Verify all tests pass without coverage: npm test / cargo test / go test / deno test"
echo "  2. Check coverage tool installation and configuration"
echo "  3. Review test directory structure and naming conventions"
echo "  4. Ensure all dependencies are properly installed"
```

STEP 6: Generate comprehensive coverage reports and actionable insights

TRY:

**Multi-Format Report Generation:**

```bash
# Generate comprehensive coverage reports in multiple formats
generate_coverage_reports() {
  echo "📊 Generating comprehensive coverage reports..."
  
  # Create reports directory structure
  mkdir -p coverage-reports/{html,json,lcov,xml}
  
  # Language-specific report generation
  case "$detected_language" in
    "deno")
      echo "🦕 Generating Deno coverage reports..."
      deno coverage coverage --html --output=coverage-reports/html/
      deno coverage coverage --json --output=coverage-reports/json/coverage.json
      deno coverage coverage --lcov --output=coverage-reports/lcov/coverage.lcov
      ;;
    "rust")
      echo "🦀 Generating Rust coverage reports..."
      # Tarpaulin generates multiple formats automatically
      cp coverage/tarpaulin-report.html coverage-reports/html/
      cp coverage/tarpaulin-report.json coverage-reports/json/
      cp coverage/cobertura.xml coverage-reports/xml/ 2>/dev/null || true
      ;;
    "go")
      echo "🐹 Generating Go coverage reports..."
      go tool cover -html=coverage.out -o coverage-reports/html/coverage.html
      go tool cover -func=coverage.out > coverage-reports/coverage-summary.txt
      ;;
    "node")
      echo "⚡ Generating Node.js coverage reports..."
      # Coverage reports already generated by jest/vitest
      cp -r coverage/* coverage-reports/ 2>/dev/null || true
      ;;
  esac
  
  echo "✅ Coverage reports generated in coverage-reports/"
}
```

**Intelligent Gap Analysis and Recommendations:**

````bash
# Generate actionable coverage improvement recommendations
generate_improvement_recommendations() {
  echo "💡 Generating coverage improvement recommendations..."
  
  # Create recommendations file
  cat > coverage-reports/recommendations.md << 'EOF'
# Coverage Improvement Recommendations

## Executive Summary
- **Current Coverage**: [TO BE FILLED]
- **Target Coverage**: 80%+
- **Critical Gaps**: [COUNT] uncovered public APIs
- **Priority**: High-impact, low-effort improvements

## High-Priority Improvements

### 1. Critical Public API Coverage
EOF

  # Add specific recommendations based on analysis
  if [ -f "/tmp/critical-gaps-$SESSION_ID.txt" ]; then
    echo "**Uncovered Public APIs requiring immediate attention:**" >> coverage-reports/recommendations.md
    cat "/tmp/critical-gaps-$SESSION_ID.txt" >> coverage-reports/recommendations.md
  fi

  cat >> coverage-reports/recommendations.md << 'EOF'

### 2. Error Handling Coverage
**Focus Areas:**
- Exception handling paths
- Error return codes
- Failure modes and recovery

### 3. Security-Sensitive Code
**Priority:**
- Authentication mechanisms
- Authorization checks
- Input validation
- Cryptographic operations

## Implementation Strategy

### Phase 1: Critical Path Coverage (Week 1)
- [ ] Cover all public APIs
- [ ] Test main error handling paths
- [ ] Validate security-critical functions

### Phase 2: Comprehensive Coverage (Week 2-3)
- [ ] Edge case testing
- [ ] Performance scenario testing
- [ ] Integration test expansion

### Phase 3: Quality Enhancement (Week 4)
- [ ] Test quality improvement
- [ ] Mock and stub refinement
- [ ] Documentation updates

## Automated Tools Integration

### CI/CD Pipeline
```bash
# Add to CI pipeline
npm run test:coverage
coverage-threshold-check 80
EOF

  echo "📋 Recommendations saved to coverage-reports/recommendations.md"
}
````

**Interactive Coverage Dashboard Generation:**

```bash
# Generate interactive HTML dashboard
generate_interactive_dashboard() {
  echo "🎯 Generating interactive coverage dashboard..."
  
  cat > coverage-reports/dashboard.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Coverage Analysis Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f7fa; }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; max-width: 1200px; margin: 0 auto; }
        .card { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.07); border: 1px solid #e1e5e9; }
        .metric { font-size: 2.5em; font-weight: 700; margin: 10px 0; }
        .metric.excellent { color: #10b981; }
        .metric.good { color: #3b82f6; }
        .metric.warning { color: #f59e0b; }
        .metric.critical { color: #ef4444; }
        .progress-bar { width: 100%; height: 8px; background: #e5e7eb; border-radius: 4px; overflow: hidden; margin: 10px 0; }
        .progress-fill { height: 100%; transition: width 0.6s ease; border-radius: 4px; }
        .progress-fill.excellent { background: linear-gradient(90deg, #10b981, #059669); }
        .progress-fill.good { background: linear-gradient(90deg, #3b82f6, #2563eb); }
        .progress-fill.warning { background: linear-gradient(90deg, #f59e0b, #d97706); }
        .progress-fill.critical { background: linear-gradient(90deg, #ef4444, #dc2626); }
        .recommendation { background: #f0f9ff; border-left: 4px solid #3b82f6; padding: 12px; margin: 10px 0; border-radius: 4px; }
        .chart-container { position: relative; height: 200px; }
        h1, h2, h3 { color: #1f2937; }
        .status-badge { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: 600; }
        .status-badge.pass { background: #d1fae5; color: #065f46; }
        .status-badge.fail { background: #fee2e2; color: #991b1b; }
    </style>
</head>
<body>
    <h1>📊 Code Coverage Analysis Dashboard</h1>
    <p>Generated on: <strong id="timestamp"></strong> | Session: <strong>SESSION_ID_PLACEHOLDER</strong></p>
    
    <div class="dashboard">
        <div class="card">
            <h2>Overall Coverage</h2>
            <div class="metric excellent" id="overall-coverage">85.2%</div>
            <div class="progress-bar">
                <div class="progress-fill excellent" style="width: 85.2%"></div>
            </div>
            <p><strong>Target:</strong> 80% | <span class="status-badge pass">PASSING</span></p>
        </div>
        
        <div class="card">
            <h2>Coverage Breakdown</h2>
            <div class="chart-container">
                <canvas id="coverageChart"></canvas>
            </div>
        </div>
        
        <div class="card">
            <h2>Critical Gaps</h2>
            <div class="metric warning" id="critical-gaps">12</div>
            <p>Uncovered public APIs</p>
            <div class="recommendation">
                <strong>Priority:</strong> Focus on authentication and error handling modules
            </div>
        </div>
        
        <div class="card">
            <h2>Quality Score</h2>
            <div class="metric good" id="quality-score">7.8/10</div>
            <div class="progress-bar">
                <div class="progress-fill good" style="width: 78%"></div>
            </div>
            <p>Based on test density and assertion quality</p>
        </div>
        
        <div class="card">
            <h2>Recommendations</h2>
            <ul>
                <li>📝 Add tests for 12 uncovered public APIs</li>
                <li>🔒 Improve security function coverage</li>
                <li>⚠️ Test error handling paths</li>
                <li>🚀 Add performance test scenarios</li>
            </ul>
        </div>
        
        <div class="card">
            <h2>Trend Analysis</h2>
            <div class="chart-container">
                <canvas id="trendChart"></canvas>
            </div>
        </div>
    </div>

    <script>
        // Set timestamp
        document.getElementById('timestamp').textContent = new Date().toLocaleString();
        
        // Coverage breakdown chart
        const ctx1 = document.getElementById('coverageChart').getContext('2d');
        new Chart(ctx1, {
            type: 'doughnut',
            data: {
                labels: ['Lines', 'Branches', 'Functions', 'Statements'],
                datasets: [{
                    data: [85.2, 78.5, 92.1, 84.7],
                    backgroundColor: ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });

        // Trend chart
        const ctx2 = document.getElementById('trendChart').getContext('2d');
        new Chart(ctx2, {
            type: 'line',
            data: {
                labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Current'],
                datasets: [{
                    label: 'Coverage %',
                    data: [65, 72, 78, 82, 85.2],
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    </script>
</body>
</html>
EOF

  # Replace placeholder with actual session ID
  sed -i.bak "s/SESSION_ID_PLACEHOLDER/$SESSION_ID/g" coverage-reports/dashboard.html
  rm coverage-reports/dashboard.html.bak
  
  echo "🎯 Interactive dashboard generated: coverage-reports/dashboard.html"
}
```

STEP 7: CI/CD integration and coverage enforcement automation

**Generate Coverage Enforcement Workflow:**

```bash
# Generate GitHub Actions workflow for coverage enforcement
generate_ci_coverage_workflow() {
  echo "🔄 Generating CI/CD coverage enforcement workflow..."
  
  mkdir -p .github/workflows
  
  cat > .github/workflows/coverage.yml << 'EOF'
name: Coverage Analysis and Enforcement

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  coverage:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Setup environment
        run: |
          # Auto-detect and setup language environment
          if [ -f "deno.json" ]; then
            curl -fsSL https://deno.land/install.sh | sh
            echo "$HOME/.deno/bin" >> $GITHUB_PATH
          elif [ -f "Cargo.toml" ]; then
            rustup update stable
            cargo install cargo-tarpaulin
          elif [ -f "go.mod" ]; then
            echo "Go environment ready"
          elif [ -f "package.json" ]; then
            node --version
            npm --version
          fi
          
      - name: Run tests with coverage
        run: |
          # Execute coverage based on project type
          if [ -f "deno.json" ]; then
            deno task test
            deno coverage coverage --json > coverage.json
          elif [ -f "Cargo.toml" ]; then
            cargo tarpaulin --out Json --output-dir coverage
          elif [ -f "go.mod" ]; then
            go test -coverprofile=coverage.out ./...
            go tool cover -func=coverage.out | tail -1 | awk '{print $3}' > coverage-percentage.txt
          elif [ -f "package.json" ]; then
            npm test -- --coverage --coverageReporters=json
          fi
          
      - name: Check coverage threshold
        run: |
          THRESHOLD=${COVERAGE_THRESHOLD:-80}
          
          # Extract coverage percentage based on project type
          if [ -f "coverage.json" ]; then
            CURRENT=$(jq -r '.percent' coverage.json)
          elif [ -f "coverage/tarpaulin-report.json" ]; then
            CURRENT=$(jq -r '.files | map(.summary.lines.percent) | add / length' coverage/tarpaulin-report.json)
          elif [ -f "coverage-percentage.txt" ]; then
            CURRENT=$(cat coverage-percentage.txt | tr -d '%')
          elif [ -f "coverage/coverage-summary.json" ]; then
            CURRENT=$(jq -r '.total.lines.pct' coverage/coverage-summary.json)
          fi
          
          echo "Current coverage: $CURRENT%"
          echo "Threshold: $THRESHOLD%"
          
          if (( $(echo "$CURRENT < $THRESHOLD" | bc -l) )); then
            echo "❌ Coverage $CURRENT% is below threshold $THRESHOLD%"
            exit 1
          else
            echo "✅ Coverage $CURRENT% meets threshold $THRESHOLD%"
          fi
          
      - name: Upload coverage reports
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.json,./coverage.out,./coverage/lcov.info
          fail_ci_if_error: false
          
      - name: Comment PR with coverage
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            let coverageData = {};
            
            // Try to read coverage data from different formats
            try {
              if (fs.existsSync('coverage.json')) {
                coverageData = JSON.parse(fs.readFileSync('coverage.json', 'utf8'));
              } else if (fs.existsSync('coverage/coverage-summary.json')) {
                coverageData = JSON.parse(fs.readFileSync('coverage/coverage-summary.json', 'utf8')).total;
              }
            } catch (e) {
              console.log('Could not parse coverage data');
              return;
            }
            
            const comment = `
            ## 📊 Coverage Report
            
            | Metric | Coverage | Status |
            |--------|----------|---------|
            | Lines | ${coverageData.lines?.pct || 'N/A'}% | ${coverageData.lines?.pct >= 80 ? '✅' : '❌'} |
            | Branches | ${coverageData.branches?.pct || 'N/A'}% | ${coverageData.branches?.pct >= 80 ? '✅' : '❌'} |
            | Functions | ${coverageData.functions?.pct || 'N/A'}% | ${coverageData.functions?.pct >= 80 ? '✅' : '❌'} |
            | Statements | ${coverageData.statements?.pct || 'N/A'}% | ${coverageData.statements?.pct >= 80 ? '✅' : '❌'} |
            
            ${coverageData.lines?.pct >= 80 ? '🎉 Great job! Coverage meets requirements.' : '⚠️ Coverage below 80% threshold. Please add more tests.'}
            
            📈 [View detailed coverage report](https://codecov.io/gh/${context.repo.owner}/${context.repo.repo}/pull/${context.issue.number})
            `;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
EOF

  echo "🔄 Coverage enforcement workflow generated: .github/workflows/coverage.yml"
}
```

STEP 8: Session state management and final reporting

**Update Session State and Generate Summary:**

```bash
# Update session state with final results
update_session_state() {
  echo "💾 Updating session state with coverage analysis results..."
  
  jq --arg timestamp "$(gdate -Iseconds 2>/dev/null || date -Iseconds)" \
     --arg status "completed" \
     --arg reports_generated "$(ls coverage-reports/ 2>/dev/null | wc -l | tr -d ' ')" \
     '.timestamp = $timestamp | .status = $status | .reportsGenerated = ($reports_generated | tonumber)' \
     /tmp/coverage-session-$SESSION_ID.json > /tmp/coverage-session-$SESSION_ID.tmp && \
  mv /tmp/coverage-session-$SESSION_ID.tmp /tmp/coverage-session-$SESSION_ID.json
}

# Generate final summary report
generate_final_summary() {
  echo "📋 Generating final coverage analysis summary..."
  
  cat > coverage-analysis-summary.md << EOF
# Coverage Analysis Summary

**Session ID:** $SESSION_ID  
**Target Project:** $ARGUMENTS  
**Analysis Date:** $(date)

## Results Overview

### Coverage Metrics
- **Overall Coverage:** [Extracted from reports]
- **Languages Analyzed:** $(jq -r '.detectedLanguages[]' /tmp/coverage-session-$SESSION_ID.json 2>/dev/null | paste -sd ',' -)
- **Critical Gaps:** [Count from analysis]
- **Reports Generated:** $(ls coverage-reports/ 2>/dev/null | wc -l | tr -d ' ') files

### Key Findings
1. **Public API Coverage:** [Status]
2. **Error Handling Coverage:** [Status]  
3. **Security Code Coverage:** [Status]
4. **Performance-Critical Coverage:** [Status]

### Generated Artifacts
- 📊 Interactive dashboard: \`coverage-reports/dashboard.html\`
- 📋 Improvement recommendations: \`coverage-reports/recommendations.md\`
- 🔄 CI/CD workflow: \`.github/workflows/coverage.yml\`
- 📈 Multi-format reports: \`coverage-reports/\`

### Next Steps
1. Review the interactive dashboard for detailed insights
2. Implement high-priority recommendations
3. Integrate coverage enforcement into CI/CD pipeline
4. Set up automated coverage monitoring

**Session completed at:** $(date)
EOF

  echo "📋 Final summary saved to coverage-analysis-summary.md"
}
```

FINALLY:

- SAVE session state for potential follow-up analysis
- PROVIDE guidance for using generated reports and tools
- SUGGEST integration with development workflow

```bash
echo "✅ Coverage analysis completed successfully"
echo "🎯 Session: $SESSION_ID"
echo "📊 Reports available in: coverage-reports/"
echo "🔄 CI/CD integration ready: .github/workflows/coverage.yml"
echo "📋 Summary: coverage-analysis-summary.md"
echo ""
echo "💡 Next actions:"
echo "  1. Open coverage-reports/dashboard.html for interactive analysis"
echo "  2. Review coverage-reports/recommendations.md for specific improvements"
echo "  3. Commit and push .github/workflows/coverage.yml to enable CI enforcement"
echo "  4. Use session ID $SESSION_ID for follow-up analysis or troubleshooting"
```

This comprehensive coverage analysis command provides intelligent technology detection, parallel sub-agent coordination for complex projects, critical path analysis, multi-format reporting, and complete CI/CD integration with actionable recommendations for coverage improvement.
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

````
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
````

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
