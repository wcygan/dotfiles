---
allowed-tools: Read, Write, Edit, MultiEdit, Bash(fd:*), Bash(rg:*), Bash(jq:*), Bash(git:*), Task
description: Analyze code for refactoring opportunities with intelligent smell detection and incremental improvements
---

## Context

- Session ID: !`gdate +%s%N 2>/dev/null || date +%s000000000 2>/dev/null || echo "session-$(date +%s)000000000"`
- Current directory: !`pwd`
- Target: $ARGUMENTS
- Project structure: !`fd . -t d -d 3 | head -15 || echo "No directory structure detected"`
- Code files: !`fd "\.(java|go|rs|py|ts|js|cpp|c|kt|scala|rb|php|cs|swift)$" . | wc -l | tr -d ' ' || echo "0"`
- Test files: !`fd "(test|spec)" . -t f | wc -l | tr -d ' ' || echo "0"`
- Large files: !`fd "\.(java|go|rs|py|ts|js|cpp|c)$" . -x wc -l {} \; 2>/dev/null | awk '{if($1>500) count++} END {print count+0}' || echo "0"`
- Technology stack: !`fd "(deno\.json|package\.json|Cargo\.toml|go\.mod|pom\.xml|build\.gradle|requirements\.txt|composer\.json)" . | head -5 || echo "No project files detected"`
- Dependencies: !`rg "(import|require|use|include)" . --type java --type go --type rust --type python --type typescript | wc -l | tr -d ' ' || echo "0"`
- Git status: !`git status --porcelain | head -5 || echo "Not a git repository"`
- Current branch: !`git branch --show-current 2>/dev/null || echo "No git repository"`
- Recent commits: !`git log --oneline -3 2>/dev/null || echo "No git history"`

## Your Task

Think deeply about optimal refactoring strategies for this codebase. Consider maintainability, performance, and architectural patterns.

STEP 1: Initialize refactoring session

- CREATE session state file: `/tmp/refactor-analysis-$SESSION_ID.json`
- SET initial state:
  ```json
  {
    "sessionId": "$SESSION_ID",
    "target": "$ARGUMENTS",
    "phase": "discovery",
    "language": "auto-detect",
    "smells": [],
    "refactorings": [],
    "priority_order": [],
    "test_coverage": null,
    "checkpoints": []
  }
  ```

STEP 2: Determine analysis scope and approach

Think harder about the optimal analysis strategy based on codebase complexity and architectural depth.

IF $ARGUMENTS is directory AND contains >100 files:

- USE sub-agent delegation for parallel analysis
- SET scope to "comprehensive"
- CREATE inter-agent communication files: `/tmp/refactor-agents-$SESSION_ID/`
  ELSE IF $ARGUMENTS is single large file (>1000 lines):
- USE extended thinking for complex architectural analysis
- SET scope to "deep"
- ENABLE ultrathink mode for intricate dependency analysis
  ELSE:
- PERFORM focused sequential analysis
- SET scope to "targeted"
- USE extended thinking for critical refactoring decisions

STEP 3: Code smell detection and analysis

FOR comprehensive scope:

- DELEGATE to 5 parallel sub-agents with coordinated analysis:
  1. **Structure Analysis Agent**: Identify architectural issues, large classes/modules
     - SAVE findings to: `/tmp/refactor-agents-$SESSION_ID/structure-analysis.json`
  2. **Duplication Detection Agent**: Find duplicate code blocks and patterns
     - SAVE findings to: `/tmp/refactor-agents-$SESSION_ID/duplication-analysis.json`
  3. **Complexity Analysis Agent**: Analyze cyclomatic complexity and method lengths
     - SAVE findings to: `/tmp/refactor-agents-$SESSION_ID/complexity-analysis.json`
  4. **Type Safety Agent**: Check for language-specific type issues
     - SAVE findings to: `/tmp/refactor-agents-$SESSION_ID/type-safety-analysis.json`
  5. **Performance Analysis Agent**: Identify performance bottlenecks and anti-patterns
     - SAVE findings to: `/tmp/refactor-agents-$SESSION_ID/performance-analysis.json`

- COORDINATE agent findings through main synthesizer after completion

FOR targeted scope:

- EXECUTE sequential analysis:
  - Language detection and context setup
  - Code smell identification
  - Complexity metrics calculation
  - Test coverage assessment

STEP 4: Language-specific smell detection

CASE detected language:
WHEN "java":

- ANALYZE for anemic domain models, god objects
- CHECK excessive static method usage
- IDENTIFY primitive obsession patterns
- REVIEW inheritance vs composition opportunities

WHEN "go":

- SCAN for empty interfaces (interface{})
- CHECK for goroutine leaks and missing error handling
- IDENTIFY package dependency cycles
- REVIEW struct size and method organization

WHEN "rust":

- ANALYZE Rc/RefCell overuse patterns
- CHECK for unnecessary cloning operations
- IDENTIFY missing trait implementations
- REVIEW error handling patterns and unwrap() usage

WHEN "typescript" OR "javascript":

- CHECK for any types and missing type annotations
- IDENTIFY callback hell and promise chain issues
- ANALYZE component complexity and props drilling
- REVIEW async/await patterns

WHEN "python":

- ANALYZE class hierarchy and multiple inheritance
- CHECK for missing type hints and docstrings
- IDENTIFY list comprehension overuse
- REVIEW exception handling patterns

STEP 5: Test coverage verification

TRY:

- EXECUTE language-specific coverage commands:
  - Java: `mvn test jacoco:report` OR `gradle test jacocoTestReport`
  - Go: `go test -cover ./...`
  - Rust: `cargo tarpaulin --out xml` OR `cargo test`
  - TypeScript: `npm test -- --coverage` OR `deno test --coverage`
  - Python: `pytest --cov=src --cov-report=xml`
- PARSE coverage reports for critical path analysis
- IDENTIFY untested code areas requiring attention
  CATCH (coverage_tool_missing):
- DOCUMENT coverage tool setup requirements
- SUGGEST manual test verification approach
- PROCEED with refactoring analysis

STEP 6: Refactoring priority analysis

- CALCULATE impact scores for each identified smell:
  - Maintainability impact (1-10)
  - Performance impact (1-10)
  - Security risk (1-10)
  - Refactoring difficulty (1-10)
- SORT by priority: (maintainability + performance + security) / difficulty
- GROUP by risk level: high, medium, low
- CREATE incremental refactoring plan

STEP 7: Generate refactoring recommendations

FOR EACH high-priority smell:

- DESCRIBE specific refactoring technique
- PROVIDE code examples (before/after)
- ESTIMATE effort and risk
- SUGGEST testing strategy
- DOCUMENT rollback plan

STEP 8: State management and progress tracking

- UPDATE session state with analysis results
- SAVE refactoring plan to `/tmp/refactor-plan-$SESSION_ID.md`
- CREATE checkpoint before each major refactoring
- TRACK test execution results and coverage changes

## Sub-Agent Delegation Pattern

FOR large codebases (>100 files), delegate to parallel agents:

### Structure Analysis Agent

- Map class/module hierarchy and dependencies
- Identify god objects and feature envy patterns
- Analyze package/namespace organization
- Detect architectural violations and cyclic dependencies

### Duplication Detection Agent

- Find exact and near-duplicate code blocks
- Identify copy-paste patterns across files
- Analyze similar method signatures and implementations
- Suggest extraction opportunities for common code

### Complexity Analysis Agent

- Calculate cyclomatic complexity for all methods/functions
- Identify deeply nested control structures
- Analyze method parameter counts and return complexity
- Find long methods and large classes requiring decomposition

### Type Safety Agent

- Check for missing type annotations and weak typing
- Identify null pointer and undefined access risks
- Analyze generic usage and type parameter consistency
- Review error handling and exception safety patterns

### Performance Analysis Agent

- Identify inefficient algorithms and data structures
- Find memory leaks and resource management issues
- Analyze database query patterns and N+1 problems
- Check for premature optimization opportunities

## Language-Specific Refactoring Patterns

### Java Refactoring Techniques

**Anemic Domain Model → Rich Domain Model**

```java
// Before: Anemic model
public class Customer {
    private String name;
    private String email;
    // Only getters/setters
}

public class CustomerService {
    public boolean isEligibleForDiscount(Customer customer) {
        // Business logic here
    }
}

// After: Rich domain model
public class Customer {
    private String name;
    private Email email;
    
    public boolean isEligibleForDiscount() {
        // Business logic moved to domain
        return this.getTotalOrders() > 10;
    }
}
```

**Replace Conditional with Strategy Pattern**

```java
// Before: Complex conditionals
public class PaymentProcessor {
    public void processPayment(PaymentType type, double amount) {
        if (type == PaymentType.CREDIT_CARD) {
            // Credit card logic
        } else if (type == PaymentType.PAYPAL) {
            // PayPal logic
        } else if (type == PaymentType.BANK_TRANSFER) {
            // Bank transfer logic
        }
    }
}

// After: Strategy pattern
public interface PaymentStrategy {
    void processPayment(double amount);
}

public class PaymentProcessor {
    private PaymentStrategy strategy;
    
    public void processPayment(double amount) {
        strategy.processPayment(amount);
    }
}
```

### Go Refactoring Techniques

**Replace Empty Interface with Type-Safe Alternatives**

```go
// Before: Empty interface
func ProcessData(data interface{}) error {
    switch v := data.(type) {
    case string:
        // Handle string
    case int:
        // Handle int
    default:
        return fmt.Errorf("unsupported type")
    }
    return nil
}

// After: Type-safe approach
type DataProcessor interface {
    Process() error
}

func ProcessData(processor DataProcessor) error {
    return processor.Process()
}
```

**Functional Options Pattern**

```go
// Before: Many constructor parameters
func NewServer(host string, port int, timeout time.Duration, 
               ssl bool, cert string) *Server {
    // Constructor logic
}

// After: Functional options
type ServerOption func(*Server)

func WithSSL(cert string) ServerOption {
    return func(s *Server) {
        s.ssl = true
        s.cert = cert
    }
}

func NewServer(host string, port int, opts ...ServerOption) *Server {
    s := &Server{host: host, port: port}
    for _, opt := range opts {
        opt(s)
    }
    return s
}
```

### Rust Refactoring Techniques

**Replace Rc/RefCell with Better Ownership**

```rust
// Before: Overuse of Rc/RefCell
use std::rc::Rc;
use std::cell::RefCell;

struct Node {
    value: i32,
    children: Vec<Rc<RefCell<Node>>>,
}

// After: Arena-based approach
struct Arena {
    nodes: Vec<Node>,
}

struct Node {
    value: i32,
    children: Vec<usize>, // Indices into arena
}
```

**Iterator-based Refactoring**

```rust
// Before: Manual loops
let mut result = Vec::new();
for item in items {
    if item.is_valid() {
        result.push(item.transform());
    }
}

// After: Iterator chains
let result: Vec<_> = items
    .into_iter()
    .filter(|item| item.is_valid())
    .map(|item| item.transform())
    .collect();
```

## Incremental Refactoring Workflow

STEP 9: Execute refactoring plan

FOR EACH refactoring in priority order:

CHECKPOINT before_refactoring:

- CREATE branch: `refactor/$REFACTORING_NAME-$SESSION_ID`
- SAVE current state and test results
- DOCUMENT rollback procedure

TRY:

- APPLY single refactoring change
- RUN relevant tests:
- Java: `mvn test -Dtest=*${ModifiedClass}*`
- Go: `go test ./... -run TestRelated`
- Rust: `cargo test related_tests`
- VERIFY no regressions introduced
- UPDATE documentation if needed

CATCH (test_failure):

- ROLLBACK to checkpoint
- ANALYZE failure root cause
- ADJUST refactoring approach
- RETRY with smaller incremental change

CATCH (compilation_error):

- FIX compilation issues immediately
- VERIFY type safety and interfaces
- ENSURE all dependencies resolved

SUCCESS:

- COMMIT with descriptive message
- UPDATE session state with completion
- MEASURE performance impact if applicable
- PROCEED to next refactoring

STEP 10: Validation and quality gates

- RUN full test suite: `$LANGUAGE_SPECIFIC_TEST_COMMAND`
- EXECUTE static analysis tools:
  - Java: `mvn spotbugs:check pmd:check`
  - Go: `golangci-lint run ./...`
  - Rust: `cargo clippy -- -D warnings`
  - TypeScript: `npm run lint`
- VERIFY performance benchmarks
- CHECK code coverage maintenance or improvement
- VALIDATE architectural consistency

FINALLY:

- UPDATE session state with final results
- GENERATE refactoring summary report
- CLEAN UP temporary files: `/tmp/refactor-*-$SESSION_ID.*`
- ARCHIVE session artifacts for future reference

## Output Artifacts

GENERATE the following deliverables:

**1. Refactoring Analysis Report** (`/refactor-analysis-$SESSION_ID.md`)

- Code smell inventory with severity rankings
- Language-specific anti-pattern analysis
- Refactoring recommendations with effort estimates
- Risk assessment and mitigation strategies

**2. Incremental Refactoring Plan** (`/refactor-plan-$SESSION_ID.md`)

- Priority-ordered refactoring tasks
- Step-by-step implementation guide
- Testing strategy for each refactoring
- Rollback procedures and checkpoints

**3. Improved Code** (modified source files)

- Refactored code with improved structure
- Enhanced readability and maintainability
- Preserved or improved test coverage
- Updated documentation and comments

**4. Quality Metrics** (`/refactor-metrics-$SESSION_ID.json`)

- Before/after complexity measurements
- Test coverage comparison
- Performance benchmark results
- Static analysis improvement scores

The refactoring process adapts to the detected programming language, project structure, and existing toolchain, providing targeted improvements that enhance code quality while maintaining functionality and test coverage.

## Session State Management Schema

**State Files Created:**

- `/tmp/refactor-analysis-$SESSION_ID.json` - Main refactoring session state
- `/tmp/refactor-plan-$SESSION_ID.md` - Incremental refactoring plan
- `/tmp/refactor-metrics-$SESSION_ID.json` - Quality metrics and measurements
- `/tmp/refactor-agents-$SESSION_ID/` - Inter-agent communication directory
  - `structure-analysis.json` - Architectural findings
  - `duplication-analysis.json` - Code duplication results
  - `complexity-analysis.json` - Complexity metrics and hotspots
  - `type-safety-analysis.json` - Type safety analysis results
  - `performance-analysis.json` - Performance bottleneck findings

**Enhanced State Schema:**

```json
{
  "sessionId": "$SESSION_ID",
  "timestamp": "ISO_8601_TIMESTAMP",
  "target": "$ARGUMENTS",
  "phase": "discovery|analysis|planning|refactoring|validation|complete",
  "scope": "targeted|deep|comprehensive",
  "language": "auto-detected_language",
  "project_info": {
    "total_files": "number",
    "large_files_count": "number",
    "test_coverage": "percentage",
    "dependency_count": "number",
    "git_status": "clean|dirty|not_repo"
  },
  "smells": [
    {
      "type": "god_class|duplicate_code|complex_method|type_safety|performance",
      "severity": "low|medium|high|critical",
      "location": "file_path:line_number",
      "description": "specific_issue_description",
      "impact_score": "calculated_priority_score",
      "refactoring_technique": "recommended_approach",
      "effort_estimate": "low|medium|high",
      "risk_level": "low|medium|high"
    }
  ],
  "refactorings": [
    {
      "id": "unique_refactoring_id",
      "priority": "high|medium|low",
      "status": "pending|in_progress|completed|failed",
      "technique": "extract_method|replace_conditional|strategy_pattern",
      "target_files": ["list_of_files"],
      "estimated_effort": "hours_or_story_points",
      "actual_effort": "time_taken",
      "rollback_commit": "git_commit_hash",
      "test_impact": "tests_affected_count",
      "performance_impact": "before_after_metrics"
    }
  ],
  "priority_order": ["ordered_refactoring_ids"],
  "checkpoints": [
    {
      "checkpoint_id": "unique_identifier",
      "timestamp": "ISO_8601_TIMESTAMP",
      "git_commit": "commit_hash",
      "test_status": "all_passing|some_failing|not_run",
      "files_modified": ["list_of_modified_files"],
      "rollback_procedure": "steps_to_undo_changes"
    }
  ],
  "metrics": {
    "before": {
      "cyclomatic_complexity": "average_complexity",
      "test_coverage": "percentage",
      "code_duplication": "percentage",
      "lines_of_code": "total_loc",
      "technical_debt_hours": "estimated_hours"
    },
    "after": {
      "cyclomatic_complexity": "improved_complexity",
      "test_coverage": "maintained_or_improved",
      "code_duplication": "reduced_percentage",
      "lines_of_code": "refactored_loc",
      "technical_debt_hours": "reduced_hours"
    },
    "improvement_percentage": "calculated_improvement"
  },
  "sub_agent_coordination": {
    "agents_used": ["structure", "duplication", "complexity", "type_safety", "performance"],
    "communication_files": ["/tmp/paths/to/agent/outputs"],
    "synthesis_complete": "boolean",
    "cross_cutting_concerns": ["shared_issues_across_agents"]
  }
}
```

**Resumability Features:**

- Checkpoint-based recovery from any point in refactoring workflow
- Individual refactoring rollback without affecting completed work
- Sub-agent result preservation across session interruptions
- Git branch and commit tracking for safe experimental refactoring
- State validation and consistency checks before each major operation

**Advanced Features:**

- **Cross-Platform Session IDs**: Fallback `date` commands for non-GNU systems
- **Inter-Agent Communication**: Structured JSON files for agent coordination
- **Extended Thinking Integration**: Automatic thinking mode escalation for complex scenarios
- **Quality Gate Validation**: Automated testing and static analysis after each refactoring
- **Incremental Progress Tracking**: Granular checkpoint system with rollback capabilities
