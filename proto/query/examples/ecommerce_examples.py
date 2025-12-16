#!/usr/bin/env python3
"""
E-commerce Query Examples

Real-world scenarios for online retail:
- Product search and filtering
- Order management
- Customer analytics
- Inventory queries
- Sales reports
"""

from datetime import datetime, timedelta
from google.protobuf.struct_pb2 import Value
from geniustechspace.query.api.v1 import (
    query_pb2,
    filter_pb2,
    sort_pb2,
    aggregation_pb2,
    search_pb2,
    pagination_pb2
)


def example_1_product_search():
    """Search products with multiple filters"""
    query = query_pb2.Query(
        entity="products",
        filter=filter_pb2.Filter(
            and_=filter_pb2.AndFilter(
                conditions=[
                    # Category filter
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="category",
                            operator=filter_pb2.OPERATOR_EQ,
                            value=Value(string_value="electronics")
                        )
                    ),
                    # Price range
                    filter_pb2.Filter(
                        and_=filter_pb2.AndFilter(
                            conditions=[
                                filter_pb2.Filter(
                                    condition=filter_pb2.Condition(
                                        field="price",
                                        operator=filter_pb2.OPERATOR_GTE,
                                        value=Value(number_value=100)
                                    )
                                ),
                                filter_pb2.Filter(
                                    condition=filter_pb2.Condition(
                                        field="price",
                                        operator=filter_pb2.OPERATOR_LTE,
                                        value=Value(number_value=500)
                                    )
                                )
                            ]
                        )
                    ),
                    # In stock
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="stock_quantity",
                            operator=filter_pb2.OPERATOR_GT,
                            value=Value(number_value=0)
                        )
                    ),
                    # Active products only
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="status",
                            operator=filter_pb2.OPERATOR_EQ,
                            value=Value(string_value="active")
                        )
                    )
                ]
            )
        ),
        sort=[
            sort_pb2.Sort(
                field="popularity_score",
                direction=sort_pb2.SORT_DIRECTION_DESC
            )
        ],
        pagination=pagination_pb2.Pagination(page_size=24)  # Grid layout: 4x6
    )
    
    print("Example 1: Product search with filters")
    print("Category: electronics")
    print("Price: $100-$500")
    print("In stock: Yes")
    print("Sort: Popularity DESC\n")
    return query


def example_2_order_history():
    """Get customer's recent orders with details"""
    customer_id = "cust_abc123"
    
    query = query_pb2.Query(
        entity="orders",
        filter=filter_pb2.Filter(
            and_=filter_pb2.AndFilter(
                conditions=[
                    # Customer filter
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="customer_id",
                            operator=filter_pb2.OPERATOR_EQ,
                            value=Value(string_value=customer_id)
                        )
                    ),
                    # Not cancelled
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="status",
                            operator=filter_pb2.OPERATOR_NE,
                            value=Value(string_value="cancelled")
                        )
                    )
                ]
            )
        ),
        projection=query_pb2.Projection(
            include=[
                "order_id",
                "order_number",
                "total_amount",
                "status",
                "created_at",
                "items.*",  # All order items
                "shipping.tracking_number"
            ]
        ),
        sort=[
            sort_pb2.Sort(
                field="created_at",
                direction=sort_pb2.SORT_DIRECTION_DESC
            )
        ],
        pagination=pagination_pb2.Pagination(page_size=10)
    )
    
    print("Example 2: Customer order history")
    print(f"Customer: {customer_id}")
    print("Excluding cancelled orders")
    print("Sort: Newest first\n")
    return query


def example_3_low_stock_alert():
    """Find products with low inventory"""
    query = query_pb2.Query(
        entity="products",
        filter=filter_pb2.Filter(
            and_=filter_pb2.AndFilter(
                conditions=[
                    # Low stock threshold
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="stock_quantity",
                            operator=filter_pb2.OPERATOR_LTE,
                            value=Value(number_value=10)
                        )
                    ),
                    # Not out of stock
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="stock_quantity",
                            operator=filter_pb2.OPERATOR_GT,
                            value=Value(number_value=0)
                        )
                    ),
                    # Active products only
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="status",
                            operator=filter_pb2.OPERATOR_EQ,
                            value=Value(string_value="active")
                        )
                    )
                ]
            )
        ),
        sort=[
            sort_pb2.Sort(
                field="stock_quantity",
                direction=sort_pb2.SORT_DIRECTION_ASC
            )
        ],
        pagination=pagination_pb2.Pagination(page_size=100)
    )
    
    print("Example 3: Low stock alert")
    print("Stock: 1-10 units")
    print("Status: Active")
    print("Sort: Lowest stock first\n")
    return query


def example_4_daily_sales_report():
    """Aggregate daily sales by category"""
    today = datetime.utcnow().date().isoformat()
    
    query = query_pb2.Query(
        entity="orders",
        filter=filter_pb2.Filter(
            and_=filter_pb2.AndFilter(
                conditions=[
                    # Today's orders
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="created_at",
                            operator=filter_pb2.OPERATOR_GTE,
                            value=Value(string_value=f"{today}T00:00:00Z")
                        )
                    ),
                    # Completed only
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="status",
                            operator=filter_pb2.OPERATOR_IN,
                            values=[
                                Value(string_value="completed"),
                                Value(string_value="shipped")
                            ]
                        )
                    )
                ]
            )
        ),
        aggregation=aggregation_pb2.Aggregation(
            group_by=["category"],
            aggregates=[
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_COUNT,
                    alias="order_count"
                ),
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_SUM,
                    field="total_amount",
                    alias="total_revenue"
                ),
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_AVG,
                    field="total_amount",
                    alias="avg_order_value"
                )
            ]
        ),
        sort=[
            sort_pb2.Sort(
                field="total_revenue",
                direction=sort_pb2.SORT_DIRECTION_DESC
            )
        ]
    )
    
    print("Example 4: Daily sales report by category")
    print(f"Date: {today}")
    print("Metrics: Count, Revenue, AOV")
    print("Group by: Category\n")
    return query


def example_5_customer_lifetime_value():
    """Calculate customer lifetime value (top spenders)"""
    query = query_pb2.Query(
        entity="orders",
        filter=filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field="status",
                operator=filter_pb2.OPERATOR_IN,
                values=[
                    Value(string_value="completed"),
                    Value(string_value="shipped"),
                    Value(string_value="delivered")
                ]
            )
        ),
        aggregation=aggregation_pb2.Aggregation(
            group_by=["customer_id"],
            aggregates=[
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_COUNT,
                    alias="order_count"
                ),
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_SUM,
                    field="total_amount",
                    alias="lifetime_value"
                ),
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_AVG,
                    field="total_amount",
                    alias="avg_order_value"
                )
            ],
            having=filter_pb2.Filter(
                condition=filter_pb2.Condition(
                    field="order_count",
                    operator=filter_pb2.OPERATOR_GTE,
                    value=Value(number_value=5)
                )
            )
        ),
        sort=[
            sort_pb2.Sort(
                field="lifetime_value",
                direction=sort_pb2.SORT_DIRECTION_DESC
            )
        ],
        pagination=pagination_pb2.Pagination(page_size=100)
    )
    
    print("Example 5: Customer lifetime value")
    print("Filter: Completed orders only")
    print("Having: At least 5 orders")
    print("Sort: Highest LTV first\n")
    return query


def example_6_product_recommendations():
    """Find similar products using semantic search"""
    product_embedding = [0.123, -0.456, 0.789] * 128  # 384-dim example
    
    query = query_pb2.Query(
        entity="products",
        filter=filter_pb2.Filter(
            and_=filter_pb2.AndFilter(
                conditions=[
                    # In stock
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="stock_quantity",
                            operator=filter_pb2.OPERATOR_GT,
                            value=Value(number_value=0)
                        )
                    ),
                    # Active
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="status",
                            operator=filter_pb2.OPERATOR_EQ,
                            value=Value(string_value="active")
                        )
                    )
                ]
            )
        ),
        search=search_pb2.Search(
            type=search_pb2.SEARCH_TYPE_SEMANTIC,
            vector_field="description_embedding",
            embedding=product_embedding,
            min_score=0.7
        ),
        pagination=pagination_pb2.Pagination(page_size=10)
    )
    
    print("Example 6: Product recommendations (semantic search)")
    print("Method: Vector similarity")
    print("Min similarity: 0.7")
    print("Result: Similar products\n")
    return query


def example_7_abandoned_carts():
    """Find abandoned shopping carts (potential recovery)"""
    cutoff_time = (datetime.utcnow() - timedelta(hours=24)).isoformat() + "Z"
    
    query = query_pb2.Query(
        entity="carts",
        filter=filter_pb2.Filter(
            and_=filter_pb2.AndFilter(
                conditions=[
                    # Not checked out
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="status",
                            operator=filter_pb2.OPERATOR_EQ,
                            value=Value(string_value="active")
                        )
                    ),
                    # Has items
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="item_count",
                            operator=filter_pb2.OPERATOR_GT,
                            value=Value(number_value=0)
                        )
                    ),
                    # Not updated in last 24h
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="updated_at",
                            operator=filter_pb2.OPERATOR_LT,
                            value=Value(string_value=cutoff_time)
                        )
                    ),
                    # Significant value
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="total_value",
                            operator=filter_pb2.OPERATOR_GTE,
                            value=Value(number_value=50)
                        )
                    )
                ]
            )
        ),
        sort=[
            sort_pb2.Sort(
                field="total_value",
                direction=sort_pb2.SORT_DIRECTION_DESC
            )
        ],
        pagination=pagination_pb2.Pagination(page_size=100)
    )
    
    print("Example 7: Abandoned carts recovery")
    print("Abandoned: >24 hours ago")
    print("Value: >$50")
    print("Sort: Highest value first\n")
    return query


def example_8_seasonal_products():
    """Find seasonal products with tags"""
    query = query_pb2.Query(
        entity="products",
        filter=filter_pb2.Filter(
            and_=filter_pb2.AndFilter(
                conditions=[
                    # Has seasonal tag
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="tags",
                            operator=filter_pb2.OPERATOR_ARRAY_CONTAINS_ANY,
                            values=[
                                Value(string_value="holiday"),
                                Value(string_value="christmas"),
                                Value(string_value="winter")
                            ]
                        )
                    ),
                    # In stock
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
        projection=query_pb2.Projection(
            include=[
                "product_id",
                "name",
                "price",
                "stock_quantity",
                "tags",
                "images.*"
            ]
        ),
        sort=[
            sort_pb2.Sort(
                field="popularity_score",
                direction=sort_pb2.SORT_DIRECTION_DESC
            )
        ],
        pagination=pagination_pb2.Pagination(page_size=50)
    )
    
    print("Example 8: Seasonal products")
    print("Tags: holiday, christmas, winter (any)")
    print("In stock: Yes")
    print("Sort: Most popular\n")
    return query


def example_9_high_value_pending_orders():
    """Monitor high-value orders pending fulfillment"""
    query = query_pb2.Query(
        entity="orders",
        filter=filter_pb2.Filter(
            and_=filter_pb2.AndFilter(
                conditions=[
                    # Pending status
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="status",
                            operator=filter_pb2.OPERATOR_IN,
                            values=[
                                Value(string_value="pending"),
                                Value(string_value="processing")
                            ]
                        )
                    ),
                    # High value
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="total_amount",
                            operator=filter_pb2.OPERATOR_GTE,
                            value=Value(number_value=1000)
                        )
                    ),
                    # Payment confirmed
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="payment_status",
                            operator=filter_pb2.OPERATOR_EQ,
                            value=Value(string_value="confirmed")
                        )
                    )
                ]
            )
        ),
        projection=query_pb2.Projection(
            include=[
                "order_id",
                "order_number",
                "customer.*",
                "total_amount",
                "status",
                "created_at",
                "items.product_id",
                "items.quantity"
            ]
        ),
        sort=[
            sort_pb2.Sort(
                field="created_at",
                direction=sort_pb2.SORT_DIRECTION_ASC  # Oldest first
            )
        ],
        pagination=pagination_pb2.Pagination(page_size=50)
    )
    
    print("Example 9: High-value pending orders")
    print("Status: Pending/Processing")
    print("Value: ≥$1000")
    print("Sort: Oldest first (priority fulfillment)\n")
    return query


def example_10_product_performance_report():
    """Analyze product performance (last 30 days)"""
    thirty_days_ago = (datetime.utcnow() - timedelta(days=30)).isoformat() + "Z"
    
    query = query_pb2.Query(
        entity="order_items",
        filter=filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field="order.created_at",
                operator=filter_pb2.OPERATOR_GTE,
                value=Value(string_value=thirty_days_ago)
            )
        ),
        aggregation=aggregation_pb2.Aggregation(
            group_by=["product_id", "product_name"],
            aggregates=[
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_SUM,
                    field="quantity",
                    alias="units_sold"
                ),
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_SUM,
                    field="line_total",
                    alias="revenue"
                ),
                aggregation_pb2.Aggregate(
                    function=aggregation_pb2.AGGREGATE_FUNCTION_COUNT_DISTINCT,
                    field="order_id",
                    alias="order_count"
                )
            ],
            having=filter_pb2.Filter(
                condition=filter_pb2.Condition(
                    field="units_sold",
                    operator=filter_pb2.OPERATOR_GTE,
                    value=Value(number_value=10)
                )
            )
        ),
        sort=[
            sort_pb2.Sort(
                field="revenue",
                direction=sort_pb2.SORT_DIRECTION_DESC
            )
        ],
        pagination=pagination_pb2.Pagination(page_size=100)
    )
    
    print("Example 10: Product performance (30 days)")
    print("Metrics: Units sold, Revenue, Orders")
    print("Having: At least 10 units sold")
    print("Sort: Highest revenue first\n")
    return query


def main():
    """Run all e-commerce examples"""
    print("=" * 60)
    print("E-COMMERCE QUERY EXAMPLES")
    print("=" * 60)
    print()
    
    examples = [
        example_1_product_search,
        example_2_order_history,
        example_3_low_stock_alert,
        example_4_daily_sales_report,
        example_5_customer_lifetime_value,
        example_6_product_recommendations,
        example_7_abandoned_carts,
        example_8_seasonal_products,
        example_9_high_value_pending_orders,
        example_10_product_performance_report
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
    print("All e-commerce examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
