# Core Session Management

Enterprise session management for users, clients, and AI agents in multi-tenant environments.

## Package

```protobuf
package geniustechspace.core.session.v1;
```

## Overview

The `core/session` module provides comprehensive session management supporting multi-factor authentication, step-up authentication, role-based access control, and context tracking for security and auditing.

## Messages

### Session

Comprehensive session data structure.

**Key Fields:**

- `session_id` (string) - Unique session identifier (8-128 chars, REQUIRED)
- `tenant_id` (string) - Tenant context (3-64 chars, REQUIRED)
- `user_id` / `agent_id` (oneof actor) - User or AI agent ID (max 128 chars)
- `device_id` (string) - Device reference (max 128 chars)
- `client_id` (string) - Client application reference (max 128 chars)
- `network_id` (string) - Network context reference (max 128 chars)
- `geo_location_id` (string) - Geographic location reference (max 128 chars)
- `status` (SessionStatus) - Lifecycle state
- `auth_status` (AuthenticationStatus) - Authentication state
- `primary_auth_method` (AuthenticationMethod) - Primary auth method used
- `additional_auth_methods` (repeated) - Additional auth methods (MFA)
- `required_mfa_methods` (repeated) - Required MFA methods
- `completed_mfa_methods` (repeated) - Completed MFA methods
- `roles` (repeated string) - User/agent roles (max 20 items)
- `permissions` (repeated string) - Granted permissions (max 100 items)
- `metadata` (map<string, string>) - Additional metadata
- `created_at` (Timestamp) - Session creation time
- `updated_at` (Timestamp) - Last activity time
- `expires_at` (Timestamp) - Session expiration time
- `authenticated_at` (Timestamp) - Authentication completion time
- `mfa_completed_at` (Timestamp) - MFA completion time

## Enumerations

### SessionStatus

Session lifecycle states:

- `SESSION_STATUS_UNSPECIFIED` (0) - Default/unknown
- `SESSION_STATUS_ACTIVE` (1) - Session is active
- `SESSION_STATUS_EXPIRED` (2) - Session expired
- `SESSION_STATUS_REVOKED` (3) - Session revoked by user/admin
- `SESSION_STATUS_SUSPENDED` (4) - Session temporarily suspended

### AuthenticationStatus

Authentication progress:

- `AUTH_STATUS_UNSPECIFIED` (0) - Default/unknown
- `AUTH_STATUS_UNAUTHENTICATED` (1) - No authentication yet
- `AUTH_STATUS_PARTIAL` (2) - Primary auth done, MFA pending
- `AUTH_STATUS_AUTHENTICATED` (3) - Fully authenticated
- `AUTH_STATUS_STEP_UP_REQUIRED` (4) - Step-up authentication required

### AuthenticationMethod

Authentication methods:

- `PASSWORD` - Password-based authentication
- `EMAIL_LINK` - Magic link via email
- `SMS_CODE` - SMS OTP
- `TOTP` - Time-based OTP (Google Authenticator)
- `WEBAUTHN` - WebAuthn/FIDO2
- `BIOMETRIC` - Fingerprint/FaceID
- `SSO` - Single Sign-On
- `API_KEY` - API key authentication

### MFAType

Multi-factor authentication types:

- `SMS` - SMS OTP
- `TOTP` - Authenticator app
- `EMAIL` - Email OTP
- `WEBAUTHN` - Security key
- `BACKUP_CODES` - Backup recovery codes

## Usage Examples

### Create Session

```protobuf
import "core/session/v1/messages.proto";

Session session = {
  session_id: generate_uuid(),
  tenant_id: "tenant_abc",
  user_id: "usr_123",
  device_id: "dev_456",
  client_id: "client_789",
  status: SESSION_STATUS_ACTIVE,
  auth_status: AUTH_STATUS_UNAUTHENTICATED,
  created_at: now(),
  expires_at: now() + 24h
};
```

### Complete Primary Authentication

```protobuf
session.auth_status = AUTH_STATUS_PARTIAL;
session.primary_auth_method = PASSWORD;
session.authenticated_at = now();
session.required_mfa_methods = [TOTP];  // Require MFA
```

### Complete MFA

```protobuf
session.auth_status = AUTH_STATUS_AUTHENTICATED;
session.completed_mfa_methods = [TOTP];
session.mfa_completed_at = now();
```

### Update Roles and Permissions

```protobuf
session.roles = ["user", "admin"];
session.permissions = [
  "users:read",
  "users:write",
  "tenants:read"
];
```

### Session Expiration

```protobuf
if now() > session.expires_at {
  session.status = SESSION_STATUS_EXPIRED;
}
```

### Session Revocation

```protobuf
session.status = SESSION_STATUS_REVOKED;
session.updated_at = now();
```

## Authentication Flows

### Password + TOTP Flow

```
1. User provides password
   → auth_status = AUTH_STATUS_PARTIAL
   → primary_auth_method = PASSWORD
   → required_mfa_methods = [TOTP]

2. User provides TOTP code
   → auth_status = AUTH_STATUS_AUTHENTICATED
   → completed_mfa_methods = [TOTP]
   → mfa_completed_at = now()
```

### Step-Up Authentication

```
1. User authenticated (low-risk)
   → auth_status = AUTH_STATUS_AUTHENTICATED

2. User attempts sensitive operation
   → auth_status = AUTH_STATUS_STEP_UP_REQUIRED
   → required_mfa_methods = [WEBAUTHN]

3. User completes step-up
   → auth_status = AUTH_STATUS_AUTHENTICATED
   → additional_auth_methods = [WEBAUTHN]
```

### Passwordless Flow

```
1. User provides email
   → Send magic link

2. User clicks link
   → auth_status = AUTH_STATUS_AUTHENTICATED
   → primary_auth_method = EMAIL_LINK
```

## Session Binding

Sessions are bound to context for security:

```protobuf
Session {
  device_id: "dev_123",    // Must match on requests
  client_id: "web_app",    // Must match on requests
  network_id: "net_456",   // Optional: IP/network binding
  geo_location_id: "geo_789"  // Optional: geofencing
}
```

**Security Benefits:**

- Prevents session hijacking
- Detects suspicious activity
- Enables anomaly detection

## Session Lifecycle

```
CREATE → ACTIVE → EXPIRED
           ↓
        REVOKED
           ↓
       SUSPENDED
```

### Timeouts

- **Idle Timeout:** 15 minutes (configurable)
- **Absolute Timeout:** 24 hours (configurable)
- **MFA Grace Period:** 5 minutes for MFA completion

### Renewal

```protobuf
if session_active_within_threshold() {
  session.expires_at = now() + session_duration;
  session.updated_at = now();
}
```

## Import Path

```protobuf
import "core/session/v1/messages.proto";
import "core/session/v1/enums.proto";
```

## Best Practices

### 1. Session Security

```protobuf
// Always bind to device and client
Session {
  device_id: device.id,
  client_id: client.id,
  network_id: network.id
}

// Validate context on every request
if request.device_id != session.device_id {
  return InvalidSessionError
}
```

### 2. Token Management

```protobuf
// Store session ID in token claims
TokenClaims {
  session_id: session.session_id,
  tenant_id: session.tenant_id,
  sub: session.user_id
}
```

### 3. MFA Enforcement

```protobuf
// Require MFA for sensitive operations
if is_sensitive_operation() {
  if !session.completed_mfa_methods {
    return MFARequiredError
  }
}
```

### 4. Session Cleanup

```protobuf
// Periodic cleanup of expired sessions
DELETE FROM sessions
WHERE expires_at < now() - retention_period;
```

### 5. Audit Logging

```protobuf
// Log all session events
log_event({
  event_type: "session.created",
  session_id: session.session_id,
  user_id: session.user_id,
  tenant_id: session.tenant_id
});
```

## Compliance

### OWASP Session Management

- Session IDs are cryptographically random
- Sessions expire after idle timeout
- Sessions have absolute timeout
- Session binding to device/client

### NIST 800-63B

- Multi-factor authentication support
- Session binding to authenticators
- Reauthentication for sensitive operations

### GDPR Article 25

- Data minimization (only essential fields)
- Privacy by design
- Right to erasure (session cleanup)

### SOC 2 Type II

- Access control enforcement
- Audit trail for all sessions
- Secure session management

### PSD2 SCA

- Strong customer authentication
- Multi-factor support
- Transaction authentication

## See Also

- [Core Token](../token/README.md) - Token structures and JWT claims
- [Core Device](../device/README.md) - Device context
- [Core Client](../client/README.md) - Client context
- [Core Network](../network/README.md) - Network context
- [Main Core README](../README.md) - Complete core module documentation
