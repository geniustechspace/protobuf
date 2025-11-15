# Client Generation Guide

This guide explains how to generate and use client libraries from the protobuf definitions.

## Overview

The repository supports generating client libraries for multiple languages:
- Go
- Python
- Java
- TypeScript/JavaScript
- C#

Each domain can be generated independently, allowing teams to only include the domains they need.

## Prerequisites

- [Buf CLI](https://buf.build/docs/installation) >= 1.47.0
- Language-specific tools (depending on your target language)

## Generating All Clients

To generate clients for all domains and all languages:

```bash
buf generate
```

This creates the following structure:

```
gen/
├── go/
│   ├── core/
│   ├── auth/
│   ├── users/
│   ├── access-policy/
│   ├── tenants/
│   ├── billing/
│   └── notifications/
├── python/
├── java/
├── typescript/
└── csharp/
```

## Generating Domain-Specific Clients

Generate clients for a specific domain:

```bash
# Generate only users domain
buf generate --path proto/users/v1/

# Generate only auth domain
buf generate --path proto/auth/v1/

# Generate specific version
buf generate --path proto/users/v2/
```

## Language-Specific Setup

### Go

#### Installation

```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

#### Usage

```go
package main

import (
    "context"
    "log"
    
    "google.golang.org/grpc"
    "google.golang.org/grpc/metadata"
    
    usersv1 "github.com/geniustechspace/protobuf/gen/go/users/v1"
)

func main() {
    // Connect to the service
    conn, err := grpc.Dial("localhost:9090", grpc.WithInsecure())
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()
    
    // Create client
    client := usersv1.NewUserServiceClient(conn)
    
    // Add tenant context to metadata
    ctx := metadata.AppendToOutgoingContext(
        context.Background(),
        "x-tenant-id", "tenant_123",
        "authorization", "Bearer <token>",
    )
    
    // Make request
    req := &usersv1.CreateUserRequest{
        TenantId:  "tenant_123",
        Email:     "user@example.com",
        Username:  "johndoe",
        Password:  "securepass",
        FirstName: "John",
        LastName:  "Doe",
    }
    
    resp, err := client.CreateUser(ctx, req)
    if err != nil {
        log.Fatal(err)
    }
    
    log.Printf("Created user: %s", resp.User.Metadata.Id)
}
```

#### Module Setup

Create a `go.mod` file:

```go
module myapp

go 1.21

require (
    github.com/geniustechspace/protobuf/gen/go v0.1.0
    google.golang.org/grpc v1.59.0
    google.golang.org/protobuf v1.31.0
)
```

### Python

#### Installation

```bash
pip install grpcio grpcio-tools
```

#### Usage

```python
import grpc
from gen.python.users.v1 import users_pb2, users_pb2_grpc

def main():
    # Connect to the service
    channel = grpc.insecure_channel('localhost:9090')
    client = users_pb2_grpc.UserServiceStub(channel)
    
    # Create metadata with tenant context
    metadata = (
        ('x-tenant-id', 'tenant_123'),
        ('authorization', 'Bearer <token>'),
    )
    
    # Make request
    request = users_pb2.CreateUserRequest(
        tenant_id='tenant_123',
        email='user@example.com',
        username='johndoe',
        password='securepass',
        first_name='John',
        last_name='Doe'
    )
    
    response = client.CreateUser(request, metadata=metadata)
    print(f"Created user: {response.user.metadata.id}")

if __name__ == '__main__':
    main()
```

#### Package Setup

Create a `setup.py`:

```python
from setuptools import setup, find_packages

setup(
    name='myapp',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'grpcio>=1.59.0',
        'grpcio-tools>=1.59.0',
        'protobuf>=4.24.0',
    ],
)
```

### Java

#### Installation

Add to `pom.xml`:

```xml
<dependencies>
    <dependency>
        <groupId>io.grpc</groupId>
        <artifactId>grpc-netty-shaded</artifactId>
        <version>1.59.0</version>
    </dependency>
    <dependency>
        <groupId>io.grpc</groupId>
        <artifactId>grpc-protobuf</artifactId>
        <version>1.59.0</version>
    </dependency>
    <dependency>
        <groupId>io.grpc</groupId>
        <artifactId>grpc-stub</artifactId>
        <version>1.59.0</version>
    </dependency>
</dependencies>
```

#### Usage

```java
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.Metadata;
import io.grpc.stub.MetadataUtils;

import com.geniustechspace.protobuf.users.v1.UsersProto.*;
import com.geniustechspace.protobuf.users.v1.UserServiceGrpc;

public class UserClient {
    public static void main(String[] args) {
        // Create channel
        ManagedChannel channel = ManagedChannelBuilder
            .forAddress("localhost", 9090)
            .usePlaintext()
            .build();
        
        // Create client with metadata
        Metadata metadata = new Metadata();
        metadata.put(
            Metadata.Key.of("x-tenant-id", Metadata.ASCII_STRING_MARSHALLER),
            "tenant_123"
        );
        metadata.put(
            Metadata.Key.of("authorization", Metadata.ASCII_STRING_MARSHALLER),
            "Bearer <token>"
        );
        
        UserServiceGrpc.UserServiceBlockingStub client = 
            UserServiceGrpc.newBlockingStub(channel);
        client = MetadataUtils.attachHeaders(client, metadata);
        
        // Make request
        CreateUserRequest request = CreateUserRequest.newBuilder()
            .setTenantId("tenant_123")
            .setEmail("user@example.com")
            .setUsername("johndoe")
            .setPassword("securepass")
            .setFirstName("John")
            .setLastName("Doe")
            .build();
        
        CreateUserResponse response = client.createUser(request);
        System.out.println("Created user: " + response.getUser().getMetadata().getId());
        
        channel.shutdown();
    }
}
```

### TypeScript

#### Installation

```bash
npm install @connectrpc/connect @connectrpc/connect-node
```

#### Usage

```typescript
import { createPromiseClient } from "@connectrpc/connect";
import { createGrpcTransport } from "@connectrpc/connect-node";
import { UserService } from "./gen/typescript/users/v1/users_connect";
import { CreateUserRequest } from "./gen/typescript/users/v1/users_pb";

async function main() {
  // Create transport
  const transport = createGrpcTransport({
    baseUrl: "http://localhost:9090",
    httpVersion: "2",
  });

  // Create client
  const client = createPromiseClient(UserService, transport);

  // Make request with headers
  const request = new CreateUserRequest({
    tenantId: "tenant_123",
    email: "user@example.com",
    username: "johndoe",
    password: "securepass",
    firstName: "John",
    lastName: "Doe",
  });

  const response = await client.createUser(request, {
    headers: {
      "x-tenant-id": "tenant_123",
      "authorization": "Bearer <token>",
    },
  });

  console.log(`Created user: ${response.user?.metadata?.id}`);
}

main();
```

#### Package Setup

Create `package.json`:

```json
{
  "name": "myapp",
  "version": "0.1.0",
  "dependencies": {
    "@connectrpc/connect": "^1.6.0",
    "@connectrpc/connect-node": "^1.6.0"
  }
}
```

### C#

#### Installation

Add to `.csproj`:

```xml
<ItemGroup>
    <PackageReference Include="Grpc.Net.Client" Version="2.59.0" />
    <PackageReference Include="Google.Protobuf" Version="3.25.0" />
    <PackageReference Include="Grpc.Tools" Version="2.59.0" PrivateAssets="All" />
</ItemGroup>
```

#### Usage

```csharp
using Grpc.Core;
using Grpc.Net.Client;
using GeniusTechSpace.Protobuf.Users.V1;

class Program
{
    static async Task Main(string[] args)
    {
        // Create channel
        var channel = GrpcChannel.ForAddress("http://localhost:9090");
        var client = new UserService.UserServiceClient(channel);
        
        // Create metadata
        var metadata = new Metadata
        {
            { "x-tenant-id", "tenant_123" },
            { "authorization", "Bearer <token>" }
        };
        
        // Make request
        var request = new CreateUserRequest
        {
            TenantId = "tenant_123",
            Email = "user@example.com",
            Username = "johndoe",
            Password = "securepass",
            FirstName = "John",
            LastName = "Doe"
        };
        
        var response = await client.CreateUserAsync(request, metadata);
        Console.WriteLine($"Created user: {response.User.Metadata.Id}");
    }
}
```

## Custom Generation Templates

You can create custom generation templates:

```yaml
# custom-buf.gen.yaml
version: v2
plugins:
  - remote: buf.build/protocolbuffers/go
    out: custom/go
    opt:
      - paths=source_relative
      - module=github.com/myorg/myrepo
```

Use it:

```bash
buf generate --template custom-buf.gen.yaml
```

## CI/CD Integration

### GitHub Actions

The repository includes automated client generation:

```yaml
# Clients are generated on every push to main
# Download from workflow artifacts:
# https://github.com/geniustechspace/protobuf/actions
```

### Publishing Clients

#### npm (TypeScript)

```bash
cd gen/typescript/users/v1
npm init -y
npm publish
```

#### PyPI (Python)

```bash
cd gen/python/users/v1
python setup.py sdist
twine upload dist/*
```

#### Maven (Java)

```bash
cd gen/java
mvn deploy
```

## Troubleshooting

### Import Errors

If you get import errors, ensure:

1. Buf dependencies are installed: `buf dep update`
2. Generated code is up to date: `buf generate`
3. Language-specific tools are installed

### Version Mismatches

Ensure protobuf and gRPC versions match:

```bash
# Check versions
buf --version
protoc --version
grpc_tools_node_protoc --version
```

### Missing Dependencies

Install buf dependencies:

```bash
buf dep update
```

## Best Practices

1. **Version Pinning**: Pin client versions in your dependency files
2. **Separate Repos**: Consider separate repos for each domain's clients
3. **Automated Updates**: Use Dependabot/Renovate to keep clients updated
4. **Error Handling**: Always handle gRPC errors properly
5. **Retry Logic**: Implement exponential backoff for transient failures
6. **Connection Pooling**: Reuse gRPC channels/connections
7. **Metadata**: Always include tenant context in metadata
8. **Timeouts**: Set appropriate request timeouts
9. **TLS**: Use TLS in production environments
10. **Testing**: Write integration tests with generated clients

## Examples Repository

For complete working examples, see:
https://github.com/geniustechspace/protobuf-examples

## Support

For issues with client generation:
1. Check Buf documentation: https://buf.build/docs
2. Open an issue in this repository
3. Join our community Discord
