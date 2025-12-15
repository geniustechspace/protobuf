# Projection Selector Language (PSL) v1

Universal field selection syntax for databases, filesystems, documents, APIs, and more.

## Quick Start

```protobuf
// Include only specific fields
Projection {
  include: ["id", "user.name", "user.email"]
}

// Include everything except secrets
Projection {
  exclude: ["**.password", "**.token", "**.ssn"]
}

// Include subtree, exclude one field
Projection {
  include: ["user.**"],
  exclude: ["user.internalNotes"]
}
```

## Syntax Reference

### Basic Paths

| Pattern            | Matches      | Example                 |
| ------------------ | ------------ | ----------------------- |
| `field`            | Single field | `name`                  |
| `parent.child`     | Nested field | `user.profile.city`     |
| `` `field.name` `` | Escaped dots | `` `user.first.name` `` |

### Lists (Repeated Fields)

| Pattern               | Matches               | Example                |
| --------------------- | --------------------- | ---------------------- |
| `field[]`             | All list elements     | `orders[]`             |
| `field[].child`       | Child in each element | `orders[].id`          |
| `field[].nested[].id` | Multi-level lists     | `orders[].items[].sku` |

### Maps (Dictionaries)

| Pattern        | Matches             | Example               |
| -------------- | ------------------- | --------------------- |
| `map[*]`       | All map keys        | `attributes[*]`       |
| `map['key']`   | Specific key        | `metadata['version']` |
| `map[*].field` | Field in all values | `users[*].email`      |

### Wildcards

| Pattern    | Matches               | Example                                    |
| ---------- | --------------------- | ------------------------------------------ |
| `*`        | One segment           | `user.*` matches `user.name`, `user.email` |
| `**`       | Zero or more segments | `user.**` matches entire user subtree      |
| `**.field` | Deep search           | `**.id` matches any `id` anywhere          |

## Evaluation Rules

### Two-Phase Algorithm

1. **Include Phase**: Build candidate set from `include` patterns

   - Empty include → include everything (default: `["**"]`)
   - Non-empty include → include only matches

2. **Exclude Phase**: Remove matches from `exclude` patterns

### Conflict Resolution (Specificity Scoring)

When a field matches both include and exclude, compute **specificity score**:

| Element                  | Score |
| ------------------------ | ----- |
| Literal segment          | +3    |
| Quoted segment           | +3    |
| Specific map key `['k']` | +2    |
| List marker `[]`         | +1    |
| Map wildcard `[*]`       | +1    |
| Single wildcard `*`      | +1    |
| Deep wildcard `**`       | +0    |

**Decision rules:**

- Higher score wins
- Equal score → exclude wins
- Parent containers auto-included if child selected

### Examples

```protobuf
// user.password excluded (exclude more specific: 3+3 vs 3+1)
include: ["user.*"]
exclude: ["user.password"]

// user.password included (include more specific: 3+3 vs 0+3)
include: ["user.password"]
exclude: ["**.password"]

// orders[].id included, orders[].total excluded
include: ["orders[].id"]
exclude: ["orders[].total"]
```

## Storage Implementations

### SQL (PostgreSQL)

```sql
-- include: ["id", "user.name", "user.email"]
SELECT
  id,
  jsonb_build_object(
    'name', user->>'name',
    'email', user->>'email'
  ) as user
FROM resources;

-- exclude: ["**.password"]
SELECT * EXCEPT (password, metadata.password)
FROM resources;
```

### MongoDB

```javascript
// include: ["id", "user.name", "orders[].total"]
db.collection.find(
  {},
  {
    _id: 1,
    "user.name": 1,
    "orders.total": 1,
  }
);

// exclude: ["internal.**"]
db.collection.aggregate([{ $project: { internal: 0 } }]);
```

### Elasticsearch

```json
{
  "_source": {
    "includes": ["id", "user.*", "tags[]"],
    "excludes": ["**.password", "internal.*"]
  }
}
```

### Filesystem (find/tree)

```bash
# include: ["src/**/*.ts"]
find src -name "*.ts"

# exclude: ["**/node_modules/**", "**/*.test.ts"]
find . -name "*.ts" \
  -not -path "*/node_modules/*" \
  -not -name "*.test.ts"
```

### JSON (jq)

```bash
# include: ["user.profile.city", "orders[].id"]
jq '{user: {profile: {city: .user.profile.city}}, orders: [.orders[].id]}'

# exclude: ["**.password"]
jq 'walk(if type == "object" then del(.password) else . end)'
```

## Validation Rules

Server MUST reject if:

| Error             | Condition                          | Code                |
| ----------------- | ---------------------------------- | ------------------- |
| Invalid syntax    | Unclosed quotes, bad escaping      | `INVALID_SYNTAX`    |
| Unknown field     | Literal segment not in schema      | `UNKNOWN_FIELD`     |
| Type mismatch     | `[]` on non-list, `[*]` on non-map | `TYPE_MISMATCH`     |
| Scalar traversal  | `scalar.field`                     | `INVALID_TRAVERSAL` |
| Too many patterns | > 200 total                        | `LIMIT_EXCEEDED`    |
| Pattern too long  | > 50 segments                      | `DEPTH_EXCEEDED`    |
| Too many `**`     | > 3 per pattern                    | `WILDCARD_LIMIT`    |

### Error Response Format

```protobuf
message ProjectionError {
  uint32 pattern_index = 1;
  string pattern = 2;
  string error_code = 3;
  string message = 4;
  uint32 segment_index = 5; // Approximate location
}
```

## Use Cases

### API Response Filtering

```protobuf
// Mobile client: minimal data
Projection {
  include: ["id", "name", "thumbnail", "status"]
}

// Admin dashboard: everything
Projection {
  include: ["**"],
  exclude: ["**.passwordHash", "**.token"]
}
```

### Multi-Tenant Data Isolation

```protobuf
// Tenant can only see their data
Projection {
  include: ["tenantId", "data.**"],
  exclude: ["data.internal.**"]
}
```

### Audit Trail Filtering

```protobuf
// Log everything except PII
Projection {
  include: ["**"],
  exclude: ["**.ssn", "**.creditCard", "**.password", "**.email"]
}
```

### Filesystem Backup

```protobuf
// Backup source code only
Projection {
  include: ["src/**", "tests/**", "*.md"],
  exclude: ["**/node_modules/**", "**/.git/**", "**/*.log"]
}
```

## Canonicalization

Before evaluation, normalize patterns:

1. **Trim whitespace**: Leading/trailing only
2. **Reject bad syntax**: `a..b`, unclosed quotes
3. **Collapse deep wildcards**: `**.**.id` → `**.id`
4. **Remove duplicates**: Identical patterns

## Limits & Performance

### Recommended Limits

- Max 200 patterns (include + exclude combined)
- Max 50 segments per pattern
- Max 3 `**` wildcards per pattern
- Max 1000 nodes evaluated per request
- Timeout: 5 seconds for pattern matching

### Optimization Tips

1. **Use specific patterns**: `user.name` faster than `**`
2. **Limit deep wildcards**: `**` requires full tree scan
3. **Pre-compile patterns**: Build matcher once, reuse
4. **Cache results**: Pattern → matched fields mapping
5. **Schema validation**: Reject unknown fields early

## Versioning

```protobuf
message Projection {
  uint32 psl_version = 1; // Current: 1
  repeated string include = 2;
  repeated string exclude = 3;
}
```

### Future: PSL v2

Potential additions:

- **Predicates**: `orders[status='pending'].id`
- **Set operators**: `(name,email)` grouping
- **Aliases**: `username:user.profile.name`
- **Computed fields**: `fullName:concat(firstName," ",lastName)`

## Grammar (EBNF)

``` markdown
pattern        := path | wildcard
path           := component ( "." component )*
component      := segment list_suffix? map_suffix?
segment        := identifier | "*" | "**" | quoted
identifier     := [A-Za-z_][A-Za-z0-9_]*
quoted         := "`" ( [^`] | "``" )* "`"
list_suffix    := "[]"
map_suffix     := "[" ( "*" | string_literal ) "]"
string_literal := "'" ( [^'] | "''" )* "'"
wildcard       := "*" | "**"
```

## FAQ

**Q: Does `include: ["user"]` return empty object or full subtree?**  
A: Empty object. Use `["user.**"]` for full subtree.

**Q: Can I re-include after excluding?**  
A: Yes, if include pattern is more specific (higher score).

**Q: Are field names case-sensitive?**  
A: Yes. `Name` ≠ `name`.

**Q: What if include and exclude are both empty?**  
A: Returns everything (default: `include=["**"]`).

**Q: How do I exclude all passwords everywhere?**  
A: `exclude: ["**.password"]`

**Q: How do I select only list IDs?**  
A: `include: ["orders[].id"]`

**Q: Can I select specific list indices?**  
A: No in PSL v1. Use `orders[]` for all elements. Filtering is separate (see filter.proto).

## Compliance Notes

- **SOC 2 CC6.1**: Data minimization via projection
- **GDPR Article 5(1)(c)**: Only fetch necessary data
- **PCI DSS 3.2.1**: Exclude cardholder data via `exclude: ["**.cardNumber", "**.cvv"]`

## See Also

- [filter.proto](v1/filter.proto) - Data filtering/querying
- [query.proto](v1/query.proto) - Main query interface
- [examples.proto](v1/examples.proto) - Usage examples
