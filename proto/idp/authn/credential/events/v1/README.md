# Credential Domain Events

**Package:** `geniustechspace.idp.authn.credential.events.v1`

## Overview

Domain events for credential lifecycle changes in authentication workflows.

## Purpose

- Track authentication security events
- Enable audit trails for compliance (SOC 2, ISO 27001)
- Trigger security workflows (e.g., anomaly detection)
- Support incident response and forensics

## Events

Events published for credential creation, validation, expiration, and revocation actions.

## Security Considerations

Events may contain sensitive metadata (IP addresses, device fingerprints). Ensure secure event bus configuration with encryption in transit.

## Related Documentation

- **Domain Model:** `../v1/README.md`
- **API Layer:** `../api/v1/README.md`
