#!/usr/bin/env bash
# Documentation Generator for Protobuf Schemas
# Generates markdown documentation from proto files

set -euo pipefail

OUTPUT_DIR="gen/docs"
OUTPUT_FILE="$OUTPUT_DIR/API_DOCUMENTATION.md"

echo "Generating API documentation..."
mkdir -p "$OUTPUT_DIR"

cat > "$OUTPUT_FILE" << 'EOF'
# API Documentation

> Auto-generated from Protocol Buffer definitions

## Table of Contents

EOF

# Function to extract service documentation
generate_service_docs() {
    local proto_file=$1
    local service_name=$(grep -E "^service " "$proto_file" | head -1 | awk '{print $2}')
    
    if [ -n "$service_name" ]; then
        echo "### $service_name" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        
        # Extract service description
        grep -B 10 "^service $service_name" "$proto_file" | grep "^//" | sed 's|^// ||' >> "$OUTPUT_FILE" || true
        echo "" >> "$OUTPUT_FILE"
        
        # Extract RPCs
        echo "**Methods:**" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        grep -A 5 "rpc " "$proto_file" | grep "rpc " | while read -r line; do
            rpc_name=$(echo "$line" | awk '{print $2}' | sed 's/(.*//') 
            request=$(echo "$line" | grep -o "([^)]*)" | head -1 | tr -d '()')
            response=$(echo "$line" | grep -o "returns ([^)]*)" | sed 's/returns (//' | tr -d ')')
            echo "- \`$rpc_name($request)\` → \`$response\`" >> "$OUTPUT_FILE"
        done
        echo "" >> "$OUTPUT_FILE"
    fi
}

# Find all service proto files
echo "Scanning proto files..."
find proto -name "service*.proto" -o -name "*_api.proto" | sort | while read -r file; do
    echo "Processing: $file"
    generate_service_docs "$file"
done

# Add domain documentation
cat >> "$OUTPUT_FILE" << 'EOF'

## Domains

### Identity Provider (IDP)
Identity and access management services including authentication, authorization, and user management.

**Packages:**
- `geniustechspace.idp.api.v1` - Main API services
- `geniustechspace.idp.authn.*` - Authentication (credentials, MFA, sessions)
- `geniustechspace.idp.authz.*` - Authorization (permissions, policies, roles)
- `geniustechspace.idp.identity.*` - Identity management (users, groups, organizations)

### Core
Shared types and utilities used across all domains.

**Packages:**
- `geniustechspace.core.api.*` - API patterns (pagination, errors, retry)
- `geniustechspace.core.common.v1` - Common types (address, contact)
- `geniustechspace.core.token.v1` - Token management (JWT)
- `geniustechspace.core.session.v1` - Session types
- `geniustechspace.core.network.v1` - Network context
- `geniustechspace.core.device.v1` - Device detection
- `geniustechspace.core.geo.v1` - Geolocation

### Contact
Contact information management.

**Packages:**
- `geniustechspace.contact.address.v1` - Address handling
- `geniustechspace.contact.phone.v1` - Phone number validation

### Human Capital Management (HCM)
Employee and workforce management.

**Packages:**
- `geniustechspace.hcm.employee.v1` - Employee records

### Preferences
User preference management.

**Packages:**
- `geniustechspace.preference.user.v1` - User preferences

## Generated Code

Generated client libraries are available in:

- **Go**: `gen/go/`
- **Rust**: `gen/rust/`
- **Java**: `gen/java/`
- **Kotlin**: `gen/kotlin/`
- **Swift**: `gen/swift/`
- **Dart**: `gen/dart/`
- **Python**: `gen/python/`
- **TypeScript**: `gen/typescript/`
  - Connect-RPC: `gen/typescript/connect/`
  - gRPC-Web: `gen/typescript/grpc-web/`
  - Protocol Buffers JS: `gen/typescript/js/`

## Validation Rules

All messages use `buf.validate` for runtime validation:

- String constraints: `min_len`, `max_len`, `pattern`, `email`, `uuid`, `uri`
- Numeric constraints: `gte`, `lte`, `gt`, `lt`
- Repeated constraints: `min_items`, `max_items`, `unique`
- Enum constraints: `defined_only`

See individual message definitions for specific validation rules.

## Compliance

This API follows compliance standards:
- **SOC 2** CC6.1, CC6.2, CC6.3
- **GDPR** Articles 4, 5, 9, 17, 30
- **ISO 27001** A.9.1, A.9.2, A.9.4
- **NIST 800-63B** Digital Identity Guidelines

---

*Generated on: $(date)*
*Buf version: $(buf --version)*
EOF

echo "✓ Documentation generated: $OUTPUT_FILE"
echo ""
echo "Preview:"
head -30 "$OUTPUT_FILE"
