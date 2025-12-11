# Session Domain Model

**Package:** `geniustechspace.idp.authn.session.v1`

## Overview

Domain entities and enums for session management in authentication workflows.

## Purpose

- Define session entity structure for authentication
- Enforce tenant isolation and security controls
- Support multi-factor authentication flows
- Comply with NIST 800-63B authentication standards

## Compliance

- **NIST 800-63B:** Digital identity authentication guidelines
- **SOC 2 CC6.1:** Logical access controls
- **ISO 27001 A.9.4:** Secret authentication information management

## Entities

### Session

Primary entity for session management. Contains tenant_id, user_id, status, and domain-specific security attributes.

## Security

- Sensitive data encrypted at rest
- Short-lived tokens for session management
- Credential hashing using industry-standard algorithms (bcrypt, Argon2)
- MFA enrollment and challenge verification

## Related Documentation

- **Domain Events:** `../events/v1/README.md`
- **API Layer:** `../api/v1/README.md`
