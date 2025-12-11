# Session API Layer

**Package:** `geniustechspace.idp.authn.session.api.v1`

## Overview

gRPC service for session management in authentication flows.

## Service: SessionService

### Authentication

All RPCs require Bearer token or specific authentication challenge credentials.

### Authorization

Permission-based access control for session operations.

### Rate Limits

Authentication operations have strict rate limits to prevent abuse:
- Validation/verification: 10/min per user
- Creation: 20/min per tenant
- Listing: 50/min per tenant

## Security

- Credentials never returned in plaintext
- Session tokens short-lived (configurable TTL)
- MFA challenges time-bound (5-minute expiry)
- Failed authentication attempts logged and rate-limited

## Compliance

- **NIST 800-63B:** Authentication assurance levels
- **SOC 2 CC6.1/CC6.7:** Access control and session management
- **ISO 27001 A.9.4:** Secret authentication information

## Related Documentation

- **Domain Model:** `../v1/README.md`
- **Domain Events:** `../events/v1/README.md`
