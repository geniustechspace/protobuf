# Datastructure Context Modules

## Overview

Comprehensive context structures for the Genius Tech Space platform providing standardized metadata for devices, clients, networks, requests, and sessions.

## Module Structure

```
datastructure/v1/
├── auth/            # Authentication data structures (ChallengeData, RiskAssessment)
├── token/           # Token claims and metadata (TokenClaims, TokenMetadata)
├── device/          # Device hardware and OS context (DeviceContext)
├── client/          # Application and platform context (ClientContext)
├── network/         # Network connectivity and security context (NetworkContext)
├── geo/             # Geographic location context (GeoLocation)
├── request/         # HTTP/gRPC request metadata (RequestContext)
├── session/         # Session management (Session)
├── pagination/      # Pagination controls
├── error/           # Error responses
└── retry/           # Retry policies
```

## Context Packages

### Auth Context (`auth/`)

**Supporting data structures**: Authentication-related reusable structures

- Challenge data for multi-step auth flows
- Risk assessment for fraud detection
- User identifier with flexible lookup

### Token Context (`token/`)

**Token claims and metadata**: JWT and OAuth token structures

- Standard JWT claims (RFC 7519)
- OpenID Connect claims
- Token metadata and lifecycle
- Token introspection (RFC 7662)

### Device Context (`device/`)

**DeviceContext**: Comprehensive device hardware and OS metadata

- Device identification, model, manufacturer
- Operating system (name, version, build, kernel)
- Browser/runtime (web/hybrid apps)
- Hardware specs (CPU, RAM, storage, screen)
- Security (jailbroken, emulator, debug mode)
- Device capabilities and trust level
- Network and geographic location references

### Client Context (`client/`)

**ClientContext**: Application-level metadata and platform details

- Client identification, version, build
- Client type and platform classification
- Application details and trust level
- Capabilities and feature flags
- SDK and framework information
- Language, locale, timezone, screen properties
- Installation lifecycle tracking
- Client fingerprinting

### Network Context (`network/`)

**NetworkContext**: Network connectivity and security analysis

- IP addressing (IPv4/IPv6, proxy, X-Forwarded-For)
- Network type (WiFi, cellular, VPN)
- Protocol details (HTTP, TLS, cipher suite)
- Request headers and geographic location
- Network characteristics (latency, bandwidth)
- Security indicators (VPN, Tor, datacenter IP, ASN)
- Risk and reputation scores

### Geographic Context (`geo/`)

**GeoLocation**: Geographic location data

- Country, region, city, postal code
- Coordinates (latitude, longitude)
- Timezone and location source

### Request Context (`request/`)

**RequestContext**: Standardized request metadata

- Protocol and HTTP method
- User agent, client IP, locale
- Request priority and validation modes
- Device, client, network context references
- User authentication and RBAC
- Request correlation and tracing

### Session Context (`session/`)

**Session**: Enterprise session management

- Session identification and status
- User/client/agent identifiers
- Tenant context (multi-tenant)
- Authentication tokens and RBAC
- Comprehensive device/client/network context
- Session lifecycle and metadata

## Design Principles

1. **Single Responsibility**: Each context package focuses on a specific domain
2. **Comprehensive Coverage**: Include all relevant metadata for security and auditing
3. **Layered Composition**: Higher-level contexts reference lower-level contexts
4. **Backward Compatibility**: Legacy fields deprecated but retained
5. **Security by Design**: Never include secrets; anonymize PII where required
6. **Compliance**: GDPR, SOC 2, NIST 800-63B compliant

## Context Hierarchy

```
RequestContext
├── RequestMetadata
├── DeviceContext → NetworkContext → GeoLocation
├── ClientContext → ClientFingerprint
└── NetworkContext → GeoLocation

Session
├── DeviceContext → NetworkContext
├── ClientContext
└── NetworkContext
```

## Usage Examples

### Authentication with Full Context

```protobuf
import "proto/datastructure/v1/device/messages.proto";
import "proto/datastructure/v1/client/messages.proto";

message AuthenticationRequest {
  string email = 1;
  geniustechspace.datastructure.v1.device.DeviceContext device = 2;
  geniustechspace.datastructure.v1.client.ClientContext client = 3;
}
```

### Session with Context

```protobuf
import "proto/datastructure/v1/session/messages.proto";

service SessionService {
  rpc GetSession(GetSessionRequest)
    returns (geniustechspace.datastructure.v1.session.Session);
}
```

## Migration Guide

**From DeviceInfo → DeviceContext**:

```protobuf
// Old
DeviceInfo device_info = 1;

// New
geniustechspace.datastructure.v1.device.DeviceContext device = 1;
```

**From inline network fields → NetworkContext**:

```protobuf
// Old
string ip_address = 1;
string user_agent = 2;

// New
geniustechspace.datastructure.v1.network.NetworkContext network = 1;
```

## Security & Compliance

- **GDPR**: IP anonymization, consent for device IDs, data minimization
- **SOC 2**: Comprehensive audit trails, security monitoring
- **NIST 800-63B**: Device trust levels, risk-based authentication

## Best Practices

1. Always include device, client, and network context in auth requests
2. Implement device and client fingerprinting for fraud detection
3. Respect privacy: anonymize IPs, follow GDPR data minimization
4. Monitor trust levels for risk-based authentication
5. Validate all context data server-side
6. Cache context data with appropriate TTLs

## Performance

- **Selective Context**: Only include required fields
- **Fingerprint Caching**: Cache with appropriate TTLs
- **Lazy Loading**: Load expensive data asynchronously
- **Context Compression**: Use protobuf binary serialization
- **Edge Computing**: Compute context at edge for low latency
