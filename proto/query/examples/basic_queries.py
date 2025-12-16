#!/usr/bin/env python3
"""
Basic Query Examples - Simple CRUD operations and filtering

Demonstrates:
- Simple equality filters
- Range queries  
- Sorting and pagination
- Field projection
- Common query patterns
"""

from google.protobuf.struct_pb2 import Value
from gen.python.query.api.v1 import (
    query_pb2,
    filter_pb2,
    sort_pb2,
    pagination_pb2
)


def example_1_simple_equality():
    """Find all active users"""
    query = query_pb2.Query(
        entity="users",
        filter=filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field="status",
                operator=filter_pb2.OPERATOR_EQ,
                value=Value(string_value="active")
            )
        ),
        pagination=pagination_pb2.Pagination(page_size=50)
    )
    
    print("Example 1: Find active users")
    print(f"Entity: {query.entity}")
    print(f"Filter: status = 'active'")
    print(f"Page size: {query.pagination.page_size}\n")
    return query


def example_2_range_query():
    """Find users created in the last 30 days"""
    from datetime import datetime, timedelta
    
    thirty_days_ago = (datetime.utcnow() - timedelta(days=30)).isoformat() + "Z"
    
    query = query_pb2.Query(
        entity="users",
        filter=filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field="created_at",
                operator=filter_pb2.OPERATOR_GTE,
                value=Value(string_value=thirty_days_ago)
            )
        ),
        sort=[
            sort_pb2.Sort(
                field="created_at",
                direction=sort_pb2.SORT_DIRECTION_DESC
            )
        ],
        pagination=pagination_pb2.Pagination(page_size=100)
    )
    
    print("Example 2: Users created in last 30 days")
    print(f"Filter: created_at >= '{thirty_days_ago}'")
    print(f"Sort: created_at DESC\n")
    return query


def example_3_multiple_conditions():
    """Find active users with admin role"""
    query = query_pb2.Query(
        entity="users",
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
                            field="role",
                            operator=filter_pb2.OPERATOR_EQ,
                            value=Value(string_value="admin")
                        )
                    )
                ]
            )
        ),
        pagination=pagination_pb2.Pagination(page_size=50)
    )
    
    print("Example 3: Active admin users")
    print("Filter: status = 'active' AND role = 'admin'\n")
    return query


def example_4_in_operator():
    """Find users with specific roles"""
    query = query_pb2.Query(
        entity="users",
        filter=filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field="role",
                operator=filter_pb2.OPERATOR_IN,
                values=[
                    Value(string_value="admin"),
                    Value(string_value="owner"),
                    Value(string_value="manager")
                ]
            )
        ),
        pagination=pagination_pb2.Pagination(page_size=100)
    )
    
    print("Example 4: Users with elevated privileges")
    print("Filter: role IN ('admin', 'owner', 'manager')\n")
    return query


def example_5_field_projection():
    """Get only specific fields (email, name) for active users"""
    query = query_pb2.Query(
        entity="users",
        filter=filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field="status",
                operator=filter_pb2.OPERATOR_EQ,
                value=Value(string_value="active")
            )
        ),
        projection=query_pb2.Projection(
            include=["id", "email", "profile.name", "created_at"]
        ),
        pagination=pagination_pb2.Pagination(page_size=50)
    )
    
    print("Example 5: Project only needed fields")
    print("Fields: id, email, profile.name, created_at")
    print("Benefit: Reduced network overhead\n")
    return query


def example_6_exclude_sensitive_fields():
    """Get all user fields except sensitive ones"""
    query = query_pb2.Query(
        entity="users",
        projection=query_pb2.Projection(
            exclude=["password_hash", "ssn", "credit_card.*"]
        ),
        pagination=pagination_pb2.Pagination(page_size=50)
    )
    
    print("Example 6: Exclude sensitive fields")
    print("Excluded: password_hash, ssn, credit_card.*\n")
    return query


def example_7_sorting():
    """Get users sorted by multiple fields"""
    query = query_pb2.Query(
        entity="users",
        sort=[
            sort_pb2.Sort(
                field="status",
                direction=sort_pb2.SORT_DIRECTION_ASC
            ),
            sort_pb2.Sort(
                field="created_at",
                direction=sort_pb2.SORT_DIRECTION_DESC
            )
        ],
        pagination=pagination_pb2.Pagination(page_size=50)
    )
    
    print("Example 7: Multi-field sorting")
    print("Sort: status ASC, created_at DESC")
    print("Result: Active users first, newest first within each status\n")
    return query


def example_8_null_check():
    """Find users without deletion timestamp (not deleted)"""
    query = query_pb2.Query(
        entity="users",
        filter=filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field="deleted_at",
                operator=filter_pb2.OPERATOR_IS_NULL
            )
        ),
        pagination=pagination_pb2.Pagination(page_size=100)
    )
    
    print("Example 8: Soft-deleted records check")
    print("Filter: deleted_at IS NULL (active records only)\n")
    return query


def example_9_string_contains():
    """Find users with email containing specific domain"""
    query = query_pb2.Query(
        entity="users",
        filter=filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field="email",
                operator=filter_pb2.OPERATOR_CONTAINS,
                value=Value(string_value="@example.com"),
                case_sensitive=False
            )
        ),
        pagination=pagination_pb2.Pagination(page_size=50)
    )
    
    print("Example 9: String contains (case-insensitive)")
    print("Filter: email CONTAINS '@example.com'\n")
    return query


def example_10_cursor_pagination():
    """Paginate through results using cursor"""
    
    # First page
    query_page1 = query_pb2.Query(
        entity="users",
        filter=filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field="status",
                operator=filter_pb2.OPERATOR_EQ,
                value=Value(string_value="active")
            )
        ),
        sort=[
            sort_pb2.Sort(
                field="created_at",
                direction=sort_pb2.SORT_DIRECTION_DESC
            )
        ],
        pagination=pagination_pb2.Pagination(page_size=50)
    )
    
    print("Example 10: Cursor pagination")
    print("Page 1: No cursor (start from beginning)")
    
    # Simulate getting next page cursor from response
    # In real usage: cursor = response.pagination.next_cursor
    simulated_cursor = "eyJpZCI6MTIzLCJjcmVhdGVkX2F0IjoiMjAyNC0wMS0xNVQxMDowMDowMFoifQ=="
    
    query_page2 = query_pb2.Query(
        entity="users",
        filter=query_page1.filter,
        sort=query_page1.sort,
        pagination=pagination_pb2.Pagination(
            page_size=50,
            cursor=simulated_cursor
        )
    )
    
    print(f"Page 2: cursor = {simulated_cursor[:30]}...")
    print("Benefit: O(log n) performance vs O(n) for offset\n")
    return query_page1, query_page2


def example_11_nested_field_access():
    """Filter by nested object field"""
    query = query_pb2.Query(
        entity="users",
        filter=filter_pb2.Filter(
            and_=filter_pb2.AndFilter(
                conditions=[
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="profile.country",
                            operator=filter_pb2.OPERATOR_EQ,
                            value=Value(string_value="US")
                        )
                    ),
                    filter_pb2.Filter(
                        condition=filter_pb2.Condition(
                            field="profile.age",
                            operator=filter_pb2.OPERATOR_GTE,
                            value=Value(number_value=18)
                        )
                    )
                ]
            )
        ),
        pagination=pagination_pb2.Pagination(page_size=50)
    )
    
    print("Example 11: Nested field access")
    print("Filter: profile.country = 'US' AND profile.age >= 18\n")
    return query


def example_12_array_contains():
    """Find users with specific tag"""
    query = query_pb2.Query(
        entity="users",
        filter=filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field="tags",
                operator=filter_pb2.OPERATOR_ARRAY_CONTAINS,
                value=Value(string_value="premium")
            )
        ),
        pagination=pagination_pb2.Pagination(page_size=50)
    )
    
    print("Example 12: Array contains")
    print("Filter: 'premium' IN tags\n")
    return query


def example_13_not_equal():
    """Find users not in pending status"""
    query = query_pb2.Query(
        entity="users",
        filter=filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field="status",
                operator=filter_pb2.OPERATOR_NE,
                value=Value(string_value="pending")
            )
        ),
        pagination=pagination_pb2.Pagination(page_size=50)
    )
    
    print("Example 13: Not equal")
    print("Filter: status != 'pending'\n")
    return query


def example_14_not_in():
    """Find users excluding certain roles"""
    query = query_pb2.Query(
        entity="users",
        filter=filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field="role",
                operator=filter_pb2.OPERATOR_NOT_IN,
                values=[
                    Value(string_value="guest"),
                    Value(string_value="suspended"),
                    Value(string_value="banned")
                ]
            )
        ),
        pagination=pagination_pb2.Pagination(page_size=100)
    )
    
    print("Example 14: Not in set")
    print("Filter: role NOT IN ('guest', 'suspended', 'banned')\n")
    return query


def example_15_with_options():
    """Query with execution options"""
    query = query_pb2.Query(
        entity="users",
        filter=filter_pb2.Filter(
            condition=filter_pb2.Condition(
                field="status",
                operator=filter_pb2.OPERATOR_EQ,
                value=Value(string_value="active")
            )
        ),
        pagination=pagination_pb2.Pagination(page_size=50),
        options=query_pb2.QueryOptions(
            timeout_ms=5000,  # 5 second timeout
            count_total=True,  # Get total count (expensive!)
            consistency=query_pb2.CONSISTENCY_LEVEL_STRONG,
            explain=False  # Set to True for debugging
        )
    )
    
    print("Example 15: Query with options")
    print("Timeout: 5000ms")
    print("Count total: True (warning: expensive!)")
    print("Consistency: STRONG\n")
    return query


def main():
    """Run all basic examples"""
    print("=" * 60)
    print("BASIC QUERY EXAMPLES")
    print("=" * 60)
    print()
    
    examples = [
        example_1_simple_equality,
        example_2_range_query,
        example_3_multiple_conditions,
        example_4_in_operator,
        example_5_field_projection,
        example_6_exclude_sensitive_fields,
        example_7_sorting,
        example_8_null_check,
        example_9_string_contains,
        example_10_cursor_pagination,
        example_11_nested_field_access,
        example_12_array_contains,
        example_13_not_equal,
        example_14_not_in,
        example_15_with_options
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
    print("All basic examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
