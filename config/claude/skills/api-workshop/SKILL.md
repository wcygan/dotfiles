---
name: api-workshop
description: >
  Design new APIs or review existing ones using debate-driven multi-agent workshop.
  Agents propose designs and challenge each other on consumer UX, domain modeling,
  security, performance, and standards compliance. Use when the user wants to design
  a new API, review an existing API, decide between REST/GraphQL, or improve API
  architecture. Keywords: api design, api review, rest api, graphql, openapi, api
  architecture, api specification, endpoint design, api standards.
context: fork
disable-model-invocation: true
argument-hint: [api-description or url]
---

# API Workshop

A debate-driven multi-agent workshop for designing and reviewing APIs. Five specialized
agents propose designs and challenge each other to produce a well-reasoned API specification.

## Prerequisites

Agents will need access to API design patterns and standards. The `REFERENCE.md` file
provides OpenAPI templates, design principles, and debate prompts.

## Inputs

The user provides:

1. **API Description** (required) — What the API should do, or URL to existing spec
2. **Context** (optional) — Business domain, constraints, existing systems
3. **Focus areas** (optional) — Which aspects matter most (see Agent Roster below)
4. **Format preference** (optional) — OpenAPI 3.x, GraphQL schema, AsyncAPI

If the user provides a URL to an existing spec, agents will review it rather than
design from scratch.

## Agent Roster

Each agent brings a specialized perspective and debates with others:

| # | Agent | Focus | Challenges |
|---|-------|-------|-----------|
| 1 | **API Designer** | Consumer UX, discoverability, naming | "Is this intuitive for developers?" |
| 2 | **Domain Modeler** | Correct modeling, consistency, DDD | "Does this match the domain?" |
| 3 | **Security Auditor** | Auth/authz, data exposure, OWASP | "What are the security risks?" |
| 4 | **Performance Analyst** | Efficiency, caching, over/under-fetching | "Will this scale?" |
| 5 | **Tech Lead** | Standards compliance, versioning, docs | "Does this follow best practices?" |

## Workflow

### Phase 1: Context Gathering (Main Agent)

Before spawning the workshop agents:

1. **If given a description**: Extract requirements, constraints, and success criteria
2. **If given a URL**: Fetch the existing API spec and summarize it
3. **Identify domain entities**: List the core resources/types involved
4. **Clarify open questions**: Ask user if anything is ambiguous
5. **Create initial context document**: `workspace/api-context.md`

### Phase 2: Initial Proposals (Sub-agents 1-5)

Spawn all five agents in parallel. Each receives:
- The context document from Phase 1
- Their agent instructions (from `agents/*.md`)
- The API design reference (`REFERENCE.md`)

Each agent independently:
1. Proposes an initial design approach
2. Creates example endpoint/schema definitions
3. Writes their rationale and concerns
4. Saves to `workspace/proposals/<agent-name>.md`

### Phase 3: Cross-Examination (Main Agent Orchestrates)

For each significant design decision, run a mini-debate:

1. **API Style** (REST vs GraphQL vs RPC)
   - API Designer proposes based on UX
   - Performance Analyst challenges based on query patterns
   - Tech Lead weighs standardization concerns

2. **Authentication Strategy** (OAuth2, API keys, JWT)
   - Security Auditor proposes approach
   - API Designer challenges if it adds friction
   - Tech Lead validates against standards

3. **Versioning Strategy** (URI, header, content negotiation)
   - Tech Lead proposes approach
   - API Designer challenges impact on consumers
   - Domain Modeler validates semantic compatibility

4. **Resource Design** (granularity, relationships, operations)
   - Domain Modeler proposes structure
   - Performance Analyst challenges N+1 issues
   - API Designer validates developer experience

5. **Error Handling** (status codes, error formats, problem details)
   - Security Auditor proposes secure defaults
   - API Designer ensures clarity for consumers
   - Tech Lead validates RFC 7807 compliance

For each debate:
- Present the question and stakes
- Let 2-3 agents argue their positions
- Synthesize the decision with rationale
- Document trade-offs considered

### Phase 4: Synthesis (Main Agent)

After all debates complete:

1. **Reconcile proposals**: Merge agent input into coherent design
2. **Resolve conflicts**: Make final calls on contested decisions
3. **Document rationale**: Explain why each choice was made
4. **Identify risks**: Note what could go wrong and mitigations
5. **Generate specification**: Create complete API spec in requested format

### Phase 5: Output

Generate the final deliverable following the template in `REFERENCE.md`:

1. **Executive Summary**: High-level design decisions and rationale
2. **Architecture**: API style, auth, versioning, error handling
3. **Specification**: Complete OpenAPI/GraphQL schema
4. **Design Rationale**: Why each major decision was made
5. **Trade-offs**: What was considered and rejected
6. **Implementation Notes**: Tips for backend developers
7. **Client Examples**: Sample requests/responses in multiple languages

Save to `workspace/api-specification.md` and present to the user.

## Debate Topics

The workshop should address these key decisions:

### API Style
- **REST**: Resource-oriented, HTTP semantics, wide tooling
- **GraphQL**: Flexible queries, type-safe, learning curve
- **RPC**: Simple, efficient, less discoverable

### Versioning
- **URI versioning**: `/v1/users` (explicit, breaks caching)
- **Header versioning**: `Accept: application/vnd.api+json;version=1` (clean URIs, harder to test)
- **Content negotiation**: Media types control breaking changes

### Authentication
- **OAuth2**: Standard, complex setup, great for delegated auth
- **API keys**: Simple, less secure, good for server-to-server
- **JWT**: Stateless, revocation challenges, flexible claims

### Pagination
- **Offset/limit**: Simple, inconsistent under writes
- **Cursor-based**: Consistent, opaque, harder to jump to page N
- **Keyset**: Efficient, requires indexed sort key

### Error Handling
- **Problem Details (RFC 7807)**: Structured, extensible, standard
- **Custom format**: Tailored to domain, non-standard
- **HTTP status only**: Simple, lacks detail

## Output Structure

```
workspace/
├── api-context.md                  # Phase 1 context gathering
├── proposals/
│   ├── api-designer.md
│   ├── domain-modeler.md
│   ├── security-auditor.md
│   ├── performance-analyst.md
│   └── tech-lead.md
├── debates/
│   ├── api-style-debate.md
│   ├── auth-strategy-debate.md
│   ├── versioning-debate.md
│   ├── resource-design-debate.md
│   └── error-handling-debate.md
└── api-specification.md            # Final deliverable
```

## Coordinator Responsibilities

1. Gather context and clarify requirements with user
2. Spawn proposal agents in parallel
3. Orchestrate debates on key design decisions
4. Ensure all agents engage (not just API Designer)
5. Synthesize final specification with rationale
6. Present deliverable to user
7. Offer to generate client SDKs or mock server if requested

## Customization

The user can customize the workshop by:

- **Skipping agents**: "Skip performance, focus on security"
- **Adding constraints**: "Must support GraphQL subscriptions"
- **Specifying style**: "Design a REST API following JSON:API spec"
- **Setting priorities**: "Optimize for developer experience over efficiency"
- **Providing examples**: "Similar to Stripe's API" or "Here's our existing API"
- **Requesting specific debates**: "Debate whether we need versioning at all"

Adapt the agent roster and debate topics accordingly.

## Example Invocations

```
/api-workshop design an API for a task management system

/api-workshop review https://api.example.com/openapi.json

/api-workshop design a GraphQL API for e-commerce with subscriptions

/api-workshop compare REST vs GraphQL for our social network
```

The workshop adapts to whether you're designing new, reviewing existing, or comparing alternatives.
