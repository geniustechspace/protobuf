# Core Device Context

Device identification, fingerprinting, and risk assessment for security and fraud detection.

## Package

```protobuf
package geniustechspace.core.device.v1;
```

## Overview

Comprehensive device metadata structures for risk assessment, fraud detection, and device management. Contains sensitive information - use responsibly with proper consent mechanisms.

## Messages

### DeviceContext

Complete device metadata for risk assessment.

**Key Fields:**
- `device_id` (string) - Unique device identifier (1-128 chars)
- `device_name` (string) - User-assigned name (max 100 chars)
- `device_model` (string) - Device model (max 100 chars)
- `manufacturer` (string) - Device manufacturer (max 100 chars)
- `os` (OperatingSystem) - Operating system type
- `os_version` / `os_build` / `kernel_version` - OS details
- `cpu_architecture` (CPUArchitecture) - Processor architecture
- `cpu_cores` / `ram_mb` / `storage_gb` - Hardware specs
- `screen_width` / `screen_height` / `screen_dpi` / `screen_size_inches` - Display
- `capabilities` (repeated DeviceCapability) - Hardware/software capabilities
- `geo_location_id` (string) - Geolocation reference
- `trust_level` (DeviceTrustLevel) - Device trust level
- `jailbroken` / `emulator` / `debuggable` - Security flags
- `first_seen_at` / `last_seen_at` - Tracking timestamps
- `metadata` (map<string, string>) - Additional properties

### DeviceFingerprint

Stable device identification for fraud detection.

**Key Fields:**
- `fingerprint_hash` (string) - SHA-256 hash of components (64 chars)
- `device_id` / `vendor_id` / `advertising_id` / `hardware_id` - Identifiers
- `installed_apps` / `fonts` / `locale` / `timezone` - Software signals
- `generated_at` / `expires_at` - Fingerprint lifecycle
- `confidence` (float) - Confidence score (0.0-1.0)
- `stability_score` (int32) - Stability score (0-100)
- `signals` (map<string, string>) - Additional signals

## Enumerations

### OperatingSystem

- `IOS`, `ANDROID`, `WINDOWS`, `MACOS`, `LINUX`, `CHROMEOS`, `WATCHOS`, `TVOS`, `IPADOS`, `HARMONY`, `TIZEN`, `WEAR_OS`, `FIRE_OS`, `KAIOS`, and more

### CPUArchitecture

- `X86_64`, `ARM64`, `X86`, `ARM`, `ARMV7`, `ARMV8`, `RISCV`, `PPC64`, `S390X`, `MIPS`, `MIPS64`, `SPARC`, `WASM`

### DeviceCapability

- `TOUCHSCREEN`, `GPS`, `NFC`, `BLUETOOTH`, `WIFI`, `CELLULAR`, `CAMERA`, `MICROPHONE`
- `ACCELEROMETER`, `GYROSCOPE`, `MAGNETOMETER`, `BAROMETER`
- `BIOMETRIC`, `SECURE_ENCLAVE`, `TPM`, `TEE`
- `SCREEN_LOCK`, `ENCRYPTION`, `VPN`, `SANDBOX`

### DeviceTrustLevel

- `UNTRUSTED` (1) - Unknown/untrusted device
- `KNOWN` (2) - Previously seen device
- `TRUSTED` (3) - Explicitly trusted device
- `VERIFIED` (4) - Device verified (certificate, MDM)
- `MANAGED` (5) - Device managed by organization (MDM/EMM)
- `COMPLIANT` (6) - Device meets compliance policies

## Usage Examples

```protobuf
import "core/device/v1/messages.proto";

DeviceContext device = {
  device_id: "dev_abc123",
  device_model: "iPhone 15 Pro",
  manufacturer: "Apple",
  os: IOS,
  os_version: "17.2",
  cpu_architecture: ARM64,
  ram_mb: 8192,
  trust_level: TRUSTED,
  jailbroken: false,
  capabilities: [BIOMETRIC, NFC, GPS]
};
```

## Privacy Warnings

⚠️ **Device fingerprinting raises serious privacy concerns:**

- Combined device data enables cross-app tracking
- Hardware IDs (IMEI, serial numbers) are highly sensitive PII
- Screen resolution and capabilities are quasi-identifiers
- Use only for fraud/security purposes, NOT advertising

## Compliance

### GDPR

- **Article 6:** Lawful basis required for processing
- **Article 30:** Records of processing activities
- **Article 4(1):** Device identifiers are personal data

### ePrivacy Directive

Device tracking requires user consent

### CCPA

Device identifiers are personal information

### Best Practices

1. **Consent:** Implement proper consent mechanisms
2. **Transparency:** Inform users in privacy policy
3. **Purpose Limitation:** Use only for security/fraud detection
4. **Data Minimization:** Collect only necessary fields
5. **Retention:** 90 days recommended, 1 year maximum
6. **Reset:** Allow users to reset device fingerprint

## Import Path

```protobuf
import "core/device/v1/messages.proto";
import "core/device/v1/enums.proto";
```

## See Also

- [Core Client](../client/README.md) - Client application tracking
- [Core Session](../session/README.md) - Session device binding
- [Main Core README](../README.md) - Complete core module documentation
