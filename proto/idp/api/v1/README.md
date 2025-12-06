# IDP API - Common Types

Common types, enumerations, and value objects shared across all IDP modules.

## Package

```protobuf
package geniustechspace.idp.api.v1;
```

## Overview

The API module provides shared definitions used across authentication, authorization, identity, and audit modules including:

- **Enumerations** - Authentication status, methods, MFA types, risk levels, token types
- **AuthContext** - Authentication context for requests
- **Principal** - Authenticated entity (user or service account)
- **Credential** - Credential metadata (NOT actual secrets)
- **PolicyViolation** - Policy constraint violations

## Files

- `enums.proto` - Shared enumerations
- `common.proto` - Common types and value objects

## Key Enumerations

### AuthenticationStatus

Authentication result states:
- `SUCCESS`, `MFA_REQUIRED`, `STEP_UP_REQUIRED`, `FAILED`
- `RATE_LIMITED`, `ACCOUNT_LOCKED`, `EXPIRED`
- `INVALID_CREDENTIALS`, `ACCOUNT_DISABLED`, `ACCOUNT_SUSPENDED`
- `PASSWORD_RESET_REQUIRED`, `TERMS_ACCEPTANCE_REQUIRED`

### AuthenticationMethod

Authentication mechanisms (15 types):
- `PASSWORD`, `PASSWORDLESS_EMAIL`, `PASSWORDLESS_SMS`
- `WEBAUTHN`, `BIOMETRIC`, `SOCIAL`
- `SAML`, `OAUTH`, `LDAP`, `CERTIFICATE`
- `OTP`, `PUSH_NOTIFICATION`, `QR_CODE`
- `API_KEY`, `SERVICE_ACCOUNT`

### MFAType

Multi-factor authentication types (8 types):
- `TOTP` (Google Authenticator, Authy)
- `SMS`, `EMAIL`, `VOICE_CALL`
- `WEBAUTHN`, `BIOMETRIC`, `PUSH_NOTIFICATION`
- `BACKUP_CODE`

### RiskLevel

Risk assessment levels:
- `LOW` - Known device, location, behavior
- `MEDIUM` - Some anomalies detected
- `HIGH` - Significant anomalies (new device, location)
- `CRITICAL` - Multiple red flags (impossible travel, bot)

### TokenType

Token purpose and scope:
- `ACCESS_TOKEN`, `REFRESH_TOKEN`, `ID_TOKEN`
- `SESSION_TOKEN`, `API_KEY`, `AUTHORIZATION_CODE`
- `DEVICE_CODE`, `PASSWORD_RESET_TOKEN`
- `EMAIL_VERIFICATION_TOKEN`, `MFA_TOKEN`, `MAGIC_LINK_TOKEN`

### SessionState

Session lifecycle states:
- `ACTIVE`, `IDLE`, `MFA_PENDING`, `STEP_UP_PENDING`
- `EXPIRED`, `REVOKED`, `TERMINATED`

## Key Messages

### AuthContext

Authentication context for requests:

```protobuf
message AuthContext {
  string tenant_id = 1;
  string user_id = 2;
  string session_id = 3;
  string token_id = 4;
  AuthenticationMethod auth_method = 5;
  google.protobuf.Timestamp authenticated_at = 6;
  bool mfa_verified = 7;
  MFAType mfa_method = 8;
  repeated string scopes = 9;
  string ip_address = 10;
}
```

### Principal

Authenticated entity (user or service account):

```protobuf
message Principal {
  string id = 1;
  PrincipalType type = 2;
  string display_name = 3;
  string email = 4;
  string tenant_id = 5;
  repeated string roles = 6;
  repeated string groups = 7;
  core.metadata.v1.Metadata metadata = 8;
}
```

### Credential

Credential metadata (NOT the credential itself):

```protobuf
message Credential {
  string id = 1;
  CredentialType type = 2;
  string user_id = 3;
  string tenant_id = 4;
  string display_name = 5;
  CredentialStatus status = 6;
  google.protobuf.Timestamp created_at = 7;
  google.protobuf.Timestamp last_used_at = 8;
  google.protobuf.Timestamp expires_at = 9;
  bool verified = 10;
  google.protobuf.Timestamp verified_at = 11;
  bool primary = 12;
  map<string, string> metadata = 13;
}
```

## Usage Examples

### Authentication Context

```protobuf
import "idp/api/v1/common.proto";

AuthContext auth_ctx = {
  tenant_id: "tenant_123",
  user_id: "user_456",
  session_id: "session_789",
  auth_method: PASSWORD,
  authenticated_at: now(),
  mfa_verified: true,
  mfa_method: TOTP,
  scopes: ["read:profile", "write:documents"],
  ip_address: "203.0.113.42"
};
```

### Principal

```protobuf
Principal principal = {
  id: "user_456",
  type: USER,
  display_name: "John Smith",
  email: "jsmith@example.com",
  tenant_id: "tenant_123",
  roles: ["admin", "editor"],
  groups: ["engineering", "leadership"]
};
```

### Credential Metadata

```protobuf
Credential cred = {
  id: "cred_789",
  type: WEBAUTHN,
  user_id: "user_456",
  tenant_id: "tenant_123",
  display_name: "YubiKey 5C",
  status: ACTIVE,
  created_at: timestamp("2024-01-15T10:00:00Z"),
  last_used_at: timestamp("2024-12-06T08:30:00Z"),
  verified: true,
  verified_at: timestamp("2024-01-15T10:05:00Z"),
  primary: true
};
```

## Security Considerations

### PII Fields

The following fields contain PII:
- `user_id` - Personal identifier (GDPR Article 4(1))
- `email` - Personal identifier (GDPR Article 4(1))
- `ip_address` - Personal data under GDPR
- `display_name` - May contain real name

### Credential Security

⚠️ **CRITICAL: The Credential message contains ONLY metadata, NEVER actual credential values:**

- ❌ NO passwords (plaintext or hashed)
- ❌ NO private keys
- ❌ NO API keys
- ❌ NO secrets
- ❌ NO tokens

Actual credentials are stored separately with encryption at rest.

## Compliance

### NIST 800-63B

- Authentication methods aligned with NIST authenticator types
- MFA types support multi-factor requirements
- Risk levels enable risk-based authentication

### OAuth 2.0 / OIDC

- Token types support RFC 6749 (OAuth 2.0)
- ID tokens support OpenID Connect Core 1.0

### GDPR

- PII fields documented
- Data minimization applied
- User identifiers marked

## Import Path

```protobuf
import "idp/api/v1/enums.proto";
import "idp/api/v1/common.proto";
```

## See Also

- [IDP Authentication](../authn/README.md)
- [IDP Authorization](../authz/README.md)
- [IDP Identity](../identity/README.md)
- [Main IDP README](../README.md)
