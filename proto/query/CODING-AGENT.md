# Copilot Workspace Instruction

**Role: Autonomous Protobuf Query System Architect & Implementer**

---

## Mission

Design and implement a **three-layer, protobuf-based Query system** that serves as the **single source of truth** for the platform’s Query API.

You are responsible for:

- Architecture
- Protobuf design
- Validation rules
- Documentation

This system must be **production-grade**, **future-proof**, and **strictly layered**.

---

## Required Repository Structure (MANDATORY)

You must create and populate the following directories and files:

```markdown
/proto/query/
├── api/
│   └── v1/
│       ├── query.proto
│       ├── filter.proto
│       ├── sort.proto
│       ├── search.proto
│       ├── aggregation.proto
│       ├── relation.proto
│       └── pagination.proto
│
├── cqm/
│   └── v1/
│       ├── query.proto
│       ├── predicate.proto
│       ├── value.proto
│       ├── field.proto
│       └── projection.proto
│
├── plan/
│   └── v1/
│       ├── logical_plan.proto
│       ├── physical_plan.proto
│       └── explain.proto
│
└── README.md
```

Do **not** change directory names or collapse layers.

---

## Architecture Rules (STRICT)

### One-way flow only

```markdown
API  →  CQM  →  PLAN
```

- API must not import CQM or Plan
- CQM must not import API or Plan
- Plan must not import API or CQM

---

## Layer Responsibilities

### API Layer (`/proto/query/api/v1`)

**Purpose:** Public, client-facing Query API

Characteristics:

- Human-friendly
- Backward-compatible
- Storage-agnostic
- Supports dot-notation paths and wildcards
- Uses `buf.validate` for constraints

Must include:

- Filters with AND/OR recursion
- Operators with enforced operand rules
- Projection via include/exclude
- Sorting
- Pagination
- Full-text & semantic search
- Aggregation & grouping
- Explicit joins as an escape hatch
- Query options, timeout, explain flag

Must NOT:

- Encode execution semantics
- Reference storage engines
- Use typed field IDs
- Leak planner concepts

---

### CQM Layer (`/proto/query/cqm/v1`)

**Purpose:** Canonical Query Model (semantic IR)

Characteristics:

- Internal-only
- Strongly typed
- Schema-resolved
- Deterministic
- No wildcards
- No stringly-typed semantics

Must include:

- Typed `Value` model
- Resolved `FieldRef`
- Normalized predicates
- Explicit operator semantics
- Canonical projections

Must NOT:

- Be backward compatible
- Be client-facing
- Reference storage or execution concepts

---

### Plan Layer (`/proto/query/plan/v1`)

**Purpose:** Logical and physical query planning representation

Characteristics:

- Declarative
- Explainable
- Debuggable
- Planner output only

Must include:

- Logical plan nodes
- Physical plan nodes
- Node graph structure
- Explain metadata

Must NOT:

- Encode SQL, Mongo, or Elasticsearch syntax
- Contain optimizer heuristics
- Include procedural execution logic

---

## Protobuf Design Rules (NON-NEGOTIABLE)

- Use `oneof` to enforce exclusivity
- Use enums for closed sets
- Never overload fields
- Never reuse enum numbers
- Reserve removed fields and enum values
- Version only via directories (`v1`, `v2`, …)
- Every message and enum must be documented
- Prefer clarity over brevity

---

## Implementation Tasks (ALL REQUIRED)

### 1. API Protos

- Implement unified `Query`
- Recursive boolean filters
- Operator ↔ operand compatibility
- Projection include/exclude patterns
- Sorting, search, aggregation, pagination
- Explicit join modeling
- Examples in comments

### 2. CQM Protos

- Canonical query representation
- Typed values
- Resolved fields
- Deterministic structure
- No client ergonomics

### 3. Plan Protos

- Logical plan model
- Physical plan model
- Explain graph and metadata

### 4. README.md

Document:

- Overall architecture
- Responsibilities of each layer
- Transformation flow
- Versioning strategy
- What belongs in each layer
- What is intentionally not modeled

---

## Quality Gate (ENFORCED)

Before finishing, verify:

- No cross-layer imports
- No duplicated semantics
- No storage-specific leakage
- No API ergonomics in CQM
- No execution logic in Plan
- Everything is documented

If anything is ambiguous:

- Choose long-term evolution over convenience
- Choose explicitness over cleverness

---

## Failure Conditions

The task is considered **failed** if you:

- Reuse API messages inside CQM
- Blur layer boundaries
- Encode SQL-like or engine-specific syntax
- Skip documentation
- Introduce implicit semantics

---

## Execution Directive

Design first.
Then implement protobufs.
Then document.

Assume this system will live for **10+ years** and power **multiple storage engines**.

You are allowed to be opinionated.
You are not allowed to be sloppy.
