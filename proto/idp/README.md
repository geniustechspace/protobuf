# Identity Provider (IDP) Module

Enterprise-grade identity provider protocol definitions for multi-tenant authentication, authorization, and identity management.

## Package

```protobuf
package geniustechspace.idp.*.v1;
```

## Overview

The IDP module provides comprehensive protocol definitions for building modern identity providers with:

- **Authentication (authn)** - Multi-method authentication (password, passwordless, WebAuthn, MFA)
- **Authorization (authz)** - RBAC, ABAC, permissions, policies, access control
- **Identity Management** - User profiles, identity lifecycle, verification
- **Audit Logging** - Compliance-ready audit trails (SOC 2, PCI DSS, GDPR)
- **Connectors** - External identity providers (LDAP, SAML, OAuth, social)
- **Protocols** - Standard protocols (OAuth 2.0, OIDC, SAML 2.0)
- **Provisioning** - SCIM-based user provisioning and directory sync
- **Webhooks** - Event-driven integrations
- **API** - Unified API definitions and common types

## Module Structure

```text
proto/idp/
├── README.md                    # This file
├── api/v1/                      # Unified API and common types
│   ├── common.proto            # Shared IDP types
│   ├── enums.proto             # Shared IDP enums
│   └── README.md
├── authn/v1/                   # Authentication
│   ├── messages.proto          # Auth requests/responses
│   ├── enums.proto             # Auth methods, statuses
│   ├── password.proto          # Password authentication
│   ├── webauthn.proto          # WebAuthn/FIDO2
│   ├── mfa.proto               # Multi-factor authentication
│   ├── session.proto           # Session management
│   ├── token.proto             # Token management
│   ├── service.proto           # Authentication service
│   └── README.md
├── authz/v1/                   # Authorization
│   ├── messages.proto          # Authz requests/responses
│   ├── enums.proto             # Permission types, scopes
│   ├── rbac.proto              # Role-Based Access Control
│   ├── abac.proto              # Attribute-Based Access Control
│   ├── policy.proto            # Authorization policies
│   ├── service.proto           # Authorization service
│   └── README.md
├── identity/v1/                # Identity Management
│   ├── messages.proto          # Identity requests/responses
│   ├── enums.proto             # Identity types, states
│   ├── user.proto              # User profiles
│   ├── verification.proto      # Identity verification
│   ├── service.proto           # Identity service
│   └── README.md
├── audit/v1/                   # Audit Logging
│   ├── messages.proto          # Audit events
│   ├── enums.proto             # Event types, categories
│   ├── service.proto           # Audit service
│   └── README.md
├── connectors/v1/              # External Connectors
│   ├── messages.proto          # Connector requests/responses
│   ├── enums.proto             # Connector types
│   ├── ldap.proto              # LDAP/Active Directory
│   ├── saml.proto              # SAML 2.0
│   ├── oauth.proto             # OAuth 2.0 providers
│   ├── social.proto            # Social login providers
│   ├── service.proto           # Connector service
│   └── README.md
├── protocols/v1/               # Standard Protocols
│   ├── messages.proto          # Protocol messages
│   ├── enums.proto             # Protocol types
│   ├── oauth2.proto            # OAuth 2.0
│   ├── oidc.proto              # OpenID Connect
│   ├── saml2.proto             # SAML 2.0
│   ├── service.proto           # Protocol service
│   └── README.md
├── provisioning/v1/            # User Provisioning
│   ├── messages.proto          # Provisioning requests/responses
│   ├── enums.proto             # Provisioning types
│   ├── scim.proto              # SCIM 2.0
│   ├── service.proto           # Provisioning service
│   └── README.md
└── webhook/v1/                 # Webhooks
    ├── messages.proto          # Webhook events
    ├── enums.proto             # Event types
    ├── service.proto           # Webhook service
    └── README.md
```

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
```

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

## Migration from deprecated/idp/v1

The new modular structure separates concerns:

- `deprecated/idp/v1/authentication.proto` → `proto/idp/authn/v1/`
- `deprecated/idp/v1/audit.proto` → `proto/idp/audit/v1/`
- Authorization moved to separate `proto/idp/authz/v1/`
- Identity management in `proto/idp/identity/v1/`

See individual module READMEs for migration guides.

## Related Modules

- [Core](../core/README.md) - Common value objects (session, device, network)
- [Users](../users/README.md) - User account management
- [Tenants](../tenants/README.md) - Multi-tenancy

## Documentation

- [Enterprise Compliance](../../docs/ENTERPRISE_COMPLIANCE.md)
- [Validation Standards](../../docs/VALIDATION.md)
- [Proto Documentation Standard](../../docs/PROTO_DOCUMENTATION_STANDARD.md)
