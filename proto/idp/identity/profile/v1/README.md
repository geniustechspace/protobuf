# Identity Profile Domain

**Package:** `geniustechspace.idp.identity.profile.v1`

## Overview

Profile domain defines **core personal identity** - the essential attributes that define who a person is. Focused purely on identity-specific information.

## Domain Boundaries

**Identity Profile Contains:**

- Personal names, biography, physical attributes
- Social media profiles (for identity verification)

**Moved to Separate Domains:**

- Contact info (address, phone) → `contact/` domain
- Employment → `hcm/employee/` domain
- Preferences (settings) → `preferences/user/` domain

## Architecture

```
proto/idp/identity/profile/v1/
├── profile.proto          # Core identity (UserProfile)
└── social.proto           # Social profiles (UserSocialProfile)
```

## Hierarchical Multi-Tenancy

All entities use `tenant_path` for unlimited nesting:

```
"acme-corp"                              // Level 1
"acme-corp/customer-1"                   // Level 2
"acme-corp/customer-1/sub-org"           // Level 3+
```

**Benefits:**

- Works with any isolation strategy (separate DB, row-based, schema-based)
- No limit on nesting depth
- Simple prefix matching for queries

## Entities

### 1. UserProfile (profile.proto)

Core personal identity information.

**Fields:**

- profile_id, user_id, tenant_path
- Personal names: given_name, family_name, middle_name, nickname
- Identity attributes: gender, birth_date
- Visual identity: picture_url, website_url
- Biography: bio
- Extension: custom_attributes (map)
- Audit: created_at, updated_at, deleted_at, version

**Relationship:** 1-to-1 with User  
**PII:** Yes - GDPR Article 4(1) & Article 9 (special category)

### 2. UserSocialProfile (social.proto)

Social media profiles for identity verification.

**Fields:**

- social_profile_id, user_id, tenant_path
- Provider: github, linkedin, twitter, facebook
- Username, profile_url
- OAuth: oauth_connection_id
- Verification: verified, verified_at
- Audit: created_at, updated_at, deleted_at, version

**Relationship:** 1-to-many with User  
**PII:** Yes - Can reveal personal information  
**Use Cases:** Social login, professional networking, identity verification

## Common Patterns

### All Entities Include

- UUID primary keys
- User ID foreign key
- Hierarchical tenant_path (1-512 characters)
- Audit timestamps (created_at, updated_at, deleted_at)
- Optimistic locking (version at field 30)
- Reserved ranges (13-19, 24-29, 31-39)
- buf/validate validation rules

## Validation Rules

- UUIDs: `.string.uuid`
- URLs: `.string.uri`
- Tenant path: 1-512 characters
- String fields: Max length validation
- Birth date: google.protobuf.Timestamp

## Usage Examples

### User Profile

```protobuf
UserProfile {
  profile_id: "uuid-123"
  user_id: "user-456"
  tenant_path: "acme-corp"
  given_name: "Jane"
  family_name: "Smith"
  nickname: "JSmith"
  gender: "Female"
  birth_date: "1990-05-15T00:00:00Z"
  picture_url: "https://cdn.example.com/avatars/jane.jpg"
  bio: "Software engineer passionate about distributed systems"
}
```

### Social Profile

```protobuf
UserSocialProfile {
  social_profile_id: "social-789"
  user_id: "user-456"
  tenant_path: "acme-corp"
  provider: "github"
  username: "janesmith"
  profile_url: "https://github.com/janesmith"
  oauth_connection_id: "oauth-conn-123"
  verified: true
  verified_at: "2025-01-15T10:30:00Z"
}
```

## API Operations (api/v1/)

### Profile APIs

- GetProfile, UpdateProfile, DeleteProfile
- ListProfiles (by tenant)

### Social Profile APIs

- ListSocialProfiles, GetSocialProfile
- CreateSocialProfile, UpdateSocialProfile, DeleteSocialProfile
- VerifySocialProfile (OAuth verification)

## Events (events/v1/)

### Profile Events

- ProfileCreated
- ProfileUpdated
- ProfileDeleted
- ProfilePictureChanged

### Social Profile Events

- SocialProfileCreated
- SocialProfileUpdated
- SocialProfileDeleted
- SocialProfileVerified
- SocialProfileConnected (OAuth)
- SocialProfileDisconnected

## Compliance

### GDPR Compliance

- **Article 4(1)**: Names are personal identifiers
- **Article 5**: Data minimization - only identity fields
- **Article 9**: Special category data (gender, birth_date)
- **Article 17**: Right to erasure (soft delete)
- **Article 30**: Audit trail (timestamps)

### SOC 2 Compliance

- **CC6.1**: Data integrity (version field)
- **CC6.3**: Audit trail (created_at, updated_at, deleted_at)

## Integration Points

### References FROM Identity Profile

- Contact domain: Address, phone, email (separate entities)
- HCM domain: Employment records
- Preferences domain: User settings

### Consumed By

- Authentication: Profile display after login
- User directories: Name, picture for listings
- Social verification: OAuth identity proofing
- Profile pages: User bio, social links

## Related Documentation

- **Contact Domain:** `../../../contact/README.md`
- **Preferences Domain:** `../../../preferences/README.md`
- **HCM Domain:** `../../../hcm/README.md`
- **User API:** `../user/api/v1/README.md`
