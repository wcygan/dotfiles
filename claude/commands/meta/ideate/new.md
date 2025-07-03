# /ideate-new

Discover and propose new Claude command opportunities based on systematic analysis of existing commands, developer workflow gaps, and emerging technology trends.

## Usage

```
/ideate-new [focus-area]
```

## Parameters

- `focus-area` (optional) - Specific area to analyze: `ai-ml`, `frontend`, `cloud`, `mobile`, `database`, `security`, `emerging`
- If no focus area specified, performs comprehensive analysis across all categories

## Process

### Phase 1: Current State Analysis

**Command Ecosystem Inventory**

1. **Count and categorize existing commands**:
   - List all commands in `claude/commands/` directory
   - Group by workflow stage (planning, development, testing, deployment, etc.)
   - Identify coverage gaps and underrepresented categories

2. **Pattern recognition**:
   - Analyze naming conventions (action-based, hyphenated, prefixed)
   - Review command complexity and argument patterns
   - Note successful command structures for replication

3. **Usage gap identification**:
   - Map developer workflow stages to command availability
   - Identify single-command categories that could expand
   - Note areas with high manual effort but no automation

### Phase 2: Market Research & Pain Point Analysis

**Developer Workflow Trends**

1. **Technology evolution tracking**:
   - Survey latest framework migrations and tool adoptions
   - Research emerging development practices and patterns
   - Identify automation opportunities in manual processes

2. **Pain point validation**:
   - Common developer complaints and friction points
   - Repeated tasks that could benefit from automation
   - Complex workflows that need systematic approaches

3. **Industry trend analysis**:
   - Cloud-native development complexity
   - AI/ML integration requirements
   - Mobile development automation gaps
   - Security and compliance automation needs

### Phase 3: Opportunity Identification

**Command Gap Analysis**

1. **High-impact opportunities**:
   - Pain points affecting 50%+ of developers
   - Manual processes with clear automation potential
   - Complex workflows needing systematic guidance

2. **Strategic opportunities**:
   - Emerging technology adoption support
   - Enterprise workflow automation
   - Developer productivity enhancement

3. **Future-focused opportunities**:
   - Next-generation technology preparation
   - Experimental workflow automation
   - Niche but valuable use cases

### Phase 4: Command Design & Prioritization

**Design Principles**

1. **Simple usage patterns**:
   - `/command [optional-context]` format
   - Auto-detection of project context when possible
   - Interactive fallback for guided assistance

2. **Contextual intelligence**:
   - Read project structure (package.json, Cargo.toml, etc.)
   - Detect frameworks and tools in use
   - Provide relevant suggestions based on environment

3. **Smart defaults**:
   - Work without arguments for common cases
   - Progressive enhancement with optional specificity
   - Fail gracefully with helpful guidance

**Prioritization Framework**

**Tier 1 (Immediate Value)**

- Addresses widespread pain points
- Clear ROI for developer productivity
- Fits existing command ecosystem

**Tier 2 (Strategic Value)**

- Supports emerging technology adoption
- Fills enterprise workflow gaps
- Enhances command synergy

**Tier 3 (Future Value)**

- Experimental/emerging technologies
- Foundation for future command development
- Niche but valuable capabilities

### Phase 5: Research Output

**Command Proposals**

For each proposed command:

1. **Name and usage**: Simple, consistent naming following existing patterns
2. **Gap description**: What current need is unmet
3. **Value proposition**: How it improves developer workflow
4. **Context awareness**: How it detects and adapts to project environment
5. **Tier classification**: Priority level and implementation timeline

**Implementation Roadmap**

- Phase 1: High-impact commands addressing major pain points
- Phase 2: Strategic commands for emerging technologies
- Phase 3: Future-focused and experimental commands

## Key Research Areas

### AI/ML Workflows

- MLOps pipeline setup and management
- Model deployment and versioning
- Data pipeline automation
- Experiment tracking integration

### Frontend Development

- Build tool migration automation
- Performance optimization workflows
- Framework-specific scaffolding gaps
- Micro-frontend architecture support

### Cloud-Native Development

- Kubernetes troubleshooting and debugging
- Multi-cluster deployment management
- Service mesh configuration
- Container optimization workflows

### Mobile Development

- Platform-specific CI/CD automation
- Testing framework setup
- Store deployment workflows
- Cross-platform development support

### Database Operations

- Zero-downtime migration strategies
- Performance optimization workflows
- Data pipeline management
- Schema evolution automation

### Security & Compliance

- Automated vulnerability scanning
- Dependency security auditing
- Compliance workflow automation
- Security hardening processes

## Output Format

Present findings as:

1. **Executive Summary**: Key gaps and highest-impact opportunities
2. **Tiered Command List**: Organized by implementation priority
3. **Usage Examples**: Simple command invocation patterns
4. **Context Integration**: How commands fit existing workflow
5. **Implementation Roadmap**: Suggested development phases

Focus on actionable insights that directly translate to valuable new commands following the established patterns and design principles.
