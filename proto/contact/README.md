# Contact Domain

**Package:** `geniustechspace.contact`

## Overview

Contact domain provides communication channel management for users - addresses, phone numbers, and email addresses. This is a **shared infrastructure domain** used across multiple systems (shipping, billing, support, 2FA, notifications).

## Architecture

Contact information is **independent of identity** - it can exist without authentication and is consumed by many domains beyond IDP.

```
proto/contact/
├── address/v1/          # Physical addresses
├── phone/v1/            # Phone numbers with verification
└── email/v1/            # Email addresses (future)
```

## Entities

### 1. UserAddress (address/v1/address.proto)

**Physical mailing addresses**

- Address types: home, work, billing, shipping
- Full address fields (street, city, state, postal, country)
- Primary flag per type
- ISO 3166-1 alpha-2 country validation

**Relationships:** 1-to-many with User  
**PII:** Yes - GDPR Article 4(1)  
**Use Cases:**
- E-commerce: Shipping & billing addresses
- Support: Contact information
- Compliance: Physical location for tax/legal purposes
- Logistics: Delivery address validation

### 2. UserPhoneNumber (phone/v1/phone.proto)

**Phone numbers with verification**

- Phone types: mobile, home, work, fax
- E.164 format validation (+1234567890)
- Country code extraction
- Extension support (business phones)
- Verification tracking (verified flag + timestamp)
- Primary flag per type

**Relationships:** 1-to-many with User  
**PII:** Yes - GDPR Article 4(1)  
**Use Cases:**
- Authentication: 2FA/MFA, SMS OTP
- Notifications: SMS alerts
- Support: Voice calls, WhatsApp contact
- Verification: Phone ownership proofing

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

### All Entities Include
- ✅ UUID primary keys (address_id, phone_id)
- ✅ User ID foreign key (nullable for guest users)
- ✅ Hierarchical tenant path
- ✅ Type classification (address_type, phone_type)
- ✅ Primary flag (one primary per type)
- ✅ Audit timestamps (created_at, updated_at, deleted_at)
- ✅ Optimistic locking (version)
- ✅ Reserved ranges for extensibility

### Reserved Field Ranges
- **12-19**: Entity-specific expansion
- **23-29**: Audit field expansion
- **31-39**: Future expansion

## Validation Rules

### Address
- Country: ISO 3166-1 alpha-2 (exactly 2 uppercase letters)
- Postal code: Up to 20 characters
- Street, city, state: Max length validation
- tenant_path: 1-512 characters

### Phone
- Number: E.164 format (`^\\+[1-9]\\d{1,14}$`)
- Extension: Up to 10 characters
- Type: 1-50 characters
- tenant_path: 1-512 characters

## Usage Examples

### Creating Address

```protobuf
UserAddress {
  address_id: "uuid-123"
  user_id: "user-456"
  tenant_path: "acme-corp"
  address_type: "shipping"
  street_line1: "123 Main St"
  city: "San Francisco"
  state: "CA"
  postal_code: "94102"
  country: "US"
  is_primary: true
}
```

### Phone with Verification

```protobuf
// Step 1: Create unverified
UserPhoneNumber {
  phone_id: "uuid-789"
  user_id: "user-456"
  tenant_path: "acme-corp"
  phone_type: "mobile"
  number: "+14155551234"
  verified: false
}

// Step 2: After verification
UserPhoneNumber {
  ...
  verified: true
  verified_at: "2025-12-09T10:30:00Z"
}
```

## API Operations

### Address APIs (address/api/v1/)
- CreateAddress, GetAddress, UpdateAddress, DeleteAddress
- ListAddresses (by user, by type, by tenant)
- SetPrimaryAddress

### Phone APIs (phone/api/v1/)
- CreatePhoneNumber, GetPhoneNumber, UpdatePhoneNumber, DeletePhoneNumber
- ListPhoneNumbers (by user, by type, by tenant)
- SendVerificationCode, VerifyPhoneNumber
- SetPrimaryPhoneNumber

## Events (events/v1/)

### Address Events
- `AddressCreated`
- `AddressUpdated`
- `AddressDeleted`
- `PrimaryAddressChanged`

### Phone Events
- `PhoneNumberCreated`
- `PhoneNumberUpdated`
- `PhoneNumberDeleted`
- `PhoneNumberVerified` (important for 2FA enrollment)
- `VerificationCodeSent`
- `VerificationFailed`
- `PrimaryPhoneNumberChanged`

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
