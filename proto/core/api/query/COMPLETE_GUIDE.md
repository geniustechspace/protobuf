# Core API Query System - Complete Guide

## Overview

Enterprise-grade, storage-agnostic query system supporting simple to complex queries across all storage types.

**More Powerful Than GraphQL:**
- ✅ Storage-agnostic (SQL, NoSQL, document, cache, graph, time-series)
- ✅ 25+ filter operators vs GraphQL's basic equality
- ✅ Built-in aggregations, full-text search, geospatial
- ✅ Type-safe enums with protocol buffer validation
- ✅ Composable filters with unlimited AND/OR/NOT nesting
- ✅ Multi-language code generation (Go, Python, Java, TypeScript, C#)

## Architecture

```
proto/core/api/query/v1/
├── filter.proto      # 25+ operators, composable AND/OR/NOT
├── sort.proto        # Multi-field sorting, null handling
├── projection.proto  # Field selection, nested relations
├── aggregation.proto # 17+ functions (COUNT, SUM, AVG, PERCENTILE, etc.)
├── search.proto      # 6 search modes (natural, fuzzy, semantic, etc.)
├── relation.proto    # Joins and relation loading
├── query.proto       # Unified query interface
├── enums.proto       # Query type and complexity enums
└── examples.proto    # Comprehensive usage examples
```

## Quick Comparison

### GraphQL Query
```graphql
query {
  users(
    where: {status: {_eq: "active"}},
    order_by: {created_at: desc},
    limit: 20
  ) {
    id
    email
    name
  }
}
```

### Our Query System
```protobuf
Query {
  filter: {field: "status", op: EQ, value: {string: "active"}},
  sort: {sorts: [{field: "created_at", direction: DESC}]},
  projection: {mode: INCLUDE, fields: ["id", "email", "name"]},
  pagination: {page_size: 20}
}
```

**Advantages:**
1. Type-safe with compile-time validation
2. Works with any storage system
3. More operators (25 vs ~10 in GraphQL)
4. Built-in aggregations
5. Full-text and semantic search
6. Geospatial queries
7. No need for resolvers or schema stitching

## Features Matrix

| Feature | GraphQL | Our System |
|---------|---------|------------|
| **Basic Filtering** | ✅ | ✅ |
| **Complex AND/OR** | Limited | ✅ Unlimited nesting |
| **Operators** | ~10 | 25+ |
| **Full-Text Search** | Extension needed | ✅ Built-in (6 modes) |
| **Geospatial** | Extension needed | ✅ Built-in |
| **Aggregations** | Extension needed | ✅ 17+ functions |
| **Array Operations** | Basic | ✅ Advanced (contains, any, all) |
| **Regex/Pattern** | Limited | ✅ Full support |
| **Type Safety** | Runtime (validation) | ✅ Compile-time |
| **Storage Support** | GraphQL servers only | ✅ Any storage |
| **Multi-language** | JS/TS focused | ✅ 5+ languages |

## Operators (25+)

### Equality & Comparison
- `EQ`, `NE` - Equal, Not equal
- `GT`, `GTE`, `LT`, `LTE` - Comparisons

### Collection
- `IN`, `NOT_IN` - List membership
- `BETWEEN` - Range

### String Matching
- `CONTAINS`, `NOT_CONTAINS` - Substring
- `STARTS_WITH`, `ENDS_WITH` - Prefix/suffix
- `MATCHES` - Regex
- `ILIKE` - Case-insensitive like

### Null Checks
- `IS_NULL`, `IS_NOT_NULL`

### Array Operations
- `ARRAY_CONTAINS` - Array contains value
- `ARRAY_CONTAINS_ANY` - Contains any of values
- `ARRAY_CONTAINS_ALL` - Contains all values

### Geospatial
- `GEO_NEAR` - Near point
- `GEO_WITHIN` - Within area
- `GEO_INTERSECTS` - Intersects shape

### Advanced
- `TEXT_SEARCH` - Full-text search
- `EXISTS` - Field exists

## Usage Examples

### Simple Query
```protobuf
Query {
  filter: {field: "status", op: EQ, value: {string: "active"}}
}
```

### Complex E-commerce Search
```protobuf
Query {
  search: {
    query: "wireless headphones",
    fields: ["name", "description"],
    options: {mode: FUZZY, fuzziness: 1, highlight: true}
  },
  filter: {and: [
    {field: "price", op: BETWEEN, value: {string: "50,200"}},
    {field: "in_stock", op: EQ, value: {string: "true"}},
    {field: "rating", op: GTE, value: {string: "4.0"}},
    {field: "category", op: IN, value: {string: "electronics,audio"}}
  ]},
  sort: {sorts: [
    {field: "popularity", direction: DESC},
    {field: "price", direction: ASC}
  ]},
  projection: {
    mode: INCLUDE,
    fields: ["id", "name", "price", "rating", "image_url"]
  },
  pagination: {page_size: 20}
}
```

### Analytics with Aggregation
```protobuf
Query {
  filter: {and: [
    {field: "created_at", op: GTE, value: {string: "2024-01-01"}},
    {field: "tenant_id", op: EQ, value: {string: "tenant_123"}}
  ]},
  group_by: {
    fields: ["status", "category"],
    aggregates: [
      {function: COUNT, alias: "total_orders"},
      {function: SUM, field: "amount", alias: "revenue"},
      {function: AVG, field: "amount", alias: "avg_order"},
      {function: PERCENTILE_95, field: "amount", alias: "p95"}
    ],
    having: "total_orders > 10"
  }
}
```

### Geospatial Query
```protobuf
Query {
  filter: {and: [
    {field: "location", op: GEO_NEAR, value: {string: "40.7128,-74.0060,10"}},
    {field: "type", op: EQ, value: {string: "restaurant"}},
    {field: "rating", op: GTE, value: {string: "4.0"}}
  ]},
  sort: {sorts: [{field: "distance", direction: ASC}]},
  pagination: {page_size: 50}
}
```

### Multi-Tenant with Relations
```protobuf
Query {
  filter: {and: [
    {field: "tenant_id", op: EQ, value: {string: "tenant_123"}},
    {field: "deleted_at", op: IS_NULL},
    {or: [
      {field: "status", op: EQ, value: {string: "active"}},
      {field: "status", op: EQ, value: {string: "pending"}}
    ]}
  ]},
  relations: {
    relations: ["created_by", "organization", "tags"],
    nested: {
      "organization": {relations: ["billing", "subscription"]}
    },
    filters: {
      "tags": {field: "approved", op: EQ, value: {string: "true"}}
    }
  },
  sort: {sorts: [{field: "created_at", direction: DESC}]},
  pagination: {page_size: 50}
}
```

## Storage Implementation

### PostgreSQL
```go
func QueryToSQL(q *queryv1.Query, table string) (string, []interface{}) {
    var clauses []string
    var args []interface{}
    
    // SELECT with projection
    selectClause := "*"
    if q.Projection != nil {
        selectClause = strings.Join(q.Projection.Fields, ", ")
    }
    
    query := fmt.Sprintf("SELECT %s FROM %s", selectClause, table)
    
    // WHERE from filter
    if q.Filter != nil {
        where, whereArgs := filterToSQL(q.Filter)
        query += " WHERE " + where
        args = append(args, whereArgs...)
    }
    
    // GROUP BY with aggregations
    if q.GroupBy != nil {
        query += " GROUP BY " + strings.Join(q.GroupBy.Fields, ", ")
        if q.GroupBy.Having != "" {
            query += " HAVING " + q.GroupBy.Having
        }
    }
    
    // ORDER BY
    if q.Sort != nil {
        var sorts []string
        for _, s := range q.Sort.Sorts {
            dir := "ASC"
            if s.Direction == queryv1.SortDirection_DESC {
              dir = "DESC"
            }
            sorts = append(sorts, fmt.Sprintf("%s %s", s.Field, dir))
        }
        query += " ORDER BY " + strings.Join(sorts, ", ")
    }
    
    // LIMIT/OFFSET
    if q.Pagination != nil {
        query += fmt.Sprintf(" LIMIT %d OFFSET %d", 
            q.Pagination.PageSize, calculateOffset(q.Pagination))
    }
    
    return query, args
}
```

### MongoDB
```go
func QueryToMongoPipeline(q *queryv1.Query) []bson.M {
    pipeline := []bson.M{}
    
    // $match from filter
    if q.Filter != nil {
        pipeline = append(pipeline, bson.M{
            "$match": filterToMongo(q.Filter),
        })
    }
    
    // $search for full-text
    if q.Search != nil {
        pipeline = append(pipeline, bson.M{
            "$search": bson.M{
                "text": bson.M{
                    "query": q.Search.Query,
                    "path":  q.Search.Fields,
                },
            },
        })
    }
    
    // $group for aggregations
    if q.GroupBy != nil {
        groupStage := bson.M{"_id": bson.M{}}
        for _, field := range q.GroupBy.Fields {
            groupStage["_id"].(bson.M)[field] = "$" + field
        }
        for _, agg := range q.GroupBy.Aggregates {
            groupStage[agg.Alias] = aggregateToMongo(agg)
        }
        pipeline = append(pipeline, bson.M{"$group": groupStage})
    }
    
    // $sort
    if q.Sort != nil {
        sortStage := bson.M{}
        for _, s := range q.Sort.Sorts {
            dir := 1
            if s.Direction == queryv1.SortDirection_DESC {
              dir = -1
            }
            sortStage[s.Field] = dir
        }
        pipeline = append(pipeline, bson.M{"$sort": sortStage})
    }
    
    // $skip and $limit
    if q.Pagination != nil {
        pipeline = append(pipeline,
            bson.M{"$skip": calculateOffset(q.Pagination)},
            bson.M{"$limit": q.Pagination.PageSize},
        )
    }
    
    return pipeline
}
```

### Elasticsearch
```go
func QueryToElasticsearch(q *queryv1.Query) map[string]interface{} {
    esQuery := map[string]interface{}{}
    
    // Search query
    if q.Search != nil {
        esQuery["query"] = map[string]interface{}{
            "multi_match": map[string]interface{}{
                "query":     q.Search.Query,
                "fields":    q.Search.Fields,
                "fuzziness": q.Search.Options.Fuzziness,
            },
        }
    }
    
    // Filter as bool.filter
    if q.Filter != nil {
        if esQuery["query"] == nil {
            esQuery["query"] = map[string]interface{}{}
        }
        esQuery["query"].(map[string]interface{})["bool"] = map[string]interface{}{
            "filter": filterToES(q.Filter),
        }
    }
    
    // Aggregations
    if q.GroupBy != nil {
        esQuery["aggs"] = aggregationsToES(q.GroupBy)
    }
    
    // Sort
    if q.Sort != nil {
        esQuery["sort"] = sortToES(q.Sort)
    }
    
    // Pagination
    esQuery["from"] = calculateOffset(q.Pagination)
    esQuery["size"] = q.Pagination.PageSize
    
    // Source fields (projection)
    if q.Projection != nil {
        esQuery["_source"] = q.Projection.Fields
    }
    
    return esQuery
}
```

## Best Practices

1. **Start Simple** - Use only needed features
2. **Index Strategy** - Index all filtered/sorted fields
3. **Pagination Required** - Always set page_size
4. **Test with Explain** - Use explain:true for performance debugging
5. **Type Conversion** - Server converts string values to proper types
6. **Nested Filters** - Use AND/OR for complex logic
7. **Field Paths** - Use dot notation: "user.profile.email"
8. **Relation Loading** - Prefer RelationLoad over Join for simple cases
9. **Aggregation Limits** - Set reasonable max_items limits
10. **Timeout Protection** - Set timeout_ms for expensive queries

## Integration with Request Package

```protobuf
// ListRequest now uses Query
message ListRequest {
  geniustechspace.core.api.query.v1.Query query = 1;
}

// SearchRequest uses Query with search
message SearchRequest {
  geniustechspace.core.api.query.v1.Query query = 1;
}

// CountRequest uses Query for filtering
message CountRequest {
  geniustechspace.core.api.query.v1.Query query = 1;
}
```

## Migration from GraphQL

| GraphQL Concept | Query System Equivalent |
|----------------|-------------------------|
| `query { }` | `Query` message |
| `where:` | `filter` field |
| `order_by:` | `sort` field |
| `limit:` | `pagination.page_size` |
| `_eq:` | `op: EQ` |
| `_in:` | `op: IN` |
| `_like:` | `op: CONTAINS` |
| `_and:` | `filter.and` |
| `_or:` | `filter.or` |
| `aggregate:` | `group_by` |

## Performance Characteristics

| Operation | SQL | MongoDB | Elasticsearch |
|-----------|-----|---------|---------------|
| Simple filter | O(log n) | O(log n) | O(log n) |
| Complex AND/OR | O(log n) | O(log n) | O(log n) |
| Full-text search | O(n) | O(log n) | O(1) |
| Aggregation | O(n) | O(n) | O(n) |
| Geo queries | O(log n) | O(log n) | O(log n) |
| Joins | O(n×m) | O(n) | O(1) |

## See Also

- [Filter Proto](v1/filter.proto) - All filter operators
- [Sort Proto](v1/sort.proto) - Sorting configuration
- [Aggregation Proto](v1/aggregation.proto) - Analytics functions
- [Search Proto](v1/search.proto) - Full-text search
- [Examples Proto](v1/examples.proto) - 50+ usage examples
- [Request Package](../request/) - Integration with CRUD requests
