# Core Token Structures

Reusable token data structures for JWT claims and token metadata.

## Package

```protobuf
package geniustechspace.core.token.v1;
```

## Overview

Domain-agnostic token structures for authentication services, API gateways, and authorization systems. Supports RFC 7519 (JWT), RFC 6749 (OAuth 2.0), and OpenID Connect Core 1.0.

## Messages

### TokenClaims
Standard JWT claims with OpenID Connect and custom extensions.

**Standard JWT Claims (RFC 7519):**
- `jti` - JWT ID (unique identifier)
- `iss` - Issuer
- `sub` - Subject (user/service ID)
- `aud` - Audience (intended recipients)
- `exp` - Expiration time
- `nbf` - Not before time
- `iat` - Issued at time

**OpenID Connect Claims:**
- `azp` - Authorized party (client ID)
- `scopes` - OAuth 2.0 scopes
- `nonce` - Nonce for replay protection

**Custom Claims:**
- `tenant_id` - Multi-tenant identifier
- `roles` - User roles (RBAC)
- `permissions` - Fine-grained permissions
- `session_id` - Associated session
- `token_type` - Type of token
- `metadata` - Extensible key-value metadata

### TokenMetadata
Non-claim token information for lifecycle management.

**Fields:**
- `token_id` - Unique token identifier
- `token_type` - Type enum (ACCESS, REFRESH, ID, API_KEY, etc.)
- `status` - Status enum (ACTIVE, EXPIRED, REVOKED, INVALID)
- `subject` - Token subject
- `scopes` - Granted scopes
- `issued_at` - Issuance timestamp
- `expires_at` - Expiration timestamp
- `revoked_at` - Revocation timestamp (if applicable)
- `issuer` - Token issuer
- `metadata` - Additional context

### TokenIntrospection
Complete token introspection result (RFC 7662).

**Fields:**
- `active` - Whether token is currently active
- `claims` - Token claims (if active)
- `metadata` - Token metadata

## Enums

### TokenType
- `ACCESS` - Short-lived access token
- `REFRESH` - Long-lived refresh token
- `ID` - OpenID Connect ID token
- `API_KEY` - API key token
- `SESSION` - Session token
- `BEARER` - Generic bearer token

### TokenStatus
- `ACTIVE` - Token is valid and active
- `EXPIRED` - Token has expired
- `REVOKED` - Token was revoked
- `INVALID` - Token is invalid

## Design Principles

1. **Standards Compliance** - Follows RFC 7519 (JWT) and RFC 7662 (Token Introspection)
2. **Domain Agnostic** - Reusable across authentication, authorization, and API services
3. **Extensible** - Metadata maps for custom claims without schema changes
4. **Minimal** - Only essential token-related structures
5. **Type Safe** - Enums for token types and status

## Usage Examples

### JWT Claims
```protobuf
import "proto/datastructure/v1/token/messages.proto";

// Create JWT claims
TokenClaims claims = {
  jti: "unique-jwt-id"
  iss: "https://auth.example.com"
  sub: "user_12345"
  aud: ["https://api.example.com"]
  exp: { seconds: 1735689600 }
  iat: { seconds: 1735603200 }
  scopes: ["read:profile", "write:data"]
  tenant_id: "tenant_abc"
  roles: ["user", "admin"]
  token_type: ACCESS
};
```

### Token Introspection
```protobuf
// Introspect token
TokenIntrospection result = {
  active: true
  claims: { ... }
  metadata: {
    token_id: "token_xyz"
    token_type: ACCESS
    status: ACTIVE
    subject: "user_12345"
    scopes: ["read:profile"]
  }
};
```

## Standards Compliance

- **RFC 7519** - JSON Web Token (JWT) claims
- **RFC 6749** - OAuth 2.0 scopes and token types
- **RFC 7662** - OAuth 2.0 Token Introspection
- **OpenID Connect Core 1.0** - ID token claims

## Use Cases

- **Authentication Services** - Issue and validate tokens
- **API Gateways** - Verify token claims for routing/authorization
- **Authorization Services** - Extract roles/permissions from tokens
- **Token Introspection** - Validate and inspect tokens
- **Audit Logging** - Record token usage and lifecycle events
