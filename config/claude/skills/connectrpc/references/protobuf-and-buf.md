# Protobuf & Buf Codegen

## Proto Schema Conventions

```protobuf
// proto/api/v1/user.proto
syntax = "proto3";

package api.v1;

option go_package = "github.com/myorg/myproject/gen/go/api/v1;apiv1";

import "google/protobuf/timestamp.proto";

// Services use verb-noun naming
service UserService {
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
  rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
  rpc DeleteUser(DeleteUserRequest) returns (DeleteUserResponse);

  // Server streaming
  rpc WatchUser(WatchUserRequest) returns (stream UserEvent);
}

message GetUserRequest {
  string id = 1;
}

message GetUserResponse {
  User user = 1;
}

message User {
  string id = 1;
  string name = 2;
  string email = 3;
  google.protobuf.Timestamp created_at = 4;
}
```

**Conventions:**
- One service per file; name file after the domain (`user.proto`, not `service.proto`)
- Request/response message names mirror the RPC: `GetUserRequest` / `GetUserResponse`
- Use `google.protobuf.Timestamp` for times, not `int64`
- Set `go_package` with full import path + short alias

## buf.yaml

```yaml
# proto/buf.yaml
version: v2
modules:
  - path: .
lint:
  use:
    - STANDARD
  except:
    - PACKAGE_VERSION_SUFFIX  # remove if you enforce v1/v2 suffixes
breaking:
  use:
    - FILE
deps:
  - buf.build/googleapis/googleapis  # for google.protobuf.*
```

## buf.gen.yaml

```yaml
# proto/buf.gen.yaml
version: v2
managed:
  enabled: true
  override:
    - file_option: go_package_prefix
      value: github.com/myorg/myproject/gen/go
plugins:
  # Go: protobuf structs
  - remote: buf.build/protocolbuffers/go
    out: ../gen/go
    opt:
      - paths=source_relative

  # Go: connect-go service stubs + clients
  - remote: buf.build/connectrpc/go
    out: ../gen/go
    opt:
      - paths=source_relative

  # TypeScript: protobuf message types (ES modules)
  - remote: buf.build/bufbuild/es
    out: ../gen/ts
    opt:
      - target=ts

  # TypeScript: connect-es service schemas
  - remote: buf.build/connectrpc/es
    out: ../gen/ts
    opt:
      - target=ts
```

## Code Generation Commands

```bash
# Install buf
go install github.com/bufbuild/buf/cmd/buf@latest

# Generate code (run from proto/ directory)
cd proto
buf generate

# Lint proto files
buf lint

# Check for breaking changes vs main branch
buf breaking --against '.git#branch=main'

# Format proto files
buf format -w
```

## Generated Go File Structure

```
gen/go/api/v1/
  user.pb.go           # Message types (User, GetUserRequest, etc.)
  user_grpc.pb.go      # gRPC stubs (if using protoc-gen-go-grpc)
  userv1connect/
    user.connect.go    # connect-go: handler interface + client constructor
```

`user.connect.go` contains:
```go
// Interface your handler must implement
type UserServiceHandler interface {
    GetUser(context.Context, *connect.Request[apiv1.GetUserRequest]) (*connect.Response[apiv1.GetUserResponse], error)
    // ...
}

// Register on mux
func NewUserServiceHandler(svc UserServiceHandler, opts ...connect.HandlerOption) (string, http.Handler)

// Create a client
func NewUserServiceClient(httpClient connect.HTTPClient, baseURL string, opts ...connect.ClientOption) UserServiceClient
```

## Generated TypeScript File Structure

```
gen/ts/api/v1/
  user_pb.ts           # Message classes + field definitions
  user_connect.ts      # Service schema (used with createClient)
```

`user_connect.ts` exports:
```typescript
export const UserService: {
  readonly typeName: "api.v1.UserService";
  readonly methods: {
    readonly getUser: {
      readonly name: "GetUser";
      readonly I: typeof GetUserRequest;
      readonly O: typeof GetUserResponse;
      readonly kind: MethodKind.Unary;
    };
    // ...
  };
};
```

## Protovalidate Integration

```bash
# Add to deps in buf.yaml
deps:
  - buf.build/bufbuild/protovalidate
```

```protobuf
import "buf/validate/validate.proto";

message CreateUserRequest {
  string email = 1 [(buf.validate.field).string.email = true];
  string name = 2 [(buf.validate.field).string = {
    min_len: 1,
    max_len: 100
  }];
}
```

```go
// Go server: validate in handler
import "github.com/bufbuild/protovalidate-go"

validator, _ := protovalidate.New()

func (s *server) CreateUser(ctx context.Context, req *connect.Request[apiv1.CreateUserRequest]) (*connect.Response[apiv1.CreateUserResponse], error) {
    if err := validator.Validate(req.Msg); err != nil {
        return nil, connect.NewError(connect.CodeInvalidArgument, err)
    }
    // ...
}
```

## Docs

- https://buf.build/docs/introduction/ — Buf toolchain overview
- https://buf.build/docs/generate/overview/ — Code generation with buf generate
- https://buf.build/docs/configuration/v2/buf-yaml/ — buf.yaml v2 reference
- https://buf.build/docs/configuration/v2/buf-gen-yaml/ — buf.gen.yaml v2 reference
- https://buf.build/plugins/connectrpc/go — connectrpc/go plugin on Buf Schema Registry
- https://buf.build/plugins/connectrpc/es — connectrpc/es plugin on Buf Schema Registry
- https://github.com/bufbuild/protovalidate — Protovalidate repo and docs
