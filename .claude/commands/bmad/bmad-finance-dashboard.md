---
description: |
  BMad kickoff command for SAYERS Finance Dashboard project.
  A Next.js + Supabase finance data visualization and management dashboard
  with shadcn/ui components, ML-powered insights, and tax compliance features.

  Greenfield fullstack application using existing Supabase backend.

project_type: "Greenfield Fullstack"
tech_stack: "Next.js 14+, Supabase, shadcn/ui, Recharts"
---

# BMad: SAYERS Finance Dashboard

Build an aesthetic, production-ready financial dashboard for managing multi-entity finances, visualizing data with charts/graphs, and generating tax compliance documents.

## Project Type
**Greenfield Fullstack Application**
- New Next.js frontend
- Existing Supabase backend (`gshsshaodoyttdxippwx` - SAYERS DATA)
- Integration with UpBank sync and ML categorization pipeline

## Project Context

### Business Requirements
- **Multi-Entity Support:** MOKAI PTY LTD, MOK HOUSE PTY LTD, Harrison Sayers (sole trader)
- **Data Sources:** 24+ Supabase tables (transactions, invoices, ML predictions, entities, contacts)
- **Compliance:** Australian tax compliance, Indigenous business tracking
- **Integration:** UpBank sync, MindsDB ML pipeline

### Technical Stack
- **Frontend:** Next.js 14+ (App Router)
- **Backend:** Supabase (existing schema)
- **UI Library:** shadcn/ui + Tailwind CSS
- **Charts:** Recharts (recommended) or Chart.js
- **Deployment:** Vercel
- **Testing:** Vitest + React Testing Library + Playwright

## Recommended BMad Workflow
Use: `.claude/.bmad-core/workflows/greenfield-fullstack.yaml`

## Agent Execution Sequence

### Planning Phase

#### 1. **Analyst** (Market Research)
**Purpose:** Research finance dashboard UX best practices and competitive landscape

**Tasks:**
- Research: Financial SaaS dashboard design patterns (Xero, QuickBooks, Wave)
- Analyze: Chart types and data visualization for accounting
- Document: Tax compliance UX patterns for Australian businesses
- Output: `docs/market-research.md`, `docs/competitor-analysis.md`

**Command:**
```bash
/bmad:analyst "Research financial dashboard UX best practices, analyze Xero/QuickBooks/Wave dashboards, document patterns for data visualization and tax compliance interfaces"
```

#### 2. **PM** (Product Requirements)
**Purpose:** Create comprehensive PRD defining all functional and non-functional requirements

**Key Requirements to Cover:**
- **Functional:**
  - Dashboard views (overview, transactions, invoices, insights)
  - Transaction categorization and editing
  - Invoice management (create, edit, view, download)
  - Tax document generation (BAS, income statements)
  - Multi-entity switching
  - Data export capabilities
  - ML insight display and interaction
  - Anomaly detection alerts

- **Non-Functional:**
  - Security: Supabase RLS, data encryption
  - Performance: <2s page loads, virtual scrolling for large lists
  - Compliance: Australian tax regulations, audit trails
  - Accessibility: WCAG AA minimum
  - Responsive: Mobile-first design
  - Data integrity: Financial calculation accuracy

**Tasks:**
- Use template: `.bmad-core/templates/prd-tmpl.yaml`
- Define UI Design Goals (aesthetic requirements, shadcn/ui usage)
- Define Technical Assumptions (Next.js App Router, Supabase patterns)
- Create Epic List (foundation, dashboard, transactions, invoices, reports, tax)
- Define Stories with Acceptance Criteria
- Output: `docs/prd.md`

**Command:**
```bash
/bmad:pm "Create PRD for SAYERS Finance Dashboard using existing Supabase schema, focus on data visualization, transaction management, and tax compliance"
```

#### 3. **Architect** (System Design)
**Purpose:** Design Next.js application architecture and Supabase integration patterns

**Key Architectural Decisions:**
- **App Structure:**
  - Next.js 14+ App Router architecture
  - Server Components vs Client Components strategy
  - API Routes vs Server Actions for mutations
  - Layout hierarchy and nested routing

- **Supabase Integration:**
  - Client-side vs server-side queries
  - RLS policy design
  - Realtime subscription patterns
  - Database views for complex queries
  - Connection pooling strategy

- **Component Architecture:**
  - shadcn/ui component library setup
  - Custom chart wrapper components
  - Reusable financial data components
  - Form handling with React Hook Form + Zod

- **State Management:**
  - React Server Components for data fetching
  - Client state (Zustand or Context)
  - Form state (React Hook Form)
  - Optimistic updates

- **Data Access Patterns:**
  - Safe query patterns to prevent n+1 problems
  - Pagination strategies
  - Caching strategy (Next.js cache, React Query)
  - Background data sync patterns

- **Security:**
  - RLS implementation
  - Authentication flow (Supabase Auth)
  - API route protection
  - Input validation (Zod schemas)

**Tasks:**
- Use template: `.bmad-core/templates/fullstack-architecture-tmpl.yaml`
- Document Next.js app structure
- Define Supabase integration patterns
- Create component architecture diagram
- Define data access patterns
- Document security architecture
- Output: `docs/architecture.md`

**Command:**
```bash
/bmad:architect "Design Next.js + Supabase architecture for finance dashboard, focus on security, performance, and scalable component patterns with shadcn/ui"
```

#### 4. **UX Expert** (Frontend Specifications)
**Purpose:** Design component specifications and user interface details

**Key UX Deliverables:**
- **Dashboard Layout:**
  - KPI card designs
  - Chart component specifications
  - Navigation structure
  - Responsive breakpoints

- **Transaction Views:**
  - Transaction list/table design
  - Filtering and sorting controls
  - Categorization UI flow
  - Bulk edit patterns

- **Invoice Management:**
  - Invoice creation form
  - Invoice list/grid view
  - PDF preview/download
  - Status indicators

- **Reports & Tax:**
  - Report generation interface
  - Tax form download flows
  - Date range selectors
  - Export format options

- **Component Library:**
  - shadcn/ui component mapping
  - Custom chart components
  - Financial data display components
  - Form components

**Tasks:**
- Use template: `.bmad-core/templates/front-end-spec-tmpl.yaml`
- Define screen wireframes (ASCII or Markdown)
- Specify shadcn/ui components to use
- Define custom component requirements
- Create component specification table
- Document responsive behavior
- Output: `docs/front-end-spec.md`

**Command:**
```bash
/bmad:ux-expert "Create frontend specifications for finance dashboard using shadcn/ui, focus on data visualization components, financial workflows, and responsive design"
```

### Validation Phase

#### 5. **PO** (Document Alignment & Sharding)
**Purpose:** Validate PRD and Architecture alignment, shard into actionable pieces

**Tasks:**
- Run: `.bmad-core/checklists/po-master-checklist.md`
- Verify PRD ↔ Architecture alignment
- Check for gaps, conflicts, ambiguities
- Shard PRD epics into `docs/prd/epic-*.md`
- Shard Architecture sections into `docs/architecture/*.md`
- Output: Sharded files + alignment report

**Command:**
```bash
/bmad:po "Run master checklist on PRD and Architecture, shard documents into epics and technical sections"
```

#### 6. **QA** (Early Test Strategy)
**Purpose:** Define comprehensive test strategy for financial application

**Critical Test Areas:**
- **Financial Calculations:**
  - Tax calculation accuracy
  - GST computation
  - Currency handling
  - Rounding rules

- **Data Integrity:**
  - Transaction totals
  - Invoice calculations
  - Balance reconciliation

- **Security:**
  - RLS policy testing
  - Authorization checks
  - Input validation

- **Integration:**
  - Supabase query correctness
  - Real-time updates
  - ML prediction display

- **UI/UX:**
  - Responsive design
  - Chart rendering
  - Form validation
  - Error handling

**Tasks:**
- Use template: `.bmad-core/templates/qa-gate-tmpl.yaml`
- Define test pyramid (unit, integration, e2e)
- Create test case templates for financial logic
- Document test data requirements
- Define quality gates for each epic
- Output: `docs/qa/test-strategy.md`

**Command:**
```bash
/bmad:qa "Create test strategy for finance dashboard, focus on financial calculation accuracy, data integrity, and security testing"
```

### Execution Phase

#### 7. **SM** (Sprint Planning)
**Purpose:** Plan iterative delivery sprints

**Tasks:**
- Review sharded epics and stories
- Prioritize based on dependencies and value
- Create sprint backlog
- Identify blockers and risks
- Plan story sequence within sprints

**Command:**
```bash
/bmad:sm "Plan sprints for finance dashboard implementation, prioritize foundation and core features first"
```

#### 8. **Dev** (Implementation)
**Purpose:** Build the application following architecture and stories

**Implementation Sequence:**
1. **Epic 1: Foundation**
   - Next.js project setup
   - shadcn/ui configuration
   - Supabase client setup
   - Authentication flow
   - Basic layout and navigation

2. **Epic 2: Dashboard**
   - KPI calculations and display
   - Chart components
   - Recent transactions widget
   - Anomaly alerts

3. **Epic 3: Transaction Management**
   - Transaction list view
   - Filtering and search
   - Categorization UI
   - Bulk operations

4. **Epic 4: Invoice Management**
   - Invoice list/grid
   - Invoice creation form
   - PDF generation
   - Invoice status tracking

5. **Epic 5: Reports & Tax**
   - Report generation
   - Tax document creation
   - Export functionality
   - Date range filtering

**Command:**
```bash
/bmad:dev "Implement [Story X.Y] following architecture specifications and frontend component design"
```

#### 9. **QA** (Testing & Validation)
**Purpose:** Execute test strategy and validate implementation

**Tasks:**
- Run unit tests for financial calculations
- Execute integration tests for Supabase queries
- Run e2e tests for critical workflows
- Validate tax calculation accuracy
- Security testing (RLS, auth)
- Performance testing (large datasets)
- Cross-browser testing
- Mobile responsiveness testing

**Command:**
```bash
/bmad:qa "Execute test plan for [Epic/Story], validate financial calculations and data integrity"
```

## Quick Start

### Step 1: Install BMad Method (if needed)
```bash
# If BMad not yet installed in project
cd /Users/harrysayers/Developer/claudelife
# Follow BMad installation instructions
```

### Step 2: Create Project Brief
```bash
/bmad:analyst "Create project brief for SAYERS Finance Dashboard - financial data visualization and tax compliance SaaS"
```

### Step 3: Follow Agent Sequence
Execute agents in order from Planning Phase → Validation Phase → Execution Phase

### Step 4: Reference Workflow
Detailed step-by-step guide: `.claude/.bmad-core/workflows/greenfield-fullstack.yaml`

## Key Configuration

### Supabase Connection
```typescript
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
```

### Environment Variables Needed
```bash
# .env.local
NEXT_PUBLIC_SUPABASE_URL=https://gshsshaodoyttdxippwx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<your-anon-key>
SUPABASE_SERVICE_ROLE_KEY=<your-service-role-key>
```

### shadcn/ui Setup
```bash
# Initialize shadcn/ui in Next.js project
npx shadcn-ui@latest init

# Install commonly needed components
npx shadcn-ui@latest add button card table form select dropdown-menu
npx shadcn-ui@latest add dialog sheet toast tabs navigation-menu
```

### Chart Library Setup
```bash
# Recharts (recommended for React integration)
npm install recharts

# Alternative: Chart.js with react-chartjs-2
npm install chart.js react-chartjs-2
```

## Templates to Use

### Planning Phase
- [x] `.bmad-core/templates/project-brief-tmpl.yaml` - Initial project brief
- [x] `.bmad-core/templates/market-research-tmpl.yaml` - Finance dashboard research
- [x] `.bmad-core/templates/competitor-analysis-tmpl.yaml` - Xero/QuickBooks analysis
- [x] `.bmad-core/templates/prd-tmpl.yaml` - Product requirements
- [x] `.bmad-core/templates/fullstack-architecture-tmpl.yaml` - Architecture design
- [x] `.bmad-core/templates/front-end-spec-tmpl.yaml` - UI specifications

### Execution Phase
- [ ] `.bmad-core/templates/story-tmpl.yaml` - User stories (repeated per story)
- [ ] `.bmad-core/templates/qa-gate-tmpl.yaml` - Quality checkpoints (per epic)

## Technical Documents to Create

Beyond BMad templates, create these custom technical documents:

1. **`docs/supabase-schema.md`**
   - Document all 24+ tables and relationships
   - Define RLS policies
   - Document database views and functions

2. **`docs/data-access-patterns.md`**
   - Safe query patterns to prevent n+1 queries
   - Pagination strategies
   - Join patterns for complex queries
   - Caching strategies

3. **`docs/tax-compliance-rules.md`**
   - Australian tax calculation logic
   - GST computation rules
   - BAS statement generation
   - Income tax document requirements

4. **`docs/ml-integration.md`**
   - How ML predictions are structured
   - Displaying confidence scores
   - Handling anomaly alerts
   - AI insight interpretation

5. **`docs/component-library.md`**
   - shadcn/ui components in use
   - Custom chart wrapper components
   - Financial data display components
   - Form component standards

## Notes

### Project-Specific Considerations

**Security Critical:**
- This app handles real financial data for multiple business entities
- Implement comprehensive RLS policies in Supabase
- Add audit trails for all data modifications
- Validate all calculations server-side
- Never trust client-side computations for tax/financial data

**Performance Critical:**
- Transaction tables can have thousands of rows
- Implement virtual scrolling for large lists
- Use database views for complex aggregations
- Optimize chart rendering with data sampling for large datasets
- Consider caching frequently accessed reports

**UX Critical:**
- Financial dashboards require specialized UX (not generic CRUD)
- Clear visual hierarchy for KPIs and alerts
- Intuitive categorization workflows
- Export/download must be reliable
- Mobile access for quick checks on-the-go

**Compliance Critical:**
- Australian tax calculation accuracy is non-negotiable
- Document all tax logic with references to ATO guidelines
- Implement comprehensive test coverage for tax calculations
- Add ability to export for accountant review
- Maintain audit trail for compliance

### Constraints

- **Cannot modify Supabase schema** - work with existing 24+ tables
- **Must integrate with existing UpBank sync** - display synced data
- **Must display ML predictions** - integrate with MindsDB pipeline
- **Multi-entity awareness** - support MOKAI, MOK HOUSE, personal
- **Indigenous business compliance** - track Supply Nation certification, etc.

### shadcn/ui Component Setup

Since shadcn MCP wasn't found on your system, you'll need to:

1. **Initialize manually:**
   ```bash
   npx shadcn-ui@latest init
   ```

2. **Install core components:**
   - Data Display: `table`, `card`, `badge`, `skeleton`
   - Forms: `form`, `input`, `select`, `date-picker`, `combobox`
   - Navigation: `navigation-menu`, `tabs`, `breadcrumb`
   - Feedback: `toast`, `alert`, `dialog`, `sheet`
   - Charts: Build custom wrappers around Recharts using shadcn Card

3. **Document in Architecture:**
   - List all shadcn components used
   - Define custom component patterns
   - Create reusable chart wrapper components

### Data Model Key Tables

**Core Entities:**
- `entities` - MOKAI, MOK HOUSE, Harrison Sayers
- `contacts` - Customers, suppliers, employees
- `bank_accounts` - UpBank accounts

**Transactions:**
- `transactions` - Business transactions with ML categorization
- `personal_transactions` - UpBank synced transactions
- `transaction_lines` - Line items with account coding

**Financial:**
- `invoices` - Receivables and payables
- `accounts` - Chart of accounts

**ML/AI:**
- `ml_models` - MindsDB model tracking
- `ai_predictions` - ML predictions with confidence scores
- `anomaly_detections` - Unusual transaction alerts
- `ai_insights` - Business intelligence insights

### Next Actions

1. **Immediate:** Run Analyst for market research
2. **Then:** Create PRD with PM agent
3. **Then:** Design architecture with Architect agent
4. **Then:** Create frontend specs with UX Expert
5. **Then:** Validate with PO and QA
6. **Finally:** Begin implementation with Dev agent

### Success Metrics

**Technical:**
- <2s page load times
- <100ms chart render times
- 100% test coverage on financial calculations
- Zero security vulnerabilities
- Mobile-responsive (down to 320px)

**Business:**
- Accurate tax calculations (100% match with accountant review)
- Reduced manual bookkeeping time (target: 50% reduction)
- Real-time financial insights available 24/7
- Professional invoice generation
- Export compatibility with major accounting software

**User:**
- Intuitive categorization workflow (<5 clicks per transaction)
- Clear visual hierarchy (tested with users)
- Fast transaction search (<1s for any query)
- Reliable PDF generation and download
- Mobile access for quick financial checks
