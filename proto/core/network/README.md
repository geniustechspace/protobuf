# Core Network Context

Network connectivity and security analysis for request validation.

## Package

```protobuf
package geniustechspace.core.network.v1;
```

## Overview

Comprehensive network and connectivity metadata for security analysis, fraud detection, and risk assessment. Contains IP addresses and network details for threat detection.

## Messages

### NetworkContext

Complete network and connectivity metadata.

**Key Fields:**
- `ip_address` (string) - Client IP address (IPv4/IPv6)
- `ip_version` (IPVersion) - IP protocol version
- `proxy_ip` (string) - Proxy/VPN IP if detected
- `x_forwarded_for` (repeated string) - X-Forwarded-For chain
- `connection_type` (ConnectionType) - Network type
- `network_operator` / `network_name` - ISP or mobile operator
- `protocol` (Protocol) - Communication protocol
- `tls_version` (TLSVersion) - TLS version
- `cipher_suite` (string) - TLS cipher suite used
- `referer` / `accept_language` / `headers` - Request headers
- `latency_ms` / `bandwidth_mbps` / `quality` - Network characteristics
- `geo_location_id` (string) - Geographic location reference
- `security` (SecurityIndicators) - Security detection flags
- `asn` / `as_organization` - Autonomous System info
- `threat_score` / `threat_types` / `blacklisted` - Risk indicators
- `detected_at` (Timestamp) - Detection timestamp
- `metadata` (map<string, string>) - Additional metadata

### SecurityIndicators

Network security detection flags.

**Fields:**
- `vpn_detected` (bool) - VPN usage detected
- `tor_detected` (bool) - Tor exit node detected
- `datacenter_ip` (bool) - IP from datacenter/cloud provider
- `mobile_network` (bool) - Mobile carrier network
- `proxy_detected` (bool) - Proxy server detected
- `bot_detected` (bool) - Bot/automated traffic detected

### ConnectionInfo

Active connection tracking.

**Key Fields:**
- `connection_id` (string) - Connection identifier
- `state` (ConnectionState) - Connection state
- `established_at` / `last_activity_at` - Connection timestamps
- `bytes_sent` / `bytes_received` / `packets_sent` / `packets_received` - Traffic stats
- `idle_timeout_seconds` / `keep_alive` / `max_concurrent_streams` - Connection properties
- `metadata` (map<string, string>) - Additional metadata

## Enumerations

### IPVersion

- `IPV4`, `IPV6`

### ConnectionType

- `WIFI`, `CELLULAR`, `ETHERNET`, `VPN`, `BLUETOOTH`, `SATELLITE`

### Protocol

- `HTTP_1_0`, `HTTP_1_1`, `HTTP_2`, `HTTP_3`, `GRPC`, `WEBSOCKET`, `MQTT`, `AMQP`

### TLSVersion

- `TLS_1_0`, `TLS_1_1`, `TLS_1_2`, `TLS_1_3`

### NetworkQuality

- `EXCELLENT`, `GOOD`, `FAIR`, `POOR`, `OFFLINE`

### ConnectionState

- `CONNECTING`, `CONNECTED`, `IDLE`, `DISCONNECTING`, `DISCONNECTED`, `ERROR`

## Usage Examples

```protobuf
import "core/network/v1/messages.proto";

NetworkContext network = {
  ip_address: "203.0.113.42",
  ip_version: IPV4,
  connection_type: WIFI,
  protocol: HTTP_2,
  tls_version: TLS_1_3,
  network_operator: "Example ISP",
  asn: "AS15169",
  as_organization: "Google LLC",
  security: {
    vpn_detected: false,
    tor_detected: false,
    datacenter_ip: false,
    bot_detected: false
  },
  threat_score: 15,  // Low risk
  blacklisted: false
};
```

## Security Considerations

### IP Addresses are PII

Under GDPR, IP addresses are personal data:

1. **Anonymization:** Anonymize last octet when possible
2. **Retention:** Limit retention period (30-90 days)
3. **Access Control:** Restrict access to IP data
4. **Logging:** Log access to IP addresses

### Threat Detection

Use network context for:
- Bot detection
- VPN/Tor detection
- Datacenter IP detection
- Geographic anomalies
- Rate limiting by IP
- Blacklist checking

### Privacy Best Practices

```protobuf
// Anonymize IP address
anonymized_ip = anonymize_last_octet(ip_address)
// "203.0.113.42" → "203.0.113.0"
```

## Compliance

### GDPR

IP addresses are personal data under Article 4(1)

### Best Practices

1. **Anonymization:** Anonymize when full IP not needed
2. **Retention:** 30-90 days maximum
3. **Purpose:** Use only for security/fraud detection
4. **Access:** Restrict access to network data
5. **Logging:** Audit all IP data access

## Import Path

```protobuf
import "core/network/v1/messages.proto";
import "core/network/v1/enums.proto";
```

## See Also

- [Core Geo](../geo/README.md) - IP-based geolocation
- [Core Session](../session/README.md) - Session network binding
- [Main Core README](../README.md) - Complete core module documentation
