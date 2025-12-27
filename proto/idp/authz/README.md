# IDP Authorization (authz)

Enterprise-grade Attribute-Based Access Control (ABAC) with Role-Based Access Control (RBAC) integration.

## Architecture

**ABAC-First Design**: The authorization engine uses ABAC as the core policy evaluation framework. RBAC is implemented as a special case of ABAC where role membership is treated as a subject attribute (`subject.roles`).

## Subdomains

```
proto/idp/authz/
├── permission/v1/     # Permission value objects (resource:action pairs)
├── role/v1/           # Role aggregate (permission collections)
├── policy/v1/         # ABAC policies with conditions
├── attribute/v1/      # Attribute definitions (SRAE model)
└── evaluation/v1/     # Policy evaluation engine types
```

## Key Concepts

### SRAE Attribute Model (NIST SP 800-162)

- **Subject (S)**: Who is requesting (user, service, API key)
- **Resource (R)**: What is being accessed (document, user, project)
- **Action (A)**: What operation is requested (read, write, delete)
- **Environment (E)**: Request context (time, IP, location, risk score)

### Policy Evaluation

All authorization requests are evaluated by the ABAC engine:

1. Collect attributes from various sources (token claims, database, external APIs)
2. Match against applicable policies
3. Combine results using configurable algorithm (deny-overrides, permit-overrides, etc.)
4. Return decision with obligations and advice

### RBAC Integration

RBAC policies are ABAC policies with `subject.roles` conditions:

```protobuf
Policy {
  name: "admin-access"
  type: RBAC
  conditions: [
    { key: "subject.roles", operator: IN, values: ["admin", "super-admin"] }
  ]
  effect: ALLOW
  actions: ["*"]
  resources: ["*"]
}
```

## Usage Examples

### Authorization Request

```protobuf
AuthorizationRequest request = {
  subject: {
    subject_id: "user_123",
    roles: ["editor", "reviewer"],
    groups: ["engineering"],
    attributes: [
      { name: "department", string_value: "engineering" }
    ]
  },
  resource: {
    resource_type: "document",
    resource_id: "doc_456",
    attributes: [
      { name: "classification", string_value: "confidential" }
    ]
  },
  action: {
    action_id: "read"
  },
  environment: {
    ip_address: "10.0.0.1",
    risk_score: 25
  }
};

AuthorizationResponse response = evaluator.Evaluate(request);
if (response.decision == Decision.PERMIT) {
  // Fulfill obligations
  for (obligation in response.obligations) {
    fulfill(obligation);
  }
  // Grant access
}
```

### Policy Definition

```protobuf
Policy {
  name: "confidential-docs-engineering"
  type: ABAC
  effect: ALLOW
  subjects: [{ type: USER, attributes: { "department": "engineering" } }]
  actions: ["read", "write"]
  resources: ["/documents/confidential/*"]
  conditions: [
    { key: "env.risk_score", operator: LESS_THAN, values: ["50"] },
    { key: "env.ip_address", operator: IN, values: ["10.0.0.0/8"] }
  ]
  priority: 100
}
```

## Multi-Tenancy

Authorization policies and entities are **tenant-agnostic**. Tenant scoping is provided via `TenantContext` at the API layer, enabling:

- Domain models independent of multi-tenancy
- Easy switching between isolation modes
- Clean separation of authorization and tenancy concerns

## Compliance

- **NIST SP 800-162**: ABAC standard implementation
- **XACML 3.0**: Policy evaluation model
- **SOC 2 CC6.2**: Access control decisions
- **ISO 27001 A.9.4**: Access control policy
- **GDPR Article 5**: Purpose limitation via policies

## Import Paths

```protobuf
// Permissions
import "idp/authz/permission/v1/permission.proto";

// Roles
import "idp/authz/role/v1/role.proto";

// Policies
import "idp/authz/policy/v1/policy.proto";

// ABAC Attributes
import "idp/authz/attribute/v1/attribute.proto";

// Policy Evaluation
import "idp/authz/evaluation/v1/evaluation.proto";
```

## See Also

- [Attribute README](attribute/v1/README.md) - Attribute definitions
- [Evaluation README](evaluation/v1/README.md) - Policy evaluation
- [Multitenancy Domain](../../multitenancy/README.md) - Tenant context
- [IDP Architecture](../ARCHITECTURE.md) - Overall architecture
