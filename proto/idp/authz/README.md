# IDP Authorization (authz)

Role-Based Access Control (RBAC) and permission management for enterprise identity providers.

## Package

```protobuf
package geniustechspace.idp.authz.v1;
```

## Overview

The authorization module provides:

- **Permission Checking** - Check if user has permission for resource action
- **Role Management** - Assign and revoke roles
- **RBAC** - Role-Based Access Control with role hierarchy
- **ABAC Support** - Attribute-Based Access Control with conditional logic
- **Policy-Based** - Flexible policy evaluation

## Files

- `enums.proto` - Authorization enumerations
- `messages.proto` - Request/response messages
- `service.proto` - gRPC service definition

## Usage Examples

### Check Permission

```protobuf
CheckPermissionRequest request = {
  tenant_id: "tenant_123",
  user_id: "user_456",
  resource: "document:doc_789",
  action: "read"
};

CheckPermissionResponse response = authz_service.CheckPermission(request);
if (response.allowed) {
  // Grant access
}
```

### Assign Role

```protobuf
AssignRoleRequest request = {
  tenant_id: "tenant_123",
  user_id: "user_456",
  role_id: "role_editor",
  assigned_by: "admin_123"
};

AssignRoleResponse response = authz_service.AssignRole(request);
```

### Temporary Role

```protobuf
AssignRoleRequest request = {
  tenant_id: "tenant_123",
  user_id: "user_456",
  role_id: "role_temp_admin",
  expires_at: timestamp("2025-12-31T23:59:59Z"),
  assigned_by: "admin_123"
};
```

## Import Path

```protobuf
import "idp/authz/v1/enums.proto";
import "idp/authz/v1/messages.proto";
import "idp/authz/v1/service.proto";
```

## See Also

- [IDP API Common](../api/README.md)
- [Main IDP README](../README.md)
