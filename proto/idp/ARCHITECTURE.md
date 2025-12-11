# IDP Architecture - Domain-First DDD/EDA Implementation

## Overview

Enterprise-grade Identity Provider following **Domain-Driven Design (DDD)** and **Event-Driven Architecture (EDA)** with a domain-first, three-layer architecture pattern. Each subdomain is self-contained and co-locates domain models, events, and APIs for independent evolution.

## Architecture Pattern

```
proto/idp/
├── identity/                    # Identity Bounded Context
│   ├── user/
│   │   ├── v1/                 # Domain Layer - User entity + enums
│   │   ├── events/v1/          # Events Layer - UserCreated, UserUpdated, etc.
│   │   └── api/v1/             # API Layer - UserService (9 RPCs)
│   │       ├── api.proto       # Convenience import
│   │       ├── request.proto   # Request messages
│   │       ├── response.proto  # Response messages
│   │       └── service.proto   # gRPC service definition
│   ├── group/                  # Same three-layer structure
│   ├── organization/           # Same three-layer structure
│   └── profile/                # Same three-layer structure
│
├── authn/                       # Authentication Bounded Context
│   ├── credential/             # Same three-layer structure
│   ├── session/                # Same three-layer structure
│   └── mfa/                    # Same three-layer structure
│
├── authz/                       # Authorization Bounded Context
│   ├── permission/             # Same three-layer structure
│   ├── role/                   # Same three-layer structure
│   └── policy/                 # Same three-layer structure
│
└── [audit, connectors, protocols, provisioning, webhook]/
    # Supporting modules (to be implemented)
```

## Package Naming Convention

```protobuf
// Domain entities and enums
package geniustechspace.idp.identity.user.v1;

// Domain events
package geniustechspace.idp.identity.user.events.v1;

// gRPC API services
package geniustechspace.idp.identity.user.api.v1;
```

**Pattern:** `geniustechspace.idp.{domain}.{subdomain}.{layer}.v1`

## Three-Layer Architecture

### Layer 1: Domain Model (`v1/`)

Pure domain entities, enums, and business rules

- Entity definitions with flattened audit fields (created_at, updated_at, deleted_at, version)
- Domain enums (UserStatus, CredentialType, etc.)
- Business invariants and protovalidate constraints
- Multi-tenant isolation (tenant_id in all entities)
- NO RPC services or request/response messages

### Layer 2: Events (`events/v1/`)

Domain events for state changes

- Lifecycle events (Created, Updated, Deleted)
- State transition events (StatusChanged, Verified)
- Published to event bus for downstream consumers
- Enables event sourcing and audit trail
- Compliance tracking (SOC 2 CC6.3, GDPR Article 30)

### Layer 3: API (`api/v1/`)

gRPC services split into modular files

- `api.proto` - Convenience import for all components
- `request.proto` - All request messages with validation
- `response.proto` - All response messages
- `service.proto` - gRPC service definition with RPCs
- Authentication/authorization annotations
- Rate limiting and compliance documentation

## Bounded Contexts

### Identity Domain (10 subdomains planned)

**Current:** user, group, organization, profile  
**Implemented APIs:** UserService (9 RPCs)  
**Key Features:**

- User lifecycle management (CRUD + status + verification)
- Group hierarchies with 6 types
- Organization hierarchies with branding
- Profile PII data with encryption requirements

**Entities:**

- **User**: 18+ fields, UserStatus enum (8 states)
- **Group**: Hierarchical with GroupType enum
- **Organization**: Multi-level with domains and branding
- **Profile**: PII value object

**Events:**

- UserCreated, UserUpdated, UserDeleted, UserStatusChanged
- UserEmailVerified, UserPhoneVerified
- (Group, Organization events to be implemented)

### Authentication Domain (authn) (3 subdomains)

**Subdomains:** credential, session, mfa  
**Status:** Domain models defined, APIs in progress  
**Key Features:**

- Multi-method authentication (6 credential types)
- Session management with risk scoring
- MFA enrollment (7 methods)

**Entities:**

- **Credential**: 6 types (PASSWORD, WEBAUTHN, TOTP, etc.)
- **Session**: Tokens, context, device fingerprinting
- **Mfa**: Enrollment and verification

### Authorization Domain (authz) (3 subdomains)

**Subdomains:** permission, role, policy  
**Status:** Domain models defined, APIs in progress  
**Key Features:**

- RBAC with role inheritance
- ABAC/PBAC with conditions
- Resource:action permission format

**Entities:**

- **Permission**: Resource-action pairs
- **Role**: Permission collections with inheritance
- **Policy**: ABAC rules with conditions

## Entity Metadata Pattern

All domain entities include **flattened audit fields** (not nested):

```protobuf
message User {
  string user_id = 1;
  string tenant_id = 2;
  // ... domain fields ...

  google.protobuf.Timestamp created_at = N;
  google.protobuf.Timestamp updated_at = N+1;
  google.protobuf.Timestamp deleted_at = N+2;  // Soft delete
  int64 version = N+3;  // Optimistic locking
}
```

**Actor tracking** (created_by, updated_by) maintained in separate audit entity.

## API File Structure

Each API layer is split into 4 modular files:

1. **api.proto** - Convenience import aggregating all components
2. **request.proto** - Request messages with buf/validate annotations
3. **response.proto** - Response messages (often entity wrappers)
4. **service.proto** - gRPC service with annotated RPCs

**Benefits:** Independent imports, better code organization, faster compilation

## Compliance & Security

**Standards:**

- GDPR (Articles 5, 15, 16, 17, 30)
- SOC 2 (CC6.1, CC6.3)
- ISO 27001 (A.9.2)
- NIST 800-63B

**Protocols:**

- OAuth 2.0, OIDC, SAML 2.0
- WebAuthn Level 2
- SCIM 2.0 (provisioning)

**Annotations:**

- PII field marking
- Encryption requirements
- Authentication/authorization per RPC
- Rate limiting documentation
- Compliance mappings

## Code Generation

```bash
# Generate all languages
buf generate --path proto/idp/

# Generate specific domain
buf generate --path proto/idp/identity/user/

# Validate before commit
buf format -w && buf lint
```

**Supported languages:** Go, Python, Java, TypeScript, C#

## Key Design Benefits

1. **Domain-First**: Each subdomain is self-contained with all three layers co-located
2. **Independent Evolution**: Domains evolve without affecting others
3. **Microservice-Ready**: Each subdomain can be extracted as independent service
4. **Event-Driven**: All state changes publish events for downstream consumers
5. **Type-Safe**: Generated clients prevent runtime errors
6. **Compliance-First**: Security and compliance annotations built-in
7. **Multi-Tenant**: Tenant isolation enforced at entity level
8. **Modular APIs**: Split files enable better code organization

## Status Summary

**Completed:**

- ✅ Identity/User: Full implementation (domain, events, API with 9 RPCs)
- ✅ Three-layer structure for all 10 subdomains
- ✅ Modular API file splitting (40 API files)
- ✅ Domain models for all entities
- ✅ Flattened audit field pattern

**In Progress:**

- 🔄 Event implementations for remaining subdomains
- 🔄 API implementations for authn/authz domains

**Planned:**

- ⏳ Supporting modules (audit, connectors, protocols, provisioning, webhook)
- ⏳ Legacy api/v1 compatibility layer

See `proto/idp/README.md` for detailed documentation.
