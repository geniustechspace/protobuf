# Core Error Handling

Enterprise error handling for distributed systems with comprehensive error categorization.

## Package

```protobuf
package geniustechspace.core.error.v1;
```

## Files

- **error_enums.proto**: Error code enumerations
  - 12 categories: Validation, Authentication, Authorization, Resource, Business, RateLimit, System, Integration, Data, File, Network, Security
  - 100+ specific error codes
- **error_messages.proto**: Error response structures
  - `ErrorDetail`: Field-level error information
  - `ErrorCategory`: Strongly-typed error classification
  - `ErrorResponse`: Complete error response
  - `ErrorSeverity`: Impact levels (INFO, WARNING, ERROR, CRITICAL, FATAL)
  - `RetryInfo`: Retry guidance for transient errors

## Usage

### Return Error Response

```yaml
status: 400
message: "Validation failed"
details:
  - code: "REQUIRED_FIELD"
    message: "Email is required"
    field: "email"
    error_category:
      validation: REQUIRED_FIELD
request_id: "f47ac10b-58cc-4372-a567-0e02b2c3d479"
occurred_at: "2025-11-16T10:30:00Z"
trace_id: "4bf92f3577b34da6a3ce929d0e0e4736"
service: "user-service"
```

### Field-Level Errors

```yaml
details:
  - code: "INVALID_EMAIL"
    message: "Invalid email format"
    field: "user.email"
    metadata:
      pattern: "^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,}$"
```

### Retry Guidance

```yaml
details:
  - code: "RATE_LIMIT_EXCEEDED"
    message: "Too many requests"
    retry_info:
      retriable: true
      retry_after_ms: 60000
      max_retries: 3
      backoff_multiplier: 2.0
```

## HTTP Status Mapping

| Code | Status                | Use Case                 |
| ---- | --------------------- | ------------------------ |
| 400  | Bad Request           | Validation errors        |
| 401  | Unauthorized          | Authentication required  |
| 403  | Forbidden             | Insufficient permissions |
| 404  | Not Found             | Resource doesn't exist   |
| 409  | Conflict              | Duplicate resource       |
| 422  | Unprocessable Entity  | Business logic errors    |
| 429  | Too Many Requests     | Rate limit exceeded      |
| 500  | Internal Server Error | Unexpected server error  |
| 502  | Bad Gateway           | Upstream service error   |
| 503  | Service Unavailable   | Temporary outage         |
| 504  | Gateway Timeout       | Upstream timeout         |

## Security

**NEVER include in errors:**

- ❌ Stack traces
- ❌ Database queries
- ❌ Internal hostnames/IPs
- ❌ Infrastructure IDs
- ❌ PII (personal identifiable information)
- ❌ Secrets/API keys

**ALWAYS include:**

- ✅ `request_id` (for support/debugging)
- ✅ `trace_id` (for distributed tracing)
- ✅ User-friendly messages
- ✅ Actionable error codes
- ✅ Help URLs

## Standards

- **RFC 7807**: Problem Details for HTTP APIs
- **Google Cloud Errors**: AIP-193 error model
- **gRPC Status**: Standard status codes

## Compliance
