# Contact Domain

**Package:** `geniustechspace.contact`

## Overview

Contact domain provides communication channel management for users - addresses, phone numbers, and email addresses. This is a **shared infrastructure domain** used across multiple systems (shipping, billing, support, 2FA, notifications).

## Architecture

Contact information is **independent of identity** - it can exist without authentication and is consumed by many domains beyond IDP.

```
proto/contact/
├── api/v1/              # Unified API (aggregates all subdomains)
├── address/
│   ├── api/v1/          # Address management API
│   └── v1/              # Physical addresses
├── email/
│   ├── api/v1/          # Email management API
│   └── v1/              # Email addresses
└── phone/
    ├── api/v1/          # Phone management API
    └── v1/              # Phone numbers with verification
```

## Entities

### 1. UserAddress (address/v1/address.proto)

**Physical mailing addresses**

- Address labels (enum): HOME, WORK, BILLING, SHIPPING, CUSTOM
- Full address fields (street, city, locality, state, postal, country)
- Custom label support for CUSTOM label type
- Tags for metadata (e.g., "default-shipping", "verified")
- Primary flag per label
- ISO 3166-1 alpha-2 country validation (case-insensitive)
- Verification timestamp

**Relationships:** 1-to-many with User  
**PII:** Yes - GDPR Article 4(1)  
**Use Cases:**

- E-commerce: Shipping & billing addresses
- Support: Contact information
- Compliance: Physical location for tax/legal purposes
- Logistics: Delivery address validation

### 2. UserPhoneNumber (phone/v1/phone.proto)

**Phone numbers with verification**

- Phone labels (enum): MOBILE, HOME, WORK, FAX, PAGER, CUSTOM
- E.164 format validation (+1234567890)
- Country code extraction
- Extension support (business phones)
- Custom label support for CUSTOM label type
- Tags for metadata (e.g., "emergency", "sms-enabled")
- Verification timestamp
- Primary flag per label

**Relationships:** 1-to-many with User  
**PII:** Yes - GDPR Article 4(1)  
**Use Cases:**

- Authentication: 2FA/MFA, SMS OTP
- Notifications: SMS alerts
- Support: Voice calls, WhatsApp contact
- Verification: Phone ownership proofing

### 3. UserEmail (email/v1/email.proto)

**Email addresses with verification**

- Email labels (enum): PERSONAL, WORK, SCHOOL, OTHER, CUSTOM
- RFC 5322 email format validation
- Domain extraction (e.g., "example.com")
- Custom label support for CUSTOM label type
- Tags for metadata (e.g., "verified", "newsletter", "marketing-consent")
- Verification timestamp
- Primary flag per label
- Normalized to lowercase for consistency

**Relationships:** 1-to-many with User  
**PII:** Yes - GDPR Article 4(1)  
**Use Cases:**

- Authentication: Email/password login, magic links
- Notifications: Transactional emails, newsletters
- Password Recovery: Reset links
- Communication: Support, marketing emails
- Verification: Email ownership proofing

## Design Principles

### 1. Domain Independence

Contact info exists independently of authentication:

```protobuf
// Guest checkout needs address without user account
UserAddress {
  address_id: "uuid-123"
  user_id: ""  // Empty for guest
  tenant_path: "store-tenant"
}
```

### 2. Verification Lifecycle

```
Create → Unverified → Send Code → Verify → Verified
```

Phone verification is critical for:

- 2FA/MFA enrollment
- SMS notification consent (TCPA compliance)
- Fraud prevention

### 3. Multi-Tenancy

Uses `tenant_path` for hierarchical isolation:

- Platform level: Your IDP tenant
- Application level: Their customer's org
- Unlimited nesting: `"acme/customer-1/sub-org"`

## Common Patterns

### Enum-Based Labels with Custom Fallback

All contact entities use enum-based classification with custom label support:

```protobuf
enum AddressLabel {
  UNSPECIFIED = 0;
  HOME = 1;
  WORK = 2;
  BILLING = 3;
  SHIPPING = 4;
  CUSTOM = 5;  // Use custom_label field
}

message UserAddress {
  AddressLabel label = 4;
  string custom_label = 11;  // Required when label = CUSTOM
  repeated string tags = 12;  // Optional metadata
}
```

**Benefits:**

- Type safety for common cases
- Database query efficiency (enum = integer)
- Flexibility for custom labels (e.g., "Mom's House", "Summer Cottage")
- Tags for additional metadata without schema changes

### All Entities Include

- ✅ UUID primary keys (address_id, phone_id, email_id)
- ✅ User ID foreign key (nullable for guest users)
- ✅ Hierarchical tenant path
- ✅ Enum-based label classification (with CUSTOM fallback)
- ✅ Custom label support for user-defined types
- ✅ Tags for metadata (lowercase-alphanumeric-hyphen)
- ✅ Primary flag (one primary per label)
- ✅ Verification timestamp
- ✅ Audit timestamps (created_at, updated_at, deleted_at)
- ✅ Optimistic locking (version)
- ✅ Reserved ranges for extensibility

### Reserved Field Ranges

- **10-19**: Entity-specific expansion (custom_label, tags, flags)
- **24-29**: Audit field expansion
- **31-39**: Future expansion

## Validation Rules

### Address

- Label: Enum (HOME, WORK, BILLING, SHIPPING, CUSTOM)
- Custom label: 1-100 characters (required when label = CUSTOM)
- Country: ISO 3166-1 alpha-2 (2 letters, case-insensitive: `^[A-Za-z]{2}$`)
- Postal code: Up to 20 characters
- City: Up to 100 characters (primary locality)
- Locality: Up to 100 characters (secondary: district, neighborhood, town)
- Street, state: Max length validation
- Tags: Lowercase alphanumeric with hyphens, max 20 tags
- tenant_path: 1-512 characters

### Phone

- Label: Enum (MOBILE, HOME, WORK, FAX, PAGER, CUSTOM)
- Number: E.164 format (`^\\+[1-9]\\d{1,14}$`)
- Extension: Up to 10 characters
- Custom label: 1-100 characters (required when label = CUSTOM)
- Tags: Lowercase alphanumeric with hyphens, max 20 tags
- tenant_path: 1-512 characters

### Email

- Label: Enum (PERSONAL, WORK, SCHOOL, OTHER, CUSTOM)
- Email: RFC 5322 format, 3-254 characters, normalized to lowercase
- Domain: Extracted from email, up to 253 characters
- Custom label: 1-100 characters (required when label = CUSTOM)
- Tags: Lowercase alphanumeric with hyphens, max 20 tags
- tenant_path: 1-512 characters

## Usage Examples

### Creating Address

```protobuf
UserAddress {
  address_id: "uuid-123"
  user_id: "user-456"
  tenant_path: "acme-corp"
  label: SHIPPING  // Enum value
  street_line1: "123 Main St"
  city: "San Francisco"
  locality: "SOMA District"
  state: "CA"
  postal_code: "94102"
  country: "US"
  tags: ["default-shipping", "verified"]
  is_primary: true
}
```

### Phone with Custom Label

```protobuf
UserPhoneNumber {
  phone_id: "uuid-789"
  user_id: "user-456"
  tenant_path: "acme-corp"
  label: CUSTOM
  custom_label: "Mom's iPhone"
  number: "+14155551234"
  tags: ["emergency", "primary-contact"]
}
```

### Email Verification Flow

```protobuf
// Step 1: Create unverified
UserEmail {
  email_id: "uuid-101"
  user_id: "user-456"
  tenant_path: "acme-corp"
  label: WORK
  email: "john@acme.com"
  domain: "acme.com"
  tags: ["primary-contact"]
  is_primary: true
}

// Step 2: After verification
UserEmail {
  ...
  verified_at: "2025-12-11T10:30:00Z"
  tags: ["primary-contact", "verified"]
}
```

## API Operations

### Unified API (contact/api/v1/services.proto)

Aggregates all subdomain services into a single API surface:

- PhoneService, AddressService, EmailService
- Clients can use unified API OR individual subdomain APIs

### Address APIs (contact/address/api/v1/)

- CreateAddress, GetAddress, UpdateAddress, DeleteAddress
- ListAddresses (by user, by label, by tenant, with pagination)
- VerifyAddress (postal code, geocode, manual verification)

### Phone APIs (contact/phone/api/v1/)

- CreatePhoneNumber, GetPhoneNumber, UpdatePhoneNumber, DeletePhoneNumber
- ListPhoneNumbers (by user, by label, by tenant, with pagination)
- SendVerificationCode (SMS/voice), VerifyPhoneNumber

### Email APIs (contact/email/api/v1/)

- CreateEmail, GetEmail, UpdateEmail, DeleteEmail
- ListEmails (by user, by label, by tenant, with pagination)
- SendVerificationEmail, VerifyEmail (token-based)

## Events (events/v1/)

### Address Events

- `AddressCreated`
- `AddressUpdated`
- `AddressDeleted`
- `AddressVerified`

### Phone Events

- `PhoneNumberCreated`
- `PhoneNumberUpdated`
- `PhoneNumberDeleted`
- `PhoneNumberVerified` (important for 2FA enrollment)
- `VerificationCodeSent`

### Email Events

- `EmailCreated`
- `EmailUpdated`
- `EmailDeleted`
- `EmailVerified` (important for authentication)
- `VerificationEmailSent`

## Compliance

### GDPR Compliance

- **Article 4(1)**: Address and phone are personal identifiers
- **Article 5**: Data minimization - only necessary fields
- **Article 17**: Right to erasure via soft delete (deleted_at)
- **Article 30**: Audit trail (created_at, updated_at)

### Industry Standards

- **vCard RFC 6350**: Contact information standard
- **E.164**: International phone number format
- **ISO 3166-1**: Country codes
- **CRM Standards**: Salesforce, Microsoft Dynamics contact models

### Telecommunications Compliance

- **TCPA**: Phone verification required before SMS marketing
- **GDPR Article 7**: Consent for phone/SMS communications
- **Do Not Call**: Phone type classification for call restrictions

## Integration Points

### Consumed By

- **IDP**: 2FA/MFA phone verification, password recovery
- **E-commerce**: Shipping & billing addresses
- **Support**: Contact information for tickets
- **Notifications**: SMS, voice calls
- **Fraud Detection**: Address/phone verification
- **Tax Systems**: Address for tax jurisdiction
- **Payment**: Billing address validation

### Integrations

- **Address Validation Services**: USPS, Google Maps, SmartyStreets
- **Phone Verification Services**: Twilio Verify, Vonage Verify
- **2FA Providers**: Twilio Authy, Duo Security
- **SMS Gateways**: Twilio, AWS SNS, MessageBird

## Related Documentation

- **Identity Profile:** `../idp/identity/profile/v1/README.md`
- **Preferences:** `../preferences/user/v1/README.md`
- **HCM:** `../hcm/employee/v1/README.md`
