# Core Circuit Breaker

Enterprise circuit breaker for cascading failure prevention.

## Package

```protobuf
package geniustechspace.core.api.circuit_breaker.v1;
```

## Files

- **circuit_breaker_enums.proto**: Circuit breaker state enum
  - `CircuitBreakerState`: CLOSED, OPEN, HALF_OPEN
- **circuit_breaker_messages.proto**: Configuration and status
  - `CircuitBreakerConfig`: Threshold configuration
  - `CircuitBreaker`: Current state and metrics

## Usage

### Define Configuration

```yaml
failure_threshold_percentage: 50
minimum_request_threshold: 10
rolling_window_ms: 10000
open_timeout: "30s"
half_open_request_count: 3
success_threshold: 2
slow_call_threshold_ms: 5000
slow_call_percentage: 80
```

### Monitor Status

```yaml
id: "payment-service-api"
state: OPEN
total_requests: 100
failed_requests: 55
failure_rate: 55.0
last_state_changed_at: "2025-11-16T10:30:00Z"
next_half_open_attempt_at: "2025-11-16T10:30:30Z"
open_count: 3
```

## State Transitions

CLOSED → OPEN       (failure_rate > threshold)
OPEN → HALF_OPEN    (after open_timeout)
HALF_OPEN → CLOSED  (success_threshold successes)
HALF_OPEN → OPEN    (any failure)

## Patterns

- **Martin Fowler**: Classic circuit breaker pattern
- **Envoy**: Outlier detection, failure percentage
- **Hystrix**: Rolling window, slow call detection
- **Resilience4j**: Configurable thresholds, metrics

## Compliance

- SOC 2 CC9.1 (Risk Management)

## Integration

Circuit breakers can be referenced in retry policies:

```proto
// In retry.messages.proto (if cross-package integration needed)
import "proto/datastructure/v1/circuit_breaker/circuit_breaker_messages.proto";
```
