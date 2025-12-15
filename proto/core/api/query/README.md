# Core API Query

**Universal, storage-agnostic query system** for all data operations.

```protobuf
package geniustechspace.core.api.query.v1;
```

## Supported Storage

SQL • NoSQL • Document • Cache • Graph • Time-series • Filesystems • Search Engines

PostgreSQL • MySQL • MongoDB • Elasticsearch • Redis • Neo4j • DynamoDB • S3 • and more

## Key Features

- ✅ **25+ Filter Operators** - EQ, IN, BETWEEN, CONTAINS, GEO_NEAR, etc.
- ✅ **Auto-Join Inference** - Relations detected from field paths
- ✅ **PSL Wildcards** - `user.**`, `**.id`, `orders[].items[].sku`
- ✅ **String Values Only** - Simple API: all values are strings
- ✅ **Full-Text Search** - Natural, Fuzzy, Semantic, Phrase modes
- ✅ **Aggregations** - COUNT, SUM, AVG, PERCENTILE_99, and 13+ more
- ✅ **Type-Safe** - Compile-time validation with Protocol Buffers

## Architecture

``` markdown
query/v1/
├── filter.proto      # 25+ operators, composable AND/OR
├── sort.proto        # Multi-field sorting, null handling
├── projection.proto  # DEPRECATED (use Query.include/exclude)
├── aggregation.proto # 17+ aggregate functions
├── search.proto      # 6 search modes
├── relation.proto    # Auto-join inference
└── query.proto       # Main interface ⭐
```

**Philosophy:** Simple by default, powerful when needed.

## Quick Examples

### Simple Filter

```protobuf
Query {
  filter: {field: "status", op: EQ, value: "active"}
}
```

### With Projection

```protobuf
Query {
  filter: {field: "status", op: EQ, value: "active"},
  include: ["id", "name", "email"]
}
```

### Auto-Join Relations

```protobuf
Query {
  filter: {field: "user.status", op: EQ, value: "verified"},
  include: ["id", "title", "user.name", "user.email"]
  // Server auto-detects "user" relation
}
```

### Complex Query

```protobuf
Query {
  filter: {and: [
    {field: "status", op: EQ, value: "active"},
    {field: "price", op: BETWEEN, value: "50,200"}
  ]},
  include: ["id", "name", "price"],
  sorts: [{field: "created_at", direction: DESC}],
  pagination: {page_size: 20}
}
```

## Core Concepts

### 1. Filter - 25+ Operators

**All values are strings** - server converts to appropriate types.

```protobuf
// Single value
{field: "status", op: EQ, value: "active"}

// List (comma-separated)
{field: "role", op: IN, value: "admin,owner,editor"}

// Range
{field: "price", op: BETWEEN, value: "50,200"}

// Geospatial (lat,lng,radius_km)
{field: "location", op: GEO_NEAR, value: "40.7128,-74.0060,10"}
```

**Operators:** EQ, NE, GT, GTE, LT, LTE, IN, NOT_IN, CONTAINS, STARTS_WITH, ENDS_WITH, MATCHES, ILIKE, IS_NULL, IS_NOT_NULL, BETWEEN, ARRAY_CONTAINS, ARRAY_CONTAINS_ANY, ARRAY_CONTAINS_ALL, GEO_NEAR, GEO_WITHIN, TEXT_SEARCH, EXISTS

**Composable:** Unlimited AND/OR nesting.

### 2. Projection - PSL Wildcards

**Projection Selector Language (PSL) v1** - Universal field selection embedded in Query

````protobuf
// Include only specific fields
Query {
  include: ["id", "email", "name"]
}

// Exclude secrets everywhere
Query {
  exclude: ["**.password", "**.token", "**.ssn"]
```protobuf
// Specific fields
include: ["id", "name", "email"]

// Exclude secrets
exclude: ["**.password", "**.token"]

// Wildcards
include: ["user.**"]              // Entire user subtree
include: ["**.id"]                // All IDs recursively
include: ["user.*"]               // Direct children only

// Lists and maps
include: ["orders[].total"]       // List navigation
include: ["metadata[*]"]          // All map keys
include: ["config['timeout']"]    // Specific key
````

**Syntax:** `.` dot notation • `*` single-level • `**` recursive • `[]` lists • `[*]` map keys

See [PSL_SPEC.md](PSL_SPEC.md) for complete reference

// Multiple aggregations
Grouping {
fields: ["category"],
aggregates: [
{function: COUNT, alias: "total"},
{function: SUM, field: "amount", alias: "revenue"},
{function: AVG, field: "rating", alias: "avg_rating"}
]
}

// With HAVING clause
Grouping {
fields: ["status"],
aggregates: [{function: COUNT, alias: "count"}],
having: "count > 10"
}

``` markdown

### 5. Full-Text Search (search.proto)

**Search Modes:**
- NATURAL - Natural language
- BOOLEAN - AND/OR/NOT operators
- PHRASE - Exact phrase match
- WILDCARD - Pattern matching
- FU3. Relations - Auto-Inference
    "comments[].author.name",
    "orders[].items.product.name"
  ]
  // Auto-loads: comments → comments.author, orders → orders.items → items.product
}

// Relations detected from filters too
Query {
  filter: {and: [
    {field: "id", op: EQ, value: "123"},
    {field: "comments.approved", op: EQ, value: "true"}
  ]},
  include: ["id", "comments.content", "comments.author.name"]
  // Server detects "comments" relation from both filter and include
}
```

**Explicit joins (for complex cases):**

```protobuf
Join {
  type: LEFT,
  relation: "users",
  local_field: "user_id",
  foreign_field: "id",
  filter: {field: "status", op: EQ, value: "active"},
  include: ["id", "name", "email"],
  alias: "author"
  // Use explicit Join only when you need custom conditions or aliases
}
```

## Usage Examples

### E-commerce Product Search

```protobuf
Query {
  search: {
    query: "wireless headphones",
    fields: ["name", "description"],
    options: {mode: FUZZY, fuzziness: 1}
  },
  filter: {
    and: [
      {field: "price", op: BETWEEN, values: ["50", "200"]},
      {field: "in_stock", op: EQ, value: "true"},
      {field: "rating", op: GTE, value: "4.0"}
    ]
  },
  sorts: [
    {field: "popularity", direction: DESC},
    {field: "price", direction: ASC}
  ],
  include: ["id", "name", "price", "image_url"],
  pagination: {page_size: 20}
}
```

### Analytics Dashboard

````protobuf
Query {
  filter: {
    field: "created_at",
    op: GTE,
    value: "2024-01-01"
  },
  grouping: {
    fields: ["status", "category"],
    aggregates: [
  No need to specify relations!** Server detects from field paths.

```protobuf
// From include paths
include: ["id", "user.name", "user.email"]
// → Auto-loads "user" relation

// From filter paths
filter: {field: "user.status", op: EQ, value: "verified"}
// → Auto-loads "user" relation

// Nested relations
include: ["user.profile.city", "user.organization.name"]
// → Auto-loads: user → user.profile, user.organization

// List relations
include: ["orders[].items[].product.name"]
// → Auto-loads: orders → orders.items → orders.items.product
````

````markdown
**Explicit Join (rare):** Only for custom conditions or aliases. }

    query += " FROM " + table

    // Auto-detect joins from filter and include paths
    joins := detectJoins(q.Filter, q.Include, schema)
    for _, join := range joins {
        query += fmt.Sprintf(" LEFT JOIN %s ON %s.%s = %s.%s",
            join.Table, table, join.LocalField, join.Table, join.ForeignField)
    }
    query += " FROM " + table

    // Filter → WHERE
    if q.Filter != nil {
        where, args := filterToSQL(q.Filter)
        query += " WHERE " + where
    }

    // Sort → ORDER BY
    if q.Sort != nil {
        query += " ORDER BY " + sortToSQL(q.Sort)
    }

    // Pagination → LIMIT/OFFSET
    if q.Pagination != nil {
        query += fmt.Sprintf(" LIMIT %d OFFSET %d",
            q.Pagination.PageSize, offset)
    }

    return query, args, nil

}

````

### MongoDB

```go
func ToMongo(q *Query) bson.M {
    pipeline := []bson.M{}

    // Filter → $match
    if q.Filter != nil {
        pipeline = append(pipeline, bson.M{"$match": filterToMongo(q.Filter)})
    }

    // Aggregation → $group
    if q.Grouping != nil {
        pipeline = append(pipeline, bson.M{"$group": groupingToMongo(q.Grouping)})
    }

    // Sort → $sort
    if len(q.Sorts) > 0 {
        pipeline = append(pipeline, bson.M{"$sort": sortsToMongo(q.Sorts)})
    }

    // Pagination → $skip + $limit
    if q.Pagination != nil {
        pipeline = append(pipeline,
            bson.M{"$skip": offset},
            bson.M{"$limit": q.Pagination.PageSize})
    }

    return bson.M{"$aggregate": pipeline}
}
````

### Elasticsearch

```go
func ToElasticsearch(q *Query) map[string]interface{} {
    query := map[string]interface{}{}

    // Search → query.match
    if q.Search != nil {
        query["query"] = map[string]interface{}{
            "multi_match": map[string]interface{}{
                "query":  q.Search.Query,
                "fields": q.Search.Fields,
            },
        }
    }

    // Filter → query.bool.filter
    if q.Filter != nil {
        query["query"].(map[string]interface{})["bool"] = map[string]interface{}{
            "filter": filterToES(q.Filter),
        }
    }

    // Sort
    if q.Sort != nil {
        query["sort"] = sortToES(q.Sort)
    }

    // Pagination
    query["from"] = offset
    query["size"] = q.Pagination.PageSize

    return query
}
```

## Best Practices

1. **Start simple** - Use only the fields you need
2. **Leverage indexes** - Ensure filtered/sorted fields are indexed
3. **Limit results** - Always set pagination.page_size
4. **Test explain** - Use explain:true to debug query performance
5. **Storage-specific options** - Use options map for vendor-specific features
6. **Use PSL wildcards** - `user.**` more maintainable than listing all fields
7. **Global secret exclusion** - `exclude: ["**.password", "**.token"]` for security
8. **Pre-compile patterns** - Cache PSL matchers for repeated queries
9. **Auto-join inference** - Use dot notation in filters/includes, relations load automatically
10. **Explicit joins only when needed** - Use Join for custom conditions or aliases

## Related

- [Pagination](../pagination/v1/messages.proto) - Cursor-based pagination
- [Request](../request/v1/messages.proto) - Request wrappers using Query
- [Response](../response/v1/messages.proto) - Response structure
- Use specific projections\*_ - `include: ["id", "name"]` not `_`
  1. **Global secret exclusion** - `exclude: ["**.password", "**.token"]`
  2. **Leverage auto-joins** - Use dot notation, no explicit relations
  3. **Set pagination** - Always limit results
  4. **Index wisely** - Filter, sort, and foreign key fields
  5. **Cache PSL patterns** - Pre-compile for repeated queries
  6. **Use timeouts** - `timeout_ms: 5000`

## Documentation

- **[GUIDE.md](GUIDE.md)** - Complete implementation guide with examples
- **[PSL_SPEC.md](PSL_SPEC.md)** - Projection Selector Language specification
- **[examples.proto](v1/examples.proto)** - Comprehensive query patterns

## Files

```markdown
v1/
├── query.proto       # Main interface ⭐
├── filter.proto      # Operators and logic
├── relation.proto    # Auto-join inference
├── sort.proto        # Sorting
├── search.proto      # Full-text search
├── aggregation.proto # Analytics
└── examples.proto    # Usage examples
```
