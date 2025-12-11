# Role Domain Events

**Package:** `geniustechspace.idp.authz.role.events.v1`

## Overview

Domain events for role lifecycle changes in authorization workflows.

## Purpose

- Track authorization configuration changes
- Enable audit trails for compliance (SOC 2 CC6.1)
- Trigger cache invalidation for authorization decisions
- Support access review workflows

## Events

Events published for role creation, updates, assignments, and removals.

## Security Considerations

Authorization changes must be propagated immediately to prevent stale access. Events trigger cache invalidation and policy re-evaluation.

## Related Documentation

- **Domain Model:** `../v1/README.md`
- **API Layer:** `../api/v1/README.md`
