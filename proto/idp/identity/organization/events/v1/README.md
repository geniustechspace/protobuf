# Organization Domain Events

**Package:** `geniustechspace.idp.identity.organization.events.v1`

## Overview

Domain events published when organization entity undergoes state changes. Supports event-driven architecture patterns.

## Purpose

- Decouple organization service from downstream consumers
- Enable audit trails and compliance logging
- Support event sourcing patterns
- Trigger downstream workflows

## Events

### OrganizationCreated

Published when new organization is created.

**Trigger:** `CreateOrganization` RPC  
**Consumers:** Audit service, notification service, analytics

### OrganizationUpdated

Published when organization is modified.

**Trigger:** `UpdateOrganization` RPC  
**Consumers:** Search index, cache invalidation, audit log

### OrganizationDeleted

Published when organization is deleted (soft or hard).

**Trigger:** `DeleteOrganization` RPC  
**Consumers:** Audit service, cleanup jobs

## Event Bus Integration

**Topic Convention:** `idp.identity.organization.{created|updated|deleted}.v1`

**Serialization:** Protocol Buffers binary format or JSON

## Related Documentation

- **Domain Model:** `../v1/README.md`
- **API Layer:** `../api/v1/README.md`
