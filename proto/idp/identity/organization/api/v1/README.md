# Organization API Layer

**Package:** `geniustechspace.idp.identity.organization.api.v1`

## Overview

gRPC service for organization lifecycle management. Provides CRUD operations and domain-specific actions.

## Service: OrganizationService

### Authentication

All RPCs require Bearer token authentication.

### Authorization

Permission-based access control:
- `idp:organizations:create` - Create new organization
- `idp:organizations:read` - Read organization details
- `idp:organizations:update` - Modify organization
- `idp:organizations:delete` - Delete organization
- `idp:organizations:list` - List organizations

### Rate Limits

- Standard operations: 100/min per tenant
- Write operations: 50/min per tenant

## Operations

### CreateOrganization

Create new organization entity.

**Request:** `CreateOrganizationRequest`  
**Response:** `CreateOrganizationResponse`  
**Events:** Publishes `OrganizationCreated`

### GetOrganization

Retrieve organization by ID.

**Request:** `GetOrganizationRequest { tenant_id, organization_id }`  
**Response:** `GetOrganizationResponse { organization }`

### UpdateOrganization

Modify existing organization.

**Request:** `UpdateOrganizationRequest` (partial update)  
**Response:** `UpdateOrganizationResponse`  
**Events:** Publishes `OrganizationUpdated`

### DeleteOrganization

Soft-delete or hard-delete organization.

**Request:** `DeleteOrganizationRequest { hard_delete }`  
**Response:** `DeleteOrganizationResponse`  
**Events:** Publishes `OrganizationDeleted`

### ListOrganizations

Paginated list with optional filters.

**Request:** `ListOrganizationsRequest { pagination, filters }`  
**Response:** `ListOrganizationsResponse { organizations, pagination }`

## Validation

All requests validated using `buf/validate`. Validation errors return `INVALID_ARGUMENT`.

## Compliance

- **SOC 2 CC6.1:** Access control and audit trails
- **ISO 27001 A.9.2:** User access management

## Code Generation

```bash
buf generate --path proto/idp/identity/organization/api/v1
```

## Related Documentation

- **Domain Model:** `../v1/README.md`
- **Domain Events:** `../events/v1/README.md`
