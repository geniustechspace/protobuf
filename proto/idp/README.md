# Identity Provider (IDP) - Domain-First Architecture

**Enterprise-grade identity provider with Domain-Driven Design (DDD) and Event-Driven Architecture (EDA)**

## Architecture Overview

The IDP follows a **domain-first, three-layer architecture** with strict separation of concerns:

1. **Domain Layer** (`{domain}/{subdomain}/v1/`) - Pure domain models, entities, enums
2. **Events Layer** (`{domain}/{subdomain}/events/v1/`) - Domain events for state changes
3. **API Layer** (`{domain}/{subdomain}/api/v1/`) - gRPC services, requests/responses

Each subdomain is self-contained with all three layers co-located, enabling independent evolution and microservice extraction.

## Package Naming Convention

```protobuf
// Domain entities and enums
package geniustechspace.idp.identity.user.v1;

// Domain events
package geniustechspace.idp.identity.user.events.v1;

// gRPC API services
package geniustechspace.idp.identity.user.api.v1;
```

**Pattern:** `geniustechspace.idp.{domain}.{subdomain}.{layer}.v1`

## Bounded Contexts

### 1. Identity Domain

**Subdomains:** user, group, organization, profile  
**Concerns:** User lifecycle, profiles, group membership, org hierarchy  
**Events:** UserCreated, GroupUpdated, OrganizationDeleted

### 2. Authentication Domain (authn)

**Subdomains:** credential, session, mfa  
**Concerns:** Multi-method auth, MFA enrollment, session management  
**Events:** CredentialCreated, SessionStarted, MfaVerified

### 3. Authorization Domain (authz)

**Subdomains:** permission, role, policy  
**Concerns:** RBAC, ABAC, permissions, access control policies  
**Events:** RoleAssigned, PermissionGranted, PolicyEvaluated

### 4. Supporting Modules

**Modules:** audit, connectors, protocols, provisioning, webhook  
**Concerns:** Audit logging, identity federation, OAuth2/OIDC, SCIM, webhooks

## Directory Structure

```text
proto/idp/
├── README.md                                    # This file
│
├── identity/                                    # Identity bounded context
│   ├── user/
│   │   ├── v1/
│   │   │   ├── user.proto                      # User entity + UserStatus enum
│   │   │   └── README.md                       # Domain model documentation
│   │   ├── events/v1/
│   │   │   ├── events.proto                    # UserCreated, UserUpdated, etc.
│   │   │   └── README.md                       # Event documentation
│   │   └── api/v1/
│   │       ├── api.proto                       # UserService gRPC operations
│   │       └── README.md                       # API documentation
│   ├── group/                                   # Same 3-layer structure
│   │   ├── v1/                                 # Group entity
│   │   ├── events/v1/                          # Group events
│   │   └── api/v1/                             # GroupService API
│   ├── organization/                            # Same 3-layer structure
│   │   ├── v1/                                 # Organization entity
│   │   ├── events/v1/                          # Organization events
│   │   └── api/v1/                             # OrganizationService API
│   └── profile/                                 # Same 3-layer structure
│       ├── v1/                                 # Profile entity (PII)
│       ├── events/v1/                          # Profile events
│       └── api/v1/                             # ProfileService API
│
├── authn/                                       # Authentication bounded context
│   ├── credential/
│   │   ├── v1/                                 # Credential entity + types
│   │   ├── events/v1/                          # CredentialCreated, etc.
│   │   └── api/v1/                             # CredentialService API
│   ├── session/
│   │   ├── v1/                                 # Session entity + status
│   │   ├── events/v1/                          # SessionStarted, etc.
│   │   └── api/v1/                             # SessionService API
│   └── mfa/
│       ├── v1/                                 # MFA entity + types
│       ├── events/v1/                          # MfaEnrolled, etc.
│       └── api/v1/                             # MfaService API
│
├── authz/                                       # Authorization bounded context
│   ├── permission/
│   │   ├── v1/                                 # Permission entity
│   │   ├── events/v1/                          # PermissionGranted, etc.
│   │   └── api/v1/                             # PermissionService API
│   ├── role/
│   │   ├── v1/                                 # Role entity + assignments
│   │   ├── events/v1/                          # RoleAssigned, etc.
│   │   └── api/v1/                             # RoleService API
│   └── policy/
│       ├── v1/                                 # Policy entity + ABAC rules
│       ├── events/v1/                          # PolicyEvaluated, etc.
│       └── api/v1/                             # PolicyService API
│
└── [audit, connectors, protocols, provisioning, webhook]/
    ├── v1/                                     # Supporting module entities
    ├── events/v1/                              # Module events
    └── api/v1/                                 # Module APIs (to be added)
```

## Three-Layer Architecture

### Layer 1: Domain Model (`v1/`)

**Purpose:** Pure domain entities, enums, and business logic

**Contains:**

- Entity definitions (User, Group, Credential, etc.)
- Domain enums (UserStatus, CredentialType, etc.)
- Business invariants and constraints
- Metadata and audit fields

**Does NOT contain:**

- RPC service definitions
- Request/response messages
- API-specific validation
- Transport concerns

**Example:** `identity/user/v1/user.proto`

```protobuf
package geniustechspace.idp.identity.user.v1;

message User {
  string id = 1;
  string tenant_id = 2;
  string email = 3;
  UserStatus status = 4;
  // ... domain fields
}

enum UserStatus {
  USER_STATUS_UNSPECIFIED = 0;
  ACTIVE = 1;
  INACTIVE = 2;
  // ...
}
```

### Layer 2: Domain Events (`events/v1/`)

**Purpose:** State change notifications for event-driven architecture

**Contains:**

- Event messages for entity lifecycle (Created, Updated, Deleted)
- Status change events (StatusChanged)
- Domain-specific events (EmailVerified, MfaEnrolled)
- Event metadata (event_id, timestamp, correlation_id)

**Pattern:** Events reference domain types via imports

**Example:** `identity/user/events/v1/events.proto`

```protobuf
package geniustechspace.idp.identity.user.events.v1;

import "idp/identity/user/v1/user.proto";
import "core/v1/common.proto";

message UserCreated {
  core.v1.Metadata metadata = 1;
  string tenant_id = 2;
  string user_id = 3;
  string email = 4;
  string created_by = 5;
}
```

### Layer 3: API Services (`api/v1/`)

**Purpose:** gRPC service contracts for external consumption

**Contains:**

- Service definitions (UserService, CredentialService, etc.)
- Request messages (CreateUserRequest, ValidateCredentialRequest)
- Response messages (GetUserResponse, ListRolesResponse)
- Validation annotations (buf.validate)
- Rate limiting documentation
- Authentication/authorization requirements

**Pattern:** API imports domain types, never the reverse

**Example:** `identity/user/api/v1/api.proto`

```protobuf
package geniustechspace.idp.identity.user.api.v1;

import "idp/identity/user/v1/user.proto";
import "core/v1/common.proto";

service UserService {
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
  // ...
}

message GetUserRequest {
  string tenant_id = 1;
  string user_id = 2;
}

message GetUserResponse {
  geniustechspace.idp.identity.user.v1.User user = 1;
}
```

## Dependency Flow

```text
API Layer (api/v1)
   ↓ imports
Domain Layer (v1) ← imports ← Events Layer (events/v1)
```

**Rules:**

- API can import domain types
- Events can import domain types
- Domain NEVER imports API or events
- Cross-domain imports allowed for relationships (e.g., policy imports role.SubjectType)

## Benefits of Domain-First Architecture

1. **Co-location:** All subdomain concerns in one directory tree
2. **Independent Evolution:** Change user API without affecting group domain
3. **Microservice Ready:** Extract `identity/user/` as standalone service
4. **Clear Boundaries:** Three layers enforce separation of concerns
5. **Event-Driven:** Events are first-class citizens, not afterthoughts
6. **Testing:** Domain models testable without gRPC infrastructure
7. **Documentation:** README at every layer explains purpose and usage

## API Services

### IdentityService (24 RPCs)

```protobuf
service IdentityService {
  // User Management: CreateUser, GetUser, UpdateUser, DeleteUser, ListUsers
  // Profile: GetUserProfile, UpdateUserProfile
  // Verification: VerifyEmail, ConfirmEmailVerification, VerifyPhone, ConfirmPhoneVerification
  // Groups: CreateGroup, GetGroup, UpdateGroup, DeleteGroup, AddGroupMember, RemoveGroupMember, ListGroups
  // Organizations: CreateOrganization, GetOrganization, UpdateOrganization, DeleteOrganization, ListOrganizations
  // Search: SearchIdentities
}
```

### AuthenticationService (10 RPCs)

```protobuf
service AuthenticationService {
  // Authentication: Authenticate, VerifyMfa
  // Sessions: RefreshToken, ValidateToken, Logout, ListSessions, RevokeSession
  // Passwords: ChangePassword, ResetPassword, ConfirmPasswordReset
}
```

### AuthorizationService (17 RPCs)

```protobuf
service AuthorizationService {
  // Checks: CheckPermission, BatchCheckPermissions
  // Roles: CreateRole, GetRole, UpdateRole, DeleteRole, ListRoles
  // Assignments: AssignRole, RevokeRole, ListRoleAssignments
  // Policies: CreatePolicy, GetPolicy, UpdatePolicy, DeletePolicy, ListPolicies
  // Queries: ListPermissions, GetUserPermissions
}
```

## Domain Models

### Identity Context

**User Aggregate:**

- 24 fields: id, tenant_id, username, email, phone, status, mfa_enabled, etc.
- 8 status states: ACTIVE, INACTIVE, SUSPENDED, LOCKED, DELETED, PENDING_VERIFICATION, PENDING_APPROVAL, EXPIRED
- Invariants: Username unique per tenant, email unique when verified

**Group Aggregate:**

- Hierarchical structure with parent_id
- 6 types: SYSTEM, CUSTOM, DEPARTMENT, TEAM, PROJECT, ROLE_BASED
- Max hierarchy depth: 10 levels

**Organization Aggregate:**

- Hierarchical structure with parent_id
- 7 types, 6 sizes, 5 statuses
- Domain ownership (email domain auto-join)
- Branding configuration (logo, colors, CSS)

### Authentication Context

**Credential Aggregate:**

- 6 types: PASSWORD, WEBAUTHN, TOTP, API_KEY, CERTIFICATE, RECOVERY_CODE
- Oneof credential_data for type-specific fields
- Password always hashed (bcrypt/argon2id)
- WebAuthn FIDO2 certified

**Session Aggregate:**

- Access/refresh token hashes (never plaintext)
- Session context: IP, user agent, device, geolocation, risk score
- Idle/absolute timeouts
- Token rotation on refresh

**MFA Value Objects:**

- MfaEnrollment: TOTP, SMS, Email, WebAuthn
- MfaChallenge: Challenge ID, expiry, attempts
- 7 methods: TOTP, SMS, EMAIL, WEBAUTHN, VOICE, PUSH, BACKUP_CODES

### Authorization Context

**Role Aggregate:**

- Permission collection with inheritance
- Parent roles for hierarchy (max depth: 5)
- 4 types: SYSTEM, CUSTOM, ORGANIZATION, APPLICATION
- System roles immutable

**Policy Aggregate:**

- ABAC/PBAC with conditions
- Allow/Deny effect (explicit deny always wins)
- Priority-based evaluation (1-1000)
- PolicyCondition: 12 operators (equals, in, contains, regex, etc.)

**Permission Value Object:**

- Format: `resource:action` (e.g., `users:read`)
- 4 scopes: GLOBAL, TENANT, ORGANIZATION, PERSONAL
- Immutable

## Domain Events (EDA)

### Identity Events

```protobuf
UserCreated, UserUpdated, UserDeleted, UserStatusChanged
EmailVerified, PhoneVerified, UserLocked, UserUnlocked
GroupCreated, GroupUpdated, GroupDeleted
UserAddedToGroup, UserRemovedFromGroup
OrganizationCreated, OrganizationUpdated, OrganizationDeleted, OrganizationStatusChanged
```

### Authentication Events

```protobuf
AuthenticationAttempted, AuthenticationSucceeded, AuthenticationFailed
SessionCreated, SessionRefreshed, SessionExpired, SessionRevoked
CredentialCreated, CredentialUpdated, CredentialRevoked, PasswordChanged
MfaEnrolled, MfaVerified, MfaRevoked, MfaChallengeCreated, MfaChallengeFailed
```

### Authorization Events

```protobuf
PermissionChecked, AccessDenied
RoleCreated, RoleUpdated, RoleDeleted, RoleAssigned, RoleRevoked
PolicyCreated, PolicyUpdated, PolicyDeleted, PolicyActivated, PolicyDeactivated
```

**Event Metadata:**
Every event includes: event_id, event_type, aggregate_id, aggregate_type, event_time, event_version, causation_id, correlation_id, actor_id, tenant_id, source

````

## Standards Compliance

### Authentication Standards

- ✅ **OAuth 2.0** (RFC 6749) - Authorization Framework
- ✅ **OpenID Connect 1.0** - Identity Layer
- ✅ **SAML 2.0** - Security Assertion Markup Language
- ✅ **WebAuthn Level 2** - W3C Web Authentication
- ✅ **FIDO2 CTAP2** - Client to Authenticator Protocol
- ✅ **RFC 6238** - TOTP Time-Based One-Time Password
- ✅ **RFC 7519** - JSON Web Token (JWT)
- ✅ **RFC 7662** - Token Introspection
- ✅ **RFC 7009** - Token Revocation

### Security Standards

- ✅ **NIST 800-63B** - Digital Identity Authentication
- ✅ **NIST 800-63C** - Federation and Assertions
- ✅ **OWASP Top 10** - Web Application Security
- ✅ **OWASP ASVS** - Application Security Verification
- ✅ **PCI DSS 4.0** - Payment Card Industry Security
- ✅ **ISO 27001** - Information Security Management

### Privacy & Compliance

- ✅ **GDPR** - General Data Protection Regulation
- ✅ **CCPA** - California Consumer Privacy Act
- ✅ **HIPAA** - Health Insurance Portability
- ✅ **SOC 2 Type II** - Service Organization Controls
- ✅ **PSD2 SCA** - Strong Customer Authentication

### Provisioning Standards

- ✅ **SCIM 2.0** (RFC 7643, 7644) - System for Cross-domain Identity Management
- ✅ **LDAP v3** (RFC 4510) - Lightweight Directory Access Protocol

## Key Features

### Multi-Tenant Architecture

All IDP modules enforce tenant isolation:

```protobuf
message AuthenticateRequest {
  string tenant_id = 1 [(buf.validate.field).string.min_len = 1];
  // ... other fields
}
````

### Comprehensive Authentication Methods

- Password-based
- Passwordless (magic link, email code, SMS)
- WebAuthn/FIDO2 (platform and cross-platform)
- Biometric (fingerprint, face, iris)
- Social login (Google, GitHub, Microsoft, etc.)
- Enterprise (SAML, LDAP, OAuth)
- Certificate-based
- Multi-factor authentication (7 types)

### Flexible Authorization

- Role-Based Access Control (RBAC)
- Attribute-Based Access Control (ABAC)
- Policy-based authorization
- Fine-grained permissions
- Resource-level access control
- Hierarchical roles

### Identity Verification

- Email verification
- Phone verification
- Document verification
- Biometric verification
- KYC (Know Your Customer)
- AML (Anti-Money Laundering)

### Audit & Compliance

- Immutable audit logs
- Tamper detection
- Digital signatures
- Event correlation
- Retention policies
- Compliance reporting

## Usage Examples

### Authentication Flow

```protobuf
import "idp/authn/v1/service.proto";
import "idp/authn/v1/messages.proto";

// 1. Authenticate with password
AuthenticateRequest request = {
  tenant_id: "tenant_123",
  email: "user@example.com",
  password: "secure_password",
  device_context: { ... },
  client_context: { ... }
};

AuthenticateResponse response = authn_service.Authenticate(request);

// 2. Verify MFA if required
if (response.status == MFA_REQUIRED) {
  VerifyMFARequest mfa_request = {
    tenant_id: "tenant_123",
    session_id: response.session_id,
    code: "123456"
  };
  VerifyMFAResponse mfa_response = authn_service.VerifyMFA(mfa_request);
}
```

### Authorization Check

```protobuf
import "idp/authz/v1/service.proto";

CheckPermissionRequest request = {
  tenant_id: "tenant_123",
  user_id: "user_456",
  resource: "documents:doc_789",
  action: "read"
};

CheckPermissionResponse response = authz_service.CheckPermission(request);
if (response.allowed) {
  // Grant access
}
```

### User Provisioning (SCIM)

```protobuf
import "idp/provisioning/v1/service.proto";

CreateUserRequest request = {
  tenant_id: "tenant_123",
  user: {
    user_name: "jsmith",
    name: {
      given_name: "John",
      family_name: "Smith"
    },
    emails: [{
      value: "jsmith@example.com",
      primary: true
    }]
  }
};

CreateUserResponse response = provisioning_service.CreateUser(request);
```

## Security Best Practices

### Transport Security

- TLS 1.3+ required for all communications
- Certificate pinning for mobile apps
- HSTS headers

### Data Protection

- Passwords: bcrypt/argon2id, NEVER logged
- Tokens: Short-lived, signed (RS256)
- PII: Encrypted at rest, labeled in docs
- Audit logs: Tamper-resistant, encrypted

### Operational Security

- Rate limiting on all endpoints
- Account lockout after failed attempts
- Anomaly detection (new device, location)
- Security event alerting
- Incident response procedures

## Privacy Considerations

### PII Fields

All PII fields are documented with:

```protobuf
// Email address. REQUIRED.
// PII: Yes - GDPR Article 4(1) personal identifier
// ENCRYPTION: Required at rest
// VALIDATION: RFC 5322 email format
string email = 3 [(buf.validate.field).string.email = true];
```

### Data Minimization

- Collect only necessary data
- Use least privilege access
- Short retention periods
- Anonymization when possible

### User Rights (GDPR)

- Right to access (Article 15)
- Right to rectification (Article 16)
- Right to erasure (Article 17)
- Right to data portability (Article 20)

## Import Paths

All IDP modules use module-relative import paths:

```protobuf
import "idp/authn/v1/messages.proto";
import "idp/authz/v1/rbac.proto";
import "idp/identity/v1/user.proto";
import "idp/audit/v1/messages.proto";
import "idp/api/v1/common.proto";
```

## Code Generation

Generate IDP clients:

```bash
# All languages
buf generate --path proto/idp/

# Specific module
buf generate --path proto/idp/authn/

# Go
go get github.com/geniustechspace/protobuf/gen/go/idp/authn/v1

# Python
pip install geniustechspace-protobuf-idp-authn

# Java
<dependency>
  <groupId>com.geniustechspace.protobuf</groupId>
  <artifactId>idp-authn-v1</artifactId>
</dependency>
```

## Related Modules

- [Core](../core/README.md) - Common value objects (session, device, network)
- [Users](../users/README.md) - User account management
- [Tenants](../tenants/README.md) - Multi-tenancy

## Documentation

- [Enterprise Compliance](../../docs/ENTERPRISE_COMPLIANCE.md)
- [Validation Standards](../../docs/VALIDATION.md)
- [Proto Documentation Standard](../../docs/PROTO_DOCUMENTATION_STANDARD.md)
