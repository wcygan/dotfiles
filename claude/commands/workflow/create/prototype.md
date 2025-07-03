# /prototype

Quickly create a working proof-of-concept implementation to validate ideas, test hypotheses, or demonstrate functionality.

## Usage

```
/prototype [feature or concept description]
```

## Prototyping Process

### 1. Rapid Setup

```bash
# Create isolated prototype environment
mkdir prototype-${FEATURE_NAME}
cd prototype-${FEATURE_NAME}

# Initialize based on requirements
deno init  # For Deno projects
cargo init # For Rust projects
go mod init prototype # For Go projects
```

### 2. Prototype Templates

#### Web API Prototype (Deno Fresh)

```typescript
// main.ts - Minimal API prototype
import { serve } from "@std/http/server.ts";

const handler = async (req: Request): Promise<Response> => {
  const url = new URL(req.url);

  if (url.pathname === "/api/demo" && req.method === "POST") {
    const data = await req.json();
    // Prototype logic here
    return Response.json({
      success: true,
      processed: data,
      timestamp: new Date().toISOString(),
    });
  }

  return new Response("Prototype API", { status: 200 });
};

console.log("Prototype running on http://localhost:8000");
await serve(handler);
```

#### CLI Tool Prototype (Rust)

```rust
// src/main.rs - Quick CLI prototype
use clap::Parser;
use anyhow::Result;

#[derive(Parser)]
#[command(name = "prototype")]
#[command(about = "A prototype CLI tool")]
struct Args {
    /// Input file to process
    #[arg(short, long)]
    input: String,
    
    /// Enable verbose output
    #[arg(short, long)]
    verbose: bool,
}

fn main() -> Result<()> {
    let args = Args::parse();
    
    println!("Processing: {}", args.input);
    
    // Prototype logic here
    let result = process_file(&args.input)?;
    
    println!("Result: {:?}", result);
    Ok(())
}

fn process_file(path: &str) -> Result<String> {
    // Mock implementation
    Ok(format!("Processed {}", path))
}
```

#### Data Pipeline Prototype (Python/Deno)

```typescript
// pipeline.ts - Stream processing prototype
import { readLines } from "@std/io/read_lines.ts";

async function* processStream(input: AsyncIterable<string>) {
  for await (const line of input) {
    // Transform logic
    const processed = line.toUpperCase().trim();
    if (processed.length > 0) {
      yield {
        original: line,
        processed,
        timestamp: Date.now(),
      };
    }
  }
}

// Usage
const file = await Deno.open("input.txt");
const lines = readLines(file);

for await (const result of processStream(lines)) {
  console.log(JSON.stringify(result));
}
```

### 3. Quick Integration Prototypes

#### Database Connection

```typescript
// Quick PostgreSQL prototype
import { Client } from "https://deno.land/x/postgres/mod.ts";

const client = new Client({
  user: "prototype",
  database: "prototype_db",
  hostname: "localhost",
  port: 5432,
});

await client.connect();

// Test query
const result = await client.queryObject`
  SELECT * FROM users WHERE active = true LIMIT 5
`;

console.log("Sample data:", result.rows);
```

#### Message Queue

```go
// Quick Redis Pub/Sub prototype
package main

import (
    "fmt"
    "github.com/redis/go-redis/v9"
    "context"
)

func main() {
    ctx := context.Background()
    rdb := redis.NewClient(&redis.Options{
        Addr: "localhost:6379",
    })

    // Publisher prototype
    go func() {
        for i := 0; i < 10; i++ {
            rdb.Publish(ctx, "prototype-channel", fmt.Sprintf("Message %d", i))
            time.Sleep(time.Second)
        }
    }()

    // Subscriber prototype
    sub := rdb.Subscribe(ctx, "prototype-channel")
    for msg := range sub.Channel() {
        fmt.Printf("Received: %s\n", msg.Payload)
    }
}
```

### 4. UI Prototypes

#### React Component (Quick)

```jsx
// PrototypeComponent.jsx
export default function PrototypeFeature({ data }) {
  const [state, setState] = useState(data);
  const [loading, setLoading] = useState(false);

  const handleAction = async () => {
    setLoading(true);
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000));
    setState((prev) => ({ ...prev, updated: Date.now() }));
    setLoading(false);
  };

  return (
    <div style={{ padding: 20, border: "1px solid #ccc" }}>
      <h3>Prototype: {state.name}</h3>
      <pre>{JSON.stringify(state, null, 2)}</pre>
      <button onClick={handleAction} disabled={loading}>
        {loading ? "Processing..." : "Test Action"}
      </button>
    </div>
  );
}
```

### 5. Algorithm Prototypes

```typescript
// algorithm-prototype.ts
function prototypeAlgorithm(input: number[]): {
  result: number[];
  metrics: {
    iterations: number;
    comparisons: number;
    timeMs: number;
  };
} {
  const start = performance.now();
  let iterations = 0;
  let comparisons = 0;

  // Prototype algorithm implementation
  const result = [...input];

  for (let i = 0; i < result.length; i++) {
    iterations++;
    for (let j = i + 1; j < result.length; j++) {
      comparisons++;
      if (result[i] > result[j]) {
        [result[i], result[j]] = [result[j], result[i]];
      }
    }
  }

  return {
    result,
    metrics: {
      iterations,
      comparisons,
      timeMs: performance.now() - start,
    },
  };
}

// Test with sample data
const testData = Array.from({ length: 100 }, () => Math.random() * 1000);
const output = prototypeAlgorithm(testData);
console.log("Metrics:", output.metrics);
```

### 6. Validation & Metrics

```typescript
// prototype-test.ts
Deno.test("Prototype validation", async (t) => {
  await t.step("performance baseline", () => {
    const start = performance.now();
    const result = prototypeFunction(testInput);
    const duration = performance.now() - start;

    assert(duration < 100, `Too slow: ${duration}ms`);
    assertEquals(result.length, expectedLength);
  });

  await t.step("edge cases", () => {
    assertDoesNotThrow(() => prototypeFunction([]));
    assertDoesNotThrow(() => prototypeFunction(null));
  });
});
```

## Output Format

````markdown
## Prototype: [Feature Name]

**Status:** Working Prototype
**Time to Build:** X minutes
**Dependencies:** [List key dependencies]

### What Works:

- ✅ Core functionality implemented
- ✅ Basic error handling
- ✅ Sample data processing

### Limitations:

- ⚠️ No authentication
- ⚠️ In-memory storage only
- ⚠️ Limited error handling

### Performance Metrics:

- Throughput: X ops/second
- Memory usage: Y MB
- Response time: Z ms

### How to Run:

```bash
# Clone and setup
git clone [prototype-repo]
cd prototype-dir

# Install and run
[package manager] install
[run command]

# Test endpoints
curl -X POST http://localhost:8000/api/demo \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```
````

### Next Steps:

1. Add authentication layer
2. Implement persistent storage
3. Add comprehensive error handling
4. Create production configuration
5. Add monitoring/logging

### Key Code:

[Include 1-2 most important code snippets]

### Learnings:

- [Technical insight 1]
- [Technical insight 2]
- [Risk or concern discovered]

```
## Prototype Strategies

1. **Time-boxed**: Limit to 2-4 hours max
2. **Feature-focused**: One core feature only
3. **Mock external dependencies**: Use in-memory/fake services
4. **Hardcode config**: No complex configuration
5. **Skip edge cases**: Happy path only
6. **Document assumptions**: List what's not handled

## Common Prototypes

- API endpoint with mock data
- CLI tool with basic functionality  
- Data processing pipeline
- Authentication flow
- Real-time websocket connection
- Background job processor
- Integration with third-party service

## Guidelines

- Start with the smallest possible implementation
- Use familiar tools for speed
- Copy/paste liberally from docs
- Don't worry about code quality initially
- Focus on proving the concept
- Measure key metrics early
- Document limitations clearly
```
