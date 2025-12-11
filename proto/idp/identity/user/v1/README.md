# User Domain Model

**Package:** `geniustechspace.idp.identity.user.v1`

## Overview

Core user domain entity for identity and access management. Defines the canonical `User` aggregate root with authentication and authorization concerns.

## Architecture

**Domain-Driven Design:** User is a lean aggregate root focused on identity, authentication, and account lifecycle. Personal/demographic data resides in the Profile subdomain for clean separation of concerns.

**Bounded Context:** Identity management core - authentication state, account status, and multi-tenant isolation.

## Entities

### User

Aggregate root representing a user account.

**Identity:**

- `user_id` (UUID) - Immutable identifier
- `tenant_id` (UUID) - Multi-tenant isolation
- `username` - Optional unique handle
- `email` - Required, unique when verified
- `phone_number` - Optional E.164 format

**Verification:**

- `email_verified_at` - NULL = not verified
- `phone_verified_at` - NULL = not verified

**Account State:**

- `status` - UserStatus enum (lifecycle management)
- `locked_until` - Temporary lock expiry

**Federation:**

- `external_id` - External IDP user ID
- `external_provider` - External IDP name

**Activity Tracking:**

- `last_login_at` - Last successful authentication
- `last_activity_at` - Last action timestamp
- `password_changed_at` - For password expiration policies

**Performance Cache:**

- `display_name` - Cached from Profile for quick access

**Metadata:**

- `tags` - Custom classification

**Audit Fields:**

- `created_at`, `updated_at`, `deleted_at`, `version`

**PII Compliance:** Email, phone, names are personal identifiers per GDPR Article 4(1). Encryption required at rest.

## Enumerations

### UserStatus

User account lifecycle states (8 values):

- `USER_STATUS_UNSPECIFIED` (0) - Invalid default
- `ACTIVE` (1) - Normal operational state
- `INACTIVE` (2) - User-disabled, can reactivate
- `SUSPENDED` (3) - Admin-disabled
- `LOCKED` (4) - Security lockout
- `DELETED` (5) - Soft-deleted
- `PENDING_VERIFICATION` (6) - Awaiting email/phone verification
- `PENDING_APPROVAL` (7) - Awaiting admin approval
- `EXPIRED` (8) - Account expired per policy

**State Transitions:** See inline documentation in `user.proto`.

## Validation Rules

All fields use `buf/validate` annotations:

- **user_id, tenant_id:** UUID format required
- **username:** 3-64 chars, alphanumeric with underscore/dash
- **email:** RFC 5322 format
- **phone_number:** E.164 format recommended
- **status:** Enum values only (defined_only)
- **created_at:** Required
- **version:** ≥ 1

## Usage

### Importing

```protobuf
import "idp/identity/user/v1/user.proto";

message MyMessage {
  geniustechspace.idp.identity.user.v1.User user = 1;
  geniustechspace.idp.identity.user.v1.UserStatus status = 2;
}
```

### Code Generation

```bash
buf generate --path proto/idp/identity/user/v1
```

Generates clients in: `gen/{go,python,java,typescript,csharp}/idp/identity/user/v1/`

## Relationships

- **Profile:** 1:1 with `identity.profile.v1.UserProfile` (personal data)
- **Organizations:** N:M via `identity.organization.v1` (membership)
- **Groups:** N:M via `identity.group.v1` (membership)
- **Credentials:** 1:N with `authn.credential.v1.Credential`
- **Sessions:** 1:N with `authn.session.v1.Session`
- **Roles:** N:M via `authz.role.v1.RoleAssignment`

## Compliance

- **SOC 2 CC6.1:** User provisioning and lifecycle management
- **SOC 2 CC6.3:** Audit trail (created_at, updated_at, deleted_at, version)
- **GDPR Article 4(1):** PII fields (email, phone_number) - encryption required
- **GDPR Article 17:** Right to erasure (soft delete via deleted_at)
- **GDPR Article 30:** Audit trail maintenance
- **ISO 27001 A.9.2:** User access management
- **GDPR Article 17:** Right to erasure (hard delete support)
- **ISO 27001 A.9.2:** User access management
- **NIST 800-63B:** Digital identity guidelines

## Security

- **Tenant Isolation:** `tenant_id` field MUST be validated on all operations
- **Encryption at Rest:** Email, phone_number require encryption
- **PII Handling:** All personal data fields require GDPR compliance
- **Audit Logging:** All mutations logged via `core.v1.Metadata`

## Events

User entity changes publish domain events (see `../events/v1/`):

- `UserCreated` - New user provisioned
- `UserUpdated` - Profile or membership changed
- `UserDeleted` - Soft or hard delete performed
- `UserStatusChanged` - Status transition occurred

## API

gRPC service operations available at `../api/v1/`:

- `CreateUser`, `GetUser`, `UpdateUser`, `DeleteUser`
- `ListUsers`, `SearchUsers`
- `UpdateUserStatus`, `VerifyUserEmail`, `VerifyUserPhone`

See `../api/v1/README.md` for detailed API documentation.

## Breaking Changes

⚠️ **v1 API is stable.** Do not:

- Remove fields or enum values
- Renumber fields
- Change field types
- Rename package

For breaking changes, create `v2` package.

## Deprecation

Use `reserved` for removed fields:

```protobuf
message User {
  reserved 99;  // old_field_name removed in v1.5
  reserved "old_field_name";
}
```

Mark deprecated fields:

```protobuf
string legacy_field = 100 [deprecated = true];
```
