# API Design Reference

Comprehensive reference for API design patterns, principles, and templates.

## Design Principles

### 1. Consumer-First Design

**Good APIs prioritize the consumer experience:**

- **Intuitive naming**: Use domain language, not implementation details
  - Good: `GET /orders/{id}/items`
  - Bad: `GET /order_item_relations?order_id={id}`

- **Predictable patterns**: Consistent URL structure and response formats
  - If `GET /users` returns a list, so should `GET /projects`
  - If `POST /users` creates, so should `POST /projects`

- **Self-documenting**: Clear without reading docs
  - Field names explain their purpose: `created_at` not `ct`
  - Error messages guide resolution: "Invalid email format" not "Validation error"

### 2. Domain-Driven Design

**APIs should reflect the business domain:**

- **Bounded contexts**: Group related resources
  - Checkout context: `/cart`, `/orders`, `/payments`
  - Catalog context: `/products`, `/categories`, `/reviews`

- **Ubiquitous language**: Use terms from domain experts
  - E-commerce: "order", "fulfillment", "inventory"
  - Healthcare: "patient", "appointment", "diagnosis"

- **Aggregates**: Design around consistency boundaries
  - Order aggregate includes line items (consistent)
  - Order references customer (eventually consistent)

### 3. Security by Default

**Assume hostile actors:**

- **Least privilege**: Require authentication by default
  - Only public read operations should be unauthenticated
  - Use scoped permissions (OAuth scopes, RBAC)

- **No sensitive data in URLs**: Query params are logged
  - Bad: `GET /users?ssn=123-45-6789`
  - Good: `POST /users/search` with body `{"ssn": "123-45-6789"}`

- **Rate limiting**: Protect against abuse
  - Document limits in response headers
  - Provide burst allowances for legitimate use

### 4. Performance-Conscious

**Design for scale:**

- **Pagination**: Always paginate collections
  - Include `next` links for cursor-based pagination
  - Document page size limits and defaults

- **Selective loading**: Let clients choose depth
  - GraphQL: Client specifies fields
  - REST: Use `fields` parameter or sparse fieldsets

- **Caching**: Make responses cacheable
  - Set appropriate `Cache-Control` headers
  - Use ETags for conditional requests

### 5. Evolvability

**APIs must change without breaking clients:**

- **Additive changes are safe**: New fields, new endpoints
- **Versioning for breaking changes**: Remove fields, change types
- **Deprecation process**: Warn → grace period → remove
- **Hypermedia**: Include links to guide navigation

## API Styles Comparison

### REST (Representational State Transfer)

**When to use:**
- Public-facing APIs with diverse clients
- Standard CRUD operations
- Leveraging HTTP semantics (caching, status codes)
- Wide tooling ecosystem matters

**Characteristics:**
- **Resources**: Nouns (`/users`, `/orders`)
- **HTTP methods**: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`
- **Stateless**: Each request contains all context
- **Hypermedia**: Links guide navigation (HATEOAS)

**Strengths:**
- Industry standard with vast tooling support
- HTTP caching works out of the box
- Easy to understand and debug (curl, browser)
- Works well with CDNs and proxies

**Weaknesses:**
- Over-fetching (get full resource when you need one field)
- Under-fetching (multiple requests for related data)
- Versioning challenges (breaking changes require new version)
- No type system (need OpenAPI for validation)

**Example:**
```http
GET /users/123
Accept: application/json

200 OK
{
  "id": 123,
  "name": "Alice",
  "email": "alice@example.com",
  "_links": {
    "orders": "/users/123/orders",
    "self": "/users/123"
  }
}
```

### GraphQL

**When to use:**
- Complex data graphs with many relationships
- Multiple client types (web, mobile) with different needs
- Frequent schema evolution
- Strong typing matters for safety

**Characteristics:**
- **Single endpoint**: `/graphql`
- **Client-specified queries**: Fetch exactly what you need
- **Strongly typed schema**: Introspection and validation
- **Mutations and subscriptions**: Reads, writes, real-time

**Strengths:**
- Precise data fetching (no over/under-fetching)
- Type safety with schema validation
- Introspection enables great tooling
- Real-time via subscriptions

**Weaknesses:**
- Caching complexity (no URL-based cache keys)
- Learning curve for consumers
- Query complexity attacks (need depth/complexity limits)
- Harder to monitor and debug than REST

**Example:**
```graphql
query GetUser {
  user(id: 123) {
    name
    email
    orders(first: 5) {
      id
      total
      items {
        product {
          name
        }
      }
    }
  }
}
```

### RPC (Remote Procedure Call)

**When to use:**
- Internal microservice communication
- Actions that don't map to resources (send email, run job)
- Performance-critical paths
- Strongly-typed client/server contracts

**Characteristics:**
- **Procedures**: Verbs (`/sendEmail`, `/calculateShipping`)
- **Transport agnostic**: gRPC uses HTTP/2, JSON-RPC uses JSON
- **Strongly typed**: Protocol Buffers, Thrift
- **Code generation**: Auto-generate clients from schema

**Strengths:**
- Very efficient (binary protocols, HTTP/2 multiplexing)
- Strong typing with code generation
- Natural for action-oriented operations
- Great for microservices (service mesh support)

**Weaknesses:**
- Less discoverable than REST
- Binary formats harder to debug
- Requires code generation tooling
- Not cacheable via HTTP semantics

**Example (gRPC):**
```protobuf
service UserService {
  rpc GetUser(GetUserRequest) returns (User);
  rpc CreateUser(CreateUserRequest) returns (User);
}

message User {
  int64 id = 1;
  string name = 2;
  string email = 3;
}
```

## Authentication Strategies

### OAuth 2.0

**When to use:**
- Delegated authorization (user grants app access to their data)
- Third-party integrations
- Public APIs with multiple client types

**Flows:**
- **Authorization Code**: Web apps with backend (most secure)
- **PKCE**: Mobile and SPA (extension of auth code)
- **Client Credentials**: Machine-to-machine
- **Refresh Tokens**: Long-lived access without re-auth

**Example:**
```http
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&code=AUTH_CODE
&redirect_uri=https://app.example.com/callback
&client_id=CLIENT_ID
&client_secret=CLIENT_SECRET

200 OK
{
  "access_token": "ACCESS_TOKEN",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "REFRESH_TOKEN"
}
```

### API Keys

**When to use:**
- Server-to-server communication
- Simple authentication needs
- Rate limiting and billing
- Internal or private APIs

**Best practices:**
- Use long, random strings (not sequential IDs)
- Support key rotation without downtime
- Scope keys to specific permissions
- Allow multiple keys per account
- Log key usage for auditing

**Example:**
```http
GET /api/users
Authorization: Bearer sk_live_abc123def456

200 OK
X-RateLimit-Remaining: 999
```

### JWT (JSON Web Tokens)

**When to use:**
- Stateless authentication
- Microservices (pass claims between services)
- Short-lived sessions
- Self-contained authorization

**Claims:**
- **Registered**: `iss`, `sub`, `aud`, `exp`, `iat`
- **Custom**: Add domain-specific claims

**Best practices:**
- Keep payload small (transmitted in every request)
- Sign with strong algorithms (RS256, ES256)
- Set short expiration times
- Use refresh tokens for long-lived sessions
- Revocation requires allowlist/denylist

**Example:**
```http
GET /api/users
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...

Decoded JWT:
{
  "sub": "user123",
  "email": "alice@example.com",
  "roles": ["admin"],
  "exp": 1735689600
}
```

## Versioning Strategies

### URI Versioning

**Pattern:** `/v1/users`, `/v2/users`

**Pros:**
- Explicit and visible
- Easy to test (just change URL)
- Works with all HTTP clients

**Cons:**
- Breaks caching (different URLs)
- Requires routing config updates
- Version number in every URL

**Example:**
```http
GET /v1/users/123
GET /v2/users/123
```

### Header Versioning

**Pattern:** `Accept: application/vnd.api+json;version=1`

**Pros:**
- Clean URLs (no version prefix)
- Can version by resource or media type
- Preserves caching (same URL)

**Cons:**
- Harder to test (need to set headers)
- Less visible to developers
- Tooling support varies

**Example:**
```http
GET /users/123
Accept: application/vnd.api+json;version=1

GET /users/123
Accept: application/vnd.api+json;version=2
```

### Content Negotiation

**Pattern:** Different media types for different versions

**Pros:**
- Follows HTTP standards
- Granular versioning per resource
- Supports multiple formats (JSON, XML, Protocol Buffers)

**Cons:**
- Complex to implement correctly
- Confusing for consumers
- Hard to document

**Example:**
```http
GET /users/123
Accept: application/vnd.user.v1+json

GET /users/123
Accept: application/vnd.user.v2+json
```

### No Versioning (Additive Changes Only)

**Pattern:** Never break compatibility, only add fields

**Pros:**
- No versioning complexity
- Single codebase
- Clients upgrade at their pace

**Cons:**
- Technical debt accumulates
- Can't remove bad design decisions
- Requires careful planning

**Strategy:**
- Add new fields, never remove or change types
- Deprecate with warnings, remove only after long grace period
- Use feature flags for behavioral changes

## Error Handling

### Problem Details (RFC 7807)

**Standard format for HTTP error responses:**

```json
{
  "type": "https://api.example.com/errors/insufficient-funds",
  "title": "Insufficient Funds",
  "status": 402,
  "detail": "Your account balance is $10 but the charge is $15.",
  "instance": "/orders/1234/pay",
  "balance": 10,
  "required": 15
}
```

**Fields:**
- `type`: URI identifying the problem type (documentation)
- `title`: Human-readable summary
- `status`: HTTP status code (convenience)
- `detail`: Human-readable explanation
- `instance`: URI identifying this occurrence
- *Custom fields*: Add domain-specific context

**Status code mapping:**
- `400 Bad Request`: Client error (invalid input)
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Authenticated but not authorized
- `404 Not Found`: Resource doesn't exist
- `409 Conflict`: State conflict (e.g., duplicate)
- `422 Unprocessable Entity`: Validation error
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server fault
- `503 Service Unavailable`: Temporary overload or maintenance

### Validation Errors

**Structured format for field-level errors:**

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Failed",
  "status": 422,
  "errors": [
    {
      "field": "email",
      "message": "must be a valid email address",
      "code": "INVALID_FORMAT"
    },
    {
      "field": "age",
      "message": "must be at least 18",
      "code": "OUT_OF_RANGE"
    }
  ]
}
```

**Best practices:**
- Use consistent error codes (enum)
- Include the invalid value (if not sensitive)
- Explain what's wrong and how to fix it
- Localize messages server-side (don't rely on client)

## Pagination Strategies

### Offset/Limit (Page-based)

**Pattern:** `?offset=20&limit=10`

**Pros:**
- Simple to implement and understand
- Can jump to arbitrary pages
- Matches SQL `OFFSET`/`LIMIT`

**Cons:**
- Inconsistent under concurrent writes (items shift)
- Performance degrades with large offsets (database must scan)
- Can see duplicates or miss items

**Example:**
```http
GET /users?offset=0&limit=10

200 OK
{
  "data": [...10 users...],
  "pagination": {
    "offset": 0,
    "limit": 10,
    "total": 1250
  }
}
```

### Cursor-based

**Pattern:** `?after=eyJpZCI6MTIzfQ==`

**Pros:**
- Consistent under writes (stable position)
- Efficient (indexed seek)
- No duplicates or missed items

**Cons:**
- Can't jump to arbitrary page
- Cursor is opaque (can't inspect)
- Requires indexed sort key

**Example:**
```http
GET /users?limit=10

200 OK
{
  "data": [...10 users...],
  "pagination": {
    "next_cursor": "eyJpZCI6MTIzfQ==",
    "has_more": true
  }
}

GET /users?after=eyJpZCI6MTIzfQ==&limit=10
```

### Keyset (Seek Method)

**Pattern:** `?after_id=123&limit=10`

**Pros:**
- Most efficient (uses indexes)
- Consistent and predictable
- Transparent (visible values)

**Cons:**
- Requires indexed sort column
- Only works with total ordering (unique key)
- Can't jump to arbitrary page

**Example:**
```http
GET /users?after_id=123&limit=10

200 OK
{
  "data": [...10 users...],
  "pagination": {
    "after_id": 133,
    "has_more": true
  }
}
```

## OpenAPI 3.1 Template

```yaml
openapi: 3.1.0
info:
  title: Example API
  version: 1.0.0
  description: |
    API for managing resources.

    ## Authentication
    Use Bearer tokens in the Authorization header.

    ## Rate Limiting
    - 1000 requests per hour per API key
    - Burst limit of 100 requests per minute
  contact:
    name: API Support
    email: api@example.com
    url: https://example.com/support
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://api-staging.example.com/v1
    description: Staging

tags:
  - name: Users
    description: User management operations
  - name: Orders
    description: Order operations

paths:
  /users:
    get:
      summary: List users
      description: Returns a paginated list of users
      operationId: listUsers
      tags: [Users]
      parameters:
        - name: limit
          in: query
          description: Number of users to return
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: cursor
          in: query
          description: Pagination cursor from previous response
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/CursorPagination'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '429':
          $ref: '#/components/responses/RateLimited'
      security:
        - bearerAuth: []

    post:
      summary: Create user
      description: Creates a new user
      operationId: createUser
      tags: [Users]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
          headers:
            Location:
              description: URI of the created user
              schema:
                type: string
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '422':
          $ref: '#/components/responses/ValidationError'
      security:
        - bearerAuth: [write:users]

  /users/{userId}:
    get:
      summary: Get user
      description: Returns a single user by ID
      operationId: getUser
      tags: [Users]
      parameters:
        - name: userId
          in: path
          required: true
          description: User ID
          schema:
            type: integer
            format: int64
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'
      security:
        - bearerAuth: []

    patch:
      summary: Update user
      description: Partially updates a user
      operationId: updateUser
      tags: [Users]
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: integer
            format: int64
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateUserRequest'
      responses:
        '200':
          description: User updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'
        '422':
          $ref: '#/components/responses/ValidationError'
      security:
        - bearerAuth: [write:users]

    delete:
      summary: Delete user
      description: Deletes a user
      operationId: deleteUser
      tags: [Users]
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: integer
            format: int64
      responses:
        '204':
          description: User deleted
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'
      security:
        - bearerAuth: [write:users]

components:
  schemas:
    User:
      type: object
      required: [id, email, name, created_at]
      properties:
        id:
          type: integer
          format: int64
          description: Unique user identifier
          example: 123
        email:
          type: string
          format: email
          description: User's email address
          example: alice@example.com
        name:
          type: string
          minLength: 1
          maxLength: 100
          description: User's full name
          example: Alice Smith
        created_at:
          type: string
          format: date-time
          description: When the user was created
          example: 2024-01-15T10:30:00Z
        _links:
          type: object
          description: Hypermedia links
          properties:
            self:
              type: string
              format: uri
              example: /users/123
            orders:
              type: string
              format: uri
              example: /users/123/orders

    CreateUserRequest:
      type: object
      required: [email, name]
      properties:
        email:
          type: string
          format: email
          example: alice@example.com
        name:
          type: string
          minLength: 1
          maxLength: 100
          example: Alice Smith

    UpdateUserRequest:
      type: object
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100

    CursorPagination:
      type: object
      properties:
        next_cursor:
          type: string
          nullable: true
          description: Cursor for next page, null if no more pages
        has_more:
          type: boolean
          description: Whether more pages exist

    Problem:
      type: object
      description: RFC 7807 Problem Details
      required: [type, title, status]
      properties:
        type:
          type: string
          format: uri
          description: URI identifying the problem type
          example: https://api.example.com/errors/validation
        title:
          type: string
          description: Short, human-readable summary
          example: Validation Failed
        status:
          type: integer
          description: HTTP status code
          example: 422
        detail:
          type: string
          description: Human-readable explanation
          example: One or more fields failed validation
        instance:
          type: string
          format: uri
          description: URI identifying this occurrence
          example: /users

    ValidationProblem:
      allOf:
        - $ref: '#/components/schemas/Problem'
        - type: object
          properties:
            errors:
              type: array
              items:
                type: object
                required: [field, message, code]
                properties:
                  field:
                    type: string
                    description: Field that failed validation
                    example: email
                  message:
                    type: string
                    description: Human-readable error message
                    example: must be a valid email address
                  code:
                    type: string
                    description: Machine-readable error code
                    example: INVALID_FORMAT

  responses:
    BadRequest:
      description: Invalid request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Problem'

    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Problem'

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Problem'

    ValidationError:
      description: Validation failed
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ValidationProblem'

    RateLimited:
      description: Rate limit exceeded
      headers:
        X-RateLimit-Limit:
          description: Request limit per hour
          schema:
            type: integer
        X-RateLimit-Remaining:
          description: Requests remaining
          schema:
            type: integer
        X-RateLimit-Reset:
          description: Time when limit resets (Unix timestamp)
          schema:
            type: integer
            format: int64
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Problem'

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT access token from OAuth2 flow

    oauth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.example.com/oauth/authorize
          tokenUrl: https://auth.example.com/oauth/token
          scopes:
            read:users: Read user information
            write:users: Create and update users
            delete:users: Delete users

security:
  - bearerAuth: []
```

## Debate Prompts

### API Style Decision

**Prompt for API Designer:**
"From a developer experience perspective, which API style (REST, GraphQL, or RPC) would be most intuitive for our use case? Consider discoverability, learning curve, and tooling."

**Prompt for Performance Analyst:**
"Which API style best matches our query patterns? Will we have over-fetching or N+1 query issues? How does caching work in each approach?"

**Prompt for Tech Lead:**
"What's the industry standard for this domain? What does our team have experience with? How does each style align with our existing infrastructure?"

### Authentication Strategy

**Prompt for Security Auditor:**
"What authentication strategy provides the right security level for our threat model? What are the risks of each approach?"

**Prompt for API Designer:**
"Which authentication method is easiest for developers to integrate? How does it impact the getting-started experience?"

**Prompt for Tech Lead:**
"What standards should we follow (OAuth2, OpenID Connect)? How do we support multiple auth methods (API keys for server, OAuth for web)?"

### Versioning Approach

**Prompt for Tech Lead:**
"Should we version via URI, header, or content negotiation? How do we handle deprecation and migration?"

**Prompt for API Designer:**
"How does the versioning strategy affect developer experience? Is it easy to test different versions?"

**Prompt for Domain Modeler:**
"Can we avoid versioning by using semantic compatibility? What domain changes would force a version bump?"

### Resource Granularity

**Prompt for Domain Modeler:**
"What are the natural aggregates and boundaries in our domain? Should this be one resource or multiple?"

**Prompt for Performance Analyst:**
"Will this design cause N+1 queries? Should we embed related data or use separate endpoints?"

**Prompt for API Designer:**
"Is this resource structure intuitive for consumers? Can they find what they need without reading docs?"

### Error Handling Strategy

**Prompt for Security Auditor:**
"Are we exposing sensitive information in error messages? Do we leak implementation details?"

**Prompt for API Designer:**
"Do error messages help developers resolve issues? Are they actionable?"

**Prompt for Tech Lead:**
"Should we use RFC 7807 Problem Details or a custom format? How do we structure validation errors?"

## Output Template

```markdown
# API Specification: [API Name]

## Executive Summary

[2-3 paragraphs summarizing the API design, key decisions, and rationale]

## Design Decisions

### API Style: [REST/GraphQL/RPC]

**Decision:** [Chosen approach]

**Rationale:** [Why this choice fits the requirements]

**Trade-offs:** [What we gave up]

### Authentication: [OAuth2/API Keys/JWT]

**Decision:** [Chosen approach]

**Rationale:** [Security, UX, and standards considerations]

**Trade-offs:** [Complexity vs security vs UX]

### Versioning: [URI/Header/None]

**Decision:** [Chosen approach]

**Rationale:** [Migration, caching, and testing considerations]

**Trade-offs:** [Flexibility vs complexity]

### Pagination: [Offset/Cursor/Keyset]

**Decision:** [Chosen approach]

**Rationale:** [Consistency, performance, and UX considerations]

**Trade-offs:** [Simplicity vs correctness]

### Error Handling: [Problem Details/Custom]

**Decision:** [Chosen approach]

**Rationale:** [Standards compliance and developer experience]

**Trade-offs:** [Standardization vs customization]

## API Specification

[Full OpenAPI 3.1 or GraphQL schema here]

## Design Rationale

### Consumer Experience

[How the API supports developer workflows]

### Domain Modeling

[How the API reflects business concepts]

### Security

[Authentication, authorization, rate limiting, data protection]

### Performance

[Caching strategy, pagination, query optimization]

### Standards Compliance

[Which RFCs, specifications, or industry standards are followed]

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| [Potential issue] | [Consequences] | [How we address it] |

## Implementation Notes

### Backend Considerations

- [Guidance for API implementers]
- [Database schema implications]
- [Caching strategy]

### Client Examples

#### cURL
```bash
# Example requests
```

#### JavaScript
```javascript
// Example client code
```

#### Python
```python
# Example client code
```

## Future Evolution

[How the API can grow without breaking changes]

[Planned extensions or features]

## Appendix: Agent Debates

### [Topic 1]

**Participants:** [Agent names]

**Outcome:** [Decision]

**Key points:**
- [Summary of debate]

### [Topic 2]

[...]
```
