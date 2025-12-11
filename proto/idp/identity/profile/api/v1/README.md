# Profile API Layer

**Package:** `geniustechspace.idp.identity.profile.api.v1`

## Overview

gRPC service for profile lifecycle management. Provides CRUD operations and domain-specific actions.

## Service: ProfileService

### Authentication

All RPCs require Bearer token authentication.

### Authorization

Permission-based access control:
- `idp:profiles:create` - Create new profile
- `idp:profiles:read` - Read profile details
- `idp:profiles:update` - Modify profile
- `idp:profiles:delete` - Delete profile
- `idp:profiles:list` - List profiles

### Rate Limits

- Standard operations: 100/min per tenant
- Write operations: 50/min per tenant

## Operations

### CreateProfile

Create new profile entity.

**Request:** `CreateProfileRequest`  
**Response:** `CreateProfileResponse`  
**Events:** Publishes `ProfileCreated`

### GetProfile

Retrieve profile by ID.

**Request:** `GetProfileRequest { tenant_id, profile_id }`  
**Response:** `GetProfileResponse { profile }`

### UpdateProfile

Modify existing profile.

**Request:** `UpdateProfileRequest` (partial update)  
**Response:** `UpdateProfileResponse`  
**Events:** Publishes `ProfileUpdated`

### DeleteProfile

Soft-delete or hard-delete profile.

**Request:** `DeleteProfileRequest { hard_delete }`  
**Response:** `DeleteProfileResponse`  
**Events:** Publishes `ProfileDeleted`

### ListProfiles

Paginated list with optional filters.

**Request:** `ListProfilesRequest { pagination, filters }`  
**Response:** `ListProfilesResponse { profiles, pagination }`

## Validation

All requests validated using `buf/validate`. Validation errors return `INVALID_ARGUMENT`.

## Compliance

- **SOC 2 CC6.1:** Access control and audit trails
- **ISO 27001 A.9.2:** User access management

## Code Generation

```bash
buf generate --path proto/idp/identity/profile/api/v1
```

## Related Documentation

- **Domain Model:** `../v1/README.md`
- **Domain Events:** `../events/v1/README.md`
