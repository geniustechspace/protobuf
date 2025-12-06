# Core Common Types

Foundational value objects used across all domains in the GeniusTech Space ecosystem.

## Package

```protobuf
package geniustechspace.core.common.v1;
```

## Overview

The `core/common` module provides reusable value objects that establish consistency across all microservices. These types handle common data structures like addresses, money, contact information, tenant context, and pagination.

## Messages

### Address

Physical or mailing address with complete location information.

**Fields:**
- `street_line1` (string) - Street address line 1 (max 255 chars)
- `street_line2` (string) - Street address line 2, optional (max 255 chars)
- `city` (string) - City or municipality (max 100 chars)
- `state` (string) - State, province, or region (max 100 chars)
- `postal_code` (string) - Postal/ZIP code (max 20 chars)
- `country` (string) - Country name or ISO code (2-100 chars)

**Usage:**
```protobuf
import "core/common/v1/common.proto";

message TenantProfile {
  geniustechspace.core.common.v1.Address billing_address = 1;
  geniustechspace.core.common.v1.Address shipping_address = 2;
}
```

**Compliance:** GDPR Article 4(1) - Addresses are PII

---

### ContactInfo

Comprehensive contact details for users and organizations.

**Fields:**
- `email` (string) - Primary email address (RFC 5322 format, max 255 chars)
- `phone` (string) - Primary phone with country code (E.164 format, max 20 chars)
- `mobile` (string) - Mobile phone with country code (max 20 chars)
- `fax` (string) - Fax number with country code (max 20 chars)

**Usage:**
```protobuf
message User {
  geniustechspace.core.common.v1.ContactInfo contact = 1;
}
```

**Compliance:** GDPR Article 4(1) - Contact info is PII

---

### Money

Currency-aware monetary values stored as minor units (cents).

**Fields:**
- `currency` (string) - ISO 4217 currency code (3 uppercase letters, e.g., "USD", "EUR")
- `amount` (int64) - Amount in smallest currency unit (e.g., cents)

**Examples:**
```
$10.50 USD = Money { currency: "USD", amount: 1050 }
€25.99 EUR = Money { currency: "EUR", amount: 2599 }
¥1000 JPY = Money { currency: "JPY", amount: 1000 }
```

**Usage:**
```protobuf
message Product {
  geniustechspace.core.common.v1.Money price = 1;
}
```

**Compliance:** PCI DSS for payment amounts

---

### TenantContext

Multi-tenant isolation and context.

**Fields:**
- `tenant_id` (string) - Tenant identifier (1-64 chars, lowercase alphanumeric with hyphens)
- `tenant_name` (string) - Display name (max 255 chars)
- `environment` (string) - Environment type: "production", "staging", "development", "test"

**Usage:**
```protobuf
message CreateUserRequest {
  geniustechspace.core.common.v1.TenantContext tenant_context = 1;
  // ... other fields
}
```

**Security:** REQUIRED in all service requests for tenant isolation

**Compliance:** SOC 2 CC6.1 - Logical Access Controls

---

### PaginationRequest

Pagination controls for list operations.

**Fields:**
- `page` (int32) - Page number, 1-indexed (default: 1)
- `page_size` (int32) - Items per page (1-1000, default: 20)
- `sort_by` (string) - Field name to sort by (max 64 chars)
- `sort_order` (string) - "asc" or "desc" (default: "desc")

**Usage:**
```protobuf
message ListUsersRequest {
  string tenant_id = 1;
  geniustechspace.core.common.v1.PaginationRequest pagination = 2;
}
```

---

### PaginationResponse

Pagination metadata for list responses.

**Fields:**
- `page` (int32) - Current page number
- `page_size` (int32) - Items in current page (0-1000)
- `total_items` (int64) - Total items across all pages
- `total_pages` (int32) - Total number of pages
- `has_next` (bool) - More pages exist
- `has_previous` (bool) - Previous pages exist

**Usage:**
```protobuf
message ListUsersResponse {
  repeated User users = 1;
  geniustechspace.core.common.v1.PaginationResponse pagination = 2;
}
```

## Import Path

```protobuf
import "core/common/v1/common.proto";
```

## Validation

All fields use `buf/validate` annotations for validation:
- Email addresses validated per RFC 5322
- Currency codes validated as ISO 4217
- String length limits enforced
- Pattern matching for tenant_id and sort_order

## Security Considerations

1. **PII Fields:** Address and ContactInfo contain personally identifiable information
2. **Encryption:** Recommend encryption at rest for residential addresses
3. **Validation:** Always validate and sanitize input data
4. **Tenant Isolation:** Always enforce tenant_id validation

## See Also

- [Core Metadata](../metadata/README.md) - Entity audit trails
- [Core Pagination](../pagination/README.md) - Alternative pagination types
- [Main Core README](../README.md) - Complete core module documentation
