# /integration-test

Investigate and establish comprehensive integration testing strategies tailored to your project's architecture, dependencies, and technology stack.

## Usage

```
/integration-test [test-type]
/integration-test [service-name]
/integration-test
```

## Context Detection

**When no argument provided:**

- Analyzes project structure and dependencies
- Identifies integration points and external dependencies
- Suggests appropriate testing strategies for detected architecture

**When test type specified:**

- Focuses on specific integration testing pattern (api, database, messaging, etc.)
- Provides targeted setup and configuration guidance
- Includes relevant tools and frameworks

**When service specified:**

- Analyzes specific service integration requirements
- Maps service dependencies and communication patterns
- Creates service-specific test strategies

## Project Analysis and Discovery

### Technology Stack Detection

**Backend Frameworks**

```bash
# Language and framework detection
find . -name "package.json" -exec jq -r '.dependencies | keys[]' {} \; | sort | uniq
find . -name "Cargo.toml" -exec grep -A 5 "\[dependencies\]" {} \;
find . -name "pom.xml" -exec grep -A 2 "<artifactId>" {} \;
find . -name "go.mod" -exec grep "require" {} \;
```

**Database Dependencies**

- SQL databases: PostgreSQL, MySQL, SQLite detection
- NoSQL databases: MongoDB, Redis, DynamoDB discovery
- Time-series: InfluxDB, TimescaleDB identification
- Graph databases: Neo4j, ArangoDB detection

**Message Systems**

- Queue systems: RabbitMQ, Apache Kafka, AWS SQS
- Pub/Sub: Redis Pub/Sub, Google Pub/Sub, Apache Pulsar
- Event streaming: Apache Kafka, Amazon Kinesis
- Message brokers: ActiveMQ, Apache Qpid

**External Services**

- HTTP APIs: REST, GraphQL endpoint detection
- Authentication: OAuth, JWT, SAML integration points
- Payment systems: Stripe, PayPal, payment gateway APIs
- Third-party services: Email, SMS, cloud storage APIs

### Architecture Pattern Recognition

**Microservices Architecture**

```yaml
# Service discovery through docker-compose, kubernetes manifests
services:
  user-service:
    image: user-service:latest
    depends_on:
      - postgres
      - redis

  order-service:
    image: order-service:latest
    depends_on:
      - postgres
      - message-queue
```

**Monolithic Applications**

- Single deployment unit with multiple modules
- Shared database with multiple schemas
- Internal API boundaries and module interfaces
- Background job and task processing systems

**Event-Driven Systems**

- Event sourcing pattern detection
- CQRS implementation identification
- Saga pattern usage discovery
- Event store and projection analysis

## Integration Testing Strategies

### API Integration Testing

**REST API Testing**

```javascript
// Jest + Supertest pattern
const request = require("supertest");
const app = require("../app");

describe("User API Integration", () => {
  beforeAll(async () => {
    // Setup test database and dependencies
    await setupTestDatabase();
    await startTestServices();
  });

  test("POST /users creates user and returns 201", async () => {
    const userData = { name: "Test User", email: "test@example.com" };

    const response = await request(app)
      .post("/users")
      .send(userData)
      .expect(201);

    expect(response.body).toMatchObject(userData);

    // Verify database persistence
    const user = await User.findById(response.body.id);
    expect(user).toBeTruthy();
  });
});
```

**GraphQL API Testing**

```javascript
// GraphQL integration testing
const { createTestClient } = require("apollo-server-testing");
const { server } = require("../server");

const { query, mutate } = createTestClient(server);

test("queries user data correctly", async () => {
  const GET_USER = gql`
    query GetUser($id: ID!) {
      user(id: $id) {
        id
        name
        email
      }
    }
  `;

  const { data } = await query({
    query: GET_USER,
    variables: { id: "test-user-id" },
  });

  expect(data.user).toMatchSnapshot();
});
```

### Database Integration Testing

**Relational Database Testing**

```python
# pytest + SQLAlchemy pattern
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from myapp.models import Base, User
from myapp.database import get_db

@pytest.fixture(scope="session")
def test_db():
    # Create test database
    engine = create_engine("postgresql://test:test@localhost/test_db")
    Base.metadata.create_all(engine)
    
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    yield TestingSessionLocal
    
    # Cleanup
    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session(test_db):
    session = test_db()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

def test_user_creation_integration(db_session):
    # Test database operations with real DB
    user = User(name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    
    retrieved_user = db_session.query(User).filter_by(email="test@example.com").first()
    assert retrieved_user is not None
    assert retrieved_user.name == "Test User"
```

**NoSQL Database Testing**

```javascript
// MongoDB integration testing
const { MongoMemoryServer } = require("mongodb-memory-server");
const mongoose = require("mongoose");
const User = require("../models/User");

describe("User Model Integration", () => {
  let mongoServer;

  beforeAll(async () => {
    mongoServer = await MongoMemoryServer.create();
    const uri = mongoServer.getUri();
    await mongoose.connect(uri);
  });

  afterAll(async () => {
    await mongoose.disconnect();
    await mongoServer.stop();
  });

  beforeEach(async () => {
    await User.deleteMany({});
  });

  test("user creation with validation", async () => {
    const userData = {
      name: "Test User",
      email: "test@example.com",
      preferences: { theme: "dark" },
    };

    const user = await User.create(userData);
    expect(user._id).toBeDefined();
    expect(user.preferences.theme).toBe("dark");
  });
});
```

### Message Queue Integration Testing

**RabbitMQ Testing**

```python
# Celery + RabbitMQ integration testing
import pytest
from celery import Celery
from myapp.tasks import process_order, send_email

@pytest.fixture
def celery_app():
    app = Celery('test_app')
    app.config_from_object({
        'broker_url': 'memory://',
        'result_backend': 'cache+memory://',
        'task_always_eager': True,  # Execute tasks synchronously
    })
    return app

def test_order_processing_workflow(celery_app):
    # Test message queue workflow
    order_data = {'id': 123, 'items': ['item1', 'item2']}
    
    # This should trigger a chain of tasks
    result = process_order.delay(order_data)
    
    assert result.successful()
    assert result.result['status'] == 'processed'
    
    # Verify side effects (email sent, inventory updated)
    # This tests the entire message flow
```

**Kafka Integration Testing**

```java
// Spring Kafka integration testing
@SpringBootTest
@TestPropertySource(properties = {
    "spring.kafka.bootstrap-servers=${spring.embedded.kafka.brokers}",
    "spring.kafka.consumer.auto-offset-reset=earliest"
})
@EmbeddedKafka(partitions = 1, topics = {"user-events", "order-events"})
class KafkaIntegrationTest {
    
    @Autowired
    private UserEventProducer producer;
    
    @Autowired
    private OrderEventConsumer consumer;
    
    @Test
    void testUserEventProcessing() throws InterruptedException {
        UserEvent event = new UserEvent("user123", "USER_CREATED");
        
        producer.sendUserEvent(event);
        
        // Wait for consumer to process
        Thread.sleep(1000);
        
        // Verify processing results
        List<ProcessedEvent> processed = consumer.getProcessedEvents();
        assertThat(processed).hasSize(1);
        assertThat(processed.get(0).getUserId()).isEqualTo("user123");
    }
}
```

### External Service Integration Testing

**HTTP Service Mocking**

```python
# Using responses library for HTTP mocking
import responses
import requests
from myapp.services import PaymentService

@responses.activate
def test_payment_processing_integration():
    # Mock external payment API
    responses.add(
        responses.POST,
        'https://api.stripe.com/v1/charges',
        json={'id': 'ch_test123', 'status': 'succeeded'},
        status=200
    )
    
    payment_service = PaymentService()
    result = payment_service.process_payment({
        'amount': 1000,
        'currency': 'usd',
        'source': 'tok_test'
    })
    
    assert result['status'] == 'succeeded'
    assert len(responses.calls) == 1
```

**Contract Testing**

```javascript
// Pact.js for consumer-driven contract testing
const { Pact } = require("@pact-foundation/pact");
const path = require("path");

const provider = new Pact({
  consumer: "user-service",
  provider: "payment-service",
  port: 1234,
  log: path.resolve(process.cwd(), "logs", "pact.log"),
  dir: path.resolve(process.cwd(), "pacts"),
});

describe("Payment Service Contract", () => {
  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());

  test("processes payment successfully", async () => {
    await provider.addInteraction({
      state: "user has valid payment method",
      uponReceiving: "a payment request",
      withRequest: {
        method: "POST",
        path: "/payments",
        headers: { "Content-Type": "application/json" },
        body: { amount: 100, currency: "USD" },
      },
      willRespondWith: {
        status: 200,
        headers: { "Content-Type": "application/json" },
        body: { id: "payment-123", status: "completed" },
      },
    });

    // Test your service against the mock
    const response = await makePayment({ amount: 100, currency: "USD" });
    expect(response.status).toBe("completed");
  });
});
```

## Environment and Infrastructure Setup

### Test Database Management

**Docker-based Test Databases**

```yaml
# docker-compose.test.yml
version: "3.8"
services:
  test-postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_pass
    ports:
      - "5433:5432"

  test-redis:
    image: redis:6-alpine
    ports:
      - "6380:6379"

  test-kafka:
    image: confluentinc/cp-kafka:latest
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9093
    ports:
      - "9093:9092"
```

**In-Memory Alternatives**

- H2 Database for JVM applications
- SQLite for file-based testing
- MongoDB Memory Server for Node.js
- Redis mock for Python applications

### Test Data Management

**Data Fixtures and Factories**

```python
# Factory Boy for test data generation
import factory
from myapp.models import User, Order

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    name = factory.Faker('name')
    email = factory.Faker('email')
    created_at = factory.Faker('date_time')

class OrderFactory(factory.Factory):
    class Meta:
        model = Order
    
    user = factory.SubFactory(UserFactory)
    total = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    status = 'pending'

# Usage in tests
def test_order_processing():
    user = UserFactory()
    order = OrderFactory(user=user, total=100.00)
    # Test logic here
```

**Database Seeding Scripts**

```sql
-- seed-test-data.sql
INSERT INTO users (id, name, email, created_at) VALUES
(1, 'Test User 1', 'user1@test.com', NOW()),
(2, 'Test User 2', 'user2@test.com', NOW());

INSERT INTO orders (id, user_id, total, status) VALUES
(1, 1, 99.99, 'completed'),
(2, 2, 149.50, 'pending');
```

### Service Virtualization

**WireMock for HTTP Services**

```java
@Test
void testExternalServiceIntegration() {
    // Setup WireMock
    WireMockServer wireMockServer = new WireMockServer(8089);
    wireMockServer.start();
    
    // Stub external service
    wireMockServer.stubFor(get(urlEqualTo("/api/users/123"))
        .willReturn(aResponse()
            .withStatus(200)
            .withHeader("Content-Type", "application/json")
            .withBody("{\"id\": 123, \"name\": \"Test User\"}")));
    
    // Test your service
    UserService service = new UserService("http://localhost:8089");
    User user = service.getUser(123);
    
    assertThat(user.getName()).isEqualTo("Test User");
    
    wireMockServer.stop();
}
```

**Test Containers**

```java
// Testcontainers for integration testing
@Testcontainers
class DatabaseIntegrationTest {
    
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:13")
            .withDatabaseName("testdb")
            .withUsername("test")
            .withPassword("test");
    
    @Test
    void testDatabaseOperations() {
        String jdbcUrl = postgres.getJdbcUrl();
        // Use real database for testing
        // Connection and test logic here
    }
}
```

## Framework-Specific Implementations

### Node.js/JavaScript

**Jest + Testing Library**

```javascript
// Integration test setup
const { setupServer } = require("msw/node");
const { rest } = require("msw");

const server = setupServer(
  rest.get("/api/users/:id", (req, res, ctx) => {
    return res(ctx.json({ id: req.params.id, name: "Test User" }));
  }),
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Python

**pytest + FastAPI**

```python
# conftest.py
import pytest
from fastapi.testclient import TestClient
from myapp.main import app
from myapp.database import get_db, engine
from myapp.models import Base

@pytest.fixture(scope="session")
def test_app():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_app):
    return test_app
```

### Java/Spring

**Spring Boot Test**

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureMockMvc
class UserControllerIntegrationTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Autowired
    private UserRepository userRepository;
    
    @Test
    @Transactional
    void createUserIntegrationTest() throws Exception {
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\":\"Test User\",\"email\":\"test@example.com\"}"))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.name").value("Test User"));
        
        // Verify database state
        List<User> users = userRepository.findAll();
        assertThat(users).hasSize(1);
    }
}
```

### Go

**Testing with Testify**

```go
// integration_test.go
func TestUserAPIIntegration(t *testing.T) {
    // Setup test database
    db := setupTestDB(t)
    defer cleanupTestDB(t, db)
    
    // Setup HTTP server
    server := httptest.NewServer(setupRoutes(db))
    defer server.Close()
    
    // Test user creation
    userData := `{"name":"Test User","email":"test@example.com"}`
    resp, err := http.Post(server.URL+"/users", "application/json", strings.NewReader(userData))
    
    assert.NoError(t, err)
    assert.Equal(t, http.StatusCreated, resp.StatusCode)
    
    // Verify database state
    var user User
    err = db.First(&user, "email = ?", "test@example.com").Error
    assert.NoError(t, err)
    assert.Equal(t, "Test User", user.Name)
}
```

### Rust

**Integration Testing with Tokio**

```rust
// tests/integration_test.rs
use tokio_test;
use myapp::{create_app, TestDatabase};

#[tokio::test]
async fn test_user_creation_integration() {
    let test_db = TestDatabase::new().await;
    let app = create_app(test_db.pool()).await;
    
    let response = app
        .oneshot(
            Request::builder()
                .method(http::Method::POST)
                .uri("/users")
                .header(http::header::CONTENT_TYPE, mime::APPLICATION_JSON.as_ref())
                .body(Body::from(r#"{"name":"Test User","email":"test@example.com"}"#))
                .unwrap(),
        )
        .await
        .unwrap();
    
    assert_eq!(response.status(), StatusCode::CREATED);
    
    // Verify database state
    let user = sqlx::query_as!(
        User,
        "SELECT id, name, email FROM users WHERE email = $1",
        "test@example.com"
    )
    .fetch_one(&test_db.pool())
    .await
    .unwrap();
    
    assert_eq!(user.name, "Test User");
}
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Integration Tests

on: [push, pull_request]

jobs:
  integration-tests:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v2

      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: "16"

      - name: Install dependencies
        run: npm ci

      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgres://postgres:test@localhost:5432/test_db
```

### Test Reporting and Coverage

**Coverage Integration**

```bash
# JavaScript/Node.js
npm run test:integration -- --coverage --coverageReporters=lcov

# Python
coverage run -m pytest tests/integration/
coverage report --show-missing

# Java/Maven
mvn test jacoco:report

# Go
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

## Best Practices and Recommendations

### Test Organization

- Separate unit, integration, and end-to-end tests
- Use consistent naming conventions
- Group tests by feature or service
- Maintain test data isolation

### Performance Considerations

- Use connection pooling for databases
- Implement parallel test execution where possible
- Cache common setup operations
- Use fast in-memory alternatives when appropriate

### Maintenance Strategy

- Regular dependency updates
- Test data refresh procedures
- Performance benchmarking
- Documentation updates

The command provides a comprehensive integration testing strategy tailored to your specific technology stack, architecture patterns, and deployment requirements.
