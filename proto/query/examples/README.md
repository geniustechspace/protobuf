# Query System - Python Usage Examples

Real-world examples demonstrating how to use the Query API in Python applications.

## Prerequisites

```bash
# Generate Python code from protobufs
buf generate --path proto/query/

# Install generated package
cd gen/python
pip install -e .

# Install dependencies
pip install protobuf grpcio
```

## Examples Overview

| File | Description | Use Cases |
|------|-------------|-----------|
| `basic_queries.py` | Simple CRUD queries | User lookup, filtering, sorting |
| `advanced_queries.py` | Complex queries | Aggregations, joins, search |
| `ecommerce_examples.py` | E-commerce scenarios | Orders, products, analytics |
| `analytics_examples.py` | Analytics queries | Dashboards, reports, metrics |
| `search_examples.py` | Search scenarios | Full-text, semantic, hybrid |
| `query_builder.py` | Helper utilities | Query construction patterns |

## Quick Start

```python
from geniustechspace.query.api.v1 import query_pb2, filter_pb2

# Simple filter query
query = query_pb2.Query(
    entity="users",
    filter=filter_pb2.Filter(
        condition=filter_pb2.Condition(
            field="status",
            operator=filter_pb2.OPERATOR_EQ,
            value={"string_value": "active"}
        )
    ),
    pagination={"page_size": 50}
)
```

## Running Examples

```bash
# Run individual examples
python proto/query/examples/basic_queries.py
python proto/query/examples/ecommerce_examples.py

# Run all examples
python proto/query/examples/run_all.py
```

## Example Categories

### 1. Basic Queries
- Simple equality filters
- Range queries
- Sorting and pagination
- Field projection

### 2. Advanced Queries
- Complex boolean logic (AND/OR/NOT)
- Aggregations and grouping
- Explicit joins
- Having clauses

### 3. E-commerce
- Product search and filtering
- Order management
- Customer analytics
- Inventory queries

### 4. Analytics
- Time-series queries
- Dashboard metrics
- Report generation
- KPI calculations

### 5. Search
- Full-text search
- Semantic search
- Hybrid search
- Faceted search

## Best Practices

### 1. Use Query Builder Pattern
```python
from query_builder import QueryBuilder

query = (QueryBuilder("users")
    .filter_eq("status", "active")
    .filter_gte("created_at", "2024-01-01")
    .sort_desc("created_at")
    .limit(50)
    .build())
```

### 2. Reusable Filter Templates
```python
def active_users_filter():
    return filter_pb2.Filter(
        and_=filter_pb2.AndFilter(
            conditions=[
                filter_pb2.Filter(
                    condition=filter_pb2.Condition(
                        field="status",
                        operator=filter_pb2.OPERATOR_EQ,
                        value={"string_value": "active"}
                    )
                ),
                filter_pb2.Filter(
                    condition=filter_pb2.Condition(
                        field="deleted_at",
                        operator=filter_pb2.OPERATOR_IS_NULL
                    )
                )
            ]
        )
    )
```

### 3. Pagination Helpers
```python
def paginate(query, page_size=50, cursor=None):
    query.pagination.page_size = page_size
    if cursor:
        query.pagination.cursor = cursor
    return query
```

### 4. Error Handling
```python
try:
    response = query_service.Execute(query)
except grpc.RpcError as e:
    if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
        # Handle validation errors
        print(f"Invalid query: {e.details()}")
    elif e.code() == grpc.StatusCode.PERMISSION_DENIED:
        # Handle permission errors
        print(f"Access denied: {e.details()}")
```

## Common Patterns

### Filter by Multiple Values (IN operator)
```python
filter_pb2.Condition(
    field="status",
    operator=filter_pb2.OPERATOR_IN,
    values=[
        {"string_value": "active"},
        {"string_value": "pending"}
    ]
)
```

### Date Range Queries
```python
filter_pb2.Filter(
    and_=filter_pb2.AndFilter(
        conditions=[
            filter_pb2.Filter(
                condition=filter_pb2.Condition(
                    field="created_at",
                    operator=filter_pb2.OPERATOR_GTE,
                    value={"timestamp_value": "2024-01-01T00:00:00Z"}
                )
            ),
            filter_pb2.Filter(
                condition=filter_pb2.Condition(
                    field="created_at",
                    operator=filter_pb2.OPERATOR_LT,
                    value={"timestamp_value": "2024-02-01T00:00:00Z"}
                )
            )
        ]
    )
)
```

### Nested Field Access
```python
filter_pb2.Condition(
    field="user.profile.country",
    operator=filter_pb2.OPERATOR_EQ,
    value={"string_value": "US"}
)
```

### Array Operations
```python
filter_pb2.Condition(
    field="tags",
    operator=filter_pb2.OPERATOR_ARRAY_CONTAINS,
    value={"string_value": "featured"}
)
```

## Testing Queries

```python
import pytest
from google.protobuf.json_format import MessageToDict

def test_query_serialization():
    query = build_users_query()
    
    # Serialize to JSON
    json_query = MessageToDict(query)
    assert json_query["entity"] == "users"
    
    # Validate required fields
    assert "pagination" in json_query
    assert json_query["pagination"]["pageSize"] > 0
```

## Performance Tips

1. **Use Cursor Pagination**: More efficient than offset for large datasets
2. **Project Only Needed Fields**: Reduce network and memory overhead
3. **Push Filters Down**: Let the storage engine filter early
4. **Use Indexes**: Filter on indexed fields when possible
5. **Batch Queries**: Combine multiple reads when possible

## Troubleshooting

### Query Validation Errors
- Check field names match schema
- Verify operator compatibility with field types
- Ensure required fields are set

### Performance Issues
- Use EXPLAIN to analyze query plan
- Check for missing indexes
- Reduce projection size
- Use cursor pagination

### Permission Errors
- Verify tenant_id is set
- Check user has field-level permissions
- Ensure user_id is provided for audit

## Additional Resources

- [Query API Documentation](../README.md)
- [Operator Reference](../api/v1/filter.proto)
- [Schema Registry Guide](../../core/README.md)
- [gRPC Python Documentation](https://grpc.io/docs/languages/python/)
