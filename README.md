# Genius Tech Space Protobuf Schema Repository

**Production-ready, domain-driven, enterprise-grade Protocol Buffer definitions for multi-tenant microservices**

[![Buf](https://img.shields.io/badge/Buf-Schema%20Registry-blue)](https://buf.build)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CI](https://github.com/geniustechspace/protobuf/workflows/Buf%20Schema%20Validation/badge.svg)](https://github.com/geniustechspace/protobuf/actions)

## 🚀 Overview

This repository contains Protocol Buffer (protobuf) schemas organized by domain with comprehensive documentation, strict versioning, and enterprise compliance standards. Built with [Buf](https://buf.build) for schema validation, linting, breaking change detection, and multi-language code generation.

### Key Features

- 📦 **Modular Architecture**: Separate files for enums, messages, requests, and services
- 🏢 **Enterprise Documentation**: Comprehensive inline docs with compliance notes
- 🔒 **Multi-Tenancy**: Built-in tenant isolation and context enforcement
- 📊 **RBAC & ABAC**: Role-based and attribute-based access control
- 🔄 **Versioning**: Semantic versioning with backward compatibility
- 🎯 **Event-Driven**: Domain events for all aggregates
- ✅ **Validation**: Declarative runtime validation with protovalidate
- 🤖 **CI/CD**: Automated linting, breaking change detection, and publishing
- 🌐 **Multi-Language**: Generated clients for Go, Python, Java, TypeScript, C#
- 📚 **Compliance**: SOC 2, GDPR, ISO 27001, PCI DSS annotations

## 📁 Repository Structure

### Flattened Domain Organization

```
proto/
├── core/                    # Foundation types
│   ├── api/                # API patterns (pagination, error, circuit breaker, retry)
│   ├── client/             # Client information
│   ├── common/             # Common reusable types
│   ├── device/             # Device information
│   ├── geo/                # Geographic data
│   ├── metadata/           # Entity metadata
│   ├── network/            # Network information
│   ├── session/            # Session data
│   └── token/              # Token types
│
├── idp/                     # Identity Provider (Domain-First Architecture)
│   ├── api/v1/             # Top-level IDP services
│   │   └── services.proto  # IdentityService, AuthenticationService, AuthorizationService
│   ├── identity/           # Identity Bounded Context
│   │   ├── user/
│   │   │   ├── v1/         # User entity + UserStatus enum
│   │   │   ├── events/v1/  # UserCreated, UserUpdated, etc.
│   │   │   └── api/v1/     # UserService with 9 RPCs
│   │   │       ├── api.proto      # Convenience import
│   │   │       ├── request.proto  # Request messages
│   │   │       ├── response.proto # Response messages
│   │   │       └── service.proto  # gRPC service
│   │   ├── group/          # Group subdomain (3 layers)
│   │   ├── organization/   # Organization subdomain (3 layers)
│   │   └── profile/        # Profile subdomain (3 layers)
│   ├── authn/              # Authentication Bounded Context
│   │   ├── credential/     # Credential subdomain (3 layers)
│   │   ├── session/        # Session subdomain (3 layers)
│   │   └── mfa/            # MFA subdomain (3 layers)
│   ├── authz/              # Authorization Bounded Context
│   │   ├── permission/     # Permission subdomain (3 layers)
│   │   ├── role/           # Role subdomain (3 layers)
│   │   └── policy/         # Policy subdomain (3 layers)
│   ├── audit/              # Audit logging
│   ├── connectors/         # External identity connectors
│   ├── protocols/          # Protocol implementations
│   ├── provisioning/       # User provisioning
│   └── webhook/            # Webhook management
│
├── contact/                 # Contact Information
│   ├── address/v1/         # Address management
│   └── phone/v1/           # Phone number management
│
├── hcm/                     # Human Capital Management
│   └── employee/v1/        # Employee data
│
├── preference/              # User Preferences
│   └── user/v1/            # User preference management
│
└── storage/                 # Storage (reserved for future)
```

### Modular File Structure Benefits

- ⚡ **Faster Compilation**: Import only what you need
- 🎯 **Clear Dependencies**: Explicit import relationships
- 📝 **Easier Reviews**: Smaller, focused file changes
- 🔧 **Better Maintenance**: Logical separation of concerns

## Features

✅ **Domain-Driven Design**: Clear separation of concerns with 6 dedicated domains  
✅ **IDP Domain-First Architecture**: 10 subdomains with three-layer structure  
✅ **Multi-Tenancy**: Built-in tenant context for secure data isolation  
✅ **Versioning**: Support for v1, v2, etc. with backward compatibility  
✅ **Event-Driven**: Domain events for key aggregates  
✅ **gRPC Services**: 6 well-defined service interfaces  
✅ **Buf Integration**: Linting, breaking change detection, and code generation  
✅ **Protovalidate**: Runtime validation with declarative rules  
✅ **Multi-Language**: Generate clients for 8 languages (Go, Rust, Java, Kotlin, Swift, Dart, Python, TypeScript)  
✅ **Comprehensive Documentation**: 49 README files across all domains

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

# Generate entire IDP domain
buf generate --path proto/idp/

# Generate specific IDP subdomain
buf generate --path proto/idp/identity/user/

# Generate specific domains
buf generate --path proto/users/v1/
```

Generated code will be placed in the `gen/` directory:

- `gen/go/` - Go code with gRPC
- `gen/rust/` - Rust code with Prost and Tonic
- `gen/java/` - Java code with gRPC
- `gen/kotlin/` - Kotlin code
- `gen/swift/` - Swift code with gRPC
- `gen/dart/` - Dart code
- `gen/python/` - Python code with gRPC
- `gen/typescript/` - TypeScript code (Connect, JS, gRPC-Web)

## Domain Documentation

### Core Domain

The core domain provides foundational types used across all domains:

- **API Patterns**: Pagination, error handling, circuit breaker, retry, request/response wrappers
- **Client Info**: Browser, device, network context
- **Common Types**: Reusable value objects
- **Device Info**: Device identification and metadata
- **Geo**: Geographic and location data
- **Metadata**: Common entity metadata (ID, timestamps, audit info)
- **Network**: Network connection information
- **Session**: Session tracking data
- **Token**: Token types and metadata

### IDP Domain

Enterprise Identity Provider with domain-first, three-layer architecture:

**Architecture Pattern:** `geniustechspace.idp.{domain}.{subdomain}.{layer}.v1`

**Three Layers:**

- **Domain (v1/)**: Pure entities and enums
- **Events (events/v1/)**: Domain events for state changes
- **API (api/v1/)**: gRPC services split into modular files (request.proto, response.proto, service.proto)

**Top-Level Services:**

- **IdentityService**: Core identity operations
- **AuthenticationService**: Authentication workflows
- **AuthorizationService**: Authorization checks

**Bounded Contexts:**

- **Identity**: user, group, organization, profile (4 subdomains)
- **Authentication (authn)**: credential, session, mfa (3 subdomains)
- **Authorization (authz)**: permission, role, policy (3 subdomains)

**Example: User Subdomain**

- **Entity**: User with 18+ fields, UserStatus enum (8 states)
- **Events**: UserCreated, UserUpdated, UserDeleted, UserStatusChanged, UserEmailVerified, UserPhoneVerified
- **API**: UserService with 9 RPCs (Create, Get, Update, Delete, List, Search, UpdateStatus, VerifyEmail, VerifyPhone)

**Status:** UserService fully implemented with modular API files. Other subdomains scaffolded.

See [proto/idp/README.md](proto/idp/README.md) and [proto/idp/ARCHITECTURE.md](proto/idp/ARCHITECTURE.md) for details.

### Contact Domain

Contact information management:

- **Address**: Structured address data with validation
- **Phone**: Phone number management with E.164 format

### HCM Domain

Human Capital Management:

- **Employee**: Employee data and management

### Preference Domain

User preference management:

- **User Preferences**: User-specific settings and preferences

### Storage Domain

Reserved for future file and object storage features.

## CI/CD Pipeline

The GitHub Actions workflow can be configured to automatically:

1. **Lint** proto files on every push and pull request
2. **Detect breaking changes** in pull requests
3. **Generate code** for all supported languages
4. **Push to Buf Schema Registry** (when configured)
5. **Deploy documentation** to GitHub Pages

To enable, create `.github/workflows/buf.yml` with appropriate workflow configuration.

## Using Generated Clients

### Go

```go
import (
    // IDP - Domain-first imports
    userv1 "github.com/geniustechspace/protobuf/gen/go/idp/identity/user/v1"
    userapiv1 "github.com/geniustechspace/protobuf/gen/go/idp/identity/user/api/v1"
    usereventsv1 "github.com/geniustechspace/protobuf/gen/go/idp/identity/user/events/v1"
    
    // Core types
    coreclientv1 "github.com/geniustechspace/protobuf/gen/go/core/client/v1"
)

// Use IDP generated types
client := userapiv1.NewUserServiceClient(conn)
user := &userv1.User{UserId: "usr_123"}
event := &usereventsv1.UserCreated{...}
```

### Python

```python
import grpc
from gen.python.idp.identity.user.v1 import user_pb2
from gen.python.idp.identity.user.api.v1 import service_pb2_grpc

channel = grpc.insecure_channel('localhost:9090')
client = service_pb2_grpc.UserServiceStub(channel)

# Use generated types
user = user_pb2.User(user_id='usr_123')
```

### TypeScript

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
  tenantPath: "tenants/tenant_123",
  email: "user@example.com",
  username: "johndoe",
});

console.log(`Created user: ${response.user?.userId}`);
```

## Schema Evolution

We follow strict backward compatibility rules:

1. **Never** remove or rename fields
2. **Never** change field types
3. **Never** change field numbers
4. **Always** add new fields with new field numbers
5. **Use** reserved fields for removed fields
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
