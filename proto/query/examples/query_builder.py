#!/usr/bin/env python3
"""
Query Builder - Fluent API for constructing queries

Provides a Pythonic, chainable interface for building complex queries
without dealing with nested protobuf message construction.

Usage:
    query = (QueryBuilder("users")
        .filter_eq("status", "active")
        .filter_gte("age", 18)
        .sort_desc("created_at")
        .limit(50)
        .build())
"""

from typing import Any, List, Optional, Union
from datetime import datetime
from google.protobuf.struct_pb2 import Value
from geniustechspace.query.api.v1 import (
    query_pb2,
    filter_pb2,
    sort_pb2,
    aggregation_pb2,
    search_pb2,
    pagination_pb2,
    relation_pb2
)


class QueryBuilder:
    """Fluent query builder for constructing protobuf queries"""
    
    def __init__(self, entity: str):
        """
        Initialize query builder
        
        Args:
            entity: Entity/collection name to query
        """
        self._entity = entity
        self._filters: List[filter_pb2.Filter] = []
        self._sorts: List[sort_pb2.Sort] = []
        self._projection: Optional[query_pb2.Projection] = None
        self._pagination: Optional[pagination_pb2.Pagination] = None
        self._aggregation: Optional[aggregation_pb2.Aggregation] = None
        self._search: Optional[search_pb2.Search] = None
        self._relations: List[relation_pb2.Relation] = []
        self._options: Optional[query_pb2.QueryOptions] = None
    
    # Filter methods
    
    def filter_eq(self, field: str, value: Any) -> 'QueryBuilder':
        """Add equality filter: field = value"""
        self._add_condition(field, filter_pb2.OPERATOR_EQ, value)
        return self
    
    def filter_ne(self, field: str, value: Any) -> 'QueryBuilder':
        """Add not-equal filter: field != value"""
        self._add_condition(field, filter_pb2.OPERATOR_NE, value)
        return self
    
    def filter_lt(self, field: str, value: Any) -> 'QueryBuilder':
        """Add less-than filter: field < value"""
        self._add_condition(field, filter_pb2.OPERATOR_LT, value)
        return self
    
    def filter_lte(self, field: str, value: Any) -> 'QueryBuilder':
        """Add less-than-or-equal filter: field <= value"""
        self._add_condition(field, filter_pb2.OPERATOR_LTE, value)
        return self
    
    def filter_gt(self, field: str, value: Any) -> 'QueryBuilder':
        """Add greater-than filter: field > value"""
        self._add_condition(field, filter_pb2.OPERATOR_GT, value)
        return self
    
    def filter_gte(self, field: str, value: Any) -> 'QueryBuilder':
        """Add greater-than-or-equal filter: field >= value"""
        self._add_condition(field, filter_pb2.OPERATOR_GTE, value)
        return self
    
    def filter_in(self, field: str, values: List[Any]) -> 'QueryBuilder':
        """Add IN filter: field IN (values)"""
        proto_values = [self._to_proto_value(v) for v in values]
        self._filters.append(filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field=field,
                operator=filter_pb2.OPERATOR_IN,
                values=proto_values
            )
        ))
        return self
    
    def filter_not_in(self, field: str, values: List[Any]) -> 'QueryBuilder':
        """Add NOT IN filter: field NOT IN (values)"""
        proto_values = [self._to_proto_value(v) for v in values]
        self._filters.append(filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field=field,
                operator=filter_pb2.OPERATOR_NOT_IN,
                values=proto_values
            )
        ))
        return self
    
    def filter_contains(self, field: str, value: str, case_sensitive: bool = True) -> 'QueryBuilder':
        """Add substring filter: field CONTAINS value"""
        self._filters.append(filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field=field,
                operator=filter_pb2.OPERATOR_CONTAINS,
                value=Value(string_value=value),
                case_sensitive=case_sensitive
            )
        ))
        return self
    
    def filter_starts_with(self, field: str, value: str) -> 'QueryBuilder':
        """Add prefix filter: field STARTS WITH value"""
        self._add_condition(field, filter_pb2.OPERATOR_STARTS_WITH, value)
        return self
    
    def filter_ends_with(self, field: str, value: str) -> 'QueryBuilder':
        """Add suffix filter: field ENDS WITH value"""
        self._add_condition(field, filter_pb2.OPERATOR_ENDS_WITH, value)
        return self
    
    def filter_matches(self, field: str, pattern: str) -> 'QueryBuilder':
        """Add regex filter: field MATCHES pattern"""
        self._add_condition(field, filter_pb2.OPERATOR_MATCHES, pattern)
        return self
    
    def filter_is_null(self, field: str) -> 'QueryBuilder':
        """Add NULL check: field IS NULL"""
        self._filters.append(filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field=field,
                operator=filter_pb2.OPERATOR_IS_NULL
            )
        ))
        return self
    
    def filter_is_not_null(self, field: str) -> 'QueryBuilder':
        """Add NOT NULL check: field IS NOT NULL"""
        self._filters.append(filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field=field,
                operator=filter_pb2.OPERATOR_IS_NOT_NULL
            )
        ))
        return self
    
    def filter_array_contains(self, field: str, value: Any) -> 'QueryBuilder':
        """Add array contains: value IN field"""
        self._add_condition(field, filter_pb2.OPERATOR_ARRAY_CONTAINS, value)
        return self
    
    # Sorting methods
    
    def sort_asc(self, field: str, nulls: str = "default") -> 'QueryBuilder':
        """Add ascending sort"""
        self._add_sort(field, sort_pb2.SORT_DIRECTION_ASC, nulls)
        return self
    
    def sort_desc(self, field: str, nulls: str = "default") -> 'QueryBuilder':
        """Add descending sort"""
        self._add_sort(field, sort_pb2.SORT_DIRECTION_DESC, nulls)
        return self
    
    # Projection methods
    
    def include(self, *fields: str) -> 'QueryBuilder':
        """Include only specified fields in result"""
        self._projection = query_pb2.Projection(include=list(fields))
        return self
    
    def exclude(self, *fields: str) -> 'QueryBuilder':
        """Exclude specified fields from result"""
        self._projection = query_pb2.Projection(exclude=list(fields))
        return self
    
    # Pagination methods
    
    def limit(self, page_size: int) -> 'QueryBuilder':
        """Set page size"""
        if not self._pagination:
            self._pagination = pagination_pb2.Pagination()
        self._pagination.page_size = page_size
        return self
    
    def cursor(self, cursor: str) -> 'QueryBuilder':
        """Set pagination cursor"""
        if not self._pagination:
            self._pagination = pagination_pb2.Pagination()
        self._pagination.cursor = cursor
        return self
    
    def offset(self, offset: int) -> 'QueryBuilder':
        """Set pagination offset (not recommended, use cursor instead)"""
        if not self._pagination:
            self._pagination = pagination_pb2.Pagination()
        self._pagination.offset = offset
        return self
    
    # Search methods
    
    def search_fulltext(self, query: str, fields: List[str] = None, 
                       min_score: float = 0.0) -> 'QueryBuilder':
        """Add full-text search"""
        self._search = search_pb2.Search(
            query=query,
            type=search_pb2.SEARCH_TYPE_FULL_TEXT,
            fields=fields or [],
            min_score=min_score
        )
        return self
    
    def search_semantic(self, query: str = None, embedding: List[float] = None,
                       vector_field: str = "embedding", 
                       min_score: float = 0.0) -> 'QueryBuilder':
        """Add semantic vector search"""
        self._search = search_pb2.Search(
            query=query or "",
            type=search_pb2.SEARCH_TYPE_SEMANTIC,
            vector_field=vector_field,
            embedding=embedding or [],
            min_score=min_score
        )
        return self
    
    # Aggregation methods
    
    def group_by(self, *fields: str) -> 'QueryBuilder':
        """Set grouping fields"""
        if not self._aggregation:
            self._aggregation = aggregation_pb2.Aggregation()
        self._aggregation.group_by.extend(fields)
        return self
    
    def count(self, alias: str = "count") -> 'QueryBuilder':
        """Add COUNT aggregate"""
        return self._add_aggregate(
            aggregation_pb2.AGGREGATE_FUNCTION_COUNT,
            alias=alias
        )
    
    def sum(self, field: str, alias: str = None) -> 'QueryBuilder':
        """Add SUM aggregate"""
        return self._add_aggregate(
            aggregation_pb2.AGGREGATE_FUNCTION_SUM,
            field=field,
            alias=alias or f"sum_{field}"
        )
    
    def avg(self, field: str, alias: str = None) -> 'QueryBuilder':
        """Add AVG aggregate"""
        return self._add_aggregate(
            aggregation_pb2.AGGREGATE_FUNCTION_AVG,
            field=field,
            alias=alias or f"avg_{field}"
        )
    
    def min(self, field: str, alias: str = None) -> 'QueryBuilder':
        """Add MIN aggregate"""
        return self._add_aggregate(
            aggregation_pb2.AGGREGATE_FUNCTION_MIN,
            field=field,
            alias=alias or f"min_{field}"
        )
    
    def max(self, field: str, alias: str = None) -> 'QueryBuilder':
        """Add MAX aggregate"""
        return self._add_aggregate(
            aggregation_pb2.AGGREGATE_FUNCTION_MAX,
            field=field,
            alias=alias or f"max_{field}"
        )
    
    # Options methods
    
    def timeout(self, timeout_ms: int) -> 'QueryBuilder':
        """Set query timeout in milliseconds"""
        if not self._options:
            self._options = query_pb2.QueryOptions()
        self._options.timeout_ms = timeout_ms
        return self
    
    def explain(self, enabled: bool = True) -> 'QueryBuilder':
        """Enable query plan explanation"""
        if not self._options:
            self._options = query_pb2.QueryOptions()
        self._options.explain = enabled
        return self
    
    def count_total(self, enabled: bool = True) -> 'QueryBuilder':
        """Enable total count (expensive!)"""
        if not self._options:
            self._options = query_pb2.QueryOptions()
        self._options.count_total = enabled
        return self
    
    def consistency(self, level: str = "strong") -> 'QueryBuilder':
        """Set consistency level: eventual, strong, or linearizable"""
        if not self._options:
            self._options = query_pb2.QueryOptions()
        
        level_map = {
            "eventual": query_pb2.CONSISTENCY_LEVEL_EVENTUAL,
            "strong": query_pb2.CONSISTENCY_LEVEL_STRONG,
            "linearizable": query_pb2.CONSISTENCY_LEVEL_LINEARIZABLE
        }
        self._options.consistency = level_map.get(level, query_pb2.CONSISTENCY_LEVEL_STRONG)
        return self
    
    # Build method
    
    def build(self) -> query_pb2.Query:
        """Build final Query protobuf message"""
        query = query_pb2.Query(entity=self._entity)
        
        # Combine filters with AND
        if self._filters:
            if len(self._filters) == 1:
                query.filter.CopyFrom(self._filters[0])
            else:
                query.filter.CopyFrom(filter_pb2.Filter(
                    and_=filter_pb2.AndFilter(conditions=self._filters)
                ))
        
        # Add sorts
        if self._sorts:
            query.sort.extend(self._sorts)
        
        # Add projection
        if self._projection:
            query.projection.CopyFrom(self._projection)
        
        # Add pagination
        if self._pagination:
            query.pagination.CopyFrom(self._pagination)
        elif not self._aggregation:  # Default pagination if not aggregating
            query.pagination.CopyFrom(pagination_pb2.Pagination(page_size=50))
        
        # Add aggregation
        if self._aggregation:
            query.aggregation.CopyFrom(self._aggregation)
        
        # Add search
        if self._search:
            query.search.CopyFrom(self._search)
        
        # Add relations
        if self._relations:
            query.relation.extend(self._relations)
        
        # Add options
        if self._options:
            query.options.CopyFrom(self._options)
        
        return query
    
    # Helper methods
    
    def _add_condition(self, field: str, operator: int, value: Any):
        """Add a condition filter"""
        self._filters.append(filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field=field,
                operator=operator,
                value=self._to_proto_value(value)
            )
        ))
    
    def _add_sort(self, field: str, direction: int, nulls: str):
        """Add a sort specification"""
        sort = sort_pb2.Sort(field=field, direction=direction)
        
        if nulls == "first":
            sort.nulls = sort_pb2.NULL_ORDERING_NULLS_FIRST
        elif nulls == "last":
            sort.nulls = sort_pb2.NULL_ORDERING_NULLS_LAST
        
        self._sorts.append(sort)
    
    def _add_aggregate(self, function: int, field: str = None, alias: str = None):
        """Add an aggregate function"""
        if not self._aggregation:
            self._aggregation = aggregation_pb2.Aggregation()
        
        agg = aggregation_pb2.Aggregate(
            function=function,
            alias=alias or "result"
        )
        
        if field:
            agg.field = field
        
        self._aggregation.aggregates.append(agg)
        return self
    
    @staticmethod
    def _to_proto_value(value: Any) -> Value:
        """Convert Python value to protobuf Value"""
        if isinstance(value, bool):
            return Value(bool_value=value)
        elif isinstance(value, int):
            return Value(number_value=value)
        elif isinstance(value, float):
            return Value(number_value=value)
        elif isinstance(value, str):
            return Value(string_value=value)
        elif isinstance(value, datetime):
            return Value(string_value=value.isoformat() + "Z")
        elif value is None:
            return Value(null_value=0)
        else:
            return Value(string_value=str(value))


# Example usage
if __name__ == "__main__":
    # Example 1: Simple filter query
    query1 = (QueryBuilder("users")
        .filter_eq("status", "active")
        .filter_gte("age", 18)
        .sort_desc("created_at")
        .limit(50)
        .build())
    
    print("Example 1: Simple filter")
    print(f"Entity: {query1.entity}")
    print(f"Filters: {len(query1.filter.and_.conditions)} conditions")
    print()
    
    # Example 2: Aggregation query
    query2 = (QueryBuilder("orders")
        .filter_eq("status", "completed")
        .group_by("customer_id")
        .count("order_count")
        .sum("total_amount", "revenue")
        .avg("total_amount", "avg_order_value")
        .build())
    
    print("Example 2: Aggregation")
    print(f"Group by: {', '.join(query2.aggregation.group_by)}")
    print(f"Aggregates: {len(query2.aggregation.aggregates)}")
    print()
    
    # Example 3: Search query
    query3 = (QueryBuilder("products")
        .search_fulltext("wireless headphones", ["name", "description"])
        .filter_gt("price", 50)
        .filter_eq("in_stock", True)
        .sort_desc("popularity_score")
        .limit(20)
        .build())
    
    print("Example 3: Full-text search")
    print(f"Search: {query3.search.query}")
    print(f"Fields: {', '.join(query3.search.fields)}")
    print()
    
    print("✓ All query builder examples completed!")
