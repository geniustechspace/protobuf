# Context Architecture - Single Responsibility Design

## Overview

Each context structure has a single, well-defined responsibility with no field duplication across contexts. Higher-level contexts compose lower-level contexts through references.

## Context Responsibilities

### 1. GeoLocation (`datastructure/v1/geo/`)

**Single Responsibility**: Geographic location data

**Fields** (source of truth):

- Country (code, name)
- Region, city, postal code
- Coordinates (latitude, longitude)
- Timezone
- Location source and timestamp

**Used By**: DeviceContext (GPS), Session, RequestContext (IP-derived)

---

### 2. DeviceContext (`datastructure/v1/device/`)

**Single Responsibility**: Physical device hardware and OS

**Fields** (source of truth):

- Device identification (ID, model, manufacturer)
- Operating system (name, version, build, kernel)
- Hardware specs (CPU architecture, cores, RAM, storage)
- Device capabilities (touchscreen, GPS, NFC)
- Security indicators (jailbroken, emulator, debug mode, trust level)
- **GPS location** → references GeoLocation
- Device timestamps (first/last seen)

**Does NOT contain**:

- ❌ Browser info → moved to ClientContext
- ❌ Display properties → moved to ClientContext
- ❌ Network info → use NetworkContext separately
- ❌ User agent → moved to ClientContext
- ❌ IP address → in NetworkContext

---

### 3. ClientContext (`datastructure/v1/client/`)

**Single Responsibility**: Application/client software metadata

**Fields** (source of truth):

- Client identification (ID, name, version, build)
- **User agent string**
- Client type and platform
- Application details (app ID, name, version)
- **Browser info** (name, version, rendering engine)
- Trust and verification (attestation, signature)
- Capabilities and feature flags
- SDK and framework info
- Language, locale, timezone
- **Display properties** (screen width, height, density, color scheme)
- Installation lifecycle

**Does NOT contain**:

- ❌ Hardware specs → in DeviceContext
- ❌ Network info → in NetworkContext
- ❌ IP address → in NetworkContext

---

### 4. NetworkContext (`datastructure/v1/network/`)

**Single Responsibility**: Network connectivity and security

**Fields** (source of truth):

- IP addressing (IP, version, proxy IP, X-Forwarded-For)
- Network type (WiFi, cellular, ethernet, VPN)
- Network operator and name
- Protocol details (HTTP version, TLS, cipher suite)
- Request headers (Referer, Accept-Language)
- Network characteristics (latency, bandwidth, quality)
- Security indicators (VPN, Tor, datacenter IP, ASN)
- Risk and reputation (threat score, blacklist status)

**Does NOT contain**:

- ❌ User agent → in ClientContext
- ❌ Geographic location → use GeoLocation separately
- ❌ Device info → in DeviceContext

---

### 5. RequestContext (`datastructure/v1/request/`)

**Single Responsibility**: Request metadata and authorization

**Composition** (references only):

- RequestMetadata (protocol, method, timeout, priority)
- → DeviceContext
- → ClientContext
- → NetworkContext
- → GeoLocation (IP-derived)
- User authentication (user ID, tenant, session, roles, permissions)
- Request tracing (correlation ID, request ID, timestamps)

**Does NOT contain**:

- ❌ Inline device fields → references DeviceContext
- ❌ Inline client fields → references ClientContext
- ❌ Inline network fields → references NetworkContext

---

### 6. Session (`datastructure/v1/session/`)

**Single Responsibility**: Session state and lifecycle

**Composition** (references only):

- Session identification and status
- User/client/agent identifiers
- Tenant context
- Authentication tokens
- Roles and permissions
- Session timestamps
- → DeviceContext
- → ClientContext
- → NetworkContext
- → GeoLocation (IP-derived)
- Legacy deprecated fields (for migration)

**Does NOT contain**:

- ❌ Inline device fields → references DeviceContext
- ❌ Inline client fields → references ClientContext
- ❌ Inline network fields → references NetworkContext

---

## Composition Hierarchy

```
RequestContext
├── RequestMetadata (inline: protocol, method, headers)
├── DeviceContext → GeoLocation (GPS)
├── ClientContext (inline: all client fields)
├── NetworkContext (inline: all network fields)
└── GeoLocation (IP-derived, separate from device GPS)

Session
├── Session fields (inline: session ID, tokens, roles, timestamps)
├── DeviceContext → GeoLocation (GPS)
├── ClientContext (inline: all client fields)
├── NetworkContext (inline: all network fields)
└── GeoLocation (IP-derived, separate from device GPS)
```

---

## Single Source of Truth Matrix

| Field Category               | Source of Truth                  | Used In                 |
| ---------------------------- | -------------------------------- | ----------------------- |
| **Device Hardware**          | DeviceContext                    | Session, RequestContext |
| **Operating System**         | DeviceContext                    | Session, RequestContext |
| **Device Security**          | DeviceContext                    | Session, RequestContext |
| **GPS Location**             | GeoLocation (in DeviceContext)   | DeviceContext           |
| **Browser Info**             | ClientContext                    | Session, RequestContext |
| **User Agent**               | ClientContext                    | Session, RequestContext |
| **Display Properties**       | ClientContext                    | Session, RequestContext |
| **Client App Info**          | ClientContext                    | Session, RequestContext |
| **Language/Locale/Timezone** | ClientContext                    | Session, RequestContext |
| **IP Address**               | NetworkContext                   | Session, RequestContext |
| **Network Type**             | NetworkContext                   | Session, RequestContext |
| **Protocol/TLS**             | NetworkContext                   | Session, RequestContext |
| **Network Security**         | NetworkContext                   | Session, RequestContext |
| **IP-derived Location**      | GeoLocation (in Session/Request) | Session, RequestContext |

---

## Benefits

### ✅ No Duplication

- Each field exists in exactly one context
- No coordination issues when updating fields
- Clear ownership and responsibility

### ✅ Single Responsibility

- DeviceContext = hardware only
- ClientContext = software only
- NetworkContext = connectivity only
- GeoLocation = geographic data only

### ✅ Composability

- Higher-level contexts reference lower-level contexts
- No inline duplication of fields
- Easy to add/remove contexts

### ✅ Maintainability

- Change a field once in its source context
- All consumers automatically see the update
- No risk of inconsistent definitions

### ✅ Clear Boundaries

- Device = physical hardware
- Client = application software
- Network = connectivity layer
- Geo = location data

---

## Usage Patterns

### Minimal Context

```protobuf
message AuthRequest {
  string email = 1;
  geniustechspace.datastructure.v1.network.NetworkContext network = 2;
}
```

### Full Context

```protobuf
message AuthRequest {
  string email = 1;
  geniustechspace.datastructure.v1.device.DeviceContext device = 2;
  geniustechspace.datastructure.v1.client.ClientContext client = 3;
  geniustechspace.datastructure.v1.network.NetworkContext network = 4;
}
```

### Selective Context

```protobuf
// Risk assessment: need device security and network threat info
message RiskAssessmentRequest {
  geniustechspace.datastructure.v1.device.DeviceContext device = 1;
  geniustechspace.datastructure.v1.network.NetworkContext network = 2;
}

// Analytics: need client and geo info only
message AnalyticsEvent {
  geniustechspace.datastructure.v1.client.ClientContext client = 1;
  geniustechspace.datastructure.v1.geo.GeoLocation geo = 2;
}
```

---

## Migration Strategy

### Phase 1: Update context definitions ✅

- Removed duplicated fields from each context
- Established single source of truth per field
- Added proper context references

### Phase 2: Update consumers (Next)

- Update services to populate separate contexts
- Stop setting deprecated fields in Session
- Migrate from inline fields to context references

### Phase 3: Remove deprecated fields (Future)

- Remove deprecated Session fields after migration period
- Remove any remaining inline field patterns
- Fully enforce composition-only pattern

---

## Field Location Quick Reference

**Looking for...**

- `user_agent`? → ClientContext
- `ip_address`? → NetworkContext
- `browser`? → ClientContext
- `screen_width/height`? → ClientContext
- `os_version`? → DeviceContext
- `jailbroken`? → DeviceContext
- `vpn_detected`? → NetworkContext
- `locale/timezone`? → ClientContext
- `latitude/longitude`? → GeoLocation
- `cpu_cores`? → DeviceContext
- `tls_version`? → NetworkContext
- `feature_flags`? → ClientContext

---

## Validation

✅ **No field duplication across contexts**
✅ **Each field has exactly one source of truth**
✅ **Composition via references, not inline copies**
✅ **Clear responsibility boundaries**
✅ **All proto files compile without errors**
