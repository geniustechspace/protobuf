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

#### Include Metadata

All domain entities should include Metadata:

```protobuf
message User {
  core.v1.Metadata metadata = 1;
  string tenant_id = 2;
  // ... other fields
}
```

#### Use Enums for Fixed Values

```protobuf
enum UserStatus {
  USER_STATUS_UNSPECIFIED = 0;  // Always include UNSPECIFIED
  USER_STATUS_ACTIVE = 1;
  USER_STATUS_INACTIVE = 2;
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

Use module-relative imports:

```protobuf
// Good
import "core/v1/common.proto";
import "users/v1/users.proto";

// Bad
import "proto/core/v1/common.proto";
```

### Package Naming

```protobuf
// Format: domain.version
package users.v1;
package billing.v2;
```

### Go Package Options

```protobuf
option go_package = "github.com/geniustechspace/protobuf/gen/go/users/v1;usersv1";
```

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

### Version Directory Structure

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

### Deprecation

Mark deprecated fields instead of removing them:

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

### Checklist

- [ ] Create domain directory: `proto/newdomain/v1/`
- [ ] Create main proto file: `newdomain.proto`
- [ ] Create events file: `events.proto`
- [ ] Define messages with Metadata
- [ ] Define gRPC service
- [ ] Define domain events
- [ ] Create domain README
- [ ] Update main README
- [ ] Run `buf lint`
- [ ] Run `buf generate`
- [ ] Test generated code
- [ ] Submit PR

### Template Structure

```
proto/newdomain/
├── v1/
│   ├── newdomain.proto
│   └── events.proto
└── README.md
```

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
