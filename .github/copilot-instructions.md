# Copilot Instructions - Protobuf Schema Repository

## Project Overview

Enterprise-grade Protocol Buffer schemas for multi-tenant microservices using [Buf](https://buf.build) for validation, linting, breaking change detection, and multi-language code generation. This is a **schema-only** repository - no application code, only `.proto` definitions with strict compliance and documentation standards.

## Critical Architecture Patterns

## Development Workflows

### Essential Buf Commands

```bash
buf lint                           # MUST pass before commits
buf format -w                      # Auto-format all protos
buf breaking --against '.git#branch=main'  # Check compatibility (PRs only)
buf generate                       # Generate code for all languages
buf generate --path proto/idp/     # Generate specific domain
```

### Critical Validation Rules

Use `buf/validate/validate.proto` annotations extensively:

- Required fields: `[(buf.validate.field).string.min_len = 1]`
- Email validation: `[(buf.validate.field).string.email = true]`
- Patterns: `[(buf.validate.field).string.pattern = "^[a-z0-9-]+$"]`
- Enums: `[(buf.validate.field).enum.defined_only = true]`

See `docs/VALIDATION.md` for comprehensive examples.

### Breaking Change Policy

- **NEVER break v1 APIs** - no field removal, type changes, or renumbering
- Reserved fields for deprecation: `reserved 5, 8 to 10; reserved "old_field";`
- Use `[deprecated = true]` annotation instead of removing fields
- Create v2 package for breaking changes

### CI/CD Pipeline (`buf.yml`)

Uses `bufbuild/buf-action@v1` which automatically:

- Lints and formats on every push/PR
- Checks breaking changes on PRs (compares to base branch)
- Generates multi-language clients (Go, Python, Java, TypeScript, C#)
- Creates per-domain client artifacts
- Publishes docs to GitHub Pages

## Project-Specific Conventions

### Import Paths

**Module-relative only** (no `proto/` prefix):

```protobuf
import "core/v1/common.proto";           // ✅ Correct
import "proto/core/v1/common.proto";     // ❌ Wrong
```

### Package Naming

```protobuf
package geniustechspace.users.v1;  // Format: geniustechspace.domain.version
```

### Field Numbering Rules

- Start at 1 (field 0 is invalid in proto3)
- tenant_path always field 1 or 2 (field 2 if entity_id is field 1). Use hierarchical tenant paths (e.g., "acme-corp", "acme-corp/customer-1") and prefer a max length of 512.
- NEVER reuse field numbers - use `reserved` instead

### Go Package Options

```protobuf
option go_package = "github.com/geniustechspace/protobuf/gen/go/users/v1;usersv1";
```

Last segment after `;` MUST match package name with version suffix (e.g., `usersv1`).

### Documentation Requirements (CRITICAL)

Every proto file MUST include (see `docs/PROTO_DOCUMENTATION_STANDARD.md`):

**File Header:**

```protobuf
// DOMAIN: [domain name]
// COMPLIANCE: SOC 2 CC6.1, GDPR Article 5, ISO 27001 A.9.2
// SECURITY: Authentication required, tenant isolation enforced
// PII: [Yes/No] - [description]
```

**Field-Level:**

```protobuf
// Email address. REQUIRED.
// PII: Yes - GDPR Article 4(1) personal identifier
// ENCRYPTION: Required at rest
// VALIDATION: RFC 5322 email format
string email = 3 [(buf.validate.field).string.email = true];
```

**Service RPCs:**

```protobuf
// CreateUser creates new user account.
// AUTHENTICATION: Required - valid bearer token
// AUTHORIZATION: Requires 'users:create' permission
// COMPLIANCE: SOC 2 CC6.1 (User provisioning)
// RATE LIMIT: 100/min per tenant
rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
```

## Common Patterns

### Pagination (Industry-Standard Cursor-Based)

**Single Responsibility:** Pagination only - sorting and filtering are separate concerns

```protobuf
import "core/api/pagination/v1/messages.proto";

message ListUsersRequest {
  string tenant_path = 1 [(buf.validate.field).string.max_len = 512];

  // Pagination (separate concern)
  core.api.pagination.v1.PaginationRequest pagination = 2;
  
  // Sorting (Google AIP-132 - add directly to request)
  string order_by = 3;  // e.g., "created_at desc"
  
  // Filtering (Google AIP-160 - add directly to request)
  string filter = 4;  // e.g., "status='active'"
}

message ListUsersResponse {
  repeated User users = 1;
  core.api.pagination.v1.PaginationResponse pagination = 2;
}
```

**Pagination uses cursor map with client-side caching:**

- First page: omit `cursor`, server returns cursor for next page
- Next pages: provide cached `cursor` from previous response → O(log n) performance
- Client caches cursors per page for bidirectional navigation
- End of results: `cursor` is empty

**Sorting format (Google AIP-132 standard):**

- `"created_at desc"` - newest first
- `"name"` - alphabetical ascending  
- `"priority desc, created_at"` - multi-field sort

### Entity Metadata Pattern (CRITICAL)

**All domain entities MUST include flattened audit fields for database efficiency.**

DO NOT use nested `core.metadata.v1.Metadata` message in entities. Use direct fields instead to support efficient search, filtering, and indexing in databases.

**Required Audit Fields Template:**

```protobuf
message User {
  string user_id = 1;
  string tenant_path = 2 [(buf.validate.field).string.max_len = 512];
  // ... domain-specific fields ...

  // Created timestamp. IMMUTABLE after creation.
  // COMPLIANCE: SOC 2 CC6.3, GDPR Article 30 (audit trail)
  google.protobuf.Timestamp created_at = N [(buf.validate.field).required = true];

  // Last updated timestamp.
  // COMPLIANCE: SOC 2 CC6.3 (change tracking)
  google.protobuf.Timestamp updated_at = N+1;

  // Deletion timestamp. If set, entity is soft deleted.
  // COMPLIANCE: GDPR Article 17, SOC 2 CC6.3 (deletion audit trail)
  // QUERY: Use "WHERE deleted_at IS NULL" for active records
  google.protobuf.Timestamp deleted_at = N+2;

  // Optimistic locking version counter. Incremented on each update.
  // COMPLIANCE: SOC 2 CC6.1 (data integrity, concurrent modification protection)
  int64 version = N+3;
}
```

**Rationale:** Flattened structure enables:

- Efficient database indexing on audit fields
- Direct filtering/searching on created_at, updated_at, deleted_at
- Better ORM mapping and query performance
- Simplified database schema generation
- Single source of truth for deletion (deleted_at IS NULL = active, IS NOT NULL = deleted)

**Note:** Actor tracking (created_by, updated_by) should be maintained in separate audit entity for detailed change history while keeping domain entities lean for frequent queries.

### Domain Events Pattern

```protobuf
// UserCreated emitted when user account is successfully created.
// EVENT: Publish to event bus for downstream consumers
// COMPLIANCE: Audit trail requirement
message UserCreated {
  string event_id = 1;  // UUID for event tracing
  google.protobuf.Timestamp event_timestamp = 2;
  string tenant_path = 3 [(buf.validate.field).string.max_len = 512];
  string user_id = 4;
  string email = 5;  // Safe for event - no password
  string created_by = 6;
  string correlation_id = 7;  // For distributed tracing
}
```

### Error Handling

Use standard gRPC status codes. For detailed errors, include context in metadata, not custom error types.

## Key Files Reference

- `buf.yaml` - Buf config with linting rules (STANDARD + UNARY_RPC)
- `buf.gen.yaml` - Code generation config for 5 languages + protovalidate
- `CONTRIBUTING.md` - PR process, field numbering, deprecation patterns
- `docs/VALIDATION.md` - Protovalidate examples and patterns
- `docs/PROTO_DOCUMENTATION_STANDARD.md` - Compliance documentation requirements
- `QUICK_START.md` - Installation, generation, usage examples

## Testing Changes

Before committing:

1. `buf lint` must pass (zero errors)
2. `buf format -w` to auto-format
3. `buf breaking --against '.git#branch=main'` on PRs (should pass unless creating v2)
4. `buf generate` verify generation works for all languages
5. Check `gen/go/` compiles: `cd gen/go && go mod init test && go build ./...`

## Common Gotchas

1. **Package naming** - Use domain-first for IDP: `geniustechspace.idp.{domain}.{subdomain}.{layer}.v1`
2. **Check if domain exists** - Use `proto/idp/` for identity and auth operations
3. **Empty directories** - `proto/idp/authn/v1/`, `proto/core/[subdomain]/` may be empty; check README location
4. **Import paths** - Always module-relative, never absolute with `proto/` prefix
5. **Tenant isolation** - Every request MUST have tenant_id; every service MUST enforce it
6. **Validation is NOT optional** - All user input fields need protovalidate annotations
7. **Compliance annotations** - Required for all PII fields and sensitive operations

## When Adding New Domains

1. Create directory: `proto/newdomain/v1/`
2. Create modular files: `messages.proto`, `service.proto`, `events.proto`, `enums.proto`
3. Add domain README explaining purpose and patterns
4. Include flattened audit fields in all entities (created_at, updated_at, deleted_at, version)
5. Include tenant_path in all requests (use hierarchical tenant paths; max_len=512)
6. Add protovalidate annotations
7. Document compliance requirements
8. Update main README.md with domain description
9. Test: `buf lint && buf generate --path proto/newdomain/`

## Additional Resources

- Buf docs: <https://buf.build/docs>
- Protovalidate: <https://github.com/bufbuild/protovalidate>
- gRPC style guide: <https://grpc.io/docs/guides/>
- Domain-driven design applied to this repo: Check modular IDP structure in `proto/idp/`
