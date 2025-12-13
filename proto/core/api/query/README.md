# Core API Query

Comprehensive, storage-agnostic query system for all data operations.

## Package

```protobuf
package geniustechspace.core.api.query.v1;
```

## Overview

Universal query interface that works with:

- **SQL**: PostgreSQL, MySQL, SQLite
- **NoSQL**: MongoDB, DynamoDB, Cassandra
- **Document**: Elasticsearch, Solr
- **Cache**: Redis, Memcached
- **Graph**: Neo4j
- **Time-series**: InfluxDB, TimescaleDB

## Architecture

**Modular Design:**

```
query/v1/
├── filter.proto      # Filtering (25+ operators)
├── sort.proto        # Multi-field sorting
├── projection.proto  # Field selection
├── aggregation.proto # Analytics (17+ functions)
├── search.proto      # Full-text search
├── relation.proto    # Joins & relations
└── query.proto       # Main query interface
```

**Philosophy:** Start simple, add complexity only when needed.

## Quick Start

### Simple Query

```protobuf
Query {
  filter: {field: "status", op: EQ, value: {string: "active"}}
}
```

### Filter + Sort

```protobuf
Query {
  filter: {field: "status", op: EQ, value: {string: "active"}},
  sort: {sorts: [{field: "created_at", direction: DESC}]}
}
```

### Complex AND/OR

```protobuf
Query {
  filter: {
    and: [
      {field: "status", op: EQ, value: {string: "active"}},
      {or: [
        {field: "tier", op: EQ, value: {string: "premium"}},
        {field: "tier", op: EQ, value: {string: "enterprise"}}
      ]}
    ]
  }
}
```

## Features

### 1. Filtering (filter.proto)

**25+ Operators:**

| Category | Operators |
|----------|-----------|
| **Equality** | EQ, NE |
| **Comparison** | GT, GTE, LT, LTE |
| **Collection** | IN, NOT_IN |
| **String** | CONTAINS, STARTS_WITH, ENDS_WITH, MATCHES, ILIKE |
| **Null** | IS_NULL, IS_NOT_NULL |
| **Range** | BETWEEN |
| **Array** | ARRAY_CONTAINS, ARRAY_CONTAINS_ANY, ARRAY_CONTAINS_ALL |
| **Geo** | GEO_NEAR, GEO_WITHIN, GEO_INTERSECTS |
| **Search** | TEXT_SEARCH |
| **Existence** | EXISTS |

**Composable:** Nest AND/OR/NOT logic infinitely.

### 2. Sorting (sort.proto)

```protobuf
SortBy {
  sorts: [
    {field: "priority", direction: DESC, null_handling: NULLS_LAST},
    {field: "created_at", direction: DESC}
  ]
}
```

### 3. Projection (projection.proto)

```protobuf
// Include only specific fields
Projection {
  mode: INCLUDE,
  fields: ["id", "email", "name"]
}

// Exclude fields
Projection {
  mode: EXCLUDE,
  fields: ["password_hash", "internal_notes"]
}

// Nested relations
Projection {
  mode: INCLUDE,
  fields: ["id", "name"],
  relations: {
    "user": {mode: INCLUDE, fields: ["id", "email"]}
  }
}
```

### 4. Aggregation (aggregation.proto)

**17+ Functions:** COUNT, SUM, AVG, MIN, MAX, STDDEV, MEDIAN, PERCENTILE_99, etc.

```protobuf
// Group by status, count per group
GroupBy {
  fields: ["status"],
  aggregates: [{function: COUNT, alias: "count"}]
}

// Multiple aggregations
GroupBy {
  fields: ["category"],
  aggregates: [
    {function: COUNT, alias: "total"},
    {function: SUM, field: "amount", alias: "revenue"},
    {function: AVG, field: "rating", alias: "avg_rating"}
  ]
}

// With HAVING clause
GroupBy {
  fields: ["status"],
  aggregates: [{function: COUNT, alias: "count"}],
  having: "count > 10"
}
```

### 5. Full-Text Search (search.proto)

**Search Modes:**
- NATURAL - Natural language
- BOOLEAN - AND/OR/NOT operators
- PHRASE - Exact phrase match
- WILDCARD - Pattern matching
- FUZZY - Typo tolerance
- SEMANTIC - Vector/embedding search

```protobuf
Search {
  query: "machine learning",
  fields: ["title", "description"],
  options: {
    mode: SEMANTIC,
    min_score: 0.7,
    highlight: true,
    field_boosts: {"title": 2.0, "description": 1.0}
  }
}
```

### 6. Relations & Joins (relation.proto)

**Simple relation loading:**

```protobuf
RelationLoad {
  relations: ["user", "comments"],
  nested: {
    "user": {relations: ["profile"]}
  },
  filters: {
    "comments": {field: "approved", op: EQ, value: {string: "true"}}
  }
}
```

**Complex joins:**

```protobuf
Join {
  type: LEFT,
  relation: "users",
  local_field: "user_id",
  foreign_field: "id",
  filter: {field: "status", op: EQ, value: {string: "active"}},
  projection: {mode: INCLUDE, fields: ["id", "email"]},
  alias: "author"
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
      {field: "price", op: BETWEEN, value: {string: "50,200"}},
      {field: "in_stock", op: EQ, value: {string: "true"}},
      {field: "rating", op: GTE, value: {string: "4.0"}}
    ]
  },
  sort: {sorts: [
    {field: "popularity", direction: DESC},
    {field: "price", direction: ASC}
  ]},
  pagination: {page_size: 20}
}
```

### Analytics Dashboard

```protobuf
Query {
  filter: {
    field: "created_at",
    op: GTE,
    value: {string: "2024-01-01"}
  },
  group_by: {
    fields: ["status", "category"],
    aggregates: [
      {function: COUNT, alias: "total"},
      {function: SUM, field: "revenue", alias: "revenue"},
      {function: AVG, field: "amount", alias: "avg_amount"}
    ]
  }
}
```

### Geospatial Query

```protobuf
Query {
  filter: {
    field: "location",
    op: GEO_NEAR,
    value: {string: "40.7128,-74.0060,10"}  // NYC, 10km radius
  },
  sort: {sorts: [{field: "distance", direction: ASC}]},
  pagination: {page_size: 50}
}
```

### Multi-Tenant with Relations

```protobuf
Query {
  filter: {
    and: [
      {field: "tenant_id", op: EQ, value: {string: "tenant_123"}},
      {field: "deleted_at", op: IS_NULL}
    ]
  },
  relations: {
    relations: ["created_by", "organization"],
    nested: {
      "organization": {relations: ["billing"]}
    }
  },
  sort: {sorts: [{field: "created_at", direction: DESC}]},
  pagination: {page_size: 50}
}
```

## Storage Implementation

### SQL (PostgreSQL)

```go
func ToSQL(q *Query) (string, []interface{}, error) {
    query := "SELECT "
    
    // Projection
    if q.Projection != nil {
        query += strings.Join(q.Projection.Fields, ", ")
    } else {
        query += "*"
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
```

### MongoDB

```go
func ToMongo(q *Query) bson.M {
    pipeline := []bson.M{}
    
    // Filter → $match
    if q.Filter != nil {
        pipeline = append(pipeline, bson.M{"$match": filterToMongo(q.Filter)})
    }
    
    // Aggregation → $group
    if q.GroupBy != nil {
        pipeline = append(pipeline, bson.M{"$group": groupByToMongo(q.GroupBy)})
    }
    
    // Sort → $sort
    if q.Sort != nil {
        pipeline = append(pipeline, bson.M{"$sort": sortToMongo(q.Sort)})
    }
    
    // Pagination → $skip + $limit
    if q.Pagination != nil {
        pipeline = append(pipeline, 
            bson.M{"$skip": offset},
            bson.M{"$limit": q.Pagination.PageSize})
    }
    
    return bson.M{"$aggregate": pipeline}
}
```

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

## Related

- [Pagination](../pagination/v1/messages.proto) - Cursor-based pagination
- [Request](../request/v1/messages.proto) - Request wrappers using Query
- [Response](../response/v1/messages.proto) - Response structure
