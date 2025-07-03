# /epic

Manages large-scale, cross-repository refactoring epics.

## Usage

```
/epic <description>
/epic status
/epic continue
/epic rollback
```

## Description

This command orchestrates complex, multi-repository architectural changes that are impossible for single-repo agents to handle. It creates master plans, coordinates parallel work, and manages dependencies between repositories.

### What it does:

#### 1. Epic Scope Analysis

Analyzes the scope of large-scale changes across multiple repositories:

**Repository Discovery:**

- Scans monorepo subdirectories for independent services
- Identifies related repositories in the same organization
- Analyzes dependency graphs between services
- Detects shared libraries and common dependencies

**Impact Assessment:**

```bash
# Generated analysis
Repositories affected: 12
├── Core Services (4)
│   ├── user-service (Go)
│   ├── auth-service (Rust) 
│   ├── payment-service (Java)
│   └── notification-service (Deno)
├── Supporting Services (6)
│   ├── analytics-service
│   ├── audit-service
│   ├── rate-limiter
│   ├── config-service
│   ├── health-checker
│   └── metrics-collector
└── Infrastructure (2)
    ├── k8s-manifests
    └── terraform-configs

Estimated effort: 8-12 weeks
Critical path: auth-service → user-service → payment-service
```

#### 2. Master Plan Generation

Creates a comprehensive `EPIC.md` that outlines the entire transformation:

**Epic Master Plan Example:**

```markdown
# Epic: Migrate All Services from REST to gRPC

## Overview

**Goal**: Migrate all microservices from REST APIs to gRPC for improved performance, type safety, and streaming capabilities.

**Timeline**: 12 weeks
**Team Size**: 8 engineers
**Risk Level**: High (involves all production services)

## Success Criteria

- [ ] All service-to-service communication uses gRPC
- [ ] Public APIs maintain REST compatibility via gRPC-Gateway
- [ ] Performance improves by 30% (p95 latency)
- [ ] Zero downtime migration completed
- [ ] All teams trained on gRPC best practices

## Epic Phases

### Phase 1: Foundation (Weeks 1-2)

**Goal**: Establish gRPC infrastructure and tooling

**Repositories**: `shared-protos`, `grpc-gateway`, `k8s-manifests`

**Tasks**:

- [ ] Create shared protocol definitions repository
- [ ] Set up Buf Schema Registry for proto management
- [ ] Implement gRPC-Gateway for REST compatibility
- [ ] Create gRPC middleware (auth, logging, metrics)
- [ ] Update CI/CD for proto generation

**Success Criteria**:

- [ ] Proto definitions build and generate code
- [ ] gRPC-Gateway routes REST to gRPC successfully
- [ ] All repos can generate client code from protos

**Dependencies**: None (foundation work)

### Phase 2: Authentication Service (Weeks 3-4)

**Goal**: Migrate auth service as it's a dependency for all others

**Repositories**: `auth-service`, `shared-protos`

**Tasks**:

- [ ] Design auth service gRPC API
- [ ] Implement gRPC server alongside existing REST API
- [ ] Create gRPC client SDK for other services
- [ ] Deploy with feature flag for gradual rollout
- [ ] Performance testing and optimization

**Success Criteria**:

- [ ] Auth gRPC API handles 100% production traffic
- [ ] Client SDK integrated in at least 2 downstream services
- [ ] Performance metrics meet or exceed REST baseline

**Dependencies**: Phase 1 completion

### Phase 3: Core Services Migration (Weeks 5-8)

**Goal**: Migrate user, payment, and notification services in parallel

**Repositories**: `user-service`, `payment-service`, `notification-service`

**Parallel Work Streams**:

#### Stream A: User Service (Lead: @alice)

- [ ] Design user management gRPC API
- [ ] Implement bidirectional streaming for real-time updates
- [ ] Migrate database operations to use gRPC transactions
- [ ] Update frontend to use gRPC-Web

#### Stream B: Payment Service (Lead: @bob)

- [ ] Design payment processing gRPC API
- [ ] Implement secure payment streaming with deadlines
- [ ] Integrate with external payment gateways via gRPC
- [ ] Implement idempotency and retry mechanisms

#### Stream C: Notification Service (Lead: @charlie)

- [ ] Design real-time notification streaming API
- [ ] Implement server-side streaming for live updates
- [ ] Migrate WebSocket connections to gRPC streaming
- [ ] Performance test high-throughput scenarios

**Coordination Points**:

- Week 6: Integration testing between all three services
- Week 7: End-to-end testing with auth service
- Week 8: Production rollout with monitoring

### Phase 4: Supporting Services (Weeks 9-11)

**Goal**: Migrate remaining services that depend on core services

**Repositories**: `analytics-service`, `audit-service`, `rate-limiter`, `config-service`

**Batch Migration Strategy**:

- Group services by criticality and dependencies
- Migrate 2 services per week with overlapping rollouts
- Focus on services with high inter-service communication

### Phase 5: Cleanup and Optimization (Week 12)

**Goal**: Remove REST endpoints and optimize gRPC performance

**Tasks**:

- [ ] Remove deprecated REST endpoints
- [ ] Optimize proto definitions for performance
- [ ] Implement advanced gRPC features (compression, connection pooling)
- [ ] Update documentation and runbooks
- [ ] Conduct post-migration performance analysis

## Risk Mitigation

### High-Risk Items

1. **Data Consistency**: During dual-write period
   - **Mitigation**: Implement transaction coordination
   - **Rollback**: Keep REST APIs until data consistency verified

2. **Performance Regression**: gRPC overhead
   - **Mitigation**: Extensive performance testing
   - **Rollback**: Feature flags for instant REST fallback

3. **Client Breaking Changes**: API compatibility
   - **Mitigation**: gRPC-Gateway maintains REST compatibility
   - **Rollback**: Version all APIs, maintain backward compatibility

### Rollback Strategy

- Phase-level rollback capability
- Feature flags for instant traffic switching
- Database migration rollback scripts
- Automated rollback triggers based on error rates

## Resource Requirements

### Team Allocation

- **Tech Lead**: Epic coordination and architecture (@dave)
- **Backend Engineers**: Service migrations (6 engineers)
- **DevOps Engineer**: Infrastructure and deployment (@eve)
- **QA Engineer**: Testing strategy and automation (@frank)

### Infrastructure

- Additional staging environments for parallel testing
- Performance testing infrastructure
- Enhanced monitoring and alerting
- Proto registry and code generation pipeline

## Communication Plan

### Weekly Sync

- **When**: Fridays 10 AM PST
- **Duration**: 1 hour
- **Attendees**: All epic contributors
- **Format**: Progress review, blocker resolution, next week planning

### Status Updates

- Daily updates in #epic-grpc-migration Slack channel
- Weekly progress reports to stakeholders
- Bi-weekly demo sessions with users/customers

### Documentation

- Epic progress tracked in this document
- Technical decisions recorded in ADR format
- Service-specific migration guides in each repository

## Dependencies and Blockers

### External Dependencies

- [ ] Legal approval for new proto license terms
- [ ] Security review of gRPC implementation
- [ ] Customer communication for API changes

### Cross-Team Dependencies

- [ ] Frontend team: gRPC-Web implementation
- [ ] Data team: Analytics pipeline updates
- [ ] Support team: New debugging procedures

## Success Metrics

### Performance Targets

- 30% improvement in p95 latency
- 20% reduction in bandwidth usage
- 50% reduction in serialization overhead

### Quality Targets

- Zero production incidents during migration
- 100% test coverage for new gRPC endpoints
- Complete documentation for all APIs

### Business Targets

- No customer-facing API breaking changes
- Improved developer experience for API consumers
- Foundation for future streaming features
```

#### 3. Repository-Specific Plan Generation

For each affected repository, generates tailored `PLAN.md` files:

**Example Service Plan:**

```markdown
# User Service gRPC Migration Plan

## Service Overview

- **Current State**: REST API with Express.js (Node.js)
- **Target State**: gRPC API with Connect-Node
- **Dependencies**: auth-service (gRPC), postgres-db
- **Downstream Consumers**: frontend-app, mobile-app, analytics-service

## Migration Steps

### Step 1: Proto Definition

- [ ] Design user.proto with all current REST endpoints
- [ ] Add streaming endpoints for real-time user updates
- [ ] Define error codes and status mappings
- [ ] Generate TypeScript client code

### Step 2: Dual Implementation

- [ ] Implement gRPC server alongside REST
- [ ] Share business logic between REST and gRPC handlers
- [ ] Add gRPC middleware (auth, logging, metrics)
- [ ] Create integration tests for both APIs

### Step 3: Client Migration

- [ ] Update frontend to use gRPC-Web
- [ ] Migrate analytics-service to use gRPC client
- [ ] Update mobile apps to use gRPC (where supported)
- [ ] Implement fallback mechanisms

### Step 4: Traffic Migration

- [ ] Deploy with feature flag (0% gRPC traffic)
- [ ] Gradually increase gRPC traffic (1%, 5%, 25%, 50%, 100%)
- [ ] Monitor performance and error rates
- [ ] Rollback capability at each step

### Step 5: Cleanup

- [ ] Remove REST endpoints
- [ ] Update documentation
- [ ] Performance optimization
```

#### 4. Cross-Repository Coordination

Manages complex dependencies and coordination between teams:

**Coordination File (`/tmp/epic-coordination.json`):**
`json\n{\n  \"epic_id\": \"grpc-migration-2024\",\n  \"status\": \"in_progress\",\n  \"current_phase\": \"phase_2\",\n  \"repositories\": {\n    \"auth-service\": {\n      \"status\": \"completed\",\n      \"branch\": \"epic/grpc-migration\",\n      \"pr\": \"https://github.com/org/auth-service/pull/42\",\n      \"lead\": \"@alice\",\n      \"completion_date\": \"2024-06-15\"\n    },\n    \"user-service\": {\n      \"status\": \"in_progress\", \n      \"branch\": \"epic/grpc-migration\",\n      \"progress\": 65,\n      \"lead\": \"@bob\",\n      \"blockers\": [\"waiting for auth-service deployment\"]\n    },\n    \"payment-service\": {\n      \"status\": \"pending\",\n      \"dependencies\": [\"user-service\"],\n      \"lead\": \"@charlie\"\n    }\n  },\n  \"milestones\": {\n    \"phase_1_complete\": \"2024-06-01\",\n    \"phase_2_complete\": \"2024-06-15\",\n    \"phase_3_target\": \"2024-07-15\"\n  },\n  \"risks\": [\n    {\n      \"description\": \"Payment service integration complexity\",\n      \"probability\": \"medium\",\n      \"impact\": \"high\",\n      \"mitigation\": \"Additional testing environment allocated\"\n    }\n  ]\n}\n`\n\n#### 5. Orchestration and Automation\nProvides master scripts and coordination commands:\n\n**Epic Management Script:**\n`bash\n#!/bin/bash\n# epic-orchestrator.sh\n\nEPIC_ID=\"grpc-migration-2024\"\nCOORD_FILE=\"/tmp/epic-coordination.json\"\n\ncase \"$1\" in\n  \"status\")\n    echo \"Epic Status: $(jq -r '.status' $COORD_FILE)\"\n    echo \"Current Phase: $(jq -r '.current_phase' $COORD_FILE)\"\n    jq -r '.repositories | to_entries[] | \"\\(.key): \\(.value.status)\"' $COORD_FILE\n    ;;\n    \n  \"start-phase\")\n    PHASE=$2\n    echo \"Starting Phase $PHASE\"\n    \n    # Get repositories for this phase\n    REPOS=$(jq -r '.phases[\"'$PHASE'\"].repositories[]' epic-plan.json)\n    \n    for repo in $REPOS; do\n      echo \"Setting up $repo...\"\n      cd ../$repo\n      git checkout -b epic/$EPIC_ID\n      /claude plan --epic-id $EPIC_ID\n      cd -\n    done\n    ;;\n    \n  \"check-dependencies\")\n    # Verify all dependencies are completed before starting next phase\n    jq -r '.repositories | to_entries[] | select(.value.status != \"completed\") | .key' $COORD_FILE\n    ;;\n    \n  \"create-prs\")\n    # Create PRs for all repositories in current phase\n    CURRENT_PHASE=$(jq -r '.current_phase' $COORD_FILE)\n    REPOS=$(jq -r '.phases[\"'$CURRENT_PHASE'\"].repositories[]' epic-plan.json)\n    \n    for repo in $REPOS; do\n      cd ../$repo\n      /claude pr --epic-id $EPIC_ID\n      cd -\n    done\n    ;;\nesac\n`\n\n### 6. Progress Tracking and Reporting\nGenerates comprehensive progress reports:\n\n**Epic Dashboard (`epic-dashboard.md`):**\n`markdown\n# Epic Progress Dashboard\n\n## Overall Progress: 45% Complete\n\n### Phase Status\n- ✅ Phase 1: Foundation (100% - Completed)\n- 🟡 Phase 2: Authentication Service (75% - In Progress)\n- ⏳ Phase 3: Core Services (0% - Pending)\n- ⏳ Phase 4: Supporting Services (0% - Pending)\n- ⏳ Phase 5: Cleanup (0% - Pending)\n\n### Repository Status\n| Repository | Status | Progress | Lead | PR | Notes |\n|------------|--------|----------|------|-------|-------|\n| shared-protos | ✅ Complete | 100% | @alice | [#12](link) | Proto registry live |\n| auth-service | 🟡 In Progress | 85% | @bob | [#34](link) | gRPC server deployed |\n| user-service | ⏳ Blocked | 0% | @charlie | - | Waiting for auth |\n| payment-service | ⏳ Not Started | 0% | @dave | - | Scheduled Week 5 |\n\n### Blockers\n- **Auth Service**: Performance testing taking longer than expected\n- **Infrastructure**: Additional staging environment approval pending\n\n### Risks\n- 🟡 **Medium Risk**: Timeline slippage due to auth service complexity\n- 🟢 **Low Risk**: Team availability during summer vacation period\n\n### Next Actions\n- Complete auth service performance optimization (Due: Friday)\n- Begin user service proto design (Starting: Monday)\n- Schedule infrastructure capacity planning meeting\n`\n\n## Examples\n\n### Start a new epic:\n`\n/epic \"Migrate all services from REST to gRPC\"\n`\n\n### Check epic status:\n`\n/epic status\n`\n\n### Continue epic work:\n`\n/epic continue\n`\n\n### Emergency rollback:\n`\n/epic rollback --to-phase 1\n`\n\n## Advanced Features\n\n### Git Worktree Integration\nAutomatically manages separate working directories:\n`bash\n# Creates parallel working environments\ngit worktree add ../auth-service-epic epic/grpc-migration\ngit worktree add ../user-service-epic epic/grpc-migration\ngit worktree add ../payment-service-epic epic/grpc-migration\n`\n\n### Dependency Graph Visualization\nGenerates Mermaid diagrams of epic dependencies:\n`mermaid\ngraph TD\n    A[shared-protos] --> B[auth-service]\n    B --> C[user-service]\n    B --> D[payment-service]\n    C --> E[analytics-service]\n    D --> E\n    C --> F[notification-service]\n`\n\n### Automated Testing Coordination\nCoordinates testing across multiple repositories:\n`yaml\n# .github/workflows/epic-integration-test.yml\nname: Epic Integration Test\n\non:\n  workflow_dispatch:\n    inputs:\n      epic_id:\n        description: 'Epic ID'\n        required: true\n\njobs:\n  test-epic:\n    runs-on: ubuntu-latest\n    strategy:\n      matrix:\n        service: [auth, user, payment]\n    \n    steps:\n    - name: Check out epic branches\n      run: |\n        git clone --branch epic/${{ github.event.inputs.epic_id }} \\\n          https://github.com/org/${{ matrix.service }}-service.git\n    \n    - name: Run integration tests\n      run: |\n        docker-compose -f epic-test-compose.yml up --abort-on-container-exit\n`\n\n## Integration with Other Commands\n- Uses `/plan` to generate repository-specific plans\n- Integrates with `/pr` for coordinated pull request creation\n- Combines with `/deploy` for phased deployment strategies\n- Uses `/coordinate` for team synchronization
