# migration-team

Plan and execute database, infrastructure, or framework migrations with comprehensive risk assessment and rollback strategies.

## Invocation

```
/migration-team [migration description]
```

**Example**: `/migration-team migrate from PostgreSQL 12 to 15 with 500GB database`

## Team Composition

- **tech-lead**: Migration strategy and architecture
- **reliability-engineer**: Rollback procedures and disaster recovery
- **performance-analyst**: Performance impact and optimization
- **test-strategist**: Test coverage and validation approach
- **devils-advocate**: Challenge necessity, identify hidden risks

## Execution Flow

### Phase 1: Assessment (Sequential)

1. **tech-lead**: Analyze current state, target state, migration complexity
2. **devils-advocate**: Challenge necessity, explore alternatives (do we need to migrate?)
3. **performance-analyst**: Baseline current performance metrics
4. **reliability-engineer**: Identify failure modes and dependencies

**Gate**: Proceed only if migration justifies risk and cost

### Phase 2: Planning (Parallel)

- **tech-lead**: Detailed migration steps, tooling, automation
- **reliability-engineer**: Rollback strategy, backup procedures
- **test-strategist**: Test plan (unit, integration, load, chaos)
- **performance-analyst**: Performance budgets and monitoring

**Gate**: All plans reviewed and risks documented

### Phase 3: Testing (Sequential)

1. **test-strategist**: Execute test plan in staging environment
2. **performance-analyst**: Validate performance meets requirements
3. **reliability-engineer**: Test rollback procedures
4. **devils-advocate**: Identify gaps in testing or overlooked scenarios

**Gate**: All tests passing, rollback verified

### Phase 4: Execution Planning (Parallel)

- **tech-lead**: Deployment runbook, timeline, automation scripts
- **reliability-engineer**: Monitoring dashboard, alert thresholds
- **test-strategist**: Production validation checklist
- **performance-analyst**: Real-time performance tracking plan

**Gate**: Runbook complete, stakeholders aligned

### Phase 5: Validation & Cleanup (Sequential)

Post-execution activities planned upfront:

1. **test-strategist**: Production validation tests
2. **performance-analyst**: Performance regression checks
3. **reliability-engineer**: System health verification
4. **tech-lead**: Cleanup plan (remove old code/data)

## Output Format

```markdown
# Migration Plan: [Name]

## Executive Summary
- **Migration**: [what → what]
- **Justification**: [why we must do this]
- **Risk Level**: [Low/Medium/High]
- **Timeline**: [duration]
- **Rollback Time**: [RTO]

## Phase 1: Assessment
### Current State
[baseline metrics, architecture]

### Target State
[goals, success criteria]

### Alternatives Considered
[why not: do nothing, partial migration, other approaches]

### Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| ... | ... | ... | ... |

## Phase 2: Planning
### Migration Steps
1. [detailed step-by-step with owners and durations]

### Rollback Strategy
- **Triggers**: [conditions requiring rollback]
- **Procedure**: [exact rollback steps]
- **Recovery Time**: [RTO estimate]
- **Data Loss**: [RPO - acceptable data loss window]

### Performance Budgets
- **Metric** | **Current** | **Target** | **Alert Threshold**

### Test Plan
- [ ] Unit tests: [coverage]
- [ ] Integration tests: [scenarios]
- [ ] Load tests: [peak capacity + 20%]
- [ ] Chaos tests: [failure injection]
- [ ] Rollback drill: [verified]

## Phase 3: Testing Results
[staging test outcomes, issues found, resolved]

## Phase 4: Execution Runbook
### Pre-Migration Checklist
- [ ] Backups verified
- [ ] Monitoring active
- [ ] Rollback tested
- [ ] Stakeholders notified
- [ ] Off-hours scheduled

### Migration Steps
| Step | Owner | Duration | Rollback Point |
|------|-------|----------|----------------|
| ... | ... | ... | ... |

### Monitoring
- **Dashboard**: [URL]
- **Alerts**: [critical thresholds]
- **On-call**: [rotation]

## Phase 5: Validation & Cleanup
### Production Validation
- [ ] Health checks passing
- [ ] Performance within budget
- [ ] User acceptance tests
- [ ] Data integrity verified

### Cleanup Plan
- [ ] Remove feature flags
- [ ] Archive old code
- [ ] Delete deprecated data
- [ ] Update documentation

## Communication Plan
- **Pre-Migration**: [stakeholder briefing]
- **During**: [status updates cadence]
- **Post**: [retrospective, lessons learned]

## Retrospective Checklist
- [ ] What went well
- [ ] What went wrong
- [ ] Action items for next migration
- [ ] Documentation updates
```

## Special Considerations

### Zero-Downtime Migrations

Use blue-green or canary patterns:

1. **Blue-Green**: Run old and new in parallel, switch traffic
2. **Canary**: Gradual rollout (1% → 10% → 50% → 100%)

### Data Migrations

- **Dual-write period**: Write to both old and new systems
- **Backfill**: Migrate historical data incrementally
- **Validation**: Compare old vs new for data integrity

### Framework/Language Upgrades

- **Incremental**: Module-by-module vs big-bang
- **Compatibility layer**: Abstract version differences
- **Dependency audit**: Check all library compatibility

## Risk Mitigation Patterns

- **Dry runs**: Execute migration in staging repeatedly
- **Rollback drills**: Practice rollback before go-live
- **Feature flags**: Control migration behavior at runtime
- **Canary deployments**: Limit blast radius of issues
- **Automated rollback**: Triggers based on metrics

## Success Criteria

- All tests passing in production
- Performance meets or exceeds baseline
- Zero critical incidents during migration
- Rollback procedure verified and documented
- Stakeholders satisfied with outcome
