# Profile Domain Events

**Package:** `geniustechspace.idp.identity.profile.events.v1`

## Overview

Domain events published when profile entity undergoes state changes. Supports event-driven architecture patterns.

## Purpose

- Decouple profile service from downstream consumers
- Enable audit trails and compliance logging
- Support event sourcing patterns
- Trigger downstream workflows

## Events

### ProfileCreated

Published when new profile is created.

**Trigger:** `CreateProfile` RPC  
**Consumers:** Audit service, notification service, analytics

### ProfileUpdated

Published when profile is modified.

**Trigger:** `UpdateProfile` RPC  
**Consumers:** Search index, cache invalidation, audit log

### ProfileDeleted

Published when profile is deleted (soft or hard).

**Trigger:** `DeleteProfile` RPC  
**Consumers:** Audit service, cleanup jobs

## Event Bus Integration

**Topic Convention:** `idp.identity.profile.{created|updated|deleted}.v1`

**Serialization:** Protocol Buffers binary format or JSON

## Related Documentation

- **Domain Model:** `../v1/README.md`
- **API Layer:** `../api/v1/README.md`
