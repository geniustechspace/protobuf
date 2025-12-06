# IDP (Identity Provider) - Version 1

Enterprise-grade, modular identity and access management system following single-responsibility principle.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Services](#services)
- [Compliance](#compliance)
- [Security](#security)
- [Getting Started](#getting-started)

## 🎯 Overview

This IDP package provides comprehensive authentication, authorization, and session management for multi-tenant SaaS platforms. It supports 15+ authentication methods including passwordless flows, social login, enterprise SSO, and hardware security keys.

**Key Features:**
- ✅ 15+ authentication methods (password, OTP, TOTP, social, SAML, WebAuthn, biometric, mTLS)
- ✅ Multi-factor authentication (TOTP, SMS, Email, WebAuthn, Push, Backup codes)
- ✅ Session management with device/client binding
- ✅ OAuth 2.0 / OpenID Connect compliant
- ✅ WebAuthn Level 2 / FIDO2 support
- ✅ Enterprise security policies (password, rate limiting, account lockout)
- ✅ Risk-based authentication
- ✅ Comprehensive audit logging (SOC 2, PCI DSS, HIPAA compliant)
- ✅ Multi-tenant isolation

## 🏗️ Architecture

### Design Principles

1. **Single Responsibility**: Each service has one clear purpose
2. **Flat Design**: No nested wrappers (1-2 nesting max)
3. **Reference by ID**: Context objects (device, client, network, geo) referenced by ID only
4. **Stateless Operations**: Services are stateless where possible
5. **Enterprise Standards**: Full compliance with industry standards

### Package Structure

```
proto/idp/v1/
├── services/              # Service definitions (8 focused services)
│   ├── auth_service.proto         # Core authentication
│   ├── token_service.proto        # Token lifecycle
│   ├── session_service.proto      # Session management
│   ├── password_service.proto     # Password operations
│   ├── webauthn_service.proto     # FIDO2/WebAuthn
│   ├── mfa_service.proto          # MFA enrollment
│   ├── security_service.proto     # Security policies
│   └── audit_service.proto        # Audit logging
│
├── messages/              # Request/Response messages
│   ├── authentication.proto       # Auth requests/responses
│   ├── tokens.proto               # Token messages
│   ├── session.proto              # Session messages
│   ├── password.proto             # Password messages
│   ├── webauthn.proto             # WebAuthn messages
│   ├── mfa.proto                  # MFA messages
│   ├── security.proto             # Security policy messages
│   └── audit.proto                # Audit event messages
│
├── enums.proto            # Shared enumerations
└── services.proto         # Legacy monolithic service (deprecated)
```

## 🔧 Services

### 1. AuthenticationService (`auth_service.proto`)

**Responsibility:** Core authentication flows (login, MFA, logout)

**RPCs:**
- `StartAuthentication` - Initiates passwordless flows (magic links, WebAuthn)
- `Authentication` - Primary authentication with credentials (15+ methods)
- `VerifyMFA` - Second-factor verification
- `Logout` - Session termination

**Use Cases:**
- User login (password, social, SAML, WebAuthn)
- Passwordless authentication (magic links)
- Multi-factor authentication flows
- User logout

**Rate Limits:**
- StartAuthentication: 10/min per IP
- Authentication: 5/min per IP, 10/min per user
- VerifyMFA: 3/5min per session
- Logout: 10/min per session

---

### 2. TokenService (`token_service.proto`)

**Responsibility:** OAuth 2.0 token lifecycle management

**RPCs:**
- `RefreshToken` - Exchange refresh token for new access token
- `RevokeToken` - Revoke specific token
- `RevokeAllTokens` - Bulk revocation (security incident, sign out everywhere)
- `ListTokens` - View active tokens
- `IntrospectToken` - Validate token (RFC 7662)

**Use Cases:**
- Token refresh (maintain session)
- Security incident response (revoke all tokens)
- "Active sessions" UI (list tokens)
- Resource server token validation

**Rate Limits:**
- RefreshToken: 10/min per token
- IntrospectToken: 100/min per client
- RevokeToken: 20/min per user
- ListTokens: 10/min per user

---

### 3. SessionService (`session_service.proto`)

**Responsibility:** Session lifecycle and monitoring

**RPCs:**
- `ListSessions` - View user's active sessions
- `RevokeSession` - Terminate specific session
- `RevokeAllSessions` - Bulk termination (sign out everywhere)

**Use Cases:**
- "Where you're logged in" UI
- Security incident (terminate suspicious session)
- Password change (force re-authentication)
- Device lost (revoke all sessions from device)

**Rate Limits:**
- ListSessions: 10/min per user
- RevokeSession: 20/min per user
- RevokeAllSessions: 5/min per user

---

### 4. PasswordService (`password_service.proto`)

**Responsibility:** Password management (reset, change)

**RPCs:**
- `ResetPassword` - Initiate password reset (sends email)
- `ConfirmPasswordReset` - Complete reset with token
- `ChangePassword` - Change password (requires old password)

**Use Cases:**
- Forgot password flow
- User changes password in settings
- Admin forces password change
- Password strength validation

**Rate Limits:**
- ResetPassword: 3/hour per email
- ConfirmPasswordReset: 5/hour per token
- ChangePassword: 10/hour per user

---

### 5. WebAuthnService (`webauthn_service.proto`)

**Responsibility:** FIDO2/WebAuthn credential management

**RPCs:**
- `BeginWebAuthnRegistration` - Start credential registration
- `CompleteWebAuthnRegistration` - Finish registration
- `BeginWebAuthnAuthentication` - Start authentication
- `CompleteWebAuthnAuthentication` - Finish authentication
- `ListWebAuthnCredentials` - View registered credentials
- `DeleteWebAuthnCredential` - Remove credential
- `UpdateWebAuthnCredential` - Update credential metadata

**Use Cases:**
- Register security key (YubiKey)
- Register platform authenticator (Touch ID, Windows Hello)
- Passwordless authentication
- Second-factor authentication
- Manage registered devices

**Rate Limits:**
- Begin*: 10/min per user
- Complete*: 5/min per user
- List/Delete/Update: 20/min per user

---

### 6. MFAService (`mfa_service.proto`)

**Responsibility:** Multi-factor authentication enrollment and management

**RPCs:**
- `BeginTOTPEnrollment` + `ConfirmTOTPEnrollment` - TOTP setup
- `BeginSMSEnrollment` + `ConfirmSMSEnrollment` - SMS OTP setup
- `BeginEmailEnrollment` + `ConfirmEmailEnrollment` - Email OTP setup
- `ListMFAFactors` - View enrolled factors
- `RemoveMFAFactor` - Remove factor
- `SetPrimaryMFAFactor` - Set default factor
- `GenerateBackupCodes` - Create recovery codes

**Use Cases:**
- User enables two-factor authentication
- Enroll authenticator app (Google Authenticator, Authy)
- Enroll SMS/Email as backup
- Generate backup codes
- Manage enrolled factors

**Rate Limits:**
- Begin*Enrollment: 5/hour per user
- Confirm*Enrollment: 10/hour per user
- ListMFAFactors: 20/min per user
- GenerateBackupCodes: 3/day per user

---

### 7. SecurityService (`security_service.proto`)

**Responsibility:** Security policy management and risk assessment

**RPCs:**
- `GetPasswordPolicy` + `UpdatePasswordPolicy` - Password requirements
- `CheckPasswordStrength` - Real-time validation
- `GetRateLimitStatus` - Check rate limit status
- `GetAccountLockoutStatus` + `UnlockAccount` - Account lockout
- `AssessRisk` - Risk-based authentication

**Use Cases:**
- Configure tenant password policy
- Real-time password strength meter
- Check if account is locked
- Admin unlocks account
- Risk assessment for adaptive auth

**Rate Limits:**
- GetPolicy: 100/min per tenant
- UpdatePolicy: 10/hour per admin
- Check/Assess: 100/min per user
- UnlockAccount: 10/hour per admin

---

### 8. AuditService (`audit_service.proto`)

**Responsibility:** Compliance audit logging and querying

**RPCs:**
- `LogAuditEvent` - Create audit log entry
- `QueryAuditEvents` - Search audit logs (advanced filtering)
- `GetAuditEvent` - Retrieve single event by ID

**Use Cases:**
- Internal service audit logging
- Compliance reporting (SOC 2, PCI DSS, HIPAA)
- Security incident investigation
- GDPR access requests
- Failed login analysis

**Rate Limits:**
- LogAuditEvent: 1000/min per service (internal)
- QueryAuditEvents: 10/min per user
- GetAuditEvent: 100/min per user

---

## ✅ Compliance

### Standards Coverage

- **OAuth 2.0** (RFC 6749): Authorization Framework
- **OpenID Connect Core 1.0**: Identity layer on OAuth 2.0
- **RFC 7519**: JSON Web Tokens (JWT)
- **RFC 7662**: Token Introspection
- **RFC 6238**: TOTP (Time-Based One-Time Password)
- **W3C WebAuthn Level 2**: Web Authentication API
- **FIDO2 CTAP2**: Client to Authenticator Protocol
- **NIST 800-63B**: Digital Identity Guidelines (AAL1-3)
- **OWASP Top 10**: Security controls implementation
- **PCI DSS 3.2.1**: Payment card industry security
- **GDPR**: General Data Protection Regulation
- **SOC 2 Type II**: Service Organization Controls
- **HIPAA**: Health Insurance Portability and Accountability Act
- **ISO 27001**: Information security management
- **PSD2**: Payment Services Directive (Strong Customer Authentication)

### Audit Requirements

All operations logged with:
- **10 event categories**: Authentication, Session, Token, Account, Security, Access Control, Data Access, Compliance, System, Error
- **8 severity levels**: DEBUG, INFO, NOTICE, WARNING, ERROR, CRITICAL, ALERT, EMERGENCY
- **Immutable logs**: Append-only with tamper detection
- **13+ month retention**: Configurable per compliance requirement
- **Query API**: Advanced filtering for compliance reports

## 🔒 Security

### Authentication Methods

1. **Password**: Bcrypt/Argon2 hashing, breach detection (HaveIBeenPwned)
2. **OTP**: One-time passwords (SMS/Email)
3. **TOTP**: RFC 6238 Time-based OTP (Google Authenticator, Authy)
4. **Magic Link**: Passwordless email/SMS link
5. **Social**: OAuth 2.0 (Google, GitHub, Microsoft, Facebook, Apple, etc.)
6. **SAML**: SAML 2.0 SSO (enterprise identity providers)
7. **WebAuthn**: FIDO2 security keys, Touch ID, Face ID, Windows Hello
8. **Biometric**: Fingerprint, Face, Iris (device-bound)
9. **Certificate**: X.509 mTLS (mutual TLS)
10. **API Key**: Service-to-service authentication
11. **Bearer Token**: OAuth 2.0 bearer tokens
12. **Refresh Token**: Token refresh flow
13. **Session**: Existing session validation
14. **Anonymous**: Guest/anonymous access
15. **Backup Code**: Recovery codes (MFA bypass)

### MFA Factors

1. **TOTP**: Authenticator apps (30-second codes)
2. **SMS**: Text message OTP
3. **Email**: Email OTP
4. **WebAuthn**: Security keys (YubiKey, Titan)
5. **Biometric**: Touch ID, Face ID, Windows Hello
6. **Push**: Mobile app approval (push notifications)
7. **Backup Codes**: Single-use recovery codes

### Security Controls

- **Rate Limiting**: Exponential backoff, per-user/IP/operation
- **Account Lockout**: Progressive lockout after failed attempts
- **Password Policies**: NIST 800-63B compliant (min length, complexity, history, breach check)
- **Risk Assessment**: Real-time risk scoring (device/location/pattern anomalies)
- **Session Binding**: Device, client, network, geo context verification
- **Token Security**: Short-lived access tokens (15min), refresh token rotation
- **Audit Logging**: All operations logged with immutable trail
- **TLS 1.3+**: Required for all transport (no exceptions)
- **Input Validation**: buf/validate constraints on all fields
- **No Sensitive Data in Logs**: Passwords, tokens, PII masked

### Privacy

- **GDPR Compliance**: Right to erasure, data minimization, consent tracking
- **PII Protection**: Email, phone, username encrypted at rest
- **Data Retention**: Configurable per tenant (90 days default)
- **User Deletion**: Cascading deletion (sessions, tokens, audit logs)
- **Explicit Consent**: Biometric data requires GDPR Article 9 consent

## 🚀 Getting Started

### Client Integration

#### 1. Simple Password Authentication

```protobuf
// Request
AuthenticationRequest {
  tenant_id: "tenant-123"
  email: "user@example.com"
  password: "SecureP@ssw0rd"
}

// Response (Success)
AuthenticationResponse {
  status: SUCCESS
  user_id: "user-456"
  tokens: {
    access_token: "eyJhbGciOiJIUzI1NiIs..."
    refresh_token: "rt_abc123..."
    token_type: BEARER
    expires_in: 900  // 15 minutes
  }
  session: {
    session_id: "sess-789"
    // ... session details
  }
}
```

#### 2. MFA Authentication Flow

```protobuf
// Step 1: Primary authentication
AuthenticationRequest {
  tenant_id: "tenant-123"
  email: "user@example.com"
  password: "SecureP@ssw0rd"
}

// Response: MFA Required
AuthenticationResponse {
  status: MFA_REQUIRED
  user_id: "user-456"
  session: {
    session_id: "temp-mfa-session-789"  // Temporary MFA session
    auth_status: AUTH_STATUS_PARTIAL
    required_mfa_methods: [MFA_TYPE_TOTP]
  }
  message: "Multi-factor authentication required"
}

// Step 2: Verify MFA
VerifyMFARequest {
  tenant_id: "tenant-123"
  session_id: "temp-mfa-session-789"
  totp_code: "123456"
}

// Response: Success (same structure as AuthenticationResponse)
AuthenticationResponse {
  status: SUCCESS
  user_id: "user-456"
  tokens: { ... }  // Full tokens granted
  session: {
    session_id: "sess-890"  // Upgraded to full session
    auth_status: AUTH_STATUS_AUTHENTICATED
    completed_mfa_methods: [MFA_TYPE_TOTP]
  }
}
```

#### 3. Passwordless WebAuthn

```protobuf
// Step 1: Start authentication
StartAuthenticationRequest {
  tenant_id: "tenant-123"
  email: "user@example.com"
}

// Response: Challenge for WebAuthn
AuthenticationResponse {
  status: MFA_REQUIRED  // Or custom status
  session: {
    session_id: "webauthn-challenge-123"
  }
  // Challenge data in metadata or custom field
}

// Step 2: Complete WebAuthn (client signs challenge)
AuthenticationRequest {
  tenant_id: "tenant-123"
  session_id: "webauthn-challenge-123"
  webauthn: {
    credential_id: "cred-abc"
    authenticator_data: "..."
    client_data_json: "..."
    signature: "..."
  }
}

// Response: Success
AuthenticationResponse {
  status: SUCCESS
  tokens: { ... }
  session: { ... }
}
```

### Service Selection Guide

| **Use Case** | **Service** | **RPC** |
|--------------|-------------|---------|
| User login | `AuthenticationService` | `Authentication` |
| Passwordless login | `AuthenticationService` | `StartAuthentication` + `Authentication` |
| MFA verification | `AuthenticationService` | `VerifyMFA` |
| User logout | `AuthenticationService` | `Logout` |
| Token refresh | `TokenService` | `RefreshToken` |
| Revoke token | `TokenService` | `RevokeToken` |
| Sign out everywhere | `TokenService` | `RevokeAllTokens` |
| View active sessions | `SessionService` | `ListSessions` |
| Remove session | `SessionService` | `RevokeSession` |
| Forgot password | `PasswordService` | `ResetPassword` + `ConfirmPasswordReset` |
| Change password | `PasswordService` | `ChangePassword` |
| Register security key | `WebAuthnService` | `Begin/CompleteWebAuthnRegistration` |
| Enable 2FA | `MFAService` | `Begin/ConfirmTOTPEnrollment` |
| Generate backup codes | `MFAService` | `GenerateBackupCodes` |
| Check password strength | `SecurityService` | `CheckPasswordStrength` |
| Assess auth risk | `SecurityService` | `AssessRisk` |
| Query audit logs | `AuditService` | `QueryAuditEvents` |

### Migration from Monolithic Service

The original `IdentityService` in `services.proto` is deprecated. Migrate to focused services:

```protobuf
// OLD (deprecated)
service IdentityService {
  rpc Authenticate(...) returns (...);
  rpc RefreshToken(...) returns (...);
  rpc ListSessions(...) returns (...);
  // ... 45+ RPCs in one service
}

// NEW (recommended)
service AuthenticationService { ... }  // 4 RPCs
service TokenService { ... }           // 5 RPCs
service SessionService { ... }         // 3 RPCs
service PasswordService { ... }        // 3 RPCs
service WebAuthnService { ... }        // 7 RPCs
service MFAService { ... }             // 10 RPCs
service SecurityService { ... }        // 7 RPCs
service AuditService { ... }           // 3 RPCs
```

**Benefits:**
- ✅ Single responsibility (easier to maintain)
- ✅ Independent scaling (scale auth separately from audit)
- ✅ Clear ownership (different teams own different services)
- ✅ Better testing (focused test suites)
- ✅ Smaller API surface (clients import only what they need)

---

## 📚 Additional Resources

- [Enterprise Standards Documentation](../../docs/ENTERPRISE_COMPLIANCE.md)
- [Proto Documentation Standard](../../docs/PROTO_DOCUMENTATION_STANDARD.md)
- [Validation Guide](../../docs/VALIDATION.md)
- [Client Generation](../../docs/CLIENT_GENERATION.md)

---

## 🤝 Contributing

See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for contribution guidelines.

## 📄 License

See [LICENSE](../../../LICENSE) for license information.
