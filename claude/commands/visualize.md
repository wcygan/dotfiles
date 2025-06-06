# /visualize

Analyzes code and architecture to generate explanatory diagrams.

## Usage
```
/visualize <target>
/visualize <target> --type <flowchart|sequence|erd|architecture>
/visualize <target> --format <mermaid|plantuml|graphviz>
/visualize <target> --output <file.md>
```

**Default Output Location**: `/docs/diagrams/` directory

## Description
This command transforms complex code, logic, and system architectures into clear, visual diagrams. A picture is worth a thousand lines of code - this command makes systems easier to understand, debug, and communicate about.

### What it generates:

#### 1. Code Flow Visualization
Analyzes function and method logic to create flowcharts:

**Function Analysis:**
```go
// Example Go function
func ProcessPayment(userID string, amount float64, paymentMethod string) (*Payment, error) {
    user, err := GetUser(userID)
    if err != nil {
        return nil, fmt.Errorf("user not found: %w", err)
    }
    
    if user.Balance < amount {
        return nil, errors.New("insufficient funds")
    }
    
    if paymentMethod == "credit_card" {
        if !ValidateCreditCard(user.CreditCard) {
            return nil, errors.New("invalid credit card")
        }
    }
    
    payment := &Payment{
        UserID: userID,
        Amount: amount,
        Method: paymentMethod,
        Status: "pending",
    }
    
    if err := SavePayment(payment); err != nil {
        return nil, fmt.Errorf("failed to save payment: %w", err)
    }
    
    if err := ProcessExternalPayment(payment); err != nil {
        payment.Status = "failed"
        SavePayment(payment)
        return nil, fmt.Errorf("external payment failed: %w", err)
    }
    
    payment.Status = "completed"
    SavePayment(payment)
    
    return payment, nil
}
```

**Generated Flowchart:**
```mermaid
flowchart TD
    A[Start: ProcessPayment] --> B[Get User by ID]
    B --> C{User Found?}
    C -->|No| D[Return Error: User Not Found]
    C -->|Yes| E{Sufficient Balance?}
    E -->|No| F[Return Error: Insufficient Funds]
    E -->|Yes| G{Payment Method == Credit Card?}
    G -->|Yes| H[Validate Credit Card]
    H --> I{Valid Credit Card?}
    I -->|No| J[Return Error: Invalid Credit Card]
    I -->|Yes| K[Create Payment Object]
    G -->|No| K
    K --> L[Save Payment to Database]
    L --> M{Save Successful?}
    M -->|No| N[Return Error: Save Failed]
    M -->|Yes| O[Process External Payment]
    O --> P{External Payment Successful?}
    P -->|No| Q[Update Status to Failed]
    Q --> R[Save Updated Payment]
    R --> S[Return Error: External Payment Failed]
    P -->|Yes| T[Update Status to Completed]
    T --> U[Save Updated Payment]
    U --> V[Return Successful Payment]
    
    style A fill:#e1f5fe
    style D fill:#ffebee
    style F fill:#ffebee
    style J fill:#ffebee
    style N fill:#ffebee
    style S fill:#ffebee
    style V fill:#e8f5e8
```

#### 2. Database Schema Visualization
Analyzes database schemas and models to create Entity Relationship Diagrams:

**Go Struct Analysis:**
```go
type User struct {
    ID        int64     `db:"id" json:"id"`
    Email     string    `db:"email" json:"email"`
    Name      string    `db:"name" json:"name"`
    CreatedAt time.Time `db:"created_at" json:"created_at"`
    Profile   *Profile  `db:"-" json:"profile,omitempty"`
    Orders    []Order   `db:"-" json:"orders,omitempty"`
}

type Profile struct {
    ID     int64  `db:"id" json:"id"`
    UserID int64  `db:"user_id" json:"user_id"`
    Bio    string `db:"bio" json:"bio"`
    Avatar string `db:"avatar" json:"avatar"`
}

type Order struct {
    ID       int64     `db:"id" json:"id"`
    UserID   int64     `db:"user_id" json:"user_id"`
    Total    float64   `db:"total" json:"total"`
    Status   string    `db:"status" json:"status"`
    Items    []Item    `db:"-" json:"items,omitempty"`
}

type Item struct {
    ID       int64   `db:"id" json:"id"`
    OrderID  int64   `db:"order_id" json:"order_id"`
    Name     string  `db:"name" json:"name"`
    Price    float64 `db:"price" json:"price"`
    Quantity int     `db:"quantity" json:"quantity"`
}
```

**Generated ERD:**
```mermaid
erDiagram
    USER {
        int64 id PK
        string email UK
        string name
        timestamp created_at
    }
    
    PROFILE {
        int64 id PK
        int64 user_id FK
        string bio
        string avatar
    }
    
    ORDER {
        int64 id PK
        int64 user_id FK
        float64 total
        string status
        timestamp created_at
    }
    
    ITEM {
        int64 id PK
        int64 order_id FK
        string name
        float64 price
        int quantity
    }
    
    USER ||--o| PROFILE : "has one"
    USER ||--o{ ORDER : "has many"
    ORDER ||--o{ ITEM : "contains many"
```

#### 3. System Architecture Diagrams
Analyzes microservices and system interactions:

**Service Discovery:**
```yaml
# docker-compose.yml analysis
services:
  auth-service:
    image: auth:latest
    ports: ["8080:8080"]
    depends_on: [postgres, redis]
    
  user-service:
    image: user:latest
    ports: ["8081:8081"]
    depends_on: [postgres, auth-service]
    
  payment-service:
    image: payment:latest
    ports: ["8082:8082"]
    depends_on: [postgres, user-service]
    
  api-gateway:
    image: nginx:latest
    ports: ["80:80"]
    depends_on: [auth-service, user-service, payment-service]
```

**Generated Architecture Diagram:**
```mermaid
graph TB
    subgraph "External"
        Client[Client Apps]
        PaymentProvider[Payment Provider API]
    end
    
    subgraph "API Layer"
        Gateway[API Gateway :80]
    end
    
    subgraph "Application Services"
        Auth[Auth Service :8080]
        User[User Service :8081]
        Payment[Payment Service :8082]
    end
    
    subgraph "Data Layer"
        DB[(PostgreSQL)]
        Cache[(Redis)]
    end
    
    Client --> Gateway
    Gateway --> Auth
    Gateway --> User
    Gateway --> Payment
    
    Auth --> DB
    Auth --> Cache
    User --> DB
    User --> Auth
    Payment --> DB
    Payment --> User
    Payment --> PaymentProvider
    
    style Client fill:#e3f2fd
    style Gateway fill:#f3e5f5
    style Auth fill:#e8f5e8
    style User fill:#e8f5e8
    style Payment fill:#e8f5e8
    style DB fill:#fff3e0
    style Cache fill:#fce4ec
```

#### 4. API Interaction Sequences
Analyzes API calls and interactions to create sequence diagrams:

**REST API Flow Analysis:**
```go
// Analyzed from HTTP handlers and client code
func HandleUserRegistration(w http.ResponseWriter, r *http.Request) {
    // 1. Validate input
    user := parseUserFromRequest(r)
    
    // 2. Check if user exists
    existingUser := userService.GetByEmail(user.Email)
    
    // 3. Create user
    newUser := userService.Create(user)
    
    // 4. Send welcome email
    emailService.SendWelcomeEmail(newUser.Email)
    
    // 5. Create audit log
    auditService.LogUserCreation(newUser.ID)
}
```

**Generated Sequence Diagram:**
```mermaid
sequenceDiagram
    participant Client
    participant API as API Gateway
    participant Auth as Auth Service
    participant User as User Service
    participant Email as Email Service
    participant Audit as Audit Service
    participant DB as Database
    
    Client->>+API: POST /api/users/register
    API->>+Auth: Validate API Key
    Auth->>-API: Valid
    
    API->>+User: Create User Request
    User->>+DB: Check if email exists
    DB->>-User: Email available
    
    User->>+DB: Insert new user
    DB->>-User: User created (ID: 123)
    
    User->>+Email: Send welcome email
    Email-->>-User: Email queued
    
    User->>+Audit: Log user creation
    Audit->>+DB: Insert audit record
    DB->>-Audit: Audit logged
    Audit-->>-User: Logged
    
    User->>-API: User created successfully
    API->>-Client: 201 Created
    
    Note over Email: Async email processing
    Email->>Email: Process welcome email
```

#### 5. Class and Module Relationships
Analyzes object-oriented code to show inheritance and composition:

**Rust Trait Analysis:**
```rust
trait Drawable {
    fn draw(&self);
}

trait Clickable {
    fn on_click(&self);
}

struct Button {
    text: String,
    position: Point,
}

struct Image {
    src: String,
    position: Point,
}

struct Panel {
    children: Vec<Box<dyn Drawable>>,
}

impl Drawable for Button {
    fn draw(&self) { /* implementation */ }
}

impl Clickable for Button {
    fn on_click(&self) { /* implementation */ }
}

impl Drawable for Image {
    fn draw(&self) { /* implementation */ }
}

impl Drawable for Panel {
    fn draw(&self) {
        for child in &self.children {
            child.draw();
        }
    }
}
```

**Generated Class Diagram:**
```mermaid
classDiagram
    class Drawable {
        <<trait>>
        +draw()
    }
    
    class Clickable {
        <<trait>>
        +on_click()
    }
    
    class Point {
        +x: i32
        +y: i32
    }
    
    class Button {
        +text: String
        +position: Point
        +draw()
        +on_click()
    }
    
    class Image {
        +src: String
        +position: Point
        +draw()
    }
    
    class Panel {
        +children: Vec~Box~dyn Drawable~~
        +draw()
    }
    
    Drawable <|.. Button : implements
    Clickable <|.. Button : implements
    Drawable <|.. Image : implements
    Drawable <|.. Panel : implements
    
    Button --> Point : contains
    Image --> Point : contains
    Panel --> Drawable : contains
```

### 6. Network and Infrastructure Diagrams
Analyzes Kubernetes manifests and infrastructure code:

**Kubernetes Deployment Analysis:**
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: web
        image: nginx:latest
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web-app
  ports:
  - port: 80
    targetPort: 80
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
spec:
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        backend:
          service:
            name: web-service
            port:
              number: 80
```

**Generated Infrastructure Diagram:**
```mermaid
graph TB
    subgraph "Internet"
        Users[Users]
    end
    
    subgraph "Kubernetes Cluster"
        subgraph "Ingress"
            Ingress[Ingress Controller<br/>app.example.com]
        end
        
        subgraph "Services"
            Service[web-service<br/>ClusterIP:80]
        end
        
        subgraph "Pods"
            Pod1[web-app-pod-1<br/>nginx:latest]
            Pod2[web-app-pod-2<br/>nginx:latest]
            Pod3[web-app-pod-3<br/>nginx:latest]
        end
    end
    
    Users --> Ingress
    Ingress --> Service
    Service --> Pod1
    Service --> Pod2
    Service --> Pod3
    
    style Users fill:#e3f2fd
    style Ingress fill:#f3e5f5
    style Service fill:#e8f5e8
    style Pod1 fill:#fff3e0
    style Pod2 fill:#fff3e0
    style Pod3 fill:#fff3e0
```

## Output Formats

### Mermaid (Default)
Generates Mermaid.js diagrams that render in GitHub, GitLab, and VS Code:
```markdown
# Function Flow Analysis

```mermaid
flowchart TD
    A[Start] --> B[Process]
    B --> C[End]
```
```

### PlantUML
Generates PlantUML diagrams for complex enterprise architectures:
```plantuml
@startuml
title Payment Processing Sequence

actor User
participant "Web App" as App
participant "Payment Service" as Payment
participant "Bank API" as Bank

User -> App: Submit Payment
App -> Payment: Process Payment Request
Payment -> Bank: Charge Credit Card
Bank --> Payment: Payment Confirmed
Payment --> App: Payment Success
App --> User: Display Confirmation

@enduml
```

### Graphviz DOT
Generates DOT files for complex dependency graphs:
```dot
digraph Dependencies {
    rankdir=TB;
    node [shape=box];
    
    "auth-service" -> "database";
    "user-service" -> "auth-service";
    "user-service" -> "database";
    "payment-service" -> "user-service";
    "api-gateway" -> "auth-service";
    "api-gateway" -> "user-service";
    "api-gateway" -> "payment-service";
}
```

## Examples

### Visualize a function:
```
/visualize ./src/payment.go:ProcessPayment
```

### Create database ERD:
```
/visualize ./models --type erd
```

### Generate system architecture:
```
/visualize ./docker-compose.yml --type architecture
```

### Create API sequence diagram:
```
/visualize ./api/handlers --type sequence
```

### Output to specific file:
```
/visualize ./src/auth.rs --output docs/diagrams/auth-flow.md
```

### Default outputs (created automatically):
```
/visualize ./src/payment.go          # Creates docs/diagrams/payment-flow.md
/visualize ./models --type erd       # Creates docs/diagrams/database-schema.md
/visualize ./docker-compose.yml     # Creates docs/diagrams/system-architecture.md
```

## File Structure Created
```
project-root/
└── docs/
    └── diagrams/
        ├── payment-flow.md          # Function flowcharts
        ├── database-schema.md       # Entity relationship diagrams  
        ├── system-architecture.md   # System and service diagrams
        ├── api-sequences.md         # API interaction sequences
        ├── class-relationships.md   # Class and module diagrams
        └── infrastructure.md        # Kubernetes and infrastructure
```

## Advanced Features

### Interactive Diagrams
Generates interactive diagrams with clickable elements:
```mermaid
flowchart TD
    A["Start"] --> B["Process"]
    B --> C["End"]
    
    click A "https://github.com/org/repo/blob/main/src/start.go" "View Source"
    click B "https://github.com/org/repo/blob/main/src/process.go" "View Source"
    click C "https://github.com/org/repo/blob/main/src/end.go" "View Source"
```

### Complexity Analysis
Annotates diagrams with complexity metrics:
```mermaid
flowchart TD
    A["Login Function<br/>Complexity: 3"] --> B{"Valid User?"}
    B -->|Yes| C["Success<br/>Path: 1"]
    B -->|No| D["Retry<br/>Path: 2"]
    D --> E{"Max Retries?"}
    E -->|Yes| F["Lock Account<br/>Path: 3"]
    E -->|No| A
```

### Dependency Analysis
Shows dependency relationships and potential circular dependencies:
```mermaid
graph TD
    A[auth] --> B[database]
    C[user] --> A
    C --> B
    D[payment] --> C
    E[notification] --> C
    F[api] --> A
    F --> C
    F --> D
    F --> E
    
    style A fill:#ff9999
    style C fill:#ff9999
    
    classDef warning fill:#ffeb3b,stroke:#f57f17,stroke-width:2px
    class A,C warning
```

## Integration with Other Commands
- Use with `/document` to include diagrams in generated documentation
- Combine with `/refactor` to visualize before/after architecture changes
- Use with `/review` to create visual explanations for code reviews
- Integrate with `/epic` to show system-wide architectural changes