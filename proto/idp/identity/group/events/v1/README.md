# Group Domain Events

**Package:** `geniustechspace.idp.identity.group.events.v1`

## Overview

Domain events published when group entity undergoes state changes. Supports event-driven architecture patterns.

## Purpose

- Decouple group service from downstream consumers
- Enable audit trails and compliance logging
- Support event sourcing patterns
- Trigger downstream workflows

## Events

### GroupCreated

Published when new group is created.

**Trigger:** `CreateGroup` RPC  
**Consumers:** Audit service, notification service, analytics

### GroupUpdated

Published when group is modified.

**Trigger:** `UpdateGroup` RPC  
**Consumers:** Search index, cache invalidation, audit log

### GroupDeleted

Published when group is deleted (soft or hard).

**Trigger:** `DeleteGroup` RPC  
**Consumers:** Audit service, cleanup jobs

## Event Bus Integration

**Topic Convention:** `idp.identity.group.{created|updated|deleted}.v1`

**Serialization:** Protocol Buffers binary format or JSON

## Related Documentation

- **Domain Model:** `../v1/README.md`
- **API Layer:** `../api/v1/README.md`
