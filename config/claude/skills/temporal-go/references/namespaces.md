# Namespaces

**Source**: https://docs.temporal.io/develop/go/namespaces

Namespaces provide isolation between workflows. Each workflow runs within a namespace. The `default` namespace is created automatically on self-hosted clusters.

## Namespace Client

```go
import "go.temporal.io/sdk/client"

// Create a namespace client (separate from the workflow client)
nc, err := client.NewNamespaceClient(client.Options{
    HostPort: "localhost:7233",
})
if err != nil {
    log.Fatal(err)
}
defer nc.Close()
```

## Register a Namespace

```go
import (
    "go.temporal.io/api/enums/v1"
    enumspb "go.temporal.io/api/enums/v1"
)

err = nc.Register(context.Background(), &workflowservice.RegisterNamespaceRequest{
    Namespace:                        "my-namespace",
    WorkflowExecutionRetentionPeriod: durationpb.New(3 * 24 * time.Hour), // required
    Description:                      "Production workflows",
    OwnerEmail:                       "team@example.com",
})
```

**Retention period is required** — minimum 1 day. Closed workflow history is deleted after this period.

## Describe a Namespace

```go
resp, err := nc.Describe(context.Background(), "my-namespace")
if err != nil {
    log.Fatal(err)
}
fmt.Println("Namespace:", resp.NamespaceInfo.Name)
fmt.Println("State:", resp.NamespaceInfo.State)
fmt.Println("Retention:", resp.Config.WorkflowExecutionRetentionTtl)
```

## Update a Namespace

```go
err = nc.Update(context.Background(), &workflowservice.UpdateNamespaceRequest{
    Namespace: "my-namespace",
    UpdateInfo: &namespace.UpdateNamespaceInfo{
        Description: "Updated description",
        OwnerEmail:  "newteam@example.com",
    },
    Config: &namespace.NamespaceConfig{
        WorkflowExecutionRetentionTtl: durationpb.New(7 * 24 * time.Hour),
    },
})
```

## List Namespaces

```go
var pageToken []byte
for {
    resp, err := nc.List(context.Background(), &workflowservice.ListNamespacesRequest{
        PageSize:      100,
        NextPageToken: pageToken,
    })
    if err != nil {
        log.Fatal(err)
    }
    for _, ns := range resp.Namespaces {
        fmt.Println(ns.NamespaceInfo.Name)
    }
    if len(resp.NextPageToken) == 0 {
        break
    }
    pageToken = resp.NextPageToken
}
```

## Delete a Namespace

```go
// Requires the namespace to be in a deletable state
err = nc.Delete(context.Background(), &operatorservice.DeleteNamespaceRequest{
    Namespace: "my-namespace",
})
```

Deletion asynchronously deletes all workflow executions and history. The namespace name becomes available for reuse after deletion completes.

## Namespace Considerations

| Concern | Self-hosted | Temporal Cloud |
|---------|-------------|----------------|
| Creation | `nc.Register()` or CLI | Console / `tcld` CLI |
| Retention period | Required (min 1 day) | Required (min 1 day) |
| Isolation | Process-level | Account-level |
| Cross-namespace calls | Not directly supported | Not directly supported |

## CLI Operations

```bash
# List namespaces
temporal operator namespace list

# Create namespace
temporal operator namespace create --retention 3d my-namespace

# Describe namespace
temporal operator namespace describe my-namespace

# Update retention
temporal operator namespace update --retention 7d my-namespace
```
