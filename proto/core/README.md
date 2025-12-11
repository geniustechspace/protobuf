# Core Proto Modules

Enterprise-grade foundational Protocol Buffer definitions providing reusable types, patterns, and utilities for all domain services in the GeniusTech Space ecosystem.

## Overview

The `proto/core` module contains domain-agnostic, reusable message definitions that establish consistency, compliance, and best practices across all microservices. These are the building blocks used by higher-level domains (IDP, storage, etc.).

## Module Structure

```
proto/core/
├── api/                # API layer concerns (request/response lifecycle)
│   ├── pagination/v1/  # Pagination controls (moved from core/pagination)
│   ├── error/v1/       # Error handling (moved from core/error)
│   ├── request/v1/     # Request metadata (moved from core/request)
│   ├── retry/v1/       # Retry policies (moved from core/retry)
│   └── circuit_breaker/v1/ # Circuit breaker (moved from core/circuit_breaker)
├── common/v1/          # Common value objects (Address, Money, TenantContext)
├── metadata/v1/        # Entity metadata and audit trails
├── events/v1/          # Event sourcing foundation
├── device/v1/          # Device identification and fingerprinting
├── client/v1/          # Client application tracking
├── network/v1/         # Network and connectivity context
├── geo/v1/             # Geolocation value objects
├── token/v1/           # Token structures and JWT claims
└── session/v1/         # Session management
```

## Core Modules

### 1. Common (`core/common/v1`)

**Purpose:** Foundational value objects used across all domains

**Key Types:**

- `Address` - Physical/mailing addresses with validation
- `ContactInfo` - Email, phone, fax contact details
- `Money` - Currency-aware monetary values (stored as minor units)
- `TenantContext` - Multi-tenant isolation context
- `PaginationRequest` / `PaginationResponse` - Standardized pagination

**Usage:**

```protobuf
import "core/common/v1/common.proto";

message CreateUserRequest {
  geniustechspace.core.common.v1.TenantContext tenant_context = 1;
  geniustechspace.core.common.v1.ContactInfo contact = 2;
  geniustechspace.core.common.v1.Address billing_address = 3;
}
```

**Compliance:**

- GDPR Article 4(1) - Address and ContactInfo are PII
- PCI DSS - Money type for payment amounts
- SOC 2 CC6.1 - Tenant isolation

---

### 2. Metadata (`core/metadata/v1`)

**Purpose:** Audit trails, versioning, and soft deletes for all entities

**Key Types:**

- `Metadata` - Complete entity lifecycle tracking

**Fields:**

- `id` - Unique entity identifier (UUID recommended)
- `created_at` / `updated_at` - Timestamps (UTC)
- `created_by` / `updated_by` - Actor identifiers
- `version` - Optimistic locking version
- `deleted` / `deleted_at` - Soft delete support

**Usage:**

```protobuf
import "core/metadata/v1/metadata.proto";

message User {
  geniustechspace.core.metadata.v1.Metadata metadata = 1;
  string email = 2;
  // ... other fields
}
```

**Compliance:**

- SOC 2 CC6.3 - Change management audit trail
- GDPR Article 5(2) - Accountability principle
- GDPR Article 17 - Right to erasure (soft delete)

---

### 3. Events (`core/events/v1`)

**Purpose:** Event sourcing and event-driven architecture foundation

**Key Types:**

- `BaseEvent` - Standard event structure for all domain events
- `EventEnvelope` - Event streaming wrapper (Kafka/Pulsar)
- `EventBatch` - Batch processing support

**Features:**

- Immutable append-only events
- Distributed tracing (correlation_id, causation_id)
- Event versioning for schema evolution
- Tenant isolation for multi-tenancy

**Usage:**

```protobuf
import "core/events/v1/events.proto";
import "google/protobuf/any.proto";

// Domain event
message UserCreatedEvent {
  string user_id = 1;
  string email = 2;
}

// Wrap in BaseEvent
geniustechspace.core.events.v1.BaseEvent event = {
  event_id: "evt_123",
  event_type: "user.created",
  aggregate_id: "usr_456",
  aggregate_type: "user",
  payload: Any.pack(user_created_event),
  // ... other fields
};
```

**Compliance:**

- SOC 2 CC7.2 - System monitoring
- ISO 27001 A.12.4.1 - Event logging

---

### 4. Pagination (`core/api/pagination/v1`)

**Location:** Moved to `core/api/*` - API layer concern

**Purpose:** Cursor-based hybrid pagination with bidirectional navigation

**Standards:** Industry-standard (MongoDB, GraphQL Relay, Stripe, Elasticsearch)

**Key Types:**

- `PaginationRequest` - Request parameters (page_size, page, cursor)
- `PaginationResponse` - Response metadata (total_size, current_page, page_size, cursor)

**Design:** Single responsibility - pagination only, sorting/filtering separate

**Performance:**

- O(log n) with client-side cursor caching
- Graceful O(n) fallback without cursor
- Client caches cursors per page for optimal bidirectional navigation

**Limits:**

- Max page_size: 1000 items
- Default page_size: 20 items

**Usage:**

```protobuf
import "core/api/pagination/v1/messages.proto";

message ListUsersRequest {
  string tenant_id = 1;
  core.api.pagination.v1.PaginationRequest pagination = 2;
  string order_by = 3;  // Sorting (separate concern)
  string filter = 4;    // Filtering (separate concern)
}

message ListUsersResponse {
  repeated User users = 1;
  core.api.pagination.v1.PaginationResponse pagination = 2;
}
```

**Cursor-based flow:**

- First page: No cursor provided, server returns cursor for page 2
- Next pages: Client provides cached cursor → O(log n) keyset pagination
- Bidirectional: Client caches cursors for forward/backward navigation
- End of collection: cursor is empty

**Performance:** Prevents memory exhaustion, O(log n) for sequential navigation, handles concurrent modifications

---

### 5. Error (`core/api/error/v1`)

**Note:** Moved to `core/api/*` - API layer concern

**Purpose:** Standardized error responses for distributed systems

**Key Types:**

- `ErrorResponse` - Top-level error container
- `ErrorDetail` - Specific error information
- `ErrorSeverity` - Impact level (INFO, WARNING, ERROR, CRITICAL, FATAL)

**Error Categories:**

- `ValidationErrorCode` - Input validation failures
- `AuthenticationErrorCode` - Authentication failures
- `AuthorizationErrorCode` - Permission denied
- `ResourceErrorCode` - Resource not found, conflicts
- `BusinessErrorCode` - Business rule violations
- `RateLimitErrorCode` - Rate limiting
- `SystemErrorCode` - Infrastructure failures
- `IntegrationErrorCode` - Third-party API failures
- `DataErrorCode` - Data integrity issues
- `FileErrorCode` - File operation failures
- `NetworkErrorCode` - Network connectivity issues
- `SecurityErrorCode` - Security violations

**Security:** Never expose stack traces, internal IDs, or infrastructure details

**Usage:**

```protobuf
import "core/api/error/v1/messages.proto";

ErrorResponse error = {
  message: "User not found",
  request_id: "req_123",
  occurred_at: timestamp,
  details: [{
    resource: RESOURCE_ERROR_CODE_NOT_FOUND,
    severity: ERROR,
    message: "User with ID usr_456 does not exist"
  }]
};
```

**Compliance:** SOC 2 CC6.1, CC7.2 | GDPR Article 32

---

### 6. Request (`core/api/request/v1`)

**Note:** Moved to `core/api/*` - API layer concern

**Purpose:** Request metadata, client context, and authorization

**Key Types:**

- `RequestMetadata` - HTTP/gRPC request metadata
- `RequestContext` - Full request context with auth info

**Features:**

- Protocol detection (HTTP/1.1, HTTP/2, gRPC, WebSocket)
- Priority levels for request routing
- Idempotency support
- Validation modes (STRICT, LENIENT, DRY_RUN)

**Usage:**

```protobuf
import "core/api/request/v1/messages.proto";to";

message CreateResourceRequest {
  geniustechspace.core.request.v1.RequestContext context = 1;
  // ... resource fields
}
```

**Security:** Never include Authorization headers, API keys, or cookies in metadata

---

### 7. Device (`core/device/v1`)

**Purpose:** Device identification, fingerprinting, and risk assessment

**Key Types:**

- `DeviceContext` - Comprehensive device metadata
- `DeviceFingerprint` - Stable device identification

**Features:**

- Operating system detection (iOS, Android, Windows, macOS, Linux)
- Hardware capabilities (biometric, NFC, GPS)
- Trust levels (UNTRUSTED, KNOWN, TRUSTED, VERIFIED, MANAGED)
- Jailbreak/root detection

**Privacy Warning:** Device fingerprinting is privacy-invasive. Use only for security purposes with proper consent.

**Compliance:**

- GDPR Article 6 - Lawful basis required
- GDPR Article 30 - Records of processing activities
- ePrivacy Directive - Device tracking consent
- CCPA - Device identifiers are personal information

---

### 8. Client (`core/client/v1`)

**Purpose:** Client application tracking and feature detection

**Key Types:**

- `ClientContext` - Client application metadata
- `ClientFingerprint` - Client identification

**Features:**

- Client types (WEB_BROWSER, MOBILE_APP, DESKTOP_APP, CLI, IoT)
- Platform detection (iOS, Android, Windows, Web)
- Framework detection (React, Flutter, React Native)
- Trust levels and attestation
- Feature flags and capabilities

**Privacy Warning:** Combined client data enables user profiling. Implement data minimization.

**Compliance:**

- GDPR Article 13 - Transparency in data collection
- ePrivacy Directive - Cookie/tracking consent
- CCPA - Do Not Track signals

---

### 9. Network (`core/network/v1`)

**Purpose:** Network connectivity and security analysis

**Key Types:**

- `NetworkContext` - Network and connectivity metadata
- `SecurityIndicators` - VPN/Tor/proxy detection

**Features:**

- IP address tracking (IPv4/IPv6)
- Connection type detection (WiFi, Cellular, VPN)
- Protocol and TLS version tracking
- Threat scoring and reputation checks
- Autonomous System (AS) information

**Security:** IP addresses are PII under GDPR. Anonymize when possible.

---

### 10. Geo (`core/geo/v1`)

**Purpose:** Geolocation value objects

**Key Types:**

- `GeoLocation` - Geographic coordinates and metadata

**Features:**

- Country, region, city, postal code
- Latitude/longitude coordinates
- Timezone (IANA format)
- Source tracking (IP, GPS, WiFi, User)

**Privacy:** Location data is highly sensitive PII. Requires user consent.

---

### 11. Token (`core/token/v1`)

**Purpose:** Token structures for authentication and authorization

**Key Types:**

- `TokenClaims` - Standard JWT claims (RFC 7519)
- `TokenMetadata` - Token audit and management
- `TokenIntrospection` - Token validation results (RFC 7662)

**Standards:**

- RFC 7519 (JWT)
- RFC 6749 (OAuth 2.0)
- OpenID Connect Core 1.0

**Usage:**

```protobuf
import "core/api/request/v1/messages.proto";

geniustechspace.core.token.v1.TokenClaims claims = {
  sub: "usr_123",
  iss: "https://auth.example.com",
  aud: ["api.example.com"],
  scopes: ["user:read", "user:write"],
  tenant_id: "tenant_abc"
};
```

---

### 12. Session (`core/session/v1`)

**Purpose:** Session management for users and AI agents

**Key Types:**

- `Session` - Comprehensive session data

**Features:**

- Multi-actor support (users, AI agents)
- Authentication status tracking
- MFA state management
- Context references (device, client, network, geo)
- RBAC (roles and permissions)

**Security:**

- Session binding (device/client/network)
- Short expiration (15min idle, 24h absolute)
- Audit logging for all lifecycle events

**Compliance:**

- OWASP Session Management Cheat Sheet
- NIST 800-63B - Digital Identity Guidelines
- GDPR Article 25 - Data Protection by Design
- SOC 2 Type II - Access Control
- PSD2 - Strong Customer Authentication

---

### 13. Retry (`core/api/retry/v1`)

**Note:** Moved to `core/api/*` - API layer concern

**Purpose:** Enterprise retry policies and strategies

**Key Types:**

- `RetryInfo` - Server guidance per request
- `RetryPolicy` - Reusable retry configuration
- `RetryStrategy` - Backoff algorithms
- `RetryMetrics` - Performance observability

**Features:**

- Backoff strategies (exponential, linear, constant, fibonacci)
- Jitter for thundering herd prevention
- Idempotency key enforcement
- Regional fallback support

**Patterns:** Matches Google Cloud, AWS SDK, and Envoy

**Compliance:** SOC 2 CC7.2, CC9.1 | PCI DSS 6.5.10 | ISO 27001 A.12.6.1

---

### 14. Circuit Breaker (`core/api/circuit_breaker/v1`)

**Note:** Moved to `core/api/*` - API layer concern

**Purpose:** Cascading failure prevention

**Key Types:**

- `CircuitBreakerConfig` - Threshold configuration
- `CircuitBreaker` - Real-time state and metrics

**States:**

- `CLOSED` - Normal operation (requests flowing)
- `OPEN` - Blocking requests (service failing)
- `HALF_OPEN` - Testing recovery (limited requests)

**Features:**

- Failure rate thresholds
- Rolling window evaluation
- Slow call detection
- Automatic recovery testing

**Patterns:** Matches Envoy, Hystrix, and Resilience4j

**Compliance:** SOC 2 CC9.1 (Risk Management)

---

## Package Naming Convention

All core modules follow the naming pattern:

```
package geniustechspace.core.<module>.v1;
```

Examples:

- `geniustechspace.core.common.v1`
- `geniustechspace.core.metadata.v1`
- `geniustechspace.core.error.v1`

## Go Package Options

```protobuf
option go_package = "github.com/geniustechspace/protobuf/gen/go/core/<module>/v1;<module>v1";
```

Example:

```protobuf
option go_package = "github.com/geniustechspace/protobuf/gen/go/core/common/v1;commonv1";
```

## Import Paths

Always use module-relative paths (no `proto/` prefix):

✅ **Correct:**

```protobuf
import "core/common/v1/common.proto";
import "core/metadata/v1/metadata.proto";
import "core/api/error/v1/messages.proto";
```

❌ **Wrong:**

```protobuf
import "proto/core/common/v1/common.proto";
```

## Cross-Module Imports

Modules can import from each other:

```protobuf
// In core/events/v1/events.proto
import "core/common/v1/common.proto";

message BaseEvent {
  geniustechspace.core.common.v1.TenantContext tenant_context = 5;
}
```

```protobuf
// In core/api/error/v1/messages.proto
import "core/api/retry/v1/messages.proto";

message ErrorResponse {
  geniustechspace.core.retry.v1.RetryInfo retry_info = 5;
}
```

## Validation

All core modules use `buf/validate` for comprehensive validation:

```protobuf
import "buf/validate/validate.proto";

message Address {
  string country = 6 [(buf.validate.field).string = {
    min_len: 2
    max_len: 100
    ignore_empty: true
  }];
}
```

## Compliance and Security

### PII Handling

Modules containing PII (marked in header):

- `core/common/v1` - Address, ContactInfo
- `core/metadata/v1` - created_by, updated_by
- `core/device/v1` - Device identifiers
- `core/client/v1` - Client metadata
- `core/network/v1` - IP addresses
- `core/geo/v1` - Location data
- `core/session/v1` - User identifiers

### Security Requirements

1. **Encryption at Rest:** All PII fields
2. **Encryption in Transit:** TLS 1.3+ required
3. **Access Logging:** All PII access must be logged
4. **Data Minimization:** Only collect necessary data
5. **Retention Policies:** 90 days recommended, 1 year maximum

### Compliance Standards

- **GDPR:** Data protection, consent, right to erasure
- **SOC 2:** Access controls, audit trails, monitoring
- **ISO 27001:** Information security management
- **PCI DSS:** Payment data protection (Money type)
- **OWASP:** Security best practices
- **NIST 800-63B:** Digital identity guidelines

## Usage Examples

### Complete Request Example

```protobuf
import "core/common/v1/common.proto";
import "core/api/request/v1/messages.proto";
import "core/metadata/v1/metadata.proto";

message CreateUserRequest {
  // Tenant isolation
  geniustechspace.core.common.v1.TenantContext tenant_context = 1;

  // Request context
  geniustechspace.core.request.v1.RequestContext context = 2;

  // User data
  string email = 3;
  string first_name = 4;
  string last_name = 5;
  geniustechspace.core.common.v1.Address address = 6;
}

message User {
  // Audit trail
  geniustechspace.core.metadata.v1.Metadata metadata = 1;

  // User data
  string email = 2;
  string first_name = 3;
  string last_name = 4;
}
```

### Event-Driven Example

```protobuf
import "core/events/v1/events.proto";
import "core/common/v1/common.proto";
import "google/protobuf/any.proto";

message UserCreatedPayload {
  string user_id = 1;
  string email = 2;
}

// Publish event
geniustechspace.core.events.v1.BaseEvent event = {
  event_id: "evt_" + uuid(),
  event_type: "user.created",
  aggregate_id: user.metadata.id,
  aggregate_type: "user",
  tenant_context: tenant_context,
  occurred_at: now(),
  triggered_by: context.user_id,
  payload: Any.pack(UserCreatedPayload{...})
};
```

### Error Handling Example

```protobuf
import "core/api/error/v1/messages.proto";

message CreateUserResponse {
  oneof result {
    User user = 1;
    geniustechspace.core.error.v1.ErrorResponse error = 2;
  }
}

// Return error
ErrorResponse error = {
  message: "Email already exists",
  request_id: context.request_id,
  occurred_at: now(),
  details: [{
    validation: VALIDATION_ERROR_CODE_ALREADY_EXISTS,
    severity: ERROR,
    field: "email",
    message: "User with email user@example.com already exists"
  }]
};
```

## Testing

Before committing changes:

```bash
# Lint all proto files
buf lint

# Format all proto files
buf format -w

# Check breaking changes (PRs only)
buf breaking --against '.git#branch=main'

# Generate code for all languages
buf generate

# Verify Go compilation
cd gen/go && go mod init test && go build ./...
```

## Contributing

When adding new core modules:

1. Create versioned directory: `proto/core/<module>/v1/`
2. Follow naming convention: `geniustechspace.core.<module>.v1`
3. Add comprehensive documentation headers
4. Include validation annotations
5. Document compliance requirements
6. Update this README
7. Run `buf lint && buf generate`

## Support

For questions or issues:

- Review `docs/PROTO_DOCUMENTATION_STANDARD.md`
- Review `docs/VALIDATION.md`
- Check `CONTRIBUTING.md` for PR process
- See `QUICK_START.md` for installation

---

**Last Updated:** December 2025  
**Version:** 1.0  
**Maintainer:** GeniusTech Space Engineering Team
