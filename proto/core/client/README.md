# Core Client Context

Client application tracking and feature detection for platform-specific behaviors.

## Package

```protobuf
package geniustechspace.core.client.v1;
```

## Overview

Comprehensive client application metadata for security, analytics, and feature compatibility. Tracks platform, version, capabilities, and trust level for risk-based authentication.

## Messages

### ClientContext

Complete client application metadata.

**Key Fields:**
- `client_id` (string) - Unique client identifier (1-128 chars)
- `client_name` / `client_version` / `build_number` - Client identification
- `user_agent` (string) - Full user agent string (max 2000 chars)
- `client_type` (ClientType) - Client category
- `platform` (ClientPlatform) - Application platform
- `platform_version` (string) - Platform OS version
- `app_id` / `app_name` / `app_version` - Application details
- `rendering_engine` (RenderingEngine) - Browser engine
- `trust_level` (ClientTrustLevel) - Trust/verification level
- `verified` / `verified_at` / `attestation` - Verification details
- `capabilities` (repeated ClientCapability) - Client capabilities
- `feature_flags` (map<string, bool>) - Feature flags for A/B testing
- `sdk_version` / `framework` / `framework_version` - SDK/framework info
- `locale` / `language` / `timezone` / `theme` - Localization
- `installed_at` / `last_updated_at` / `launch_count` - Lifecycle
- `metadata` (map<string, string>) - Additional properties

### ClientFingerprint

Unique client identification for fraud detection.

**Key Fields:**
- `fingerprint_hash` (string) - SHA-256 hash (64 chars)
- `user_agent` / `canvas_fingerprint` / `webgl_fingerprint` / `audio_fingerprint` - Browser fingerprints
- `fonts` / `plugins` - Installed fonts/plugins
- `vendor` / `renderer` - GPU details
- `generated_at` / `expires_at` / `confidence` - Fingerprint metadata
- `signals` (map<string, string>) - Additional signals

## Enumerations

### ClientType

- `WEB_BROWSER`, `MOBILE_APP`, `DESKTOP_APP`, `CLI`, `SERVICE`, `IOT_DEVICE`, `API_CLIENT`, `WEBHOOK`, `BROWSER_EXTENSION`

### ClientPlatform

- `IOS`, `ANDROID`, `WINDOWS`, `MACOS`, `LINUX`, `WEB`, `CHROMEOS`, `TVOS`, `WATCHOS`

### ClientTrustLevel

- `UNTRUSTED` (1) - Unknown client
- `KNOWN` (2) - Previously seen
- `TRUSTED` (3) - Explicitly trusted
- `VERIFIED` (4) - Platform attestation verified
- `FIRST_PARTY` (5) - First-party app
- `MANAGED` (6) - Enterprise-managed

### RenderingEngine

- `BLINK` (Chrome/Edge), `WEBKIT` (Safari), `GECKO` (Firefox), `TRIDENT` (IE), `EDGEHTML` (Edge Legacy)

### Framework

- `REACT`, `ANGULAR`, `VUE`, `FLUTTER`, `REACT_NATIVE`, `XAMARIN`, `ELECTRON`, `NEXT_JS`, `SVELTE`

### ClientCapability

- `PUSH_NOTIFICATIONS`, `BACKGROUND_SYNC`, `GEOLOCATION`, `CAMERA`, `MICROPHONE`, `BIOMETRIC`, `NFC`, `BLUETOOTH`, `OFFLINE_SUPPORT`, `SERVICE_WORKER`, `WEB_ASSEMBLY`, `WEBRTC`, `WEBSOCKETS`

## Usage Examples

```protobuf
import "core/client/v1/messages.proto";

ClientContext client = {
  client_id: "web_app_v1",
  client_name: "My Web App",
  client_version: "1.2.3",
  user_agent: "Mozilla/5.0...",
  client_type: WEB_BROWSER,
  platform: WEB,
  trust_level: VERIFIED,
  verified: true,
  framework: REACT,
  framework_version: "18.2.0",
  locale: "en-US",
  language: "en"
};
```

## Privacy Warnings

⚠️ **Client fingerprinting is privacy-invasive:**

- Quasi-identifiers combined enable user profiling
- Browser vendors (Safari, Firefox) actively block fingerprinting
- Use only for security/fraud detection, NOT advertising

## Compliance

### GDPR

- **Article 13:** Transparency in data collection required
- **Article 30:** Records of processing activities

### ePrivacy Directive

Cookie/tracking requires user consent

### CCPA

Users must be able to opt-out of tracking

### Browser Policies

Respect Do Not Track (DNT) signals

## Best Practices

1. **Consent:** Inform users about client tracking
2. **Opt-out:** Provide opt-out mechanism
3. **Purpose:** Use only for security purposes
4. **Minimize:** Collect only necessary data
5. **Retention:** 90 days recommended
6. **DNT:** Respect Do Not Track signals

## Import Path

```protobuf
import "core/client/v1/messages.proto";
import "core/client/v1/enums.proto";
```

## See Also

- [Core Device](../device/README.md) - Device identification
- [Core Session](../session/README.md) - Session client binding
- [Main Core README](../README.md) - Complete core module documentation
