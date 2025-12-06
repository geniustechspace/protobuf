# Core Events

Event sourcing foundation for event-driven architecture and CQRS patterns.

## Package

```protobuf
package geniustechspace.core.events.v1;
```

## Overview

The `core/events` module provides standardized event structures for event sourcing, event-driven architecture, and distributed tracing across all domains.

## Messages

### BaseEvent

Foundation for all domain events.

**Fields:**
- `event_id` (string) - Unique event identifier (1-128 chars, UUID v4)
- `event_type` (string) - Event type (e.g., "user.created", "tenant.updated")
- `aggregate_id` (string) - Entity ID that triggered event (1-128 chars)
- `aggregate_type` (string) - Entity type (e.g., "user", "tenant")
- `tenant_context` (TenantContext) - Tenant isolation context (REQUIRED)
- `occurred_at` (Timestamp) - Event occurrence time (UTC, REQUIRED)
- `triggered_by` (string) - User/service that triggered event (max 128 chars)
- `event_version` (int32) - Event schema version (≥1)
- `payload` (Any) - Domain-specific event payload
- `metadata` (map<string, string>) - Additional event metadata
- `correlation_id` (string) - Distributed tracing correlation ID (max 128 chars)
- `causation_id` (string) - Event ID that caused this event (max 128 chars)

**Usage:**
```protobuf
import "core/events/v1/events.proto";
import "google/protobuf/any.proto";

message UserCreatedPayload {
  string user_id = 1;
  string email = 2;
  string tenant_id = 3;
}

// Create event
geniustechspace.core.events.v1.BaseEvent event = {
  event_id: generate_uuid(),
  event_type: "user.created",
  aggregate_id: "usr_123",
  aggregate_type: "user",
  tenant_context: {...},
  occurred_at: now(),
  triggered_by: "usr_admin",
  event_version: 1,
  payload: Any.pack(UserCreatedPayload{...}),
  correlation_id: "corr_456"
};
```

### EventEnvelope

Event streaming wrapper for Kafka, Pulsar, etc.

**Fields:**
- `event` (BaseEvent) - The actual event (REQUIRED)
- `partition_key` (string) - Routing key for partitioning (1-128 chars)
- `sequence` (int64) - Sequence number for ordering (≥0)

**Usage:**
```protobuf
geniustechspace.core.events.v1.EventEnvelope envelope = {
  event: base_event,
  partition_key: tenant_id,  // Ensures same tenant → same partition
  sequence: 12345
};

// Publish to Kafka/Pulsar
publish(topic: "user.events", envelope);
```

### EventBatch

Batch processing support for ETL and analytics.

**Fields:**
- `events` (repeated BaseEvent) - Events in batch (1-1000 items, REQUIRED)
- `batch_id` (string) - Batch identifier (1-128 chars, REQUIRED)
- `batch_timestamp` (Timestamp) - Batch creation time (REQUIRED)

**Usage:**
```protobuf
geniustechspace.core.events.v1.EventBatch batch = {
  events: [event1, event2, event3, ...],
  batch_id: generate_uuid(),
  batch_timestamp: now()
};

// Process batch
process_batch(batch);
```

## Event Naming Convention

Event types follow the pattern: `<domain>.<action>`

Examples:
- `user.created` - User account created
- `user.updated` - User account updated
- `user.deleted` - User account deleted
- `tenant.created` - Tenant created
- `subscription.activated` - Subscription activated
- `payment.succeeded` - Payment succeeded
- `session.expired` - Session expired

**Rules:**
- Lowercase only
- Use dots (.) as separators
- Past tense for completed actions
- Present tense for ongoing states

## Event Sourcing Pattern

### Event Store

Events are immutable and append-only:

```
Event Store (Append-Only Log)
┌─────────────────────────────────────┐
│ Event 1: user.created (v1)          │
│ Event 2: user.updated (v2)          │
│ Event 3: user.email_verified (v3)   │
│ Event 4: user.role_changed (v4)     │
└─────────────────────────────────────┘
```

### Event Replay

Reconstruct entity state from events:

```go
func ReconstructUser(events []BaseEvent) User {
  user := User{}
  for _, event := range events {
    switch event.event_type {
    case "user.created":
      payload := UnpackUserCreated(event.payload)
      user.id = payload.user_id
      user.email = payload.email
    case "user.updated":
      payload := UnpackUserUpdated(event.payload)
      user.email = payload.email
    // ... handle other events
    }
  }
  return user
}
```

### Snapshots

Optimize replay with periodic snapshots:

```
Snapshot (v100) + Events (v101-v150)
┌─────────────────┐  ┌──────────────────┐
│ User State v100 │→ │ Events 101-150   │
└─────────────────┘  └──────────────────┘
```

## Distributed Tracing

### Correlation ID

Groups related events across services:

```
User Service          Payment Service       Notification Service
    │                      │                         │
    │ event_id: evt_1      │                         │
    │ correlation: corr_1  │                         │
    ├─────────────────────→│ event_id: evt_2         │
    │                      │ correlation: corr_1     │
    │                      │ causation: evt_1        │
    │                      ├────────────────────────→│ event_id: evt_3
    │                      │                         │ correlation: corr_1
    │                      │                         │ causation: evt_2
```

### Causation Chain

Tracks event causality:

```
evt_1 (user.created)
  └─→ evt_2 (subscription.created, causation: evt_1)
        └─→ evt_3 (payment.processed, causation: evt_2)
              └─→ evt_4 (email.sent, causation: evt_3)
```

## Event Versioning

Support schema evolution with event_version:

```protobuf
// Version 1
message UserCreatedV1 {
  string user_id = 1;
  string email = 2;
}

// Version 2 - added phone
message UserCreatedV2 {
  string user_id = 1;
  string email = 2;
  string phone = 3;  // New field
}

// Handle multiple versions
func ProcessUserCreated(event BaseEvent) {
  switch event.event_version {
  case 1:
    v1 := UnpackV1(event.payload)
    // Process v1
  case 2:
    v2 := UnpackV2(event.payload)
    // Process v2
  }
}
```

## Import Path

```protobuf
import "core/events/v1/events.proto";
import "core/common/v1/common.proto";  // For TenantContext
import "google/protobuf/any.proto";    // For payload
```

## Best Practices

### 1. Event Immutability

Never modify events after creation:
- Events are historical facts
- Corrections via compensating events
- Deletions via tombstone events

### 2. Idempotency

Events must be idempotent:
- Same event applied multiple times = same result
- Use event_id for deduplication
- Check if already processed before applying

### 3. Tenant Isolation

Always include tenant_context:
```protobuf
BaseEvent {
  tenant_context: {
    tenant_id: "tenant_abc"
  }
}
```

### 4. Payload Design

Keep payloads focused and minimal:
```protobuf
// Good - minimal data
message UserCreatedPayload {
  string user_id = 1;
  string email = 2;
}

// Bad - entire entity
message UserCreatedPayload {
  User user = 1;  // Too much data
}
```

### 5. Error Handling

Events should represent success:
```protobuf
// Good
event_type: "payment.succeeded"
event_type: "payment.failed"  // Failure is also an event

// Bad
event_type: "payment.error"  // Too generic
```

## Compliance

### SOC 2 CC7.2 (System Monitoring)

- Complete audit trail of all system events
- Immutable event log
- Timestamp tracking

### ISO 27001 A.12.4.1 (Event Logging)

- Security event logging
- Event integrity protection
- Event retention policies

### GDPR Considerations

- Events may contain PII - handle appropriately
- Support right to erasure via tombstone events
- Retain events per data retention policies

## See Also

- [Core Metadata](../metadata/README.md) - Entity audit trails
- [Core Common](../common/README.md) - TenantContext
- [Main Core README](../README.md) - Complete core module documentation
