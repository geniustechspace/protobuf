#!/usr/bin/env python3
"""
gRPC Client Example - Full integration with query service

Demonstrates:
- Connecting to query service via gRPC
- Executing queries and processing responses
- Error handling and retry logic
- Pagination handling
- Query explain mode
"""

import grpc
from typing import Optional, Iterator
from datetime import datetime
from google.protobuf.json_format import MessageToDict

# Import generated protobuf code
from geniustechspace.query.api.v1 import (
    query_pb2,
    filter_pb2,
    sort_pb2,
    pagination_pb2
)

# Assuming generated gRPC service
# from geniustechspace.query.api.v1 import services_pb2_grpc


class QueryClient:
    """Client for Query Service"""
    
    def __init__(self, host: str = "localhost:50051", 
                 tenant_id: str = "tenant_123",
                 timeout: int = 30):
        """
        Initialize query client
        
        Args:
            host: gRPC server address
            tenant_id: Tenant ID for multi-tenancy
            timeout: Default timeout in seconds
        """
        self.host = host
        self.tenant_id = tenant_id
        self.timeout = timeout
        self._channel: Optional[grpc.Channel] = None
        self._stub = None
    
    def connect(self):
        """Establish gRPC connection"""
        # For production, use secure channel:
        # credentials = grpc.ssl_channel_credentials()
        # self._channel = grpc.secure_channel(self.host, credentials)
        
        # For development:
        self._channel = grpc.insecure_channel(self.host)
        
        # Create stub (uncomment when service proto is available)
        # self._stub = services_pb2_grpc.QueryServiceStub(self._channel)
        
        print(f"Connected to {self.host}")
    
    def close(self):
        """Close gRPC connection"""
        if self._channel:
            self._channel.close()
            print("Connection closed")
    
    def execute_query(self, query: query_pb2.Query, 
                     timeout: Optional[int] = None) -> dict:
        """
        Execute query and return response
        
        Args:
            query: Query protobuf message
            timeout: Optional timeout override
            
        Returns:
            Response as dictionary
        """
        if not self._stub:
            raise RuntimeError("Not connected. Call connect() first.")
        
        # Add tenant context (in metadata or query)
        metadata = [
            ('tenant-id', self.tenant_id),
            ('request-id', f"req_{datetime.utcnow().timestamp()}")
        ]
        
        try:
            # Execute query (uncomment when service is available)
            # response = self._stub.Execute(
            #     query,
            #     timeout=timeout or self.timeout,
            #     metadata=metadata
            # )
            
            # For now, return mock response
            response = self._mock_response(query)
            
            return MessageToDict(response)
            
        except grpc.RpcError as e:
            self._handle_grpc_error(e)
            raise
    
    def execute_paginated(self, query: query_pb2.Query, 
                         max_pages: int = 10) -> Iterator[dict]:
        """
        Execute query with automatic pagination
        
        Args:
            query: Query protobuf message
            max_pages: Maximum pages to fetch
            
        Yields:
            Response dictionaries for each page
        """
        page = 0
        cursor = None
        
        while page < max_pages:
            # Set cursor for subsequent pages
            if cursor:
                query.pagination.cursor = cursor
            
            response = self.execute_query(query)
            yield response
            
            # Check if more pages
            pagination = response.get('pagination', {})
            cursor = pagination.get('nextCursor')
            
            if not cursor or not pagination.get('hasMore'):
                break
            
            page += 1
            print(f"Fetched page {page + 1}")
    
    def explain_query(self, query: query_pb2.Query) -> dict:
        """
        Get query execution plan
        
        Args:
            query: Query to explain
            
        Returns:
            Explain result
        """
        # Enable explain mode
        if not query.options.explain:
            query.options.explain = True
        
        response = self.execute_query(query)
        
        if 'explain' in response:
            return response['explain']
        else:
            print("Warning: Explain result not available")
            return {}
    
    def _mock_response(self, query: query_pb2.Query) -> dict:
        """Generate mock response for testing"""
        # This would be replaced with actual gRPC call
        return {
            'results': [
                {'id': '1', 'name': 'Item 1'},
                {'id': '2', 'name': 'Item 2'}
            ],
            'pagination': {
                'totalCount': 100,
                'pageSize': query.pagination.page_size or 50,
                'hasMore': True,
                'nextCursor': 'next_page_cursor_abc123'
            }
        }
    
    def _handle_grpc_error(self, error: grpc.RpcError):
        """Handle gRPC errors with user-friendly messages"""
        code = error.code()
        details = error.details()
        
        error_messages = {
            grpc.StatusCode.INVALID_ARGUMENT: f"Invalid query: {details}",
            grpc.StatusCode.NOT_FOUND: f"Entity not found: {details}",
            grpc.StatusCode.PERMISSION_DENIED: f"Access denied: {details}",
            grpc.StatusCode.UNAUTHENTICATED: "Authentication required",
            grpc.StatusCode.DEADLINE_EXCEEDED: "Query timeout",
            grpc.StatusCode.RESOURCE_EXHAUSTED: "Rate limit exceeded",
            grpc.StatusCode.UNAVAILABLE: "Service unavailable"
        }
        
        message = error_messages.get(code, f"Query failed: {details}")
        print(f"Error [{code.name}]: {message}")


def example_1_simple_query():
    """Execute simple query with client"""
    client = QueryClient(tenant_id="tenant_demo")
    
    try:
        client.connect()
        
        # Build query
        query = query_pb2.Query(
            entity="users",
            filter=filter_pb2.Filter(
                condition=filter_pb2.Condition(
                    field="status",
                    operator=filter_pb2.OPERATOR_EQ,
                    value={"string_value": "active"}
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
        
        # Execute
        print("Executing query...")
        response = client.execute_query(query)
        
        print(f"Results: {len(response.get('results', []))} items")
        print(f"Total: {response['pagination']['totalCount']}")
        
    finally:
        client.close()


def example_2_paginated_query():
    """Execute query with pagination"""
    client = QueryClient(tenant_id="tenant_demo")
    
    try:
        client.connect()
        
        query = query_pb2.Query(
            entity="products",
            pagination=pagination_pb2.Pagination(page_size=100)
        )
        
        print("Fetching all pages...")
        total_items = 0
        
        for page_num, response in enumerate(client.execute_paginated(query, max_pages=5)):
            items = len(response.get('results', []))
            total_items += items
            print(f"Page {page_num + 1}: {items} items")
        
        print(f"Total fetched: {total_items} items")
        
    finally:
        client.close()


def example_3_explain_query():
    """Get query execution plan"""
    client = QueryClient(tenant_id="tenant_demo")
    
    try:
        client.connect()
        
        query = query_pb2.Query(
            entity="orders",
            filter=filter_pb2.Filter(
                and_=filter_pb2.AndFilter(
                    conditions=[
                        filter_pb2.Filter(
                            condition=filter_pb2.Condition(
                                field="total_amount",
                                operator=filter_pb2.OPERATOR_GTE,
                                value={"number_value": 1000}
                            )
                        ),
                        filter_pb2.Filter(
                            condition=filter_pb2.Condition(
                                field="status",
                                operator=filter_pb2.OPERATOR_EQ,
                                value={"string_value": "completed"}
                            )
                        )
                    ]
                )
            )
        )
        
        print("Getting query plan...")
        explain = client.explain_query(query)
        
        if explain:
            print("\nQuery Plan:")
            print(f"Estimated cost: {explain.get('cost', {}).get('totalCost', 'N/A')}")
            print(f"Estimated time: {explain.get('cost', {}).get('estimatedTimeMs', 'N/A')}ms")
            
            recommendations = explain.get('recommendations', [])
            if recommendations:
                print(f"\nRecommendations ({len(recommendations)}):")
                for rec in recommendations:
                    print(f"  - [{rec['severity']}] {rec['description']}")
        
    finally:
        client.close()


def example_4_error_handling():
    """Demonstrate error handling"""
    client = QueryClient(tenant_id="tenant_demo")
    
    try:
        client.connect()
        
        # Invalid query (missing required field)
        query = query_pb2.Query(
            entity="",  # Invalid: empty entity
            pagination=pagination_pb2.Pagination(page_size=50)
        )
        
        try:
            response = client.execute_query(query)
        except grpc.RpcError as e:
            print(f"Caught expected error: {e.code().name}")
        
    finally:
        client.close()


def main():
    """Run all client examples"""
    print("=" * 60)
    print("gRPC CLIENT EXAMPLES")
    print("=" * 60)
    print()
    
    print("Note: These examples use mock responses.")
    print("Connect to actual query service to see real results.")
    print()
    
    examples = [
        ("Simple Query", example_1_simple_query),
        ("Paginated Query", example_2_paginated_query),
        ("Explain Query", example_3_explain_query),
        ("Error Handling", example_4_error_handling)
    ]
    
    for name, example_func in examples:
        print("-" * 60)
        print(f"Example: {name}")
        print("-" * 60)
        try:
            example_func()
            print("✓ Completed\n")
        except Exception as e:
            print(f"✗ Error: {e}\n")


if __name__ == "__main__":
    main()
