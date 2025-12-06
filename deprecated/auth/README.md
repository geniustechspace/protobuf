# Authentication Module (auth/v1) [DEPRECATED]

⚠️ **DEPRECATED**: For standard identity provider operations, use `idp/v1` instead.

Enterprise-grade Identity Provider (IDP) protocol definitions for comprehensive authentication and authorization services.

## Deprecation Notice

This module has been superseded by `idp/v1` for standard IDP use cases. The `auth/v1` module remains available for enterprise scenarios requiring advanced features not needed in typical identity provider implementations.

**Use `idp/v1` for:**
- Standard authentication (password, OTP, MFA)
- OAuth2/OIDC token management
- Password reset/change
- Session management

**Continue using `auth/v1` for:**
- WebAuthn/FIDO2
- Complex multi-step authentication
- Detailed risk assessment
- SAML 2.0
- Social login with multiple providers
- Extensive audit logging

## Overview

This module provides complete authentication infrastructure supporting:

- **Multi-Factor Authentication (MFA)**: TOTP, SMS, Email, Push Notifications, WebAuthn
- **Passwordless Authentication**: Magic Links, WebAuthn, Biometrics
- **OAuth2 & OpenID Connect**: Full OAuth2 authorization server implementation
- **SAML 2.0**: Enterprise SSO integration
- **Social Login**: Google, Facebook, Apple, GitHub, etc.
- **Session Management**: Distributed session tracking and lifecycle management
- **Token Management**: JWT, Refresh Tokens, API Keys
- **Risk-Based Authentication**: Adaptive authentication based on risk assessment
- **Device Trust**: Device fingerprinting and trust levels

## Module Structure

```
auth/v1/
├── enums.proto           # All authentication enumerations
├── messages.proto        # Core request/response messages
├── tokens.proto          # Token management messages
├── proofs.proto          # Authentication proof types
├── webauthn.proto        # WebAuthn/FIDO2 implementation
├── services.proto        # gRPC service definitions
└── events.proto          # Domain events for event sourcing
```

## File Descriptions

### enums.proto
Comprehensive enumerations for authentication operations:
- **AuthenticationStatus**: Authentication flow states
- **AuthenticationMethod**: Available authentication methods
- **AuthenticationFactor**: NIST 800-63B factor categories
- **MultiFactorType**: MFA method types
- **TokenType**: All token types in the system
- **OAuth2GrantType**: OAuth2 grant flows
- **SessionType**: Session categories
- **DeviceTrustLevel**: Device verification levels
- **PasswordPolicyStrength**: Password complexity levels
- **SocialProvider**: Supported social login providers
- **SAMLBindingType**: SAML protocol bindings
- **RiskLevel**: Risk assessment levels

### messages.proto
Core authentication messages following single responsibility principle:

**Authentication Flow:**
- `AuthenticationRequest/Response`: Multi-step authentication
- `PasswordResetRequest/Response`: Password reset flow
- `PasswordChangeRequest/Response`: Password change operations
- `PasswordValidationRequest/Response`: Policy validation

**Session Management:**
- `SessionListRequest/Response`: List user sessions
- `SessionRevokeRequest/Response`: Revoke specific session
- `SessionRevokeAllRequest/Response`: Revoke all sessions

**Note:** Session data uses `geniustechspace.datastructure.v1.session.Session` from the datastructure module.

**Supporting Messages:**

- `DeviceInfo`: Device fingerprinting (reused from `geniustechspace.datastructure.v1.device.DeviceInfo`)
- `GeoLocation`: Geographic data (reused from `geniustechspace.datastructure.v1.geo.GeoLocation`)
- `ChallengeData`: Authentication challenges
- `RiskAssessment`: Security risk analysis
- `UserIdentifier`: Flexible user identification


### tokens.proto
Complete token lifecycle management:

**Token Sets:**
- `TokenSet`: Access, refresh, and ID tokens
- `TokenRefreshRequest/Response`: Token refresh flow
- `TokenRevokeRequest/Response`: Token revocation
- `TokenIntrospectRequest/Response`: RFC 7662 introspection

**JWT Management:**
- `JWTClaims`: Standard and custom JWT claims

**API Keys:**
- `ApiKeyCreateRequest/Response`: API key generation
- `ApiKeyInfo`: API key metadata
- `ApiKeyListRequest/Response`: List API keys
- `ApiKeyRevokeRequest/Response`: API key revocation

**Token Rotation:**
- `TokenRotationPolicy`: Rotation configuration
- `TokenRotateRequest/Response`: Manual rotation

### proofs.proto
Authentication proof types (single responsibility per message):

**Knowledge Factor (Something you know):**
- `PasswordProof`: Password credentials
- `OTPProof`: One-time passwords
- `TOTPProof`: Time-based OTP
- `BackupCodeProof`: Recovery codes
- `SecurityAnswerProof`: Security questions

**Possession Factor (Something you have):**
- `MagicLinkProof`: Magic link tokens
- `DeviceCodeProof`: OAuth2 device flow
- `PushNotificationProof`: Push authentication
- `TokenProof`: Bearer tokens
- `CertificateProof`: X.509 certificates
- `SmartCardProof`: Smart card authentication
- `SecurityKeyProof`: Hardware security keys

**Inherence Factor (Something you are):**
- `BiometricProof`: Biometric authentication
- `WebAuthnProof`: WebAuthn assertions

**Federated Identity:**
- `SSOAssertion`: SAML/JWT assertions
- `SocialLoginProof`: Social provider OAuth2

**Container:**
- `AuthProof`: Flexible container for any proof type

### webauthn.proto
Complete W3C WebAuthn Level 2 implementation:

**Registration (Attestation):**
- `WebAuthnRegistrationOptionsRequest/Response`: Registration challenge
- `WebAuthnRegistrationRequest/Response`: Credential registration

**Authentication (Assertion):**
- `WebAuthnAuthenticationOptionsRequest/Response`: Auth challenge
- `WebAuthnAuthenticationRequest/Response`: Authentication

**Credential Management:**
- `WebAuthnCredentialInfo`: Credential metadata
- `WebAuthnCredentialListRequest/Response`: List credentials
- `WebAuthnCredentialUpdateRequest/Response`: Update credential
- `WebAuthnCredentialDeleteRequest/Response`: Delete credential

**Supporting Messages:**
- `WebAuthnCredential`: Attestation/assertion data
- `CredentialParameter`: Algorithm support
- `CredentialDescriptor`: Credential identification
- `AuthenticatorSelection`: Authenticator requirements

### services.proto
Comprehensive gRPC service definitions:

**AuthenticationService:**
- User authentication flows
- Multi-step authentication
- Passwordless authentication
- Token refresh and validation
- Logout operations

**PasswordService:**
- Password reset flows
- Password change
- Password validation
- Password policy management

**MFAService:**
- MFA enrollment and verification
- MFA method management
- Backup codes generation

**WebAuthnService:**
- WebAuthn registration and authentication
- Credential lifecycle management

**SessionService:**
- Session lifecycle management
- Session listing and revocation

**TokenService:**
- Token introspection and revocation
- Token rotation
- API key management

**OAuth2Service:**
- OAuth2 authorization server
- Token endpoint
- Client registration and management
- UserInfo endpoint (OIDC)
- Device authorization flow

**SocialLoginService:**
- Social provider authentication
- Account linking/unlinking
- Authorization URL generation

**SAMLService:**
- SAML 2.0 SP and IDP flows
- SSO initiation and assertion processing
- Single Logout (SLO)
- Metadata exchange

### events.proto
Domain events for audit logging, security monitoring, and event sourcing:

**Authentication Events:**
- `UserAuthenticatedEvent`: Successful authentication
- `AuthenticationFailedEvent`: Failed attempts
- `AuthenticationChallengeIssuedEvent`: Challenge issued

**Session Events:**
- `SessionCreatedEvent`: New session
- `SessionExtendedEvent`: Session extension
- `SessionRevokedEvent`: Manual revocation
- `SessionExpiredEvent`: Natural expiration
- `UserLoggedOutEvent`: User logout

**Password Events:**
- `PasswordResetRequestedEvent`: Reset initiated
- `PasswordResetCompletedEvent`: Reset completed
- `PasswordChangedEvent`: Password changed
- `PasswordCompromisedEvent`: Breach detected

**Token Events:**
- `TokenIssuedEvent`: Token issuance
- `TokenRefreshedEvent`: Token refresh
- `TokenRevokedEvent`: Token revocation
- `TokenExpiredEvent`: Token expiration
- `TokenIntrospectedEvent`: Token introspection

**MFA Events:**
- `MFAEnrolledEvent`: MFA enrollment
- `MFAVerifiedEvent`: Successful verification
- `MFAFailedEvent`: Failed verification
- `MFADisabledEvent`: MFA disabled
- `BackupCodesGeneratedEvent`: Backup codes generated
- `BackupCodeUsedEvent`: Backup code used

**WebAuthn Events:**
- `WebAuthnCredentialRegisteredEvent`: Credential registration
- `WebAuthnCredentialUsedEvent`: Credential usage
- `WebAuthnCredentialDeletedEvent`: Credential deletion

**Device Trust Events:**
- `DeviceTrustedEvent`: Device trusted
- `DeviceRemovedEvent`: Device removed
- `DeviceCompromisedEvent`: Device compromise detected

**Security Events:**
- `SuspiciousActivityDetectedEvent`: Anomaly detection
- `AccountLockedEvent`: Account locked
- `AccountUnlockedEvent`: Account unlocked
- `BruteForceDetectedEvent`: Brute force attack
- `RateLimitExceededEvent`: Rate limit exceeded

**OAuth2 & Social Events:**
- `OAuth2ClientRegisteredEvent`: Client registration
- `OAuth2AuthorizationGrantedEvent`: Authorization granted
- `SocialAccountLinkedEvent`: Social account linked
- `SocialAccountUnlinkedEvent`: Social account unlinked
- `SocialLoginEvent`: Social login

**API Key Events:**
- `ApiKeyCreatedEvent`: API key created
- `ApiKeyUsedEvent`: API key used
- `ApiKeyRevokedEvent`: API key revoked

**SAML Events:**
- `SAMLAuthenticationEvent`: SAML authentication
- `SAMLLogoutEvent`: SAML logout

## Design Principles

### 1. Single Responsibility
Each message focuses on a single concern. Large messages are split into focused, composable units.

### 2. Flat Design
Prefer flat structures over deep nesting where possible for better performance and clarity.

### 3. Enum Naming
Enums do not contain the "Enum" suffix except for the `_UNSPECIFIED` value:
- ✅ `AuthenticationStatus.AUTHENTICATED`
- ❌ `AuthenticationStatusEnum.AUTHENTICATION_STATUS_AUTHENTICATED`

### 4. Reserved Fields
All messages include reserved field ranges for future extensions without breaking changes.

### 5. Compliance & Security
- **NIST 800-63B**: Authentication assurance levels
- **OAuth 2.0**: RFC 6749 compliance
- **OIDC Core 1.0**: OpenID Connect support
- **W3C WebAuthn Level 2**: FIDO2 compliance
- **SAML 2.0**: Enterprise SSO
- **SOC 2**: Security monitoring and audit logging
- **ISO 27001**: Event logging requirements
- **GDPR**: Data protection and privacy

### 6. No Duplication
Common messages from `datastructure/v1/*` are reused:
- Pagination: `geniustechspace.datastructure.v1.pagination`
- Errors: `geniustechspace.datastructure.v1.error`
- Request context: `geniustechspace.datastructure.v1.request`
- Session: `geniustechspace.datastructure.v1.session`
- Retry: `geniustechspace.datastructure.v1.retry`

## Usage Examples

### Basic Authentication
```protobuf
// Request
AuthenticationRequest {
  email: "user@example.com"
  proof: {
    password: { password: "secure_password" }
  }
  tenant_id: "tenant_123"
  session_type: WEB
}

// Response
AuthenticationResponse {
  status: AUTHENTICATED
  user_id: "usr_123"
  tokens: {
    access_token: "eyJ..."
    refresh_token: "ref_..."
    expires_in: 3600
  }
  session_info: { ... }
}
```

### MFA Flow
```protobuf
// Step 1: Initial authentication
AuthenticationResponse {
  status: MFA_REQUIRED
  auth_id: "auth_abc123"
  required_methods: [TOTP, WEBAUTHN]
}

// Step 2: MFA verification
AuthenticationRequest {
  auth_id: "auth_abc123"
  proof: {
    totp: { code: "123456" }
  }
}
```

### WebAuthn Registration
```protobuf
// Get registration options
WebAuthnRegistrationOptionsRequest {
  user_id: "usr_123"
  username: "user@example.com"
  display_name: "John Doe"
}

// Register credential
WebAuthnRegistrationRequest {
  user_id: "usr_123"
  credential_name: "YubiKey 5"
  credential: { ... }
}
```

### OAuth2 Authorization
```protobuf
// Authorization request
OAuth2AuthorizeRequest {
  client_id: "client_123"
  response_type: "code"
  redirect_uri: "https://app.example.com/callback"
  scopes: ["read", "write"]
  state: "random_state"
  code_challenge: "challenge"
  code_challenge_method: "S256"
}

// Token exchange
OAuth2TokenRequest {
  grant_type: AUTHORIZATION_CODE
  code: "auth_code_123"
  redirect_uri: "https://app.example.com/callback"
  client_id: "client_123"
  code_verifier: "verifier"
}
```

## Security Considerations

### 1. Transport Security
- All endpoints MUST use TLS 1.3+
- Certificate pinning recommended for mobile apps

### 2. Rate Limiting
- Implement per-IP and per-user rate limits
- Progressive delays for failed authentication attempts
- Use `RateLimitExceededEvent` for monitoring

### 3. Token Security
- Access tokens: Short-lived (15-60 minutes)
- Refresh tokens: Long-lived (30-90 days)
- Implement token rotation
- Use secure token storage (HttpOnly cookies, secure storage)

### 4. Password Security
- Enforce strong password policies
- Check passwords against breach databases (HaveIBeenPwned)
- Use Argon2id for password hashing
- Implement password history

### 5. MFA Security
- Require MFA for privileged operations
- Support multiple MFA methods
- Generate cryptographically secure backup codes
- Implement backup code single-use policy

### 6. Session Security
- Implement concurrent session limits
- Track session devices and locations
- Enable user session review and revocation
- Implement session fixation protection

### 7. Risk-Based Authentication
- Monitor authentication patterns
- Detect anomalies (location, device, time)
- Implement adaptive authentication
- Challenge high-risk authentications

### 8. Audit Logging
- Log all authentication events
- Log security events (failures, locks, breaches)
- Never log credentials or tokens
- Implement log aggregation and SIEM integration

## Integration with Other Modules

### Core Module
- `core.v1.Metadata`: Entity metadata and versioning
- `core.v1.types`: Common types (Address, Money, ContactInfo)

### Datastructure Module
- `datastructure.v1.pagination`: Pagination controls
- `datastructure.v1.error`: Error responses
- `datastructure.v1.request`: Request context
- `datastructure.v1.session`: Session management
- `datastructure.v1.retry`: Retry policies

### Users Module
- User profile management
- User roles and permissions
- User preferences

### Tenants Module
- Multi-tenant isolation
- Tenant-specific configurations
- Tenant authentication policies

### Access Policy Module
- Fine-grained authorization
- Role-based access control (RBAC)
- Attribute-based access control (ABAC)

## Client Generation

This module supports client generation for:
- **Go**: `github.com/geniustechspace/protobuf/gen/go/auth/v1`
- **TypeScript**: `@geniustechspace/protobuf/auth/v1`
- **C#**: `GeniusTechSpace.Protobuf.Auth.V1`
- **Java**: `com.geniustechspace.protobuf.auth.v1`
- **Python**: `geniustechspace.protobuf.auth.v1`

See [CLIENT_GENERATION.md](../../docs/CLIENT_GENERATION.md) for details.

## Testing

### Unit Testing
Test individual message validation and serialization.

### Integration Testing
Test service implementations against the protocol definitions.

### Security Testing
- Penetration testing
- Vulnerability scanning
- Compliance validation

### Performance Testing
- Authentication throughput
- Token generation performance
- Session lookup performance

## Migration Guide

Since this is the initial setup, breaking changes are acceptable. Future changes will follow semantic versioning.

### Version History
- **v1.0.0** (Initial): Complete enterprise IDP implementation

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for contribution guidelines.

## License

See [LICENSE](../../LICENSE) for licensing information.

## Support

For questions or issues, contact the platform team.
