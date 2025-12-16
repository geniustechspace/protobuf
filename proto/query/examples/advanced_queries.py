#!/usr/bin/env python3
"""
Advanced Query Examples - Complex scenarios

Demonstrates:
- Complex boolean logic (deeply nested AND/OR/NOT)
- Multi-level aggregations with HAVING clauses
- Explicit joins across entities
- Hybrid search (full-text + semantic)
- Window functions simulation
- Subquery patterns
"""

from datetime import datetime, timedelta
from google.protobuf.struct_pb2 import Value
from geniustechspace.query.api.v1 import (
    query_pb2,
    filter_pb2,
    sort_pb2,
    aggregation_pb2,
    search_pb2,
    relation_pb2,
    pagination_pb2
)


def example_1_complex_boolean_logic():
    """
    Find users who match complex criteria:
    (status='active' AND (role='admin' OR role='owner'))
    OR (status='trial' AND created_at > 30 days ago AND tags contains 'vip')
    """
    thirty_days_ago = (datetime.utcnow() - timedelta(days=30)).isoformat() + "Z"
    
    query = query_pb2.Query(
        entity="users",
        filter=filter_pb2.Filter(
            or_=filter_pb2.OrFilter(
                conditions=[
                    # Branch 1: Active admins/owners
                    filter_pb2.Filter(
                        and_=filter_pb2.AndFilter(
                            conditions=[
                                filter_pb2.Filter(
                                    condition=filter_pb2.Condition(
                                        field="status",
                                        operator=filter_pb2.OPERATOR_EQ,
                                        value=Value(string_value="active")
                                    )
                                ),
                                filter_pb2.Filter(
                                    or_=filter_pb2.OrFilter(
                                        conditions=[
                                            filter_pb2.Filter(
                                                condition=filter_pb2.Condition(
                                                    field="role",
                                                    operator=filter_pb2.OPERATOR_EQ,
                                                    value=Value(string_value="admin")
                                                )
                                            ),
                                            filter_pb2.Filter(
                                                condition=filter_pb2.Condition(
                                                    field="role",
                                                    operator=filter_pb2.OPERATOR_EQ,
                                                    value=Value(string_value="owner")
                                                )
                                            )
                                        ]
                                    )
                                )
                            ]
                        )
                    ),
                    # Branch 2: Recent VIP trials
                    filter_pb2.Filter(
                        and_=filter_pb2.AndFilter(
                            conditions=[
                                filter_pb2.Filter(
                                    condition=filter_pb2.Condition(
                                        field="status",
                                        operator=filter_pb2.OPERATOR_EQ,
                                        value=Value(string_value="trial")
                                    )
                                ),
                                filter_pb2.Filter(
                                    condition=filter_pb2.Condition(
                                        field="created_at",
                                        operator=filter_pb2.OPERATOR_GTE,
                                        value=Value(string_value=thirty_days_ago)
                                    )
                                ),
                                filter_pb2.Filter(
                                    condition=filter_pb2.Condition(
                                        field="tags",
                                        operator=filter_pb2.OPERATOR_ARRAY_CONTAINS,
                                        value=Value(string_value="vip")
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        ),
        pagination=pagination_pb2.Pagination(page_size=100)
    )
    
    print("Example 1: Complex boolean logic")
    print("Logic: (active admins/owners) OR (recent VIP trials)")
    print("Nesting: 3 levels deep\n")
    return query


def example_2_negation_filter():
    """
    Find products NOT matching certain criteria:
    NOT (discontinued OR out_of_stock OR (price < 10 AND quality = 'low'))
    """
    query = query_pb2.Query(
        entity="products",
        filter=filter_pb2.Filter(
            not_=filter_pb2.NotFilter(
                condition=filter_pb2.Filter(
                    or_=filter_pb2.OrFilter(
                        conditions=[
                            # Discontinued
                            filter_pb2.Filter(
                                condition=filter_pb2.Condition(
                                    field="discontinued",
                                    operator=filter_pb2.OPERATOR_EQ,
                                    value=Value(bool_value=True)
                                )
                            ),
                            # Out of stock
                            filter_pb2.Filter(
                                condition=filter_pb2.Condition(
                                    field="stock_quantity",
                                    operator=filter_pb2.OPERATOR_EQ,
                                    value=Value(number_value=0)
                                )
                            ),
                            # Cheap and low quality
                            filter_pb2.Filter(
                                and_=filter_pb2.AndFilter(
                                    conditions=[
                                        filter_pb2.Filter(
                                            condition=filter_pb2.Condition(
                                                field="price",
                                                operator=filter_pb2.OPERATOR_LT,
                                                value=Value(number_value=10)
                                            )
                                        ),
                                        filter_pb2.Filter(
                                            condition=filter_pb2.Condition(
                                                field="quality",
                                                operator=filter_pb2.OPERATOR_EQ,
                                                value=Value(string_value="low")
                                            )
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                )
            )
        ),
        pagination=pagination_pb2.Pagination(page_size=100)
    )
    
    print("Example 2: Negation filter")
    print("Logic: NOT (discontinued OR out_of_stock OR cheap_low_quality)")
    print("Result: High-quality available products\n")
    return query


def example_3_multi_level_aggregation():
    """
    Sales report with multiple aggregations and HAVING clause:
    Group by category, subcategory
    Show categories with >$10k revenue
    """
    query = query_pb2.Query(
        entity="sales",
        filter=filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field="status",
                operator=filter_pb2.OPERATOR_EQ,
                value=Value(string_value="completed")
            )
        ),
        aggregation=aggregation_pb2.Aggregation(
            group_by=["category", "subcategory"],
            aggregates=[
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_COUNT,
                    alias="transaction_count"
                ),
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_SUM,
                    field="amount",
                    alias="total_revenue"
                ),
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_AVG,
                    field="amount",
                    alias="avg_transaction"
                ),
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_MIN,
                    field="amount",
                    alias="min_sale"
                ),
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_MAX,
                    field="amount",
                    alias="max_sale"
                ),
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_COUNT_DISTINCT,
                    field="customer_id",
                    alias="unique_customers"
                )
            ],
            having=filter_pb2.Filter(
                and_=filter_pb2.AndFilter(
                    conditions=[
                        # Revenue > $10k
                        filter_pb2.Filter(
                            condition=filter_pb2.Condition(
                                field="total_revenue",
                                operator=filter_pb2.OPERATOR_GTE,
                                value=Value(number_value=10000)
                            )
                        ),
                        # At least 100 transactions
                        filter_pb2.Filter(
                            condition=filter_pb2.Condition(
                                field="transaction_count",
                                operator=filter_pb2.OPERATOR_GTE,
                                value=Value(number_value=100)
                            )
                        )
                    ]
                )
            )
        ),
        sort=[
            sort_pb2.Sort(
                field="total_revenue",
                direction=sort_pb2.SORT_DIRECTION_DESC
            )
        ]
    )
    
    print("Example 3: Multi-level aggregation with HAVING")
    print("Group by: category, subcategory")
    print("Having: revenue ≥ $10k AND count ≥ 100")
    print("Aggregates: 6 functions\n")
    return query


def example_4_percentile_aggregation():
    """Calculate response time percentiles for API endpoints"""
    query = query_pb2.Query(
        entity="api_logs",
        filter=filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field="timestamp",
                operator=filter_pb2.OPERATOR_GTE,
                value=Value(string_value=(datetime.utcnow() - timedelta(hours=1)).isoformat() + "Z")
            )
        ),
        aggregation=aggregation_pb2.Aggregation(
            group_by=["endpoint", "method"],
            aggregates=[
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_COUNT,
                    alias="request_count"
                ),
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_PERCENTILE,
                    field="response_time_ms",
                    percentile=50.0,
                    alias="p50"
                ),
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_PERCENTILE,
                    field="response_time_ms",
                    percentile=95.0,
                    alias="p95"
                ),
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_PERCENTILE,
                    field="response_time_ms",
                    percentile=99.0,
                    alias="p99"
                ),
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_MAX,
                    field="response_time_ms",
                    alias="max_latency"
                )
            ]
        ),
        sort=[
            sort_pb2.Sort(
                field="p99",
                direction=sort_pb2.SORT_DIRECTION_DESC
            )
        ]
    )
    
    print("Example 4: Percentile aggregation (SLA monitoring)")
    print("Timeframe: Last 1 hour")
    print("Metrics: p50, p95, p99, max latency\n")
    return query


def example_5_explicit_join():
    """
    Join orders with customers and products:
    Orders INNER JOIN Customers ON customer_id
         LEFT JOIN Products ON product_id
    """
    query = query_pb2.Query(
        entity="orders",
        filter=filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field="status",
                operator=filter_pb2.OPERATOR_IN,
                values=[
                    Value(string_value="completed"),
                    Value(string_value="shipped")
                ]
            )
        ),
        relation=[
            # INNER JOIN customers
            relation_pb2.Relation(
                entity="customers",
                alias="customer",
                type=relation_pb2.JOIN_TYPE_INNER,
                on=filter_pb2.Filter(
                    condition=filter_pb2.Condition(
                        field="customer_id",
                        operator=filter_pb2.OPERATOR_EQ,
                        value=Value(string_value="customer.id")  # Field reference
                    )
                ),
                eager=True
            ),
            # LEFT JOIN products
            relation_pb2.Relation(
                entity="products",
                alias="product",
                type=relation_pb2.JOIN_TYPE_LEFT_OUTER,
                on=filter_pb2.Filter(
                    condition=filter_pb2.Condition(
                        field="product_id",
                        operator=filter_pb2.OPERATOR_EQ,
                        value=Value(string_value="product.id")
                    )
                ),
                eager=True
            )
        ],
        projection=query_pb2.Projection(
            include=[
                "order_id",
                "total_amount",
                "customer.name",
                "customer.email",
                "product.name",
                "product.price"
            ]
        ),
        sort=[
            sort_pb2.Sort(
                field="created_at",
                direction=sort_pb2.SORT_DIRECTION_DESC
            )
        ],
        pagination=pagination_pb2.Pagination(page_size=50)
    )
    
    print("Example 5: Explicit joins")
    print("Joins: orders → customers (INNER), orders → products (LEFT)")
    print("Projection: Denormalized result\n")
    return query


def example_6_hybrid_search():
    """
    Hybrid search combining full-text and semantic:
    Match "wireless headphones" in text OR similar by embedding
    """
    # Simulated embedding vector (384 dimensions)
    query_embedding = [0.123] * 384
    
    query = query_pb2.Query(
        entity="products",
        filter=filter_pb2.Filter(
            and_=filter_pb2.AndFilter(
                conditions=[
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="status",
                            operator=filter_pb2.OPERATOR_EQ,
                            value=Value(string_value="active")
                        )
                    ),
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="stock_quantity",
                            operator=filter_pb2.OPERATOR_GT,
                            value=Value(number_value=0)
                        )
                    )
                ]
            )
        ),
        search=search_pb2.Search(
            query="wireless headphones",
            type=search_pb2.SEARCH_TYPE_HYBRID,
            fields=["name", "description", "tags"],
            vector_field="description_embedding",
            embedding=query_embedding,
            min_score=0.5,
            boost={
                "name": 2.0,  # Boost title matches
                "description": 1.0,
                "tags": 1.5
            }
        ),
        pagination=pagination_pb2.Pagination(page_size=20)
    )
    
    print("Example 6: Hybrid search")
    print("Text: 'wireless headphones'")
    print("Vector: 384-dim embedding")
    print("Combines: Full-text + semantic similarity\n")
    return query


def example_7_time_series_bucketing():
    """
    Time-series analysis with hourly buckets:
    Simulate time bucketing using aggregation
    """
    seven_days_ago = (datetime.utcnow() - timedelta(days=7)).isoformat() + "Z"
    
    query = query_pb2.Query(
        entity="events",
        filter=filter_pb2.Filter(
            and_=filter_pb2.AndFilter(
                conditions=[
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="timestamp",
                            operator=filter_pb2.OPERATOR_GTE,
                            value=Value(string_value=seven_days_ago)
                        )
                    ),
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="event_type",
                            operator=filter_pb2.OPERATOR_EQ,
                            value=Value(string_value="page_view")
                        )
                    )
                ]
            )
        ),
        aggregation=aggregation_pb2.Aggregation(
            group_by=["date_trunc_hour(timestamp)", "page_url"],  # Custom function
            aggregates=[
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_COUNT,
                    alias="page_views"
                ),
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_COUNT_DISTINCT,
                    field="user_id",
                    alias="unique_visitors"
                )
            ]
        ),
        sort=[
            sort_pb2.Sort(
                field="date_trunc_hour(timestamp)",
                direction=sort_pb2.SORT_DIRECTION_ASC
            )
        ]
    )
    
    print("Example 7: Time-series bucketing")
    print("Timeframe: Last 7 days")
    print("Granularity: Hourly")
    print("Metrics: Page views, Unique visitors\n")
    return query


def example_8_variance_stddev():
    """Statistical analysis with variance and standard deviation"""
    query = query_pb2.Query(
        entity="sensor_readings",
        filter=filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field="timestamp",
                operator=filter_pb2.OPERATOR_GTE,
                value=Value(string_value=(datetime.utcnow() - timedelta(hours=24)).isoformat() + "Z")
            )
        ),
        aggregation=aggregation_pb2.Aggregation(
            group_by=["sensor_id", "location"],
            aggregates=[
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_COUNT,
                    alias="reading_count"
                ),
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_AVG,
                    field="temperature",
                    alias="avg_temp"
                ),
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_STDDEV,
                    field="temperature",
                    alias="temp_stddev"
                ),
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_VARIANCE,
                    field="temperature",
                    alias="temp_variance"
                ),
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_MIN,
                    field="temperature",
                    alias="min_temp"
                ),
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_MAX,
                    field="temperature",
                    alias="max_temp"
                )
            ],
            having=filter_pb2.Filter(
                condition=filter_pb2.Condition(
                    field="temp_stddev",
                    operator=filter_pb2.OPERATOR_GT,
                    value=Value(number_value=5.0)  # High variability
                )
            )
        ),
        sort=[
            sort_pb2.Sort(
                field="temp_stddev",
                direction=sort_pb2.SORT_DIRECTION_DESC
            )
        ]
    )
    
    print("Example 8: Statistical analysis")
    print("Metrics: Avg, StdDev, Variance, Min, Max")
    print("Having: StdDev > 5 (anomaly detection)\n")
    return query


def example_9_case_insensitive_search():
    """Case-insensitive pattern matching across multiple fields"""
    query = query_pb2.Query(
        entity="users",
        filter=filter_pb2.Filter(
            or_=filter_pb2.OrFilter(
                conditions=[
                    # Email contains domain (case-insensitive)
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="email",
                            operator=filter_pb2.OPERATOR_CONTAINS,
                            value=Value(string_value="@ACME.COM"),
                            case_sensitive=False
                        )
                    ),
                    # Name starts with prefix (case-insensitive)
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="profile.name",
                            operator=filter_pb2.OPERATOR_STARTS_WITH,
                            value=Value(string_value="john"),
                            case_sensitive=False
                        )
                    ),
                    # Company contains keyword (case-insensitive)
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="company.name",
                            operator=filter_pb2.OPERATOR_CONTAINS,
                            value=Value(string_value="tech"),
                            case_sensitive=False
                        )
                    )
                ]
            )
        ),
        pagination=pagination_pb2.Pagination(page_size=100)
    )
    
    print("Example 9: Case-insensitive search")
    print("Fields: email, name, company")
    print("Matches: Any of the patterns\n")
    return query


def example_10_regex_pattern_matching():
    """Advanced regex pattern matching"""
    query = query_pb2.Query(
        entity="documents",
        filter=filter_pb2.Filter(
            and_=filter_pb2.AndFilter(
                conditions=[
                    # Email format validation
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="contact_email",
                            operator=filter_pb2.OPERATOR_MATCHES,
                            value=Value(string_value=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
                        )
                    ),
                    # Phone format (US)
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="phone",
                            operator=filter_pb2.OPERATOR_MATCHES,
                            value=Value(string_value=r"^\+1-\d{3}-\d{3}-\d{4}$")
                        )
                    ),
                    # Document ID format
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="document_id",
                            operator=filter_pb2.OPERATOR_MATCHES,
                            value=Value(string_value=r"^DOC-\d{6}-[A-Z]{3}$")
                        )
                    )
                ]
            )
        ),
        pagination=pagination_pb2.Pagination(page_size=50)
    )
    
    print("Example 10: Regex pattern matching")
    print("Patterns: Email, Phone (US), Document ID")
    print("Use case: Data validation queries\n")
    return query


def main():
    """Run all advanced examples"""
    print("=" * 60)
    print("ADVANCED QUERY EXAMPLES")
    print("=" * 60)
    print()
    
    examples = [
        example_1_complex_boolean_logic,
        example_2_negation_filter,
        example_3_multi_level_aggregation,
        example_4_percentile_aggregation,
        example_5_explicit_join,
        example_6_hybrid_search,
        example_7_time_series_bucketing,
        example_8_variance_stddev,
        example_9_case_insensitive_search,
        example_10_regex_pattern_matching
    ]
    
    for example_func in examples:
        try:
            result = example_func()
            print("✓ Query constructed successfully")
            print("-" * 60)
            print()
        except Exception as e:
            print(f"✗ Error: {e}")
            print("-" * 60)
            print()
    
    print("=" * 60)
    print("All advanced examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
