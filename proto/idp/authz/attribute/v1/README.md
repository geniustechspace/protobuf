# Authorization Attributes

Enterprise-grade attribute definitions for Attribute-Based Access Control (ABAC).

## Overview

This module defines the attribute types and structures used in ABAC policy evaluation. Following the NIST SP 800-162 ABAC model, attributes are categorized into:

- **Subject (S)**: Attributes describing the requester (user, service, API key)
- **Resource (R)**: Attributes describing the target resource
- **Action (A)**: Attributes describing the requested operation
- **Environment (E)**: Attributes describing the context (time, location, device)

## Key Types

### AttributeDefinition

Defines an attribute schema including:
- Category (SRAE model)
- Data type (string, integer, boolean, timestamp, etc.)
- Source (token claim, header, database lookup, external API)
- Sensitivity level (for audit/logging control)

### Attribute Value Types

Runtime attribute values used during policy evaluation:
- `SubjectAttributes` - Complete subject attribute set
- `ResourceAttributes` - Complete resource attribute set
- `ActionAttributes` - Action being requested
- `EnvironmentAttributes` - Request context (IP, location, device, risk score)

## Attribute Sources

Attributes can be resolved from multiple sources:

| Source | Description |
|--------|-------------|
| `TOKEN_CLAIM` | JWT/OAuth2 token claims |
| `REQUEST_HEADER` | HTTP request headers |
| `REQUEST_CONTEXT` | gRPC metadata, request context |
| `USER_PROFILE` | Database lookup (PIP) |
| `GROUP_MEMBERSHIP` | Group membership lookup |
| `EXTERNAL_API` | External Policy Information Point |
| `COMPUTED` | Runtime computed values |
| `STATIC` | Constant values |

## Usage

Attributes are used in:
1. **Policy Definitions** - Conditions reference attribute names
2. **Evaluation Requests** - Attribute values provided for decision making
3. **Audit Logging** - Sensitivity controls what gets logged

## Compliance

- **NIST SP 800-162**: ABAC standard implementation
- **SOC 2 CC6.2**: Fine-grained access control
- **ISO 27001 A.9.4**: Access control policy
