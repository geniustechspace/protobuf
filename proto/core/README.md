# Core Domain

## Overview

The Core domain provides foundational types and utilities that are shared across all other domains in the system. It establishes the baseline for multi-tenancy, metadata management, pagination, and event-driven architecture.

## Key Components

### Common Types (v1/common.proto)

#### TenantContext
Provides multi-tenant isolation for all requests:
```protobuf
message TenantContext {
  string tenant_id = 1;
  string tenant_name = 2;
  string tier = 3;
  string status = 4;
}
```

**Usage**: Include in every request to ensure tenant isolation and proper data scoping.

#### Metadata
Common metadata for all entities:
```protobuf
message Metadata {
  string id = 1;
  google.protobuf.Timestamp created_at = 2;
  google.protobuf.Timestamp updated_at = 3;
  string created_by = 4;
  string updated_by = 5;
  int64 version = 6;
  bool deleted = 7;
  google.protobuf.Timestamp deleted_at = 8;
}
```

**Features**:
- Unique ID generation
- Automatic timestamps
- Audit trail (created_by, updated_by)
- Optimistic locking (version)
- Soft deletes (deleted, deleted_at)

#### Pagination
Request and response types for paginated lists:

```protobuf
message PaginationRequest {
  int32 page = 1;
  int32 page_size = 2;
  string sort_by = 3;
  string sort_order = 4;
}

message PaginationResponse {
  int32 page = 1;
  int32 page_size = 2;
  int64 total_items = 3;
  int32 total_pages = 4;
  bool has_next = 5;
  bool has_previous = 6;
}
```

#### Value Objects
- **Address**: Physical/mailing addresses
- **ContactInfo**: Email, phone, mobile, fax
- **Money**: Currency and amount representation
- **ErrorResponse**: Standardized error responses

### Events (v1/events.proto)

#### BaseEvent
Foundation for all domain events:
```protobuf
message BaseEvent {
  string event_id = 1;
  string event_type = 2;
  string aggregate_id = 3;
  string aggregate_type = 4;
  TenantContext tenant_context = 5;
  google.protobuf.Timestamp occurred_at = 6;
  string triggered_by = 7;
  int32 event_version = 8;
  google.protobuf.Any payload = 9;
  map<string, string> metadata = 10;
  string correlation_id = 11;
  string causation_id = 12;
}
```

**Features**:
- Event sourcing support
- Distributed tracing (correlation_id, causation_id)
- Schema evolution (event_version)
- Tenant isolation
- Flexible payload with Any type

## Version 2 (v2)

### Enhanced Features

#### TenantContext v2
Added hierarchical tenancy and regional support:
```protobuf
message TenantContext {
  // v1 fields...
  string parent_tenant_id = 5;
  string region = 6;
  repeated string features = 7;
}
```

#### Metadata v2
Added tags and audit trail:
```protobuf
message Metadata {
  // v1 fields...
  repeated string tags = 9;
  repeated AuditEntry audit_trail = 10;
}
```

#### Pagination v2
Added cursor-based pagination:
```protobuf
message PaginationRequest {
  // v1 fields...
  string cursor = 5;
}

message PaginationResponse {
  // v1 fields...
  string next_cursor = 7;
  string previous_cursor = 8;
}
```

## Migration Guide

### From v1 to v2

All v2 additions are backward compatible. Existing v1 clients will continue to work without changes.

**New features to adopt**:
1. Use cursor-based pagination for better performance on large datasets
2. Add tags to entities for better categorization
3. Use hierarchical tenancy for enterprise customers with subsidiaries
4. Specify region for data residency compliance

## Best Practices

1. **Always include TenantContext**: Every request must include tenant_id for proper isolation
2. **Use Metadata consistently**: All domain entities should include Metadata
3. **Implement soft deletes**: Use the deleted flag instead of hard deletes
4. **Version your events**: Include event_version in BaseEvent payload
5. **Paginate large lists**: Always use pagination for list operations
6. **Include audit information**: Track who created/updated entities

## Examples

### Creating an Entity with Metadata

```go
user := &usersv1.User{
    Metadata: &corev1.Metadata{
        Id:        uuid.New().String(),
        CreatedAt: timestamppb.Now(),
        UpdatedAt: timestamppb.Now(),
        CreatedBy: currentUserId,
        UpdatedBy: currentUserId,
        Version:   1,
        Deleted:   false,
    },
    TenantId: tenantId,
    Email:    "user@example.com",
    // ... other fields
}
```

### Publishing a Domain Event

```go
event := &corev1.BaseEvent{
    EventId:       uuid.New().String(),
    EventType:     "user.created",
    AggregateId:   user.Metadata.Id,
    AggregateType: "user",
    TenantContext: &corev1.TenantContext{
        TenantId: tenantId,
    },
    OccurredAt:    timestamppb.Now(),
    TriggeredBy:   currentUserId,
    EventVersion:  1,
    CorrelationId: requestId,
}
```

### Using Pagination

```go
request := &usersv1.ListUsersRequest{
    TenantId: tenantId,
    Pagination: &corev1.PaginationRequest{
        Page:      0,
        PageSize:  20,
        SortBy:    "created_at",
        SortOrder: "desc",
    },
}
```

## Dependencies

- `google/protobuf/timestamp.proto`
- `google/protobuf/any.proto`

## Related Domains

All domains depend on Core for:
- TenantContext
- Metadata
- Pagination
- BaseEvent
