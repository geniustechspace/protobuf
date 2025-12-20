Domain subpackage (domain layer): holds domain (registrar/ownership/zone metadata).

This package follows the three-layer IDP architecture:

- Domain layer: `proto/dns/domain/v1/` (entities and enums only)
- Events layer: `proto/dns/domain/events/v1/` (domain events)
- API layer:    `proto/dns/domain/api/v1/` (gRPC services and request/response messages)

Conventions:
- `tenant_path` is field 2 when `domain_id` is field 1. Use hierarchical tenant paths (max_len=512).
- Include flattened audit fields on domain entities.
- Use protovalidate annotations for required and pattern checks.

See `docs/PROTO_DOCUMENTATION_STANDARD.md` for full documentation requirements.
