# Core API Query - Complete Guide

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Filter System](#filter-system)
4. [Projection (Field Selection)](#projection-field-selection)
5. [Relations & Auto-Joins](#relations--auto-joins)
6. [Search](#search)
7. [Aggregation](#aggregation)
8. [Sorting](#sorting)
9. [Storage Implementation](#storage-implementation)
10. [Migration Guide](#migration-guide)
11. [Best Practices](#best-practices)

## Overview

**Universal, storage-agnostic query system** for all data operations.

**Supported Storage:**

- SQL: PostgreSQL, MySQL, SQLite, SQL Server
- NoSQL: MongoDB, DynamoDB, Cassandra
- Document: Elasticsearch, Solr
- Cache: Redis, Memcached
- Graph: Neo4j
- Time-series: InfluxDB, TimescaleDB
- Filesystems: POSIX, S3, Azure Blob

**Key Features:**

- 25+ filter operators
- Auto-join inference from field paths
- PSL wildcards for field selection
- Full-text search (6 modes)
- Aggregations (17+ functions)
- Geospatial queries
- Type-safe with compile-time validation

## Quick Start

### Simple Query

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

### With Relations (Auto-Join)

```protobuf
Query {
  filter: {field: "user.status", op: EQ, value: "verified"},
  include: ["id", "title", "user.name", "user.email"]
  // Server auto-detects and loads "user" relation
}
```

### Complex Query

```protobuf
Query {
  filter: {and: [
    {field: "status", op: EQ, value: "active"},
    {field: "price", op: BETWEEN, values: ["50", "200"]},
    {field: "rating", op: GTE, value: "4.0"}
  ]},
  include: ["id", "name", "price"],
  sorts: [{field: "popularity", direction: DESC}],
  pagination: {page_size: 20}
}
```

## Filter System

### Type-Safe Values

**Use `value` for scalars, `values` for collections:**

```protobuf
Filter {
  field: "status"
  op: EQ
  value: "active"  // Scalar: single string
}

Filter {
  field: "role"
  op: IN
  values: ["admin", "owner", "editor"]  // Collection: array of strings
}
```

### 25+ Operators

#### Equality & Comparison

```protobuf
{field: "age", op: EQ, value: "25"}
{field: "age", op: NE, value: "0"}
{field: "score", op: GT, value: "90"}
{field: "score", op: GTE, value: "80"}
{field: "price", op: LT, value: "100"}
{field: "price", op: LTE, value: "50"}
```

#### Collection Operators

```protobuf
// IN - array of values
{field: "status", op: IN, values: ["active", "pending", "approved"]}

// NOT_IN
{field: "role", op: NOT_IN, values: ["blocked", "suspended"]}

// BETWEEN - array with min/max
{field: "price", op: BETWEEN, values: ["50", "200"]}
```

#### String Matching

```protobuf
{field: "email", op: CONTAINS, value: "@company.com"}
{field: "name", op: STARTS_WITH, value: "John"}
{field: "title", op: ENDS_WITH, value: "Manager"}
{field: "phone", op: MATCHES, value: "^\\+1[0-9]{10}$"}
{field: "description", op: ILIKE, value: "%search%"}
```

#### Null Checks

```protobuf
{field: "deleted_at", op: IS_NULL}
{field: "verified_at", op: IS_NOT_NULL}
```

#### Array Operations

```protobuf
// Array contains single value
{field: "tags", op: ARRAY_CONTAINS, value: "featured"}

// Array contains any of
{field: "permissions", op: ARRAY_CONTAINS_ANY, values: ["read", "write", "admin"]}

// Array contains all of
{field: "skills", op: ARRAY_CONTAINS_ALL, values: ["python", "docker"]}
```

#### Geospatial

```protobuf
// Near point: lat, lng, radius_km as array
{field: "location", op: GEO_NEAR, values: ["40.7128", "-74.0060", "10"]}

// Within bounding box (single value as GeoJSON)
{field: "location", op: GEO_WITHIN, value: "[[40.7128,-74.0060],[40.7580,-73.9855]]"}
```

### Composable Logic

#### AND Conditions

```protobuf
Filter {
  and: [
    {field: "status", op: EQ, value: "active"},
    {field: "tier", op: IN, values: ["premium", "enterprise"]}
  ]
}
```

#### OR Conditions

```protobuf
Filter {
  or: [
    {field: "role", op: EQ, value: "admin"},
    {field: "role", op: EQ, value: "owner"}
  ]
}
```

#### Nested AND/OR

```protobuf
Filter {
  and: [
    {field: "status", op: EQ, value: "active"},
    {or: [
      {field: "tier", op: EQ, value: "premium"},
      {field: "tier", op: EQ, value: "enterprise"}
    ]}
  ]
}
```

## Projection (Field Selection)

### PSL (Projection Selector Language) v1

Universal field selection using wildcards and patterns.

#### Basic Selection

```protobuf
Query {
  include: ["id", "name", "email"]
}
```

#### Exclude Secrets

```protobuf
Query {
  exclude: ["**.password", "**.token", "**.ssn", "**.apiKey"]
}
```

#### Nested Fields

```protobuf
Query {
  include: ["id", "user.name", "user.profile.avatar"]
}
```

#### Wildcards

**Single-level wildcard (`*`):**

```protobuf
Query {
  include: ["user.*"]  // All direct children of user
}
```

**Recursive wildcard (`**`):\*\*

```protobuf
Query {
  include: ["user.**"]  // Entire user subtree
}
```

**Deep field search:**

```protobuf
Query {
  include: ["**.id", "**.createdAt"]  // All IDs and timestamps
}
```

#### Lists

```protobuf
Query {
  include: [
    "orders[].id",
    "orders[].total",
    "orders[].items[].sku"
  ]
}
```

#### Maps

```protobuf
// All map keys
Query {
  include: ["attributes[*]", "metadata[*]"]
}

// Specific key
Query {
  include: ["metadata['version']", "config['timeout']"]
}
```

#### Mixed Include/Exclude

```protobuf
Query {
  include: ["user.**"],
  exclude: ["user.internalNotes", "user.password"]
}
```

### PSL Syntax Reference

| Pattern         | Matches              | Example                              |
| --------------- | -------------------- | ------------------------------------ |
| `field`         | Single field         | `name`                               |
| `parent.child`  | Nested field         | `user.email`                         |
| `*`             | One segment          | `user.*` → `user.name`, `user.email` |
| `**`            | Recursive            | `user.**` → entire user tree         |
| `**.field`      | Deep search          | `**.id` → all IDs                    |
| `field[]`       | List elements        | `orders[]`                           |
| `field[].child` | List children        | `orders[].total`                     |
| `map[*]`        | All map keys         | `attributes[*]`                      |
| `map['key']`    | Specific key         | `metadata['version']`                |
| `` `field` ``   | Escape special chars | `` `user.first.name` ``              |

## Relations & Auto-Joins

### Auto-Inference

**No need to specify relations separately!** Server detects from field paths.

#### Simple Auto-Join

```protobuf
Query {
  include: ["id", "user.name", "user.email"]
  // Server auto-loads "user" relation
}
```

#### Nested Relations

```protobuf
Query {
  include: [
    "id",
    "user.name",
    "user.profile.city",
    "user.organization.name"
  ]
  // Auto-loads: user → user.profile → user.organization
}
```

#### From Filters

```protobuf
Query {
  filter: {field: "user.status", op: EQ, value: "verified"},
  include: ["id", "title"]
  // Auto-loads "user" from filter
}
```

#### List Relations

```protobuf
Query {
  include: [
    "id",
    "comments[].content",
    "comments[].author.name",
    "orders[].items[].product.name"
  ]
  // Auto-loads: comments → comments.author,
  //             orders → orders.items → orders.items.product
}
```

#### Wildcards Relations

```protobuf
Query {
  include: ["id", "user.**"]  // Loads entire user subtree
}

Query {
  include: ["**.metadata"]  // Loads all metadata relations
}
```

### Explicit Joins (Rare)

Use only when you need:

- Custom join conditions
- Table aliases
- Non-standard foreign keys

```protobuf
Query {
  joins: [{
    type: LEFT,
    relation: "users",
    local_field: "author_id",
    foreign_field: "id",
    filter: {field: "status", op: EQ, value: "verified"},
    alias: "verified_author"
  }]
}
```

## Search

### Full-Text Search Modes

#### Natural Language

```protobuf
Search {
  query: "machine learning tutorial",
  fields: ["title", "description"],
  options: {mode: NATURAL}
}
```

#### Universal Search (All Fields)

```protobuf
Search {
  query: "error",
  fields: ["**"],  // Searches all text fields
  options: {mode: NATURAL}
}
```

#### Fuzzy Search (Typo Tolerance)

```protobuf
Search {
  query: "pythn",  // Will match "python"
  fields: ["tags"],
  options: {mode: FUZZY, fuzziness: 2}
}
```

#### Phrase Match

```protobuf
Search {
  query: "artificial intelligence",
  fields: ["title", "content"],
  options: {mode: PHRASE}
}
```

#### Field Boosting

```protobuf
Search {
  query: "kubernetes",
  fields: ["title", "description"],
  options: {
    mode: NATURAL,
    field_boosts: {"title": 2.0, "description": 1.0}
  }
}
```

#### Semantic/Vector Search

```protobuf
Search {
  query: "How to deploy containers",
  fields: ["content"],
  options: {mode: SEMANTIC, min_score: 0.7}
}
```

## Aggregation

### Group By with Aggregates

#### Count by Group

```protobuf
Grouping {
  fields: ["status"],
  aggregates: [{function: COUNT, alias: "count"}]
}
```

#### Multiple Aggregates

```protobuf
Grouping {
  fields: ["category"],
  aggregates: [
    {function: COUNT, alias: "total"},
    {function: SUM, field: "amount", alias: "revenue"},
    {function: AVG, field: "rating", alias: "avg_rating"},
    {function: MIN, field: "price", alias: "min_price"},
    {function: MAX, field: "price", alias: "max_price"}
  ]
}
```

#### With HAVING Filter

```protobuf
Grouping {
  fields: ["user_id"],
  aggregates: [{function: COUNT, alias: "order_count"}],
  having: "order_count > 5"
}
```

### Available Functions

| Function       | Description         |
| -------------- | ------------------- |
| COUNT          | Count rows          |
| COUNT_DISTINCT | Count unique values |
| SUM            | Sum values          |
| AVG            | Average             |
| MIN            | Minimum value       |
| MAX            | Maximum value       |
| STDDEV         | Standard deviation  |
| VARIANCE       | Variance            |
| MEDIAN         | Median value        |
| PERCENTILE_50  | 50th percentile     |
| PERCENTILE_90  | 90th percentile     |
| PERCENTILE_95  | 95th percentile     |
| PERCENTILE_99  | 99th percentile     |
| ARRAY_AGG      | Aggregate to array  |
| STRING_AGG     | Concatenate strings |
| FIRST          | First value         |
| LAST           | Last value          |

## Sorting

### Simple Sort

```protobuf
// In Query
sorts: [{field: "created_at", direction: DESC}]
```

### Multi-Field Sort

```protobuf
sorts: [
    {field: "priority", direction: DESC},
    {field: "created_at", direction: ASC}
  ]
}
```

### Null Handling

```protobuf
sorts: [{
    field: "completed_at",
    direction: ASC,
    null_handling: NULLS_LAST
  }]
}
```

### Sort by Relation

```protobuf
Query {
  include: ["id", "user.name"],
  sorts: [{field: "user.created_at", direction: DESC}]
  // Auto-loads user for sorting
}
```

## Storage Implementation

### SQL (PostgreSQL Example)

```go
func ToSQL(q *Query) (string, []interface{}, error) {
    var query strings.Builder
    args := []interface{}{}
    argIndex := 1

    // SELECT with projection
    query.WriteString("SELECT ")
    if len(q.Include) > 0 {
        fields := expandPSL(q.Include, schema)
        if len(q.Exclude) > 0 {
            excludeSet := expandPSL(q.Exclude, schema)
            fields = subtract(fields, excludeSet)
        }
        query.WriteString(strings.Join(fields, ", "))
    } else {
        query.WriteString("*")
    }

    query.WriteString(" FROM ")
    query.WriteString(table)

    // Auto-detect joins
    joins := detectJoins(q.Filter, q.Include, schema)
    for _, join := range joins {
        query.WriteString(fmt.Sprintf(
            " LEFT JOIN %s ON %s.%s = %s.%s",
            join.Table, table, join.LocalField,
            join.Table, join.ForeignField))
    }

    // WHERE clause
    if q.Filter != nil {
        where, whereArgs := filterToSQL(q.Filter, &argIndex)
        query.WriteString(" WHERE ")
        query.WriteString(where)
        args = append(args, whereArgs...)
    }

    // ORDER BY
    if q.Sort != nil {
        query.WriteString(" ORDER BY ")
        query.WriteString(sortToSQL(q.Sort))
    }

    // LIMIT/OFFSET
    if q.Pagination != nil {
        query.WriteString(fmt.Sprintf(" LIMIT $%d OFFSET $%d",
            argIndex, argIndex+1))
        args = append(args, q.Pagination.PageSize, offset)
    }

    return query.String(), args, nil
}

func filterToSQL(f *Filter, argIndex *int) (string, []interface{}) {
    if len(f.And) > 0 {
        parts := []string{}
        args := []interface{}{}
        for _, sub := range f.And {
            sql, subArgs := filterToSQL(sub, argIndex)
            parts = append(parts, sql)
            args = append(args, subArgs...)
        }
        return "(" + strings.Join(parts, " AND ") + ")", args
    }

    if len(f.Or) > 0 {
        parts := []string{}
        args := []interface{}{}
        for _, sub := range f.Or {
            sql, subArgs := filterToSQL(sub, argIndex)
            parts = append(parts, sql)
            args = append(args, subArgs...)
        }
        return "(" + strings.Join(parts, " OR ") + ")", args
    }

    // Convert operator
    var sql string
    args := []interface{}{}

    switch f.Op {
    case EQ:
        sql = fmt.Sprintf("%s = $%d", f.Field, *argIndex)
        args = append(args, f.Value)
        *argIndex++
    case IN:
        placeholders := []string{}
        for _, v := range f.Values {
            placeholders = append(placeholders, fmt.Sprintf("$%d", *argIndex))
            args = append(args, v)
            *argIndex++
        }
        sql = fmt.Sprintf("%s IN (%s)", f.Field,
            strings.Join(placeholders, ","))
    case BETWEEN:
        sql = fmt.Sprintf("%s BETWEEN $%d AND $%d",
            f.Field, *argIndex, *argIndex+1)
        args = append(args, f.Values[0], f.Values[1])
        *argIndex += 2
    // ... more operators
    }

    return sql, args
}

func detectJoins(filter *Filter, include []string, schema *Schema) []Join {
    relations := make(map[string]bool)

    // From filter
    if filter != nil {
        extractRelationsFromFilter(filter, relations)
    }

    // From include paths
    for _, path := range include {
        parts := strings.Split(path, ".")
        for i := 0; i < len(parts)-1; i++ {
            relation := strings.Join(parts[:i+1], ".")
            relations[relation] = true
        }
    }

    // Convert to joins
    joins := []Join{}
    for relation := range relations {
        joinInfo := schema.GetJoin(relation)
        joins = append(joins, joinInfo)
    }

    return joins
}
```

### MongoDB Example

```go
func ToMongo(q *Query) bson.M {
    pipeline := []bson.M{}

    // $match
    if q.Filter != nil {
        pipeline = append(pipeline,
            bson.M{"$match": filterToMongo(q.Filter)})
    }

    // $lookup for relations
    relations := detectRelations(q.Filter, q.Include)
    for _, rel := range relations {
        pipeline = append(pipeline, bson.M{
            "$lookup": bson.M{
                "from":         rel.Collection,
                "localField":   rel.LocalField,
                "foreignField": rel.ForeignField,
                "as":           rel.Alias,
            },
        })
    }

    // $project
    if len(q.Include) > 0 {
        projection := expandPSLToMongo(q.Include, q.Exclude)
        pipeline = append(pipeline,
            bson.M{"$project": projection})
    }

    // $sort
    if len(q.Sorts) > 0 {
        pipeline = append(pipeline,
            bson.M{"$sort": sortsToMongo(q.Sorts)})
    }

    // $skip + $limit
    if q.Pagination != nil {
        pipeline = append(pipeline,
            bson.M{"$skip": offset},
            bson.M{"$limit": q.Pagination.PageSize})
    }

    return bson.M{"$aggregate": pipeline}
}

func filterToMongo(f *Filter) bson.M {
    if len(f.And) > 0 {
        conditions := []bson.M{}
        for _, sub := range f.And {
            conditions = append(conditions, filterToMongo(sub))
        }
        return bson.M{"$and": conditions}
    }

    if len(f.Or) > 0 {
        conditions := []bson.M{}
        for _, sub := range f.Or {
            conditions = append(conditions, filterToMongo(sub))
        }
        return bson.M{"$or": conditions}
    }

    switch f.Op {
    case EQ:
        return bson.M{f.Field: f.Value}
    case IN:
        return bson.M{f.Field: bson.M{"$in": f.Values}}
    case GT:
        return bson.M{f.Field: bson.M{"$gt": f.Value}}
    // ... more operators
    }
}
```

## Migration Guide

### From GraphQL

**GraphQL:**

```graphql
query {
  users(
    where: { status: { _eq: "active" }, role: { _in: ["admin", "owner"] } }
  ) {
    id
    email
  }
}
```

**Query System:**

```protobuf
Query {
  filter: {and: [
    {field: "status", op: EQ, value: "active"},
    {field: "role", op: IN, values: ["admin", "owner"]}
  ]},
  include: ["id", "email"]
}
```

### From Old Query Format

**Old (deprecated):**

```protobuf
Query {
  filter: {field: "status", op: EQ, value: "active"},
  projection: {include: ["id", "user.name"]},
  relations: {relations: ["user"]}
}
```

**New (current):**

```protobuf
Query {
  filter: {field: "status", op: EQ, value: "active"},
  include: ["id", "user.name"]
  // Relations auto-detected from paths
}
```

**Key Changes:**

1. **Filter values:** Scalars use `value: "X"`, lists use `values: ["A", "B"]`
2. **Projection:** `projection: {include: [...]}` → `include: [...]`
3. **Relations:** Remove `relations` field - auto-detected from paths

## Best Practices

### 1. Use Specific Projections

**Bad:**

```protobuf
Query {
  filter: {field: "status", op: EQ, value: "active"}
  // Returns all fields
}
```

**Good:**

```protobuf
Query {
  filter: {field: "status", op: EQ, value: "active"},
  include: ["id", "name", "email"]
}
```

### 2. Global Secret Exclusion

```protobuf
Query {
  exclude: ["**.password", "**.token", "**.ssn", "**.apiKey"]
  // Protects secrets everywhere
}
```

### 3. Leverage Auto-Joins

**Bad (explicit joins for standard FK):**

```protobuf
Query {
  joins: [{relation: "users", local_field: "user_id", foreign_field: "id"}]
}
```

**Good (auto-inference):**

```protobuf
Query {
  include: ["id", "user.name", "user.email"]
  // Auto-detects standard FK relationship
}
```

### 4. Use Wildcards for Flexibility

```protobuf
Query {
  include: ["id", "user.**"]  // Easy to maintain
}
```

### 5. Always Set Pagination

```protobuf
Query {
  filter: {field: "status", op: EQ, value: "active"},
  pagination: {page_size: 50}
}
```

### 6. Index Filtered/Sorted Fields

Ensure database indexes cover:

- Filter fields
- Sort fields
- Foreign keys (for joins)

### 7. Test with Explain

Use storage-specific explain plans:

```sql
EXPLAIN ANALYZE <generated_query>
```

### 8. Pre-compile PSL Patterns

Cache PSL matchers for repeated queries:

```go
var commonPatterns = map[string]*PSLMatcher{
    "user_fields": CompilePSL([]string{"user.**"}),
    "safe_fields": CompilePSL([]string{"**"}, []string{"**.password"}),
}
```

### 9. Use Timeouts

```protobuf
Query {
  filter: {...},
  timeout_ms: 5000  // 5 seconds max
}
```

### 10. Batch Relation Loads

Server should batch relation loads to avoid N+1:

```go
// Bad: Load user for each post
for _, post := range posts {
    post.User = LoadUser(post.UserID)
}

// Good: Batch load
userIDs := extractUserIDs(posts)
users := LoadUsersInBatch(userIDs)
attachUsers(posts, users)
```

## Common Patterns

### Multi-Tenant with Security

```protobuf
Query {
  filter: {and: [
    {field: "tenant_id", op: EQ, value: "tenant_123"},
    {field: "deleted_at", op: IS_NULL}
  ]},
  exclude: ["**.password", "**.token"],
  pagination: {page_size: 50}
}
```

### E-commerce Product Search

```protobuf
Query {
  search: {
    query: "wireless headphones",
    fields: ["name", "description"],
    options: {mode: FUZZY, fuzziness: 1}
  },
  filter: {and: [
    {field: "price", op: BETWEEN, values: ["50", "200"]},
    {field: "in_stock", op: EQ, value: "true"},
    {field: "rating", op: GTE, value: "4.0"}
  ]},
  include: ["id", "name", "price", "image_url"],
  sorts: [
    {field: "popularity", direction: DESC},
    {field: "price", direction: ASC}
  ],
  pagination: {page_size: 20}
}
```

### Analytics Dashboard

```protobuf
Query {
  filter: {
    field: "created_at",
    op: GTE,
    value: "2024-01-01"
  },
  grouping: {
    fields: ["status", "category"],
    aggregates: [
      {function: COUNT, alias: "total"},
      {function: SUM, field: "revenue", alias: "revenue"},
      {function: AVG, field: "amount", alias: "avg_amount"}
    ]
  }
}
```

### Geospatial: Nearby Locations

```protobuf
Query {
  filter: {
    field: "location",
    op: GEO_NEAR,
    values: ["40.7128", "-74.0060", "10"]  // NYC, 10km
  },
  include: ["id", "name", "address", "rating"],
  sorts: [{field: "distance", direction: ASC}],
  pagination: {page_size: 50}
}
```

## Resources

- [README.md](README.md) - Package overview and quick examples
- [PSL_SPEC.md](PSL_SPEC.md) - Complete PSL syntax specification
- [examples.proto](v1/examples.proto) - Comprehensive query examples
- [query.proto](v1/query.proto) - Main query message definition
- [filter.proto](v1/filter.proto) - Filter operators and syntax

---

**Version:** v1  
**Status:** Stable  
**Note:** Deprecated `Projection` and `RelationLoad` messages have been removed. Use flattened Query syntax.
