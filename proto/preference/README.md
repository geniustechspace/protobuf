# Preference Domain

**Package:** `geniustechspace.preference`

## Overview

Preference domain manages user-level configuration, settings, and preferences across localization, notifications, privacy, and accessibility. This is **non-PII configuration data** that controls how users interact with systems.

## Architecture

Preference is **separate from identity** - it manages frequently changing UI/UX configurations, not personal identifiers.

```
proto/preference/
├── user/v1/             # User-level preferences
└── tenant/v1/           # Tenant-level configuration (future)
```

## Entities

### 1. UserPreferences (user/v1/preferences.proto)

**User preferences and settings**

**Localization:**
- Preferred language (ISO 639-1)
- Timezone (IANA)
- Locale (BCP 47)
- Date/time format
- Currency (ISO 4217)

**Notification Preferences:**
- Email, SMS, push, in-app toggles
- Notification frequency (realtime, daily, weekly digest)
- Quiet hours (HH:MM format)

**Privacy Preferences:**
- Profile visibility (public, private, connections_only)
- Search engine indexing
- Online status display
- Last activity display
- Allow contact from non-connections

**Accessibility Preferences:**
- High contrast mode
- Reduced motion
- Screen reader optimization
- Font size multiplier (1.0 = default, 1.5 = 150%)
- Keyboard navigation only

**Relationship:** 1-to-1 with User  
**PII:** No - Configuration data only  
**Use Cases:**
- UI personalization
- Localization/i18n
- Communication consent (GDPR compliance)
- Accessibility adaptations (WCAG compliance)
- Privacy controls

## Design Principles

### 1. Non-PII Classification
```
Identity (PII):         Name, birthdate, gender → Rarely changes, high security
Preferences (Non-PII):  Language, theme, dark mode → Changes frequently, low security
```

Preferences can be cached aggressively, replicated globally, and stored in fast databases without PII restrictions.

### 2. Consent Management
Notification preferences map directly to GDPR/CCPA consent:
```protobuf
NotificationPreferences {
  email_enabled: true    // GDPR Article 7 consent
  sms_enabled: false     // TCPA consent required
  push_enabled: true     // Device permission
}
```

### 3. Accessibility First
Preferences support WCAG 2.1 compliance:
```protobuf
AccessibilityPreferences {
  high_contrast: true    // WCAG 1.4.3 Contrast
  font_size_multiplier: 1.5  // WCAG 1.4.4 Resize text
  screen_reader: true    // WCAG 1.3.1 Info and Relationships
}
```

### 4. Multi-Tenancy
Uses `tenant_path` for hierarchical isolation - tenant admins can set defaults, users can override.

## Common Patterns

### All Entities Include
- ✅ UUID primary key (preferences_id)
- ✅ User ID foreign key (1-to-1 relationship)
- ✅ Hierarchical tenant path
- ✅ Nested preference groups (notifications, privacy, accessibility)
- ✅ Audit timestamps (created_at, updated_at)
- ✅ Reserved ranges for extensibility
- ✅ No version field (preferences don't need optimistic locking)

### Reserved Field Ranges
- **10-19**: Localization expansion
- **23-29**: Preference groups expansion
- **32-39**: Future expansion

## Validation Rules

### Localization
- Language: ISO 639-1 (exactly 2 lowercase letters: `en`, `es`, `fr`)
- Locale: BCP 47 (`en-US`, `fr-FR` - language-COUNTRY)
- Currency: ISO 4217 (exactly 3 uppercase letters: `USD`, `EUR`)
- Timezone: IANA timezone database (`America/New_York`, `Europe/London`)

### Preferences
- tenant_path: 1-512 characters
- Notification frequency: Enum validation (realtime, daily_digest, weekly_digest)
- Quiet hours: HH:MM format (24-hour)
- Font size multiplier: Float (0.5 to 3.0 typical range)

## Usage Examples

### Creating Default Preferences

```protobuf
UserPreferences {
  preferences_id: "uuid-123"
  user_id: "user-456"
  tenant_path: "acme-corp"
  preferred_language: "en"
  timezone: "America/New_York"
  locale: "en-US"
  date_format: "MM/DD/YYYY"
  time_format: "12h"
  currency: "USD"
  
  notifications: {
    email_enabled: true
    sms_enabled: false  // Requires separate consent
    push_enabled: true
    in_app_enabled: true
    frequency: "realtime"
  }
  
  privacy: {
    profile_visibility: "connections_only"
    searchable: false
    show_online_status: true
    show_last_activity: false
    allow_contact: false
  }
  
  accessibility: {
    high_contrast: false
    reduced_motion: false
    screen_reader: false
    font_size_multiplier: 1.0
    keyboard_navigation: false
  }
}
```

### Partial Updates

```protobuf
// Update only language
UpdateUserPreferences {
  preferences_id: "uuid-123"
  preferred_language: "es"
  locale: "es-ES"
}

// Enable high contrast mode
UpdateUserPreferences {
  preferences_id: "uuid-123"
  accessibility: {
    high_contrast: true
  }
}
```

## API Operations

### Preferences APIs (user/api/v1/)
- GetUserPreferences (by user_id or preferences_id)
- UpdateUserPreferences (partial update support)
- ResetUserPreferences (restore defaults)
- GetTenantDefaults (tenant-level default preferences)

## Events (events/v1/)

### Preference Events
- `UserPreferencesCreated`
- `UserPreferencesUpdated` (with changed fields)
- `LocalizationChanged` (language/timezone/locale)
- `NotificationPreferencesChanged` (consent tracking)
- `PrivacyPreferencesChanged` (privacy settings audit)
- `AccessibilityPreferencesChanged` (accessibility audit)
- `UserPreferencesReset` (back to defaults)

## Compliance

### GDPR Compliance
- **Article 7**: Notification preferences = consent management
- **Article 6**: Privacy preferences = lawful basis for processing
- **Article 17**: Right to erasure (reset to defaults, then delete)
- **Recital 32**: Consent must be freely given, specific, informed

### WCAG 2.1 Compliance
- **Level A**: Keyboard navigation (2.1.1)
- **Level AA**: High contrast (1.4.3), Resize text (1.4.4)
- **Level AAA**: Reduced motion (2.3.3)

### CAN-SPAM Act / TCPA
- Email opt-in: Required for marketing emails
- SMS opt-in: Required before sending SMS (TCPA)
- Frequency preferences: Honor quiet hours
- Unsubscribe: Must support opt-out

### CCPA Compliance
- Privacy preferences = "Do Not Sell My Personal Information"
- Searchable flag = control over data sharing
- Profile visibility = control over personal data disclosure

## Integration Points

### Consumed By
- **UI/Frontend**: Theme, language, accessibility adaptations
- **Notification Service**: Email/SMS consent, frequency, quiet hours
- **Analytics**: Respect privacy settings for tracking
- **Search Engines**: Honor searchable flag for indexing
- **i18n Systems**: Language, locale, date/time/currency formats

### Default Sources
- **Browser**: Language, timezone detection
- **GeoIP**: Country → default locale, currency
- **Tenant Config**: Tenant-level defaults
- **System**: Application-wide defaults

## Related Documentation
- **Identity Profile:** `../idp/identity/profile/v1/README.md`
- **Contact:** `../contact/README.md`
- **HCM:** `../hcm/employee/v1/README.md`

## Migration Notes

If migrating from embedded settings:
1. Extract preferences from user profile
2. Create UserPreferences with defaults
3. Migrate notification consent from separate consent tables
4. Link accessibility settings from separate accessibility tables
5. Maintain backward compatibility with cached preferences
