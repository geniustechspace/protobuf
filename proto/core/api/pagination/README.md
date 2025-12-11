# Core Pagination

Hybrid pagination with cursor-based optimization and bidirectional navigation.

**Standards Compliance:** Industry-standard cursor pagination (MongoDB, GraphQL Relay, Stripe, Elasticsearch)

**Design Philosophy:** Single responsibility - pagination only, sorting and filtering handled separately

**Performance Strategy:** O(log n) with client-side cursor caching, graceful O(n) fallback

## Package

```protobuf
package geniustechspace.core.api.pagination.v1;
```

## Messages

- **PaginationRequest**: Parameters for paginated queries (input)
- **PaginationResponse**: Metadata about paginated result sets (output)

## Single Responsibility

This module **only** handles pagination. Related concerns are separated:

- **Sorting**: Add `string order_by` field directly to your List request message
- **Filtering**: Add `string filter` field directly to your List request message
- **Pagination**: Use `PaginationRequest` and `PaginationResponse`

## How It Works

### Intelligent Cursor Caching

**The system automatically optimizes based on what the client provides:**

1. **No cursor** → Server uses offset (acceptable for first load/jumps)
2. **Cursor provided** → Server uses keyset pagination (O(log n) - fast!)
3. **Server always returns cursor** → Client caches for next navigation

### Navigation Flow

```text
Page 1 (no cursor)     → Server: OFFSET, returns cursor₁
  ↓ cache cursor₁
Page 2 (cursor₁)       → Server: KEYSET (fast!), returns cursor₂
  ↓ cache cursor₂  
Page 3 (cursor₂)       → Server: KEYSET (fast!), returns cursor₃
  ← back to Page 2     → Client uses cached cursor₂ → KEYSET (fast!)
  → jump to Page 5     → No cached cursor → OFFSET (once), cache cursor₅
```

**Result:** Sequential navigation is always fast, random jumps acceptable

## Field Reference

### PaginationRequest

- `page_size`: Items per page (0 = default 20, max 1000)
- `page`: Page number (1-indexed), works with or without cursor
- `cursor`: Map of field→value from last item (e.g., `{"created_at": "...", "id": "..."}`)

### PaginationResponse

- `total_size`: Total items across all pages (optional, may be estimate)
- `current_page`: Current page number being returned
- `page_size`: Actual items in current page
- `cursor`: Position after current page for next request (client should cache)

## Example Usage

### Basic List Request

```proto
import "core/api/pagination/v1/messages.proto";

message ListUsersRequest {
  string tenant_id = 1;
  core.api.pagination.v1.PaginationRequest pagination = 2;
  string order_by = 3;  // Sorting (separate concern)
  string filter = 4;    // Filtering (separate concern)
}

message ListUsersResponse {
  repeated User users = 1;
  core.api.pagination.v1.PaginationResponse pagination = 2;
}
```

### Example 1: Basic Pagination (First Load)

```go
// Page 1 - no cursor yet
req := &ListUsersRequest{
  TenantId: "tenant-123",
  Pagination: &PaginationRequest{
    Page: 1,
    PageSize: 20,
  },
  OrderBy: "created_at desc, id desc",
}

resp := client.ListUsers(ctx, req)

// Response includes cursor for next page
// Client should cache: cursors[2] = resp.Pagination.Cursor

// Display: "Page 1 of 78"
totalPages := (resp.Pagination.TotalSize + 19) / 20
```

### Example 2: Navigate Forward (With Cursor)

```go
// Page 2 - using cached cursor
req := &ListUsersRequest{
  TenantId: "tenant-123",
  Pagination: &PaginationRequest{
    Page: 2,
    PageSize: 20,
    Cursor: cursors[2],  // Cursor from page 1 response
  },
  OrderBy: "created_at desc, id desc",
}

resp := client.ListUsers(ctx, req)
// Server uses KEYSET pagination (fast!)
// Cache: cursors[3] = resp.Pagination.Cursor
```

### Example 3: Navigate Backward (Cached Cursor)

```go
// Back to page 1 - using cached cursor
req := &ListUsersRequest{
  TenantId: "tenant-123",
  Pagination: &PaginationRequest{
    Page: 1,
    PageSize: 20,
    // No cursor = page 1
  },
  OrderBy: "created_at desc, id desc",
}

resp := client.ListUsers(ctx, req)
// Fast - same as initial load
```

### Example 4: Client-Side Cursor Cache

```javascript
class PaginationState {
  constructor() {
    this.cursors = new Map();  // page → cursor mapping
    this.currentPage = 1;
    this.pageSize = 20;
  }

  async goToPage(page) {
    const request = {
      tenant_id: "tenant-123",
      pagination: {
        page: page,
        page_size: this.pageSize,
        cursor: this.cursors.get(page) || {}  // Use cached cursor if available
      },
      order_by: "created_at desc, id desc"
    };

    const response = await client.listUsers(request);

    // Cache cursor for next page
    if (response.pagination.cursor) {
      this.cursors.set(page + 1, response.pagination.cursor);
    }

    this.currentPage = page;
    return response;
  }

  // Navigate forward - always uses cursor (fast!)
  async nextPage() {
    return this.goToPage(this.currentPage + 1);
  }

  // Navigate backward - uses cached cursor if available
  async previousPage() {
    return this.goToPage(this.currentPage - 1);
  }

  // Jump to specific page - falls back to offset if not cached
  async jumpToPage(page) {
    return this.goToPage(page);
  }
}
```

### Server Implementation Pattern

```go
func (s *UserService) ListUsers(req *ListUsersRequest) (*ListUsersResponse, error) {
    p := req.Pagination
    
    // Decide mode based on fields
    if p.LastValue != "" || p.LastId != "" {
        // KEYSET MODE
        return s.listUsersKeyset(req)
    } else {
        // OFFSET MODE
        return s.listUsersOffset(req)
    }
}

func (s *UserService) listUsersOffset(req *ListUsersRequest) (*ListUsersResponse, error) {
    page := req.Pagination.Page
    if page == 0 {
        page = 1
    }
    pageSize := req.Pagination.PageSize
    if pageSize == 0 {
        pageSize = 20
    }
    
    offset := (page - 1) * pageSize
    
    users := db.Query("SELECT * FROM users ORDER BY created_at DESC LIMIT ? OFFSET ?", 
                      pageSize, offset)
    total := db.QueryOne("SELECT COUNT(*) FROM users")
    
    return &ListUsersResponse{
        Users: users,
        Pagination: &PaginationResponse{
            TotalSize: total,
        },
    }
}

func (s *UserService) listUsersKeyset(req *ListUsersRequest) (*ListUsersResponse, error) {
    pageSize := req.Pagination.PageSize
    if pageSize == 0 {
        pageSize = 20
    }
    
    query := `
        SELECT * FROM users 
        WHERE (created_at, id) < (?, ?)
        ORDER BY created_at DESC, id DESC 
        LIMIT ?
    `
    
    users := db.Query(query, req.Pagination.LastValue, req.Pagination.LastId, pageSize)
    
    var lastValue, lastId string
    if len(users) > 0 {
        lastItem := users[len(users)-1]
        lastValue = lastItem.CreatedAt.Format(time.RFC3339Nano)
        lastId = lastItem.Id
    }
    
    return &ListUsersResponse{
        Users: users,
        Pagination: &PaginationResponse{
            LastValue: lastValue,
            LastId:    lastId,
            // TotalSize omitted in keyset mode
        },
    }
}
```

## Performance Comparison

| Dataset Size | Mode | Page 1 | Page 100 | Page 1000 |
|--------------|------|--------|----------|-----------|
| **100K records** | Offset | 5ms | 150ms | 2.5s |
| **100K records** | Keyset | 5ms | 8ms | 10ms |
| **1M records** | Offset | 10ms | 1.5s | 45s ⚠️ |
| **1M records** | Keyset | 10ms | 12ms | 15ms ✅ |

## Compliance

- **Google AIP-158**: Standard pagination patterns
- **SOC 2 CC6.3**: Change management and audit trail
- **Single Responsibility**: Pagination separate from sorting/filtering
- Prevents memory exhaustion and timeout issues

## Best Practices

- **Use offset mode** for UI pagination where users expect page numbers
- **Use keyset mode** for data exports, large datasets, or infinite scroll
- **Always index** (sort_field, id) for keyset mode performance
- **Validate** page and page_size on server, apply limits
- **Document** which mode your API endpoints support
