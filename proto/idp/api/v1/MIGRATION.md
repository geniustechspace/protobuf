# Migration Guide: Legacy Consolidated API → Modular Subdomain APIs

## Overview

The legacy consolidated API files (`authn_api.proto`, `authz_api.proto`, `identity_api.proto`, `services.proto`) are **deprecated** in favor of modular subdomain-specific APIs.

**Migration Timeline:**
- **Deprecated:** Current version (v1)
- **Support End:** 6 months from deprecation notice
- **Removal:** After support period

## Why Migrate?

The modular subdomain APIs provide:
- **Better separation of concerns** - Each subdomain has isolated API layer
- **Independent versioning** - Update one subdomain without affecting others
- **Clearer ownership** - Domain-driven boundaries match team structure
- **Reduced coupling** - Services depend only on what they need
- **Smaller generated clients** - Import only required subdomains

## Architecture Change

### Before (Deprecated)
```
proto/idp/api/v1/
├── authn_api.proto      (all authentication APIs)
├── authz_api.proto      (all authorization APIs)
├── identity_api.proto   (all identity APIs)
└── services.proto       (all services combined)
```

### After (Current)
```
proto/idp/
├── identity/
│   ├── user/api/v1/         (User subdomain API)
│   ├── group/api/v1/        (Group subdomain API)
│   ├── organization/api/v1/ (Organization subdomain API)
│   └── profile/api/v1/      (Profile subdomain API)
├── authn/
│   ├── credential/api/v1/   (Credential subdomain API)
│   ├── session/api/v1/      (Session subdomain API)
│   └── mfa/api/v1/          (MFA subdomain API)
└── authz/
    ├── permission/api/v1/   (Permission subdomain API)
    ├── role/api/v1/         (Role subdomain API)
    └── policy/api/v1/       (Policy subdomain API)
```

## Migration Mappings

### Identity Domain

#### User Operations

**Legacy Import:**
```protobuf
import "idp/api/v1/identity_api.proto";
```

**New Import:**
```protobuf
import "idp/identity/user/api/v1/service.proto";
```

**Package Change:**
- Before: `geniustechspace.idp.api.v1`
- After: `geniustechspace.idp.identity.user.api.v1`

**Example Migration:**
```protobuf
// Before
service IdentityService {
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
  rpc UpdateUser(UpdateUserRequest) returns (UpdateUserResponse);
  rpc DeleteUser(DeleteUserRequest) returns (DeleteUserResponse);
  rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
}

// After
service UserService {
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
  rpc UpdateUser(UpdateUserRequest) returns (UpdateUserResponse);
  rpc DeleteUser(DeleteUserRequest) returns (DeleteUserResponse);
  rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
}
```

#### Group Operations

**Legacy Import:**
```protobuf
import "idp/api/v1/identity_api.proto";
```

**New Import:**
```protobuf
import "idp/identity/group/api/v1/service.proto";
```

**Service Change:**
- Before: `IdentityService.CreateGroup`, `IdentityService.GetGroup`, etc.
- After: `GroupService.CreateGroup`, `GroupService.GetGroup`, etc.

#### Organization Operations

**Legacy Import:**
```protobuf
import "idp/api/v1/identity_api.proto";
```

**New Import:**
```protobuf
import "idp/identity/organization/api/v1/service.proto";
```

**Service Change:**
- Before: `IdentityService.CreateOrganization`, `IdentityService.GetOrganization`, etc.
- After: `OrganizationService.CreateOrganization`, `OrganizationService.GetOrganization`, etc.

#### Profile Operations

**Legacy Import:**
```protobuf
import "idp/api/v1/identity_api.proto";
```

**New Import:**
```protobuf
import "idp/identity/profile/api/v1/service.proto";
```

**Service Change:**
- Before: `IdentityService.GetUserProfile`, `IdentityService.UpdateUserProfile`
- After: `ProfileService.GetProfile`, `ProfileService.UpdateProfile`

### Authentication Domain

#### Credential Operations

**Legacy Import:**
```protobuf
import "idp/api/v1/authn_api.proto";
```

**New Import:**
```protobuf
import "idp/authn/credential/api/v1/service.proto";
```

**Package Change:**
- Before: `geniustechspace.idp.api.v1`
- After: `geniustechspace.idp.authn.credential.api.v1`

**Example Migration:**
```protobuf
// Before (in AuthenticationService)
rpc CreateCredential(CreateCredentialRequest) returns (CreateCredentialResponse);
rpc VerifyCredential(VerifyCredentialRequest) returns (VerifyCredentialResponse);

// After (in CredentialService)
rpc CreateCredential(CreateCredentialRequest) returns (CreateCredentialResponse);
rpc VerifyCredential(VerifyCredentialRequest) returns (VerifyCredentialResponse);
```

#### Session Operations

**Legacy Import:**
```protobuf
import "idp/api/v1/authn_api.proto";
```

**New Import:**
```protobuf
import "idp/authn/session/api/v1/service.proto";
```

**Service Change:**
- Before: `AuthenticationService.CreateSession`, `AuthenticationService.ValidateSession`
- After: `SessionService.CreateSession`, `SessionService.ValidateSession`

#### MFA Operations

**Legacy Import:**
```protobuf
import "idp/api/v1/authn_api.proto";
```

**New Import:**
```protobuf
import "idp/authn/mfa/api/v1/service.proto";
```

**Service Change:**
- Before: `AuthenticationService.EnrollMFA`, `AuthenticationService.VerifyMFA`
- After: `MfaService.EnrollMfa`, `MfaService.VerifyMfa`

### Authorization Domain

#### Permission Operations

**Legacy Import:**
```protobuf
import "idp/api/v1/authz_api.proto";
```

**New Import:**
```protobuf
import "idp/authz/permission/api/v1/service.proto";
```

**Package Change:**
- Before: `geniustechspace.idp.api.v1`
- After: `geniustechspace.idp.authz.permission.api.v1`

**Service Change:**
- Before: `AuthorizationService.CheckPermission`, `AuthorizationService.GrantPermission`
- After: `PermissionService.CheckPermission`, `PermissionService.GrantPermission`

#### Role Operations

**Legacy Import:**
```protobuf
import "idp/api/v1/authz_api.proto";
```

**New Import:**
```protobuf
import "idp/authz/role/api/v1/service.proto";
```

**Service Change:**
- Before: `AuthorizationService.CreateRole`, `AuthorizationService.AssignRole`
- After: `RoleService.CreateRole`, `RoleService.AssignRole`

#### Policy Operations

**Legacy Import:**
```protobuf
import "idp/api/v1/authz_api.proto";
```

**New Import:**
```protobuf
import "idp/authz/policy/api/v1/service.proto";
```

**Service Change:**
- Before: `AuthorizationService.CreatePolicy`, `AuthorizationService.EvaluatePolicy`
- After: `PolicyService.CreatePolicy`, `PolicyService.EvaluatePolicy`

## Code Migration Examples

### Go Client Migration

#### Before (Legacy)
```go
import (
    idpv1 "github.com/geniustechspace/protobuf/gen/go/idp/api/v1"
)

// Create user using legacy consolidated service
client := idpv1.NewIdentityServiceClient(conn)
resp, err := client.CreateUser(ctx, &idpv1.CreateUserRequest{
    TenantId: "tenant-123",
    Email: "user@example.com",
})
```

#### After (Modular)
```go
import (
    userapiv1 "github.com/geniustechspace/protobuf/gen/go/idp/identity/user/api/v1"
)

// Create user using modular subdomain service
client := userapiv1.NewUserServiceClient(conn)
resp, err := client.CreateUser(ctx, &userapiv1.CreateUserRequest{
    TenantId: "tenant-123",
    Email: "user@example.com",
})
```

### Python Client Migration

#### Before (Legacy)
```python
from geniustechspace.protobuf.idp.api.v1 import services_pb2, services_pb2_grpc

# Create channel and stub
channel = grpc.insecure_channel('localhost:50051')
stub = services_pb2_grpc.IdentityServiceStub(channel)

# Create user
response = stub.CreateUser(services_pb2.CreateUserRequest(
    tenant_id="tenant-123",
    email="user@example.com"
))
```

#### After (Modular)
```python
from geniustechspace.protobuf.idp.identity.user.api.v1 import (
    service_pb2, 
    service_pb2_grpc
)

# Create channel and stub
channel = grpc.insecure_channel('localhost:50051')
stub = service_pb2_grpc.UserServiceStub(channel)

# Create user
response = stub.CreateUser(service_pb2.CreateUserRequest(
    tenant_id="tenant-123",
    email="user@example.com"
))
```

### TypeScript/JavaScript Migration

#### Before (Legacy)
```typescript
import { IdentityServiceClient } from '@geniustechspace/protobuf/idp/api/v1/services_grpc_pb';
import { CreateUserRequest } from '@geniustechspace/protobuf/idp/api/v1/identity_api_pb';

const client = new IdentityServiceClient('localhost:50051', credentials);

const request = new CreateUserRequest();
request.setTenantId('tenant-123');
request.setEmail('user@example.com');

client.createUser(request, (err, response) => {
    // Handle response
});
```

#### After (Modular)
```typescript
import { UserServiceClient } from '@geniustechspace/protobuf/idp/identity/user/api/v1/service_grpc_pb';
import { CreateUserRequest } from '@geniustechspace/protobuf/idp/identity/user/api/v1/request_pb';

const client = new UserServiceClient('localhost:50051', credentials);

const request = new CreateUserRequest();
request.setTenantId('tenant-123');
request.setEmail('user@example.com');

client.createUser(request, (err, response) => {
    // Handle response
});
```

## Request/Response Message Changes

### Breaking Changes

Most request/response messages **retain the same structure** but are now defined in subdomain-specific files:

**Before:**
- Defined in: `proto/idp/api/v1/identity_api.proto`
- Package: `geniustechspace.idp.api.v1`
- Message: `CreateUserRequest`, `CreateUserResponse`

**After:**
- Defined in: `proto/idp/identity/user/api/v1/request.proto` and `response.proto`
- Package: `geniustechspace.idp.identity.user.api.v1`
- Message: Same names, different package

### Field Changes

**Entity Audit Fields** have been standardized across all entities:

**Before (inconsistent):**
```protobuf
message User {
    // Some entities had nested metadata
    core.metadata.v1.Metadata metadata = 10;
    
    // Some entities had created_by
    string created_by = 11;
    
    // Some entities had boolean deleted
    bool deleted = 12;
}
```

**After (standardized):**
```protobuf
message User {
    // All entities now use flattened audit fields
    google.protobuf.Timestamp created_at = 2 [(buf.validate.field).required = true];
    google.protobuf.Timestamp updated_at = 3;
    google.protobuf.Timestamp deleted_at = 7;  // NULL = active, NOT NULL = deleted
    int64 version = 6;  // Optimistic locking
}
```

**Impact:** If your code accesses `metadata.created_at`, change to `created_at`. Remove references to `created_by` and `deleted` boolean.

## gRPC Service Endpoints

### Before (Consolidated Services)
```
# Single service with all operations
grpc://your-idp-server.com/geniustechspace.idp.api.v1.IdentityService/CreateUser
grpc://your-idp-server.com/geniustechspace.idp.api.v1.IdentityService/CreateGroup
grpc://your-idp-server.com/geniustechspace.idp.api.v1.AuthenticationService/CreateSession
grpc://your-idp-server.com/geniustechspace.idp.api.v1.AuthorizationService/CheckPermission
```

### After (Modular Services)
```
# Separate services per subdomain
grpc://your-idp-server.com/geniustechspace.idp.identity.user.api.v1.UserService/CreateUser
grpc://your-idp-server.com/geniustechspace.idp.identity.group.api.v1.GroupService/CreateGroup
grpc://your-idp-server.com/geniustechspace.idp.authn.session.api.v1.SessionService/CreateSession
grpc://your-idp-server.com/geniustechspace.idp.authz.permission.api.v1.PermissionService/CheckPermission
```

**Impact:** Update service registrations in your gRPC server and client connection logic.

## Testing Strategy

1. **Parallel Running**: Run both legacy and new APIs during transition period
2. **Feature Flags**: Use flags to toggle between legacy/new API usage
3. **Gradual Migration**: Migrate one subdomain at a time
4. **Integration Tests**: Update tests to use new package paths
5. **Monitor Metrics**: Track legacy API usage to identify remaining dependencies

## Migration Checklist

- [ ] Identify all files importing `idp/api/v1/` protos
- [ ] Update imports to subdomain-specific paths
- [ ] Update package references in code
- [ ] Update service client instantiation
- [ ] Update gRPC service registrations (server-side)
- [ ] Replace `metadata.created_at` with `created_at` (and similar for other audit fields)
- [ ] Remove references to `created_by` and `deleted` boolean
- [ ] Update integration tests
- [ ] Update documentation
- [ ] Run `buf generate` to regenerate clients
- [ ] Test thoroughly in staging environment
- [ ] Deploy to production
- [ ] Monitor for errors
- [ ] Remove legacy API imports after validation

## Support

For migration assistance:
- **Documentation**: See `proto/idp/ARCHITECTURE.md` for subdomain structure
- **Issues**: File GitHub issues with `migration` label
- **Examples**: Check `proto/idp/identity/user/api/v1/` for reference implementation

## FAQ

**Q: Can I use both legacy and new APIs during migration?**  
A: Yes, both are supported during the transition period (6 months).

**Q: Will message field numbers change?**  
A: No, field numbers remain stable. Only package names change.

**Q: Do I need to update my database schema?**  
A: Yes, if you persisted `metadata` nested objects. Flatten to `created_at`, `updated_at`, `deleted_at`, `version` fields. Remove `created_by` and `deleted` boolean.

**Q: How do I handle breaking changes?**  
A: The main breaking change is audit field structure. Update entity persistence layer to use flattened fields. Check `deleted_at IS NULL` for active records instead of `deleted = false`.

**Q: When will legacy APIs be removed?**  
A: 6 months after this deprecation notice. Monitor changelog for exact removal date.

**Q: Can I request extension of support period?**  
A: Yes, contact maintainers with justification for extension request.
