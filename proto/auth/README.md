# Auth Domain

## Overview

The Auth domain handles authentication and session management. It provides secure user authentication, token management, session tracking, and password reset functionality.

## Services

### AuthService

Provides authentication and session management operations.

## Key Components

### Messages

#### Credentials
```protobuf
message Credentials {
  string email = 1;
  string password = 2;
  string tenant_id = 3;
}
```

#### TokenResponse
```protobuf
message TokenResponse {
  string access_token = 1;
  string refresh_token = 2;
  string token_type = 3;
  int64 expires_in = 4;
  google.protobuf.Timestamp expires_at = 5;
  repeated string scopes = 6;
}
```

#### Session
```protobuf
message Session {
  string session_id = 1;
  string user_id = 2;
  string tenant_id = 3;
  google.protobuf.Timestamp created_at = 4;
  google.protobuf.Timestamp expires_at = 5;
  string ip_address = 6;
  string user_agent = 7;
  map<string, string> metadata = 8;
}
```

## gRPC Operations

### Authenticate
Authenticate a user with credentials.

**Request**:
```protobuf
message AuthenticateRequest {
  Credentials credentials = 1;
  string device_id = 2;
  string ip_address = 3;
  string user_agent = 4;
}
```

**Response**:
```protobuf
message AuthenticateResponse {
  TokenResponse token = 1;
  Session session = 2;
  string user_id = 3;
}
```

**Example**:
```go
resp, err := authClient.Authenticate(ctx, &authv1.AuthenticateRequest{
    Credentials: &authv1.Credentials{
        Email:    "user@example.com",
        Password: "securepassword",
        TenantId: "tenant_123",
    },
    IpAddress: "192.168.1.1",
    UserAgent: "Mozilla/5.0...",
})
```

### RefreshToken
Refresh an access token using a refresh token.

**Request**:
```protobuf
message RefreshTokenRequest {
  string refresh_token = 1;
  string tenant_id = 2;
}
```

### ValidateToken
Validate an access token.

**Request**:
```protobuf
message ValidateTokenRequest {
  string access_token = 1;
  string tenant_id = 2;
}
```

**Response**:
```protobuf
message ValidateTokenResponse {
  bool valid = 1;
  string user_id = 2;
  string tenant_id = 3;
  repeated string scopes = 4;
  google.protobuf.Timestamp expires_at = 5;
}
```

### Logout
Logout and invalidate a session.

**Request**:
```protobuf
message LogoutRequest {
  string session_id = 1;
  string tenant_id = 2;
}
```

### RequestPasswordReset
Initiate a password reset flow.

**Request**:
```protobuf
message RequestPasswordResetRequest {
  string email = 1;
  string tenant_id = 2;
}
```

### ConfirmPasswordReset
Complete a password reset with the reset token.

**Request**:
```protobuf
message ConfirmPasswordResetRequest {
  string reset_token = 1;
  string new_password = 2;
}
```

## Domain Events

### UserAuthenticatedEvent
```protobuf
message UserAuthenticatedEvent {
  string user_id = 1;
  string tenant_id = 2;
  string session_id = 3;
  google.protobuf.Timestamp authenticated_at = 4;
  string ip_address = 5;
  string user_agent = 6;
}
```

### UserLoggedOutEvent
```protobuf
message UserLoggedOutEvent {
  string user_id = 1;
  string tenant_id = 2;
  string session_id = 3;
  google.protobuf.Timestamp logged_out_at = 4;
}
```

### PasswordResetRequestedEvent
```protobuf
message PasswordResetRequestedEvent {
  string user_id = 1;
  string tenant_id = 2;
  string email = 3;
  google.protobuf.Timestamp requested_at = 4;
}
```

### AuthenticationFailedEvent
```protobuf
message AuthenticationFailedEvent {
  string email = 1;
  string tenant_id = 2;
  string reason = 3;
  google.protobuf.Timestamp failed_at = 4;
  string ip_address = 5;
}
```

## Security Considerations

### Token Management
- **Access tokens**: Short-lived (15-30 minutes recommended)
- **Refresh tokens**: Long-lived (7-30 days recommended)
- **Token rotation**: Refresh tokens should be rotated on use
- **Token storage**: Store refresh tokens securely (encrypted in database)

### Password Security
- Hash passwords with bcrypt (cost factor 10-12)
- Enforce password complexity requirements
- Implement rate limiting on authentication attempts
- Track failed login attempts per user/IP

### Session Security
- Use secure, random session IDs
- Store session metadata (IP, user agent) for anomaly detection
- Implement session timeout
- Allow users to view and revoke active sessions

### Rate Limiting
Implement rate limiting for:
- Authentication attempts: 5 per minute per IP
- Password reset requests: 3 per hour per email
- Token refresh: 10 per minute per user

## Integration Patterns

### API Gateway Integration

```go
// Middleware to validate tokens
func AuthMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        token := extractToken(r)
        
        resp, err := authClient.ValidateToken(ctx, &authv1.ValidateTokenRequest{
            AccessToken: token,
            TenantId:    extractTenantId(r),
        })
        
        if err != nil || !resp.Valid {
            http.Error(w, "Unauthorized", http.StatusUnauthorized)
            return
        }
        
        // Add user context to request
        ctx := context.WithValue(r.Context(), "user_id", resp.UserId)
        ctx = context.WithValue(ctx, "tenant_id", resp.TenantId)
        
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}
```

### Event-Driven Integration

Subscribe to auth events for:
- **UserAuthenticatedEvent**: Update last login timestamp, send notification
- **AuthenticationFailedEvent**: Detect brute force attacks, trigger alerts
- **PasswordResetRequestedEvent**: Send password reset email
- **TokenRefreshedEvent**: Audit token usage

## Best Practices

1. **Always validate tenant_id**: Ensure the authenticated user belongs to the requested tenant
2. **Use HTTPS**: Never transmit tokens over unencrypted connections
3. **Implement CSRF protection**: Use CSRF tokens for web applications
4. **Store tokens securely**: Use secure storage (httpOnly cookies, secure storage APIs)
5. **Validate token expiration**: Check both server-side and client-side
6. **Implement logout everywhere**: Allow users to logout from all sessions
7. **Audit authentication events**: Log all authentication attempts and outcomes
8. **Use MFA**: Support multi-factor authentication for enhanced security

## Error Handling

Common error scenarios:
- Invalid credentials: `UNAUTHENTICATED`
- Expired token: `UNAUTHENTICATED`
- Invalid tenant: `PERMISSION_DENIED`
- Account suspended: `PERMISSION_DENIED`
- Rate limit exceeded: `RESOURCE_EXHAUSTED`

## Monitoring

Key metrics to track:
- Authentication success/failure rates
- Token refresh rates
- Session durations
- Password reset requests
- Failed login attempts by IP
- Concurrent sessions per user

## Dependencies

- Core domain for TenantContext
- Users domain for user information

## Related Domains

- **Users**: User profile and management
- **Access Policy**: Authorization and permissions
- **Notifications**: Send authentication-related notifications
