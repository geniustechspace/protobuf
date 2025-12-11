# Role Domain Model

**Package:** `geniustechspace.idp.authz.role.v1`

## Overview

Domain entities and enums for role-based authorization controls.

## Purpose

- Define role entity structure for access control
- Implement fine-grained authorization patterns
- Support Role-Based Access Control (RBAC) and Attribute-Based Access Control (ABAC)
- Enforce least-privilege principle

## Compliance

- **SOC 2 CC6.1:** Logical and physical access controls
- **ISO 27001 A.9.2:** User access management
- **ISO 27001 A.9.4:** Access control to systems and applications

## Entities

### Role

Primary entity for role management. Supports hierarchical structures and dynamic evaluation.

## Authorization Models

- **RBAC:** Role-based access control via role assignments
- **ABAC:** Attribute-based access control via policy evaluation
- **Hybrid:** Combined RBAC + ABAC for flexible authorization

## Related Documentation

- **Domain Events:** `../events/v1/README.md`
- **API Layer:** `../api/v1/README.md`
