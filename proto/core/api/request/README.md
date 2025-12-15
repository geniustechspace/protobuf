# Core Request API

Standardized request messages and internal context structures for all services.

## Package

```protobuf
package geniustechspace.core.api.request.v1;
```

**Go**: `github.com/geniustechspace/protobuf/gen/go/core/api/request/v1;requestv1`  
**Java**: `com.geniustechspace.protobuf.core.api.request.v1`  
**C#**: `GeniusTechSpace.Protobuf.Core.Api.Request.V1`

## Overview

This package provides TWO separate architectural patterns:

### 1. CRUD Request Messages (messages.proto)

Generic request wrappers for all CRUD operations sent by clients over gRPC.

**Pattern**: Generic messages with `google.protobuf.Any` OR domain-specific typed messages.

**Examples**:

- `Request` - Generic wrapper for custom operations
- `CreateRequest` - Create single entity
- `UpdateRequest` - Update with field mask
- `ListRequest` - Paginated list with filtering
- `DeleteRequest` - Soft/hard delete
- `BatchCreateRequest`, `BatchUpdateRequest`, etc.

### 2. Internal Request Context (context.proto)

Internal data structure built by middleware from gRPC metadata + Session lookup. **NOT sent in proto messages.**

**Pattern**: Server-side only structure with embedded Session for zero-trust validation.

**Key Message**: `RequestContext` with embedded `core.session.v1.Session`

---

## Part 1: CRUD Request Messages

### Architecture Pattern

```text
Client                  gRPC Wire             Server
  ↓                        ↓                    ↓
CreateUserRequest    →  Protobuf Bytes  →   Unmarshal
(domain-specific)                            Validate
                                             Process
```

### Generic vs Typed Requests

**Generic (Reusable with Any):**

```protobuf
message CreateRequest {
  google.protobuf.Any data = 1;  // Any domain entity
  string idempotency_key = 2;
  bool dry_run = 3;
  google.protobuf.FieldMask field_mask = 4;
}
```

**Domain-Specific (Type-Safe):**

```protobuf
// In proto/idp/identity/user/v1/messages.proto
message CreateUserRequest {
  User data = 1;  // ✅ Typed - no Any unpacking
  string idempotency_key = 2;
  bool dry_run = 3;
  google.protobuf.FieldMask field_mask = 4;
}
```

### Request Types

| Request Type           | Purpose                  | Key Fields                                 |
| ---------------------- | ------------------------ | ------------------------------------------ |
| **CreateRequest**      | Create single entity     | data, idempotency_key, dry_run, field_mask |
| **BatchCreateRequest** | Create multiple entities | data (repeated), continue_on_error         |
| **GetRequest**         | Retrieve by ID           | id, field_mask, include_deleted            |
| **ListRequest**        | Paginated list           | pagination, order_by, filter, field_mask   |
| **SearchRequest**      | Full-text search         | query, search_fields, pagination, filter   |
| **UpdateRequest**      | Update entity            | id, data, field_mask (required), version   |
| **BatchUpdateRequest** | Update multiple          | updates (repeated), continue_on_error      |
| **DeleteRequest**      | Delete entity            | id, hard_delete, version                   |
| **BatchDeleteRequest** | Delete multiple          | ids (repeated), hard_delete                |
| **RestoreRequest**     | Restore soft-deleted     | id, idempotency_key                        |
| **CountRequest**       | Count entities           | filter, include_deleted                    |
| **ExistsRequest**      | Check existence          | id, include_deleted                        |
| **ExportRequest**      | Export to format         | format, filter, field_mask                 |
| **ImportRequest**      | Import from format       | format, data (bytes), continue_on_error    |

### Usage Examples

#### Create Operation

**Service Definition:**

```protobuf
service UserService {
  rpc CreateUser(CreateUserRequest) returns (UserResponse);
}

message CreateUserRequest {
  User data = 1;
  string idempotency_key = 2;
  bool dry_run = 3;
  google.protobuf.FieldMask field_mask = 4;
}
```

**Client:**

```go
resp, err := client.CreateUser(ctx, &CreateUserRequest{
    Data: &User{
        Email: "john@example.com",
        Name:  "John Doe",
    },
    IdempotencyKey: "create-user-123",
    FieldMask: &fieldmaskpb.FieldMask{
        Paths: []string{"user_id", "email", "created_at"},
    },
})
```

#### List with Query System

**Service Definition:**

```protobuf
service UserService {
  rpc ListUsers(ListRequest) returns (ListUsersResponse);
}

// Use the standard ListRequest from request package
message ListRequest {
  // Comprehensive query from query package
  core.api.query.v1.Query query = 1;
}
```

**Client - Simple Filter:**

```go
import queryv1 "github.com/geniustechspace/protobuf/gen/go/core/api/query/v1"

resp, err := client.ListUsers(ctx, &requestv1.ListRequest{
    Query: &queryv1.Query{
        Filter: &queryv1.Filter{
            Field: "status",
            Op:    queryv1.FilterOperator_EQ,
            Value: "active",
        },
        Sorts: []*queryv1.Sorting{
            {Field: "created_at", Direction: queryv1.SortDirection_DESC},
        },
        Include: []string{"user_id", "email", "name", "status"},
        Pagination: &paginationv1.PaginationRequest{
            PageSize: 50,
        },
    },
})
```

**Client - Complex Nested Filter:**

```go
// (status = 'active') AND (role IN ['admin','user'] OR created_at > '2024-01-01')
resp, err := client.ListUsers(ctx, &requestv1.ListRequest{
    Query: &queryv1.Query{
        Filter: &queryv1.Filter{
            And: []*queryv1.Filter{
                // status = 'active'
                {
                    Field: "status",
                    Op:    queryv1.FilterOperator_EQ,
                    Value: "active",
                },
                // role IN ['admin','user'] OR created_at > '2024-01-01'
                {
                    Or: []*queryv1.Filter{
                        // role IN ['admin','user']
                        {
                            Field:  "role",
                            Op:     queryv1.FilterOperator_IN,
                            Values: []string{"admin", "user"},
                        },
                        // created_at > '2024-01-01'
                        {
                            Field: "created_at",
                            Op:    queryv1.FilterOperator_GT,
                            Value: "2024-01-01",
                        },
                    },
                },
            },
        },
        Sorts: []*queryv1.Sorting{
            {Field: "created_at", Direction: queryv1.SortDirection_DESC},
        },
        Include: []string{"user_id", "email", "name", "status"},
        Pagination: &paginationv1.PaginationRequest{
            PageSize: 50,
        },
    },
})
```

#### Update with Field Mask

**Service Definition:**

```protobuf
service UserService {
  rpc UpdateUser(UpdateUserRequest) returns (UserResponse);
}

message UpdateUserRequest {
  string id = 1;
  User data = 2;
  google.protobuf.FieldMask field_mask = 3;  // REQUIRED
  int64 version = 4;
  string idempotency_key = 5;
}
```

**Client:**

```go
resp, err := client.UpdateUser(ctx, &UpdateUserRequest{
    Id: "user_12345",
    Data: &User{
        Email:  "newemail@example.com",
        Status: UserStatus_ACTIVE,
    },
    FieldMask: &fieldmaskpb.FieldMask{
        Paths: []string{"email", "status"},  // Only update these
    },
    Version: 5,  // Optimistic locking
    IdempotencyKey: "update-user-456",
})
```

#### Batch Operations

**Create Multiple:**

```go
resp, err := client.BatchCreateUsers(ctx, &BatchCreateUsersRequest{
    Data: []*User{
        {Email: "user1@example.com", Name: "User 1"},
        {Email: "user2@example.com", Name: "User 2"},
        {Email: "user3@example.com", Name: "User 3"},
    },
    ContinueOnError: true,  // Don't rollback on first failure
    IdempotencyKey: "batch-create-789",
})
```

---

## Part 2: Internal Request Context

Internal data structure built by middleware - **NOT sent in proto messages.**

### Context Architecture Pattern

```text
Proto Definition (Type Schema)
        ↓
  NOT in Request Messages
        ↓
gRPC Metadata (Transport)
        ↓
Middleware Builder
  (metadata + Session lookup)
        ↓
RequestContext (In-Memory)
        ↓
Handler Consumption
```

### RequestContext Structure

```protobuf
message RequestContext {
  // Request tracking
  string request_id = 1;
  string correlation_id = 2;
  string idempotency_key = 3;

  // Request control (per-request, not session-stable)
  RequestProtocol protocol = 20;
  HTTPRequestMethod method = 21;
  int64 timeout_ms = 22;
  RequestPriority priority = 23;
  RequestValidationMode validation = 24;
  RequestIdempotencyMode idempotency_mode = 26;

  // Session (embedded - zero duplication)
  core.session.v1.Session session = 100;

  // Request lifecycle
  google.protobuf.Timestamp created_at = 101;
  google.protobuf.Timestamp expires_at = 102;

  // Request metadata
  map<string, string> metadata = 103;
}
```

### Middleware Implementation

```go
func (m *Middleware) buildRequestContext(ctx context.Context) (*requestv1.RequestContext, error) {
    // Extract from gRPC metadata
    md, _ := metadata.FromIncomingContext(ctx)
    sessionID := md.Get("x-session-id")[0]

    // Lookup Session (cached 99.9% of requests)
    session, err := m.sessionService.Get(ctx, &GetSessionRequest{
        SessionId: sessionID,
    })
    if err != nil {
        return nil, status.Error(codes.Unauthenticated, "invalid session")
    }

    // Build RequestContext
    return &requestv1.RequestContext{
        RequestId:     md.Get("x-request-id")[0],
        CorrelationId: md.Get("x-correlation-id")[0],
        IdempotencyKey: md.Get("x-idempotency-key")[0],
        Protocol:      detectProtocol(ctx),
        Method:        detectMethod(ctx),
        Timeout_Ms:    int64(grpc.Timeout(ctx).Milliseconds()),
        Session:       session,  // Embed full Session
        CreatedAt:     timestamppb.Now(),
        ExpiresAt:     timestamppb.New(time.Now().Add(5 * time.Minute)),
    }, nil
}
```

### Service Handler

```go
func (s *UserService) CreateUser(ctx context.Context, req *CreateUserRequest) (*UserResponse, error) {
    // Extract RequestContext (built by middleware)
    reqCtx := getRequestContext(ctx)

    // Zero-trust validation
    if reqCtx.Session.Status != sessionv1.SessionStatus_SESSION_STATUS_ACTIVE {
        return nil, status.Error(codes.Unauthenticated, "session not active")
    }

    // Check permissions (from embedded Session)
    if !hasPermission(reqCtx.Session.Permissions, "users:create") {
        return nil, status.Error(codes.PermissionDenied, "missing permission")
    }

    // Use request data + session context
    user := &User{
        TenantPath: reqCtx.Session.TenantPath,
        Email:      req.Data.Email,  // From request
        CreatedBy:  reqCtx.Session.UserId,  // From session
    }

    // Handle idempotency
    if req.IdempotencyKey != "" && reqCtx.IdempotencyKey != req.IdempotencyKey {
        return nil, status.Error(codes.InvalidArgument, "idempotency key mismatch")
    }

    // Dry run mode
    if req.DryRun {
        if err := s.validator.Validate(user); err != nil {
            return nil, err
        }
        return &UserResponse{Message: "Validation passed (dry run)"}, nil
    }

    // Persist entity
    created, err := s.repo.Create(ctx, user)
    if err != nil {
        return nil, err
    }

    return &UserResponse{Data: created}, nil
}
```

## Common Patterns

### GraphQL-Like Filtering

**Why Structured Filters?**

| Feature              | String Filters (Legacy)    | Structured Filters (GraphQL-like) |
| -------------------- | -------------------------- | --------------------------------- |
| **Type Safety**      | ❌ Parse errors at runtime | ✅ Compile-time validation        |
| **Nested Logic**     | ⚠️ Limited by syntax       | ✅ Unlimited nesting              |
| **Composability**    | ❌ String concatenation    | ✅ Object composition             |
| **Client Libraries** | ❌ Manual string building  | ✅ Type-safe builders             |
| **Validation**       | ⚠️ Server-side only        | ✅ Proto validation rules         |

**Filter Operators:**

```go
// Equality
FILTER_OPERATOR_EQ       // field == value
FILTER_OPERATOR_NE       // field != value

// Comparison
FILTER_OPERATOR_GT       // field > value
FILTER_OPERATOR_GTE      // field >= value
FILTER_OPERATOR_LT       // field < value
FILTER_OPERATOR_LTE      // field <= value

// Collections
FILTER_OPERATOR_IN       // field IN [val1, val2]
FILTER_OPERATOR_NOT_IN   // field NOT IN [val1, val2]

// Strings
FILTER_OPERATOR_CONTAINS      // field CONTAINS "substring"
FILTER_OPERATOR_STARTS_WITH   // field STARTS WITH "prefix"
FILTER_OPERATOR_ENDS_WITH     // field ENDS WITH "suffix"
FILTER_OPERATOR_MATCHES       // field MATCHES "regex"

// Null checks
FILTER_OPERATOR_IS_NULL       // field IS NULL
FILTER_OPERATOR_IS_NOT_NULL   // field IS NOT NULL

// Advanced
FILTER_OPERATOR_BETWEEN  // field BETWEEN [min, max]
FILTER_OPERATOR_EXISTS   // field EXISTS
```

**Logical Operators:**

```go
LOGICAL_OPERATOR_AND  // All filters must match
LOGICAL_OPERATOR_OR   // At least one filter must match
LOGICAL_OPERATOR_NOT  // Negate the filter (expects 1 child)
```

**Examples:**

```go
import queryv1 "github.com/geniustechspace/protobuf/gen/go/core/api/query/v1"

// 1. Simple equality filter
&queryv1.Filter{
    Field: "status",
    Op:    queryv1.FilterOperator_EQ,
    Value: "active",
}

// 2. Range filter (created_at BETWEEN '2024-01-01' AND '2024-12-31')
&queryv1.Filter{
    Field:  "created_at",
    Op:     queryv1.FilterOperator_BETWEEN,
    Values: []string{"2024-01-01T00:00:00Z", "2024-12-31T23:59:59Z"},
}

// 3. NOT filter (status != 'deleted')
&queryv1.Filter{
    Field: "status",
    Op:    queryv1.FilterOperator_NE,
    Value: "deleted",
}

// 4. Complex nested: (tier = 'premium' OR tier = 'enterprise') AND (status = 'active') AND (created_at > '2024-01-01')
&queryv1.Filter{
    And: []*queryv1.Filter{
        // (tier = 'premium' OR tier = 'enterprise')
        {
            Or: []*queryv1.Filter{
                {
                    Field: "tier",
                    Op:    queryv1.FilterOperator_EQ,
                    Value: "premium",
                },
                {
                    Field: "tier",
                    Op:    queryv1.FilterOperator_EQ,
                    Value: "enterprise",
                },
            },
        },
        // status = 'active'
        {
            Field: "status",
            Op:    queryv1.FilterOperator_EQ,
            Value: "active",
        },
        // created_at > '2024-01-01'
        {
            Field: "created_at",
            Op:    queryv1.FilterOperator_GT,
            Value: "2024-01-01",
        },
    },
}
```

**Server-Side Processing:**

```go
import queryv1 "github.com/geniustechspace/protobuf/gen/go/core/api/query/v1"

func applyFilter(query *gorm.DB, filter *queryv1.Filter) *gorm.DB {
    if filter == nil {
        return query
    }

    // Handle logical operators (AND/OR)
    if len(filter.And) > 0 {
        for _, f := range filter.And {
            query = applyFilter(query, f)
        }
        return query
    }

    if len(filter.Or) > 0 {
        orConditions := query.Session(&gorm.Session{})
        for i, f := range filter.Or {
            if i == 0 {
                orConditions = applyFilter(orConditions, f)
            } else {
                orConditions = orConditions.Or(applyFilter(query.Session(&gorm.Session{}), f))
            }
        }
        return query.Where(orConditions)
    }

    // Handle field operators
    switch filter.Op {
    case queryv1.FilterOperator_EQ:
        return query.Where(filter.Field + " = ?", filter.Value)
    case queryv1.FilterOperator_NE:
        return query.Where(filter.Field + " != ?", filter.Value)
    case queryv1.FilterOperator_GT:
        return query.Where(filter.Field + " > ?", filter.Value)
    case queryv1.FilterOperator_GTE:
        return query.Where(filter.Field + " >= ?", filter.Value)
    case queryv1.FilterOperator_LT:
        return query.Where(filter.Field + " < ?", filter.Value)
    case queryv1.FilterOperator_LTE:
        return query.Where(filter.Field + " <= ?", filter.Value)
    case queryv1.FilterOperator_IN:
        return query.Where(filter.Field + " IN ?", filter.Values)
    case queryv1.FilterOperator_NOT_IN:
        return query.Where(filter.Field + " NOT IN ?", filter.Values)
    case queryv1.FilterOperator_CONTAINS:
        return query.Where(filter.Field + " LIKE ?", "%"+filter.Value+"%")
    case queryv1.FilterOperator_STARTS_WITH:
        return query.Where(filter.Field + " LIKE ?", filter.Value+"%")
    case queryv1.FilterOperator_ENDS_WITH:
        return query.Where(filter.Field + " LIKE ?", "%"+filter.Value)
    case queryv1.FilterOperator_IS_NULL:
        return query.Where(filter.Field + " IS NULL")
    case queryv1.FilterOperator_IS_NOT_NULL:
        return query.Where(filter.Field + " IS NOT NULL")
    case queryv1.FilterOperator_BETWEEN:
        if len(filter.Values) == 2 {
            return query.Where(filter.Field + " BETWEEN ? AND ?", filter.Values[0], filter.Values[1])
        }
    }
    return query
}
```

### Field Mask Usage

**Update only specific fields:**

```go
// Client specifies exactly what to update
fieldMask: &fieldmaskpb.FieldMask{
    Paths: []string{"email", "status"},
}

// Server applies only specified fields
func applyFieldMask(dst, src *User, mask *fieldmaskpb.FieldMask) {
    for _, path := range mask.Paths {
        switch path {
        case "email":
            dst.Email = src.Email
        case "status":
            dst.Status = src.Status
        // ... other fields
        }
    }
}
```

### Idempotency

**Prevent duplicate operations:**

```go
// Client provides idempotency key
req := &CreateUserRequest{
    Data: user,
    IdempotencyKey: "create-user-" + uuid.New().String(),
}

// Server checks cache
if cached := idempotencyCache.Get(req.IdempotencyKey); cached != nil {
    return cached.(*UserResponse), nil  // Return cached result
}

// Process + cache result
resp, err := s.createUser(ctx, req)
if err == nil {
    idempotencyCache.Set(req.IdempotencyKey, resp, 24*time.Hour)
}
```

### Optimistic Locking

**Prevent lost updates:**

```go
// Client includes version from previous Get
req := &UpdateUserRequest{
    Id:      "user_123",
    Data:    updatedUser,
    Version: 5,  // From previous Get
}

// Server validates version
current, _ := s.repo.Get(ctx, req.Id)
if current.Version != req.Version {
    return nil, status.Error(codes.Aborted, "version mismatch - entity was modified")
}

// Update with version increment
updatedUser.Version = current.Version + 1
```

## Best Practices

### Request Messages

1. **Use domain-specific typed requests** in production (not generic with Any)
2. **Always include field_mask in updates** to prevent accidental overwrites
3. **Provide idempotency_key** for create/update/delete operations
4. **Use version field** for optimistic locking on updates
5. **Set continue_on_error** appropriately for batch operations
6. **Use dry_run** for validation without persistence

### Request Context

1. **Never send RequestContext in proto messages** - Build server-side only
2. **Use gRPC metadata for identifiers** - x-session-id, x-request-id
3. **Cache Session aggressively** - TTL = token expiry, 99.9% hit rate
4. **Validate session independently** - Zero-trust, don't trust upstream
5. **Access Session through embedding** - `reqCtx.Session.UserId`
6. **Extract idempotency_key from both** - metadata AND request body

## Related Documentation

- [Response Messages](../response/v1/messages.proto) - Matching response structures
- [Pagination](../pagination/v1/messages.proto) - Cursor-based pagination pattern
- [Error Handling](../error/v1/messages.proto) - Error context structure
- [Session](../../session/v1/messages.proto) - Embedded Session structure
- [Validation Rules](../../../docs/VALIDATION.md) - Protovalidate patterns
