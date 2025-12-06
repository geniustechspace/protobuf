# IDP (Identity Provider) - Version 1 - Modular Architecture

Enterprise-grade, modular identity and access management system with single-responsibility modules.

## 📋 Table of Contents

- [Architecture Overview](#architecture-overview)
- [Module Structure](#module-structure)
- [Migration Guide](#migration-guide)
- [Module Reference](#module-reference)
- [Design Principles](#design-principles)

## 🏗️ Architecture Overview

The IDP package is organized into **8 focused modules**, each responsible for a single domain:

```
proto/idp/v1/
├── auth/           # Core authentication (login, logout, credentials)
├── mfa/            # Multi-factor authentication enrollment
├── token/          # OAuth 2.0 token lifecycle
├── session/        # Session management and monitoring
├── password/       # Password reset and change
├── webauthn/       # FIDO2/WebAuthn credentials
├── security/       # Security policies and risk assessment
└── audit/          # Compliance audit logging
```

### Design Principles

1. **Single Responsibility**: Each module handles ONE domain
2. **Flat Structure**: messages.proto, enums.proto, types.proto, service.proto per module
3. **Self-Contained**: Modules can be used independently
4. **Cross-Module References**: Import from other modules only when needed
5. **Consistent Naming**: Package = `idp.v1.{module}`

## 📁 Module Structure

Each module follows a consistent pattern:

```
{module}/
├── enums.proto      # Module-specific enumerations
├── types.proto      # Complex data types (optional)
├── messages.proto   # Request/Response messages
└── service.proto    # gRPC service definition
```

### Package Naming Convention

- **Old**: `package geniustechspace.idp.v1;`
- **New**: `package geniustechspace.idp.v1.{module};`

Examples:
- `idp.v1.auth` - Authentication module
- `idp.v1.mfa` - MFA module
- `idp.v1.token` - Token module

### Generated Code Paths

**Go:**
```go
import authv1 "github.com/geniustechspace/protobuf/gen/go/idp/v1/auth"
import mfav1 "github.com/geniustechspace/protobuf/gen/go/idp/v1/mfa"
import tokenv1 "github.com/geniustechspace/protobuf/gen/go/idp/v1/token"
```

**Java:**
```java
import com.geniustechspace.protobuf.idp.v1.auth.*;
import com.geniustechspace.protobuf.idp.v1.mfa.*;
import com.geniustechspace.protobuf.idp.v1.token.*;
```

**C#:**
```csharp
using GeniusTechSpace.Protobuf.Idp.V1.Auth;
using GeniusTechSpace.Protobuf.Idp.V1.Mfa;
using GeniusTechSpace.Protobuf.Idp.V1.Token;
```

## 🔄 Migration Guide

### Old Structure (Deprecated)

```
proto/idp/v1/
├── enums.proto              # All enums in one file
├── authentication.proto     # Auth messages mixed with others
├── tokens.proto             # Token messages
├── session.proto            # Session messages
├── password.proto           # Password messages
├── mfa.proto                # MFA messages
├── webauthn.proto           # WebAuthn messages
├── security.proto           # Security messages
├── audit.proto              # Audit messages
└── services.proto           # Monolithic service (45+ RPCs)
```

### New Structure (Recommended)

```
proto/idp/v1/
├── auth/
│   ├── enums.proto          # AuthenticationStatus, BiometricType, SocialProvider
│   ├── types.proto          # WebAuthnAssertion, BiometricAssertion, ClientCertificate
│   ├── messages.proto       # Start/Authentication/Logout Request/Response
│   └── service.proto        # AuthenticationService (3 RPCs)
├── mfa/
│   ├── enums.proto          # MFAFactorType, MFAFactorStatus
│   ├── types.proto          # MFAFactor
│   ├── messages.proto       # Begin/Confirm Enrollment, List/Remove/Set Factor, Backup Codes
│   └── service.proto        # MFAService (10 RPCs)
├── token/
│   ├── enums.proto          # TokenType (if needed)
│   ├── messages.proto       # AuthTokenSet, List/Refresh/Revoke/Introspect
│   └── service.proto        # TokenService (5 RPCs)
├── session/
│   ├── messages.proto       # List/Revoke/RevokeAll Sessions
│   └── service.proto        # SessionService (3 RPCs)
├── password/
│   ├── messages.proto       # Reset/ConfirmReset/Change Password
│   └── service.proto        # PasswordService (3 RPCs)
├── webauthn/
│   ├── enums.proto          # AuthenticatorAttachment, UserVerification
│   ├── types.proto          # WebAuthnCredential
│   ├── messages.proto       # Begin/Complete Registration/Authentication, Credential CRUD
│   └── service.proto        # WebAuthnService (7 RPCs)
├── security/
│   ├── enums.proto          # RiskLevel, PasswordStrengthLevel
│   ├── messages.proto       # Policies, RateLimit, Lockout, Risk Assessment
│   └── service.proto        # SecurityService (7 RPCs)
└── audit/
    ├── enums.proto          # AuditCategory, AuditSeverity, AuditResult
    ├── messages.proto       # AuditEvent, Specialized Events, Query
    └── service.proto        # AuditService (3 RPCs)
```

### Import Changes

**Old:**
```protobuf
import "proto/idp/v1/enums.proto";
import "proto/idp/v1/authentication.proto";
import "proto/idp/v1/tokens.proto";
```

**New:**
```protobuf
import "proto/idp/v1/auth/enums.proto";
import "proto/idp/v1/auth/messages.proto";
import "proto/idp/v1/token/messages.proto";
```

### Message Reference Changes

**Old:**
```protobuf
package myapp.v1;
import "proto/idp/v1/authentication.proto";

message UserLogin {
  idp.v1.AuthenticationRequest auth_request = 1;  // Old package
}
```

**New:**
```protobuf
package myapp.v1;
import "proto/idp/v1/auth/messages.proto";

message UserLogin {
  idp.v1.auth.AuthenticationRequest auth_request = 1;  // New package
}
```

## 📚 Module Reference

### 1. Auth Module (`idp.v1.auth`)

**Responsibility:** Core authentication (login, logout, credential validation)

**Files:**
- `enums.proto`: AuthenticationStatus, BiometricType, SocialProvider
- `types.proto`: WebAuthnAssertion, BiometricAssertion, ClientCertificate
- `messages.proto`: StartAuthenticationRequest/Response, AuthenticationRequest/Response, LogoutRequest/Response
- `service.proto`: AuthenticationService

**Key Messages:**
- `StartAuthenticationRequest` - Passwordless flow initiation
- `AuthenticationRequest` - Primary authentication (15+ methods)
- `AuthenticationResponse` - Unified response (SUCCESS, MFA_REQUIRED, FAILED)
- `LogoutRequest/Response` - Session termination

**Service RPCs:**
- `StartAuthentication(StartAuthenticationRequest) → AuthenticationResponse`
- `Authentication(AuthenticationRequest) → AuthenticationResponse`
- `Logout(LogoutRequest) → LogoutResponse`

**Supported Credentials:**
- Password, OTP, TOTP, Magic Link
- Social (OAuth 2.0), SAML 2.0
- WebAuthn/FIDO2, Biometric
- Client Certificate (mTLS), Backup Code

---

### 2. MFA Module (`idp.v1.mfa`)

**Responsibility:** Multi-factor authentication enrollment and management

**Files:**
- `enums.proto`: MFAFactorType, MFAFactorStatus
- `types.proto`: MFAFactor
- `messages.proto`: Begin/Confirm enrollment for TOTP/SMS/Email, Factor management, Backup codes
- `service.proto`: MFAService

**Key Messages:**
- `BeginTOTPEnrollmentRequest/Response` - Start TOTP setup (QR code, secret)
- `ConfirmTOTPEnrollmentRequest/Response` - Verify TOTP code
- `Begin/ConfirmSMSEnrollmentRequest/Response` - SMS OTP setup
- `Begin/ConfirmEmailEnrollmentRequest/Response` - Email OTP setup
- `ListMFAFactorsRequest/Response` - View enrolled factors
- `RemoveMFAFactorRequest/Response` - Remove factor
- `SetPrimaryMFAFactorRequest/Response` - Set default factor
- `GenerateBackupCodesRequest/Response` - Create recovery codes

**Service RPCs:** 10 RPCs for complete MFA lifecycle

---

### 3. Token Module (`idp.v1.token`)

**Responsibility:** OAuth 2.0 token lifecycle (refresh, revoke, introspect)

**Files:**
- `enums.proto`: TokenType (if needed)
- `messages.proto`: AuthTokenSet, List/Refresh/Revoke/Introspect tokens
- `service.proto`: TokenService

**Key Messages:**
- `AuthTokenSet` - Token bundle (access, refresh, ID token)
- `RefreshTokenRequest/Response` - Token refresh
- `RevokeTokenRequest/Response` - Single token revocation
- `RevokeAllTokensRequest/Response` - Bulk revocation
- `ListTokensRequest/Response` - View active tokens
- `IntrospectTokenRequest/Response` - Token validation (RFC 7662)

**Service RPCs:**
- `RefreshToken` - Exchange refresh token for new access token
- `RevokeToken` - Revoke specific token
- `RevokeAllTokens` - Bulk revocation (sign out everywhere)
- `ListTokens` - View user's active tokens
- `IntrospectToken` - Validate token (RFC 7662)

---

### 4. Session Module (`idp.v1.session`)

**Responsibility:** Session lifecycle and monitoring

**Files:**
- `messages.proto`: List/Revoke/RevokeAll sessions
- `service.proto`: SessionService

**Key Messages:**
- `ListSessionsRequest/Response` - View user's sessions
- `RevokeSessionRequest/Response` - Terminate specific session
- `RevokeAllSessionsRequest/Response` - Bulk termination

**Service RPCs:**
- `ListSessions` - View active sessions
- `RevokeSession` - Terminate specific session
- `RevokeAllSessions` - Sign out everywhere

---

### 5. Password Module (`idp.v1.password`)

**Responsibility:** Password reset and change

**Files:**
- `messages.proto`: Reset/ConfirmReset/Change password
- `service.proto`: PasswordService

**Key Messages:**
- `ResetPasswordRequest/Response` - Initiate reset (sends email)
- `ConfirmPasswordResetRequest/Response` - Complete reset with token
- `ChangePasswordRequest/Response` - Change password (authenticated)

**Service RPCs:**
- `ResetPassword` - Initiate reset flow
- `ConfirmPasswordReset` - Complete reset with token
- `ChangePassword` - Change password (requires old password)

---

### 6. WebAuthn Module (`idp.v1.webauthn`)

**Responsibility:** FIDO2/WebAuthn credential management

**Files:**
- `enums.proto`: WebAuthnAuthenticatorAttachment, WebAuthnUserVerification
- `types.proto`: WebAuthnCredential
- `messages.proto`: Begin/Complete Registration/Authentication, Credential CRUD
- `service.proto`: WebAuthnService

**Key Messages:**
- `Begin/CompleteWebAuthnRegistrationRequest/Response` - Credential registration
- `Begin/CompleteWebAuthnAuthenticationRequest/Response` - Authentication ceremony
- `ListWebAuthnCredentialsRequest/Response` - View registered credentials
- `Delete/UpdateWebAuthnCredentialRequest/Response` - Credential management

**Service RPCs:** 7 RPCs for complete WebAuthn lifecycle

---

### 7. Security Module (`idp.v1.security`)

**Responsibility:** Security policies, risk assessment, account lockout

**Files:**
- `enums.proto`: RiskLevel, PasswordStrengthLevel
- `messages.proto`: Password/RateLimit/Lockout policies, Risk assessment
- `service.proto`: SecurityService

**Key Messages:**
- `GetPasswordPolicyRequest/Response` - Retrieve password requirements
- `UpdatePasswordPolicyRequest/Response` - Update policy (admin)
- `CheckPasswordStrengthRequest/Response` - Real-time validation
- `GetRateLimitStatusRequest/Response` - Check rate limit
- `Get/UnlockAccountLockoutRequest/Response` - Account lockout management
- `AssessRiskRequest/Response` - Risk-based authentication

**Service RPCs:**
- Password policy management (Get/Update/Check)
- Rate limit status
- Account lockout (Get/Unlock)
- Risk assessment

---

### 8. Audit Module (`idp.v1.audit`)

**Responsibility:** Compliance audit logging and querying

**Files:**
- `enums.proto`: AuditCategory, AuditSeverity, AuditResult
- `messages.proto`: AuditEvent, Specialized events, Query API
- `service.proto`: AuditService

**Key Messages:**
- `AuditEvent` - Base audit event (10 categories, 8 severity levels)
- `AuthenticationAuditEvent`, `SessionAuditEvent`, etc. - Specialized events
- `AuditEventQuery/Response` - Advanced filtering and search
- `LogAuditEventRequest/Response` - Create log entry

**Service RPCs:**
- `LogAuditEvent` - Create audit log entry (internal)
- `QueryAuditEvents` - Search audit logs (advanced filtering)
- `GetAuditEvent` - Retrieve single event by ID

**Event Categories:** Authentication, Session, Token, Account, Security, Access Control, Data Access, Compliance, System, Error

---

## 🎯 Benefits of Modular Structure

### 1. **Clear Separation of Concerns**
Each module has a single, well-defined responsibility. No confusion about where functionality belongs.

### 2. **Independent Evolution**
Modules can evolve independently without affecting others. Change MFA enrollment without touching authentication.

### 3. **Easier Testing**
Test each module in isolation. Focused test suites per module.

### 4. **Better Documentation**
Module-specific documentation is more discoverable and maintainable.

### 5. **Selective Imports**
Import only what you need. Don't pollute namespace with unused types.

**Old (Monolithic):**
```protobuf
import "proto/idp/v1/enums.proto";  // Gets ALL enums (50+ types)
```

**New (Modular):**
```protobuf
import "proto/idp/v1/auth/enums.proto";  // Gets only auth enums (3 types)
```

### 6. **Team Ownership**
Different teams can own different modules:
- **Auth Team** → auth/
- **Security Team** → security/ + audit/
- **Product Team** → mfa/ + password/

### 7. **Microservice Alignment**
Each module can map to a microservice if needed:
- `auth-service` implements `auth/service.proto`
- `mfa-service` implements `mfa/service.proto`
- `token-service` implements `token/service.proto`

## 🚀 Getting Started

### Option 1: Use New Modular Structure (Recommended)

```protobuf
syntax = "proto3";

package myapp.v1;

// Import only what you need
import "proto/idp/v1/auth/messages.proto";
import "proto/idp/v1/mfa/messages.proto";

message LoginFlow {
  idp.v1.auth.AuthenticationRequest auth = 1;
  idp.v1.mfa.VerifyMFARequest mfa = 2;
}
```

### Option 2: Use Legacy Files (Deprecated)

Legacy files still available for backward compatibility:
- `proto/idp/v1/authentication.proto`
- `proto/idp/v1/tokens.proto`
- `proto/idp/v1/services.proto`
- etc.

**⚠️ Warning:** Legacy files are deprecated and will be removed in v2.

## 📊 Module Comparison

| Module | Files | Messages | Enums | Services | RPCs |
|--------|-------|----------|-------|----------|------|
| **auth** | 4 | 6 | 3 | 1 | 3 |
| **mfa** | 4 | 18 | 2 | 1 | 10 |
| **token** | 3 | 10 | 1 | 1 | 5 |
| **session** | 2 | 6 | 0 | 1 | 3 |
| **password** | 2 | 6 | 0 | 1 | 3 |
| **webauthn** | 4 | 14 | 2 | 1 | 7 |
| **security** | 3 | 12 | 2 | 1 | 7 |
| **audit** | 3 | 20+ | 4 | 1 | 3 |
| **TOTAL** | **25** | **92+** | **14+** | **8** | **41** |

## 📝 Additional Resources

- [Enterprise Standards](../../../docs/ENTERPRISE_COMPLIANCE.md)
- [Proto Documentation Standard](../../../docs/PROTO_DOCUMENTATION_STANDARD.md)
- [Validation Guide](../../../docs/VALIDATION.md)
- [Client Generation](../../../docs/CLIENT_GENERATION.md)

## 🤝 Contributing

See [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## 📄 License

See [LICENSE](../../../../LICENSE)
