# Feature Specification

> **Status**: Draft | Review | Approved | Implemented
> **Created**: YYYY-MM-DD
> **Authors**: spec-team
> **Reviewers**: [Names]

---

## Overview

**Problem Statement**:
[What user pain point or business need does this address?]

**Goals**:
* [Measurable outcome 1]
* [Measurable outcome 2]

**Non-Goals**:
* [Explicitly out of scope]
* [Future work, not this iteration]

**Success Metrics**:
* [How will we measure success?]
* [KPIs or analytics to track]

---

## User Stories

### Story 1: [Title]

**As a** [persona]
**I want** [capability]
**So that** [benefit]

**Acceptance criteria:**
- [ ] [Testable condition]
- [ ] [Testable condition]

**Priority**: High | Medium | Low
**Dependencies**: [Other stories or systems]

---

## API Contracts

### [HTTP Method] /path/to/endpoint

**Description**: [What this endpoint does]

**Authentication**: [Required|Optional|None]

**Request**:
```json
{
  "field": "type // description"
}
```

**Response (200 OK)**:
```json
{
  "field": "type // description"
}
```

**Errors**:
* `XXX Error Name` - Condition

---

## Data Models

### Entity: [EntityName]

**Description**: [What this represents]

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |

**Relationships**:
* [Relationship description]

**Indexes**:
* `(field)` - Purpose

**Validation rules**:
* [Rule description]

---

## Acceptance Tests

### Test Scenario: [Name]

**Story**: [Link to user story]

**Given** [initial state]
**When** [action]
**Then** [expected outcome]

**Edge cases**:
* [Boundary condition]
* [Error condition]

**Performance criteria**: [Response time, throughput]

---

## Rollback Plan

**Database changes**:
- [ ] Schema changes are backwards-compatible
- [ ] Migrations are idempotent

**Code deployment**:
- [ ] Feature flag controls new behavior
- [ ] Rollback procedure < 5 minutes

**Monitoring**:
- [ ] Metrics track adoption
- [ ] Alerts for error rates

---

## Open Questions

* [Question 1 - needs decision from stakeholder X]
* [Question 2 - depends on external API availability]

---

## References

* [Link to product brief]
* [Link to design mocks]
* [Link to related specs]
