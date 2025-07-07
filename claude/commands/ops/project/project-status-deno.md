---
allowed-tools: Bash(deno:*), Bash(fd:*), Bash(rg:*), Bash(jq:*), Bash(gdate:*), Bash(echo:*), Bash(which:*), Bash(eza:*), Bash(bat:*)
description: Comprehensive Deno TypeScript project health check with type checking, testing, linting, and formatting analysis
---

## Context

- Session ID: !`gdate +%s%N 2>/dev/null || date +%s%N 2>/dev/null || echo "$(date +%s)$(jot -r 1 100000 999999 2>/dev/null || shuf -i 100000-999999 -n 1 2>/dev/null || echo $RANDOM$RANDOM)"`
- Check mode: $ARGUMENTS (optional - quick or detailed, default: quick)
- Current directory: !`pwd`
- Deno version: !`deno --version 2>&1 | head -1 || echo "Deno not installed"`
- Project detected: !`[ -f deno.json ] || [ -f deno.jsonc ] && echo "✅ Deno project found" || echo "❌ No deno.json found"`
- Fresh project: !`rg -q "@fresh/core" deno.json* import_map.json 2>/dev/null && echo "Fresh 2.0 project detected" || echo "Not a Fresh project"`
- Import map: !`[ -f import_map.json ] && echo "import_map.json present" || echo "No import map (using deno.json imports)"`

## Your Task

STEP 1: Initialize Deno project health check session

- CREATE session state file: `/tmp/deno-status-$SESSION_ID.json`
- VALIDATE Deno project presence (deno.json/deno.jsonc)
- DETERMINE check mode from $ARGUMENTS (quick vs detailed)
- GATHER initial project metadata

```bash
# Initialize session state
echo '{
  "sessionId": "'$SESSION_ID'",
  "timestamp": "'$(gdate -Iseconds 2>/dev/null || date -Iseconds)'",
  "checkMode": "'${ARGUMENTS:-quick}'",
  "projectPath": "'$(pwd)'",
  "healthStatus": {
    "typecheck": "pending",
    "tests": "pending",
    "lint": "pending",
    "format": "pending",
    "tasks": "pending",
    "dependencies": "pending"
  },
  "issues": []
}' > /tmp/deno-status-$SESSION_ID.json
```

STEP 2: Type checking and compilation health

TRY:

```bash
echo "🔍 TYPE CHECK STATUS"
echo "═══════════════════════"

# Run type checking
if deno check **/*.ts **/*.tsx 2>/dev/null || deno check main.ts mod.ts 2>/dev/null; then
    echo "✅ Type checking passes"
    jq '.healthStatus.typecheck = "pass"' /tmp/deno-status-$SESSION_ID.json > /tmp/deno-status-$SESSION_ID.tmp && mv /tmp/deno-status-$SESSION_ID.tmp /tmp/deno-status-$SESSION_ID.json
else
    echo "❌ Type errors detected"
    jq '.healthStatus.typecheck = "fail"' /tmp/deno-status-$SESSION_ID.json > /tmp/deno-status-$SESSION_ID.tmp && mv /tmp/deno-status-$SESSION_ID.tmp /tmp/deno-status-$SESSION_ID.json
    echo "Run 'deno check' for details"
fi

# Count TypeScript files
ts_count=$(fd "\.(ts|tsx)$" . --exclude node_modules --exclude _fresh 2>/dev/null | wc -l || echo "0")
echo "   TypeScript files: $ts_count"

# Check for JSX/TSX files (React/Preact)
tsx_count=$(fd "\.tsx$" . --exclude node_modules --exclude _fresh 2>/dev/null | wc -l || echo "0")
[ "$tsx_count" -gt 0 ] && echo "   TSX files: $tsx_count (React/Preact components)"
```

CATCH (typecheck_failed):

```bash
echo "⚠️  Type check failed - checking for common issues:"
echo "  - Missing type definitions: check import statements"
echo "  - Configuration issues: verify deno.json settings"
echo "  - Import errors: ensure all imports are valid"
```

STEP 3: Test suite health analysis

```bash
echo ""
echo "🧪 TEST STATUS"
echo "═══════════════"

# Check for test files
test_file_count=$(fd "_test\.(ts|tsx|js|jsx)$|\.test\.(ts|tsx|js|jsx)$" . 2>/dev/null | wc -l || echo "0")
echo "   Test files: $test_file_count"

if [ "$test_file_count" -gt 0 ]; then
    if [ "${ARGUMENTS:-quick}" = "detailed" ]; then
        # Detailed mode: run all tests
        if deno test --allow-all 2>&1 | rg -q "ok \|"; then
            echo "✅ All tests pass"
            jq '.healthStatus.tests = "pass"' /tmp/deno-status-$SESSION_ID.json > /tmp/deno-status-$SESSION_ID.tmp && mv /tmp/deno-status-$SESSION_ID.tmp /tmp/deno-status-$SESSION_ID.json
            
            # Count passing tests
            test_count=$(deno test --allow-all 2>&1 | rg -c "ok \|" || echo "0")
            echo "   Passing tests: $test_count"
        else
            echo "❌ Test failures detected"
            jq '.healthStatus.tests = "fail"' /tmp/deno-status-$SESSION_ID.json > /tmp/deno-status-$SESSION_ID.tmp && mv /tmp/deno-status-$SESSION_ID.tmp /tmp/deno-status-$SESSION_ID.json
            echo "Run 'deno test' for details"
        fi
        
        # Coverage analysis (if enabled)
        if deno test --coverage=/tmp/cov-$SESSION_ID --allow-all >/dev/null 2>&1; then
            echo "📊 Generating coverage report..."
            deno coverage /tmp/cov-$SESSION_ID --lcov > /tmp/coverage-$SESSION_ID.lcov 2>/dev/null
            if [ -f /tmp/coverage-$SESSION_ID.lcov ]; then
                echo "   Coverage data generated"
            fi
            rm -rf /tmp/cov-$SESSION_ID /tmp/coverage-$SESSION_ID.lcov
        fi
    else
        # Quick mode: just verify tests can be discovered
        if deno test --no-run --allow-all >/dev/null 2>&1; then
            echo "✅ Tests compile successfully"
            jq '.healthStatus.tests = "pass"' /tmp/deno-status-$SESSION_ID.json > /tmp/deno-status-$SESSION_ID.tmp && mv /tmp/deno-status-$SESSION_ID.tmp /tmp/deno-status-$SESSION_ID.json
        else
            echo "❌ Test compilation failed"
            jq '.healthStatus.tests = "fail"' /tmp/deno-status-$SESSION_ID.json > /tmp/deno-status-$SESSION_ID.tmp && mv /tmp/deno-status-$SESSION_ID.tmp /tmp/deno-status-$SESSION_ID.json
        fi
    fi
else
    echo "⚠️  No test files found"
    echo "   Create test files with _test.ts or .test.ts suffix"
    jq '.healthStatus.tests = "warn"' /tmp/deno-status-$SESSION_ID.json > /tmp/deno-status-$SESSION_ID.tmp && mv /tmp/deno-status-$SESSION_ID.tmp /tmp/deno-status-$SESSION_ID.json
fi
```

STEP 4: Code quality - linting and formatting

```bash
echo ""
echo "🔍 CODE QUALITY"
echo "═══════════════"

# Linting
lint_output=$(deno lint 2>&1)
if echo "$lint_output" | rg -q "Checked.*file.*no problems found"; then
    echo "✅ No lint issues"
    jq '.healthStatus.lint = "pass"' /tmp/deno-status-$SESSION_ID.json > /tmp/deno-status-$SESSION_ID.tmp && mv /tmp/deno-status-$SESSION_ID.tmp /tmp/deno-status-$SESSION_ID.json
else
    problem_count=$(echo "$lint_output" | rg -c "at " || echo "0")
    if [ "$problem_count" -gt 0 ]; then
        echo "⚠️  $problem_count lint issues found"
        jq '.healthStatus.lint = "warn"' /tmp/deno-status-$SESSION_ID.json > /tmp/deno-status-$SESSION_ID.tmp && mv /tmp/deno-status-$SESSION_ID.tmp /tmp/deno-status-$SESSION_ID.json
        echo "Run 'deno lint' for details"
    else
        echo "✅ Linting passed"
        jq '.healthStatus.lint = "pass"' /tmp/deno-status-$SESSION_ID.json > /tmp/deno-status-$SESSION_ID.tmp && mv /tmp/deno-status-$SESSION_ID.tmp /tmp/deno-status-$SESSION_ID.json
    fi
fi

# Formatting
if deno fmt --check >/dev/null 2>&1; then
    echo "✅ Code properly formatted"
    jq '.healthStatus.format = "pass"' /tmp/deno-status-$SESSION_ID.json > /tmp/deno-status-$SESSION_ID.tmp && mv /tmp/deno-status-$SESSION_ID.tmp /tmp/deno-status-$SESSION_ID.json
else
    unformatted=$(deno fmt --check 2>&1 | rg -c "from " || echo "0")
    echo "⚠️  $unformatted files need formatting"
    jq '.healthStatus.format = "warn"' /tmp/deno-status-$SESSION_ID.json > /tmp/deno-status-$SESSION_ID.tmp && mv /tmp/deno-status-$SESSION_ID.tmp /tmp/deno-status-$SESSION_ID.json
    echo "Run 'deno fmt' to fix"
fi
```

STEP 5: Task management and project configuration

```bash
echo ""
echo "📋 TASKS & CONFIGURATION"
echo "═══════════════════════"

# Check for deno.json tasks
if [ -f deno.json ] || [ -f deno.jsonc ]; then
    task_count=$(deno task 2>&1 | rg -c "^  " || echo "0")
    if [ "$task_count" -gt 0 ]; then
        echo "✅ $task_count tasks configured"
        jq '.healthStatus.tasks = "pass"' /tmp/deno-status-$SESSION_ID.json > /tmp/deno-status-$SESSION_ID.tmp && mv /tmp/deno-status-$SESSION_ID.tmp /tmp/deno-status-$SESSION_ID.json
        
        # List common tasks if present
        echo "   Available tasks:"
        deno task 2>&1 | rg "^  (dev|test|build|start|check|fmt|lint)" | head -5 || true
    else
        echo "⚠️  No tasks configured"
        jq '.healthStatus.tasks = "warn"' /tmp/deno-status-$SESSION_ID.json > /tmp/deno-status-$SESSION_ID.tmp && mv /tmp/deno-status-$SESSION_ID.tmp /tmp/deno-status-$SESSION_ID.json
        echo "   Add tasks to deno.json for common operations"
    fi
    
    # Check for compiler options
    if rg -q "compilerOptions" deno.json* 2>/dev/null; then
        echo "✅ Compiler options configured"
    fi
    
    # Check for import map or imports
    if rg -q "imports" deno.json* 2>/dev/null || [ -f import_map.json ]; then
        echo "✅ Import mappings configured"
    fi
else
    echo "❌ No deno.json configuration file"
    jq '.healthStatus.tasks = "fail"' /tmp/deno-status-$SESSION_ID.json > /tmp/deno-status-$SESSION_ID.tmp && mv /tmp/deno-status-$SESSION_ID.tmp /tmp/deno-status-$SESSION_ID.json
    echo "   Create with: deno init"
fi
```

STEP 6: Dependency analysis and caching

```bash
echo ""
echo "📦 DEPENDENCIES & CACHE"
echo "═════════════════════"

# Analyze dependencies
if [ -f deno.lock ]; then
    echo "✅ Lock file present (dependencies locked)"
    dep_count=$(jq -r '.remote | length' deno.lock 2>/dev/null || echo "0")
    echo "   Locked dependencies: $dep_count"
else
    echo "⚠️  No lock file found"
    echo "   Generate with: deno cache --lock=deno.lock --lock-write deps.ts"
fi

# Check cache status
if [ "${ARGUMENTS:-quick}" = "detailed" ]; then
    echo ""
    echo "🔄 Checking dependency cache..."
    
    # Try to cache dependencies
    if deno cache --reload --lock=deno.lock deps.ts main.ts mod.ts 2>/dev/null; then
        echo "✅ Dependencies cached successfully"
        jq '.healthStatus.dependencies = "pass"' /tmp/deno-status-$SESSION_ID.json > /tmp/deno-status-$SESSION_ID.tmp && mv /tmp/deno-status-$SESSION_ID.tmp /tmp/deno-status-$SESSION_ID.json
    else
        echo "ℹ️  Some dependencies may need caching"
        jq '.healthStatus.dependencies = "warn"' /tmp/deno-status-$SESSION_ID.json > /tmp/deno-status-$SESSION_ID.tmp && mv /tmp/deno-status-$SESSION_ID.tmp /tmp/deno-status-$SESSION_ID.json
    fi
    
    # Analyze import sources
    echo ""
    echo "📊 Import Analysis:"
    jsr_imports=$(rg -c "jsr:@" . --type ts --type tsx 2>/dev/null || echo "0")
    npm_imports=$(rg -c "npm:" . --type ts --type tsx 2>/dev/null || echo "0")
    https_imports=$(rg -c "https://" . --type ts --type tsx 2>/dev/null || echo "0")
    
    [ "$jsr_imports" -gt 0 ] && echo "   JSR imports: $jsr_imports (recommended)"
    [ "$npm_imports" -gt 0 ] && echo "   NPM imports: $npm_imports"
    [ "$https_imports" -gt 0 ] && echo "   HTTPS imports: $https_imports (consider using JSR)"
else
    jq '.healthStatus.dependencies = "pass"' /tmp/deno-status-$SESSION_ID.json > /tmp/deno-status-$SESSION_ID.tmp && mv /tmp/deno-status-$SESSION_ID.tmp /tmp/deno-status-$SESSION_ID.json
fi
```

STEP 7: Project structure and Fresh-specific checks

IF check_mode is "detailed":

```bash
echo ""
echo "📁 PROJECT STRUCTURE"
echo "══════════════════"

# Check for important files
[ -f README.md ] && echo "✅ README.md present" || echo "⚠️  Missing README.md"
[ -f LICENSE ] && echo "✅ LICENSE present" || echo "⚠️  Missing LICENSE file"
[ -f .gitignore ] && echo "✅ .gitignore present" || echo "⚠️  Missing .gitignore"
[ -d .github/workflows ] && echo "✅ CI/CD workflows present" || echo "ℹ️  No GitHub Actions workflows"

# Fresh-specific checks
if rg -q "@fresh/core" deno.json* import_map.json 2>/dev/null; then
    echo ""
    echo "🍋 FRESH 2.0 PROJECT ANALYSIS"
    
    # Check Fresh structure
    [ -d routes ] && echo "✅ routes/ directory present" || echo "❌ Missing routes directory"
    [ -d islands ] && echo "✅ islands/ directory present" || echo "❌ Missing islands directory"
    [ -d components ] && echo "✅ components/ directory present" || echo "ℹ️  No components directory"
    [ -d static ] && echo "✅ static/ directory present" || echo "ℹ️  No static directory"
    
    # Fresh-specific files
    [ -f fresh.gen.ts ] && echo "✅ fresh.gen.ts present" || echo "⚠️  Missing fresh.gen.ts (run deno task manifest)"
    [ -f dev.ts ] && echo "✅ dev.ts present" || echo "⚠️  Missing dev.ts"
    [ -f main.ts ] && echo "✅ main.ts present" || echo "⚠️  Missing main.ts"
    
    # Count routes and islands
    route_count=$(fd "\.tsx?$" routes 2>/dev/null | wc -l || echo "0")
    island_count=$(fd "\.tsx?$" islands 2>/dev/null | wc -l || echo "0")
    echo "   Routes: $route_count"
    echo "   Islands: $island_count"
fi

# General project patterns
echo ""
echo "📊 PROJECT METRICS"
file_count=$(fd "\.(ts|tsx|js|jsx)$" . --exclude node_modules --exclude _fresh 2>/dev/null | wc -l || echo "0")
echo "   Total source files: $file_count"

# Check for common patterns
[ -d tests ] && echo "   tests/ directory present"
[ -d scripts ] && echo "   scripts/ directory present"
[ -f deps.ts ] && echo "   deps.ts present (dependency management)"
[ -f mod.ts ] && echo "   mod.ts present (module entry point)"
```

FINALLY: Generate executive summary and recommendations

```bash
echo ""
echo "═══════════════════════════════════════════"
echo "📊 DENO PROJECT HEALTH SUMMARY"
echo "═══════════════════════════════════════════"
echo "Session: $SESSION_ID"
echo "Project: $(basename $(pwd))"
echo "Deno Version: $(deno --version 2>&1 | head -1 | rg -o "[0-9]+\.[0-9]+\.[0-9]+" || echo "unknown")"
echo ""

# Overall health score
health_data=$(cat /tmp/deno-status-$SESSION_ID.json)
pass_count=$(echo "$health_data" | jq -r '[.healthStatus[] | select(. == "pass")] | length')
total_checks=$(echo "$health_data" | jq -r '[.healthStatus[] | select(. != "pending")] | length')
health_percentage=$((pass_count * 100 / total_checks))

echo "🏆 Overall Health Score: $health_percentage%"
echo ""

# Quick status overview
echo "Status Overview:"
echo "$health_data" | jq -r '.healthStatus | to_entries[] | select(.value != "pending") | "  \(.key): \(.value)"' | sed 's/pass/✅/g; s/fail/❌/g; s/warn/⚠️/g'

# Recommendations
echo ""
echo "📋 RECOMMENDATIONS"
echo "═════════════════"

if [ "$health_percentage" -eq 100 ]; then
    echo "✨ Excellent! Your Deno project is in great health."
else
    echo "$health_data" | jq -r '.healthStatus | to_entries[] | select(.value != "pass" and .value != "pending") | .key' | while read -r failing_check; do
        case "$failing_check" in
            "typecheck")
                echo "🔧 Fix type errors: deno check **/*.ts"
                ;;
            "tests")
                echo "🧪 Fix failing tests: deno test"
                ;;
            "lint")
                echo "🔍 Fix lint issues: deno lint"
                ;;
            "format")
                echo "💅 Format code: deno fmt"
                ;;
            "tasks")
                echo "📋 Add tasks to deno.json for common operations"
                ;;
            "dependencies")
                echo "📦 Cache dependencies: deno cache deps.ts"
                ;;
        esac
    done
fi

# Additional recommendations
[ ! -f deno.json ] && [ ! -f deno.jsonc ] && echo "🔧 Initialize project: deno init"
[ ! -f deno.lock ] && echo "🔒 Create lock file: deno cache --lock=deno.lock --lock-write deps.ts"
[ "$test_file_count" -eq 0 ] && echo "🧪 Add tests: create files with _test.ts suffix"
[ ! -f README.md ] && echo "📝 Add a README.md file"
[ "$https_imports" -gt 0 ] && echo "📦 Consider migrating HTTPS imports to JSR"

echo ""
echo "💾 Full report saved to: /tmp/deno-status-$SESSION_ID.json"
```

## Quick Reference

### Usage Examples

```bash
# Quick health check (default)
/project-status-deno

# Detailed analysis with all checks
/project-status-deno detailed

# From a specific project directory
cd my-deno-project && /project-status-deno
```

### Health Checks Performed

1. **Type Checking**: TypeScript compilation and type safety
2. **Test Suite**: Test discovery, execution, and coverage
3. **Code Quality**: Linting and formatting standards
4. **Task Management**: deno.json configuration and tasks
5. **Dependencies**: Lock file, caching, and import analysis
6. **Project Structure**: Best practices and Fresh framework
7. **Import Patterns**: JSR vs NPM vs HTTPS imports (detailed mode)

This command provides comprehensive Deno project health monitoring with emphasis on modern Deno best practices and Fresh 2.0 support.
