# Group Domain Model

**Package:** `geniustechspace.idp.identity.group.v1`

## Overview

Domain entity and enums for group management in the IDP identity system.

## Purpose

- Define canonical Group entity structure
- Enforce tenant isolation
- Provide lifecycle status management
- Support organizational hierarchies and relationships

## Entities

### Group

Primary entity representing a group. Includes tenant_id, metadata, audit fields, and domain-specific attributes.

## Validation Rules

All fields use `buf/validate` annotations for request validation.

## Usage

```protobuf
import "idp/identity/group/v1/group.proto";

message MyMessage {
  geniustechspace.idp.identity.group.v1.Group group = 1;
}
```

## Related Documentation

- **Domain Events:** `../events/v1/README.md`
- **API Layer:** `../api/v1/README.md`
