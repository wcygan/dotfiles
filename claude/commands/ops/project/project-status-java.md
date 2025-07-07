---
allowed-tools: Bash(java:*), Bash(javac:*), Bash(gradle:*), Bash(mvn:*), Bash(fd:*), Bash(rg:*), Bash(jq:*), Bash(gdate:*), Bash(echo:*), Bash(which:*), Bash(eza:*), Bash(bat:*)
description: Comprehensive Java project health check with build, test, and code quality analysis for Gradle/Maven projects
---

## Context

- Session ID: !`gdate +%s%N 2>/dev/null || date +%s%N 2>/dev/null || echo "$(date +%s)$(jot -r 1 100000 999999 2>/dev/null || shuf -i 100000-999999 -n 1 2>/dev/null || echo $RANDOM$RANDOM)"`
- Check mode: $ARGUMENTS (optional - quick or detailed, default: quick)
- Current directory: !`pwd`
- Java version: !`java -version 2>&1 | head -1 || echo "Java not installed"`
- Build tool: !`[ -f build.gradle ] || [ -f build.gradle.kts ] && echo "Gradle" || ([ -f pom.xml ] && echo "Maven" || echo "No build file found")`
- Spring Boot: !`rg -q "spring-boot" build.gradle* pom.xml 2>/dev/null && echo "Spring Boot detected" || echo "Not a Spring Boot project"`
- Quarkus: !`rg -q "quarkus" build.gradle* pom.xml 2>/dev/null && echo "Quarkus detected" || echo "Not a Quarkus project"`

## Your Task

STEP 1: Initialize Java project health check session

- CREATE session state file: `/tmp/java-status-$SESSION_ID.json`
- DETECT build system (Gradle/Maven)
- DETERMINE check mode from $ARGUMENTS (quick vs detailed)
- GATHER initial project metadata

```bash
# Initialize session state
echo '{
  "sessionId": "'$SESSION_ID'",
  "timestamp": "'$(gdate -Iseconds 2>/dev/null || date -Iseconds)'",
  "checkMode": "'${ARGUMENTS:-quick}'",
  "projectPath": "'$(pwd)'",
  "buildTool": "unknown",
  "healthStatus": {
    "build": "pending",
    "tests": "pending",
    "checkstyle": "pending",
    "spotbugs": "pending",
    "dependencies": "pending",
    "coverage": "pending"
  },
  "issues": []
}' > /tmp/java-status-$SESSION_ID.json

# Detect build tool
if [ -f build.gradle ] || [ -f build.gradle.kts ]; then
    jq '.buildTool = "gradle"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
elif [ -f pom.xml ]; then
    jq '.buildTool = "maven"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
fi
```

STEP 2: Build and compilation health check

TRY:

```bash
echo "🔨 BUILD STATUS"
echo "═══════════════"

build_tool=$(jq -r '.buildTool' /tmp/java-status-$SESSION_ID.json)

case "$build_tool" in
    "gradle")
        # Gradle build
        if ./gradlew build -x test >/dev/null 2>&1 || gradle build -x test >/dev/null 2>&1; then
            echo "✅ Project builds successfully (Gradle)"
            jq '.healthStatus.build = "pass"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
        else
            echo "❌ Build errors detected"
            jq '.healthStatus.build = "fail"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
            echo "Run './gradlew build' for details"
        fi
        
        # Check Gradle wrapper
        if [ -f gradlew ]; then
            echo "✅ Gradle wrapper present"
            wrapper_version=$(./gradlew --version 2>/dev/null | rg "Gradle" | head -1 || echo "Unknown version")
            echo "   $wrapper_version"
        else
            echo "⚠️  No Gradle wrapper found"
            echo "   Generate with: gradle wrapper"
        fi
        ;;
        
    "maven")
        # Maven build
        if mvn compile >/dev/null 2>&1; then
            echo "✅ Project builds successfully (Maven)"
            jq '.healthStatus.build = "pass"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
        else
            echo "❌ Build errors detected"
            jq '.healthStatus.build = "fail"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
            echo "Run 'mvn compile' for details"
        fi
        
        # Check Maven wrapper
        if [ -f mvnw ]; then
            echo "✅ Maven wrapper present"
        else
            echo "⚠️  No Maven wrapper found"
            echo "   Generate with: mvn wrapper:wrapper"
        fi
        ;;
        
    *)
        echo "❌ No recognized build system found"
        echo "   Supported: Gradle (build.gradle) or Maven (pom.xml)"
        jq '.healthStatus.build = "fail"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
        ;;
esac

# Check for Java source files
src_count=$(fd "\.java$" src 2>/dev/null | wc -l || echo "0")
echo "   Java files: $src_count"
```

CATCH (build_check_failed):

```bash
echo "⚠️  Build check failed - checking for common issues:"
echo "  - JDK version mismatch: check java -version"
echo "  - Missing dependencies: run dependency download"
echo "  - Syntax errors: check compiler output"
```

STEP 3: Test suite health analysis

```bash
echo ""
echo "🧪 TEST STATUS"
echo "═══════════════"

case "$build_tool" in
    "gradle")
        if [ "${ARGUMENTS:-quick}" = "detailed" ]; then
            # Detailed mode: run all tests
            if ./gradlew test 2>&1 | rg -q "BUILD SUCCESSFUL" || gradle test 2>&1 | rg -q "BUILD SUCCESSFUL"; then
                echo "✅ All tests pass"
                jq '.healthStatus.tests = "pass"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
            else
                echo "❌ Test failures detected"
                jq '.healthStatus.tests = "fail"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
                echo "Run './gradlew test' for details"
            fi
            
            # Test report location
            if [ -d build/reports/tests ]; then
                echo "📊 Test reports: build/reports/tests/test/index.html"
            fi
        else
            # Quick mode: just check test compilation
            if ./gradlew testClasses >/dev/null 2>&1 || gradle testClasses >/dev/null 2>&1; then
                echo "✅ Tests compile successfully"
                jq '.healthStatus.tests = "pass"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
            else
                echo "❌ Test compilation failed"
                jq '.healthStatus.tests = "fail"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
            fi
        fi
        ;;
        
    "maven")
        if [ "${ARGUMENTS:-quick}" = "detailed" ]; then
            # Detailed mode: run all tests
            if mvn test 2>&1 | rg -q "BUILD SUCCESS"; then
                echo "✅ All tests pass"
                jq '.healthStatus.tests = "pass"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
            else
                echo "❌ Test failures detected"
                jq '.healthStatus.tests = "fail"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
                echo "Run 'mvn test' for details"
            fi
            
            # Test report location
            if [ -d target/surefire-reports ]; then
                echo "📊 Test reports: target/surefire-reports/"
            fi
        else
            # Quick mode: just compile tests
            if mvn test-compile >/dev/null 2>&1; then
                echo "✅ Tests compile successfully"
                jq '.healthStatus.tests = "pass"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
            else
                echo "❌ Test compilation failed"
                jq '.healthStatus.tests = "fail"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
            fi
        fi
        ;;
esac

# Count test files
test_count=$(fd "Test.*\.java$|.*Test\.java$" src/test 2>/dev/null | wc -l || echo "0")
echo "   Test files: $test_count"
```

STEP 4: Code quality and static analysis

```bash
echo ""
echo "🔍 CODE QUALITY"
echo "═══════════════"

case "$build_tool" in
    "gradle")
        # Checkstyle
        if rg -q "checkstyle" build.gradle* 2>/dev/null; then
            if ./gradlew checkstyleMain >/dev/null 2>&1; then
                echo "✅ Checkstyle passes"
                jq '.healthStatus.checkstyle = "pass"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
            else
                echo "⚠️  Checkstyle violations found"
                jq '.healthStatus.checkstyle = "warn"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
                echo "Run './gradlew checkstyleMain' for details"
            fi
        else
            echo "ℹ️  Checkstyle not configured"
        fi
        
        # SpotBugs
        if rg -q "spotbugs" build.gradle* 2>/dev/null; then
            if ./gradlew spotbugsMain >/dev/null 2>&1; then
                echo "✅ SpotBugs analysis clean"
                jq '.healthStatus.spotbugs = "pass"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
            else
                echo "⚠️  SpotBugs found issues"
                jq '.healthStatus.spotbugs = "warn"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
                echo "Report: build/reports/spotbugs/main.html"
            fi
        else
            echo "ℹ️  SpotBugs not configured"
        fi
        ;;
        
    "maven")
        # Checkstyle via Maven
        if rg -q "maven-checkstyle-plugin" pom.xml 2>/dev/null; then
            if mvn checkstyle:check >/dev/null 2>&1; then
                echo "✅ Checkstyle passes"
                jq '.healthStatus.checkstyle = "pass"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
            else
                echo "⚠️  Checkstyle violations found"
                jq '.healthStatus.checkstyle = "warn"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
                echo "Run 'mvn checkstyle:check' for details"
            fi
        else
            echo "ℹ️  Checkstyle not configured"
        fi
        
        # SpotBugs via Maven
        if rg -q "spotbugs-maven-plugin" pom.xml 2>/dev/null; then
            if mvn spotbugs:check >/dev/null 2>&1; then
                echo "✅ SpotBugs analysis clean"
                jq '.healthStatus.spotbugs = "pass"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
            else
                echo "⚠️  SpotBugs found issues"
                jq '.healthStatus.spotbugs = "warn"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
            fi
        else
            echo "ℹ️  SpotBugs not configured"
        fi
        ;;
esac
```

STEP 5: Dependency and security analysis

```bash
echo ""
echo "📦 DEPENDENCIES & SECURITY"
echo "══════════════════════════"

case "$build_tool" in
    "gradle")
        # Dependency updates
        if [ "${ARGUMENTS:-quick}" = "detailed" ]; then
            echo "🔄 Checking for dependency updates..."
            if ./gradlew dependencyUpdates >/dev/null 2>&1; then
                outdated=$(fd "dependency-updates-report" build/reports 2>/dev/null | head -1)
                if [ -n "$outdated" ]; then
                    updates=$(rg -c "->.*" "$outdated" 2>/dev/null || echo "0")
                    if [ "$updates" -gt 0 ]; then
                        echo "⚠️  $updates dependencies have updates available"
                    else
                        echo "✅ All dependencies up to date"
                    fi
                fi
            fi
        fi
        
        # Vulnerability check
        if rg -q "dependency-check" build.gradle* 2>/dev/null; then
            echo "🔒 Running security vulnerability scan..."
            if ./gradlew dependencyCheckAnalyze >/dev/null 2>&1; then
                echo "✅ Security scan complete"
                echo "   Report: build/reports/dependency-check-report.html"
            else
                echo "⚠️  Security scan failed"
            fi
        else
            echo "ℹ️  OWASP dependency-check not configured"
        fi
        
        jq '.healthStatus.dependencies = "pass"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
        ;;
        
    "maven")
        # Dependency analysis
        if [ "${ARGUMENTS:-quick}" = "detailed" ]; then
            echo "🔄 Analyzing dependencies..."
            if mvn dependency:analyze >/dev/null 2>&1; then
                echo "✅ Dependency analysis complete"
            else
                echo "⚠️  Dependency issues found"
            fi
            
            # Check for updates
            if mvn versions:display-dependency-updates >/dev/null 2>&1; then
                echo "   Run 'mvn versions:display-dependency-updates' for available updates"
            fi
        fi
        
        # Security check
        if mvn dependency-check:check >/dev/null 2>&1; then
            echo "🔒 Security scan complete"
            echo "   Report: target/dependency-check-report.html"
        else
            echo "ℹ️  OWASP dependency-check not configured"
        fi
        
        jq '.healthStatus.dependencies = "pass"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
        ;;
esac
```

STEP 6: Test coverage analysis (detailed mode)

IF check_mode is "detailed":

```bash
echo ""
echo "📊 TEST COVERAGE"
echo "═══════════════"

case "$build_tool" in
    "gradle")
        # JaCoCo coverage
        if rg -q "jacoco" build.gradle* 2>/dev/null; then
            if ./gradlew jacocoTestReport >/dev/null 2>&1; then
                echo "✅ Coverage report generated"
                jq '.healthStatus.coverage = "pass"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
                
                # Try to extract coverage percentage
                if [ -f build/reports/jacoco/test/html/index.html ]; then
                    coverage=$(rg -o "Total.*?([0-9]+%)" build/reports/jacoco/test/html/index.html | rg -o "[0-9]+%" | head -1 || echo "N/A")
                    echo "   Coverage: $coverage"
                    echo "   Report: build/reports/jacoco/test/html/index.html"
                fi
            else
                echo "⚠️  Coverage generation failed"
            fi
        else
            echo "ℹ️  JaCoCo not configured"
        fi
        ;;
        
    "maven")
        # JaCoCo via Maven
        if rg -q "jacoco-maven-plugin" pom.xml 2>/dev/null; then
            if mvn jacoco:report >/dev/null 2>&1; then
                echo "✅ Coverage report generated"
                jq '.healthStatus.coverage = "pass"' /tmp/java-status-$SESSION_ID.json > /tmp/java-status-$SESSION_ID.tmp && mv /tmp/java-status-$SESSION_ID.tmp /tmp/java-status-$SESSION_ID.json
                echo "   Report: target/site/jacoco/index.html"
            else
                echo "⚠️  Coverage generation failed"
            fi
        else
            echo "ℹ️  JaCoCo not configured"
        fi
        ;;
esac
```

STEP 7: Project structure and framework detection

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

# Framework detection
echo ""
echo "🚀 FRAMEWORKS & TECHNOLOGIES"

# Spring Boot
if rg -q "spring-boot" build.gradle* pom.xml 2>/dev/null; then
    echo "✅ Spring Boot detected"
    boot_version=$(rg -o "spring-boot:([0-9]+\.[0-9]+\.[0-9]+)" build.gradle* pom.xml 2>/dev/null | rg -o "[0-9]+\.[0-9]+\.[0-9]+" | head -1 || echo "version unknown")
    echo "   Version: $boot_version"
    [ -f src/main/resources/application.properties ] && echo "   Config: application.properties"
    [ -f src/main/resources/application.yml ] && echo "   Config: application.yml"
fi

# Quarkus
if rg -q "quarkus" build.gradle* pom.xml 2>/dev/null; then
    echo "✅ Quarkus detected"
    quarkus_version=$(rg -o "quarkus.*:([0-9]+\.[0-9]+\.[0-9]+)" build.gradle* pom.xml 2>/dev/null | rg -o "[0-9]+\.[0-9]+\.[0-9]+" | head -1 || echo "version unknown")
    echo "   Version: $quarkus_version"
fi

# Database technologies
echo ""
echo "💾 DATABASE TECHNOLOGIES"
rg -q "jooq" build.gradle* pom.xml 2>/dev/null && echo "✅ jOOQ detected (type-safe SQL)"
rg -q "hibernate|jpa" build.gradle* pom.xml 2>/dev/null && echo "✅ JPA/Hibernate detected"
rg -q "flyway" build.gradle* pom.xml 2>/dev/null && echo "✅ Flyway migrations detected"
rg -q "liquibase" build.gradle* pom.xml 2>/dev/null && echo "✅ Liquibase migrations detected"

# Temporal workflow
if rg -q "temporal" build.gradle* pom.xml 2>/dev/null; then
    echo ""
    echo "⚡ Temporal workflow engine detected"
fi
```

FINALLY: Generate executive summary and recommendations

```bash
echo ""
echo "═══════════════════════════════════════════"
echo "📊 JAVA PROJECT HEALTH SUMMARY"
echo "═══════════════════════════════════════════"
echo "Session: $SESSION_ID"
echo "Build Tool: $(jq -r '.buildTool' /tmp/java-status-$SESSION_ID.json)"
echo "Java Version: $(java -version 2>&1 | head -1 | rg -o "[0-9]+\.[0-9]+\.[0-9]+" || echo "unknown")"
echo ""

# Overall health score
health_data=$(cat /tmp/java-status-$SESSION_ID.json)
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
    echo "✨ Excellent! Your Java project is in great health."
else
    echo "$health_data" | jq -r '.healthStatus | to_entries[] | select(.value != "pass" and .value != "pending") | .key' | while read -r failing_check; do
        case "$failing_check" in
            "build")
                echo "🔧 Fix build errors: check compiler output"
                ;;
            "tests")
                echo "🧪 Fix failing tests: review test reports"
                ;;
            "checkstyle")
                echo "💅 Fix code style violations"
                ;;
            "spotbugs")
                echo "🐛 Address SpotBugs findings"
                ;;
            "dependencies")
                echo "📦 Update dependencies and check vulnerabilities"
                ;;
            "coverage")
                echo "📊 Improve test coverage"
                ;;
        esac
    done
fi

# Build tool specific recommendations
build_tool=$(jq -r '.buildTool' /tmp/java-status-$SESSION_ID.json)
if [ "$build_tool" = "gradle" ] && [ ! -f gradlew ]; then
    echo "🔧 Generate Gradle wrapper: gradle wrapper"
elif [ "$build_tool" = "maven" ] && [ ! -f mvnw ]; then
    echo "🔧 Generate Maven wrapper: mvn wrapper:wrapper"
fi

[ ! -f README.md ] && echo "📝 Add a README.md file"
[ ! -f LICENSE ] && echo "⚖️  Add a LICENSE file"

echo ""
echo "💾 Full report saved to: /tmp/java-status-$SESSION_ID.json"
```

## Quick Reference

### Usage Examples

```bash
# Quick health check (default)
/project-status-java

# Detailed analysis with all checks
/project-status-java detailed

# From a specific project directory
cd my-java-project && /project-status-java
```

### Health Checks Performed

1. **Build Health**: Compilation for Gradle/Maven projects
2. **Test Suite**: Test execution and reporting
3. **Code Quality**: Checkstyle and SpotBugs analysis
4. **Dependencies**: Update checks and vulnerability scanning
5. **Test Coverage**: JaCoCo coverage analysis (detailed mode)
6. **Project Structure**: Best practices and framework detection
7. **Framework Analysis**: Spring Boot, Quarkus, database tools

This command provides comprehensive Java project health monitoring supporting both Gradle and Maven build systems.
