# Group API Layer

**Package:** `geniustechspace.idp.identity.group.api.v1`

## Overview

gRPC service for group lifecycle management. Provides CRUD operations and domain-specific actions.

## Service: GroupService

### Authentication

All RPCs require Bearer token authentication.

### Authorization

Permission-based access control:
- `idp:groups:create` - Create new group
- `idp:groups:read` - Read group details
- `idp:groups:update` - Modify group
- `idp:groups:delete` - Delete group
- `idp:groups:list` - List groups

### Rate Limits

- Standard operations: 100/min per tenant
- Write operations: 50/min per tenant

## Operations

### CreateGroup

Create new group entity.

**Request:** `CreateGroupRequest`  
**Response:** `CreateGroupResponse`  
**Events:** Publishes `GroupCreated`

### GetGroup

Retrieve group by ID.

**Request:** `GetGroupRequest { tenant_id, group_id }`  
**Response:** `GetGroupResponse { group }`

### UpdateGroup

Modify existing group.

**Request:** `UpdateGroupRequest` (partial update)  
**Response:** `UpdateGroupResponse`  
**Events:** Publishes `GroupUpdated`

### DeleteGroup

Soft-delete or hard-delete group.

**Request:** `DeleteGroupRequest { hard_delete }`  
**Response:** `DeleteGroupResponse`  
**Events:** Publishes `GroupDeleted`

### ListGroups

Paginated list with optional filters.

**Request:** `ListGroupsRequest { pagination, filters }`  
**Response:** `ListGroupsResponse { groups, pagination }`

## Validation

All requests validated using `buf/validate`. Validation errors return `INVALID_ARGUMENT`.

## Compliance

- **SOC 2 CC6.1:** Access control and audit trails
- **ISO 27001 A.9.2:** User access management

## Code Generation

```bash
buf generate --path proto/idp/identity/group/api/v1
```

## Related Documentation

- **Domain Model:** `../v1/README.md`
- **Domain Events:** `../events/v1/README.md`
