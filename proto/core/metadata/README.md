# Core Metadata

Entity lifecycle tracking, audit trails, and versioning for all domain entities.

## Package

```protobuf
package geniustechspace.core.metadata.v1;
```

## Overview

The `core/metadata` module provides comprehensive metadata tracking for entity lifecycles, including creation/modification timestamps, actor tracking, optimistic locking, and soft delete support.

## Messages

### Metadata

Complete audit trail and version control for entities.

**Fields:**
- `id` (string) - Unique entity identifier (1-128 chars, UUID v4 recommended)
- `created_at` (Timestamp) - Entity creation time (UTC, REQUIRED)
- `updated_at` (Timestamp) - Last modification time (UTC, REQUIRED)
- `created_by` (string) - User who created entity (1-128 chars, REQUIRED)
- `updated_by` (string) - User who last modified entity (1-128 chars, REQUIRED)
- `version` (int64) - Version number for optimistic locking (≥1, REQUIRED)
- `deleted` (bool) - Soft delete flag
- `deleted_at` (Timestamp) - Deletion timestamp (optional)

**Usage:**
```protobuf
import "core/metadata/v1/metadata.proto";

message User {
  geniustechspace.core.metadata.v1.Metadata metadata = 1;
  string email = 2;
  string first_name = 3;
  string last_name = 4;
}

message Tenant {
  geniustechspace.core.metadata.v1.Metadata metadata = 1;
  string name = 2;
  // ... other fields
}
```

## Features

### Audit Trail

Tracks complete entity lifecycle:
- **Who** created/modified (created_by, updated_by)
- **When** created/modified (created_at, updated_at)
- **What** entity (id)
- **Deletion** tracking (deleted, deleted_at)

**Compliance:** SOC 2 CC6.3, GDPR Article 5(2)

### Optimistic Locking

Prevents concurrent update conflicts:

1. Client reads entity with `version=5`
2. Client modifies entity locally
3. Client sends update with `version=5`
4. Server validates: if current `version != 5`, reject (conflict)
5. Server increments to `version=6` on success

**Example:**
```go
// Read
user := GetUser(id) // version = 5

// Update attempt
user.email = "new@example.com"
err := UpdateUser(user, expectedVersion: 5)
if err == VersionConflict {
  // Handle conflict - someone else updated
  // Typical strategies:
  // 1. Reload and retry
  // 2. Show conflict to user
  // 3. Merge changes
}
```

### Soft Delete

Logical deletion without physical removal:

- **Retention:** Data retained for audit trails, compliance, legal holds
- **Behavior:** When `deleted=true`, entity hidden from normal queries
- **Recovery:** Special queries can retrieve deleted entities
- **Cleanup:** Physical deletion after retention period

**Usage:**
```protobuf
// Soft delete
user.metadata.deleted = true;
user.metadata.deleted_at = now();

// Query excluding deleted
SELECT * FROM users WHERE metadata.deleted = false;

// Query including deleted (admin/audit)
SELECT * FROM users WHERE metadata.deleted = true;
```

**Compliance:** GDPR Article 17 (Right to erasure with retention)

## Field Details

### id

- **Format:** UUID v4, ULID, or prefixed ID (e.g., "usr_01HQZX...")
- **Generation:** Server-side on creation
- **Immutable:** Never changes after creation
- **Uniqueness:** Global uniqueness recommended

### created_at / updated_at

- **Timezone:** Always UTC
- **Format:** RFC 3339 (2025-12-06T12:34:56Z)
- **Generation:** Automatic server-side
- **Immutable:** created_at never changes; updated_at changes on every update

### created_by / updated_by

- **Format:** User ID from authentication context
- **Examples:** "usr_123", "service:api-gateway", "system"
- **PII:** Yes - user identifiers are PII
- **Audit:** Required for accountability and forensics

### version

- **Initial:** Starts at 1 on creation
- **Increment:** +1 on every successful update
- **Concurrency:** Used for optimistic locking
- **Validation:** Client must provide expected version for updates

### deleted / deleted_at

- **Soft Delete:** Mark entities as deleted without physical removal
- **Retention:** Support data retention policies
- **Compliance:** Required for GDPR, legal holds, e-discovery
- **Queries:** Filter on deleted flag for normal vs. audit queries

## Import Path

```protobuf
import "core/metadata/v1/metadata.proto";
```

## Best Practices

### Entity Design

Always embed Metadata as first field:

```protobuf
message MyEntity {
  geniustechspace.core.metadata.v1.Metadata metadata = 1;
  // ... entity-specific fields
}
```

### Update Operations

```protobuf
message UpdateUserRequest {
  string user_id = 1;
  int64 expected_version = 2;  // For optimistic locking
  User user = 3;
}

message UpdateUserResponse {
  oneof result {
    User user = 1;
    VersionConflictError conflict = 2;
  }
}
```

### Deletion Operations

```protobuf
message DeleteUserRequest {
  string user_id = 1;
  bool hard_delete = 2;  // true = physical, false = soft (default)
}
```

### Audit Queries

```protobuf
message ListAuditTrailRequest {
  string entity_type = 1;  // "user", "tenant", etc.
  string entity_id = 2;
  google.protobuf.Timestamp start_time = 3;
  google.protobuf.Timestamp end_time = 4;
}
```

## Compliance

### SOC 2 CC6.3 (Change Management)

- Tracks all entity changes
- Records who made changes
- Timestamps all modifications
- Supports audit trails

### GDPR Article 5(2) (Accountability)

- Demonstrates compliance with data protection principles
- Provides evidence of data processing
- Supports data subject rights

### GDPR Article 17 (Right to Erasure)

- Soft delete supports "right to be forgotten"
- Balances erasure with retention requirements
- Enables legal holds and e-discovery

## See Also

- [Core Events](../events/README.md) - Event sourcing with metadata
- [Core Common](../common/README.md) - Common value objects
- [Main Core README](../README.md) - Complete core module documentation
