# Request Module

Standardized request metadata for HTTP/gRPC handling across all services.

## Package

**Name**: `geniustechspace.datastructure.v1.request`

**Go**: `github.com/geniustechspace/protobuf/gen/go/datastructure/v1/request;requestv1`
**Java**: `space.geniustech.datastructure.v1.request`
**C#**: `GeniusTechSpace.Datastructure.V1.Request`

## Messages

### RequestMetadata

Complete request context for all services.

**Required Fields:**

- `method` - HTTP method (GET, POST, etc.)
- `protocol` - Communication protocol (HTTP/2, gRPC, etc.)
- `request_id` - Unique request identifier (UUID)
- `trace_id` - Distributed trace ID (W3C traceparent)

**Example:**

```go
metadata := &requestv1.RequestMetadata{
    Method:      requestv1.RequestMethod_POST,
    Protocol:    requestv1.RequestProtocol_HTTP_2,
    RequestId:   uuid.New().String(),
    TraceId:     "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01",
    ContentType: requestv1.ContentType_JSON,
    Priority:    requestv1.RequestPriority_NORMAL,
    Source:      requestv1.RequestSource_WEB_BROWSER,
    UserAgent:   "Mozilla/5.0...",
    Locale:      "en-US",
    CreatedAt:   timestamppb.Now(),
}
```

### RequestContext

Extended context with authentication/authorization.

**Example:**

```go
ctx := &requestv1.RequestContext{
    Metadata:  metadata,
    UserId:    "user-123",
    TenantId:  "acme-corp",
    SessionId: "session-456",
    Roles:     []string{"admin", "user"},
    Permissions: []string{"users:read", "users:write"},
}
```

### RetryInfo

Retry guidance for failed requests.

**Example:**

```go
retryInfo := &requestv1.RetryInfo{
    Retriable:          true,
    RetryType:          requestv1.RetryType_RATE_LIMITED,
    RetryAfterMs:       5000,  // 5 seconds
    MaxRetries:         3,
    BackoffMultiplier:  2.0,
    MaxRetryDelayMs:    60000, // 1 minute
    JitterFactor:       0.1,
}
```

## Enums

### RequestMethod (13 values)

`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`, `TRACE`, `CONNECT`

### RequestStatus (11 values)

`PENDING`, `VALIDATING`, `PROCESSING`, `COMPLETED`, `FAILED`, `CANCELLED`, `TIMEOUT`, `PARTIAL`, `RETRYING`, `QUEUED`

### ContentType (22 values)

`JSON`, `XML`, `CSV`, `PROTOBUF`, `TEXT`, `HTML`, `PDF`, `EXCEL`, `YAML`, `MESSAGEPACK`, `BINARY`, `FORM_DATA`, `FORM_URLENCODED`, `GRAPHQL`, `JSON_LD`, `JPEG`, `PNG`, `GIF`, `SVG`, `MP4`, `MP3`

### RequestPriority (6 values)

`LOW`, `NORMAL`, `HIGH`, `CRITICAL`, `URGENT`

### RequestSource (13 values)

`WEB_BROWSER`, `MOBILE_APP`, `DESKTOP_APP`, `API_CLIENT`, `INTERNAL_SERVICE`, `CLI`, `THIRD_PARTY`, `WEBHOOK`, `SCHEDULED_JOB`, `ADMIN_PANEL`, `TEST`, `DEVELOPMENT`

### RequestProtocol (12 values)
