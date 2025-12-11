# Role API Layer

**Package:** `geniustechspace.idp.authz.role.api.v1`

## Overview

gRPC service for role management in authorization workflows.

## Service: RoleService

### Authentication

All RPCs require Bearer token authentication.

### Authorization

Permission-based access control for managing authorization configurations:
- `idp:authz:roles:create` - Create role
- `idp:authz:roles:read` - Read role details
- `idp:authz:roles:update` - Modify role
- `idp:authz:roles:delete` - Delete role

### Rate Limits

- Standard operations: 100/min per tenant
- Evaluation operations: 1000/min per tenant (high throughput for real-time checks)

## Operations

CRUD operations for role management plus evaluation/checking operations for real-time authorization decisions.

## Compliance

- **SOC 2 CC6.1:** Access control management and audit trails
- **ISO 27001 A.9.2:** User access management procedures
- **Least Privilege:** Enforce minimal necessary access

## Related Documentation

- **Domain Model:** `../v1/README.md`
- **Domain Events:** `../events/v1/README.md`
