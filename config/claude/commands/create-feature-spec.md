---
description: Generate incremental feature specs for test-verified development
---

Create a focused feature specification that integrates with an existing codebase, enabling incremental development with test verification.

**Input**: User provides feature description via $ARGUMENTS

**Output**: `/specs/<feature-name>.md` with streamlined structure for single-feature implementation

---

# Feature Spec Structure

Feature specs are lighter than project specs—focused on one increment of work that can be verified through passing tests with no regressions.

## Section 1: What (Requirements)

```markdown
# Feature: [Feature Name]

## Overview
[1-2 sentences describing what this feature does and why it's needed]

## User-Facing Behavior
[Describe what the user will experience or how the API will behave]
- [Interaction/behavior 1]
- [Interaction/behavior 2]

## Requirements
- [ ] [Requirement 1]: [Clear, testable statement]
- [ ] [Requirement 2]: [Clear, testable statement]
- [ ] [Requirement 3]: [Clear, testable statement]

## Out of Scope
[Explicitly list what this feature will NOT include]
```

## Section 2: How (Approach)

```markdown
## Technical Approach

### Existing Patterns to Follow
[Reference patterns discovered in codebase scan]
- [Pattern 1]: Found in `path/to/file.ts`
- [Pattern 2]: Found in `path/to/other.ts`

### Files to Modify
| File | Change Type | Description |
|------|-------------|-------------|
| `path/to/file.ts` | Modify | [What changes] |
| `path/to/new.ts` | Create | [What it contains] |

### Key Decisions
- **[Decision area]**: [Chosen approach]
  - Why: [Brief rationale]

### Dependencies
- [New dependency, if any]: [Purpose]
```

## Section 3: Tasks (Implementation Steps)

```markdown
## Implementation Tasks

### Pre-Implementation Checklist
- [ ] Existing tests pass
- [ ] Understood dependencies and patterns
- [ ] No blocking questions
- [ ] [Any feature-specific prerequisites]

### Tasks
- [ ] **Task 1**: [Specific, testable unit of work]
  - Acceptance: [How to verify]

- [ ] **Task 2**: [Specific, testable unit of work]
  - Acceptance: [How to verify]

- [ ] **Task 3**: [Specific, testable unit of work]
  - Acceptance: [How to verify]

### Test Plan
[Adapt based on existing test infrastructure]

**Existing test patterns**: [What testing approach the codebase uses]

**Tests to write**:
- [ ] [Test case 1]: [Expected behavior]
- [ ] [Test case 2]: [Expected behavior]
- [ ] [Test case 3]: [Edge case or error handling]

### Verification
- [ ] All new tests pass
- [ ] All existing tests pass (no regressions)
- [ ] [Any feature-specific verification]
```

---

# Execution Instructions

1. **Parse feature name from $ARGUMENTS**
   - Convert to kebab-case for filename
   - Example: "add dark mode toggle" → `add-dark-mode-toggle.md`

2. **Quick codebase scan** to identify:
   - Existing architectural patterns
   - Files likely to be modified
   - Testing infrastructure and conventions
   - Relevant existing code to reference

3. **Generate feature spec** with all three sections:
   - What: Requirements derived from user description
   - How: Approach based on existing patterns
   - Tasks: Concrete steps with test plan

4. **Ensure `/specs/` directory exists**
   - Create if missing

5. **Write spec file** to `/specs/<feature-name>.md`

6. **Provide summary**:
   - Feature name and file location
   - Key files that will be modified
   - Number of tasks identified
   - Next step: Review spec or begin implementation

---

# Codebase Analysis Guidelines

**Quick scan approach** (don't deep dive):
- Identify main patterns (MVC, hooks, services, etc.)
- Find files matching feature area (by name/grep)
- Check for existing tests and their style
- Note any SPEC.md or architectural docs

**Pattern recognition**:
- How are similar features structured?
- What naming conventions are used?
- How is state managed?
- How are errors handled?

**Test infrastructure detection**:
- What test framework is used?
- Where do tests live?
- What's the test naming convention?
- Are there test utilities/helpers?

---

# Adapting to Feature Size

**Small features** (hours of work):
- 2-3 requirements
- 1-2 files to modify
- 2-3 tasks
- Basic test cases

**Medium features** (1-3 days):
- 4-6 requirements
- 3-5 files to modify
- 5-8 tasks
- Comprehensive test coverage

**Large features** (week+):
- Consider breaking into multiple feature specs
- Or use phased tasks within single spec
- More detailed pattern analysis
- Integration test focus

---

# Example

**Input**: `/create-feature-spec add user preferences API endpoint`

**Generated spec** (`/specs/add-user-preferences-api-endpoint.md`):

```markdown
# Feature: User Preferences API Endpoint

## Overview
Add a REST endpoint for reading and updating user preferences, enabling clients to persist user settings.

## User-Facing Behavior
- GET `/api/users/:id/preferences` returns current preferences
- PATCH `/api/users/:id/preferences` updates specific fields
- Returns 404 if user not found, 401 if unauthorized

## Requirements
- [ ] Authenticated users can read their own preferences
- [ ] Authenticated users can update their own preferences
- [ ] Preferences are persisted to database
- [ ] Invalid preference values return 400 with validation errors

## Out of Scope
- Admin access to other users' preferences
- Preference history/audit log
- Bulk preference operations

---

## Technical Approach

### Existing Patterns to Follow
- REST controllers: Found in `src/controllers/*.ts`
- Validation: Using zod schemas in `src/schemas/`
- Auth middleware: `src/middleware/auth.ts`

### Files to Modify
| File | Change Type | Description |
|------|-------------|-------------|
| `src/controllers/user.ts` | Modify | Add preference endpoints |
| `src/schemas/preferences.ts` | Create | Validation schema |
| `src/models/user.ts` | Modify | Add preferences field |
| `tests/controllers/user.test.ts` | Modify | Add preference tests |

### Key Decisions
- **Storage**: Preferences as JSON column on User model
  - Why: Flexible schema, single query to fetch with user

### Dependencies
- None required

---

## Implementation Tasks

### Pre-Implementation Checklist
- [ ] Existing tests pass
- [ ] Understood User model structure
- [ ] No blocking questions

### Tasks
- [ ] **Task 1**: Add preferences JSON column to User model
  - Acceptance: Migration runs, column exists

- [ ] **Task 2**: Create zod schema for preferences validation
  - Acceptance: Schema validates known preference fields

- [ ] **Task 3**: Add GET endpoint for preferences
  - Acceptance: Returns preferences for authenticated user

- [ ] **Task 4**: Add PATCH endpoint for preferences
  - Acceptance: Updates and persists preferences

- [ ] **Task 5**: Add auth checks
  - Acceptance: 401 for unauthenticated, 403 for other users

### Test Plan
**Existing test patterns**: Jest with supertest for API tests

**Tests to write**:
- [ ] GET returns preferences for authenticated user
- [ ] GET returns 401 for unauthenticated request
- [ ] PATCH updates specific preference fields
- [ ] PATCH returns 400 for invalid preference values
- [ ] PATCH returns 403 when accessing other user's preferences

### Verification
- [ ] All new tests pass
- [ ] All existing tests pass (no regressions)
- [ ] Manual test with API client
```

---

# Guidelines

**Keep specs actionable**:
- Every requirement should map to a test
- Every task should be completable independently
- Avoid vague language ("improve", "enhance", "better")

**Respect existing codebase**:
- Follow discovered patterns, don't introduce new ones
- Use existing utilities and helpers
- Match code style and conventions

**Enable verification**:
- Pre-implementation checklist catches issues early
- Test plan ensures coverage
- Verification section confirms completion

**Stay focused**:
- One feature per spec
- Defer related features to separate specs
- "Out of Scope" prevents creep
