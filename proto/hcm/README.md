# Human Capital Management (HCM) Domain

**Package:** `geniustechspace.hcm`

## Overview

HCM domain manages employment records, organizational structure, and workforce data. This domain is **separate from identity** - it represents the business relationship between people and organizations, not personal identity attributes.

## Architecture

HCM is an independent domain that **references** identity but operates independently. It can exist without IDP for contractor management, external employees, or legacy workforce systems.

```
proto/hcm/
├── employee/v1/         # Employment records
└── organization/v1/     # Departments, teams, hierarchy (future)
```

## Entities

### 1. Employee (employee/v1/employee.proto)

**Employment relationship record**

- Company/organization name
- Job title, department
- Employee ID (for HR/payroll)
- Manager hierarchy (reporting structure)
- Employment type (full-time, part-time, contract, intern)
- Start/end dates
- Current position flag
- Location (tax jurisdiction)
- Job description/responsibilities

**Relationship:** Many-to-many with User (multiple employments, history)  
**PII:** Yes - Employment data is personal information  
**Use Cases:**
- HR systems: Employee records, onboarding, offboarding
- Payroll: Compensation, tax reporting
- Org charts: Reporting hierarchy, team structure
- Access control: Role-based permissions based on employment
- Compliance: Labor law, employment verification

## Design Principles

### 1. Domain Separation

```
Identity (IDP):    Who you are → Name, birthdate, profile
Contact:           How to reach you → Phone, address, email
Preferences:       How you like things → Language, theme, notifications
HCM:               Where you work → Company, job title, manager
```

Employment is NOT part of identity:
- Identity: "John Smith, born 1990-01-15"
- Employment: "Works at Acme Corp as Senior Engineer"

### 2. Employment Lifecycle

```
Hire → Active → Transfer → Termination → History
```

Timeline:
```protobuf
// Hired: 2023-01-15
Employee {
  start_date: "2023-01-15"
  is_current: true
  end_date: null
}

// Promoted: 2024-06-01
Employee {
  start_date: "2024-06-01"  // New record
  job_title: "Senior Engineer"
  is_current: true
}

// Terminated: 2025-12-31
Employee {
  end_date: "2025-12-31"
  is_current: false
}
```

### 3. Organizational Hierarchy

```protobuf
// Manager relationship
Employee {
  user_id: "alice-uuid"
  manager_id: "bob-uuid"  // Bob manages Alice
}

// Building org chart:
// CEO (manager_id: null)
//  └─ VP Engineering (manager_id: ceo_user_id)
//     └─ Senior Engineer (manager_id: vp_user_id)
```

### 4. Multi-Tenancy

Uses `tenant_path` for:
- Multi-company holding companies
- Subsidiaries and acquisitions
- Contractors working for multiple clients
- Consulting firms with client placements

Example:
```
"acme-corp/subsidiary-a"
"acme-corp/customer-1/project-team"
```

## Common Patterns

### All Entities Include
- ✅ UUID primary key (employment_id)
- ✅ User ID foreign key (links to identity)
- ✅ Hierarchical tenant path
- ✅ Employment lifecycle dates (start_date, end_date)
- ✅ Current status flag (is_current)
- ✅ Audit timestamps (created_at, updated_at, deleted_at)
- ✅ Optimistic locking (version)
- ✅ Reserved ranges for extensibility

### Reserved Field Ranges
- **15-19**: Employment-specific expansion
- **23-29**: Audit field expansion
- **31-39**: Future expansion

## Validation Rules

### Employee
- User ID: Valid UUID (required)
- Manager ID: Valid UUID (nullable)
- Employee ID: Up to 50 characters (for HR integration)
- Company: Max 255 characters
- Job title: Max 100 characters
- Department: Max 100 characters
- Location: Max 255 characters
- Employment type: Max 50 characters
- Description: Max 1000 characters
- tenant_path: 1-512 characters

### Business Rules
- start_date < end_date (if end_date set)
- Only one is_current=true per user per tenant
- manager_id cannot be user_id (no self-management)
- Soft delete preserves employment history

## Usage Examples

### Creating Employment Record

```protobuf
Employee {
  employment_id: "emp-uuid-123"
  user_id: "user-456"
  tenant_path: "acme-corp"
  company: "Acme Corporation"
  job_title: "Software Engineer"
  department: "Engineering"
  employee_id: "EMP-12345"
  manager_id: "manager-user-789"
  employment_type: "full-time"
  start_date: "2025-01-15T00:00:00Z"
  is_current: true
  location: "San Francisco, CA, USA"
  description: "Backend development, API design"
}
```

### Employment History

```protobuf
// Current position
Employee {
  employment_id: "emp-3"
  user_id: "user-456"
  job_title: "Senior Software Engineer"
  start_date: "2024-06-01"
  is_current: true
  end_date: null
}

// Previous position (same company)
Employee {
  employment_id: "emp-2"
  user_id: "user-456"
  job_title: "Software Engineer"
  start_date: "2023-01-15"
  end_date: "2024-05-31"
  is_current: false
}

// Old position (different company)
Employee {
  employment_id: "emp-1"
  user_id: "user-456"
  company: "OldCorp"
  job_title: "Junior Developer"
  start_date: "2021-06-01"
  end_date: "2022-12-31"
  is_current: false
}
```

### Org Chart Query

```sql
-- Get all direct reports
SELECT * FROM employee 
WHERE manager_id = 'bob-uuid' 
  AND is_current = true;

-- Get reporting chain
WITH RECURSIVE org_chart AS (
  SELECT * FROM employee WHERE user_id = 'alice-uuid'
  UNION ALL
  SELECT e.* FROM employee e
  INNER JOIN org_chart oc ON e.user_id = oc.manager_id
)
SELECT * FROM org_chart;
```

## API Operations

### Employee APIs (employee/api/v1/)
- CreateEmployee (onboarding)
- GetEmployee, GetEmployeeByUserId
- UpdateEmployee (job changes, transfers)
- TerminateEmployee (set end_date, is_current=false)
- ListEmployees (by tenant, by department, by manager)
- GetEmploymentHistory (all records for user)
- GetDirectReports (by manager_id)
- GetOrgChart (hierarchical organization structure)

## Events (events/v1/)

### Employment Events
- `EmployeeHired` (onboarding started)
- `EmployeeUpdated` (job change, transfer)
- `EmployeePromoted` (title/level change)
- `EmployeeTransferred` (department/location change)
- `EmployeeTerminated` (offboarding)
- `ManagerChanged` (reporting hierarchy change)
- `EmploymentHistoryCreated` (new historical record)

## Compliance

### ISO 30414 (Human Capital Reporting)
- Standard for human capital reporting metrics
- Workforce composition, diversity, productivity
- Cost, recruitment, turnover, succession planning
- Employee data: employment_type, start_date, end_date

### SOC 2 CC6.1 (Logical Access)
- Employment status drives access control
- Onboarding: Grant access based on role
- Offboarding: Revoke access immediately on termination
- Audit trail: Track employment changes

### Employment Law Compliance
- **FLSA**: Employment type (exempt/non-exempt)
- **Tax reporting**: Location determines tax jurisdiction
- **Labor law**: Start/end dates for tenure calculations
- **Benefits**: Employment type determines eligibility
- **WARN Act**: Mass layoff reporting (end_date tracking)

### Data Privacy
- **GDPR Article 88**: Employment data protection
- **CCPA**: Employment records are personal information
- Retention: Keep historical employment for legal requirements
- Right to access: Employees can request employment history

## Integration Points

### Consumed By
- **Access Control**: Role-based permissions from job title
- **Payroll**: Employee ID, location, employment type
- **Benefits**: Eligibility based on employment type, tenure
- **Org Charts**: Manager hierarchy visualization
- **Time Tracking**: Active employees for timesheet systems
- **Performance Management**: Goal setting, reviews
- **Recruiting**: Internal job postings, referrals

### References
- **Identity (IDP)**: user_id links to profile
- **Contact**: Physical location from address domain
- **Directory**: Email, phone for org directory

### Integrations
- **HR Systems**: Workday, SAP SuccessFactors, Oracle HCM
- **Payroll**: ADP, Gusto, Paychex
- **Benefits**: Zenefits, Namely
- **Background Check**: Checkr, Accurate Background
- **E-Verify**: Employment eligibility verification

## Related Documentation
- **Identity Profile:** `../idp/identity/profile/v1/README.md`
- **Contact:** `../contact/README.md`
- **Preferences:** `../preferences/README.md`

## Future Expansion

### Organization Entity (organization/v1/)
```protobuf
message Organization {
  string organization_id = 1;
  string tenant_path = 2;
  string name = 3;
  string parent_organization_id = 4;  // Hierarchy
  string organization_type = 5;  // department, team, division
}
```

### Position Entity (position/v1/)
```protobuf
message Position {
  string position_id = 1;
  string organization_id = 2;
  string job_title = 3;
  string job_code = 4;
  int32 headcount = 5;  // Approved headcount
}
```
