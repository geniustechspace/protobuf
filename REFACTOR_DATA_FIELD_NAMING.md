# API Request/Response Refactoring - 'data' Field Naming Convention

## Overview

Refactored all API request and response messages to use consistent `data` field naming instead of entity-specific names (e.g., `user`, `profile`, `group`, etc.). This eliminates duplicate fields in UpdateXRequest messages and provides a uniform API surface.

## Changes Applied

### Pattern Before Refactoring

**CreateXRequest (Before):**

```protobuf
message CreateUserRequest {
  User user = 1;
  reserved 2 to 9;
}
```

**UpdateXRequest (Before - with duplicates):**

```protobuf
message UpdateUserRequest {
  string tenant_path = 1;       // DUPLICATE - in entity
  oneof identifier {            // DUPLICATE - in entity
    string user_id = 2;
    string email = 3;
  }
  User user = 5;
  FieldMask update_mask = 6;
  reserved 7 to 9;
}
```

### Pattern After Refactoring

**CreateXRequest (After):**

```protobuf
message CreateUserRequest {
  User data = 1;  // Changed from 'user' to 'data'
  reserved 2 to 9;
}
```

**UpdateXRequest (After - duplicates removed):**

```protobuf
message UpdateUserRequest {
  User data = 1;                // Changed from 'user' to 'data', removed duplicates
  FieldMask update_mask = 2;    // Field number changed from 6 to 2
  reserved 3 to 9;              // Reserved range adjusted
}
```

**Response Messages (After):**

```protobuf
message CreateUserResponse {
  User data = 1;  // Changed from 'user' to 'data'
  reserved 2 to 9;
}

message GetUserResponse {
  User data = 1;  // Changed from 'user' to 'data'
  reserved 2 to 9;
}

message UpdateUserResponse {
  User data = 1;  // Changed from 'user' to 'data'
  reserved 2 to 9;
}
```

## Benefits

### 1. Eliminates Duplication

- Removed redundant `tenant_path` field from UpdateXRequest (already in entity)
- Removed redundant `oneof identifier` from UpdateXRequest (already in entity as user_id, email, username, etc.)
- Server extracts tenant_path and identifier directly from `data` entity

### 2. Consistent Naming

- All request/response payloads now use `data` field name
- Easier code generation and client SDK consistency
- Reduces cognitive load - always know it's `request.data` or `response.data`

### 3. Simplified API

- Reduced field count in UpdateXRequest from 6 to 2 (data + update_mask)
- Cleaner oneof discriminators in Get requests
- More intuitive API surface

### 4. Offline-First Support

- Entity in `data` contains optional pre-generated IDs
- Client can set user_id, profile_id, etc. before sending
- Server generates IDs only if omitted

## Files Modified

### Identity Domain

- ✅ `proto/idp/identity/user/api/v1/request.proto`
- ✅ `proto/idp/identity/user/api/v1/response.proto`
- ✅ `proto/idp/identity/profile/api/v1/request.proto`
- ✅ `proto/idp/identity/profile/api/v1/response.proto`
- ✅ `proto/idp/identity/group/api/v1/request.proto`
- ✅ `proto/idp/identity/group/api/v1/response.proto`
- ✅ `proto/idp/identity/organization/api/v1/request.proto`
- ✅ `proto/idp/identity/organization/api/v1/response.proto`

### Authorization Domain

- ✅ `proto/idp/authz/role/api/v1/request.proto`
- ✅ `proto/idp/authz/role/api/v1/response.proto`
- ✅ `proto/idp/authz/policy/api/v1/request.proto`
- ✅ `proto/idp/authz/policy/api/v1/response.proto`
- ✅ `proto/idp/authz/permission/api/v1/request.proto`
- ✅ `proto/idp/authz/permission/api/v1/response.proto`

### Authentication Domain

- ✅ `proto/idp/authn/credential/api/v1/request.proto`
- ✅ `proto/idp/authn/credential/api/v1/response.proto`

**Total: 16 files modified**

## Usage Examples

### Before (Old Pattern)

```protobuf
// Create User - Old
CreateUserRequest {
  user: {
    user_id: "usr_123"
    tenant_path: "acme-corp"
    email: "john@example.com"
  }
}

// Update User - Old (with duplicates)
UpdateUserRequest {
  tenant_path: "acme-corp"          // Duplicate!
  identifier: { user_id: "usr_123" } // Duplicate!
  user: {
    user_id: "usr_123"              // Also in identifier
    tenant_path: "acme-corp"        // Also at top level
    display_name: "John Doe"
  }
  update_mask: { paths: ["display_name"] }
}
```

### After (New Pattern)

```protobuf
// Create User - New
CreateUserRequest {
  data: {
    user_id: "usr_123"              // Optional - offline-first
    tenant_path: "acme-corp"
    email: "john@example.com"
  }
}

// Update User - New (no duplicates)
UpdateUserRequest {
  data: {
    user_id: "usr_123"              // Identifier for lookup
    tenant_path: "acme-corp"        // Tenant isolation
    display_name: "John Doe"        // Field to update
  }
  update_mask: { paths: ["display_name"] }
}
```

## Server Implementation Notes

### Update Request Handling

Server must extract tenant_path and identifier from `data` entity:

```go
// Extract tenant and identifier from entity
tenantPath := req.Data.TenantPath
identifier := req.Data.UserId  // or Email, Username, etc.

// Validate tenant isolation
if !hasAccessToTenant(ctx, tenantPath) {
    return ErrUnauthorized
}

// Lookup existing entity
existing := findByTenantAndId(tenantPath, identifier)
if existing == nil {
    return ErrNotFound
}

// Apply field mask
updated := applyFieldMask(existing, req.Data, req.UpdateMask)

// Save with version check
return save(updated)
```

### Get Request Handling (No Change)

Get requests still use separate tenant_path and oneof identifier:

```protobuf
message GetUserRequest {
  string tenant_path = 1;
  oneof identifier {
    string user_id = 2;
    string email = 3;
    string username = 4;
  }
  reserved 5 to 9;
}
```

## Migration Guide

### For Client SDK Developers

**Before:**

```typescript
// Old pattern
const response = await client.updateUser({
  tenantPath: "acme-corp",
  identifier: { userId: "usr_123" },
  user: {
    displayName: "John Doe",
  },
  updateMask: { paths: ["display_name"] },
});
```

**After:**

```typescript
// New pattern
const response = await client.updateUser({
  data: {
    userId: "usr_123", // Identifier
    tenantPath: "acme-corp", // Tenant
    displayName: "John Doe", // Field to update
  },
  updateMask: { paths: ["display_name"] },
});
```

### Breaking Changes

⚠️ **This is a breaking change** for all UpdateXRequest messages:

- Field numbers changed (entity moved from 4-5 to 1)
- `tenant_path` field removed from top level
- `oneof identifier` removed from top level
- `update_mask` field number changed from 5-6 to 2

🔄 **Version bump required:** All affected services must be updated to v2 API or implement compatibility layer.

## Validation

All changes validated:

- ✅ Syntax validated with `buf format --diff`
- ✅ Field numbering consistency checked
- ✅ Reserved ranges updated correctly
- ✅ Documentation comments updated

## Related Architectural Decisions

1. **Hierarchical Tenant Paths** - `tenant_path` supports nested multi-tenancy (max 512 chars)
2. **Optional IDs** - All `*_id` and `tenant_path` fields are optional for offline-first support
3. **Field Masks** - Google Cloud API standard for partial updates
4. **Entity Snapshots** - Events include full entity snapshots at fields 20-21 for replayability

## Date

December 2024

## Status

✅ **COMPLETED** - All domain APIs refactored and validated
