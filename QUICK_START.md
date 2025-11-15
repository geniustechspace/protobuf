# Quick Start Guide

Get started with the GeniusTechSpace protobuf schemas in 5 minutes!

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
├── go/          # Go packages
├── python/      # Python modules
├── java/        # Java classes
├── typescript/  # TypeScript/JavaScript
├── csharp/      # C# classes
└── docs/        # Documentation
```

### Generate Specific Domain

```bash
# Generate only users domain
buf generate --path proto/users/v1/

# Generate only auth domain
buf generate --path proto/auth/v1/
```

## 4. Use Generated Code

### Go Example

```go
package main

import (
    "context"
    "log"
    
    "google.golang.org/grpc"
    usersv1 "github.com/geniustechspace/protobuf/gen/go/users/v1"
)

func main() {
    conn, _ := grpc.Dial("localhost:9090", grpc.WithInsecure())
    defer conn.Close()
    
    client := usersv1.NewUserServiceClient(conn)
    
    resp, err := client.CreateUser(context.Background(), &usersv1.CreateUserRequest{
        TenantId:  "tenant_123",
        Email:     "user@example.com",
        Username:  "johndoe",
        FirstName: "John",
        LastName:  "Doe",
    })
    
    if err != nil {
        log.Fatal(err)
    }
    
    log.Printf("Created user: %s", resp.User.Metadata.Id)
}
```

### Python Example

```python
import grpc
from gen.python.users.v1 import users_pb2, users_pb2_grpc

channel = grpc.insecure_channel('localhost:9090')
client = users_pb2_grpc.UserServiceStub(channel)

response = client.CreateUser(users_pb2.CreateUserRequest(
    tenant_id='tenant_123',
    email='user@example.com',
    username='johndoe',
    first_name='John',
    last_name='Doe'
))

print(f"Created user: {response.user.metadata.id}")
```

### TypeScript Example

```typescript
import { createPromiseClient } from "@connectrpc/connect";
import { createGrpcTransport } from "@connectrpc/connect-node";
import { UserService } from "./gen/typescript/users/v1/users_connect";

const transport = createGrpcTransport({
  baseUrl: "http://localhost:9090",
});

const client = createPromiseClient(UserService, transport);

const response = await client.createUser({
  tenantId: "tenant_123",
  email: "user@example.com",
  username: "johndoe",
  firstName: "John",
  lastName: "Doe",
});

console.log(`Created user: ${response.user?.metadata?.id}`);
```

## 5. Explore Domains

### Core Domain
Common types, tenant context, events
```bash
cat proto/core/README.md
```

### Auth Domain
Authentication, sessions, tokens
```bash
cat proto/auth/README.md
```

### Users Domain
User management, profiles
```bash
ls proto/users/v1/
```

### Tenants Domain
Multi-tenant management
```bash
cat proto/tenants/README.md
```

### Billing Domain
Subscriptions, invoices, payments
```bash
ls proto/billing/v1/
```

### Access Policy Domain
Roles, permissions, authorization
```bash
ls proto/access_policy/v1/
```

### Notifications Domain
Multi-channel notifications
```bash
ls proto/notifications/v1/
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

The repository uses the **buf-action** GitHub Action for streamlined CI/CD:

```yaml
# .github/workflows/buf.yml
- name: Buf Lint, Format, and Breaking
  uses: bufbuild/buf-action@v1
  with:
    token: ${{ secrets.GITHUB_TOKEN }}
    format: true
    lint: true
    breaking: true
    pr_comment: true  # Automatic PR comments
```

Benefits:
- ✅ **Consolidated Action**: Single action replaces multiple setup steps
- ✅ **Built-in Best Practices**: Automatic configuration
- ✅ **PR Comments**: Status comments on pull requests
- ✅ **Git Integration**: Enhanced integration with Git data
- ✅ **BSR Publishing**: Easy Buf Schema Registry publishing

Workflow runs on:
- Every push
- Every pull request

## 9. Documentation

### Main Documentation
- [README.md](README.md) - Overview and features
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Design patterns
- [CLIENT_GENERATION.md](docs/CLIENT_GENERATION.md) - Generate clients
- [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Deploy services
- [VALIDATION.md](docs/VALIDATION.md) - Protovalidate guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guide

### Domain Documentation
- [Core](proto/core/README.md)
- [Auth](proto/auth/README.md)
- [Tenants](proto/tenants/README.md)

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
│   ├── core/             # Common types
│   ├── auth/             # Authentication
│   ├── users/            # User management
│   ├── access_policy/    # Authorization
│   ├── tenants/          # Multi-tenancy
│   ├── billing/          # Payments
│   └── notifications/    # Notifications
├── gen/                  # Generated code (gitignored)
├── docs/                 # Documentation
├── buf.yaml              # Buf configuration
├── buf.gen.yaml          # Code generation config
└── .github/workflows/    # CI/CD pipelines
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
