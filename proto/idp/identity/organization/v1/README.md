# Organization Domain Model

**Package:** `geniustechspace.idp.identity.organization.v1`

## Overview

Domain entity and enums for organization management in the IDP identity system.

## Purpose

- Define canonical Organization entity structure
- Enforce tenant isolation
- Provide lifecycle status management
- Support organizational hierarchies and relationships

## Entities

### Organization

Primary entity representing a organization. Includes tenant_id, metadata, audit fields, and domain-specific attributes.

## Validation Rules

All fields use `buf/validate` annotations for request validation.

## Usage

```protobuf
import "idp/identity/organization/v1/organization.proto";

message MyMessage {
  geniustechspace.idp.identity.organization.v1.Organization organization = 1;
}
```

## Related Documentation

- **Domain Events:** `../events/v1/README.md`
- **API Layer:** `../api/v1/README.md`
