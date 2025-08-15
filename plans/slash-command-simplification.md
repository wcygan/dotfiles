# Slash Command Simplification Plan

## Current State Analysis

**Total Commands:** ~175 files
**Critical Issues:**
- **Extreme complexity**: Top command is 1,644 lines (should be ~100-200 max)
- **Excessive parallelization**: Commands mandate 8-10 agents for simple tasks
- **Massive duplication**: 36 context commands, 30 persona commands, 6 project status commands
- **Scope creep**: Single commands trying to be complete frameworks

## Issues by Category

### 1. Over-Engineered Monsters (1000+ lines)
- `/health-check` (1,644 lines) - Should be ~200 lines
- `/flaky-fix` (1,193 lines) - Should be ~150 lines  
- `/api-docs` (1,123 lines) - Should be ~200 lines
- `/refactor` (987 lines) - Should be ~100 lines

### 2. Duplicate Command Categories
- **Context Loading**: 36 commands for loading different tech contexts
- **Agent Personas**: 30 boilerplate persona commands
- **Project Status**: 6 nearly identical project status commands
- **Dependency Analysis**: 4 overlapping dependency commands

### 3. Parallel Agent Abuse
- Commands force 8-10 agents for simple tasks
- Violates the 2-3 agent guideline from updated template
- Creates unnecessary complexity and token waste

## Simplification Strategy

### Phase 1: Emergency Consolidation (High Impact)

#### 1.1 Merge Project Status Commands → Single Parameterized Command
**Before:** 6 files (project-status-deno.md, project-status-go.md, etc.)
**After:** 1 file with `$ARGUMENTS` parameter

#### 1.2 Create Dynamic Context System
**Before:** 36 context-specific commands
**After:** 1 smart context command that detects technology and loads appropriate context

#### 1.3 Template-Based Persona System
**Before:** 30 boilerplate persona files
**After:** 1 persona template with role parameter

### Phase 2: Simplify Over-Engineered Commands (Critical)

#### 2.1 Break Down the Big 5 (1000+ lines each)
- `/health-check`: Split into focused health checks
- `/flaky-fix`: Simplify to core flaky test detection/fix
- `/api-docs`: Focus on single API documentation
- `/accessibility-expert`: Remove excessive framework coverage
- `/refactor`: Complete rewrite following `/commit` pattern

#### 2.2 Agent Usage Normalization
- Limit all commands to 2-3 agents maximum
- Remove mandatory parallelization for simple tasks
- Follow updated parallel template guidelines

### Phase 3: Quality Standardization

#### 3.1 Use `/commit` as Gold Standard
- 89 lines - perfect length reference
- Clear single purpose
- Appropriate tool usage
- No unnecessary agent spawning

#### 3.2 Eliminate Duplicate Functionality
- Merge overlapping analysis commands
- Consolidate similar scaffolding commands
- Remove redundant workflow commands

## Implementation Priority

### Immediate (Week 1)
1. **Fix the worst offenders**: Simplify top 5 largest commands
2. **Consolidate project status**: 6 → 1 command
3. **Update parallel agent usage**: Remove 8-10 agent mandates

### High Priority (Week 2) 
4. **Dynamic context system**: 36 → 1 smart context command
5. **Persona templates**: 30 → 1 parameterized system
6. **Dependency analysis**: 4 → 2 focused commands

### Medium Priority (Week 3)
7. **Test command optimization**: Simplify test generation/analysis
8. **Documentation commands**: Merge overlapping doc generators
9. **Workflow streamlining**: Remove redundant workflow steps

## Expected Results

### Quantitative Improvements
- **Commands**: 175 → ~100-120 (30% reduction)
- **Average size**: 400 → 150-200 lines (50% reduction)  
- **Largest command**: 1,644 → 300 lines maximum
- **Parallel agents**: 8-10 → 2-3 maximum per command

### Qualitative Improvements
- **Usability**: Commands actually usable instead of overwhelming
- **Maintainability**: Easier to update and modify
- **Consistency**: Standardized patterns across all commands
- **Performance**: Faster execution with appropriate parallelization

## Success Metrics

### Before State
- Largest command: 1,644 lines
- Commands with 8+ agents: ~15
- Duplicate functionality: ~40 commands
- Average complexity: Too high to use effectively

### Target State
- Largest command: <300 lines
- Commands with 3+ agents: <5 (only when beneficial)
- Duplicate functionality: Eliminated
- Average complexity: Immediately usable

## Risk Mitigation

1. **Backup current commands** before major changes
2. **Test each simplified command** to ensure functionality
3. **Migrate gradually** - fix worst offenders first
4. **Keep `/commit` unchanged** - it's the perfect example
5. **Document changes** for any breaking command interfaces

This plan transforms an unwieldy collection of over-engineered commands into a clean, focused, and actually usable slash command system following modern Claude Code best practices.