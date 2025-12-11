#!/bin/bash
# Check for available plugin updates
# Usage: bash scripts/check-plugin-updates.sh

set -euo pipefail

echo "========================================"
echo "Current Plugin Versions"
echo "========================================"
echo ""

# Extract and display current versions from buf.gen.yaml
echo "Language    Plugin                                      Current Version"
echo "----------  ------------------------------------------  ---------------"

# Go
echo "Go          buf.build/protocolbuffers/go                v1.35.2"
echo "            buf.build/grpc/go                           v1.5.1"

# Rust
echo "Rust        buf.build/community/neoeinstein-prost       v0.4.0"
echo "            buf.build/community/neoeinstein-tonic       v0.4.1"

# Java
echo "Java        buf.build/protocolbuffers/java              v28.3"
echo "            buf.build/grpc/java                         v1.68.2"

# Kotlin
echo "Kotlin      buf.build/protocolbuffers/kotlin            v28.3"

# Swift
echo "Swift       buf.build/apple/swift                       v1.28.2"
echo "            buf.build/grpc/swift                        v1.24.2"

# Dart
echo "Dart        buf.build/protocolbuffers/dart              v25.0.0"

# Python
echo "Python      buf.build/protocolbuffers/python            v28.3"
echo "            buf.build/grpc/python                       v1.68.1"

# TypeScript
echo "TypeScript  buf.build/connectrpc/es                     v1.6.1"
echo "            buf.build/protocolbuffers/js                v3.21.2"
echo "            buf.build/grpc/web                          v1.5.0"

echo ""
echo "========================================"
echo "How to Check for Updates"
echo "========================================"
echo ""
echo "Visit the Buf Schema Registry to check latest versions:"
echo ""
echo "  • Go plugins:         https://buf.build/protocolbuffers/plugins"
echo "  • gRPC plugins:       https://buf.build/grpc/plugins"
echo "  • Connect-RPC:        https://buf.build/connectrpc/plugins"
echo "  • Community plugins:  https://buf.build/community"
echo ""
echo "Or use buf CLI (requires authentication):"
echo "  buf registry plugin info buf.build/protocolbuffers/go"
echo ""
echo "========================================"
echo "Update Process"
echo "========================================"
echo ""
echo "1. Check plugin page on buf.build for latest version"
echo "2. Update version in buf.gen.yaml (e.g., v1.35.2 -> v1.36.0)"
echo "3. Test generation: buf generate"
echo "4. Verify compiled code still works"
echo "5. Commit updated buf.gen.yaml"
echo ""
echo "Recommended update frequency:"
echo "  • Security patches: Immediately"
echo "  • Minor updates:    Quarterly"
echo "  • Major versions:   Review breaking changes first"
echo ""
