# Protovalidate Integration Guide

## Overview

This repository uses [protovalidate](https://github.com/bufbuild/protovalidate) to provide runtime validation of protobuf messages. Protovalidate enables you to define validation rules directly in your `.proto` files using field options, ensuring data quality and correctness at runtime.

## Benefits

✅ **Type Safety**: Validation rules are defined alongside your schema  
✅ **Runtime Validation**: Automatic validation in generated code  
✅ **Multi-Language**: Consistent validation across Go, Python, Java, and more  
✅ **Declarative**: Simple annotation-based validation rules  
✅ **Composable**: Build complex validation logic from simple rules

## Installation

Protovalidate is already configured in this repository:

```yaml
# buf.yaml
deps:
  - buf.build/bufbuild/protovalidate

# buf.gen.yaml
plugins:
  - remote: buf.build/bufbuild/protovalidate-go:latest
  - remote: buf.build/bufbuild/protovalidate-python:latest
```

## Usage Examples

### String Validation

#### Email Validation

```protobuf
import "buf/validate/validate.proto";

message CreateUserRequest {
  string email = 1 [(buf.validate.field).string.email = true];
}
```

#### Length Constraints

```protobuf
message User {
  string username = 1 [(buf.validate.field).string = {
    min_len: 3
    max_len: 50
  }];

  string first_name = 2 [(buf.validate.field).string = {
    min_len: 1
    max_len: 100
  }];
}
```

#### Pattern Matching

```protobuf
message CreateTenantRequest {
  // Only lowercase alphanumeric and hyphens
  string slug = 1 [(buf.validate.field).string = {
    min_len: 3
    max_len: 50
    pattern: "^[a-z0-9-]+$"
  }];

  // Username: alphanumeric, underscore, hyphen
  string username = 2 [(buf.validate.field).string = {
    min_len: 3
    max_len: 50
    pattern: "^[a-zA-Z0-9_-]+$"
  }];
}
```

#### URI Validation

```protobuf
message User {
  string avatar_url = 1 [(buf.validate.field).string.uri = true];
  string website = 2 [(buf.validate.field).string.uri = true];
}
```

### Numeric Validation

#### Range Constraints

```protobuf
message TenantSettings {
  int32 max_users = 1 [(buf.validate.field).int32 = {
    gte: 1
    lte: 10000
  }];

  int32 max_storage_gb = 2 [(buf.validate.field).int32 = {
    gte: 1
    lte: 10000
  }];
}
```

#### Positive Numbers

```protobuf
message Money {
  int64 amount = 1 [(buf.validate.field).int64.gte = 0];
}
```

### Enum Validation

```protobuf
enum UserStatus {
  USER_STATUS_UNSPECIFIED = 0;
  USER_STATUS_ACTIVE = 1;
  USER_STATUS_INACTIVE = 2;
}

message User {
  // Ensure only defined enum values are used
  UserStatus status = 1 [(buf.validate.field).enum.defined_only = true];
}
```

### Repeated Field Validation

```protobuf
message ListUsersRequest {
  // At least one user ID required
  repeated string user_ids = 1 [(buf.validate.field).repeated = {
    min_items: 1
    max_items: 100
  }];
}
```

### Map Validation

```protobuf
message UserPreferences {
  map<string, string> custom_preferences = 1 [(buf.validate.field).map = {
    min_pairs: 0
    max_pairs: 50
    keys: {
      string: {
        min_len: 1
        max_len: 100
      }
    }
    values: {
      string: {
        max_len: 1000
      }
    }
  }];
}
```

### Required Fields

```protobuf
message CreateUserRequest {
  // tenant_id is required (cannot be empty)
  string tenant_id = 1 [(buf.validate.field).string.min_len = 1];

  // email is required and must be valid
  string email = 2 [(buf.validate.field).string.email = true];

  // password is required with minimum length
  string password = 3 [(buf.validate.field).string.min_len = 8];
}
```

### Timestamp Validation

```protobuf
import "google/protobuf/timestamp.proto";

message Subscription {
  google.protobuf.Timestamp start_date = 1 [(buf.validate.field).timestamp = {
    required: true
  }];

  // End date must be after start date
  google.protobuf.Timestamp end_date = 2 [(buf.validate.field).timestamp = {
    required: true
    gt_now: false
  }];
}
```

### Message-Level Validation

```protobuf
message DateRange {
  option (buf.validate.message).cel = {
    id: "date_range.valid"
    message: "end_date must be after start_date"
    expression: "this.end_date > this.start_date"
  };

  google.protobuf.Timestamp start_date = 1;
  google.protobuf.Timestamp end_date = 2;
}
```

## Validation in Code

### Go Example

```go
import (
    "github.com/bufbuild/protovalidate-go"
    usersv1 "github.com/geniustechspace/protobuf/gen/go/users/v1"
)

func CreateUser(ctx context.Context, req *usersv1.CreateUserRequest) error {
    // Create validator
    v, err := protovalidate.New()
    if err != nil {
        return fmt.Errorf("failed to create validator: %w", err)
    }

    // Validate the request
    if err := v.Validate(req); err != nil {
        return fmt.Errorf("validation failed: %w", err)
    }

    // Request is valid, proceed with creation
    // ...
}
```

### Python Example

```python
from buf.validate import validate_pb2
from protovalidate import validate
from gen.python.users.v1 import users_pb2

def create_user(request: users_pb2.CreateUserRequest):
    # Validate the request
    try:
        validate(request)
    except Exception as e:
        raise ValueError(f"Validation failed: {e}")

    # Request is valid, proceed with creation
    # ...
```

### Java Example

```java
import build.buf.protovalidate.Validator;
import build.buf.protovalidate.ValidationException;
import com.geniustechspace.protobuf.users.v1.UsersProto.CreateUserRequest;

public void createUser(CreateUserRequest request) throws ValidationException {
    // Create validator
    Validator validator = new Validator();

    // Validate the request
    validator.validate(request);

    // Request is valid, proceed with creation
    // ...
}
```

## Best Practices

### 1. Always Validate User Input

```protobuf
// Good: Validation on all user-facing fields
message CreateUserRequest {
  string tenant_id = 1 [(buf.validate.field).string.min_len = 1];
  string email = 2 [(buf.validate.field).string.email = true];
  string password = 3 [(buf.validate.field).string.min_len = 8];
}

// Bad: No validation
message CreateUserRequest {
  string tenant_id = 1;
  string email = 2;
  string password = 3;
}
```

### 2. Use Appropriate Constraints

```protobuf
// Good: Realistic constraints
message User {
  string username = 1 [(buf.validate.field).string = {
    min_len: 3
    max_len: 50
    pattern: "^[a-zA-Z0-9_-]+$"
  }];
}

// Too loose
message User {
  string username = 1; // No constraints
}

// Too strict
message User {
  string username = 1 [(buf.validate.field).string = {
    min_len: 20  // Too long minimum
    max_len: 20  // Too restrictive
  }];
}
```

### 3. Validate Enums

```protobuf
// Good: Only allow defined values
message User {
  UserStatus status = 1 [(buf.validate.field).enum.defined_only = true];
}

// Bad: Allow any integer value
message User {
  UserStatus status = 1;
}
```

### 4. Document Validation Rules

```protobuf
message CreateUserRequest {
  // Username must be 3-50 characters, alphanumeric with underscore/hyphen
  string username = 1 [(buf.validate.field).string = {
    min_len: 3
    max_len: 50
    pattern: "^[a-zA-Z0-9_-]+$"
  }];

  // Password must be at least 8 characters
  string password = 2 [(buf.validate.field).string.min_len = 8];
}
```

### 5. Test Validation Rules

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
        {
            name: "invalid email",
            req: &usersv1.CreateUserRequest{
                TenantId: "tenant_123",
                Email:    "invalid-email",
                Username: "johndoe",
                Password: "securepass123",
            },
            wantErr: true,
        },
        {
            name: "short password",
            req: &usersv1.CreateUserRequest{
                TenantId: "tenant_123",
                Email:    "user@example.com",
                Username: "johndoe",
                Password: "short",
            },
            wantErr: true,
        },
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

## Common Validation Patterns

### Email Validation

```protobuf
string email = 1 [(buf.validate.field).string.email = true];
```

### UUID Validation

```protobuf
string user_id = 1 [(buf.validate.field).string.uuid = true];
```

### Phone Number (Basic)

```protobuf
string phone = 1 [(buf.validate.field).string.pattern = "^\\+?[1-9]\\d{1,14}$"];
```

### URL Validation

```protobuf
string website = 1 [(buf.validate.field).string.uri = true];
```

### Slug Validation

```protobuf
string slug = 1 [(buf.validate.field).string.pattern = "^[a-z0-9-]+$"];
```

### Money Amount (Cents)

```protobuf
int64 amount_cents = 1 [(buf.validate.field).int64.gte = 0];
```

### Percentage

```protobuf
int32 discount_percent = 1 [(buf.validate.field).int32 = {
  gte: 0
  lte: 100
}];
```

## Error Handling

### Error Messages

Validation errors contain detailed information:

```
validation error:
 - email: value must be a valid email address [string.email]
 - username: value length must be at least 3 characters [string.min_len]
 - password: value length must be at least 8 characters [string.min_len]
```

### Structured Error Handling

```go
if err := v.Validate(req); err != nil {
    // Parse validation error
    if validationErr, ok := err.(*protovalidate.ValidationError); ok {
        for _, violation := range validationErr.Violations {
            log.Printf("Field: %s, Constraint: %s, Message: %s",
                violation.FieldPath,
                violation.ConstraintId,
                violation.Message)
        }
    }
    return err
}
```

## Performance Considerations

1. **Reuse Validator Instance**: Create the validator once and reuse it
2. **Validate Early**: Validate at API boundaries before processing
3. **Cache Compiled Rules**: Protovalidate caches compiled validation rules
4. **Async Validation**: For heavy workloads, consider async validation

## Migration Guide

### Adding Validation to Existing Schemas

1. Add protovalidate import:

```protobuf
import "buf/validate/validate.proto";
```

2. Add validation rules incrementally:

```protobuf
// Start with critical fields
message CreateUserRequest {
  string tenant_id = 1 [(buf.validate.field).string.min_len = 1];
  string email = 2 [(buf.validate.field).string.email = true];

  // Add more rules gradually
  string username = 3;  // Add validation later
}
```

3. Test thoroughly before deploying

4. Monitor validation failures in production

## Resources

- [Protovalidate Documentation](https://github.com/bufbuild/protovalidate)
- [Protovalidate Go](https://github.com/bufbuild/protovalidate-go)
- [Protovalidate Python](https://github.com/bufbuild/protovalidate-python)
- [Buf Schema Registry](https://buf.build/bufbuild/protovalidate)

## Support

For issues with validation:

1. Check the [protovalidate documentation](https://github.com/bufbuild/protovalidate)
2. Review [validation examples](https://github.com/bufbuild/protovalidate/tree/main/examples)
3. Open an issue in this repository
