DNS subpackages for domain and record management.

This folder contains the DNS domain and DNS record subpackages. Use the
`domain` package for ownership/registrar/zone-level metadata and the
`record` package for per-record (subdomain) CRUD and resolver operations.

Follow repository conventions in `docs/PROTO_DOCUMENTATION_STANDARD.md`:
- module-relative imports
- `tenant_path` placement rules (use hierarchical tenant paths; max_len=512)
- flattened audit fields (`created_at`, `updated_at`, `deleted_at`, `version`)
- protovalidate annotations
