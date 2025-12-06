# Comprehensive Project Structure

**Genius Tech Space - Protocol Buffer Schema Repository**

Version: 1.0.0  
Last Updated: December 6, 2025  
Repository: https://github.com/geniustechspace/protobuf

---

## Table of Contents

1. [Overview](#overview)
2. [Directory Structure](#directory-structure)
3. [Domain Architecture](#domain-architecture)
4. [File Organization](#file-organization)
5. [Service Catalog](#service-catalog)
6. [Event Catalog](#event-catalog)
7. [Data Structure Layer](#data-structure-layer)
8. [Configuration Files](#configuration-files)
9. [Documentation](#documentation)
10. [Code Generation](#code-generation)
11. [Dependencies](#dependencies)
12. [Technology Stack](#technology-stack)

---

## Overview

### Purpose

Enterprise-grade Protocol Buffer schema repository providing:
- Domain-driven design with clear separation of concerns
- Multi-tenant support across all domains
- Event-driven architecture patterns
- gRPC service definitions
- Multi-language client generation
- Comprehensive validation and documentation

### Key Characteristics

- **Architecture**: Domain-Driven Design (DDD)
- **Tenancy**: Multi-tenant with isolation at protocol level
- **Versioning**: Semantic versioning with v1/v2 support
- **Pattern**: Event-driven with domain events
- **API Style**: gRPC with Protocol Buffers
- **Languages**: Go, Python, Java, TypeScript, C#
- **Standards**: Enterprise compliance (SOC 2, GDPR, ISO 27001, PCI DSS)

---

## Directory Structure

```
protobuf/
│
├── proto/                           # Protocol Buffer definitions
│   ├── core/                        # Foundation types
│   │   └── v1/
│   │       ├── metadata.proto       # Common metadata patterns
│   │       ├── types.proto          # Shared value objects
│   │       └── events.proto         # Base event structure
│   │
│   ├── datastructure/               # Context data structures (NEW)
│   │   ├── ARCHITECTURE.md          # Context composition architecture
│   │   ├── README.md                # Usage guide
│   │   └── v1/
│   │       ├── circuit_breaker/     # Circuit breaker patterns
│   │       │   ├── enums.proto
│   │       │   ├── messages.proto
│   │       │   └── README.md
│   │       ├── client/              # Client/application context
│   │       │   ├── enums.proto
│   │       │   └── messages.proto
│   │       ├── credentials/         # Credential structures
│   │       ├── device/              # Device hardware context
│   │       │   ├── enums.proto
│   │       │   └── messages.proto
│   │       ├── error/               # Error handling patterns
│   │       │   ├── enums.proto
│   │       │   ├── messages.proto
│   │       │   └── README.md
│   │       ├── geo/                 # Geographic location
│   │       │   ├── enums.proto
│   │       │   └── messages.proto
│   │       ├── network/             # Network connectivity context
│   │       │   ├── enums.proto
│   │       │   └── messages.proto
│   │       ├── pagination/          # Pagination patterns
│   │       │   └── messages.proto
│   │       ├── request/             # Request metadata
│   │       │   ├── enums.proto
│   │       │   └── messages.proto
│   │       ├── retry/               # Retry strategies
│   │       │   ├── enums.proto
│   │       │   └── messages.proto
│   │       ├── session/             # Session state
│   │       │   ├── enums.proto
│   │       │   └── messages.proto
│   │       └── token/               # Token structures
│   │           ├── enums.proto
│   │           └── messages.proto
│   │
│   ├── idp/                         # Identity Provider (IDP)
│   │   ├── README.md
│   │   ├── IDP_VS_AUTH.md          # IDP vs Auth domain comparison
│   │   ├── FLAT_DESIGN_REFACTOR.md # Design decisions
│   │   ├── ENTERPRISE_UPGRADE.md   # Enterprise features
│   │   └── v1/
│   │       ├── enums.proto          # Core IDP enumerations
│   │       ├── services.proto       # Main IdentityService
│   │       │
│   │       ├── authentication.proto # Auth operations
│   │       ├── auth_service.proto   # Dedicated auth service
│   │       ├── auth/                # Modular auth components
│   │       │   ├── enums.proto
│   │       │   ├── messages.proto
│   │       │   ├── service.proto
│   │       │   └── types.proto
│   │       │
│   │       ├── tokens.proto         # Token management
│   │       ├── token_service.proto  # Dedicated token service
│   │       ├── token/               # Modular token components
│   │       │   ├── enums.proto
│   │       │   ├── messages.proto
│   │       │   └── service.proto
│   │       │
│   │       ├── password.proto       # Password operations
│   │       ├── password_service.proto # Dedicated password service
│   │       ├── password/            # Modular password components
│   │       │   ├── messages.proto
│   │       │   └── service.proto
│   │       │
│   │       ├── session.proto        # Session management
│   │       ├── session_service.proto # Dedicated session service
│   │       ├── session/             # Modular session components
│   │       │   ├── messages.proto
│   │       │   └── service.proto
│   │       │
│   │       ├── mfa.proto           # Multi-factor auth
│   │       ├── mfa_service.proto   # Dedicated MFA service
│   │       ├── mfa/                # Modular MFA components
│   │       │   ├── enums.proto
│   │       │   ├── messages.proto
│   │       │   ├── service.proto
│   │       │   └── types.proto
│   │       │
│   │       ├── webauthn.proto      # WebAuthn/FIDO2
│   │       ├── webauthn_service.proto # Dedicated WebAuthn service
│   │       ├── webauthn/           # Modular WebAuthn components
│   │       │   ├── enums.proto
│   │       │   ├── messages.proto
│   │       │   └── service.proto
│   │       │
│   │       ├── security.proto      # Security operations
│   │       ├── security_service.proto # Dedicated security service
│   │       ├── security/           # Modular security components
│   │       │   ├── enums.proto
│   │       │   ├── messages.proto
│   │       │   └── service.proto
│   │       │
│   │       ├── audit.proto         # Audit logging
│   │       ├── audit_service.proto # Dedicated audit service
│   │       ├── audit/              # Modular audit components
│   │       │   ├── enums.proto
│   │       │   ├── messages.proto
│   │       │   └── service.proto
│   │       │
│   │       ├── MODULAR_ARCHITECTURE.md # Architecture documentation
│   │       └── README.md           # IDP v1 overview
│   │
│   ├── auth/                        # Authentication [DEPRECATED]
│   │   ├── README.md                # Migration guide to IDP
│   │   └── v1/
│   │       ├── enums.proto          # Status enumerations
│   │       ├── authentication.proto # Auth messages
│   │       ├── password.proto       # Password management
│   │       ├── session.proto        # Session management
│   │       ├── tokens.proto         # Token structures
│   │       ├── proofs.proto         # Auth proof types
│   │       ├── webauthn.proto       # WebAuthn/FIDO2
│   │       ├── messages.proto       # Shared messages
│   │       ├── services.proto       # AuthenticationService
│   │       └── events.proto         # Auth domain events
│   │
│   ├── users/                       # User Management
│   │   ├── README.md
│   │   └── v1/
│   │       ├── users.proto          # User domain
│   │       └── events.proto         # User domain events
│   │
│   ├── access_policy/               # Authorization & RBAC
│   │   ├── README.md
│   │   └── v1/
│   │       ├── enums.proto          # Policy enumerations
│   │       ├── messages.proto       # Roles, permissions
│   │       ├── requests.proto       # Request messages
│   │       ├── service.proto        # AccessPolicyService
│   │       ├── access_policy.proto  # Main domain file
│   │       ├── access_policy_new.proto # Refactored version
│   │       └── events.proto         # Access policy events
│   │
│   ├── tenants/                     # Multi-Tenant Management
│   │   ├── README.md
│   │   └── v1/
│   │       ├── tenants.proto        # Tenant domain
│   │       └── events.proto         # Tenant domain events
│   │
│   ├── billing/                     # Billing & Subscriptions
│   │   ├── README.md
│   │   └── v1/
│   │       ├── billing.proto        # Billing domain
│   │       └── events.proto         # Billing domain events
│   │
│   ├── notifications/               # Multi-Channel Notifications
│   │   ├── README.md
│   │   └── v1/
│   │       ├── notifications.proto  # Notification domain
│   │       └── events.proto         # Notification domain events
│   │
│   └── IDP_VS_AUTH.md              # IDP vs Auth comparison doc
│
├── docs/                            # Project documentation
│   ├── ARCHITECTURE.md              # System architecture
│   ├── CLIENT_GENERATION.md         # Client generation guide
│   ├── DEPLOYMENT.md                # Deployment strategies
│   ├── VALIDATION.md                # Validation patterns
│   ├── PROTO_DOCUMENTATION_STANDARD.md # Proto doc standards
│   ├── ENTERPRISE_COMPLIANCE.md     # Compliance documentation
│   ├── ENTERPRISE_COMPLIANCE_SUMMARY.md # Compliance summary
│   └── ENTERPRISE_STANDARDS.md      # Enterprise standards
│
├── gen/                             # Generated code (gitignored)
│   ├── go/                          # Generated Go code
│   ├── python/                      # Generated Python code
│   ├── java/                        # Generated Java code
│   ├── typescript/                  # Generated TypeScript code
│   ├── csharp/                      # Generated C# code
│   └── docs/                        # Generated documentation
│
├── .github/                         # GitHub configuration
│   └── workflows/
│       └── buf.yml                  # CI/CD workflow
│
├── buf.yaml                         # Buf configuration
├── buf.gen.yaml                     # Code generation config
├── README.md                        # Main documentation
├── SUMMARY.md                       # Implementation summary
├── QUICK_START.md                   # Quick start guide
├── CONTRIBUTING.md                  # Contribution guidelines
├── LICENSE                          # License file
└── PROJECT_STRUCTURE.md            # This file
```

---

## Domain Architecture

### Domain Breakdown

#### 1. **Core Domain** (`proto/core/`)

**Purpose**: Foundation types used across all domains

**Components**:
- `metadata.proto`: Common metadata (ID, timestamps, tenant context)
- `types.proto`: Shared value objects (Address, Money, ContactInfo)
- `events.proto`: Base event structure for event-driven patterns

**Key Messages**:
- `Metadata` - Universal entity metadata
- `TenantContext` - Multi-tenant isolation
- `Address` - Physical/mailing addresses
- `Money` - Currency and amount
- `ContactInfo` - Email, phone contact details
- `BaseEvent` - Foundation for all domain events

**Usage**: Imported by all domain services for common types

---

#### 2. **Data Structure Domain** (`proto/datastructure/`)

**Purpose**: Context data structures with single responsibility design

**Architecture**: Composition-based, no field duplication

**Components**:

##### **Geographic Context** (`geo/`)
- `GeoLocation`: Country, region, city, coordinates, timezone
- Source of truth for all geographic data

##### **Device Context** (`device/`)
- `DeviceContext`: Hardware specs, OS details, security indicators
- Device identification, capabilities, trust level
- References GeoLocation for GPS data

##### **Client Context** (`client/`)
- `ClientContext`: Application/browser metadata
- User agent, display properties, language/locale
- Application details, SDK info, feature flags

##### **Network Context** (`network/`)
- `NetworkContext`: IP addressing, network type, protocol details
- TLS/security info, VPN detection, threat assessment

##### **Request Context** (`request/`)
- `RequestContext`: Request metadata and authorization
- Composes Device, Client, Network, and Geo contexts
- User authentication, tracing, priority

##### **Session Context** (`session/`)
- `Session`: Session state and lifecycle
- Composes Device, Client, Network contexts
- Authentication tokens, roles, permissions

##### **Other Structures**
- `circuit_breaker/`: Circuit breaker patterns
- `error/`: Error handling structures
- `pagination/`: Pagination patterns
- `retry/`: Retry strategies
- `token/`: Token structures

**Key Design Principle**: Each context has single responsibility with no field duplication across contexts

---

#### 3. **Identity Provider Domain (IDP)** (`proto/idp/`)

**Purpose**: Comprehensive identity and authentication management

**Status**: Active, modern implementation (replaces auth domain)

**Architecture**: Both flat (root level) and modular (subdirectories) files

**Services** (9 total):
1. `IdentityService` - Unified identity operations
2. `AuthenticationService` - Core authentication
3. `TokenService` - Token lifecycle management
4. `PasswordService` - Password operations
5. `SessionService` - Session management
6. `MFAService` - Multi-factor authentication
7. `WebAuthnService` - WebAuthn/FIDO2
8. `SecurityService` - Security operations
9. `AuditService` - Audit logging

**Components**:

##### **Authentication** (`authentication.proto`, `auth_service.proto`, `auth/`)
- Login, logout, refresh token
- Credential validation
- Authentication factors

##### **Token Management** (`tokens.proto`, `token_service.proto`, `token/`)
- JWT token generation/validation
- Refresh token handling
- Token revocation

##### **Password Management** (`password.proto`, `password_service.proto`, `password/`)
- Password creation, update, reset
- Password policies and validation
- Temporary password generation

##### **Session Management** (`session.proto`, `session_service.proto`, `session/`)
- Session creation, validation, termination
- Multi-device session tracking
- Session security

##### **Multi-Factor Authentication** (`mfa.proto`, `mfa_service.proto`, `mfa/`)
- TOTP (Time-based One-Time Password)
- SMS, Email verification codes
- Backup codes

##### **WebAuthn/FIDO2** (`webauthn.proto`, `webauthn_service.proto`, `webauthn/`)
- Passwordless authentication
- Biometric authentication
- Hardware security keys

##### **Security Operations** (`security.proto`, `security_service.proto`, `security/`)
- Risk assessment
- Anomaly detection
- Security events

##### **Audit Logging** (`audit.proto`, `audit_service.proto`, `audit/`)
- Authentication events
- Security audit trails
- Compliance logging

**Documentation**:
- `README.md` - IDP overview
- `IDP_VS_AUTH.md` - Comparison with legacy auth domain
- `FLAT_DESIGN_REFACTOR.md` - Design decisions
- `ENTERPRISE_UPGRADE.md` - Enterprise features
- `MODULAR_ARCHITECTURE.md` - Architecture guide

---

#### 4. **Authentication Domain [DEPRECATED]** (`proto/auth/`)

**Purpose**: Legacy authentication and session management

**Status**: Deprecated in favor of `proto/idp/`

**Migration Path**: Use IDP domain for new implementations

**Services**:
- `AuthenticationService` - Basic auth operations

**Components**:
- `authentication.proto` - Auth messages
- `tokens.proto` - Token structures
- `password.proto` - Password management
- `session.proto` - Session handling
- `webauthn.proto` - WebAuthn support
- `proofs.proto` - Auth proof types
- `events.proto` - Auth events

**Note**: Kept for backward compatibility during migration period

---

#### 5. **Users Domain** (`proto/users/`)

**Purpose**: User profile and lifecycle management

**Service**: `UserService`

**Key Operations**:
- `CreateUser` - User registration
- `GetUser` - Retrieve user details
- `UpdateUser` - Profile updates
- `DeleteUser` - User removal
- `ListUsers` - User directory
- `UpdateUserStatus` - Status management
- `ChangePassword` - Password changes

**Key Messages**:
- `User` - Core user entity
- `UserProfile` - Extended profile data
- `UserPreferences` - User settings
- `UserAddress` - Physical addresses

**Events** (7 total):
- `UserCreatedEvent`
- `UserUpdatedEvent`
- `UserDeletedEvent`
- `UserStatusChangedEvent`
- `PasswordChangedEvent`
- `UserEmailVerifiedEvent`
- `UserPhoneVerifiedEvent`

**Features**:
- Multi-tenant user isolation
- Status management (Active, Suspended, Deleted)
- Email/phone verification
- Profile customization
- Soft delete support

---

#### 6. **Access Policy Domain** (`proto/access_policy/`)

**Purpose**: Role-Based Access Control (RBAC) and authorization

**Service**: `AccessPolicyService`

**Key Operations**:
- `CreateRole` - Define new roles
- `AssignRole` - Assign roles to users
- `CreatePermission` - Define permissions
- `CheckPermission` - Authorization check
- `CreatePolicy` - Create access policies
- `ListRoles` - Role directory
- `ListPermissions` - Permission catalog
- `RevokeRole` - Remove role assignment

**Key Messages**:
- `Role` - Role definition
- `Permission` - Permission definition
- `Policy` - Access policy with conditions
- `PolicyCondition` - Conditional access rules

**Events** (8 total):
- `RoleCreatedEvent`
- `RoleAssignedEvent`
- `RoleRevokedEvent`
- `PermissionCreatedEvent`
- `PermissionAssignedEvent`
- `PolicyCreatedEvent`
- `PolicyUpdatedEvent`
- `PermissionCheckedEvent`

**Features**:
- Hierarchical roles
- Fine-grained permissions
- Attribute-based policies
- Conditional access rules
- Permission inheritance

---

#### 7. **Tenants Domain** (`proto/tenants/`)

**Purpose**: Multi-tenant organization management

**Service**: `TenantService`

**Key Operations**:
- `CreateTenant` - Onboard new tenant
- `GetTenant` - Retrieve tenant details
- `UpdateTenant` - Update tenant info
- `DeleteTenant` - Remove tenant
- `ListTenants` - Tenant directory
- `UpdateTenantStatus` - Status management
- `UpdateTenantTier` - Tier upgrades/downgrades
- `GetTenantUsage` - Usage metrics

**Key Messages**:
- `Tenant` - Core tenant entity
- `TenantSettings` - Configuration settings
- `TenantBranding` - Custom branding
- `TenantUsage` - Resource usage tracking

**Events** (7 total):
- `TenantCreatedEvent`
- `TenantUpdatedEvent`
- `TenantDeletedEvent`
- `TenantStatusChangedEvent`
- `TenantTierChangedEvent`
- `TenantSuspendedEvent`
- `TenantReactivatedEvent`

**Features**:
- Tiered tenancy (Free, Starter, Professional, Enterprise)
- Custom branding per tenant
- Resource usage tracking
- Tenant isolation enforcement
- Status management (Active, Suspended, Trial)

---

#### 8. **Billing Domain** (`proto/billing/`)

**Purpose**: Subscription and payment management

**Service**: `BillingService`

**Key Operations**:
- `CreateSubscription` - New subscription
- `UpdateSubscription` - Modify subscription
- `CancelSubscription` - End subscription
- `ListSubscriptions` - Subscription list
- `GetInvoice` - Invoice details
- `PayInvoice` - Process payment
- `ListInvoices` - Invoice history
- `AddPaymentMethod` - Payment setup
- `RemovePaymentMethod` - Remove payment

**Key Messages**:
- `Subscription` - Subscription details
- `Invoice` - Invoice data
- `Payment` - Payment record
- `Plan` - Pricing plan
- `PaymentMethod` - Payment information

**Events** (11 total):
- `SubscriptionCreatedEvent`
- `SubscriptionUpdatedEvent`
- `SubscriptionCanceledEvent`
- `SubscriptionRenewedEvent`
- `InvoiceGeneratedEvent`
- `InvoicePaidEvent`
- `InvoiceOverdueEvent`
- `PaymentSucceededEvent`
- `PaymentFailedEvent`
- `PaymentMethodAddedEvent`
- `PaymentMethodRemovedEvent`

**Features**:
- Recurring subscriptions
- Invoice generation
- Multiple payment methods
- Payment processing
- Subscription lifecycle

---

#### 9. **Notifications Domain** (`proto/notifications/`)

**Purpose**: Multi-channel notification delivery

**Service**: `NotificationService`

**Key Operations**:
- `SendNotification` - Deliver notification
- `GetNotification` - Retrieve notification
- `ListNotifications` - Notification history
- `MarkNotificationRead` - Read tracking
- `DeleteNotification` - Remove notification
- `UpdatePreferences` - Notification settings
- `GetPreferences` - Retrieve preferences
- `BatchSendNotifications` - Bulk delivery

**Key Messages**:
- `Notification` - Notification entity
- `NotificationPreferences` - User preferences
- `NotificationTemplate` - Template definition
- `NotificationChannel` - Channel config

**Events** (6 total):
- `NotificationSentEvent`
- `NotificationDeliveredEvent`
- `NotificationReadEvent`
- `NotificationFailedEvent`
- `NotificationDeletedEvent`
- `NotificationPreferencesUpdatedEvent`

**Features**:
- Multi-channel (Email, SMS, Push, In-App)
- Priority levels (Low, Normal, High, Urgent)
- Read tracking
- User preferences
- Template support
- Batch delivery

---

## File Organization

### Proto File Patterns

Each domain follows consistent file organization:

#### **Standard Domain Structure**

```
domain/
└── v1/
    ├── enums.proto       # Domain-specific enumerations
    ├── messages.proto    # Core domain messages
    ├── requests.proto    # Request/response messages
    ├── service.proto     # gRPC service definition
    ├── events.proto      # Domain events
    └── {domain}.proto    # Main file (often aggregates)
```

#### **IDP Modular Structure**

```
idp/v1/
├── {feature}.proto              # Flat files at root
├── {feature}_service.proto      # Flat service files
└── {feature}/                   # Modular subdirectories
    ├── enums.proto
    ├── messages.proto
    ├── service.proto
    └── types.proto
```

**Note**: IDP supports both flat and modular imports for flexibility

### Naming Conventions

#### **Files**
- Snake case: `access_policy.proto`, `user_service.proto`
- Descriptive: `password_reset.proto`, `mfa_totp.proto`
- Versioned: Always in `v1/`, `v2/` directory

#### **Messages**
- PascalCase: `UserProfile`, `TenantSettings`
- Request suffix: `CreateUserRequest`
- Response suffix: `CreateUserResponse`
- Event suffix: `UserCreatedEvent`

#### **Services**
- PascalCase with "Service" suffix: `UserService`, `BillingService`
- Descriptive: `AuthenticationService`, `NotificationService`

#### **RPCs**
- Verb-first: `CreateUser`, `UpdateTenant`, `SendNotification`
- Action-oriented: `ValidateToken`, `CheckPermission`, `ProcessPayment`

#### **Fields**
- Snake case: `user_id`, `tenant_context`, `created_at`
- Descriptive: `email_verified`, `subscription_status`

#### **Enums**
- PascalCase: `UserStatus`, `NotificationType`
- Values UPPER_SNAKE_CASE: `USER_STATUS_ACTIVE`, `NOTIFICATION_TYPE_EMAIL`
- Always include `_UNSPECIFIED` as value 0

---

## Service Catalog

### Complete Service Inventory

| # | Service | Domain | RPCs | Description |
|---|---------|--------|------|-------------|
| 1 | `IdentityService` | IDP | 20+ | Unified identity operations |
| 2 | `AuthenticationService` | IDP/Auth | 6 | Core authentication |
| 3 | `TokenService` | IDP | 6 | Token lifecycle management |
| 4 | `PasswordService` | IDP | 5 | Password operations |
| 5 | `SessionService` | IDP | 6 | Session management |
| 6 | `MFAService` | IDP | 8 | Multi-factor authentication |
| 7 | `WebAuthnService` | IDP | 6 | WebAuthn/FIDO2 |
| 8 | `SecurityService` | IDP | 7 | Security operations |
| 9 | `AuditService` | IDP | 5 | Audit logging |
| 10 | `UserService` | Users | 7 | User management |
| 11 | `AccessPolicyService` | Access Policy | 8 | Authorization & RBAC |
| 12 | `TenantService` | Tenants | 8 | Multi-tenant management |
| 13 | `BillingService` | Billing | 9 | Subscriptions & payments |
| 14 | `NotificationService` | Notifications | 8 | Multi-channel notifications |

**Total Services**: 14  
**Total RPC Methods**: 100+  
**Proto Files**: 92  

### Service Details

#### **IdentityService** (IDP)

```protobuf
service IdentityService {
  // Authentication
  rpc Authenticate(AuthenticateRequest) returns (AuthenticateResponse);
  rpc RefreshToken(RefreshTokenRequest) returns (RefreshTokenResponse);
  rpc Logout(LogoutRequest) returns (LogoutResponse);
  
  // Token Management
  rpc ValidateToken(ValidateTokenRequest) returns (ValidateTokenResponse);
  rpc RevokeToken(RevokeTokenRequest) returns (RevokeTokenResponse);
  
  // Password
  rpc ChangePassword(ChangePasswordRequest) returns (ChangePasswordResponse);
  rpc ResetPassword(ResetPasswordRequest) returns (ResetPasswordResponse);
  rpc RequestPasswordReset(RequestPasswordResetRequest) returns (RequestPasswordResetResponse);
  
  // Session
  rpc CreateSession(CreateSessionRequest) returns (CreateSessionResponse);
  rpc GetSession(GetSessionRequest) returns (GetSessionResponse);
  rpc TerminateSession(TerminateSessionRequest) returns (TerminateSessionResponse);
  rpc ListSessions(ListSessionsRequest) returns (ListSessionsResponse);
  
  // MFA
  rpc EnableMFA(EnableMFARequest) returns (EnableMFAResponse);
  rpc VerifyMFA(VerifyMFARequest) returns (VerifyMFAResponse);
  rpc DisableMFA(DisableMFARequest) returns (DisableMFAResponse);
  
  // WebAuthn
  rpc RegisterWebAuthn(RegisterWebAuthnRequest) returns (RegisterWebAuthnResponse);
  rpc AuthenticateWebAuthn(AuthenticateWebAuthnRequest) returns (AuthenticateWebAuthnResponse);
  
  // Security
  rpc AssessRisk(AssessRiskRequest) returns (AssessRiskResponse);
  
  // Audit
  rpc GetAuditLog(GetAuditLogRequest) returns (GetAuditLogResponse);
}
```

#### **UserService** (Users)

```protobuf
service UserService {
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
  rpc UpdateUser(UpdateUserRequest) returns (UpdateUserResponse);
  rpc DeleteUser(DeleteUserRequest) returns (DeleteUserResponse);
  rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
  rpc UpdateUserStatus(UpdateUserStatusRequest) returns (UpdateUserStatusResponse);
  rpc ChangePassword(ChangePasswordRequest) returns (ChangePasswordResponse);
}
```

#### **AccessPolicyService** (Access Policy)

```protobuf
service AccessPolicyService {
  rpc CreateRole(CreateRoleRequest) returns (CreateRoleResponse);
  rpc AssignRole(AssignRoleRequest) returns (AssignRoleResponse);
  rpc RevokeRole(RevokeRoleRequest) returns (RevokeRoleResponse);
  rpc CreatePermission(CreatePermissionRequest) returns (CreatePermissionResponse);
  rpc CheckPermission(CheckPermissionRequest) returns (CheckPermissionResponse);
  rpc CreatePolicy(CreatePolicyRequest) returns (CreatePolicyResponse);
  rpc ListRoles(ListRolesRequest) returns (ListRolesResponse);
  rpc ListPermissions(ListPermissionsRequest) returns (ListPermissionsResponse);
}
```

#### **TenantService** (Tenants)

```protobuf
service TenantService {
  rpc CreateTenant(CreateTenantRequest) returns (CreateTenantResponse);
  rpc GetTenant(GetTenantRequest) returns (GetTenantResponse);
  rpc UpdateTenant(UpdateTenantRequest) returns (UpdateTenantResponse);
  rpc DeleteTenant(DeleteTenantRequest) returns (DeleteTenantResponse);
  rpc ListTenants(ListTenantsRequest) returns (ListTenantsResponse);
  rpc UpdateTenantStatus(UpdateTenantStatusRequest) returns (UpdateTenantStatusResponse);
  rpc UpdateTenantTier(UpdateTenantTierRequest) returns (UpdateTenantTierResponse);
  rpc GetTenantUsage(GetTenantUsageRequest) returns (GetTenantUsageResponse);
}
```

#### **BillingService** (Billing)

```protobuf
service BillingService {
  rpc CreateSubscription(CreateSubscriptionRequest) returns (CreateSubscriptionResponse);
  rpc UpdateSubscription(UpdateSubscriptionRequest) returns (UpdateSubscriptionResponse);
  rpc CancelSubscription(CancelSubscriptionRequest) returns (CancelSubscriptionResponse);
  rpc ListSubscriptions(ListSubscriptionsRequest) returns (ListSubscriptionsResponse);
  rpc GetInvoice(GetInvoiceRequest) returns (GetInvoiceResponse);
  rpc PayInvoice(PayInvoiceRequest) returns (PayInvoiceResponse);
  rpc ListInvoices(ListInvoicesRequest) returns (ListInvoicesResponse);
  rpc AddPaymentMethod(AddPaymentMethodRequest) returns (AddPaymentMethodResponse);
  rpc RemovePaymentMethod(RemovePaymentMethodRequest) returns (RemovePaymentMethodResponse);
}
```

#### **NotificationService** (Notifications)

```protobuf
service NotificationService {
  rpc SendNotification(SendNotificationRequest) returns (SendNotificationResponse);
  rpc GetNotification(GetNotificationRequest) returns (GetNotificationResponse);
  rpc ListNotifications(ListNotificationsRequest) returns (ListNotificationsResponse);
  rpc MarkNotificationRead(MarkNotificationReadRequest) returns (MarkNotificationReadResponse);
  rpc DeleteNotification(DeleteNotificationRequest) returns (DeleteNotificationResponse);
  rpc UpdatePreferences(UpdatePreferencesRequest) returns (UpdatePreferencesResponse);
  rpc GetPreferences(GetPreferencesRequest) returns (GetPreferencesResponse);
  rpc BatchSendNotifications(BatchSendNotificationsRequest) returns (BatchSendNotificationsResponse);
}
```

---

## Event Catalog

### Event-Driven Architecture

All domains publish events for important state changes, enabling:
- Event sourcing
- CQRS patterns
- Audit trails
- Real-time notifications
- Inter-service communication

### Event Structure

All events inherit from `BaseEvent`:

```protobuf
message BaseEvent {
  string event_id = 1;                          // Unique event identifier
  string event_type = 2;                        // Event type name
  string aggregate_id = 3;                      // ID of affected entity
  int32 aggregate_version = 4;                  // Version of entity
  TenantContext tenant_context = 5;             // Multi-tenant context
  google.protobuf.Timestamp occurred_at = 6;    // Event timestamp
  string user_id = 7;                           // User who triggered event
  string session_id = 8;                        // Session context
  google.protobuf.Any payload = 9;              // Event payload
  map<string, string> metadata = 10;            // Additional metadata
  string correlation_id = 11;                   // Trace ID
  string causation_id = 12;                     // Parent event ID
}
```

### Domain Events Inventory

#### **Core Domain Events**
- `BaseEvent` - Foundation for all events

#### **Users Domain Events** (7 events)
- `UserCreatedEvent` - New user registered
- `UserUpdatedEvent` - User profile updated
- `UserDeletedEvent` - User removed
- `UserStatusChangedEvent` - Status transition
- `PasswordChangedEvent` - Password updated
- `UserEmailVerifiedEvent` - Email verified
- `UserPhoneVerifiedEvent` - Phone verified

#### **Access Policy Domain Events** (8 events)
- `RoleCreatedEvent` - New role defined
- `RoleAssignedEvent` - Role assigned to user
- `RoleRevokedEvent` - Role removed from user
- `PermissionCreatedEvent` - New permission defined
- `PermissionAssignedEvent` - Permission granted
- `PolicyCreatedEvent` - New policy created
- `PolicyUpdatedEvent` - Policy modified
- `PermissionCheckedEvent` - Authorization check performed

#### **Tenants Domain Events** (7 events)
- `TenantCreatedEvent` - New tenant onboarded
- `TenantUpdatedEvent` - Tenant info updated
- `TenantDeletedEvent` - Tenant removed
- `TenantStatusChangedEvent` - Status transition
- `TenantTierChangedEvent` - Tier upgrade/downgrade
- `TenantSuspendedEvent` - Tenant suspended
- `TenantReactivatedEvent` - Tenant reactivated

#### **Billing Domain Events** (11 events)
- `SubscriptionCreatedEvent` - New subscription
- `SubscriptionUpdatedEvent` - Subscription modified
- `SubscriptionCanceledEvent` - Subscription ended
- `SubscriptionRenewedEvent` - Subscription renewed
- `InvoiceGeneratedEvent` - Invoice created
- `InvoicePaidEvent` - Payment received
- `InvoiceOverdueEvent` - Payment overdue
- `PaymentSucceededEvent` - Payment successful
- `PaymentFailedEvent` - Payment failed
- `PaymentMethodAddedEvent` - Payment method added
- `PaymentMethodRemovedEvent` - Payment method removed

#### **Notifications Domain Events** (6 events)
- `NotificationSentEvent` - Notification dispatched
- `NotificationDeliveredEvent` - Notification delivered
- `NotificationReadEvent` - Notification read by user
- `NotificationFailedEvent` - Delivery failed
- `NotificationDeletedEvent` - Notification removed
- `NotificationPreferencesUpdatedEvent` - Preferences changed

#### **Auth Domain Events** (6 events) [DEPRECATED]
- `UserAuthenticatedEvent`
- `UserLoggedOutEvent`
- `TokenRefreshedEvent`
- `PasswordResetRequestedEvent`
- `PasswordChangedEvent`
- `SessionExpiredEvent`

**Total Events**: 45+ across all domains

---

## Data Structure Layer

### Context Architecture

The data structure layer provides reusable context structures following **Single Responsibility Principle** with **composition over duplication**.

### Key Principles

1. **Single Source of Truth**: Each field exists in exactly one context
2. **No Duplication**: No field is repeated across contexts
3. **Composition**: Higher-level contexts reference lower-level contexts
4. **Clear Boundaries**: Each context has specific responsibility

### Context Hierarchy

```
RequestContext
├── RequestMetadata (inline: protocol, method, headers)
├── DeviceContext → GeoLocation (GPS)
├── ClientContext (inline: all client fields)
├── NetworkContext (inline: all network fields)
└── GeoLocation (IP-derived, separate from device GPS)

Session
├── Session fields (inline: session ID, tokens, roles)
├── DeviceContext → GeoLocation (GPS)
├── ClientContext (inline: all client fields)
├── NetworkContext (inline: all network fields)
└── GeoLocation (IP-derived)
```

### Context Responsibilities

| Context | Responsibility | Key Fields |
|---------|---------------|-----------|
| **GeoLocation** | Geographic data | Country, region, city, coordinates, timezone |
| **DeviceContext** | Hardware & OS | Device ID, model, OS, CPU, RAM, security indicators |
| **ClientContext** | Application software | User agent, browser, display, language, app version |
| **NetworkContext** | Network connectivity | IP address, network type, protocol, TLS, VPN detection |
| **RequestContext** | Request metadata | Composition of all contexts + auth data |
| **Session** | Session state | Session lifecycle + composition of contexts |
| **ErrorContext** | Error handling | Error codes, messages, stack traces |
| **CircuitBreaker** | Resilience patterns | Circuit state, failure thresholds |
| **RetryContext** | Retry strategies | Retry count, backoff policies |
| **PaginationContext** | Pagination | Page size, tokens, cursors |

### Usage Patterns

#### **Minimal Context** (authentication only)
```protobuf
message LoginRequest {
  string email = 1;
  string password = 2;
  geniustechspace.datastructure.v1.network.NetworkContext network = 3;
}
```

#### **Full Context** (comprehensive tracking)
```protobuf
message CreateUserRequest {
  string tenant_id = 1;
  User user = 2;
  geniustechspace.datastructure.v1.device.DeviceContext device = 3;
  geniustechspace.datastructure.v1.client.ClientContext client = 4;
  geniustechspace.datastructure.v1.network.NetworkContext network = 5;
  geniustechspace.datastructure.v1.geo.GeoLocation geo = 6;
}
```

#### **Selective Context** (specific needs)
```protobuf
// Risk assessment
message RiskAssessmentRequest {
  geniustechspace.datastructure.v1.device.DeviceContext device = 1;
  geniustechspace.datastructure.v1.network.NetworkContext network = 2;
}

// Analytics
message AnalyticsEvent {
  geniustechspace.datastructure.v1.client.ClientContext client = 1;
  geniustechspace.datastructure.v1.geo.GeoLocation geo = 2;
}
```

---

## Configuration Files

### buf.yaml

**Purpose**: Buf module configuration, linting, and breaking change detection

```yaml
version: v2
modules:
  - path: proto
    name: buf.build/geniustechspace/protobuf
deps:
  - buf.build/bufbuild/protovalidate
  - buf.build/googleapis/googleapis
lint:
  use:
    - STANDARD
    - UNARY_RPC
  except:
    - PACKAGE_VERSION_SUFFIX
  enum_zero_value_suffix: _UNSPECIFIED
  rpc_allow_same_request_response: false
  rpc_allow_google_protobuf_empty_requests: false
  rpc_allow_google_protobuf_empty_responses: false
  service_suffix: Service
breaking:
  use:
    - FILE
  ignore:
    - proto/core/v2
  ignore_unstable_packages: false
```

**Key Settings**:
- **Linting**: STANDARD + UNARY_RPC rules
- **Breaking Changes**: FILE-level detection
- **Enum Convention**: All enums end with `_UNSPECIFIED` for zero value
- **Service Convention**: All services end with `Service`

### buf.gen.yaml

**Purpose**: Multi-language code generation configuration

```yaml
version: v2
managed:
  enabled: true
  override:
    - file_option: go_package_prefix
      value: github.com/geniustechspace/protobuf/gen/go
    - file_option: java_package_prefix
      value: com.geniustechspace.protobuf
    - file_option: csharp_namespace_prefix
      value: GeniusTechSpace.Protobuf
plugins:
  # Go
  - remote: buf.build/protocolbuffers/go:latest
  - remote: buf.build/grpc/go:latest
  - remote: buf.build/bufbuild/protovalidate-go:latest
  
  # Java
  - remote: buf.build/protocolbuffers/java:latest
  - remote: buf.build/grpc/java:latest
  
  # Python
  - remote: buf.build/protocolbuffers/python:latest
  - remote: buf.build/grpc/python:latest
  - remote: buf.build/bufbuild/protovalidate-python:latest
  
  # TypeScript
  - remote: buf.build/connectrpc/es:latest
  
  # C#
  - remote: buf.build/protocolbuffers/csharp:latest
  - remote: buf.build/grpc/csharp:latest
  
  # Documentation
  - remote: buf.build/bufbuild/buf-plugin-doc:latest
```

**Supported Languages**:
- Go (with validation)
- Java
- Python (with validation)
- TypeScript
- C#
- Documentation (Markdown)

---

## Documentation

### Documentation Structure

#### **Root Documentation**
- `README.md` - Main overview, quick start, features
- `SUMMARY.md` - Implementation summary and metrics
- `QUICK_START.md` - 5-minute getting started guide
- `CONTRIBUTING.md` - Contribution guidelines
- `LICENSE` - License information
- `PROJECT_STRUCTURE.md` - This comprehensive guide

#### **Docs Directory** (`docs/`)
- `ARCHITECTURE.md` - System architecture and patterns
- `CLIENT_GENERATION.md` - Language-specific client generation
- `DEPLOYMENT.md` - Kubernetes, service mesh, monitoring
- `VALIDATION.md` - Validation patterns and rules
- `PROTO_DOCUMENTATION_STANDARD.md` - Proto documentation standards
- `ENTERPRISE_COMPLIANCE.md` - Compliance documentation
- `ENTERPRISE_COMPLIANCE_SUMMARY.md` - Compliance summary
- `ENTERPRISE_STANDARDS.md` - Enterprise standards

#### **Domain Documentation** (within proto/)
- `proto/core/README.md` - Core types and usage
- `proto/idp/README.md` - IDP overview
- `proto/idp/IDP_VS_AUTH.md` - IDP vs Auth comparison
- `proto/idp/FLAT_DESIGN_REFACTOR.md` - Design decisions
- `proto/idp/ENTERPRISE_UPGRADE.md` - Enterprise features
- `proto/idp/v1/MODULAR_ARCHITECTURE.md` - Modular architecture
- `proto/auth/README.md` - Auth domain (deprecated)
- `proto/users/README.md` - User management
- `proto/access_policy/README.md` - RBAC documentation
- `proto/tenants/README.md` - Multi-tenancy guide
- `proto/billing/README.md` - Billing and subscriptions
- `proto/notifications/README.md` - Notification system
- `proto/datastructure/ARCHITECTURE.md` - Context architecture
- `proto/datastructure/README.md` - Data structure usage
- `proto/datastructure/v1/*/README.md` - Component-specific docs

**Total Documentation**: ~60+ KB of comprehensive guides

---

## Code Generation

### Generation Process

#### **Command**
```bash
buf generate
```

#### **Output Structure**
```
gen/
├── go/
│   ├── core/v1/
│   ├── idp/v1/
│   ├── users/v1/
│   ├── access_policy/v1/
│   ├── tenants/v1/
│   ├── billing/v1/
│   └── notifications/v1/
├── python/
│   └── [same structure]
├── java/
│   └── [same structure]
├── typescript/
│   └── [same structure]
├── csharp/
│   └── [same structure]
└── docs/
    └── index.md
```

### Language-Specific Generation

#### **Go**
```bash
# Full generation
buf generate

# Domain-specific
buf generate --path proto/users/v1/

# Usage
import usersv1 "github.com/geniustechspace/protobuf/gen/go/users/v1"
```

#### **Python**
```bash
# Generation
buf generate

# Usage
from gen.python.users.v1 import users_pb2, users_pb2_grpc
```

#### **Java**
```bash
# Generation
buf generate

# Usage
import com.geniustechspace.protobuf.users.v1.UsersProto;
```

#### **TypeScript**
```bash
# Generation
buf generate

# Usage
import { User, UserService } from './gen/typescript/users/v1';
```

#### **C#**
```bash
# Generation
buf generate

# Usage
using GeniusTechSpace.Protobuf.Users.V1;
```

### Per-Domain Client Generation

Generate independent client libraries for specific domains:

```bash
# Users domain only
buf generate --path proto/users/v1/

# Billing domain only
buf generate --path proto/billing/v1/

# Multiple domains
buf generate --path proto/users/v1/ --path proto/billing/v1/
```

### Documentation Generation

```bash
# Generate markdown docs
buf generate

# Output: gen/docs/index.md
```

---

## Dependencies

### External Dependencies

#### **Buf Registry Dependencies**

1. **buf.build/bufbuild/protovalidate**
   - Purpose: Runtime validation
   - Usage: Declarative validation rules in proto files
   - Example:
     ```protobuf
     import "buf/validate/validate.proto";
     
     message CreateUserRequest {
       string email = 1 [(buf.validate.field).string.email = true];
       string password = 2 [(buf.validate.field).string.min_len = 8];
     }
     ```

2. **buf.build/googleapis/googleapis**
   - Purpose: Google common types
   - Usage: Timestamp, Duration, Any, Empty
   - Example:
     ```protobuf
     import "google/protobuf/timestamp.proto";
     
     message User {
       google.protobuf.Timestamp created_at = 1;
     }
     ```

### Internal Dependencies

#### **Cross-Domain Dependencies**

- All domains depend on `core/v1` for common types
- All domains reference `datastructure/v1` contexts as needed
- IDP provides authentication for all other domains
- Access Policy provides authorization for all domains
- Tenants provides multi-tenancy context for all domains

#### **Dependency Graph**

```
core/v1 (foundation)
  ↓
datastructure/v1 (contexts)
  ↓
idp/v1 (authentication)
  ↓
users/v1, tenants/v1 (identity & organization)
  ↓
access_policy/v1 (authorization)
  ↓
billing/v1, notifications/v1 (business services)
```

---

## Technology Stack

### Core Technologies

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| **Schema Definition** | Protocol Buffers | v3 | API definition language |
| **Build Tool** | Buf CLI | 1.47.0+ | Schema management |
| **RPC Framework** | gRPC | Latest | Service communication |
| **Validation** | protovalidate | Latest | Runtime validation |
| **Version Control** | Git | Latest | Source control |
| **CI/CD** | GitHub Actions | - | Automation |

### Code Generation Plugins

| Language | Plugins | Purpose |
|----------|---------|---------|
| **Go** | protoc-gen-go, protoc-gen-go-grpc, protovalidate-go | Go client generation |
| **Python** | protoc-gen-python, protoc-gen-python-grpc, protovalidate-python | Python client generation |
| **Java** | protoc-gen-java, protoc-gen-java-grpc | Java client generation |
| **TypeScript** | connectrpc/es | TypeScript client generation |
| **C#** | protoc-gen-csharp, protoc-gen-csharp-grpc | C# client generation |
| **Documentation** | buf-plugin-doc | Markdown documentation |

### Development Tools

- **Buf CLI**: Schema linting, breaking change detection, code generation
- **Git**: Version control
- **GitHub**: Repository hosting, CI/CD
- **VS Code**: Recommended IDE (with Buf extension)

### Deployment Technologies

- **Kubernetes**: Container orchestration
- **Istio/Linkerd**: Service mesh
- **Prometheus**: Metrics
- **Grafana**: Dashboards
- **Jaeger/Zipkin**: Distributed tracing
- **ELK/Loki**: Log aggregation

---

## Project Metrics

### Repository Statistics

| Metric | Count |
|--------|-------|
| **Total Domains** | 9 |
| **Active Domains** | 8 (excluding deprecated auth) |
| **Proto Files** | 92 |
| **Services** | 14 |
| **RPC Methods** | 100+ |
| **Domain Events** | 45+ |
| **Message Types** | 200+ |
| **Enum Types** | 50+ |
| **Documentation Files** | 20+ |
| **Documentation Size** | ~60 KB |
| **Supported Languages** | 5 (Go, Python, Java, TypeScript, C#) |
| **CI/CD Jobs** | 7 |
| **External Dependencies** | 2 (protovalidate, googleapis) |

### File Breakdown

| Category | Count |
|----------|-------|
| **Core Proto Files** | 3 |
| **Data Structure Proto Files** | 30+ |
| **IDP Proto Files** | 35+ |
| **Auth Proto Files** (deprecated) | 8 |
| **Domain Proto Files** (users, tenants, etc.) | 12 |
| **Configuration Files** | 2 (buf.yaml, buf.gen.yaml) |
| **Documentation Files** | 20+ |
| **Total Files** | 110+ |

### Lines of Code (Approximate)

| Type | Lines |
|------|-------|
| **Proto Definitions** | ~15,000 |
| **Documentation** | ~10,000 |
| **Configuration** | ~200 |
| **Total** | ~25,200 |

---

## Quality Assurance

### Validation & Linting

- ✅ **Buf Linting**: STANDARD + UNARY_RPC rules
- ✅ **Breaking Change Detection**: FILE-level detection
- ✅ **Import Path Validation**: Module-relative imports
- ✅ **Naming Conventions**: Enforced via linting
- ✅ **Code Formatting**: Consistent formatting
- ✅ **Runtime Validation**: protovalidate integration

### CI/CD Pipeline

**GitHub Actions Workflow** (`.github/workflows/buf.yml`):

1. **Lint Job**: Validate proto files, check formatting
2. **Breaking Job**: Detect breaking changes in PRs
3. **Build Job**: Generate code for all languages
4. **Schema List Job**: Create schema inventory
5. **Push to Registry Job**: Publish to Buf Schema Registry
6. **Generate Clients Job**: Per-domain, per-language clients
7. **Documentation Job**: Generate and deploy docs

### Testing Strategy

- **Schema Validation**: Automated via Buf CLI
- **Breaking Change Tests**: Against main branch
- **Code Generation Tests**: Verify all languages compile
- **Integration Tests**: In consuming services
- **Contract Tests**: Between services

---

## Best Practices

### Schema Design

1. ✅ **Always include tenant_id** in requests
2. ✅ **Use Metadata message** for common fields
3. ✅ **Publish events** for state changes
4. ✅ **Use pagination** for list operations
5. ✅ **Implement soft deletes** via metadata
6. ✅ **Reserve field numbers** for deprecated fields
7. ✅ **Version packages** (v1, v2) for major changes

### Code Organization

1. ✅ **Separate files** for enums, messages, services, events
2. ✅ **Module-relative imports** (no absolute paths)
3. ✅ **Consistent naming** (PascalCase messages, snake_case fields)
4. ✅ **Comprehensive documentation** in proto files
5. ✅ **README per domain** explaining usage

### Multi-Tenancy

1. ✅ **TenantContext in all requests**
2. ✅ **Tenant isolation enforcement**
3. ✅ **Tenant-scoped queries**
4. ✅ **Tenant-scoped caching**
5. ✅ **Tenant-aware events**

### Event-Driven

1. ✅ **BaseEvent as foundation**
2. ✅ **Correlation/causation IDs** for tracing
3. ✅ **Immutable events**
4. ✅ **Event versioning**
5. ✅ **Event schema evolution**

---

## Migration & Evolution

### Version Evolution

#### **v1 → v2 Migration**

```protobuf
// v1/users.proto
message User {
  string id = 1;
  string name = 2;
}

// v2/users.proto (backward compatible)
message User {
  string id = 1;
  string name = 2;
  string email = 3;         // New field added
  repeated string tags = 4; // New field added
  reserved 5, 6;            // Reserved for future use
}
```

**Rules**:
- ✅ Never remove or rename fields
- ✅ Never change field types
- ✅ Never change field numbers
- ✅ Always add new fields with new field numbers
- ✅ Use reserved fields for deprecated fields
- ✅ Version packages (v1, v2) for major breaking changes

### Auth → IDP Migration

**Status**: Auth domain deprecated, IDP domain active

**Migration Path**:
1. New implementations use `proto/idp/v1`
2. Existing implementations can continue using `proto/auth/v1`
3. Gradual migration via dual support
4. Eventually remove `proto/auth/` after migration period

**Key Differences**:
- IDP has modular architecture (both flat and subdirectory files)
- IDP has more comprehensive service separation
- IDP includes advanced features (MFA, WebAuthn, Security, Audit)
- IDP follows latest enterprise standards

---

## Future Roadmap

### Planned Enhancements

#### **Phase 1: Core Improvements** (Q1 2025)
- [ ] Complete Auth → IDP migration
- [ ] Enhanced validation rules
- [ ] Performance optimization patterns
- [ ] Advanced error handling

#### **Phase 2: Enterprise Features** (Q2 2025)
- [ ] Audit trail enhancements
- [ ] Compliance automation
- [ ] Advanced ABAC policies
- [ ] Multi-region support

#### **Phase 3: Developer Experience** (Q3 2025)
- [ ] Interactive documentation
- [ ] Code examples repository
- [ ] SDK improvements
- [ ] Testing frameworks

#### **Phase 4: Scalability** (Q4 2025)
- [ ] Sharding strategies
- [ ] Caching patterns
- [ ] Performance benchmarks
- [ ] Load testing frameworks

---

## Support & Resources

### Getting Help

- **Issues**: https://github.com/geniustechspace/protobuf/issues
- **Discussions**: https://github.com/geniustechspace/protobuf/discussions
- **Documentation**: https://github.com/geniustechspace/protobuf/tree/main/docs

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Submitting issues
- Creating pull requests
- Code review process
- Documentation standards

### External Resources

- **Protocol Buffers**: https://protobuf.dev
- **gRPC**: https://grpc.io
- **Buf**: https://buf.build/docs
- **Protovalidate**: https://github.com/bufbuild/protovalidate

---

## License

See [LICENSE](LICENSE) file for details.

---

## Conclusion

This Protocol Buffer schema repository provides a **comprehensive, production-ready foundation** for building enterprise-grade, multi-tenant, event-driven microservices. 

### Key Strengths

✅ **Well-Organized**: Clear domain boundaries and file structure  
✅ **Scalable**: Designed for enterprise scale and complexity  
✅ **Multi-Tenant**: Built-in tenancy support throughout  
✅ **Event-Driven**: Comprehensive event catalog for async communication  
✅ **Multi-Language**: Support for 5+ programming languages  
✅ **Documented**: Extensive documentation for all domains  
✅ **Validated**: Automated linting and breaking change detection  
✅ **Modern**: Follows latest protobuf and gRPC best practices  

### Getting Started

1. **Clone the repository**
2. **Install Buf CLI**
3. **Run `buf generate`**
4. **Start building services**

See [QUICK_START.md](QUICK_START.md) for detailed setup instructions.

---

**Last Updated**: December 6, 2025  
**Version**: 1.0.0  
**Maintainer**: Genius Tech Space  
**Repository**: https://github.com/geniustechspace/protobuf
