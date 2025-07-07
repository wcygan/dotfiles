---
allowed-tools: Read, Write, Bash(fd:*), Bash(rg:*), Bash(git:*), Bash(gdate:*), Bash(jq:*), Bash(wc:*), Task, WebFetch
description: Generate comprehensive technical analysis and implementation guide with adaptive research and project-specific optimization
---

## Context

- Session ID: !`gdate +%s%N`
- Current directory: !`pwd`
- Analysis target: $ARGUMENTS
- Project structure: !`fd . -t d -d 3 | head -15 || echo "No directories found"`
- Code files: !`fd "\.(rs|go|java|py|js|ts|cpp|c|kt|scala|rb|php|cs|swift)$" . | wc -l | tr -d ' ' || echo "0"`
- Configuration files: !`fd "(package\.json|Cargo\.toml|go\.mod|pom\.xml|deno\.json|requirements\.txt|composer\.json|build\.gradle)$" . -d 3 || echo "No config files"`
- Documentation: !`fd "(README|CHANGELOG|CONTRIBUTING|LICENSE)\.md$" . -d 2 | head -5 || echo "No docs found"`
- Test files: !`fd "(test|spec)" . -t f | wc -l | tr -d ' ' || echo "0"`
- Git repository: !`git rev-parse --is-inside-work-tree 2>/dev/null && echo "Yes" || echo "No"`
- Recent changes: !`git log --oneline -5 2>/dev/null || echo "No git repository"`
- Branch status: !`git status --porcelain 2>/dev/null | wc -l | tr -d ' ' | xargs -I {} echo "{} uncommitted files" || echo "N/A"`
- Technology stack indicators: !`rg "(import|require|use|include|from)" . --type rust --type go --type java --type python --type typescript | head -10 | cut -d: -f3 | sort -u | head -5 || echo "No imports detected"`

## Your Task

STEP 1: Initialize comprehensive analysis session

- CREATE session state file: `/tmp/elaborate-analysis-$SESSION_ID.json`
- SET initial state:
  ```json
  {
    "sessionId": "$SESSION_ID",
    "target": "$ARGUMENTS",
    "phase": "initialization",
    "technology_stack": "auto-detect",
    "complexity_level": "unknown",
    "analysis_domains": [],
    "research_findings": {},
    "implementation_phases": [],
    "artifacts_created": [],
    "checkpoints": []
  }
  ```
- CREATE analysis workspace: `/tmp/elaborate-analysis-$SESSION_ID/`
- INITIALIZE project context analysis and technology detection

STEP 2: Project-specific context analysis and technology detection

Think deeply about the optimal analysis strategy based on the detected project characteristics and technology stack.

- ANALYZE project structure from Context section
- DETERMINE primary technology stack and architectural patterns
- IDENTIFY analysis scope and complexity requirements
- ASSESS documentation and testing maturity level

IF Code files > 100 AND multiple technology stacks detected:

- SET complexity_level = "enterprise"
- ENABLE multi-domain parallel analysis with sub-agents
- FOCUS on system integration, scalability, and architectural patterns
  ELSE IF Code files > 20 AND single technology stack:
- SET complexity_level = "moderate"
- USE focused single-domain analysis with extended thinking
- PRIORITIZE implementation patterns and best practices
  ELSE:
- SET complexity_level = "simple"
- PROCEED with straightforward analysis and concrete examples
- EMPHASIZE getting-started guides and foundational patterns

STEP 3: Adaptive research strategy execution

TRY:

IF complexity_level == "enterprise":

- USE Task tool to delegate comprehensive parallel research:
  1. **Architecture Analysis Agent**: System design patterns, microservices, scalability
     - SAVE findings to: `/tmp/elaborate-analysis-$SESSION_ID/architecture-research.json`
  2. **Implementation Strategy Agent**: Technology-specific best practices, frameworks, tooling
     - SAVE findings to: `/tmp/elaborate-analysis-$SESSION_ID/implementation-research.json`
  3. **Testing & Quality Agent**: Testing frameworks, CI/CD, quality gates, performance
     - SAVE findings to: `/tmp/elaborate-analysis-$SESSION_ID/testing-research.json`
  4. **DevOps & Deployment Agent**: Infrastructure, monitoring, deployment strategies
     - SAVE findings to: `/tmp/elaborate-analysis-$SESSION_ID/devops-research.json`
  5. **Risk & Alternatives Agent**: Technical debt, security, alternative approaches
     - SAVE findings to: `/tmp/elaborate-analysis-$SESSION_ID/risk-research.json`

- COORDINATE findings through main synthesizer after sub-agent completion

ELSE IF complexity_level == "moderate":

- EXECUTE focused research with extended thinking:
  - Think harder about technology-specific implementation patterns and architectural decisions
  - RESEARCH current best practices for detected technology stack
  - IDENTIFY common pitfalls and optimization opportunities
  - DOCUMENT proven patterns and anti-patterns

ELSE:

- PERFORM streamlined analysis:
  - FOCUS on essential implementation guidance
  - PRIORITIZE getting-started examples and basic patterns
  - INCLUDE fundamental best practices and common workflows

CATCH (research_source_unavailable):

- LOG unavailable sources to session state
- CONTINUE with available information and internal knowledge
- PROVIDE manual research recommendations for missing sources
- SAVE fallback guidance and alternative reference materials

STEP 4: Technology-specific implementation guidance

CASE detected_technology:
WHEN "rust":

- ANALYZE Cargo.toml dependencies and feature flags
- FOCUS on ownership patterns, error handling, async programming
- INCLUDE performance optimization and memory safety examples
- DOCUMENT testing with cargo test and integration patterns

WHEN "go":

- ANALYZE go.mod dependencies and module structure
- FOCUS on concurrency patterns, error handling, interfaces
- INCLUDE deployment strategies and performance tuning
- DOCUMENT testing patterns and benchmarking approaches

WHEN "java":

- ANALYZE build configuration (Maven/Gradle) and dependencies
- FOCUS on design patterns, Spring ecosystem, JVM optimization
- INCLUDE enterprise patterns and testing strategies
- DOCUMENT deployment and monitoring for production systems

WHEN "typescript" OR "javascript":

- ANALYZE package.json dependencies and build tools
- FOCUS on modern ES features, async patterns, type safety
- INCLUDE framework-specific guidance (React, Vue, Node.js)
- DOCUMENT testing strategies and bundle optimization

WHEN "python":

- ANALYZE requirements and project structure
- FOCUS on package management, virtual environments, async patterns
- INCLUDE framework-specific guidance (Django, FastAPI, Flask)
- DOCUMENT testing and deployment best practices

WHEN "multiple" OR "unknown":

- PROVIDE polyglot development guidance
- FOCUS on language-agnostic architectural patterns
- INCLUDE integration strategies between technologies
- DOCUMENT cross-language communication and shared tooling

STEP 5: Comprehensive analysis synthesis and artifact generation

- ORGANIZE research findings by implementation priority:
  - Foundation and setup requirements
  - Core implementation patterns and examples
  - Advanced features and optimization strategies
  - Testing, deployment, and monitoring approaches
  - Maintenance and evolution considerations

- SYNTHESIZE project-specific recommendations:
  - Integration with existing codebase patterns
  - Adaptation strategies for detected architecture
  - Performance considerations for current scale
  - Security requirements and compliance patterns

STEP 6: Multi-phase implementation roadmap creation

- GENERATE realistic implementation phases:
  ```json
  {
    "phase_1": {
      "name": "Foundation Setup",
      "duration": "1-2 weeks",
      "deliverables": ["Basic structure", "Core dependencies", "Initial tests"],
      "success_criteria": ["Build succeeds", "Basic functionality works"],
      "risks": ["Dependency conflicts", "Environment setup issues"]
    },
    "phase_2": {
      "name": "Core Implementation",
      "duration": "3-4 weeks",
      "deliverables": ["Main features", "Integration points", "Comprehensive tests"],
      "success_criteria": ["Feature complete", "Tests pass", "Documentation current"],
      "risks": ["Performance issues", "Integration complexity"]
    },
    "phase_3": {
      "name": "Production Readiness",
      "duration": "1-2 weeks",
      "deliverables": ["Monitoring", "Deployment automation", "Performance optimization"],
      "success_criteria": ["Production deployed", "Monitoring active", "Performance acceptable"],
      "risks": ["Deployment issues", "Performance degradation"]
    }
  }
  ```

STEP 7: State management and artifact creation

- UPDATE session state with analysis results and recommendations
- CREATE comprehensive analysis guide: `/tmp/elaborate-analysis-$SESSION_ID/comprehensive-guide.md`
- GENERATE implementation checklist: `/tmp/elaborate-analysis-$SESSION_ID/implementation-checklist.md`
- SAVE technology-specific examples: `/tmp/elaborate-analysis-$SESSION_ID/code-examples/`
- CREATE deployment guide: `/tmp/elaborate-analysis-$SESSION_ID/deployment-guide.md`
- DOCUMENT architectural decisions: `/tmp/elaborate-analysis-$SESSION_ID/architecture-decisions.md`

STEP 8: Advanced analysis enhancement for complex scenarios

IF complexity_level == "enterprise" AND multiple sub-agents used:

- COORDINATE cross-domain analysis synthesis
- IDENTIFY integration points and potential conflicts between recommendations
- GENERATE enterprise-specific guidance:
  - Governance and compliance considerations
  - Team coordination and knowledge sharing strategies
  - Risk mitigation and rollback procedures
  - Performance monitoring and optimization at scale

STEP 9: Quality assurance and validation

TRY:

- VALIDATE generated code examples for syntax correctness
- VERIFY recommended dependencies are current and secure
- CHECK implementation roadmap for realistic timelines
- ENSURE documentation completeness and clarity

CATCH (validation_failed):

- LOG validation issues to session state
- PROVIDE corrected examples and recommendations
- INCLUDE troubleshooting guidance for common issues

FINALLY:

- UPDATE session state: phase = "complete"
- GENERATE comprehensive analysis summary with key recommendations
- ARCHIVE session artifacts for future reference
- CLEAN UP temporary processing files: `/tmp/elaborate-temp-$SESSION_ID-*`

## Analysis Framework

### Core Sections (generated programmatically based on complexity level)

CASE complexity_level:
WHEN "enterprise":

1. **Executive Summary** (2-3 sentences with business impact)
2. **System Architecture** (microservices, data flow, integration patterns)
3. **Technology Selection Matrix** (comparison with justification)
4. **Implementation Phases** (4-6 phases with dependencies)
5. **Code Examples & Patterns** (5+ examples with enterprise considerations)
6. **Integration Strategy** (APIs, event sourcing, data consistency)
7. **Testing Framework** (unit, integration, performance, chaos)
8. **Security & Compliance** (authentication, authorization, data protection)
9. **DevOps & Deployment** (CI/CD, infrastructure as code, monitoring)
10. **Risk Assessment** (technical, operational, business risks)
11. **Alternative Architectures** (3+ variations with trade-off analysis)
12. **Production Considerations** (scaling, monitoring, incident response)
13. **Governance & Standards** (code quality, documentation, knowledge sharing)
14. **Resource Library** (architecture docs, tools, training materials)

WHEN "moderate":

1. **Executive Summary** (2-3 sentences with technical focus)
2. **Technical Architecture** (components, data flow, technology stack)
3. **Implementation Phases** (3-4 phases with realistic timelines)
4. **Code Examples** (3-4 concrete implementations with best practices)
5. **Integration Strategy** (APIs, dependencies, data management)
6. **Testing Approach** (unit, integration, performance testing)
7. **Risk Assessment** (technical and operational risks)
8. **Alternative Approaches** (2-3 variations with trade-offs)
9. **Production Considerations** (deployment, monitoring, maintenance)
10. **Resource Library** (documentation, tools, learning resources)

WHEN "simple":

1. **Project Overview** (clear problem statement and solution approach)
2. **Technology Stack** (chosen technologies with rationale)
3. **Implementation Plan** (2-3 phases with step-by-step guidance)
4. **Code Examples** (2-3 working examples with explanations)
5. **Setup Guide** (environment setup and dependency management)
6. **Testing Strategy** (basic testing approach and tools)
7. **Deployment Guide** (simple deployment instructions)
8. **Next Steps** (future enhancements and learning resources)

### Comprehensive Code Examples by Technology

**Rust Implementation Patterns:**

```rust
// Advanced error handling with custom error types
use thiserror::Error;
use serde::{Deserialize, Serialize};

#[derive(Error, Debug)]
pub enum AnalysisError {
    #[error("Invalid input: {message}")]
    InvalidInput { message: String },
    #[error("Processing failed: {source}")]
    ProcessingError { 
        #[from] 
        source: Box<dyn std::error::Error + Send + Sync> 
    },
    #[error("Resource not found: {resource}")]
    NotFound { resource: String },
}

#[derive(Debug, Serialize, Deserialize)]
pub struct AnalysisResult {
    pub success: bool,
    pub data: Option<serde_json::Value>,
    pub metrics: AnalysisMetrics,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct AnalysisMetrics {
    pub processing_time_ms: u64,
    pub memory_usage_kb: u64,
    pub items_processed: usize,
}

// Async processing with proper error handling
pub async fn process_analysis_request(
    input: &str,
) -> Result<AnalysisResult, AnalysisError> {
    let start_time = std::time::Instant::now();
    
    // Validate input
    if input.is_empty() {
        return Err(AnalysisError::InvalidInput {
            message: "Input cannot be empty".to_string(),
        });
    }
    
    // Process with timeout
    let result = tokio::time::timeout(
        std::time::Duration::from_secs(30),
        async {
            // Simulated async processing
            tokio::time::sleep(std::time::Duration::from_millis(100)).await;
            serde_json::json!({
                "analysis": "comprehensive",
                "confidence": 0.95,
                "recommendations": ["optimize", "refactor", "test"]
            })
        }
    ).await
    .map_err(|_| AnalysisError::ProcessingError {
        source: "Timeout during processing".into(),
    })?;
    
    let metrics = AnalysisMetrics {
        processing_time_ms: start_time.elapsed().as_millis() as u64,
        memory_usage_kb: 0, // Would be calculated in real implementation
        items_processed: 1,
    };
    
    Ok(AnalysisResult {
        success: true,
        data: Some(result),
        metrics,
    })
}

// Testing patterns with mock and async
#[cfg(test)]
mod tests {
    use super::*;
    use tokio;
    
    #[tokio::test]
    async fn test_successful_analysis() {
        let result = process_analysis_request("valid input").await;
        assert!(result.is_ok());
        
        let analysis = result.unwrap();
        assert!(analysis.success);
        assert!(analysis.data.is_some());
    }
    
    #[tokio::test]
    async fn test_empty_input_error() {
        let result = process_analysis_request("").await;
        assert!(result.is_err());
        
        match result.unwrap_err() {
            AnalysisError::InvalidInput { message } => {
                assert_eq!(message, "Input cannot be empty");
            },
            _ => panic!("Expected InvalidInput error"),
        }
    }
}
```

**Go Implementation Patterns:**

```go
// Enterprise-grade Go implementation with proper error handling
package analysis

import (
    "context"
    "encoding/json"
    "fmt"
    "log/slog"
    "time"
    
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promauto"
)

// Custom error types with proper wrapping
type AnalysisError struct {
    Code    string `json:"code"`
    Message string `json:"message"`
    Cause   error  `json:"-"`
}

func (e *AnalysisError) Error() string {
    if e.Cause != nil {
        return fmt.Sprintf("%s: %s (caused by: %v)", e.Code, e.Message, e.Cause)
    }
    return fmt.Sprintf("%s: %s", e.Code, e.Message)
}

func (e *AnalysisError) Unwrap() error {
    return e.Cause
}

// Metrics for observability
var (
    analysisRequests = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "analysis_requests_total",
            Help: "Total number of analysis requests",
        },
        []string{"status"},
    )
    
    analysisDuration = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name: "analysis_duration_seconds",
            Help: "Duration of analysis requests",
        },
        []string{"type"},
    )
)

// Service interface for dependency injection
type AnalysisService interface {
    ProcessRequest(ctx context.Context, req *AnalysisRequest) (*AnalysisResult, error)
}

type analysisService struct {
    logger   *slog.Logger
    timeout  time.Duration
    maxItems int
}

// Constructor with options pattern
type ServiceOption func(*analysisService)

func WithTimeout(timeout time.Duration) ServiceOption {
    return func(s *analysisService) {
        s.timeout = timeout
    }
}

func WithMaxItems(max int) ServiceOption {
    return func(s *analysisService) {
        s.maxItems = max
    }
}

func NewAnalysisService(logger *slog.Logger, opts ...ServiceOption) AnalysisService {
    s := &analysisService{
        logger:   logger,
        timeout:  30 * time.Second,
        maxItems: 1000,
    }
    
    for _, opt := range opts {
        opt(s)
    }
    
    return s
}

// Request and response types
type AnalysisRequest struct {
    Input string            `json:"input" validate:"required,min=1"`
    Type  string            `json:"type" validate:"required,oneof=quick detailed comprehensive"`
    Meta  map[string]string `json:"meta,omitempty"`
}

type AnalysisResult struct {
    Success bool                   `json:"success"`
    Data    map[string]interface{} `json:"data,omitempty"`
    Metrics AnalysisMetrics        `json:"metrics"`
    Error   string                 `json:"error,omitempty"`
}

type AnalysisMetrics struct {
    ProcessingTimeMs int64 `json:"processing_time_ms"`
    MemoryUsageKB   int64 `json:"memory_usage_kb"`
    ItemsProcessed  int   `json:"items_processed"`
}

// Main processing method with proper error handling and observability
func (s *analysisService) ProcessRequest(ctx context.Context, req *AnalysisRequest) (*AnalysisResult, error) {
    start := time.Now()
    defer func() {
        analysisDuration.WithLabelValues(req.Type).Observe(time.Since(start).Seconds())
    }()
    
    s.logger.Info("Processing analysis request",
        slog.String("type", req.Type),
        slog.String("input_length", fmt.Sprintf("%d", len(req.Input))))
    
    // Validate input
    if req.Input == "" {
        err := &AnalysisError{
            Code:    "INVALID_INPUT",
            Message: "Input cannot be empty",
        }
        analysisRequests.WithLabelValues("error").Inc()
        return nil, err
    }
    
    // Create timeout context
    timeoutCtx, cancel := context.WithTimeout(ctx, s.timeout)
    defer cancel()
    
    // Process with proper cancellation handling
    resultChan := make(chan *AnalysisResult, 1)
    errorChan := make(chan error, 1)
    
    go func() {
        result, err := s.processAnalysis(timeoutCtx, req)
        if err != nil {
            errorChan <- err
            return
        }
        resultChan <- result
    }()
    
    select {
    case result := <-resultChan:
        analysisRequests.WithLabelValues("success").Inc()
        s.logger.Info("Analysis completed successfully",
            slog.Duration("duration", time.Since(start)))
        return result, nil
        
    case err := <-errorChan:
        analysisRequests.WithLabelValues("error").Inc()
        s.logger.Error("Analysis failed",
            slog.String("error", err.Error()),
            slog.Duration("duration", time.Since(start)))
        return nil, err
        
    case <-timeoutCtx.Done():
        err := &AnalysisError{
            Code:    "TIMEOUT",
            Message: fmt.Sprintf("Analysis timed out after %v", s.timeout),
            Cause:   timeoutCtx.Err(),
        }
        analysisRequests.WithLabelValues("timeout").Inc()
        return nil, err
    }
}

func (s *analysisService) processAnalysis(ctx context.Context, req *AnalysisRequest) (*AnalysisResult, error) {
    // Simulate processing time
    select {
    case <-time.After(100 * time.Millisecond):
        // Processing completed
    case <-ctx.Done():
        return nil, ctx.Err()
    }
    
    data := map[string]interface{}{
        "analysis_type": req.Type,
        "confidence":    0.95,
        "recommendations": []string{
            "optimize performance",
            "add monitoring",
            "improve error handling",
        },
    }
    
    return &AnalysisResult{
        Success: true,
        Data:    data,
        Metrics: AnalysisMetrics{
            ProcessingTimeMs: 100,
            MemoryUsageKB:   512,
            ItemsProcessed:  1,
        },
    }, nil
}

// Testing patterns with testify
package analysis_test

import (
    "context"
    "log/slog"
    "testing"
    "time"
    
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestAnalysisService_ProcessRequest_Success(t *testing.T) {
    logger := slog.Default()
    service := NewAnalysisService(logger, WithTimeout(5*time.Second))
    
    req := &AnalysisRequest{
        Input: "test input",
        Type:  "quick",
    }
    
    result, err := service.ProcessRequest(context.Background(), req)
    
    require.NoError(t, err)
    assert.True(t, result.Success)
    assert.NotNil(t, result.Data)
    assert.Greater(t, result.Metrics.ProcessingTimeMs, int64(0))
}

func TestAnalysisService_ProcessRequest_EmptyInput(t *testing.T) {
    logger := slog.Default()
    service := NewAnalysisService(logger)
    
    req := &AnalysisRequest{
        Input: "",
        Type:  "quick",
    }
    
    result, err := service.ProcessRequest(context.Background(), req)
    
    require.Error(t, err)
    assert.Nil(t, result)
    
    var analysisErr *AnalysisError
    require.ErrorAs(t, err, &analysisErr)
    assert.Equal(t, "INVALID_INPUT", analysisErr.Code)
}

func TestAnalysisService_ProcessRequest_Timeout(t *testing.T) {
    logger := slog.Default()
    service := NewAnalysisService(logger, WithTimeout(1*time.Millisecond))
    
    req := &AnalysisRequest{
        Input: "test input",
        Type:  "comprehensive", // This would take longer
    }
    
    result, err := service.ProcessRequest(context.Background(), req)
    
    require.Error(t, err)
    assert.Nil(t, result)
    
    var analysisErr *AnalysisError
    require.ErrorAs(t, err, &analysisErr)
    assert.Equal(t, "TIMEOUT", analysisErr.Code)
}
```

### Enhanced Quality Standards

**Code Quality Requirements:**

- ALL code examples must compile and run without errors
- Include comprehensive error handling with custom error types
- Implement proper logging and observability patterns
- Use dependency injection and testable architectures
- Include both unit and integration test examples
- Follow language-specific best practices and idioms
- Document all public APIs and complex business logic

**Documentation Standards:**

- Provide context and rationale for architectural decisions
- Include setup instructions with version requirements
- Document environment variables and configuration options
- Explain trade-offs between different implementation approaches
- Include troubleshooting guides for common issues
- Reference official documentation and authoritative sources

**Security Considerations:**

- Input validation and sanitization patterns
- Authentication and authorization examples
- Secure configuration management
- Data protection and privacy compliance
- Security testing and vulnerability scanning
- Incident response and monitoring procedures

### Extended Thinking Integration

**For Enterprise Architecture Decisions:**

Think deeply about enterprise-specific requirements:

- Multi-team coordination and knowledge sharing strategies
- Governance models and compliance frameworks
- Risk assessment across technical, operational, and business dimensions
- Performance and scalability requirements under load
- Integration patterns with existing enterprise systems
- Change management and rollback procedures

**For Technology Selection:**

Think harder about technology evaluation criteria:

- Technical debt implications and migration paths
- Team expertise and learning curve considerations
- Ecosystem maturity and long-term viability
- Performance characteristics under different workloads
- Security model and compliance requirements
- Community support and vendor relationship factors

**For Implementation Planning:**

Consider multiple implementation approaches:

- Incremental vs. big-bang deployment strategies
- Feature flags and progressive rollout mechanisms
- A/B testing and experimentation frameworks
- Monitoring and observability from day one
- Disaster recovery and business continuity planning
- Cost optimization and resource management strategies

### Session State Management Schema

**Enhanced State File Structure:**

```json
{
  "sessionId": "$SESSION_ID",
  "timestamp": "ISO_8601_TIMESTAMP",
  "target": "$ARGUMENTS",
  "phase": "initialization|research|analysis|synthesis|validation|complete",
  "technology_stack": {
    "primary": "rust|go|java|typescript|python|multiple",
    "secondary": ["frameworks", "libraries", "tools"],
    "confidence": "high|medium|low"
  },
  "complexity_level": "simple|moderate|enterprise",
  "analysis_domains": [
    "architecture",
    "implementation",
    "testing",
    "devops",
    "security"
  ],
  "research_findings": {
    "architecture": { "confidence": 0.95, "sources": 3, "key_patterns": [] },
    "implementation": { "confidence": 0.90, "sources": 5, "examples": [] },
    "testing": { "confidence": 0.85, "sources": 2, "frameworks": [] }
  },
  "implementation_phases": {
    "total_estimated_weeks": 6,
    "phases": [
      {
        "name": "Foundation Setup",
        "duration_weeks": 2,
        "confidence": "high",
        "dependencies": [],
        "risks": ["low"]
      }
    ]
  },
  "artifacts_created": [
    "/tmp/elaborate-analysis-$SESSION_ID/comprehensive-guide.md",
    "/tmp/elaborate-analysis-$SESSION_ID/implementation-checklist.md"
  ],
  "checkpoints": [
    {
      "phase": "research_complete",
      "timestamp": "ISO_8601_TIMESTAMP",
      "validation": "passed"
    }
  ],
  "quality_metrics": {
    "code_examples_validated": true,
    "documentation_complete": true,
    "implementation_roadmap_realistic": true,
    "security_considerations_included": true
  },
  "sub_agent_coordination": {
    "agents_used": ["architecture", "implementation", "testing", "devops", "risk"],
    "coordination_files": ["/tmp/paths/to/agent/outputs"],
    "synthesis_complete": true,
    "cross_cutting_concerns": []
  }
}
```

**Resumability and Recovery Features:**

- Checkpoint-based recovery from any analysis phase
- Cross-session state sharing for team collaboration
- Incremental artifact updates without full regeneration
- Sub-agent result caching and reuse
- Quality validation checkpoints with automatic retry

This enhanced analysis framework provides enterprise-grade technical guidance with comprehensive examples, proper error handling, and production-ready patterns across multiple programming languages and architectural complexity levels.
