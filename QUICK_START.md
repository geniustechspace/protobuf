# Quick Start Guide

Get started with the Genius Tech Space protobuf schemas in 5 minutes!

## 1. Installation

### Install Buf CLI

**macOS**:

```bash
brew install bufbuild/buf/buf
```

**Linux**:

```bash
curl -sSL https://github.com/bufbuild/buf/releases/download/v1.47.2/buf-Linux-x86_64 -o /usr/local/bin/buf
chmod +x /usr/local/bin/buf
```

**Windows** (Chocolatey):

```bash
choco install buf
```

### Clone Repository

```bash
git clone https://github.com/geniustechspace/protobuf.git
cd protobuf
```

## 2. Validate Schemas

```bash
# Lint all schemas
buf lint

# Check formatting
buf format --diff

# Apply formatting
buf format -w
```

## 3. Generate Code

### Generate All Languages

```bash
buf generate
```

This generates code in `gen/` directory:

```
gen/
├── go/          # Go packages with gRPC
├── rust/        # Rust with Prost and Tonic
├── java/        # Java classes with gRPC
├── kotlin/      # Kotlin classes
├── swift/       # Swift with gRPC
├── dart/        # Dart classes
├── python/      # Python modules with gRPC
└── typescript/  # TypeScript (Connect, JS, gRPC-Web)
```

### Generate Specific Domain

```bash
# Generate entire IDP domain (all subdomains)
buf generate --path proto/idp/

# Generate specific IDP subdomain
buf generate --path proto/idp/identity/user/

# Generate other domains
buf generate --path proto/<domain/subdomain>/v1/
```

## 4. Use Generated Code

### Go Example - IDP Domain-First

```go
package main

import (
    "context"
    "log"

    "google.golang.org/grpc"

    // IDP imports - modular structure
    userv1 "github.com/geniustechspace/protobuf/gen/go/idp/identity/user/v1"
    userapiv1 "github.com/geniustechspace/protobuf/gen/go/idp/identity/user/api/v1"
)

func main() {
    conn, _ := grpc.Dial("localhost:9090", grpc.WithInsecure())
    defer conn.Close()

    // Use API layer for service
    client := userapiv1.NewUserServiceClient(conn)

    // Use domain layer types in request
    resp, err := client.CreateUser(context.Background(), &userapiv1.CreateUserRequest{
        TenantId: "tenant_123",
        Email:    "user@example.com",
        Username: "johndoe",
        Profile: &userv1.UserProfile{
            FirstName: "John",
            LastName:  "Doe",
        },
    })

    if err != nil {
        log.Fatal(err)
    }

    // Response contains domain entity
    log.Printf("Created user: %s", resp.User.UserId)
}
```

### Python Example

```python
import grpc
from gen.python.idp.identity.user.v1 import user_pb2
from gen.python.idp.identity.user.api.v1 import service_pb2_grpc

channel = grpc.insecure_channel('localhost:9090')
client = service_pb2_grpc.UserServiceStub(channel)

# Use generated types
user = user_pb2.User(user_id='usr_123')
```

### TypeScript Example - IDP Domain-First

```typescript
import { createPromiseClient } from "@connectrpc/connect";
import { createGrpcTransport } from "@connectrpc/connect-node";

// IDP modular imports
import { UserService } from "./gen/typescript/idp/identity/user/api/v1/service_connect";
import type { User } from "./gen/typescript/idp/identity/user/v1/user_pb";

const transport = createGrpcTransport({
  baseUrl: "http://localhost:9090",
});

const client = createPromiseClient(UserService, transport);

const response = await client.createUser({
  tenantId: "tenant_123",
  email: "user@example.com",
  username: "johndoe",
  profile: {
    firstName: "John",
    lastName: "Doe",
  },
});

console.log(`Created user: ${response.user?.userId}`);
```

## 5. Explore Domains

### IDP Domain (Domain-First Architecture)

Enterprise Identity Provider with three-layer structure

```bash
# Overview
cat proto/idp/README.md
cat proto/idp/ARCHITECTURE.md

# Explore User subdomain (three layers)
ls proto/idp/identity/user/v1/          # Domain layer - User entity
ls proto/idp/identity/user/events/v1/   # Events layer - UserCreated, etc.
ls proto/idp/identity/user/api/v1/      # API layer - UserService (modular)

# View modular API files
cat proto/idp/identity/user/api/v1/service.proto   # gRPC service
cat proto/idp/identity/user/api/v1/request.proto   # Request messages
cat proto/idp/identity/user/api/v1/response.proto  # Response messages

# List all subdomains
ls proto/idp/identity/  # user, group, organization, profile
ls proto/idp/authn/     # credential, session, mfa
ls proto/idp/authz/     # permission, role, policy
```

### Core Domain

Common types, API patterns, metadata

```bash
cat proto/core/README.md
ls proto/core/api/      # Pagination, errors, circuit breaker, retry
ls proto/core/metadata/ # Entity metadata
```

### Other Domains

Contact, HCM, Preference, Storage

```bash
ls proto/contact/address/v1/  # Address management
ls proto/contact/phone/v1/    # Phone management
ls proto/hcm/employee/v1/     # Employee data
ls proto/preference/user/v1/  # User preferences
```

## 6. Make Changes

### Create Feature Branch

```bash
git checkout -b feature/my-changes
```

### Edit Proto Files

```bash
# Edit a domain
vim proto/users/v1/users.proto

# Lint changes
buf lint

# Format changes
buf format -w
```

### Check Breaking Changes

```bash
buf breaking --against '.git#branch=main'
```

### Test Generation

```bash
buf generate
```

### Commit Changes

```bash
git add .
git commit -m "feat: add new field to User"
git push origin feature/my-changes
```

## 7. Common Tasks

### List All Services

```bash
find proto -name "*.proto" -exec grep "^service" {} +
```

### List All Messages

```bash
find proto -name "*.proto" -exec grep "^message" {} +
```

### Count Proto Files

```bash
find proto -name "*.proto" | wc -l
```

### View Domain Structure

```bash
tree proto/
```

## 8. CI/CD

The repository can use the **buf-action** GitHub Action for streamlined CI/CD:

```yaml
# .github/workflows/buf.yml
- name: Buf Lint, Format, and Breaking
  uses: bufbuild/buf-action@v1
  with:
    token: ${{ secrets.GITHUB_TOKEN }}
    format: true
    lint: true
    breaking: true
    pr_comment: true # Automatic PR comments
```

Benefits:

- ✅ **Consolidated Action**: Single action replaces multiple setup steps
- ✅ **Built-in Best Practices**: Automatic configuration
- ✅ **PR Comments**: Status comments on pull requests
- ✅ **Git Integration**: Enhanced integration with Git data
- ✅ **BSR Publishing**: Easy Buf Schema Registry publishing

Can run on:

- Every push
- Every pull request

## 9. Documentation

### Main Documentation

- [README.md](README.md) - Overview and features
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guide
- [QUICK_START.md](QUICK_START.md) - This guide
- [SUMMARY.md](SUMMARY.md) - Implementation summary
- [VALIDATION.md](docs/VALIDATION.md) - Protovalidate guide
- [PROTO_DOCUMENTATION_STANDARD.md](docs/PROTO_DOCUMENTATION_STANDARD.md) - Documentation standards

### Domain Documentation

- [IDP Architecture](proto/idp/ARCHITECTURE.md)
- [IDP Overview](proto/idp/README.md)
- [Core](proto/core/README.md)
- Plus 49 README files across all domains

## 10. Support

### Issues

Open an issue: https://github.com/geniustechspace/protobuf/issues

### Questions

Start a discussion: https://github.com/geniustechspace/protobuf/discussions

### Community

Join Discord: [link]

## Quick Reference

### Buf Commands

```bash
buf lint                    # Lint schemas
buf format -w              # Format schemas
buf breaking               # Check breaking changes
buf generate               # Generate code
buf dep update            # Update dependencies
```

### Directory Structure

```
protobuf/
├── proto/                 # Protocol buffer definitions
│   ├── core/             # Foundation types
│   ├── idp/              # Identity Provider (10 subdomains)
│   ├── contact/          # Contact information
│   ├── hcm/              # Human Capital Management
│   ├── preference/       # User preferences
│   └── storage/          # Storage (reserved)
├── gen/                  # Generated code (gitignored)
├── docs/                 # Documentation
├── buf.yaml              # Buf configuration
├── buf.gen.yaml          # Code generation config
└── .github/workflows/    # CI/CD pipelines (when configured)
```

### Key Concepts

- **Multi-Tenancy**: All requests include `tenant_id`
- **Versioning**: v1, v2, etc. for backward compatibility
- **Events**: Domain events for state changes
- **Metadata**: All entities include common metadata
- **Pagination**: Standard pagination for lists

## Next Steps

1. ✅ Install Buf and clone repo
2. ✅ Generate code for your language
3. ✅ Read domain documentation
4. ✅ Build your first service
5. ✅ Contribute improvements

Happy coding! 🚀
