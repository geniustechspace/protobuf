# Deployment Guide

This guide covers deployment strategies for services using these protobuf schemas.

## Overview

The protobuf schemas are designed to support multiple deployment architectures:
- Kubernetes-based microservices
- Serverless functions (AWS Lambda, Google Cloud Functions)
- Traditional VM-based deployments
- Docker Compose for local development

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (1.24+)
- kubectl CLI
- Helm (optional)
- Container registry access

### Service Deployment

#### 1. Build Docker Image

```dockerfile
# Dockerfile for a gRPC service
FROM golang:1.21 AS builder
WORKDIR /app

# Copy generated protobuf code
COPY gen/go ./gen/go

# Copy service code
COPY . .

# Build
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/service

FROM alpine:latest
RUN apk --no-cache add ca-certificates
COPY --from=builder /app/service /service

EXPOSE 9090
CMD ["/service"]
```

#### 2. Kubernetes Manifests

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
  labels:
    app: user-service
    domain: users
spec:
  replicas: 3
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
        domain: users
    spec:
      containers:
      - name: user-service
        image: ghcr.io/geniustechspace/user-service:v1.0.0
        ports:
        - containerPort: 9090
          name: grpc
        - containerPort: 9091
          name: metrics
        env:
        - name: GRPC_PORT
          value: "9090"
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: host
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: password
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          grpc:
            port: 9090
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          grpc:
            port: 9090
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: user-service
  labels:
    app: user-service
spec:
  selector:
    app: user-service
  ports:
  - port: 9090
    targetPort: 9090
    name: grpc
  - port: 9091
    targetPort: 9091
    name: metrics
  type: ClusterIP
```

#### 3. ConfigMap for Environment

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: service-config
data:
  ENVIRONMENT: "production"
  LOG_LEVEL: "info"
  TENANT_ISOLATION_LEVEL: "database"
  ENABLE_TRACING: "true"
  JAEGER_ENDPOINT: "http://jaeger-collector:14268/api/traces"
```

#### 4. Deploy

```bash
kubectl apply -f configmap.yaml
kubectl apply -f deployment.yaml

# Verify deployment
kubectl get pods -l app=user-service
kubectl logs -l app=user-service
```

### Service Mesh Integration (Istio)

#### 1. Install Istio

```bash
istioctl install --set profile=production
```

#### 2. Enable Sidecar Injection

```bash
kubectl label namespace default istio-injection=enabled
```

#### 3. Virtual Service

```yaml
# virtualservice.yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: user-service
spec:
  hosts:
  - user-service
  http:
  - match:
    - headers:
        x-api-version:
          exact: v1
    route:
    - destination:
        host: user-service
        subset: v1
  - match:
    - headers:
        x-api-version:
          exact: v2
    route:
    - destination:
        host: user-service
        subset: v2
  - route:
    - destination:
        host: user-service
        subset: v1
      weight: 90
    - destination:
        host: user-service
        subset: v2
      weight: 10
```

#### 4. Destination Rule

```yaml
# destinationrule.yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: user-service
spec:
  host: user-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 30s
      baseEjectionTime: 30s
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

## Multi-Tenancy Deployment Strategies

### Strategy 1: Namespace per Tenant (High Isolation)

```bash
# Create tenant namespace
kubectl create namespace tenant-acme

# Deploy service for tenant
kubectl apply -f deployment.yaml -n tenant-acme

# Each tenant gets dedicated resources
```

### Strategy 2: Shared Services with Row-Level Security

```yaml
# Single deployment serving all tenants
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
spec:
  replicas: 10
  template:
    spec:
      containers:
      - name: user-service
        env:
        - name: TENANT_ISOLATION
          value: "row-level"
        - name: ENFORCE_TENANT_ID
          value: "true"
```

### Strategy 3: Tenant Routing via API Gateway

```yaml
# api-gateway configmap
apiVersion: v1
kind: ConfigMap
metadata:
  name: tenant-routing
data:
  routes.yaml: |
    tenants:
      acme:
        database: postgres-acme
        namespace: tenant-acme
      globex:
        database: postgres-globex
        namespace: tenant-globex
```

## Monitoring and Observability

### Prometheus Metrics

```yaml
# servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: user-service
spec:
  selector:
    matchLabels:
      app: user-service
  endpoints:
  - port: metrics
    path: /metrics
    interval: 30s
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "User Service Metrics",
    "panels": [
      {
        "title": "Request Rate by Tenant",
        "targets": [
          {
            "expr": "rate(grpc_server_handled_total{service='UserService'}[5m])"
          }
        ]
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(grpc_server_handled_total{grpc_code!='OK'}[5m])"
          }
        ]
      }
    ]
  }
}
```

### Distributed Tracing

```yaml
# jaeger deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jaeger
spec:
  template:
    spec:
      containers:
      - name: jaeger
        image: jaegertracing/all-in-one:latest
        ports:
        - containerPort: 16686
          name: ui
        - containerPort: 14268
          name: collector
```

## Event Bus Deployment

### Kafka

```yaml
# kafka.yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: event-bus
spec:
  kafka:
    replicas: 3
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
    config:
      offsets.topic.replication.factor: 3
      transaction.state.log.replication.factor: 3
      transaction.state.log.min.isr: 2
  zookeeper:
    replicas: 3
```

### NATS

```yaml
# nats.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: nats
spec:
  serviceName: nats
  replicas: 3
  template:
    spec:
      containers:
      - name: nats
        image: nats:latest
        args:
        - "-js"
        - "-sd=/data"
        ports:
        - containerPort: 4222
          name: client
        - containerPort: 6222
          name: cluster
        - containerPort: 8222
          name: monitor
```

## Database Deployment

### PostgreSQL per Tenant

```yaml
# postgres-tenant.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres-tenant-acme
spec:
  serviceName: postgres-tenant-acme
  replicas: 1
  template:
    spec:
      containers:
      - name: postgres
        image: postgres:15
        env:
        - name: POSTGRES_DB
          value: tenant_acme
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: postgres-credentials-acme
              key: username
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-credentials-acme
              key: password
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 20Gi
```

## Auto-Scaling

### Horizontal Pod Autoscaler

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: user-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: user-service
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: grpc_server_handled_total
      target:
        type: AverageValue
        averageValue: "1000"
```

### Vertical Pod Autoscaler

```yaml
# vpa.yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: user-service-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: user-service
  updatePolicy:
    updateMode: "Auto"
```

## CI/CD Pipeline

### GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Deploy Services

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate Protobuf Code
        run: buf generate
      
      - name: Build Docker Image
        run: |
          docker build -t ghcr.io/geniustechspace/user-service:${{ github.sha }} .
          docker push ghcr.io/geniustechspace/user-service:${{ github.sha }}
      
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/user-service \
            user-service=ghcr.io/geniustechspace/user-service:${{ github.sha }}
          kubectl rollout status deployment/user-service
```

## Disaster Recovery

### Backup Strategy

```yaml
# velero backup
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: daily-backup
spec:
  schedule: "0 2 * * *"
  template:
    includedNamespaces:
    - default
    - tenant-*
    storageLocation: default
```

### Multi-Region Deployment

```yaml
# Deploy to multiple regions
regions:
  - us-east-1
  - eu-west-1
  - ap-southeast-1

# Each region gets full stack
# Route traffic based on geography
```

## Security Best Practices

1. **TLS Everywhere**: Use mutual TLS between services
2. **Secrets Management**: Use HashiCorp Vault or AWS Secrets Manager
3. **Network Policies**: Restrict pod-to-pod communication
4. **RBAC**: Implement strict role-based access control
5. **Pod Security**: Use Pod Security Standards
6. **Image Scanning**: Scan container images for vulnerabilities

```yaml
# networkpolicy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: user-service-policy
spec:
  podSelector:
    matchLabels:
      app: user-service
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: api-gateway
    ports:
    - protocol: TCP
      port: 9090
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
```

## Cost Optimization

1. **Right-sizing**: Use VPA to optimize resource requests
2. **Spot Instances**: Use spot/preemptible nodes for non-critical workloads
3. **Resource Limits**: Set appropriate limits to prevent over-provisioning
4. **Cluster Autoscaler**: Scale nodes based on demand
5. **Reserved Capacity**: Use reserved instances for baseline load

## Troubleshooting

### Common Issues

**Connection Refused**
```bash
kubectl port-forward svc/user-service 9090:9090
grpcurl -plaintext localhost:9090 list
```

**High Latency**
```bash
# Check metrics
kubectl top pods -l app=user-service

# Check logs
kubectl logs -l app=user-service --tail=100
```

**Failed Health Checks**
```bash
# Check readiness
kubectl describe pod <pod-name>

# Test health endpoint
kubectl exec <pod-name> -- grpc-health-probe -addr=:9090
```

## Support

For deployment assistance:
- Email: devops@geniustechspace.com
- Slack: #deployment-help
- Documentation: https://docs.geniustechspace.com
