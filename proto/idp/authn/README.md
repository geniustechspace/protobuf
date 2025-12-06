# IDP Authentication (authn)

Multi-method authentication with MFA support for enterprise identity providers.

## Package

```protobuf
package geniustechspace.idp.authn.v1;
```

## Overview

The authentication module provides comprehensive authentication capabilities including:

- **15 Authentication Methods** - Password, passwordless (email, SMS), WebAuthn, biometric, social, SAML, OAuth, LDAP, certificates, OTP, push notifications, QR codes, API keys, service accounts
- **Multi-Factor Authentication** - 8 MFA types (TOTP, SMS, email, voice, WebAuthn, biometric, push, backup codes)
- **Risk-Based Authentication** - Real-time risk scoring with adaptive actions
- **Session Management** - Secure session lifecycle with device binding
- **Type-Safe Credentials** - Oneof for flexible, type-safe credential submission

## Files

- `enums.proto` - Authentication enumerations
- `messages.proto` - Request/response messages
- `service.proto` - gRPC service definition

## Key Messages

### AuthenticateRequest

Initiates authentication with credentials:

```protobuf
message AuthenticateRequest {
  string tenant_id = 1;
  idp.api.v1.AuthenticationMethod method = 2;
  oneof proof {
    PasswordProof password = 3;
    EmailProof email = 4;
    SmsProof sms = 5;
    WebAuthnProof webauthn = 6;
    BiometricProof biometric = 7;
    SocialProof social = 8;
    ApiKeyProof api_key = 9;
    CertificateProof certificate = 10;
  }
  core.device.v1.DeviceContext device_context = 11;
  core.client.v1.ClientContext client_context = 12;
  core.network.v1.NetworkContext network_context = 13;
  bool remember_device = 14;
  repeated string scopes = 15;
}
```

### AuthenticateResponse

Returns authentication result with tokens or MFA requirement:

```protobuf
message AuthenticateResponse {
  idp.api.v1.AuthenticationStatus status = 1;
  bool success = 2;
  string session_id = 3;
  string access_token = 4;
  string refresh_token = 5;
  string id_token = 6;
  int32 expires_in = 7;
  string token_type = 8;
  bool mfa_required = 9;
  repeated idp.api.v1.MFAType mfa_methods = 10;
  string user_id = 11;
  idp.api.v1.RiskLevel risk_level = 12;
  int32 risk_score = 13;
  string message = 14;
  google.protobuf.Timestamp authenticated_at = 15;
}
```

## Authentication Methods

### Password Authentication

```protobuf
AuthenticateRequest request = {
  tenant_id: "tenant_123",
  method: PASSWORD,
  password: {
    identifier: "user@example.com",
    password: "secure_password"
  },
  device_context: { ... },
  remember_device: true
};
```

### Passwordless Email

```protobuf
// Step 1: Request magic link
AuthenticateRequest request = {
  tenant_id: "tenant_123",
  method: PASSWORDLESS_EMAIL,
  email: {
    email: "user@example.com"
  }
};

// Step 2: Verify with token from email
AuthenticateRequest verify = {
  tenant_id: "tenant_123",
  method: PASSWORDLESS_EMAIL,
  email: {
    email: "user@example.com",
    token: "magic_link_token"
  }
};
```

### WebAuthn/FIDO2

```protobuf
AuthenticateRequest request = {
  tenant_id: "tenant_123",
  method: WEBAUTHN,
  webauthn: {
    credential_id: "base64_credential_id",
    authenticator_data: bytes(...),
    client_data_json: bytes(...),
    signature: bytes(...),
    user_handle: bytes(...)
  }
};
```

### Social Login

```protobuf
AuthenticateRequest request = {
  tenant_id: "tenant_123",
  method: SOCIAL,
  social: {
    provider: GOOGLE,
    authorization_code: "oauth_code_from_google",
    redirect_uri: "https://example.com/callback",
    state: "csrf_token"
  }
};
```

### API Key

```protobuf
AuthenticateRequest request = {
  tenant_id: "tenant_123",
  method: API_KEY,
  api_key: {
    api_key: "sk_live_..."
  }
};
```

## Multi-Factor Authentication

### TOTP Verification

```protobuf
// After successful authentication with MFA required
VerifyMFARequest request = {
  tenant_id: "tenant_123",
  session_id: "session_from_authenticate",
  method: TOTP,
  totp: {
    code: "123456"
  },
  remember_device: true
};
```

### SMS Verification

```protobuf
VerifyMFARequest request = {
  tenant_id: "tenant_123",
  session_id: "session_id",
  method: SMS,
  sms: {
    phone_number: "+14155551234",
    code: "654321"
  }
};
```

### Backup Code

```protobuf
VerifyMFARequest request = {
  tenant_id: "tenant_123",
  session_id: "session_id",
  method: BACKUP_CODE,
  backup_code: {
    code: "ABCD-1234-EFGH-5678"
  }
};
```

## Complete Authentication Flow

```protobuf
// 1. Authenticate with password
AuthenticateRequest auth_req = {
  tenant_id: "tenant_123",
  method: PASSWORD,
  password: {
    identifier: "user@example.com",
    password: "secure_password"
  },
  device_context: { ... },
  client_context: { ... },
  network_context: { ... }
};

AuthenticateResponse auth_resp = authn_service.Authenticate(auth_req);

// 2. Handle response
if (auth_resp.mfa_required) {
  // MFA required - show MFA options
  // auth_resp.mfa_methods contains available methods
  
  // 3. Verify MFA
  VerifyMFARequest mfa_req = {
    tenant_id: "tenant_123",
    session_id: auth_resp.session_id,
    method: TOTP,
    totp: { code: "123456" },
    remember_device: true
  };
  
  VerifyMFAResponse mfa_resp = authn_service.VerifyMFA(mfa_req);
  
  if (mfa_resp.success) {
    // Store tokens
    store_tokens(mfa_resp.access_token, mfa_resp.refresh_token);
  }
} else if (auth_resp.success) {
  // Authentication successful without MFA
  store_tokens(auth_resp.access_token, auth_resp.refresh_token);
}
```

## Logout

```protobuf
// Logout current session
LogoutRequest request = {
  tenant_id: "tenant_123",
  user_id: "user_456"
};

// Logout specific session
LogoutRequest request = {
  tenant_id: "tenant_123",
  user_id: "user_456",
  session_id: "session_789"
};

// Logout all sessions
LogoutRequest request = {
  tenant_id: "tenant_123",
  user_id: "user_456",
  logout_all: true,
  revoke_tokens: true
};
```

## Security Considerations

### Password Security

⚠️ **CRITICAL: Passwords must NEVER be logged:**

- Transmitted over TLS 1.3+ only
- Hashed with bcrypt (cost 12+) or argon2id
- Never stored in logs, metrics, or traces
- Never displayed in error messages

### Rate Limiting

All authentication endpoints enforce rate limiting:

- **Authenticate**: 10/min per IP, 5/min per identifier
- **VerifyMFA**: 5/min per session
- **Logout**: 20/min per user

### Device Binding

Use `remember_device` for trusted device management:

```protobuf
AuthenticateRequest request = {
  // ...
  device_context: {
    device_id: "device_123",
    device_fingerprint: { ... }
  },
  remember_device: true  // Skip MFA on this device for 30 days
};
```

### Risk Assessment

Response includes risk assessment:

```protobuf
AuthenticateResponse response = {
  risk_level: HIGH,  // New device, different location
  risk_score: 75,    // 0-100 scale
  mfa_required: true // Force MFA for high risk
};
```

## Compliance

### NIST 800-63B

- **Section 4.1**: Authentication process
- **Section 4.2**: Authenticator types (15 methods)
- **Section 4.3**: Multi-factor authenticators (8 types)
- **Section 4.4**: Risk-based authentication
- **Section 5.1.1**: Password requirements

### W3C WebAuthn Level 2

- WebAuthn attestation and assertion
- Platform and cross-platform authenticators
- User verification requirements

### OAuth 2.0 / OIDC

- RFC 6749: OAuth 2.0 authorization framework
- OpenID Connect Core 1.0: ID tokens

### GDPR

- Email, phone, user_id are PII (Article 4(1))
- Explicit consent required for biometric data (Article 9)

## Import Path

```protobuf
import "idp/authn/v1/enums.proto";
import "idp/authn/v1/messages.proto";
import "idp/authn/v1/service.proto";
```

## See Also

- [IDP API Common](../api/README.md) - Shared types and enums
- [Core Session](../../core/session/README.md) - Session types
- [Core Device](../../core/device/README.md) - Device context
- [Main IDP README](../README.md)
