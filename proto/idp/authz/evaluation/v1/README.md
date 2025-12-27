# Authorization Evaluation Engine

Enterprise-grade policy evaluation engine for ABAC with RBAC integration.

## Overview

This module defines the policy evaluation types following XACML standards:

- **Authorization Request**: SRAE (Subject, Resource, Action, Environment) attributes
- **Authorization Response**: Decision with obligations and advice
- **Evaluation Trace**: Debugging and audit trail

## Key Types

### AuthorizationRequest

Complete request for access decision including:
- Subject attributes (who)
- Resource attributes (what)
- Action attributes (operation)
- Environment attributes (context)
- Tenant scope for multi-tenant evaluation

### AuthorizationResponse

Decision response including:
- **Decision**: PERMIT, DENY, INDETERMINATE, NOT_APPLICABLE
- **Obligations**: Required actions for PEP
- **Advice**: Optional guidance
- **Metrics**: Performance data
- **Trace**: Debug information

### Decision Values

| Decision | Meaning |
|----------|---------|
| `PERMIT` | Access granted |
| `DENY` | Access explicitly denied |
| `INDETERMINATE` | Cannot determine (error) |
| `NOT_APPLICABLE` | No policies apply |

### Combining Algorithms

How multiple policy results are combined:

| Algorithm | Behavior |
|-----------|----------|
| `DENY_OVERRIDES` | Any deny wins (default, most secure) |
| `PERMIT_OVERRIDES` | Any permit wins |
| `FIRST_APPLICABLE` | First matching policy decides |
| `ORDERED_DENY_OVERRIDES` | Priority-ordered, deny wins |

## Obligations and Advice

### Obligations (Mandatory)

Actions that MUST be performed by the PEP:
- `LOG`: Audit logging
- `NOTIFY`: Alert users/admins
- `REQUIRE_MFA`: Step-up authentication
- `ENCRYPT`: Data encryption
- `MASK_DATA`: PII redaction
- `RATE_LIMIT`: Throttling

### Advice (Optional)

Non-mandatory guidance:
- `DISPLAY_WARNING`: User warnings
- `SUGGEST_ALTERNATIVE`: Alternative actions
- `PROVIDE_HELP`: Documentation links

## Usage

```protobuf
// Build authorization request
AuthorizationRequest request = {
  subject: {
    subject_id: "user-123",
    roles: ["admin"],
    groups: ["engineering"],
  },
  resource: {
    resource_type: "document",
    resource_id: "doc-456",
  },
  action: {
    action_id: "read",
  },
  environment: {
    ip_address: "10.0.0.1",
    risk_score: 25,
  },
};

// Evaluate and handle decision
AuthorizationResponse response = authzService.Evaluate(request);
if (response.decision == Decision.PERMIT) {
  // Fulfill obligations
  for (Obligation o : response.obligations) {
    fulfill(o);
  }
  // Proceed with access
} else {
  // Deny access with reason
  denyAccess(response.details.reason);
}
```

## Compliance

- **XACML 3.0**: Policy evaluation standard
- **NIST SP 800-162**: ABAC implementation
- **SOC 2 CC6.2**: Access control decisions
- **ISO 27001 A.9.4**: Access control policy enforcement
