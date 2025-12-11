# User Domain Events

**Package:** `geniustechspace.idp.identity.user.events.v1`

## Overview

Domain events published when user entity undergoes state changes. Enables event-driven architecture (EDA) patterns across microservices consuming user lifecycle events.

## Purpose

- Decouple user service from downstream consumers
- Enable audit trail and compliance logging
- Support event sourcing and CQRS patterns
- Trigger workflows (e.g., welcome email on UserCreated)
- Maintain read model consistency in distributed systems

## Events

All events follow a consistent structure:

**Common Fields (1-16):**

- Event metadata: `event_id`, `tenant_id`, `event_timestamp`, `user_id`
- Business context: domain-specific fields
- Tracing: `correlation_id`, `metadata`

**Reserved Fields (17-19):** Reserved for future expansion

**Event Sourcing (20-21):** Entity snapshots

- `user_snapshot` - Complete entity state (for reconstruction)
- `user_snapshot_before` / `user_snapshot_after` - State before/after change

**Reserved Fields (22-29):** Reserved for future expansion

**Audit Context (30-33):** Traceability fields (always last)

- `session_id` - User session that triggered event
- `device_id` - Device reference for fraud detection
- `client_id` - Client application reference
- `network_id` - Network/IP context reference

### UserCreated

Published when new user account is successfully created.

**Trigger:** `CreateUser` RPC completes successfully  
**Consumers:** Notification service, audit service, analytics, welcome email workflow  
**Idempotency:** Use `event_id` to deduplicate

**Key Fields:**

- `event_id`, `tenant_id`, `event_timestamp` - Event identification
- `user_id`, `email`, `username`, `display_name` - User data
- `created_by`, `source` - Actor and creation source
- `password_set`, `email_verified` - Setup status
- `external_provider` - SSO/federated identity
- `correlation_id` - Distributed tracing
- `user_snapshot` - Complete User entity state after creation
- `session_id`, `device_id`, `client_id`, `network_id` - Audit context

**Example:**

```json
{
  "metadata": { "event_id": "evt_abc123", "timestamp": "2024-01-15T10:30:00Z" },
  "tenant_id": "tnt_xyz",
  "user_id": "usr_123",
  "email": "user@example.com",
  "display_name": "John Doe",
  "created_by": "admin_usr_456"
}
```

### UserUpdated

Published when user profile or memberships are modified.

**Trigger:** `UpdateUser` RPC completes successfully  
**Consumers:** Search index, notification service, audit log, cache invalidation  
**Idempotency:** Use `event_id` to deduplicate

**Key Fields:**

- `updated_by` - Actor who performed update
- `changed_fields` - Array of field names that changed
- `previous_values`, `new_values` - Change tracking (JSON maps)
- `reason` - Optional update reason
- `user_snapshot_before`, `user_snapshot_after` - State before/after update
- Audit context: `session_id`, `device_id`, `client_id`, `network_id`

**Use Case:** Inspect `changed_fields` to determine if relevant changes occurred (e.g., email changed → trigger verification flow).

### UserDeleted

Published when user account is soft-deleted or hard-deleted.

**Trigger:** `DeleteUser` RPC completes successfully  
**Consumers:** Audit service, data retention service, cleanup jobs  
**Compliance:** GDPR Article 17 (Right to erasure)

**Key Fields:**

- `deleted_by` - Actor who performed deletion
- `deletion_type` - SOFT_DELETE, HARD_DELETE, or GDPR_ERASURE
- `reason` - Deletion reason (audit trail)
- `hard_delete_scheduled`, `hard_delete_at` - Scheduled permanent deletion
- `gdpr_erasure_request` - GDPR compliance flag
- `user_snapshot_before` - Final state before deletion
- Audit context: `session_id`, `device_id`, `client_id`, `network_id`

**Data Retention:**

- SOFT_DELETE: User marked deleted, data retained per policy
- HARD_DELETE: Permanent erasure, consumers purge data
- GDPR_ERASURE: Right to erasure, comprehensive data removal

### UserStatusChanged

Published when user status transitions (e.g., ACTIVE → SUSPENDED).

**Trigger:** `UpdateUserStatus` RPC completes successfully  
**Consumers:** Access control service, notification service, audit log  
**Security:** Status changes may affect active sessions (e.g., SUSPENDED → invalidate sessions)

**Key Fields:**

- `previous_status`, `new_status` - Status transition
- `reason` - Change reason (e.g., "Policy violation")
- `automatic` - Whether change was automatic (policy) or manual (admin)
- `changed_by` - Actor who changed status
- `user_snapshot_after` - State after status change
- Audit context: `session_id`, `device_id`, `client_id`, `network_id`

### Additional Events

**UserEmailVerified** - Email verification completed  
**UserPhoneVerified** - Phone verification completed  
**UserPasswordChanged** - Password updated (critical security event)  
**UserLocked** - Account locked (security/brute force)  
**UserUnlocked** - Account unlocked by admin

All events include full audit context and entity snapshots for event sourcing.

## Event Bus Integration

**Recommended Event Bus:** Apache Kafka, RabbitMQ, AWS EventBridge, Google Pub/Sub

**Topic Naming Convention:**

- `idp.identity.user.created.v1`
- `idp.identity.user.updated.v1`
- `idp.identity.user.deleted.v1`
- `idp.identity.user.status_changed.v1`

**Message Format:** Serialize events using Protocol Buffers binary format or JSON

**Ordering:** Use `user_id` as partition key to guarantee ordering per user

## Consuming Events

### Example Consumer (Go)

```go
import userevent "github.com/geniustechspace/protobuf/gen/go/idp/identity/user/events/v1"

func HandleUserCreated(msg []byte) error {
    var event userevent.UserCreated
    if err := proto.Unmarshal(msg, &event); err != nil {
        return err
    }

    // Check idempotency
    if alreadyProcessed(event.Metadata.EventId) {
        return nil
    }

    // Process event (e.g., send welcome email)
    sendWelcomeEmail(event.Email, event.DisplayName)

    // Mark as processed
    markProcessed(event.Metadata.EventId)
    return nil
}
```

## Validation

Events include `buf/validate` annotations:

- `tenant_id`, `user_id` - Must be valid UUIDs
- `email` - RFC 5322 format (in UserCreated)
- `updated_fields` - Non-empty array (in UserUpdated)
- `old_status`, `new_status` - Must be defined enum values (in UserStatusChanged)

## Compliance

- **SOC 2 CC6.1:** Events provide audit trail for user provisioning changes
- **GDPR Article 30:** Events contribute to record of processing activities
- **Retention:** Event logs retained per regulatory requirements (typically 7 years)

## PII Considerations

⚠️ **Events contain personal data:**

- `email`, `display_name` are PII per GDPR Article 4(1)
- `phone_number` (if included) requires encryption in transit/rest
- Event bus must enforce tenant isolation
- Consumers must handle PII per data processing agreements

**Recommendation:** Minimize PII in events. Consider publishing user_id only, let consumers fetch details via API if needed.

## Idempotency

All events include `metadata.event_id` (UUID) for deduplication:

```protobuf
message UserCreated {
  core.v1.Metadata metadata = 1;  // Contains event_id
  // ...
}
```

Consumers MUST implement idempotent processing to handle duplicate deliveries.

## Versioning

Events follow package versioning (`events.v1`). For breaking changes:

1. Create `events.v2` package
2. Publish both v1 and v2 events during migration
3. Deprecate v1 after consumer migration complete

## Testing

Mock events for unit testing:

```go
event := &userevent.UserCreated{
    Metadata: &corev1.Metadata{
        EventId: "test_evt_123",
        Timestamp: timestamppb.Now(),
    },
    TenantId: "test_tenant",
    UserId: "test_user",
    Email: "test@example.com",
}
```

## Related Documentation

- **Domain Model:** `../v1/README.md` - User entity definition
- **API Layer:** `../api/v1/README.md` - gRPC operations that trigger events
- **Core Events:** `../../../../core/v1/events.proto` - Common event metadata
