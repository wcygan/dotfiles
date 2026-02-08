# Specification Reference

Templates and standards for the spec-team workflow.

## User Story Format

```markdown
## Story: [Short descriptive title]

**As a** [type of user/persona]
**I want** [capability or action]
**So that** [benefit or value]

**Acceptance criteria:**
- [ ] [Given/When/Then or specific observable outcome]
- [ ] [Given/When/Then or specific observable outcome]
- [ ] [Edge case or error condition]

**Priority**: [High|Medium|Low]
**Effort**: [S|M|L|XL] (optional)
**Dependencies**: [List of other stories or systems]

**Notes**: [Context, assumptions, open questions]
```

### Example

```markdown
## Story: OAuth Login with Google

**As a** new user
**I want** to sign in with my Google account
**So that** I don't have to create another password

**Acceptance criteria:**
- [ ] Given I click "Sign in with Google", when I complete OAuth flow, then I'm redirected back and logged in
- [ ] Given Google returns an error, when OAuth fails, then I see a user-friendly error message
- [ ] Given I've signed in before, when I return, then my session persists for 7 days

**Priority**: High
**Dependencies**: Session management, user profile creation

**Notes**: Assume Google OAuth 2.0. Need to register app in Google Console.
```

---

## API Contract Format

```markdown
### [HTTP Method] /path/to/endpoint

**Description**: [What this endpoint does]

**Authentication**: [Required|Optional|None] - [auth scheme]

**Request**:
```json
{
  "field": "type // description",
  "nested": {
    "required": "string // must be non-empty"
  }
}
```

**Response (200 OK)**:
```json
{
  "id": "uuid // resource identifier",
  "created_at": "ISO8601 timestamp"
}
```

**Errors**:
* `400 Bad Request` - Invalid input (e.g., missing required field)
* `401 Unauthorized` - Missing or invalid auth token
* `409 Conflict` - Resource already exists

**Notes**: [Rate limits, pagination, versioning]
```

### Example

```markdown
### POST /auth/oauth/callback

**Description**: Completes OAuth flow and creates session

**Authentication**: None (public endpoint)

**Request**:
```json
{
  "code": "string // OAuth authorization code from provider",
  "state": "string // CSRF token from initial request",
  "provider": "string // one of: google, github"
}
```

**Response (200 OK)**:
```json
{
  "session_token": "string // JWT valid for 7 days",
  "user": {
    "id": "uuid",
    "email": "string",
    "name": "string"
  }
}
```

**Errors**:
* `400 Bad Request` - Invalid code or state mismatch
* `401 Unauthorized` - OAuth provider rejected token exchange
* `500 Internal Server Error` - Failed to create user record

**Notes**: Set HttpOnly cookie with session_token. State must match initial OAuth request to prevent CSRF.
```

---

## Data Model Format

```markdown
## Entity: [EntityName]

**Description**: [What this entity represents]

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| created_at | TIMESTAMP | NOT NULL | Creation time |
| field_name | TYPE | [constraints] | [description] |

**Relationships**:
* `belongs_to :other_entity` - Foreign key `other_entity_id`
* `has_many :child_entities` - One-to-many relationship

**Indexes**:
* `(field1, field2)` - Composite index for common query
* `(email)` - Unique index

**Validation rules**:
* Email must match RFC 5322 format
* Username must be 3-30 alphanumeric characters

**Notes**: [Soft deletes, versioning, encryption requirements]
```

### Example

```markdown
## Entity: User

**Description**: Authenticated user account

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address |
| name | VARCHAR(100) | NOT NULL | Display name |
| provider | VARCHAR(20) | NOT NULL | OAuth provider (google, github) |
| provider_id | VARCHAR(255) | NOT NULL | ID from OAuth provider |
| created_at | TIMESTAMP | NOT NULL | Account creation time |
| last_login | TIMESTAMP | NULL | Most recent login |

**Relationships**:
* `has_many :sessions` - User can have multiple active sessions

**Indexes**:
* `(email)` - Unique index for lookup
* `(provider, provider_id)` - Unique composite to prevent duplicate OAuth accounts

**Validation rules**:
* Email must be valid format (RFC 5322)
* Provider must be one of: google, github
* Name must be 1-100 characters

**Notes**: Do NOT store passwords (OAuth only). Soft delete by setting deleted_at timestamp.
```

---

## Acceptance Test Format

```markdown
## Test Scenario: [Descriptive name]

**Story**: [Link to user story]

**Given** [initial state]
**When** [action occurs]
**Then** [expected outcome]

**Variations**:
* **Given** [alternative state] **When** [action] **Then** [different outcome]

**Edge cases**:
* [Boundary condition to test]
* [Error condition to test]

**Performance criteria**: [Response time, throughput, etc.]
```

### Example

```markdown
## Test Scenario: Google OAuth Happy Path

**Story**: OAuth Login with Google

**Given** user clicks "Sign in with Google"
**When** they complete Google OAuth and return with valid code
**Then** they are logged in with a session token and redirected to dashboard

**Variations**:
* **Given** user cancels OAuth flow **When** they return to app **Then** they see "Login cancelled" message
* **Given** OAuth code is expired **When** we attempt token exchange **Then** user sees "Session expired, please try again"

**Edge cases**:
* State parameter mismatch (CSRF attempt) → reject with 400
* Network failure during token exchange → retry 3x then show error
* Email already exists with different provider → offer to link accounts

**Performance criteria**: OAuth callback processing < 500ms (p95)
```

---

## Rollback & Migration Checklist

Include in final spec if the feature affects persistent data:

```markdown
## Rollback Plan

**Database changes**:
- [ ] All schema changes are backwards-compatible (additive only)
- [ ] New columns have defaults or are nullable
- [ ] Indexes can be built online without locking

**Data migration**:
- [ ] Migration script is idempotent (safe to re-run)
- [ ] Batch size limits prevent timeouts
- [ ] Progress tracking/resume capability

**Code deployment**:
- [ ] Feature flag controls new behavior
- [ ] Old clients can still call deprecated endpoints
- [ ] Rollback procedure documented (< 5 minutes)

**Monitoring**:
- [ ] Metrics track new feature adoption
- [ ] Alerts for elevated error rates
- [ ] Dashboards show before/after comparison
```
