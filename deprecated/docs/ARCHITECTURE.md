# Architecture Overview

## Design Principles

This protobuf schema repository follows enterprise-grade design principles:

### 1. Domain-Driven Design (DDD)

The schema is organized around business domains, not technical concerns:

- **Core**: Foundational types and cross-cutting concerns
- **Auth**: Identity and access management
- **Users**: User lifecycle and profile management
- **Access-Policy**: Authorization and permissions
- **Tenants**: Multi-tenant organization management
- **Billing**: Subscription and payment processing
- **Notifications**: Communication and alerting

Each domain is independent and can be developed, deployed, and scaled separately.

### 2. Multi-Tenancy

Every domain is tenant-aware:

```protobuf
message TenantContext {
  string tenant_id = 1;
  string tenant_name = 2;
  string tier = 3;
  string status = 4;
}
```

All requests include tenant context for:
- Data isolation
- Access control
- Billing and metering
- Custom configurations

### 3. Event-Driven Architecture

Each domain defines events for important state changes:

```protobuf
message BaseEvent {
  string event_id = 1;
  string event_type = 2;
  string aggregate_id = 3;
  TenantContext tenant_context = 5;
  google.protobuf.Timestamp occurred_at = 6;
  google.protobuf.Any payload = 9;
}
```

Events enable:
- Loose coupling between services
- Audit trails
- Event sourcing
- CQRS patterns
- Real-time notifications

### 4. Versioning Strategy

Support for multiple API versions:

```
proto/
├── users/
│   ├── v1/
│   │   ├── users.proto
│   │   └── events.proto
│   └── v2/
│       ├── users.proto
│       └── events.proto
```

Version evolution rules:
- v1 remains stable and unchanged
- v2 adds new features with backward compatibility
- Clients can migrate at their own pace
- Breaking changes require new major version

### 5. Separation of Concerns

Each proto file has a specific purpose:

- **{domain}.proto**: Core domain models and services
- **events.proto**: Domain events
- **common.proto**: Shared types within a domain

## Architectural Patterns

### Microservices Communication

```
┌─────────────┐         ┌─────────────┐
│   Client    │─gRPC───▶│ Auth Service│
└─────────────┘         └─────────────┘
                              │
                          validates
                              │
                              ▼
┌─────────────┐         ┌─────────────┐
│User Service │◀─gRPC──│ API Gateway │
└─────────────┘         └─────────────┘
      │                       │
   publishes              subscribes
      │                       │
      ▼                       ▼
┌──────────────────────────────────────┐
│         Event Bus (Kafka/NATS)       │
└──────────────────────────────────────┘
      │                       │
      ▼                       ▼
┌─────────────┐         ┌─────────────┐
│Notification │         │  Billing    │
│  Service    │         │  Service    │
└─────────────┘         └─────────────┘
```

### Request Flow with Tenant Context

```
1. Client → API Gateway (with tenant_id in metadata/header)
2. API Gateway → Auth Service (validate token, get tenant context)
3. API Gateway → Domain Service (with TenantContext)
4. Domain Service → Database (scoped by tenant_id)
5. Domain Service → Event Bus (publish domain event)
6. Event Bus → Subscribers (async processing)
```

### Data Isolation Strategy

**Database per Tenant** (highest isolation):
```
tenant_a_db
tenant_b_db
tenant_c_db
```

**Schema per Tenant** (balanced):
```
shared_db
  ├── tenant_a_schema
  ├── tenant_b_schema
  └── tenant_c_schema
```

**Row-level Tenancy** (most cost-effective):
```
shared_db
  └── users_table
      ├── (tenant_id='a', user_id='1', ...)
      ├── (tenant_id='a', user_id='2', ...)
      ├── (tenant_id='b', user_id='1', ...)
      └── (tenant_id='c', user_id='1', ...)
```

All queries include `WHERE tenant_id = ?` filter.

## Security Considerations

### Authentication Flow

```protobuf
// 1. Client authenticates
rpc Authenticate(AuthenticateRequest) returns (AuthenticateResponse);

message AuthenticateRequest {
  Credentials credentials = 1;  // email, password, tenant_id
}

message AuthenticateResponse {
  TokenResponse token = 1;      // JWT tokens
  Session session = 2;          // session info
}

// 2. Subsequent requests include token
metadata: {
  "authorization": "Bearer <access_token>",
  "x-tenant-id": "<tenant_id>"
}
```

### Authorization Flow

```protobuf
// Check if user has permission
rpc CheckPermission(CheckPermissionRequest) returns (CheckPermissionResponse);

message CheckPermissionRequest {
  string tenant_id = 1;
  string user_id = 2;
  string resource = 3;  // e.g., "users"
  string action = 4;    // e.g., "create"
}
```

### Tenant Isolation

All services must:
1. Validate tenant_id from request metadata
2. Ensure user belongs to the tenant
3. Scope all database queries by tenant_id
4. Include tenant_id in all events

## Scalability Patterns

### Horizontal Scaling

Each domain service can scale independently:

```
Load Balancer
      │
      ├──▶ User Service (Pod 1)
      ├──▶ User Service (Pod 2)
      └──▶ User Service (Pod 3)
```

### Data Partitioning

Event streams partitioned by tenant_id:

```
Kafka Topic: user.events
  Partition 0: tenant_a events
  Partition 1: tenant_b events
  Partition 2: tenant_c events
```

### Caching Strategy

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Redis Cache │ (tenant-scoped keys)
└──────┬──────┘
       │ (cache miss)
       ▼
┌─────────────┐
│  Database   │
└─────────────┘
```

Cache keys include tenant_id: `tenant:{tenant_id}:user:{user_id}`

## Observability

### Distributed Tracing

Events include correlation IDs:

```protobuf
message BaseEvent {
  string correlation_id = 11;  // trace across services
  string causation_id = 12;    // parent event
}
```

### Metrics

Track per-tenant metrics:
- Request rates
- Error rates
- Response times
- Resource usage

### Logging

Structured logs with tenant context:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "service": "user-service",
  "tenant_id": "tenant_123",
  "user_id": "user_456",
  "action": "create_user",
  "request_id": "req_789"
}
```

## Deployment Architecture

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: user-service
        image: user-service:latest
        env:
        - name: GRPC_PORT
          value: "9090"
        - name: TENANT_ISOLATION_LEVEL
          value: "database"
```

### Service Mesh

Using Istio/Linkerd for:
- Mutual TLS between services
- Traffic management
- Circuit breaking
- Request retries

## Client Generation

### Per-Domain Clients

Generate independent client libraries:

```bash
# Generate only user domain client
buf generate --path proto/users/v1/

# Package for distribution
npm pack gen/typescript/users/v1/
mvn deploy gen/java/users/v1/
python setup.py sdist gen/python/users/v1/
```

### Version Compatibility

Clients specify the version they support:

```go
import usersv1 "github.com/geniustechspace/protobuf/gen/go/users/v1"
import usersv2 "github.com/geniustechspace/protobuf/gen/go/users/v2"
```

## Best Practices

### 1. Always Include Tenant Context

```protobuf
message CreateUserRequest {
  string tenant_id = 1;  // Always first field
  // ... other fields
}
```

### 2. Use Metadata for Common Fields

```protobuf
message User {
  core.v1.Metadata metadata = 1;  // ID, timestamps, etc.
  string tenant_id = 2;
  // ... domain-specific fields
}
```

### 3. Publish Events for State Changes

```protobuf
service UserService {
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
  // After success, publish UserCreatedEvent
}
```

### 4. Use Pagination for Lists

```protobuf
message ListUsersRequest {
  string tenant_id = 1;
  core.v1.PaginationRequest pagination = 2;
}

message ListUsersResponse {
  repeated User users = 1;
  core.v1.PaginationResponse pagination = 2;
}
```

### 5. Implement Soft Deletes

```protobuf
message Metadata {
  bool deleted = 7;
  google.protobuf.Timestamp deleted_at = 8;
}
```

## Migration Strategies

### From v1 to v2

1. Deploy v2 services alongside v1
2. Update API gateway to support both versions
3. Migrate clients gradually
4. Monitor metrics for both versions
5. Deprecate v1 after migration period
6. Remove v1 services

### Adding New Domains

1. Create proto files in `proto/new-domain/v1/`
2. Define messages, services, and events
3. Run `buf lint` and `buf breaking`
4. Generate code with `buf generate`
5. Implement service
6. Update API gateway routing
7. Document in README and domain docs

## Conclusion

This architecture provides:
- ✅ Strong tenant isolation
- ✅ Independent domain scaling
- ✅ Event-driven communication
- ✅ Backward-compatible evolution
- ✅ Multi-language support
- ✅ Enterprise-grade security
- ✅ Comprehensive observability
