# Enterprise Compliance Guide

## Overview

This document outlines the enterprise compliance standards and best practices implemented in this protobuf schema repository.

## Schema Organization Standards

### Single Responsibility Principle

Each proto file should contain messages and services related to a single domain concept:

✅ **Good Example**:
```
proto/users/v1/
├── users.proto          # User entity and CRUD operations
├── events.proto         # User-related domain events
└── README.md           # Domain documentation
```

❌ **Bad Example**:
```
proto/users/v1/
└── everything.proto    # Users, roles, permissions all mixed
```

### File Naming Conventions

- **Domain files**: `{domain}.proto` (e.g., `users.proto`, `tenants.proto`)
- **Event files**: `events.proto` (domain events)
- **Common/shared**: `common.proto` (shared types within domain)

### Message Organization

#### One Primary Entity Per File

Each domain proto file should focus on one primary entity:

```protobuf
// users.proto - Focuses on User entity
message User { ... }
message CreateUserRequest { ... }
message CreateUserResponse { ... }
message UpdateUserRequest { ... }
// ... other User-related messages
```

#### Separate Events

Domain events should be in a separate file:

```protobuf
// events.proto - User-related events
message UserCreatedEvent { ... }
message UserUpdatedEvent { ... }
message UserDeletedEvent { ... }
```

## Documentation Standards

### Required Documentation Elements

#### 1. Proto File Header

Every proto file must include:

```protobuf
syntax = "proto3";

package users.v1;

// Import statements
import "buf/validate/validate.proto";
import "core/v1/common.proto";

// Options
option go_package = "github.com/geniustechspace/protobuf/gen/go/users/v1;usersv1";
option java_multiple_files = true;
option java_package = "com.geniustechspace.protobuf.users.v1";
option csharp_namespace = "GeniusTechSpace.Protobuf.Users.V1";
```

#### 2. Message Comments

All messages should have descriptive comments:

```protobuf
// User represents a user in the system with full profile information.
// This is the primary entity for user management across all tenants.
message User {
  // Unique metadata including ID, timestamps, and audit trail
  core.v1.Metadata metadata = 1;
  
  // Tenant identifier for multi-tenancy isolation
  string tenant_id = 2 [(buf.validate.field).string.min_len = 1];
  
  // User's email address, must be unique within tenant
  string email = 3 [(buf.validate.field).string.email = true];
  
  // ... other fields with comments
}
```

#### 3. Service Documentation

Services must document their purpose and behavior:

```protobuf
// UserService provides comprehensive user management operations.
// All operations require tenant_id for proper multi-tenant isolation.
// 
// Authentication: All RPCs require valid authentication token
// Authorization: User must have appropriate role/permissions
service UserService {
  // CreateUser creates a new user within the specified tenant.
  // 
  // Errors:
  //   - INVALID_ARGUMENT: Invalid email format or missing required fields
  //   - ALREADY_EXISTS: Email already exists in this tenant
  //   - PERMISSION_DENIED: Insufficient permissions
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
  
  // ... other RPCs with documentation
}
```

#### 4. Domain README

Each domain must have a comprehensive README.md:

```markdown
# Domain Name

## Overview
Brief description of the domain and its purpose.

## Key Components
List of main messages and services.

## Usage Examples
Code examples in multiple languages.

## Best Practices
Guidelines for using this domain.

## Related Domains
Dependencies and relationships.
```

## Validation Standards

### Required Field Validation

All user-facing request fields must have appropriate validation:

```protobuf
message CreateUserRequest {
  // Required: Tenant identifier
  string tenant_id = 1 [(buf.validate.field).string.min_len = 1];
  
  // Required: Valid email address
  string email = 2 [(buf.validate.field).string.email = true];
  
  // Required: Username with length and pattern constraints
  string username = 3 [(buf.validate.field).string = {
    min_len: 3
    max_len: 50
    pattern: "^[a-zA-Z0-9_-]+$"
  }];
  
  // Required: Minimum password length for security
  string password = 4 [(buf.validate.field).string.min_len = 8];
}
```

### Validation Best Practices

1. **Always validate tenant_id**: Ensure it's not empty
2. **Email validation**: Use `email = true` constraint
3. **String lengths**: Set reasonable min/max lengths
4. **Patterns**: Use regex for format validation (usernames, slugs)
5. **Enums**: Use `defined_only = true` to prevent invalid values
6. **Numbers**: Set appropriate ranges with `gte`/`lte`
7. **URLs**: Use `uri = true` for URL validation

## Security Standards

### Authentication Context

All services must enforce authentication:

```protobuf
// All requests must include authentication token in metadata
// Token validation occurs at API gateway before reaching service
service UserService {
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
}
```

### Tenant Isolation

Every request message must include `tenant_id`:

```protobuf
message CreateUserRequest {
  // REQUIRED: Ensures data isolation between tenants
  string tenant_id = 1 [(buf.validate.field).string.min_len = 1];
  
  // ... other fields
}
```

### Sensitive Data

#### Password Handling

```protobuf
// Passwords should NEVER be returned in responses
message CreateUserRequest {
  // Password is input-only, never stored in plain text
  string password = 1 [(buf.validate.field).string.min_len = 8];
}

// Response should NOT include password
message CreateUserResponse {
  User user = 1;  // User message should not have password field
}
```

#### PII Protection

```protobuf
// Mark PII fields for proper handling
message User {
  // Email is PII, handle according to data protection regulations
  string email = 1 [(buf.validate.field).string.email = true];
  
  // Phone is PII
  string phone = 2;
  
  // SSN/Tax ID should be encrypted at rest
  string tax_id = 3;  // Consider using encrypted field type
}
```

## Versioning Standards

### Version Strategy

- **v1**: Initial stable version
- **v2**: Major changes with backward incompatibility
- **v1.1**: Not used in package names, only in documentation

### Backward Compatibility

#### Allowed Changes (Backward Compatible)

✅ Add new fields (with new field numbers)
✅ Add new messages
✅ Add new services
✅ Add new enum values
✅ Add new RPCs to existing services

#### Breaking Changes (Require New Version)

❌ Remove fields
❌ Rename fields
❌ Change field types
❌ Change field numbers
❌ Remove messages
❌ Remove services
❌ Remove enum values

### Deprecation

Mark deprecated fields instead of removing:

```protobuf
message User {
  string id = 1;
  
  // Deprecated: Use first_name and last_name instead
  string name = 2 [deprecated = true];
  
  string first_name = 3;
  string last_name = 4;
}
```

## Code Generation Standards

### Multi-Language Support

All schemas must support generation for:

- **Go**: With protovalidate-go
- **Python**: With protovalidate-python
- **Java**: With validation annotations
- **TypeScript**: For web/mobile clients
- **C#**: For .NET applications

### Generated Code Quality

```yaml
# buf.gen.yaml
plugins:
  # Use latest stable versions
  - remote: buf.build/protocolbuffers/go:latest
  - remote: buf.build/bufbuild/protovalidate-go:latest
```

## Testing Standards

### Validation Testing

All validation rules must be tested:

```go
func TestCreateUserValidation(t *testing.T) {
    tests := []struct {
        name    string
        req     *usersv1.CreateUserRequest
        wantErr bool
    }{
        {
            name: "valid request",
            req: &usersv1.CreateUserRequest{
                TenantId: "tenant_123",
                Email:    "user@example.com",
                Username: "johndoe",
                Password: "securepass123",
            },
            wantErr: false,
        },
        // ... more test cases
    }
    
    v, _ := protovalidate.New()
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := v.Validate(tt.req)
            if (err != nil) != tt.wantErr {
                t.Errorf("Validate() error = %v, wantErr %v", err, tt.wantErr)
            }
        })
    }
}
```

### Service Testing

All service methods should have integration tests.

## CI/CD Standards

### Automated Checks

Every PR must pass:

1. **Buf Lint**: Style and naming conventions
2. **Buf Format**: Consistent formatting
3. **Breaking Changes**: No unintended breaking changes
4. **Code Generation**: Successful generation for all languages
5. **Validation Tests**: All validation rules tested

### GitHub Actions Integration

```yaml
name: Buf CI/CD

jobs:
  buf:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: bufbuild/buf-action@v1
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          format: true
          lint: true
          breaking: true
          pr_comment: true
```

## Audit and Compliance

### Audit Trail

All entities should support audit trails:

```protobuf
message Metadata {
  string id = 1;
  google.protobuf.Timestamp created_at = 2;
  google.protobuf.Timestamp updated_at = 3;
  string created_by = 4;  // User ID who created
  string updated_by = 5;  // User ID who last updated
  int64 version = 6;      // For optimistic locking
}
```

### Data Retention

```protobuf
message Metadata {
  bool deleted = 7;  // Soft delete flag
  google.protobuf.Timestamp deleted_at = 8;  // Deletion timestamp
}
```

### GDPR Compliance

1. **Right to Access**: All user data retrievable via APIs
2. **Right to Deletion**: Soft delete with permanent deletion capability
3. **Data Portability**: Export APIs for user data
4. **Consent Management**: Track consent in user preferences

```protobuf
message UserPreferences {
  bool marketing_consent = 1;
  bool analytics_consent = 2;
  google.protobuf.Timestamp consent_updated_at = 3;
}
```

## Performance Standards

### Message Size Limits

- Keep messages under 1MB for optimal performance
- Use pagination for large lists
- Stream large data transfers

### Pagination

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

### Efficient Queries

Use field masks for partial updates:

```protobuf
import "google/protobuf/field_mask.proto";

message UpdateUserRequest {
  string tenant_id = 1;
  string user_id = 2;
  User user = 3;
  google.protobuf.FieldMask update_mask = 4;
}
```

## Monitoring and Observability

### Structured Logging

Include context in all operations:

```go
log.Info("User created",
    "tenant_id", req.TenantId,
    "user_id", user.Metadata.Id,
    "email", req.Email,
)
```

### Metrics

Track key metrics:
- Request rates per service/RPC
- Error rates per error type
- Latency percentiles (p50, p95, p99)
- Validation failure rates

### Distributed Tracing

Use correlation IDs:

```protobuf
message BaseEvent {
  string correlation_id = 11;  // Trace requests across services
  string causation_id = 12;     // Track event causality
}
```

## Disaster Recovery

### Backup Strategy

- **Proto Files**: Version controlled in Git
- **Generated Code**: Reproducible from proto files
- **Documentation**: Auto-generated and versioned

### Schema Migration

1. Deploy new version alongside old version
2. Migrate clients gradually
3. Monitor for issues
4. Deprecate old version after migration period
5. Remove old version after deprecation period

## Review Checklist

Before merging changes, verify:

- [ ] All proto files follow single responsibility principle
- [ ] Documentation is complete (comments, README)
- [ ] Validation rules are appropriate and tested
- [ ] Tenant isolation is enforced
- [ ] Sensitive data is handled properly
- [ ] No breaking changes (or new version created)
- [ ] Code generates successfully for all languages
- [ ] Buf lint passes
- [ ] Buf format applied
- [ ] CI/CD pipeline passes
- [ ] Tests cover validation rules
- [ ] Security review completed

## Compliance Certifications

This repository follows standards from:

- **ISO 27001**: Information security management
- **SOC 2**: Security, availability, confidentiality
- **GDPR**: Data protection and privacy
- **HIPAA**: Healthcare data protection (when applicable)

## Support and Questions

For compliance questions:
- Email: compliance@geniustechspace.com
- Documentation: https://docs.geniustechspace.com/compliance
- Slack: #compliance-help
