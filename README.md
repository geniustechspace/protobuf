# GeniusTechSpace Protobuf Schema Repository

Production-ready, domain-driven, tenant-aware Protocol Buffer definitions for microservices architecture.

## Overview

This repository contains Protocol Buffer (protobuf) schemas organized by domain with support for versioning, multi-tenancy, and event-driven architectures. It uses [Buf](https://buf.build) for linting, breaking change detection, code generation, and schema registry integration.

## Domain Structure

The repository is organized into the following top-level domains:

```
proto/
├── core/              # Common types, tenant context, base events
├── auth/              # Authentication and session management
├── users/             # User management and profiles
├── access-policy/     # Role-based access control (RBAC)
├── tenants/           # Multi-tenant organization management
├── billing/           # Subscription, invoicing, and payments
└── notifications/     # Multi-channel notification system
```

Each domain contains versioned subdirectories (v1, v2, etc.) to support backward-compatible schema evolution.

## Features

✅ **Domain-Driven Design**: Clear separation of concerns with dedicated domains  
✅ **Multi-Tenancy**: Built-in tenant context for secure data isolation  
✅ **Versioning**: Support for v1, v2, etc. with backward compatibility  
✅ **Event-Driven**: Domain events for each aggregate  
✅ **gRPC Services**: Well-defined service interfaces  
✅ **Buf Integration**: Linting, breaking change detection, and code generation  
✅ **Protovalidate**: Runtime validation with declarative rules  
✅ **CI/CD Pipeline**: Automated validation and client generation with buf-action  
✅ **Multi-Language**: Generate clients for Go, Python, Java, TypeScript, C#  
✅ **Documentation**: Auto-generated API documentation

## Quick Start

### Prerequisites

- [Buf CLI](https://buf.build/docs/installation) >= 1.47.0
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/geniustechspace/protobuf.git
cd protobuf

# Install buf (if not already installed)
# macOS
brew install bufbuild/buf/buf

# Linux
curl -sSL https://github.com/bufbuild/buf/releases/download/v1.47.2/buf-Linux-x86_64 -o /usr/local/bin/buf
chmod +x /usr/local/bin/buf

# Windows (via Chocolatey)
choco install buf
```

### Linting

```bash
# Lint all proto files
buf lint

# Check formatting
buf format --diff

# Fix formatting
buf format -w
```

### Breaking Change Detection

```bash
# Check against main branch
buf breaking --against '.git#branch=main'
```

### Code Generation

```bash
# Generate code for all languages
buf generate

# Generate for specific path
buf generate --path proto/users/v1/
```

Generated code will be placed in the `gen/` directory:
- `gen/go/` - Go code
- `gen/python/` - Python code
- `gen/java/` - Java code
- `gen/typescript/` - TypeScript code
- `gen/csharp/` - C# code
- `gen/docs/` - Documentation

## Domain Documentation

### Core Domain

The core domain provides foundational types used across all domains:

- **TenantContext**: Multi-tenant isolation context
- **Metadata**: Common entity metadata (ID, timestamps, audit info)
- **Pagination**: Request/response types for paginated lists
- **Address, ContactInfo, Money**: Common value objects
- **ErrorResponse**: Standardized error responses
- **BaseEvent**: Foundation for all domain events

### Auth Domain

Authentication and session management:

- **Services**: AuthService
- **Key Operations**: Authenticate, RefreshToken, ValidateToken, Logout, PasswordReset
- **Events**: UserAuthenticated, UserLoggedOut, PasswordResetRequested

### Users Domain

User management and profiles:

- **Services**: UserService
- **Key Operations**: CreateUser, GetUser, UpdateUser, DeleteUser, ListUsers
- **Events**: UserCreated, UserUpdated, UserDeleted, UserStatusChanged

### Access Policy Domain

Role-based access control (RBAC):

- **Services**: AccessPolicyService
- **Key Operations**: CreateRole, AssignRole, CheckPermission
- **Events**: RoleCreated, RoleAssigned, PermissionChecked

### Tenants Domain

Multi-tenant organization management:

- **Services**: TenantService
- **Key Operations**: CreateTenant, UpdateTenant, UpdateTenantStatus, GetTenantUsage
- **Events**: TenantCreated, TenantStatusChanged, TenantTierChanged

### Billing Domain

Subscription and billing management:

- **Services**: BillingService
- **Key Operations**: CreateSubscription, CancelSubscription, PayInvoice
- **Events**: SubscriptionCreated, InvoicePaid, PaymentFailed

### Notifications Domain

Multi-channel notification system:

- **Services**: NotificationService
- **Key Operations**: SendNotification, ListNotifications, MarkNotificationRead
- **Events**: NotificationSent, NotificationDelivered, NotificationRead

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/buf.yml`) automatically:

1. **Lints** proto files on every push and pull request
2. **Detects breaking changes** in pull requests
3. **Generates code** for all supported languages
4. **Lists schemas** and creates an inventory
5. **Pushes to Buf Schema Registry** (when configured)
6. **Generates domain-specific clients** for independent deployment
7. **Generates documentation** and deploys to GitHub Pages

## Using Generated Clients

### Go

```go
import (
    usersv1 "github.com/geniustechspace/protobuf/gen/go/users/v1"
)

// Use the generated types and services
```

### Python

```python
from gen.python.users.v1 import users_pb2, users_pb2_grpc

# Use the generated types and services
```

### Java

```java
import com.geniustechspace.protobuf.users.v1.UsersProto;
import com.geniustechspace.protobuf.users.v1.UserServiceGrpc;

// Use the generated types and services
```

### TypeScript

```typescript
import { User, UserService } from './gen/typescript/users/v1';

// Use the generated types and services
```

## Schema Evolution

We follow strict backward compatibility rules:

1. **Never** remove or rename fields
2. **Never** change field types
3. **Never** change field numbers
4. **Always** add new fields with new field numbers
5. **Use** reserved fields for deprecated fields
6. **Version** your packages (v1, v2) for major breaking changes

Example of evolving from v1 to v2:

```protobuf
// v1/users.proto
message User {
  string id = 1;
  string name = 2;
}

// v2/users.proto (backward compatible)
message User {
  string id = 1;
  string name = 2;
  string email = 3;  // New field added
  repeated string tags = 4;  // New field added
}
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Run `buf lint` and `buf format -w`
4. Run `buf breaking --against '.git#branch=main'` to check for breaking changes
5. Create a pull request

## Buf Schema Registry

To push schemas to Buf Schema Registry:

1. Create an account at https://buf.build
2. Create a repository: `buf.build/geniustechspace/protobuf`
3. Generate a token
4. Add `BUF_TOKEN` to GitHub secrets
5. Uncomment the `buf push` step in `.github/workflows/buf.yml`

## Validation

This repository uses [protovalidate](https://github.com/bufbuild/protovalidate) for runtime validation:

```protobuf
import "buf/validate/validate.proto";

message CreateUserRequest {
  string tenant_id = 1 [(buf.validate.field).string.min_len = 1];
  string email = 2 [(buf.validate.field).string.email = true];
  string username = 3 [(buf.validate.field).string = {
    min_len: 3
    max_len: 50
    pattern: "^[a-zA-Z0-9_-]+$"
  }];
  string password = 4 [(buf.validate.field).string.min_len = 8];
}
```

See [VALIDATION.md](docs/VALIDATION.md) for comprehensive validation guide.

## License

See [LICENSE](LICENSE) file for details.

## Support

For issues and questions, please open an issue in this repository.