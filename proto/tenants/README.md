# Tenants Domain

## Overview

The Tenants domain manages multi-tenant organizations. It handles tenant lifecycle, configuration, tier management, and usage tracking. This domain is central to the multi-tenancy architecture.

## Services

### TenantService

Provides tenant management operations.

## Key Components

### Tenant

```protobuf
message Tenant {
  core.v1.Metadata metadata = 1;
  string name = 2;
  string slug = 3;
  string domain = 4;
  TenantStatus status = 5;
  TenantTier tier = 6;
  TenantSettings settings = 7;
  core.v1.ContactInfo contact_info = 8;
  core.v1.Address billing_address = 9;
  map<string, string> metadata_fields = 10;
}
```

### Enums

#### TenantStatus
```protobuf
enum TenantStatus {
  TENANT_STATUS_UNSPECIFIED = 0;
  TENANT_STATUS_ACTIVE = 1;
  TENANT_STATUS_SUSPENDED = 2;
  TENANT_STATUS_TRIAL = 3;
  TENANT_STATUS_INACTIVE = 4;
  TENANT_STATUS_DELETED = 5;
}
```

#### TenantTier
```protobuf
enum TenantTier {
  TENANT_TIER_UNSPECIFIED = 0;
  TENANT_TIER_FREE = 1;
  TENANT_TIER_STARTER = 2;
  TENANT_TIER_PROFESSIONAL = 3;
  TENANT_TIER_ENTERPRISE = 4;
}
```

### TenantSettings

```protobuf
message TenantSettings {
  int32 max_users = 1;
  int32 max_storage_gb = 2;
  bool custom_domain_enabled = 3;
  bool sso_enabled = 4;
  bool api_access_enabled = 5;
  repeated string allowed_ip_ranges = 6;
  map<string, string> feature_flags = 7;
  TenantBranding branding = 8;
}
```

## gRPC Operations

### CreateTenant

Create a new tenant organization.

**Request**:
```protobuf
message CreateTenantRequest {
  string name = 1;
  string slug = 2;
  string domain = 3;
  TenantTier tier = 4;
  core.v1.ContactInfo contact_info = 5;
  core.v1.Address billing_address = 6;
}
```

**Example**:
```go
resp, err := tenantClient.CreateTenant(ctx, &tenantsv1.CreateTenantRequest{
    Name: "Acme Corporation",
    Slug: "acme",
    Domain: "acme.example.com",
    Tier: tenantsv1.TenantTier_TENANT_TIER_PROFESSIONAL,
    ContactInfo: &corev1.ContactInfo{
        Email: "admin@acme.com",
        Phone: "+1-555-0100",
    },
})
```

### GetTenant

Retrieve tenant information.

### UpdateTenant

Update tenant details and settings.

### UpdateTenantStatus

Change tenant status (activate, suspend, etc.).

**Request**:
```protobuf
message UpdateTenantStatusRequest {
  string tenant_id = 1;
  TenantStatus status = 2;
  string reason = 3;
}
```

### UpdateTenantTier

Upgrade or downgrade tenant tier.

**Request**:
```protobuf
message UpdateTenantTierRequest {
  string tenant_id = 1;
  TenantTier tier = 2;
}
```

### GetTenantUsage

Retrieve tenant usage statistics.

**Response**:
```protobuf
message GetTenantUsageResponse {
  int32 user_count = 1;
  int64 storage_used_bytes = 2;
  int64 api_calls_count = 3;
  google.protobuf.Timestamp last_activity_at = 4;
}
```

## Domain Events

### TenantCreatedEvent
```protobuf
message TenantCreatedEvent {
  string tenant_id = 1;
  string name = 2;
  string slug = 3;
  TenantTier tier = 4;
  google.protobuf.Timestamp created_at = 5;
}
```

### TenantStatusChangedEvent
```protobuf
message TenantStatusChangedEvent {
  string tenant_id = 1;
  TenantStatus old_status = 2;
  TenantStatus new_status = 3;
  string reason = 4;
  google.protobuf.Timestamp changed_at = 5;
}
```

### TenantTierChangedEvent
```protobuf
message TenantTierChangedEvent {
  string tenant_id = 1;
  TenantTier old_tier = 2;
  TenantTier new_tier = 3;
  google.protobuf.Timestamp changed_at = 4;
}
```

## Multi-Tenancy Patterns

### Database Isolation Strategies

#### 1. Database per Tenant (Highest Isolation)
```yaml
tenant_acme:
  database: postgres-acme
  host: db-acme.example.com
tenant_globex:
  database: postgres-globex
  host: db-globex.example.com
```

**Pros**: Maximum isolation, compliance-friendly
**Cons**: Higher cost, complex management

#### 2. Schema per Tenant (Balanced)
```sql
CREATE SCHEMA tenant_acme;
CREATE SCHEMA tenant_globex;
```

**Pros**: Good isolation, easier backups per tenant
**Cons**: Schema management overhead

#### 3. Row-Level Tenancy (Most Cost-Effective)
```sql
SELECT * FROM users WHERE tenant_id = 'tenant_acme';
```

**Pros**: Simple, cost-effective
**Cons**: Risk of data leakage, performance impact

### Tenant Resolution

Resolve tenant from:
1. **Subdomain**: `acme.example.com` → tenant_acme
2. **Custom domain**: `app.acme.com` → tenant_acme
3. **Path**: `example.com/acme` → tenant_acme
4. **Header**: `X-Tenant-ID: tenant_acme`

### Tenant Middleware

```go
func TenantMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Extract tenant from subdomain
        host := r.Host
        parts := strings.Split(host, ".")
        slug := parts[0]
        
        // Resolve tenant
        tenant, err := tenantRepo.GetBySlug(ctx, slug)
        if err != nil {
            http.Error(w, "Tenant not found", http.StatusNotFound)
            return
        }
        
        // Check tenant status
        if tenant.Status != tenantsv1.TenantStatus_TENANT_STATUS_ACTIVE {
            http.Error(w, "Tenant suspended", http.StatusForbidden)
            return
        }
        
        // Add to context
        ctx := context.WithValue(r.Context(), "tenant", tenant)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}
```

## Tier Management

### Feature Matrix

| Feature | Free | Starter | Professional | Enterprise |
|---------|------|---------|--------------|------------|
| Users | 5 | 25 | 100 | Unlimited |
| Storage | 1 GB | 10 GB | 100 GB | Custom |
| API Access | ❌ | ✅ | ✅ | ✅ |
| SSO | ❌ | ❌ | ✅ | ✅ |
| Custom Domain | ❌ | ❌ | ✅ | ✅ |
| Priority Support | ❌ | ❌ | ❌ | ✅ |

### Tier Enforcement

```go
func CheckTierLimit(tenant *Tenant, feature string) error {
    settings := tenant.Settings
    
    switch feature {
    case "max_users":
        currentUsers := getUserCount(tenant.Metadata.Id)
        if currentUsers >= settings.MaxUsers {
            return errors.New("user limit reached")
        }
    case "custom_domain":
        if !settings.CustomDomainEnabled {
            return errors.New("custom domain not available in current tier")
        }
    case "sso":
        if !settings.SsoEnabled {
            return errors.New("SSO not available in current tier")
        }
    }
    return nil
}
```

## Trial Management

### Trial Period
- Default: 14 days
- Status: `TENANT_STATUS_TRIAL`
- Automatic conversion or suspension after trial ends

### Trial to Paid Conversion

```go
// Subscribe to TenantCreatedEvent
func HandleTenantCreated(event *TenantCreatedEvent) {
    if event.Tier == TenantTier_TENANT_TIER_TRIAL {
        // Schedule trial end reminder
        scheduler.Schedule(event.TenantId, "trial_ending_soon", time.Now().Add(11*24*time.Hour))
        
        // Schedule trial end
        scheduler.Schedule(event.TenantId, "trial_ended", time.Now().Add(14*24*time.Hour))
    }
}
```

## Branding

### Custom Branding

```protobuf
message TenantBranding {
  string logo_url = 1;
  string primary_color = 2;
  string secondary_color = 3;
  string favicon_url = 4;
  string custom_css = 5;
}
```

**Example**:
```go
branding := &tenantsv1.TenantBranding{
    LogoUrl:       "https://cdn.acme.com/logo.png",
    PrimaryColor:  "#0066cc",
    SecondaryColor: "#ff9900",
    FaviconUrl:    "https://cdn.acme.com/favicon.ico",
}
```

## Usage Tracking

Track tenant usage for:
- Billing calculations
- Tier limit enforcement
- Analytics and reporting

```go
// Update usage metrics
func UpdateTenantUsage(tenantId string) {
    usage := &TenantUsage{
        TenantId:         tenantId,
        UserCount:        countUsers(tenantId),
        StorageUsedBytes: calculateStorage(tenantId),
        ApiCallsCount:    countApiCalls(tenantId, last24Hours),
        LastActivityAt:   time.Now(),
    }
    usageRepo.Save(usage)
}
```

## Best Practices

1. **Validate tenant_id**: Always validate tenant_id in every request
2. **Check status**: Verify tenant status before processing requests
3. **Enforce limits**: Check tier limits before allowing operations
4. **Audit changes**: Log all tenant configuration changes
5. **Secure isolation**: Ensure complete data isolation between tenants
6. **Performance**: Index tenant_id in all multi-tenant tables
7. **Monitoring**: Track tenant-specific metrics separately

## Integration Examples

### Onboarding Flow

```go
// 1. Create tenant
tenant, _ := tenantClient.CreateTenant(ctx, createReq)

// 2. Create admin user
user, _ := userClient.CreateUser(ctx, &usersv1.CreateUserRequest{
    TenantId: tenant.Tenant.Metadata.Id,
    Email:    "admin@acme.com",
    Roles:    []string{"admin"},
})

// 3. Create subscription
subscription, _ := billingClient.CreateSubscription(ctx, &billingv1.CreateSubscriptionRequest{
    TenantId: tenant.Tenant.Metadata.Id,
    PlanId:   "professional",
    Trial:    true,
})

// 4. Send welcome email
notificationClient.SendNotification(ctx, &notificationsv1.SendNotificationRequest{
    TenantId: tenant.Tenant.Metadata.Id,
    UserIds:  []string{user.User.Metadata.Id},
    Type:     notificationsv1.NotificationType_NOTIFICATION_TYPE_SUCCESS,
    Title:    "Welcome to the platform!",
})
```

## Dependencies

- Core domain for Metadata, ContactInfo, Address
- Billing domain for subscription management
- Users domain for user management

## Related Domains

- **Billing**: Subscription and payment processing
- **Users**: Tenant user management
- **Notifications**: Tenant communication
