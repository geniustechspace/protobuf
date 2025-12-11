# Core Retry Policies

Enterprise-grade retry configuration for distributed systems.

## Package

```protobuf
package geniustechspace.core.api.retry.v1;
```

## Files

- **retry_enums.proto**: Retry-related enumerations
  - `RetryCode`: Why retry was triggered
  - `BackoffStrategy`: Delay calculation algorithms
  - `RetryPolicyType`: Policy classifications
  - `RetryOutcome`: Retry attempt results
- **retry_messages.proto**: Retry configuration and metrics
  - `RetryInfo`: Per-request server guidance
  - `RetryStrategy`: Backoff timing configuration
  - `RetryPolicy`: Complete retry policy
  - `RetryMetrics`: Performance metrics

## Usage

### Define a Policy

```yaml
name: "api-default"
policy_type: DEFAULT
retry_strategy:
  backoff_strategy: EXPONENTIAL
  initial_delay_ms: 1000
  max_delay_ms: 30000
  backoff_multiplier: 2.0
  jitter_factor: 0.1
max_attempts: 3
total_timeout_ms: 60000
retryable_retry_codes: [NETWORK_ERROR, REQUEST_TIMEOUT, SERVICE_UNAVAILABLE]
retriable_status_codes: [429, 503, 504]
```

### Server Returns RetryInfo

```yaml
retriable: true
retry_code: RATE_LIMIT
retry_after_ms: 5000
current_attempt: 1
retry_policy: "api-default"
```

## Quota Management

Retry quotas are managed by a separate Quota Service, not embedded in RetryPolicy.
See `proto/quota/v1/retry_quota.proto` (if exists).

## Standards

- **Google Cloud**: Exponential backoff with jitter
- **AWS SDK**: Decorrelated jitter, regional fallback
- **Envoy**: Retry budgets, deadlines

## Compliance

- SOC 2 CC7.2, CC9.1
- PCI DSS 6.5.10
- ISO 27001 A.12.6.1
