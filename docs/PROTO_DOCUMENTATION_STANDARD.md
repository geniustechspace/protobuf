# Proto File Documentation Standard

## Overview

This document defines the comprehensive documentation standard for all protocol buffer definitions in this repository, including compliance annotations, security requirements, and field-level documentation.

## File Structure

### Header Section

Every proto file must begin with:

```protobuf
// Copyright 2024 GeniusTechSpace
//
// Licensed under the Apache License, Version 2.0 (the "License");
// ...

// [Message/Service/Enum Name] Definition
//
// Brief description of the file's purpose and domain.
//
// DOMAIN: [Domain name]
// CATEGORY: [Category, e.g., Security, Business Logic]
// VERSION: [v1, v2, etc.]
//
// COMPLIANCE:
// - SOC 2 [Control]: Description
// - ISO 27001 [Control]: Description
// - GDPR [Article]: Description
// - [Other standards]: Description
//
// SECURITY:
// - [Security consideration 1]
// - [Security consideration 2]
//
// AUDIT:
// - [Audit requirement 1]
// - [Audit requirement 2]
```

### Package and Options

```protobuf
syntax = "proto3";

package [domain].v1;

import "buf/validate/validate.proto";
import "[other imports]";

option csharp_namespace = "GeniusTechSpace.Protobuf.[Domain].V1";
option go_package = "github.com/geniustechspace/protobuf/gen/go/[domain]/v1;[domain]v1";
option java_multiple_files = true;
option java_package = "com.geniustechspace.protobuf.[domain].v1";
```

## Message Documentation

### Message-Level Documentation

Every message must include:

```protobuf
// [MessageName] [brief description].
//
// [Detailed description of message purpose and usage]
//
// COMPLIANCE:
// - [Relevant compliance standard and requirement]
//
// DATA CLASSIFICATION: [PII/Non-PII/PHI/Financial]
// RETENTION POLICY: [Retention requirements]
// ENCRYPTION: [Encryption requirements]
//
// VALIDATION RULES:
// - [Rule 1]
// - [Rule 2]
//
// EXAMPLE USAGE (Go):
//   [Code example]
//
// EXAMPLE USAGE (Python):
//   [Code example]
message MessageName {
  // Fields...
}
```

### Field-Level Documentation

Every field must include:

```protobuf
  // [Field description]
  //
  // REQUIRED/OPTIONAL: [Specify if required]
  // PII: [Yes/No] - [If PII, specify type]
  // ENCRYPTION: [At rest/In transit/Both/None]
  //
  // VALIDATION:
  // - [Validation rule 1]
  // - [Validation rule 2]
  //
  // SECURITY:
  // - [Security consideration if applicable]
  //
  // COMPLIANCE:
  // - [Relevant compliance requirement if applicable]
  //
  // ERROR CONDITIONS:
  // - [Error condition 1]
  // - [Error condition 2]
  string field_name = 1 [(buf.validate.field).string.min_len = 1];
```

## Enum Documentation

### Enum-Level Documentation

```protobuf
// [EnumName] [brief description].
//
// [Detailed description]
//
// COMPLIANCE:
// - [Relevant compliance standard]
//
// STATE TRANSITIONS:
// - [Transition 1]
// - [Transition 2]
//
// SECURITY IMPLICATIONS:
// - [Implication 1]
// - [Implication 2]
enum EnumName {
```

### Enum Value Documentation

```protobuf
  // [Value description]
  // AUTHENTICATION: [Allowed/Blocked]
  // AUTHORIZATION: [Authorization level]
  // COMPLIANCE: [Compliance note]
  // TRANSITIONS FROM: [Previous states]
  ENUM_VALUE_NAME = 1;
```

## Service Documentation

### Service-Level Documentation

```protobuf
// [ServiceName] [brief description].
//
// [Detailed service description]
//
// SERVICE LEVEL AGREEMENT (SLA):
// - Availability: [percentage]
// - Latency: [targets]
// - Error Rate: [target]
//
// COMPLIANCE CERTIFICATIONS:
// - [Certification 1]
// - [Certification 2]
//
// MONITORING:
// - [Monitoring requirement 1]
// - [Monitoring requirement 2]
service ServiceName {
```

### RPC Method Documentation

```protobuf
  // [MethodName] [brief description].
  //
  // [Detailed description]
  //
  // AUTHENTICATION: [Required/Optional] - [Details]
  // AUTHORIZATION: [Required permissions]
  //
  // VALIDATION:
  // - [Validation rule 1]
  // - [Validation rule 2]
  //
  // EVENTS PUBLISHED:
  // - [Event 1]
  //
  // ERRORS:
  // - [Error code]: [Description]
  //
  // COMPLIANCE:
  // - [Relevant compliance requirement]
  //
  // RATE LIMITING:
  // - [Rate limit specification]
  //
  // EXAMPLE:
  //   [Code example]
  rpc MethodName(RequestType) returns (ResponseType);
```

## Compliance Documentation

### SOC 2 Controls

When documenting SOC 2 compliance, reference specific controls:

- **CC6.1**: Logical and physical access controls
- **CC6.2**: Prior to issuing system credentials and granting system access
- **CC6.6**: Encryption of customer data at rest and in transit
- **CC6.7**: Use of encryption keys
- **CC6.8**: Monitoring of system components

Example:
```protobuf
// COMPLIANCE:
// - SOC 2 CC6.1: Implements logical access controls through role validation
```

### ISO 27001 Controls

Reference specific Annex A controls:

- **A.9.2**: User access management
- **A.9.4**: System and application access control
- **A.18.1**: Compliance with legal and contractual requirements

Example:
```protobuf
// COMPLIANCE:
// - ISO 27001 A.9.2.1: User registration and de-registration procedures
```

### GDPR Articles

Reference specific GDPR articles:

- **Article 4**: Definitions (personal data, processing, etc.)
- **Article 5**: Principles (lawfulness, purpose limitation, etc.)
- **Article 15**: Right of access
- **Article 16**: Right to rectification
- **Article 17**: Right to erasure
- **Article 25**: Data protection by design

Example:
```protobuf
// COMPLIANCE:
// - GDPR Article 5: Data minimization principle applied
// - GDPR Article 25: Data protection by design (encryption at rest)
```

### HIPAA Requirements

For healthcare-related data:

- **164.312(a)(1)**: Access control
- **164.312(c)(1)**: Integrity controls
- **164.312(d)**: Person or entity authentication
- **164.312(e)(1)**: Transmission security

Example:
```protobuf
// COMPLIANCE:
// - HIPAA 164.312(a)(1): Implements unique user identification
```

## Security Documentation

### Required Security Fields

Every message handling sensitive data must document:

```protobuf
// SECURITY:
// - Encryption: [At rest/In transit/Both]
// - Access Control: [Who can access]
// - Audit Logging: [What is logged]
// - Rate Limiting: [If applicable]
// - Data Classification: [Public/Internal/Confidential/Restricted]
```

### PII Documentation

For fields containing PII:

```protobuf
// PII: Yes - [Type of PII: Direct identifier/Indirect identifier/Sensitive]
// ENCRYPTION: [Required at rest/Required in transit/Both]
// COMPLIANCE: GDPR Article 4(1) - Personal data identifier
// DATA SUBJECT RIGHTS: [Access/Rectification/Erasure/Portability]
```

## Validation Documentation

### Protovalidate Rules

Document all validation rules with rationale:

```protobuf
// VALIDATION:
// - Email format: RFC 5322 compliant
// - Minimum length: 3 characters (prevents null/empty entries)
// - Maximum length: 50 characters (database constraint)
// - Pattern: ^[a-zA-Z0-9_-]+$ (security - prevents injection)
string email = 1 [(buf.validate.field).string = {
  email: true
  min_len: 3
  max_len: 50
}];
```

## Examples

### Complete Message Example

```protobuf
// User represents a user account in the system.
//
// This is the primary aggregate for user management, containing
// profile information, preferences, and security status.
//
// COMPLIANCE:
// - SOC 2 CC6.1: User entity for access control
// - GDPR Article 5: Personal data processing
// - ISO 27001 A.9.2: User access management
//
// DATA CLASSIFICATION: PII
// RETENTION POLICY: 90 days after soft delete
// ENCRYPTION: Email and phone encrypted at rest
//
// VALIDATION RULES:
// - tenant_id: Required for multi-tenant isolation
// - email: Valid format, unique within tenant
// - username: 3-50 chars, alphanumeric only
//
// EXAMPLE USAGE (Go):
//   user := &usersv1.User{
//       Metadata:  metadata,
//       TenantId:  "tenant_123",
//       Email:     "user@example.com",
//       Username:  "johndoe",
//       Status:    usersv1.UserStatus_USER_STATUS_ACTIVE,
//   }
message User {
  // Unique identifier and audit metadata.
  // REQUIRED: Must be set for all persisted entities.
  // AUDIT: Includes created_by, updated_by, timestamps.
  core.v1.Metadata metadata = 1;

  // Tenant identifier for multi-tenant isolation.
  // REQUIRED: Non-empty string.
  // COMPLIANCE: SOC 2 CC6.1 - Logical access controls.
  // VALIDATION: Minimum length 1 character.
  string tenant_id = 2 [(buf.validate.field).string.min_len = 1];

  // User's email address.
  // REQUIRED: Valid email format.
  // PII: Yes - Direct identifier under GDPR.
  // ENCRYPTION: Encrypted at rest.
  // VALIDATION: RFC 5322 email format.
  string email = 3 [(buf.validate.field).string.email = true];
}
```

## Documentation Checklist

Before committing any proto file, verify:

- [ ] File header with copyright and license
- [ ] Module-level documentation with domain, compliance, security
- [ ] All messages documented with purpose and compliance
- [ ] All fields documented with requirements and validation
- [ ] All enums documented with state transitions
- [ ] All services documented with SLA and authentication
- [ ] All RPCs documented with authorization and errors
- [ ] Examples provided in at least one language
- [ ] Validation rules explained with rationale
- [ ] Security and encryption requirements specified
- [ ] PII fields marked and compliance noted
- [ ] Audit requirements documented

## Tools and Automation

### Documentation Linting

Use `buf lint` with documentation rules:

```yaml
# buf.yaml
lint:
  use:
    - STANDARD
    - COMMENTS  # Enable comment linting
```

### Documentation Generation

Generate documentation from proto files:

```bash
buf generate --template buf.gen.yaml
```

### Validation

Ensure all required documentation sections present:

```bash
# Check for required documentation sections
grep -r "COMPLIANCE:" proto/
grep -r "SECURITY:" proto/
grep -r "PII:" proto/
```

## Maintenance

- Review documentation quarterly for accuracy
- Update compliance references when standards change
- Add new examples when patterns evolve
- Keep validation rules synchronized with implementation
- Document all breaking changes in migration guides

## References

- [SOC 2 Trust Services Criteria](https://www.aicpa.org/soc2)
- [ISO 27001 Standards](https://www.iso.org/isoiec-27001-information-security.html)
- [GDPR Official Text](https://gdpr-info.eu/)
- [NIST 800-53](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/index.html)
