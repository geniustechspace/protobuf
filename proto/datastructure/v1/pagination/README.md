# Pagination Module

Standardized pagination controls for all list/query operations.

## Package

`geniustechspace.datastructure.v1.pagination`

## Messages

- **PaginationParams**: Parameters for paginated queries (input)
- **PaginationInfo**: Metadata about paginated result sets (output)

## Usage

- Use `PaginationParams` in request messages for paginated APIs
- Use `PaginationInfo` in response messages to provide pagination metadata

## Field Semantics

- `page`: 1-indexed page number (first page is 1)
- `page_size`: Items per page (default 20, max 1000)
- `ordering`, `sort_by`, `sort_order`: Flexible sorting options
- `total_items`, `total_pages`: For UI and navigation
- `has_next`, `has_previous`: For enabling/disabling navigation controls

## Validation

- All fields have buf.validate constraints for safety and consistency

## Compliance

- SOC 2 CC6.3 (Change management)
- Prevents memory exhaustion and timeout issues with large datasets

## Example

```proto
message ListUsersRequest {
  geniustechspace.datastructure.v1.pagination.PaginationParams pagination = 1;
}

message ListUsersResponse {
  repeated User users = 1;
  geniustechspace.datastructure.v1.pagination.PaginationInfo pagination = 2;
}
```

## Best Practices

- Always validate `page` and `page_size` on the server
- Default to reasonable limits (e.g., page_size=20, max=1000)
- Use 1-indexed pages for user-friendly APIs
- Provide `total_items` and `total_pages` for UI navigation
