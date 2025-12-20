Record subpackage (domain layer): per-record (subdomain) messages.

This package follows the three-layer IDP architecture:


Use this package for the Record entity only. Records reference `domain_id` from
the `domain` package. Keep business logic and propagation details in the
service/reconciler that consumes these protos.

Follow protovalidate and documentation conventions from repository standards.
 `tenant_path` is field 2 when `domain_id` is field 1. Use hierarchical tenant paths (max_len=512).

