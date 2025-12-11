# User API Layer

**Package:** `geniustechspace.idp.identity.user.api.v1`

## Overview

gRPC service definitions for user lifecycle management. Provides CRUD operations, search, status management, and verification endpoints for user accounts.

## Purpose

- Expose user domain operations via gRPC
- Enforce authentication and authorization
- Validate request payloads using buf/validate
- Publish domain events on mutations
- Provide multi-tenant isolation

## Service: UserService

### Authentication

**All RPCs require authentication:**

- Bearer token in metadata: `authorization: Bearer <token>`
- Token validated by auth interceptor
- Invalid/expired tokens return `UNAUTHENTICATED` status

### Authorization

**Permission-based access control:**

| Operation        | Required Permission       | Self-Access Allowed  |
| ---------------- | ------------------------- | -------------------- |
| CreateUser       | `idp:users:create`        | No                   |
| GetUser          | `idp:users:read`          | Yes (own user_id)    |
| UpdateUser       | `idp:users:update`        | Yes (limited fields) |
| DeleteUser       | `idp:users:delete`        | No                   |
| ListUsers        | `idp:users:list`          | No                   |
| SearchUsers      | `idp:users:search`        | No                   |
| UpdateUserStatus | `idp:users:status:update` | No                   |
| VerifyUserEmail  | `idp:users:email:verify`  | Yes (token-based)    |
| VerifyUserPhone  | `idp:users:phone:verify`  | Yes (code-based)     |

**Self-Access:** Users can read/update their own profile without elevated permissions. Update operation restricts writable fields for self-access (cannot modify status, organization memberships).

### Rate Limits

Per-tenant rate limits enforced:

- **CreateUser:** 20/min (prevent bulk account creation abuse)
- **GetUser:** 100/min
- **UpdateUser:** 50/min
- **DeleteUser:** 20/min (prevent bulk deletion)
- **ListUsers:** 50/min
- **SearchUsers:** 30/min (search is expensive)
- **UpdateUserStatus:** 50/min
- **VerifyUserEmail:** 10/min per user
- **VerifyUserPhone:** 10/min per user

Rate limit exceeded returns `RESOURCE_EXHAUSTED` status with `Retry-After` header.

## Operations

### CreateUser

**Purpose:** Provision new user account

**Request:**

```protobuf
message CreateUserRequest {
  string tenant_id = 1;        // REQUIRED
  string email = 2;            // REQUIRED, unique per tenant
  string display_name = 3;     // OPTIONAL
  string given_name = 4;       // OPTIONAL
  string family_name = 5;      // OPTIONAL
  string phone_number = 6;     // OPTIONAL, E.164 format
  string preferred_language = 7; // OPTIONAL, ISO 639-1
  string timezone = 8;         // OPTIONAL, IANA timezone
  string avatar_url = 9;       // OPTIONAL, HTTPS URL
  map<string, string> metadata = 10; // OPTIONAL, max 50 entries
  repeated string organization_ids = 11; // OPTIONAL
  repeated string group_ids = 12;        // OPTIONAL
}
```

**Response:** `CreateUserResponse { User user = 1; }`

**Events Published:** `UserCreated`

**Error Codes:**

- `ALREADY_EXISTS` - Email already registered in tenant
- `INVALID_ARGUMENT` - Validation failed (invalid email, phone format, etc.)
- `PERMISSION_DENIED` - Missing `idp:users:create` permission

**Example (gRPC CLI):**

```bash
grpcurl -d '{
  "tenant_id": "tnt_abc123",
  "email": "john.doe@example.com",
  "display_name": "John Doe",
  "given_name": "John",
  "family_name": "Doe"
}' \
-H "authorization: Bearer $TOKEN" \
idp-api.example.com:443 \
geniustechspace.idp.identity.user.api.v1.UserService/CreateUser
```

### GetUser

**Purpose:** Retrieve user by ID

**Request:**

```protobuf
message GetUserRequest {
  string tenant_id = 1;  // REQUIRED
  string user_id = 2;    // REQUIRED
}
```

**Response:** `GetUserResponse { User user = 1; }`

**Error Codes:**

- `NOT_FOUND` - User does not exist in tenant
- `PERMISSION_DENIED` - Missing permission (unless self-access)

### UpdateUser

**Purpose:** Modify user profile and memberships

**Request:**

```protobuf
message UpdateUserRequest {
  string tenant_id = 1;   // REQUIRED
  string user_id = 2;     // REQUIRED
  optional string display_name = 3;
  optional string given_name = 4;
  optional string family_name = 5;
  optional string phone_number = 6;
  optional string preferred_language = 7;
  optional string timezone = 8;
  optional string avatar_url = 9;
  map<string, string> metadata = 10;       // Merge operation
  repeated string organization_ids = 11;   // Replace operation
  repeated string group_ids = 12;          // Replace operation
}
```

**Partial Update:** Only provided fields are modified. Use `optional` to distinguish between "not provided" and "set to empty".

**Metadata:** Merge operation - new keys added, existing keys updated, empty value removes key.

**Memberships:** Replace operation - provided IDs replace entire membership list.

**Response:** `UpdateUserResponse { User user = 1; }`

**Events Published:** `UserUpdated`

**Error Codes:**

- `NOT_FOUND` - User does not exist
- `INVALID_ARGUMENT` - Validation failed
- `PERMISSION_DENIED` - Missing permission or attempting restricted field update

### DeleteUser

**Purpose:** Soft-delete or hard-delete user account

**Request:**

```protobuf
message DeleteUserRequest {
  string tenant_id = 1;   // REQUIRED
  string user_id = 2;     // REQUIRED
  bool hard_delete = 3;   // false = soft delete, true = permanent erasure
}
```

**Soft Delete:** User status set to `DELETED`, data retained per retention policy  
**Hard Delete:** Permanent data erasure per GDPR Article 17 (Right to erasure)

**Response:** `DeleteUserResponse { string user_id = 1; bool hard_deleted = 2; }`

**Events Published:** `UserDeleted`

**Side Effects:**

- Hard delete: Sessions invalidated, credentials purged, audit log retained
- Soft delete: Sessions invalidated, credentials disabled, data retained

**Error Codes:**

- `NOT_FOUND` - User does not exist
- `PERMISSION_DENIED` - Missing `idp:users:delete` permission

### ListUsers

**Purpose:** Paginated list of users with optional filters

**Request:**

```protobuf
message ListUsersRequest {
  string tenant_id = 1;
  core.v1.PaginationRequest pagination = 2;  // page_size, page_token
  optional string organization_id = 3;       // Filter by org
  optional string group_id = 4;              // Filter by group
  optional UserStatus status = 5;            // Filter by status
}
```

**Pagination:** Use `page_token` from previous response for next page. Default `page_size=50`, max `100`.

**Response:**

```protobuf
message ListUsersResponse {
  repeated User users = 1;
  core.v1.PaginationResponse pagination = 2;  // next_page_token, total_count
}
```

**Error Codes:**

- `INVALID_ARGUMENT` - Invalid page_token or filters
- `PERMISSION_DENIED` - Missing `idp:users:list` permission

### SearchUsers

**Purpose:** Full-text search across user fields

**Request:**

```protobuf
message SearchUsersRequest {
  string tenant_id = 1;
  string query = 2;  // REQUIRED, min 2 chars, searches email/display_name/given_name/family_name
  core.v1.PaginationRequest pagination = 3;
  optional UserStatus status = 4;
}
```

**Search Fields:** email, display_name, given_name, family_name (case-insensitive, partial match)

**Response:** Same as `ListUsersResponse`

**Performance:** Search queries are expensive. Enforce rate limit (30/min). Consider dedicated search index (Elasticsearch) for large datasets.

**Error Codes:**

- `INVALID_ARGUMENT` - Query too short (<2 chars)
- `PERMISSION_DENIED` - Missing `idp:users:search` permission

### UpdateUserStatus

**Purpose:** Change user account status (e.g., suspend, activate)

**Request:**

```protobuf
message UpdateUserStatusRequest {
  string tenant_id = 1;
  string user_id = 2;
  UserStatus status = 3;   // Cannot be UNSPECIFIED
  string reason = 4;       // OPTIONAL, audit trail
}
```

**Valid Transitions:** See `../v1/README.md` for status state machine

**Response:** `UpdateUserStatusResponse { User user = 1; }`

**Events Published:** `UserStatusChanged`

**Side Effects:**

- `SUSPENDED`, `LOCKED`, `DELETED` → invalidate active sessions
- `PENDING_VERIFICATION` → trigger verification flow

**Error Codes:**

- `NOT_FOUND` - User does not exist
- `INVALID_ARGUMENT` - Invalid status transition
- `PERMISSION_DENIED` - Missing `idp:users:status:update` permission

### VerifyUserEmail

**Purpose:** Mark email as verified (token-based or admin override)

**Request:**

```protobuf
message VerifyUserEmailRequest {
  string tenant_id = 1;
  string user_id = 2;
  optional string verification_token = 3;  // From verification email link
}
```

**Verification Flow:**

1. User receives email with verification link containing token
2. User clicks link, frontend calls `VerifyUserEmail` with token
3. Server validates token, sets `email_verified=true`

**Admin Override:** If `verification_token` not provided, requires `idp:users:email:verify` permission (admin can force verify).

**Response:** `VerifyUserEmailResponse { User user = 1; }`

**Events Published:** `UserUpdated` (updated_fields includes "email_verified")

**Error Codes:**

- `NOT_FOUND` - User or token does not exist
- `INVALID_ARGUMENT` - Token expired or invalid
- `PERMISSION_DENIED` - Missing permission (if token not provided)

### VerifyUserPhone

**Purpose:** Mark phone as verified (OTP-based or admin override)

**Request:**

```protobuf
message VerifyUserPhoneRequest {
  string tenant_id = 1;
  string user_id = 2;
  optional string verification_code = 3;  // 6-digit OTP from SMS
}
```

**Verification Flow:**

1. User requests phone verification, system sends SMS with 6-digit code
2. User submits code, frontend calls `VerifyUserPhone` with code
3. Server validates code (time-limited), sets `phone_verified=true`

**Admin Override:** If `verification_code` not provided, requires `idp:users:phone:verify` permission.

**Response:** `VerifyUserPhoneResponse { User user = 1; }`

**Events Published:** `UserUpdated` (updated_fields includes "phone_verified")

**Error Codes:**

- `NOT_FOUND` - User does not exist
- `INVALID_ARGUMENT` - Code expired or incorrect
- `PERMISSION_DENIED` - Missing permission (if code not provided)

## Validation

All requests validated using `buf/validate` annotations. Validation errors return `INVALID_ARGUMENT` with detailed field errors in status details.

**Example Validation Error:**

```json
{
  "code": "INVALID_ARGUMENT",
  "message": "Validation failed",
  "details": [
    {
      "field": "email",
      "constraint": "email",
      "message": "must be a valid email address"
    }
  ]
}
```

## Compliance

- **SOC 2 CC6.1:** User provisioning audit trail via events
- **GDPR Article 15:** GetUser supports right of access
- **GDPR Article 16:** UpdateUser supports right to rectification
- **GDPR Article 17:** DeleteUser supports right to erasure (hard_delete=true)
- **GDPR Article 30:** All operations logged for record of processing
- **ISO 27001 A.9.2:** Permission-based access control

## Security

**Tenant Isolation:** `tenant_id` validated on every operation. Cross-tenant access blocked.

**PII Encryption:** Email, phone_number encrypted at rest. TLS required in transit.

**Audit Logging:** All mutations logged with actor, timestamp, changes made.

**Session Management:** Status changes (SUSPENDED, LOCKED, DELETED) invalidate active sessions.

## Code Generation

Generate gRPC clients:

```bash
buf generate --path proto/idp/identity/user/api/v1
```

**Outputs:**

- Go: `gen/go/idp/identity/user/api/v1/userapiv1/`
- Python: `gen/python/idp/identity/user/api/v1/`
- Java: `gen/java/idp/identity/user/api/v1/`
- TypeScript: `gen/typescript/idp/identity/user/api/v1/`
- C#: `gen/csharp/Idp/Identity/User/Api/V1/`

## Client Examples

### Go Client

```go
import userapiv1 "github.com/geniustechspace/protobuf/gen/go/idp/identity/user/api/v1"

client := userapiv1.NewUserServiceClient(conn)
ctx := metadata.AppendToOutgoingContext(context.Background(), "authorization", "Bearer "+token)

resp, err := client.CreateUser(ctx, &userapiv1.CreateUserRequest{
    TenantId: "tnt_abc123",
    Email: "john@example.com",
    DisplayName: "John Doe",
})
```

### Python Client

```python
from idp.identity.user.api.v1 import api_pb2, api_pb2_grpc

channel = grpc.secure_channel('idp-api.example.com:443', creds)
client = api_pb2_grpc.UserServiceStub(channel)

metadata = [('authorization', f'Bearer {token}')]
response = client.CreateUser(
    api_pb2.CreateUserRequest(
        tenant_id='tnt_abc123',
        email='john@example.com',
        display_name='John Doe'
    ),
    metadata=metadata
)
```

## Related Documentation

- **Domain Model:** `../v1/README.md` - User entity definition
- **Domain Events:** `../events/v1/README.md` - Events published by this API
- **Core Pagination:** `../../../../core/v1/` - PaginationRequest/Response types
