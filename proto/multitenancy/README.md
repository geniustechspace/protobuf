# Multitenancy Domain

Enterprise-grade multi-tenancy management enabling complete decoupling of tenant isolation from domain entities.

## Overview

The multitenancy domain provides a dedicated bounded context for managing tenant lifecycle, hierarchy, membership, and isolation modes. This separation follows DDD principles and enables:

- **Domain Entity Independence**: Core domain entities (users, groups, roles, etc.) have no knowledge of multi-tenancy
- **Flexible Isolation Modes**: Easy switching between shared, silo, hybrid, and pool isolation strategies
- **Hierarchical Tenancy**: Support for B2B2B scenarios with unlimited nesting levels
- **Clean API Boundaries**: Tenant context provided at request level, not embedded in entities

## Architecture Pattern

```
proto/multitenancy/
├── v1/                         # Domain Layer
│   ├── tenant.proto            # Tenant aggregate root + settings
│   └── context.proto           # TenantContext + TenantMembership
├── events/v1/                  # Events Layer
│   └── events.proto            # Tenant lifecycle events
└── api/v1/                     # API Layer
    └── service.proto           # TenantService gRPC definitions
```

## Key Concepts

### Tenant Entity

The `Tenant` aggregate root represents an isolated organizational boundary:

- **Hierarchical**: Supports parent-child relationships for reseller/white-label scenarios
- **Immutable Isolation**: Isolation mode set at creation, cannot be changed without migration
- **Configurable Settings**: Per-tenant limits, policies, and branding

### Tenant Context

`TenantContext` is a request-scoped value object that:

- Provides tenant information to API handlers without coupling to domain entities
- Resolved at middleware/gateway level from various sources (token, header, subdomain)
- Supports hierarchical access control with effective tenant IDs

### Isolation Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| `SHARED` | All tenants share tables with row-level security | High tenant count, cost-efficient |
| `SILO` | Each tenant has own database/schema | Strict compliance, large enterprise |
| `HYBRID` | Shared operational, isolated sensitive data | Balanced compliance/performance |
| `POOL` | Tenant groups share schemas | Horizontal scaling |

### Tenant Membership

`TenantMembership` associates subjects (users, groups, service accounts) with tenants:

- Users can belong to multiple tenants
- Membership includes role (owner, admin, member, guest)
- Supports invitation workflow for pending members

## Usage

### Providing Tenant Context in Requests

Instead of including `tenant_path` in domain entity fields, include `TenantContext` in API requests:

```protobuf
message CreateUserRequest {
  // Tenant context for the operation (resolved by middleware)
  multitenancy.v1.TenantContext tenant_context = 1;
  
  // Domain-specific fields (no tenant_path!)
  string email = 2;
  string username = 3;
}
```

### Middleware/Gateway Integration

```go
// Resolve tenant context at API gateway
func ResolveTenant(ctx context.Context, req *Request) (*TenantContext, error) {
    // Extract from bearer token, API key, or header
    tenantID := extractTenantID(req)
    
    // Resolve full context including hierarchy
    return tenantService.ResolveTenantContext(ctx, &ResolveTenantContextRequest{
        Source:     TenantResolutionSource_TOKEN,
        Identifier: tenantID,
        SubjectID:  extractSubjectID(req),
    })
}
```

## Compliance

- **SOC 2 CC6.1**: Logical access controls via tenant isolation
- **SOC 2 CC6.3**: Audit trail via tenant lifecycle events
- **GDPR Article 5**: Data isolation by design
- **GDPR Article 17**: Tenant deletion with data erasure support
- **ISO 27001 A.9.1**: Access control policy via tenant boundaries

## Events

| Event | Trigger | Use Case |
|-------|---------|----------|
| `TenantCreated` | New tenant provisioned | Infrastructure provisioning |
| `TenantUpdated` | Settings/config changed | Configuration propagation |
| `TenantStatusChanged` | Status transition | Workflow automation |
| `TenantDeleted` | Soft-delete initiated | Cleanup, archival |
| `TenantMemberAdded` | User joins tenant | Access provisioning |
| `TenantMemberRemoved` | User leaves tenant | Access revocation |
| `TenantSettingsChanged` | Policy updated | Policy enforcement |

## Best Practices

1. **Never embed tenant_path in domain entities** - Use TenantContext in API layer
2. **Resolve tenant early** - Middleware should resolve context before handler
3. **Validate membership** - Ensure subject has membership in requested tenant
4. **Use hierarchical access** - Leverage effective_tenant_ids for inherited permissions
5. **Audit everything** - Publish events for all tenant operations
