# IDP Identity Management

Comprehensive identity management for users, groups, organizations, and profiles.

## Package

```protobuf
package geniustechspace.idp.identity.v1;
```

## Overview

The identity module provides complete identity lifecycle management with:

- **User Management** - User accounts, status, credentials, organizations
- **Profile Management** - User profiles with personal data, social profiles, custom attributes
- **Group Management** - Groups for organizing users, role assignment, hierarchical groups
- **Organization Management** - Organizations with hierarchy, branding, domain verification
- **Verification** - Email and phone verification workflows
- **Search** - Cross-entity search across users, groups, organizations

## Module Structure

```text
proto/idp/identity/v1/
├── service.proto          # IdentityService (main service)
├── identity.proto         # Core identity operations (verification, search)
├── user.proto             # User entity and CRUD operations
├── profile.proto          # User profile management
├── group.proto            # Group entity and member management
├── organization.proto     # Organization entity and hierarchy
└── README.md              # This file
```

## Files

### service.proto

Main gRPC service with 25 operations:

- User CRUD (5): Create, Get, Update, Delete, List
- Profile (2): Get, Update
- Verification (4): Email verify/confirm, Phone verify/confirm
- Group CRUD (7): Create, Get, Update, Delete, List, Add/Remove members
- Organization CRUD (5): Create, Get, Update, Delete, List
- Search (1): Universal identity search

### user.proto

User account entity:

- `User` message - Complete user account with status, MFA, organizations, groups
- `UserStatus` enum - ACTIVE, INACTIVE, SUSPENDED, LOCKED, DELETED, PENDING_VERIFICATION, PENDING_APPROVAL, EXPIRED
- CRUD operations with tenant isolation

### profile.proto

Extended user profile:

- `UserProfile` message - Personal data, social profiles, custom attributes
- `PhoneNumber`, `SocialProfile` - Structured contact information
- Profile operations (get, update)

### group.proto

Group management:

- `Group` message - Group with members, roles, hierarchical parent
- `GroupType` enum - SYSTEM, CUSTOM, DEPARTMENT, TEAM, PROJECT, ROLE_BASED
- Group CRUD + member management

### organization.proto

Organization structure:

- `Organization` message - Organization with hierarchy, domains, branding
- `OrganizationType` enum - ENTERPRISE, SMB, STARTUP, NON_PROFIT, GOVERNMENT, EDUCATIONAL, PERSONAL
- `OrganizationSize` enum - INDIVIDUAL, SMALL, MEDIUM, LARGE, ENTERPRISE, VERY_LARGE
- `OrganizationBranding` - Logo, colors for visual identity

### identity.proto

Core identity operations:

- Email/phone verification workflows
- Universal search across users, groups, organizations
- `IdentityType` enum - USER, GROUP, ORGANIZATION

## Usage Examples

### Create User

```protobuf
import "idp/identity/v1/service.proto";

CreateUserRequest request = {
  tenant_id: "tenant_123",
  username: "jsmith",
  email: "jsmith@example.com",
  phone_number: "+14155551234",
  password: "secure_password",
  organization_ids: ["org_456"],
  group_ids: ["group_789"],
  send_verification_email: true
};

CreateUserResponse response = identity_service.CreateUser(request);
```

### Update User Profile

```protobuf
UpdateUserProfileRequest request = {
  tenant_id: "tenant_123",
  user_id: "user_123",
  given_name: "John",
  family_name: "Smith",
  display_name: "John Smith",
  picture_url: "https://example.com/avatar.jpg",
  locale: "en-US",
  timezone: "America/New_York",
  company: "Example Corp",
  job_title: "Software Engineer"
};

UpdateUserProfileResponse response = identity_service.UpdateUserProfile(request);
```

### Create Group

```protobuf
CreateGroupRequest request = {
  tenant_id: "tenant_123",
  name: "engineering",
  display_name: "Engineering Team",
  description: "Software engineering team",
  type: TEAM,
  organization_id: "org_456",
  member_user_ids: ["user_123", "user_456"],
  role_ids: ["role_developer"]
};

CreateGroupResponse response = identity_service.CreateGroup(request);
```

### Create Organization

```protobuf
CreateOrganizationRequest request = {
  tenant_id: "tenant_123",
  name: "acme-corp",
  display_name: "Acme Corporation",
  description: "Leading provider of widgets",
  domain: "acme.com",
  type: ENTERPRISE,
  size: LARGE,
  website: "https://acme.com",
  industry: "Technology",
  branding: {
    logo_url: "https://acme.com/logo.png",
    primary_color: "#FF5733",
    secondary_color: "#3498DB"
  }
};

CreateOrganizationResponse response = identity_service.CreateOrganization(request);
```

### Email Verification Flow

```protobuf
// Step 1: Initiate verification
VerifyEmailRequest request = {
  tenant_id: "tenant_123",
  user_id: "user_456",
  email: "user@example.com"
};
VerifyEmailResponse response = identity_service.VerifyEmail(request);

// Step 2: User clicks link in email
ConfirmEmailVerificationRequest confirm = {
  tenant_id: "tenant_123",
  user_id: "user_456",
  token: "token_from_email_link"
};
ConfirmEmailVerificationResponse confirmed = identity_service.ConfirmEmailVerification(confirm);
```

### Universal Search

```protobuf
SearchIdentitiesRequest request = {
  tenant_id: "tenant_123",
  query: "john",
  types: [USER, GROUP],
  page_size: 20
};

SearchIdentitiesResponse response = identity_service.SearchIdentities(request);
// Returns users and groups matching "john"
```

## Key Features

### Multi-Tenant Architecture

All entities enforce strict tenant isolation:

```protobuf
message User {
  string id = 1;
  string tenant_id = 2; // ALWAYS required
  // ...
}
```

### Hierarchical Structures

Both groups and organizations support hierarchy:

```protobuf
// Parent-child group relationships
Group engineering = {
  parent_group_id: "group_technology" // Optional parent
};

// Parent-child organization relationships
Organization subsidiary = {
  parent_organization_id: "org_parent_company"
};
```

### Flexible Status Management

Users have granular status tracking:

- `ACTIVE` - Normal operation
- `INACTIVE` - Temporarily inactive
- `SUSPENDED` - Admin-suspended
- `LOCKED` - Security-locked
- `DELETED` - Soft deleted
- `PENDING_VERIFICATION` - Awaiting email/phone verification
- `PENDING_APPROVAL` - Awaiting admin approval
- `EXPIRED` - Account expired

### Federated Identity

Support for external identity providers:

```protobuf
User user = {
  external_id: "google_123456789",
  external_provider: "google",
  email: "user@example.com"
};
```

## Privacy & Compliance

### PII Fields

Extensive PII documentation on all fields:

```protobuf
// Email. REQUIRED.
// PII: Yes - GDPR Article 4(1) personal identifier
// ENCRYPTION: Required at rest
// VALIDATION: RFC 5322 email format
string email = 4 [(buf.validate.field).string.email = true];
```

### GDPR Compliance

- **Article 5**: Data minimization applied throughout
- **Article 17**: Right to erasure via `hard_delete` flag
- **Article 25**: Privacy by design with encryption at rest
- **Article 30**: Records of processing documented

### Data Protection

- Passwords: Never stored in identity messages, only in auth system
- Encryption: All PII fields require encryption at rest
- Validation: buf/validate annotations enforce data quality
- Soft delete: Default behavior preserves audit trail

## Import Paths

```protobuf
import "idp/identity/v1/service.proto";
import "idp/identity/v1/identity.proto";
import "idp/identity/v1/user.proto";
import "idp/identity/v1/profile.proto";
import "idp/identity/v1/group.proto";
import "idp/identity/v1/organization.proto";
```

## See Also

- [IDP Authentication](../authn/README.md) - User authentication
- [IDP Authorization](../authz/README.md) - Role-based access control
- [IDP Audit](../audit/README.md) - Audit logging
- [Main IDP README](../README.md)
