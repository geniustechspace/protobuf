# Query System - Three-Layer Architecture

**Production-grade, storage-agnostic Query API for multi-backend data retrieval**

---

## Overview

This Query System provides a **three-layer protobuf-based architecture** designed for 10+ year longevity across multiple storage engines. The system separates concerns between client-facing APIs, semantic validation, and execution planning.

### Design Philosophy

- **Storage-Agnostic**: No SQL, MongoDB, or Elasticsearch concepts leak into the API
- **Strongly Typed**: Semantic validation happens at the CQM layer
- **One-Way Flow**: API → CQM → Plan (no upward deserialization)
- **Future-Proof**: Designed for additive evolution and backward compatibility

### Key Use Cases

- **Multi-Backend Queries**: Single API for SQL, NoSQL, and search engines
- **SDK Generation**: Type-safe clients for Go, Python, Java, TypeScript, C#
- **Query Optimization**: Explainable plans for debugging and cost analysis
- **Cross-Storage Federation**: Join data across different storage systems

---

## Architecture

### Three-Layer Design

```
┌─────────────────────────────────────────────────────────────┐
│                      CLIENT APPLICATION                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ gRPC/REST
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Layer 1: Query API                        │
│                   (proto/query/api/v1/)                      │
│                                                               │
│  Purpose: Client-facing, human-friendly query interface      │
│  Characteristics:                                             │
│    • Dot notation field paths ("user.profile.name")         │
│    • Loosely typed values (JSON-like)                        │
│    • Wildcards in projection ("profile.*")                   │
│    • Backward compatible evolution                           │
│                                                               │
│  Files: query.proto, filter.proto, sort.proto,              │
│         search.proto, aggregation.proto, etc.                │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Parser + Schema Resolver
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Layer 2: Canonical Query Model (CQM)            │
│                   (proto/query/cqm/v1/)                      │
│                                                               │
│  Purpose: Semantic, schema-bound query representation        │
│  Characteristics:                                             │
│    • Strongly typed (TypedValue, FieldRef)                   │
│    • Schema-resolved (field IDs, not paths)                  │
│    • Deterministic (no ambiguity)                            │
│    • Internal-only (never exposed to clients)                │
│                                                               │
│  Files: query.proto, predicate.proto, value.proto,          │
│         field.proto, projection.proto                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Query Planner + Optimizer
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                Layer 3: Query Plan (Logical + Physical)      │
│                   (proto/query/plan/v1/)                     │
│                                                               │
│  Purpose: Execution plans for debugging and optimization     │
│  Characteristics:                                             │
│    • Declarative (logical plan)                              │
│    • Concrete (physical plan with algorithms)                │
│    • Explainable (cost breakdown, recommendations)           │
│    • Storage-specific (index hints, join strategies)         │
│                                                               │
│  Files: logical_plan.proto, physical_plan.proto,            │
│         explain.proto                                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Execution Engine
                              ▼
                        Storage Backends
              (SQL, NoSQL, Search, Graph, etc.)
```

### Data Flow (One-Way Transformation)

```
API Query (from client)
    ↓
[Parser + Validator]
    ↓
Canonical Query (CQM)
    ↓
[Query Planner]
    ↓
Logical Plan
    ↓
[Optimizer]
    ↓
Physical Plan
    ↓
[Executor]
    ↓
Results (to client)
```

**Critical Rule**: Never deserialize upward. Physical Plans cannot be converted back to CQM. CQM cannot be converted back to API Query.

---

## Layer Responsibilities

### Layer 1: Query API (`proto/query/api/v1/`)

**Purpose**: Client-facing query interface

**What It Contains**:
- `query.proto`: Unified Query message composing all capabilities
- `filter.proto`: Recursive boolean filters (AND/OR/NOT + predicates)
- `sort.proto`: Multi-field sorting with null handling
- `search.proto`: Full-text and semantic search specifications
- `aggregation.proto`: Grouping and aggregate functions
- `relation.proto`: Explicit joins (escape hatch for complex queries)
- `pagination.proto`: Cursor and offset-based pagination

**Design Principles**:
- Human-friendly: Field paths as strings ("address.city")
- Backward compatible: Only additive changes
- Storage-agnostic: No SQL WHERE or MongoDB $match syntax
- Composable: Filter + Search + Sort + Aggregate work together

**What Belongs Here**:
✅ Client ergonomics (dot notation, wildcards)
✅ Validation rules (buf.validate annotations)
✅ Documentation for SDK users
✅ Backward compatibility guarantees

**What Does NOT Belong Here**:
❌ Schema-resolved field IDs
❌ Type-specific value representations
❌ Execution hints or optimizer guidance
❌ Storage engine concepts

**Evolution Strategy**:
- Version: `v1`, `v2`, etc. (directory-based)
- Breaking changes: Create new version, deprecate old
- Non-breaking: Add optional fields, new enums
- Deprecation: Use `[deprecated = true]` annotation

---

### Layer 2: Canonical Query Model (`proto/query/cqm/v1/`)

**Purpose**: Semantic, schema-bound query representation

**What It Contains**:
- `query.proto`: CanonicalQuery with resolved references
- `predicate.proto`: Strongly-typed boolean expressions
- `value.proto`: TypedValue with explicit type encoding
- `field.proto`: FieldRef with schema IDs and metadata
- `projection.proto`: Resolved field selections (wildcards expanded)

**Design Principles**:
- Strongly typed: All fields and values have concrete types
- Schema-resolved: Field paths → FieldRef with IDs
- Deterministic: No ambiguity, no wildcards, no string DSLs
- Internal-only: Never accept from clients, never expose in public APIs

**What Belongs Here**:
✅ Schema-resolved field references (FieldRef with field_id)
✅ Type-validated values (TypedValue with concrete types)
✅ Operator-type compatibility guarantees
✅ Normalized boolean logic (no implicit AND)

**What Does NOT Belong Here**:
❌ Client convenience features (dot notation, wildcards)
❌ Storage hints or execution strategies
❌ Cost estimates or performance metrics
❌ User-facing error messages

**Validation State**:
If a CQM exists, these are guaranteed:
- ✓ All fields exist in schema
- ✓ All types are compatible with operators
- ✓ All references are resolvable
- ✓ No semantic ambiguity

**Evolution Strategy**:
- Version freely (not tied to API versions)
- Breaking changes OK (internal-only)
- Optimize for planner efficiency, not client ergonomics

---

### Layer 3: Query Plan (`proto/query/plan/v1/`)

**Purpose**: Execution plans for debugging and optimization

**What It Contains**:
- `logical_plan.proto`: Declarative plan (scan, filter, join, aggregate)
- `physical_plan.proto`: Concrete plan (index scan, hash join, algorithms)
- `explain.proto`: Explainability (cost breakdown, recommendations)

**Design Principles**:
- Declarative: Logical plans describe WHAT to do
- Concrete: Physical plans describe HOW to execute
- Explainable: Cost models and optimization recommendations
- Debuggable: Execution timelines and statistics

**What Belongs Here**:
✅ Logical operations (scan, filter, join, aggregate)
✅ Physical algorithms (hash join, merge join, index scan)
✅ Cost estimates and statistics
✅ Optimization recommendations (missing indexes, etc.)

**What Does NOT Belong Here**:
❌ SQL strings or MongoDB pipelines (storage-specific)
❌ Procedural execution logic (that's in the executor)
❌ Optimizer heuristics (those evolve independently)

**Use Cases**:
- **Explain Plans**: Show users why query is slow
- **Cost Estimation**: Predict performance before execution
- **Debugging**: Identify bottlenecks in execution
- **Optimization**: Suggest indexes or query rewrites

**Evolution Strategy**:
- Change freely (internal representation)
- Explain format can evolve independently
- Statistics and recommendations can be added

---

## Operator Taxonomy

### Comparison Operators
- **EQ**: Equality (`field = value`)
- **NE**: Inequality (`field != value`)
- **LT, LTE, GT, GTE**: Ordering comparisons
  - Type compatibility: Numeric, Date, Timestamp, String (lexicographic)

### Set Operators
- **IN**: Set membership (`field IN (value1, value2, ...)`)
- **NOT_IN**: Set exclusion (`field NOT IN (value1, value2, ...)`)

### String Operators
- **CONTAINS**: Substring match (case-sensitive by default)
- **STARTS_WITH**: Prefix match
- **ENDS_WITH**: Suffix match
- **MATCHES**: Regex pattern match (RE2 syntax)

### Null Operators
- **IS_NULL**: Null check
- **IS_NOT_NULL**: Not null check

### Array Operators
- **ARRAY_CONTAINS**: Value in array (`value IN field`)
- **ARRAY_CONTAINS_ANY**: Any value in array (`ANY(values) IN field`)
- **ARRAY_CONTAINS_ALL**: All values in array (`ALL(values) IN field`)

### Logical Operators
- **AND**: All conditions must be true
- **OR**: At least one condition must be true
- **NOT**: Invert condition result

---

## Query Examples

### Example 1: Simple Filter Query

**API Layer** (client sends):
```protobuf
Query {
  entity: "users"
  filter: {
    and: {
      conditions: [
        { condition: { field: "status", operator: EQ, value: "active" } },
        { condition: { field: "created_at", operator: GT, value: "2024-01-01" } }
      ]
    }
  }
  projection: { include: ["id", "email", "created_at"] }
  sort: [{ field: "created_at", direction: DESC }]
  pagination: { page_size: 50 }
}
```

**CQM Layer** (internal representation):
```protobuf
CanonicalQuery {
  query_id: "550e8400-e29b-41d4-a716-446655440000"
  entity: { entity_id: "ent_123", entity_name: "users", schema_version: "v2" }
  predicate: {
    compound: {
      operator: AND
      operands: [
        { comparison: {
          left: { field_id: "fld_status", field_name: "status", field_type: STRING }
          operator: EQ
          value: { string_value: "active" }
        }},
        { comparison: {
          left: { field_id: "fld_created_at", field_name: "created_at", field_type: TIMESTAMP }
          operator: GT
          value: { timestamp_value: "2024-01-01T00:00:00Z" }
        }}
      ]
    }
  }
  projection: {
    fields: [
      { field_id: "fld_id", field_name: "id", field_type: UUID },
      { field_id: "fld_email", field_name: "email", field_type: STRING },
      { field_id: "fld_created_at", field_name: "created_at", field_type: TIMESTAMP }
    ]
    primary_key: [{ field_id: "fld_id", field_name: "id" }]
  }
}
```

**Plan Layer** (execution plan):
```protobuf
LogicalPlan {
  root: {
    node_type: limit { limit: 50 }
    children: [{
      node_type: sort { sorts: [{ field: "created_at", direction: DESC }] }
      children: [{
        node_type: project { fields: ["id", "email", "created_at"] }
        children: [{
          node_type: filter { predicate: {...} }
          children: [{
            node_type: scan { entity: "users", index_hint: "idx_status_created_at" }
          }]
        }]
      }]
    }]
  }
}
```

### Example 2: Aggregation Query

**API Layer**:
```protobuf
Query {
  entity: "orders"
  filter: {
    condition: { field: "status", operator: EQ, value: "completed" }
  }
  aggregation: {
    group_by: ["customer_id"]
    aggregates: [
      { function: COUNT, alias: "order_count" },
      { function: SUM, field: "total_amount", alias: "total_revenue" },
      { function: AVG, field: "total_amount", alias: "avg_order_value" }
    ]
    having: {
      condition: { field: "order_count", operator: GTE, value: 5 }
    }
  }
  sort: [{ field: "total_revenue", direction: DESC }]
}
```

### Example 3: Hybrid Search Query

**API Layer**:
```protobuf
Query {
  entity: "documents"
  filter: {
    and: {
      conditions: [
        { condition: { field: "category", operator: EQ, value: "research" } },
        { condition: { field: "published_at", operator: GTE, value: "2024-01-01" } }
      ]
    }
  }
  search: {
    query: "machine learning optimization"
    type: HYBRID
    fields: ["title", "abstract", "content"]
    vector_field: "content_embedding"
    min_score: 0.7
    boost: { "title": 2.0, "abstract": 1.5 }
  }
  pagination: { page_size: 20 }
}
```

---

## Transformation Pipeline

### Stage 1: API → CQM Transformation

**Parser Responsibilities**:
1. ✅ Validate API Query structure (buf.validate rules)
2. ✅ Resolve field paths to FieldRef using schema registry
3. ✅ Expand wildcards in projections
4. ✅ Validate operator-type compatibility
5. ✅ Coerce values to TypedValue with correct types
6. ✅ Normalize boolean logic (flatten unnecessary nesting)
7. ✅ Apply field-level permissions (omit inaccessible fields)
8. ✅ Generate query_id for tracing

**Error Conditions**:
- ❌ Field does not exist in schema
- ❌ Operator incompatible with field type (e.g., LT on string)
- ❌ Value type does not match field type
- ❌ User lacks permission to access field
- ❌ Invalid regex pattern in MATCHES operator

### Stage 2: CQM → Logical Plan

**Planner Responsibilities**:
1. ✅ Build operator tree (scan, filter, project, sort, limit)
2. ✅ Push filters down to scans when possible
3. ✅ Identify join opportunities (from FieldRef paths)
4. ✅ Estimate cardinalities for each operator
5. ✅ Generate plan_id for tracing

**Optimizations** (applied here or in next stage):
- Filter pushdown to storage engine
- Predicate reordering (most selective first)
- Join order optimization
- Projection pruning (eliminate unused fields)

### Stage 3: Logical Plan → Physical Plan

**Optimizer Responsibilities**:
1. ✅ Select indexes for scans (based on predicates and statistics)
2. ✅ Choose join algorithms (hash, merge, nested loop)
3. ✅ Choose aggregation strategy (hash or sort-based)
4. ✅ Estimate costs using storage engine statistics
5. ✅ Select degree of parallelism
6. ✅ Generate optimization recommendations

**Cost Model Factors**:
- Index selectivity (how many rows match)
- Join cardinality (result size of join)
- Sort cost (in-memory vs external)
- Network cost (for distributed queries)

---

## Versioning Strategy

### API Layer Versioning (`proto/query/api/v1/`)

**Philosophy**: **Slow evolution, strong backward compatibility**

**Version Scope**:
- Major version: `v1`, `v2`, etc.
- Changes that require new version:
  - Removing fields or enum values
  - Changing field types or semantics
  - Changing message structure (oneof changes)
  - Incompatible validation changes

**Backward-Compatible Changes** (stay in v1):
- ✅ Adding new optional fields
- ✅ Adding new enum values (with UNSPECIFIED default)
- ✅ Adding new message types
- ✅ Relaxing validation (min → lower, max → higher)
- ✅ Deprecating fields (mark `[deprecated = true]`)

**Example Migration Path**:
```
v1: Initial API release (stable for years)
  └─> v1.1: Add optional search.fuzzy field (backward compatible)
  └─> v1.2: Add new VECTOR_SIMILAR operator (backward compatible)
  └─> v1.3: Deprecate relation.eager field (backward compatible)

v2: Major revision (when v1 becomes constraining)
  - Remove deprecated fields
  - Change filter structure for performance
  - Breaking changes OK (clients must migrate)
```

### CQM Layer Versioning (`proto/query/cqm/v1/`)

**Philosophy**: **Internal-only, evolve freely**

**Version Scope**:
- Not tied to API versions
- Can version independently for optimizer improvements
- Breaking changes OK (not client-facing)

**When to Version**:
- ✅ New field types or value representations
- ✅ Changed semantic validation rules
- ✅ New predicate operators (internal representation)

### Plan Layer Versioning (`proto/query/plan/v1/`)

**Philosophy**: **Implementation detail, change freely**

**Version Scope**:
- Logical plan format can evolve independently of physical plan
- Explain format can change for better user experience
- No client contract (except explain output for authorized users)

---

## What Belongs in Each Layer

### ✅ Query API Layer
- Client ergonomics: dot notation, wildcards, case_sensitive flags
- Human-readable field names (strings)
- Loosely typed values (google.protobuf.Value)
- Backward compatibility guarantees
- Public documentation for SDK users

### ✅ CQM Layer
- Schema-resolved field references (IDs, not names)
- Strongly typed values (TypedValue with concrete types)
- Normalized boolean logic (no implicit AND/OR)
- Operator-type compatibility validation
- Wildcard expansion (wildcards → explicit field list)

### ✅ Plan Layer
- Logical operations (scan, filter, join, aggregate)
- Physical algorithms (hash join, merge join, index scan)
- Cost estimates and statistics
- Execution timelines and profiling data
- Optimization recommendations

### ❌ What Does NOT Belong Anywhere
- SQL strings or storage-specific query languages
- Procedural execution logic (if/else, loops)
- Optimizer heuristics encoded in protobuf
- Client-side validation logic (use buf.validate)
- Engine-specific hacks or workarounds

---

## Cross-Cutting Concerns

### Multi-Tenancy
- **Requirement**: All queries MUST include tenant_id
- **Enforcement**: At API validation layer (reject queries without tenant_id)
- **Isolation**: Planner MUST inject tenant_id filters into all scans
- **Security**: Storage engine MUST enforce row-level security by tenant

### Field-Level Permissions
- **Resolution**: During API → CQM transformation
- **Approach**: Schema registry provides field ACLs
- **Enforcement**: Omit inaccessible fields from projection, reject filters on forbidden fields
- **Audit**: Log access attempts to sensitive fields

### Compliance (PII Handling)
- **Identification**: Schema registry marks PII fields (is_pii flag)
- **Projection**: Warn or reject queries projecting PII without proper authorization
- **Audit**: Log all PII field access with user_id and correlation_id
- **Encryption**: Handle encrypted fields transparently (decrypt in executor)

### Distributed Tracing
- **Query ID**: Generated during API → CQM transformation (UUID)
- **Correlation ID**: Propagated from client request headers
- **Plan IDs**: Link Logical Plan → Physical Plan → Explain
- **Timeline**: ExecutionEvent messages for distributed tracing systems

---

## Testing Strategy

### API Layer Tests
- **Schema Validation**: Ensure buf.validate rules are correct
- **Example Queries**: Verify common query patterns parse correctly
- **Error Cases**: Invalid operators, missing required fields, etc.
- **Backward Compatibility**: Ensure v1 queries work across updates

### CQM Layer Tests
- **Type Resolution**: Field paths → FieldRef with correct types
- **Operator Validation**: Ensure LT only works on ordered types
- **Wildcard Expansion**: Verify "profile.*" expands to all subfields
- **Normalization**: Ensure boolean logic is simplified correctly

### Plan Layer Tests
- **Plan Generation**: CQM → Logical Plan correctness
- **Cost Estimation**: Verify cost model is reasonable
- **Optimization Rules**: Test filter pushdown, join reordering
- **Explain Output**: Ensure recommendations are actionable

### End-to-End Tests
- **Storage Engines**: Verify plans execute correctly on SQL, NoSQL, Search
- **Performance**: Benchmark query latency and throughput
- **Correctness**: Compare results across different storage backends
- **Regression**: Ensure optimizations don't break existing queries

---

## Migration Guide

### From Legacy Query Systems

#### Step 1: Map Existing Queries to API Layer
```
Legacy:   SELECT id, email FROM users WHERE status = 'active'
Query API: Query {
             entity: "users"
             filter: { condition: { field: "status", operator: EQ, value: "active" } }
             projection: { include: ["id", "email"] }
           }
```

#### Step 2: Implement Schema Registry
- Define entity schemas with field IDs, types, indexes
- Implement field resolution (path → FieldRef)
- Implement permission checks

#### Step 3: Implement CQM Transformer
- Parse API Query → Canonical Query
- Validate types and operators
- Expand wildcards

#### Step 4: Implement Query Planner
- CQM → Logical Plan
- Basic optimizer (filter pushdown, join order)

#### Step 5: Implement Physical Planner (per storage engine)
- Logical Plan → Physical Plan
- Storage-specific optimizations
- Index selection

#### Step 6: Implement Executor (per storage engine)
- Physical Plan → Storage-specific queries (SQL, MongoDB, etc.)
- Execute and return results

---

## Maintenance Guidelines

### Adding New Operators

1. **API Layer**: Add enum value to `Operator` in `filter.proto`
2. **Documentation**: Document operator semantics, type compatibility, examples
3. **CQM Layer**: Add enum value to `ComparisonOperator` in `predicate.proto`
4. **Transformer**: Implement API Operator → CQM ComparisonOperator mapping
5. **Validator**: Add type compatibility checks
6. **Planner**: Handle new operator in logical plan generation
7. **Executor**: Implement operator in storage-specific executors
8. **Tests**: Add test cases for new operator

### Adding New Aggregation Functions

1. **API Layer**: Add enum value to `AggregateFunction` in `aggregation.proto`
2. **Documentation**: Document function semantics, input types, output type
3. **CQM Layer**: Add enum value to `AggregateFunction` in `query.proto`
4. **Planner**: Handle function in aggregation node generation
5. **Physical Plan**: Choose hash or sort-based aggregation
6. **Executor**: Implement function in storage-specific aggregators
7. **Tests**: Add test cases for new function

### Deprecating Fields

**Never remove fields. Use deprecation process:**

```protobuf
message Query {
  // Old field (deprecated)
  repeated Relation relation = 8 [deprecated = true];
  
  // New field (replacement)
  repeated RelationV2 relations = 9;
  
  // Reserve old field number to prevent reuse
  reserved 8;
  reserved "relation";
}
```

---

## Performance Considerations

### API Layer
- **Validation**: Use buf.validate for efficient protobuf-level validation
- **Parsing**: Avoid expensive regex or string parsing in API layer

### CQM Layer
- **Field Resolution**: Cache schema lookups (field path → FieldRef)
- **Type Coercion**: Pre-validate types to avoid runtime errors
- **Wildcard Expansion**: Limit expansion depth to prevent DoS

### Plan Layer
- **Cost Model**: Use statistics (not queries) for cost estimation
- **Plan Caching**: Cache plans for identical queries (by query fingerprint)
- **Explain**: Generate explain plans lazily (only if requested)

### General
- **Pagination**: Prefer cursor-based (O(log n)) over offset (O(n))
- **Projection**: Always project minimal fields (reduce network/memory)
- **Filter Pushdown**: Push filters to storage engine when possible

---

## Observability

### Metrics to Track
- Query parse time (API → CQM)
- Planning time (CQM → Logical Plan → Physical Plan)
- Execution time (per operator)
- Result set size (rows returned)
- Cache hit rate (plan cache, result cache)
- Error rate (by error type)

### Logs to Capture
- Query ID + Correlation ID (link to traces)
- Tenant ID + User ID (for audit)
- PII field access (compliance)
- Slow queries (> threshold)
- Plan changes (optimizer version upgrades)

### Tracing
- Span per layer (API → CQM → Plan → Executor)
- Span per physical operator (scan, join, aggregate)
- Attach plan_id to spans for correlation

---

## Future Extensions

### Planned Features
- **Geospatial Queries**: GEO_WITHIN, GEO_NEAR operators
- **Graph Traversal**: Recursive queries for graph databases
- **Time-Series**: Window functions and time-based aggregations
- **Vector Search**: Improved semantic search with custom distance metrics
- **Federated Queries**: Join across multiple storage engines

### Research Areas
- **Cost Model Tuning**: Machine learning for cost estimation
- **Adaptive Execution**: Re-plan during execution based on intermediate results
- **Query Hints**: Allow expert users to guide optimizer
- **Materialized Views**: Automatic view recommendation and refresh

---

## Contributing

### Before Adding Features
1. ✅ Determine which layer the feature belongs to
2. ✅ Check if it violates layer boundaries
3. ✅ Consider backward compatibility (API layer only)
4. ✅ Update documentation and examples

### Code Review Checklist
- [ ] No cross-layer imports (API does not import CQM/Plan)
- [ ] No storage-specific concepts in API or CQM
- [ ] All messages and fields documented
- [ ] Examples updated in README
- [ ] Tests added for new functionality
- [ ] buf.validate rules added for API changes

### Prohibited Patterns
- ❌ SQL strings in API or CQM layers
- ❌ Upward deserialization (Plan → CQM → API)
- ❌ Implicit type coercion in CQM
- ❌ Client-facing CQM or Plan messages

---

## Appendices

### A. Complete File List

```
proto/query/
├── api/
│   └── v1/
│       ├── query.proto          # Unified Query message
│       ├── filter.proto         # Filter conditions (AND/OR/NOT)
│       ├── sort.proto           # Sorting specifications
│       ├── search.proto         # Full-text and semantic search
│       ├── aggregation.proto    # Grouping and aggregation
│       ├── relation.proto       # Explicit joins
│       └── pagination.proto     # Cursor and offset pagination
│
├── cqm/
│   └── v1/
│       ├── query.proto          # CanonicalQuery
│       ├── predicate.proto      # Strongly-typed predicates
│       ├── value.proto          # TypedValue with concrete types
│       ├── field.proto          # FieldRef with schema IDs
│       └── projection.proto     # Resolved field selections
│
├── plan/
│   └── v1/
│       ├── logical_plan.proto   # Declarative query plan
│       ├── physical_plan.proto  # Concrete execution plan
│       └── explain.proto        # Explainability and cost analysis
│
└── README.md (this file)
```

### B. Glossary

- **API Query**: Client-facing query message (loosely typed)
- **CQM**: Canonical Query Model (strongly typed, schema-resolved)
- **FieldRef**: Schema-resolved field reference with ID and type
- **TypedValue**: Strongly-typed value representation
- **Logical Plan**: Declarative query execution plan
- **Physical Plan**: Concrete query execution plan with algorithms
- **Predicate**: Boolean expression (filter condition)
- **Projection**: Field selection (which fields to return)
- **Operator**: Comparison or logical operation (EQ, AND, etc.)
- **Planner**: Transforms CQM into Logical Plan
- **Optimizer**: Transforms Logical Plan into Physical Plan
- **Executor**: Runs Physical Plan against storage engine

### C. Reference Links

- **Buf Documentation**: https://buf.build/docs
- **Protovalidate**: https://github.com/bufbuild/protovalidate
- **Protocol Buffers**: https://protobuf.dev
- **Query Planning Theory**: "Database System Concepts" (Silberschatz)
- **Cost-Based Optimization**: "Database Management Systems" (Ramakrishnan)

---

**Last Updated**: 2024-12-16  
**Schema Version**: v1  
**Maintainers**: Query Infrastructure Team  
**License**: See LICENSE file
