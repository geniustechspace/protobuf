# Contributing to Protobuf Schema Repository

Thank you for your interest in contributing! This document provides guidelines for contributing to the protobuf schema repository.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Schema Design Guidelines](#schema-design-guidelines)
- [Versioning Guidelines](#versioning-guidelines)
- [Testing Changes](#testing-changes)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

- Be respectful and inclusive
- Collaborate openly
- Accept constructive criticism
- Focus on what's best for the community

## Getting Started

### Prerequisites

- [Buf CLI](https://buf.build/docs/installation) >= 1.47.0
- Git
- Basic understanding of Protocol Buffers
- Familiarity with gRPC

### Setup

```bash
# Clone the repository
git clone https://github.com/geniustechspace/protobuf.git
cd protobuf

# Install Buf
brew install bufbuild/buf/buf  # macOS
# or follow installation guide for other platforms

# Verify installation
buf --version
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/add-new-domain
```

### 2. Make Your Changes

Follow the [Schema Design Guidelines](#schema-design-guidelines) when making changes.

### 3. Lint Your Changes

```bash
buf lint
```

Fix any linting errors before proceeding.

### 4. Format Your Changes

```bash
buf format -w
```

### 5. Check for Breaking Changes

```bash
buf breaking --against '.git#branch=main'
```

**Important**: Breaking changes are not allowed in existing versions. If you need to make breaking changes, create a new version (e.g., v2).

### 6. Generate Code

```bash
buf generate
```

Verify that code generation works for all target languages.

### 7. Update Documentation

Update relevant documentation:

- Domain README files
- Main README.md
- Architecture documentation
- Client generation guides

### 8. Commit Your Changes

```bash
git add .
git commit -m "feat: add new domain for XYZ"
```

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

## Schema Design Guidelines

### General Principles

1. **Domain-Driven Design**: Organize schemas by business domain
2. **Multi-Tenancy**: Include tenant_id in all requests
3. **Consistency**: Follow existing patterns and conventions
4. **Documentation**: Add comments to complex messages and fields

### Message Design

#### Use Meaningful Names

```protobuf
// Good
message CreateUserRequest {
  string tenant_id = 1;
  string email = 2;
}

// Bad
message Req {
  string tid = 1;
  string e = 2;
}
```

#### Include Flattened Audit Fields

All domain entities MUST include flattened audit fields (not nested Metadata):

```protobuf
message User {
  string user_id = 1;
  string tenant_id = 2;
  // ... domain-specific fields ...

  // Audit fields (flattened for database efficiency)
  google.protobuf.Timestamp created_at = N [(buf.validate.field).required = true];
  google.protobuf.Timestamp updated_at = N+1;
  google.protobuf.Timestamp deleted_at = N+2;  // Soft delete
  int64 version = N+3;  // Optimistic locking
}
```

**Rationale:** Flattened structure enables efficient database indexing, direct filtering on timestamps, and better ORM mapping. Actor tracking (created_by, updated_by) is maintained in separate audit entity.

#### Use Enums for Fixed Values

```protobuf
enum UserStatus {
  USER_STATUS_UNSPECIFIED = 0;  // Always include UNSPECIFIED
  ACTIVE = 1;
  INACTIVE = 2;
}
```

#### Request/Response Naming

```protobuf
// Service name: UserService
// RPC name: CreateUser
// Request: CreateUserRequest
// Response: CreateUserResponse

service UserService {
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
}
```

### Field Numbering

- Start at 1
- Never reuse field numbers
- Reserve deprecated field numbers:

```protobuf
message User {
  reserved 5, 8 to 10;  // Deprecated fields
  reserved "old_field_name";

  string id = 1;
  string name = 2;
  // ...
}
```

### Import Guidelines

Use module-relative imports (no `proto/` prefix):

```protobuf
// Good - IDP imports
import "idp/api/v1/services.proto";  // Top-level IDP services
import "idp/identity/user/v1/user.proto";
import "idp/identity/user/events/v1/events.proto";
import "idp/identity/user/api/v1/request.proto";
import "core/metadata/v1/metadata.proto";

// Good - Core imports
import "core/api/pagination/v1/messages.proto";
import "core/client/v1/messages.proto";

// Bad
import "proto/idp/identity/user/v1/user.proto";
import "proto/core/api/pagination/v1/messages.proto";
```

### Package Naming

**IDP Domain-First Pattern (current):**

```protobuf
// Format: geniustechspace.idp.{domain}.{subdomain}.{layer}.v1
package geniustechspace.idp.identity.user.v1;           // Entity layer
package geniustechspace.idp.identity.user.events.v1;    // Events layer
package geniustechspace.idp.identity.user.api.v1;       // API layer
```

### Go Package Options

**Legacy:**

```protobuf
option go_package = "github.com/geniustechspace/protobuf/gen/go/users/v1;usersv1";
```

**IDP Domain-First:**

```protobuf
// Entity layer
option go_package = "github.com/geniustechspace/protobuf/gen/go/idp/identity/user/v1;idpidentityuserv1";

// Events layer
option go_package = "github.com/geniustechspace/protobuf/gen/go/idp/identity/user/events/v1;idpidentityusereventsv1";

// API layer
option go_package = "github.com/geniustechspace/protobuf/gen/go/idp/identity/user/api/v1;userapiv1";
```

Last segment after `;` should be concise and unique.

## Versioning Guidelines

### When to Create a New Version

Create a new version (v2, v3, etc.) when you need to:

- Remove fields
- Change field types
- Change field numbers
- Rename messages or fields
- Change service signatures

### Backward Compatible Changes (Same Version)

You can make these changes in the same version:

- Add new fields (use new field numbers)
- Add new messages
- Add new services
- Add new enum values
- Add new RPCs to existing services

### Field Deprecation

Mark fields as deprecated instead of removing them:

```protobuf
message User {
  string id = 1;
  string name = 2 [deprecated = true];  // Use first_name and last_name instead
  string first_name = 3;
  string last_name = 4;
}
```

## Testing Changes

### Lint Testing

```bash
buf lint
```

All schemas must pass linting.

### Breaking Change Testing

```bash
buf breaking --against '.git#branch=main'
```

Ensure no breaking changes in existing versions.

### Format Testing

```bash
buf format --diff --exit-code
```

Ensure code is properly formatted.

### Generation Testing

```bash
buf generate

# Verify Go code compiles
cd gen/go && go mod init test && go mod tidy && go build ./...

# Verify Python imports work
cd gen/python && python -c "import users.v1.users_pb2"
```

## Pull Request Process

### Before Submitting

- [ ] Changes pass `buf lint`
- [ ] Changes pass `buf breaking` (or new version created)
- [ ] Code is formatted with `buf format -w`
- [ ] Code generation succeeds
- [ ] Documentation is updated
- [ ] Commit messages follow Conventional Commits

### PR Description Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] New domain
- [ ] New version
- [ ] Backward-compatible changes
- [ ] Documentation
- [ ] Bug fix

## Changes Made

- Added X message
- Updated Y service
- Created Z documentation

## Breaking Changes

List any breaking changes (should be in new version only)

## Testing

- [ ] Buf lint passes
- [ ] Buf breaking passes
- [ ] Code generation succeeds
- [ ] Documentation updated

## Related Issues

Closes #123
```

### Review Process

1. Automated checks run (linting, breaking, generation)
2. Code review by maintainers
3. Address feedback
4. Approval required from at least one maintainer
5. Merge to main

### After Merge

- CI/CD pipeline runs
- Code is generated for all languages
- Clients are published (if configured)
- Documentation is deployed

## Adding a New Domain

### For IDP Subdomains (Recommended)

**Checklist:**

- [ ] Create subdomain directory: `proto/idp/{domain}/{subdomain}/`
- [ ] Create domain layer: `v1/{subdomain}.proto` with entity + enums
- [ ] Add flattened audit fields: created_at, updated_at, deleted_at, version
- [ ] Create events layer: `events/v1/events.proto` with domain events
- [ ] Create API layer: `api/v1/` with 4 files:
  - [ ] `api.proto` - Convenience import
  - [ ] `request.proto` - Request messages with buf/validate
  - [ ] `response.proto` - Response messages
  - [ ] `service.proto` - gRPC service definition
- [ ] Create README at each layer
- [ ] Update `proto/idp/README.md`
- [ ] Run `buf lint`
- [ ] Run `buf format -w`
- [ ] Run `buf generate --path proto/idp/{domain}/{subdomain}/`
- [ ] Test generated code
- [ ] Submit PR

**Three-Layer Structure:**

```
proto/idp/{domain}/{subdomain}/
├── v1/                      # Domain Layer
│   ├── {subdomain}.proto    # Entity + enums
│   └── README.md            # Domain documentation
├── events/v1/               # Events Layer
│   ├── events.proto         # Domain events
│   └── README.md            # Events documentation
└── api/v1/                  # API Layer
    ├── api.proto            # Convenience import
    ├── request.proto        # Request messages
    ├── response.proto       # Response messages
    ├── service.proto        # gRPC service
    └── README.md            # API documentation
```

### For Top-Level Domains

For domains outside IDP (like contact, hcm, preference):

- [ ] Create domain directory: `proto/{domain}/`
- [ ] Create subdomain: `proto/{domain}/{subdomain}/v1/`
- [ ] Add proto files with entities, enums, services
- [ ] Create README files
- [ ] Follow same validation and audit field patterns
- [ ] Run buf lint, format, and generate
- [ ] Submit PR

## Code Review Guidelines

### For Reviewers

- Check for backward compatibility
- Verify naming conventions
- Ensure documentation is clear
- Test code generation
- Look for security issues
- Validate multi-tenancy support

### For Contributors

- Be responsive to feedback
- Explain design decisions
- Update based on comments
- Retest after changes

## Questions or Issues?

- Open an issue for bugs or feature requests
- Start a discussion for design questions
- Join our Discord for community support

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Additional Resources

- [Protocol Buffers Documentation](https://protobuf.dev/)
- [Buf Documentation](https://buf.build/docs)
- [gRPC Documentation](https://grpc.io/docs/)
- [Domain-Driven Design](https://martinfowler.com/tags/domain%20driven%20design.html)

## Thank You!

Your contributions help make this project better for everyone. Thank you for your time and effort! 🎉
