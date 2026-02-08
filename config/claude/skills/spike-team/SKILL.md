# spike-team

Time-boxed technical exploration comparing multiple implementation approaches.

## Spawn Pattern

```
/spike-team <exploration-topic>
```

## Team Composition

- **implementation-investigator-1** (research): Explores approach A
- **implementation-investigator-2** (research): Explores approach B
- **implementation-investigator-3** (research): Explores approach C (optional)
- **api-designer**: Evaluates interface/API implications of each approach
- **devils-advocate**: Challenges necessity and advocates for simplest solution
- **tech-lead**: Synthesizes findings and produces final recommendation

## Orchestration Flow

### Phase 1: Parallel Investigation (60-120 min)

Each investigator explores one approach:
- Research existing implementations/libraries
- Prototype minimal proof of concept
- Document dependencies and complexity
- Identify edge cases and limitations
- Estimate effort (S/M/L/XL scale)

**Output**: Individual approach reports

### Phase 2: Interface Review (20-30 min)

api-designer evaluates:
- API ergonomics for each approach
- Integration points with existing code
- Developer experience implications
- Consistency with codebase patterns

**Output**: Interface comparison matrix

### Phase 3: Simplicity Challenge (15-20 min)

devils-advocate questions:
- Do we actually need this?
- What's the simplest thing that could work?
- Can we solve this without new dependencies?
- Are we over-engineering?

**Output**: Necessity assessment and minimal alternative

### Phase 4: Synthesis (30-45 min)

tech-lead produces:
- Side-by-side comparison table
- Recommended approach with rationale
- Implementation plan for chosen approach
- Migration/rollback strategy

**Output**: Spike report with decision

## Time Boxing

- **Total spike**: 2-4 hours
- **Per approach**: 60-120 minutes investigation
- **Hard stop**: After 4 hours, synthesize with incomplete data

## Success Criteria

- [ ] 2-3 approaches explored with working PoCs
- [ ] Effort estimates documented (S/M/L/XL)
- [ ] Pros/cons matrix completed
- [ ] Clear recommendation with rationale
- [ ] Rollback plan identified

## When to Use

- Choosing between architectural patterns
- Evaluating libraries/frameworks
- Designing new system components
- Prototyping technical solutions
- Before committing to major refactors

## When NOT to Use

- Already know the solution
- Single obvious approach
- Simple config/setup changes
- Time-sensitive bug fixes
