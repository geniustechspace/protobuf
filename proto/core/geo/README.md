# Core Geolocation

Geographic location value objects for IP-based and GPS-based location tracking.

## Package

```protobuf
package geniustechspace.core.geo.v1;
```

## Overview

Geolocation data structures for geographic targeting, fraud detection, and compliance. Location data is highly sensitive PII requiring user consent.

## Messages

### GeoLocation

Geographic location data with coordinates and metadata.

**Fields:**
- `country_code` (string) - ISO 3166-1 alpha-2 country code
- `country` (string) - Country name
- `region` (string) - State/province/region
- `city` (string) - City name
- `town` (string) - Town/district
- `postal_code` (string) - Postal/ZIP code
- `latitude` (double) - Latitude coordinate
- `longitude` (double) - Longitude coordinate
- `timezone` (string) - IANA timezone (e.g., "America/New_York")
- `determined_at` (Timestamp) - When location was determined (UTC)
- `source` (GeoLocationSource) - Source of geolocation data
- `metadata` (map<string, string>) - Additional metadata (no PII)

## Enumerations

### GeoLocationSource

Source of geolocation data:

- `IP` (1) - IP address geolocation (least accurate, 50-100km)
- `GPS` (2) - GPS/GNSS coordinates (most accurate, <10m)
- `WIFI` (3) - WiFi triangulation (10-50m accuracy)
- `CELLULAR` (4) - Cell tower triangulation (50-500m accuracy)
- `USER` (5) - User-provided location
- `MANUAL` (6) - Manually entered
- `GEOCODING` (7) - Reverse geocoding from address
- `BLUETOOTH` (8) - Bluetooth beacon
- `HYBRID` (9) - Multiple sources combined

## Usage Examples

### IP-Based Geolocation

```protobuf
import "core/geo/v1/messages.proto";

GeoLocation location = {
  country_code: "US",
  country: "United States",
  region: "California",
  city: "San Francisco",
  postal_code: "94102",
  latitude: 37.7749,
  longitude: -122.4194,
  timezone: "America/Los_Angeles",
  source: IP,
  determined_at: now()
};
```

### GPS-Based Geolocation

```protobuf
GeoLocation location = {
  country_code: "GB",
  country: "United Kingdom",
  region: "England",
  city: "London",
  latitude: 51.5074,
  longitude: -0.1278,
  timezone: "Europe/London",
  source: GPS,
  determined_at: now()
};
```

### Hybrid Geolocation

```protobuf
GeoLocation location = {
  // Combined IP + WiFi + GPS for best accuracy
  country_code: "JP",
  city: "Tokyo",
  latitude: 35.6762,
  longitude: 139.6503,
  timezone: "Asia/Tokyo",
  source: HYBRID,
  determined_at: now()
};
```

## Accuracy by Source

| Source | Typical Accuracy | Use Case |
|--------|------------------|----------|
| GPS | <10m | Navigation, delivery |
| WiFi | 10-50m | Indoor location |
| Cellular | 50-500m | Approximate location |
| IP | 50-100km | Country/city level |
| User | Varies | Self-reported |

## Privacy Warnings

⚠️ **Location data is highly sensitive PII:**

- Reveals home address, workplace, movement patterns
- Can identify individuals even without names
- Subject to strict regulations (GDPR, CCPA)
- Requires explicit user consent

### Privacy Best Practices

1. **Consent:** Explicit opt-in required for precise location
2. **Transparency:** Explain why location is needed
3. **Minimization:** Use least precise location needed
4. **Anonymization:** Remove exact coordinates when possible
5. **Retention:** Short retention periods (30-90 days)
6. **Access Control:** Restrict access to location data

### Data Minimization

```protobuf
// For fraud detection - city level is enough
GeoLocation location = {
  country_code: "US",
  city: "San Francisco",
  // Don't store: latitude, longitude, postal_code
  source: IP
};

// For delivery - precise coordinates needed
GeoLocation location = {
  country_code: "US",
  city: "San Francisco",
  postal_code: "94102",
  latitude: 37.7749,
  longitude: -122.4194,
  source: GPS
};
```

## Compliance

### GDPR

- **Article 4(1):** Location data is personal data
- **Article 9:** Precise location may be sensitive data
- **Article 6:** Requires lawful basis (usually consent)
- **Article 7:** Consent must be freely given, specific, informed
- **Article 17:** Right to erasure applies

### CCPA

Location data is personal information requiring disclosure

### ePrivacy Directive

Location tracking requires informed consent

### COPPA

Special protections for children's location data

## Use Cases

### Fraud Detection

```protobuf
// Check if IP location matches user's stated country
if user.country != network.geo_location.country_code {
  flag_suspicious_activity()
}
```

### Content Localization

```protobuf
// Serve localized content based on location
content_language = get_language(geo_location.country_code)
content_currency = get_currency(geo_location.country_code)
```

### Geofencing

```protobuf
// Check if user is in allowed region
if !is_in_region(geo_location, allowed_regions) {
  return RegionRestrictedError
}
```

### Timezone Detection

```protobuf
// Auto-detect user timezone
user.timezone = geo_location.timezone
```

## Import Path

```protobuf
import "core/geo/v1/messages.proto";
import "core/geo/v1/enums.proto";
```

## See Also

- [Core Network](../network/README.md) - IP-based geolocation
- [Core Device](../device/README.md) - Device GPS capabilities
- [Main Core README](../README.md) - Complete core module documentation
