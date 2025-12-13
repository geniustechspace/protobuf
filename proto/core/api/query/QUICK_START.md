# Query System - Quick Start

## What You Get

A complete, storage-agnostic query system **more powerful than GraphQL**:

✅ **25+ filter operators** (GraphQL has ~10)  
✅ **17+ aggregation functions** (COUNT, SUM, AVG, PERCENTILE, etc.)  
✅ **6 search modes** (natural, fuzzy, semantic, boolean, phrase, wildcard)  
✅ **Geospatial queries** built-in  
✅ **Works with any storage** (SQL, NoSQL, document, cache, graph)  
✅ **Type-safe** with compile-time validation  
✅ **Multi-language** code generation (Go, Python, Java, TypeScript, C#)

## Files Created

```
proto/core/api/query/v1/
├── filter.proto      # 25+ operators, composable AND/OR/NOT
├── sort.proto        # Multi-field sorting
├── projection.proto  # Field selection
├── aggregation.proto # 17+ analytics functions
├── search.proto      # Full-text & semantic search
├── relation.proto    # Joins & relation loading
├── query.proto       # Main unified interface ⭐
├── enums.proto       # Query types & complexity
└── examples.proto    # 50+ usage examples

Documentation:
├── README.md         # Full documentation
└── COMPLETE_GUIDE.md # Storage implementations
```

## Simple Example

```protobuf
import "core/api/query/v1/query.proto";

// Simple filter
Query {
  filter: {
    field: "status",
    op: EQ,
    value: {string: "active"}
  }
}
```

## Complex Example

```protobuf
// E-commerce product search
Query {
  search: {
    query: "wireless headphones",
    fields: ["name", "description"],
    options: {mode: FUZZY, fuzziness: 1}
  },
  filter: {and: [
    {field: "price", op: BETWEEN, value: {string: "50,200"}},
    {field: "in_stock", op: EQ, value: {string: "true"}},
    {field: "rating", op: GTE, value: {string: "4.0"}}
  ]},
  sort: {sorts: [
    {field: "popularity", direction: DESC}
  ]},
  projection: {
    mode: INCLUDE,
    fields: ["id", "name", "price", "rating"]
  },
  pagination: {page_size: 20}
}
```

## Integration with Request Package

The request package now uses Query:

```protobuf
// Before (old Filter)
message ListRequest {
  Filter filter = 1;  // Limited to 13 operators
  string order_by = 2;
  PaginationRequest pagination = 3;
}

// After (comprehensive Query)
message ListRequest {
  Query query = 1;  // 25+ operators, search, aggregation, etc.
}
```

## Usage in Your Services

```protobuf
// In your domain service
service UserService {
  rpc ListUsers(core.api.request.v1.ListRequest) returns (ListUsersResponse);
  rpc SearchUsers(core.api.request.v1.SearchRequest) returns (SearchUsersResponse);
}

// Client builds query
ListRequest {
  query: {
    filter: {and: [
      {field: "tenant_id", op: EQ, value: {string: "tenant_123"}},
      {field: "status", op: IN, value: {string: "active,pending"}},
      {field: "deleted_at", op: IS_NULL}
    ]},
    sort: {sorts: [{field: "created_at", direction: DESC}]},
    pagination: {page_size: 50}
  }
}
```

## All 25+ Operators

**Equality:** EQ, NE  
**Comparison:** GT, GTE, LT, LTE  
**Collection:** IN, NOT_IN, BETWEEN  
**String:** CONTAINS, NOT_CONTAINS, STARTS_WITH, ENDS_WITH, MATCHES, ILIKE  
**Null:** IS_NULL, IS_NOT_NULL  
**Array:** ARRAY_CONTAINS, ARRAY_CONTAINS_ANY, ARRAY_CONTAINS_ALL  
**Geo:** GEO_NEAR, GEO_WITHIN, GEO_INTERSECTS  
**Search:** TEXT_SEARCH  
**Existence:** EXISTS

## Storage Support

Works with any storage system:

- **SQL**: PostgreSQL, MySQL, SQLite
- **NoSQL**: MongoDB, DynamoDB, Cassandra
- **Document**: Elasticsearch, Solr
- **Cache**: Redis, Memcached
- **Graph**: Neo4j
- **Time-series**: InfluxDB, TimescaleDB

Your server-side code converts Query to storage-specific queries.

## Why Better Than GraphQL?

| Feature | GraphQL | Query System |
|---------|---------|--------------|
| Operators | ~10 | 25+ |
| Aggregations | Need extensions | ✅ Built-in (17+) |
| Full-text search | Need extensions | ✅ Built-in (6 modes) |
| Geospatial | Need extensions | ✅ Built-in |
| Type safety | Runtime | ✅ Compile-time |
| Storage support | GraphQL servers | ✅ Any storage |
| Multi-language | JS/TS focus | ✅ 5+ languages |

## Next Steps

1. **See examples**: [examples.proto](v1/examples.proto) - 50+ patterns
2. **Read guide**: [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md) - Storage implementations
3. **Use in services**: Import `core/api/query/v1/query.proto`
4. **Server-side**: Convert Query to your storage's query language

## Code Generation

```bash
# Already generated for you!
buf generate --path proto/core/api/query/

# Output in:
gen/
├── go/core/api/query/v1/
├── python/core/api/query/v1/
├── java/com/geniustechspace/protobuf/core/api/query/v1/
├── typescript/core/api/query/v1/
└── csharp/Core/Api/Query/V1/
```

## Support

- Examples: [examples.proto](v1/examples.proto)
- Full docs: [README.md](README.md)
- Implementation guide: [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)
- All protos in: [v1/](v1/)
