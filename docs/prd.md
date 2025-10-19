---
date: "2025-10-17"
version: "1.0"
status: "Draft"
project: "SAYERS Financial Dashboard"
author: "PM Agent (BMad Method)"
---

# Product Requirements Document
## SAYERS Financial Dashboard

### Document Control
- **Version**: 1.0
- **Status**: Draft
- **Last Updated**: 2025-10-17
- **Project Type**: Greenfield Fullstack Application
- **Tech Stack**: Next.js 14+, Supabase, shadcn/ui v4, TypeScript

---

## 1. Executive Summary

### 1.1 Project Vision
Build a comprehensive financial management dashboard that provides complete visibility and control over personal and multi-business entity finances in a single unified system.

### 1.2 Target Users
**Primary User**: Harrison Robert Sayers
- **Personal**: Individual financial tracking via UpBank integration
- **MOKAI PTY LTD**: Indigenous technology consultancy (cybersecurity, GRC, IRAP)
- **MOK HOUSE PTY LTD**: Music production and creative services

### 1.3 Business Goals
1. **Financial Visibility**: Real-time view of all financial activity across entities
2. **Tax Compliance**: Accurate Australian tax reporting (BAS, P&L, Balance Sheet)
3. **Efficiency**: Reduce manual bookkeeping time by 50%
4. **Insights**: ML-powered categorization and anomaly detection
5. **Cash Flow**: Predictive forecasting for business planning

### 1.4 Success Metrics
- **Adoption**: Daily active usage for financial decision-making
- **Accuracy**: 100% match with accountant-verified calculations
- **Performance**: <2s page load, <100ms chart render
- **Time Savings**: 50% reduction in manual bookkeeping time
- **Coverage**: 100% of transactions categorized and tracked

---

## 2. Problem Statement

### 2.1 Current Pain Points
1. **Fragmented Data**: Financial data spread across UpBank, invoices, receipts, spreadsheets
2. **Manual Tracking**: Time-consuming manual categorization and reconciliation
3. **Limited Visibility**: No real-time view of cash flow or spending patterns
4. **Tax Complexity**: Difficult to separate personal vs business expenses for Australian tax
5. **Multi-Entity Chaos**: Managing MOKAI, MOK HOUSE, and personal finances separately
6. **No Forecasting**: Reactive rather than proactive financial management
7. **Reconciliation Errors**: Manual processes prone to mistakes

### 2.2 Why Now?
- **Data Infrastructure Ready**: 23 Supabase tables with 300+ rows already established
- **UpBank Integration Live**: 256 personal transactions syncing automatically
- **ML Pipeline Active**: MindsDB categorization and anomaly detection operational
- **Business Growth**: MOKAI and MOK HOUSE scaling, need professional financial management
- **Tax Season**: Australian BAS compliance requires accurate quarterly reporting

### 2.3 Impact of Not Solving
- Continued inefficiency and time waste on manual bookkeeping
- Risk of tax errors and non-compliance
- Poor financial decision-making due to lack of visibility
- Missed opportunities for cost optimization
- Potential cash flow crises without forecasting

---

## 3. User Stories & Use Cases

### Phase 1: Transaction & Spending Tracking (MVP)

#### Epic 1.1: Unified Transaction View
**As a** user
**I want to** see all transactions (personal + business) in one place
**So that** I have complete financial visibility

**User Stories:**
1. **View All Transactions**
   - As a user, I want to see a unified list of all transactions from personal_transactions and transactions tables
   - **Acceptance Criteria**:
     - Display transaction date, description, amount, category, entity
     - Show ML-assigned category and confidence score
     - Include project tags (DiDi, Repco, Nintendo, etc.)
     - Support pagination (50 transactions per page)
     - Load initial view in <2 seconds
   - **Priority**: Must Have
   - **Dependencies**: None

2. **Filter by Entity**
   - As a user, I want to filter transactions by entity (Personal/MOKAI/MOK HOUSE)
   - **Acceptance Criteria**:
     - Entity selector dropdown in header
     - Filter persists across page navigation
     - Show entity-specific totals
     - Update charts to match filter
   - **Priority**: Must Have
   - **Dependencies**: Story 1.1.1

3. **Search Transactions**
   - As a user, I want to search transactions by description, amount, or category
   - **Acceptance Criteria**:
     - Real-time search (debounced 300ms)
     - Match partial strings in description
     - Support amount ranges (e.g., "$50-$100")
     - Highlight search terms in results
   - **Priority**: Must Have
   - **Dependencies**: Story 1.1.1

#### Epic 1.2: Category Breakdown & Analysis
**As a** user
**I want to** see spending broken down by category
**So that** I understand where money is going

**User Stories:**
1. **Category Spending Chart**
   - As a user, I want to see a pie/donut chart of spending by category
   - **Acceptance Criteria**:
     - Show top 10 categories with percentages
     - "Other" category for remaining
     - Responsive design (mobile-friendly)
     - Click category to drill down to transactions
   - **Priority**: Must Have
   - **Dependencies**: Story 1.1.1

2. **Spending Trends Over Time**
   - As a user, I want to see spending trends by month/week
   - **Acceptance Criteria**:
     - Line chart with time selector (week/month/quarter/year)
     - Compare current period to previous
     - Show trend direction (up/down percentage)
     - Export chart as PNG/PDF
   - **Priority**: Should Have
   - **Dependencies**: Story 1.2.1

#### Epic 1.3: Project-Based Tracking
**As a** business owner
**I want to** track expenses by project
**So that** I can understand project profitability

**User Stories:**
1. **Project Filter**
   - As a user, I want to filter transactions by project (DiDi, Repco, Nintendo, etc.)
   - **Acceptance Criteria**:
     - Project selector shows all active projects
     - Display project-specific totals
     - Show project timeline (start/end dates)
     - Calculate project ROI if revenue data available
   - **Priority**: Should Have
   - **Dependencies**: Story 1.1.1

### Phase 2: Invoicing & Cash Flow

#### Epic 2.1: Invoice Management
**As a** business owner
**I want to** manage receivables and payables
**So that** I can track what I'm owed and what I owe

**User Stories:**
1. **Invoice List View**
   - As a user, I want to see all invoices with status indicators
   - **Acceptance Criteria**:
     - Display invoice number, contact, amount, due date, status
     - Color-coded status (draft/sent/paid/overdue)
     - Sort by date, amount, status
     - Filter by entity, contact, status, date range
   - **Priority**: Must Have
   - **Dependencies**: None

2. **Create Invoice**
   - As a user, I want to create new invoices
   - **Acceptance Criteria**:
     - Form validation (required fields: contact, amount, due date)
     - Line item support with descriptions
     - GST calculation (10% Australian tax)
     - Auto-increment invoice numbers
     - Save as draft or mark sent
   - **Priority**: Must Have
   - **Dependencies**: Story 2.1.1

3. **Invoice Payment Tracking**
   - As a user, I want to mark invoices as paid
   - **Acceptance Criteria**:
     - Record payment date and method
     - Link to bank transaction if applicable
     - Calculate days to payment (for metrics)
     - Update account balances
   - **Priority**: Must Have
   - **Dependencies**: Story 2.1.1, 2.1.2

4. **Generate Invoice PDF**
   - As a user, I want to download professional invoice PDFs
   - **Acceptance Criteria**:
     - Professional template with logo/branding
     - Include all invoice details + line items
     - Show GST breakdown
     - Include payment instructions
   - **Priority**: Should Have
   - **Dependencies**: Story 2.1.2

#### Epic 2.2: Cash Flow Dashboard
**As a** business owner
**I want to** visualize cash flow over time
**So that** I can plan for future expenses and investments

**User Stories:**
1. **Cash Flow Timeline**
   - As a user, I want to see inflows and outflows over time
   - **Acceptance Criteria**:
     - Waterfall chart showing daily/weekly/monthly cash flow
     - Separate bars for income vs expenses
     - Running balance line overlay
     - Zoom to specific time periods
   - **Priority**: Must Have
   - **Dependencies**: Story 2.1.1

2. **Cash Flow Forecasting**
   - As a user, I want to see predicted future cash flow
   - **Acceptance Criteria**:
     - Use ML predictions from cash_flow_forecasts table
     - Show confidence intervals
     - Include recurring transactions
     - Highlight predicted low-balance periods
   - **Priority**: Should Have
   - **Dependencies**: Story 2.2.1

3. **Overdue Invoice Alerts**
   - As a user, I want to be notified of overdue invoices
   - **Acceptance Criteria**:
     - Dashboard alert badge showing count
     - List of overdue invoices with days overdue
     - One-click to send reminder email
     - Track reminder history
   - **Priority**: Should Have
   - **Dependencies**: Story 2.1.1

### Phase 3: Budgeting & Alerts

#### Epic 3.1: Budget Creation & Tracking
**As a** user
**I want to** set budgets by category
**So that** I can control spending

**User Stories:**
1. **Create Budgets**
   - As a user, I want to set monthly budgets by category
   - **Acceptance Criteria**:
     - Budget form with category selector and amount
     - Support multiple time periods (weekly/monthly/yearly)
     - Copy budgets from previous period
     - Entity-specific budgets
   - **Priority**: Should Have
   - **Dependencies**: Story 1.2.1

2. **Budget vs Actual**
   - As a user, I want to compare budget to actual spending
   - **Acceptance Criteria**:
     - Progress bars showing percentage spent
     - Color coding (green/yellow/red based on threshold)
     - Show remaining budget
     - Trend indicator (on track/over budget/under budget)
   - **Priority**: Should Have
   - **Dependencies**: Story 3.1.1

#### Epic 3.2: Spending Alerts
**As a** user
**I want to** receive alerts when approaching budget limits
**So that** I can adjust spending proactively

**User Stories:**
1. **Budget Alert System**
   - As a user, I want alerts at 80% and 100% of budget
   - **Acceptance Criteria**:
     - Dashboard notification badge
     - Alert list with category and percentage
     - Dismissible notifications
     - Email alerts (optional)
   - **Priority**: Could Have
   - **Dependencies**: Story 3.1.2

#### Epic 3.3: Anomaly Detection
**As a** user
**I want to** be alerted to unusual transactions
**So that** I can catch errors or fraud

**User Stories:**
1. **Anomaly Alerts**
   - As a user, I want to see transactions flagged as anomalies
   - **Acceptance Criteria**:
     - Use anomaly_score from ML pipeline
     - Show anomalies on dashboard
     - Explain why transaction is flagged
     - Allow marking as normal/fraud
   - **Priority**: Should Have
   - **Dependencies**: Story 1.1.1

### Phase 4: Accounting & Reporting

#### Epic 4.1: Profit & Loss Statement
**As a** business owner
**I want to** generate P&L statements
**So that** I can understand business profitability

**User Stories:**
1. **P&L Report Generation**
   - As a user, I want to generate P&L for a date range
   - **Acceptance Criteria**:
     - Calculate revenue (income accounts)
     - Calculate expenses (expense accounts)
     - Show gross profit, operating profit, net profit
     - Compare to previous period
     - Export to PDF/Excel
   - **Priority**: Must Have
   - **Dependencies**: None

2. **Multi-Entity P&L Comparison**
   - As a user, I want to compare P&L across entities
   - **Acceptance Criteria**:
     - Side-by-side comparison table
     - Highlight variance (positive/negative)
     - Consolidate all entities option
     - Drill down to account level
   - **Priority**: Should Have
   - **Dependencies**: Story 4.1.1

#### Epic 4.2: Balance Sheet
**As a** business owner
**I want to** generate balance sheets
**So that** I can understand financial position

**User Stories:**
1. **Balance Sheet Report**
   - As a user, I want to see assets, liabilities, and equity
   - **Acceptance Criteria**:
     - Calculate from accounts table (52 accounts)
     - Show current balances
     - Group by account type (asset/liability/equity)
     - Verify accounting equation (Assets = Liabilities + Equity)
   - **Priority**: Must Have
   - **Dependencies**: None

#### Epic 4.3: BAS Statement Generation
**As an** Australian business owner
**I want to** generate BAS statements
**So that** I can comply with quarterly tax reporting

**User Stories:**
1. **BAS Calculation**
   - As a user, I want to calculate GST for BAS
   - **Acceptance Criteria**:
     - Calculate GST collected (sales)
     - Calculate GST paid (purchases)
     - Compute net GST owing/refund
     - Match ATO BAS form structure
     - Include all required fields (G1, 1A, 1B, etc.)
   - **Priority**: Must Have
   - **Dependencies**: Story 1.1.1

2. **Export BAS for ATO Lodgment**
   - As a user, I want to export BAS in ATO-compatible format
   - **Acceptance Criteria**:
     - Generate PDF matching ATO form
     - Include all required metadata
     - Validate calculations
     - Provide export for accountant review
   - **Priority**: Must Have
   - **Dependencies**: Story 4.3.1

#### Epic 4.4: Chart of Accounts
**As a** user
**I want to** view account balances and transactions
**So that** I can verify financial accuracy

**User Stories:**
1. **Account List View**
   - As a user, I want to see all accounts with balances
   - **Acceptance Criteria**:
     - Display 52 accounts from accounts table
     - Show current balance, account type, description
     - Sort by type, name, balance
     - Search by account name/code
   - **Priority**: Should Have
   - **Dependencies**: None

2. **Account Transaction History**
   - As a user, I want to see all transactions for an account
   - **Acceptance Criteria**:
     - Drill down from account to transactions
     - Show running balance
     - Filter by date range
     - Export to CSV
   - **Priority**: Should Have
   - **Dependencies**: Story 4.4.1

### Phase 5: Analytics & ML Insights

#### Epic 5.1: AI Insights Dashboard
**As a** user
**I want to** see ML-generated financial insights
**So that** I can make better financial decisions

**User Stories:**
1. **Insight Display**
   - As a user, I want to see AI-generated insights on dashboard
   - **Acceptance Criteria**:
     - Display insights from ai_insights table
     - Show insight type, description, confidence
     - Prioritize high-confidence insights
     - Link to relevant data (transaction/category)
   - **Priority**: Should Have
   - **Dependencies**: None

#### Epic 5.2: Spending Trends & Predictions
**As a** user
**I want to** see historical trends and future predictions
**So that** I can anticipate financial needs

**User Stories:**
1. **Trend Analysis**
   - As a user, I want to see spending trends by category
   - **Acceptance Criteria**:
     - Line charts showing historical trends
     - Identify seasonal patterns
     - Show year-over-year comparison
     - Highlight significant changes
   - **Priority**: Should Have
   - **Dependencies**: Story 1.2.1

2. **Predictive Spending**
   - As a user, I want to see predicted future spending
   - **Acceptance Criteria**:
     - Use ML predictions from ai_predictions table
     - Show confidence intervals
     - Explain prediction basis
     - Update monthly based on new data
   - **Priority**: Could Have
   - **Dependencies**: Story 5.2.1

### Phase 6: Polish & UX

#### Epic 6.1: Export Capabilities
**As a** user
**I want to** export data in various formats
**So that** I can use data in other systems

**User Stories:**
1. **Export to CSV/Excel**
   - As a user, I want to export any table/report to CSV/Excel
   - **Acceptance Criteria**:
     - Export button on all data views
     - Preserve formatting and calculations
     - Include filters applied
     - Filename includes date range
   - **Priority**: Should Have
   - **Dependencies**: None

2. **PDF Report Generation**
   - As a user, I want to generate PDF reports
   - **Acceptance Criteria**:
     - Professional formatting
     - Include charts as images
     - Header with logo and date
     - Page numbers and table of contents
   - **Priority**: Should Have
   - **Dependencies**: Story 6.1.1

#### Epic 6.2: Mobile Responsiveness
**As a** user
**I want to** access the dashboard on mobile
**So that** I can check finances on-the-go

**User Stories:**
1. **Mobile-Optimized Layout**
   - As a user, I want the dashboard to work on mobile
   - **Acceptance Criteria**:
     - Responsive design down to 320px width
     - Touch-friendly controls
     - Simplified charts for small screens
     - Fast mobile performance (<3s load on 4G)
   - **Priority**: Should Have
   - **Dependencies**: All Phase 1-5 epics

#### Epic 6.3: Keyboard Shortcuts
**As a** power user
**I want to** use keyboard shortcuts
**So that** I can work more efficiently

**User Stories:**
1. **Navigation Shortcuts**
   - As a user, I want keyboard shortcuts for common actions
   - **Acceptance Criteria**:
     - `Cmd+K` for search
     - `Cmd+N` for new invoice/transaction
     - `Cmd+E` for entity switcher
     - `?` to show shortcut help
   - **Priority**: Could Have
   - **Dependencies**: Phase 1-4 epics

---

## 4. Functional Requirements

### 4.1 Data Model Requirements

#### 4.1.1 Multi-Entity Data Segregation
- **FR-001**: System MUST support data segregation for Personal, MOKAI, MOK HOUSE
- **FR-002**: Entity selector MUST be visible on all screens
- **FR-003**: Selected entity MUST persist across sessions (localStorage)
- **FR-004**: All queries MUST filter by selected entity (except consolidated views)

#### 4.1.2 Transaction Management
- **FR-010**: System MUST display both personal_transactions and transactions tables
- **FR-011**: System MUST show ML-assigned category and confidence score
- **FR-012**: Users MUST be able to override AI categorization
- **FR-013**: System MUST track project tags (DiDi, Repco, Nintendo, etc.)
- **FR-014**: Transaction edits MUST be audited (created_at, updated_at)

#### 4.1.3 Invoice Operations
- **FR-020**: Users MUST be able to create, edit, view, delete invoices
- **FR-021**: System MUST calculate GST at 10% for Australian tax
- **FR-022**: Invoice numbers MUST auto-increment per entity
- **FR-023**: System MUST track invoice status (draft/sent/paid/overdue)
- **FR-024**: System MUST support line items with descriptions

#### 4.1.4 Financial Calculations
- **FR-030**: All financial calculations MUST be performed server-side
- **FR-031**: System MUST validate accounting equation (Assets = Liabilities + Equity)
- **FR-032**: GST calculations MUST match ATO requirements
- **FR-033**: Currency amounts MUST use precise decimal handling (no floating point errors)
- **FR-034**: P&L and Balance Sheet MUST calculate from accounts table

#### 4.1.5 Reporting
- **FR-040**: Users MUST be able to generate P&L for any date range
- **FR-041**: Users MUST be able to generate Balance Sheet for any date
- **FR-042**: Users MUST be able to generate BAS quarterly reports
- **FR-043**: All reports MUST be exportable to PDF, CSV, Excel
- **FR-044**: Reports MUST show comparison to previous period

### 4.2 Integration Requirements

#### 4.2.1 Supabase Integration
- **FR-050**: System MUST connect to Supabase project `gshsshaodoyttdxippwx`
- **FR-051**: System MUST use TypeScript types generated from Supabase schema
- **FR-052**: System MUST implement Row-Level Security (RLS) policies
- **FR-053**: System MUST handle Supabase errors gracefully

#### 4.2.2 UpBank Sync
- **FR-060**: System MUST display UpBank-synced personal transactions
- **FR-061**: System MUST show sync status and last sync time
- **FR-062**: System MUST handle sync errors from sync_errors table

#### 4.2.3 ML Pipeline
- **FR-070**: System MUST display ML categorizations from MindsDB
- **FR-071**: System MUST show confidence scores for AI predictions
- **FR-072**: System MUST display anomaly detections with explanations
- **FR-073**: System MUST visualize cash flow forecasts

### 4.3 User Interface Requirements

#### 4.3.1 Dashboard Layout
- **FR-080**: Dashboard MUST show KPIs (total income, expenses, net, cash balance)
- **FR-081**: Dashboard MUST display recent transactions (last 10)
- **FR-082**: Dashboard MUST show spending breakdown chart
- **FR-083**: Dashboard MUST alert on overdue invoices
- **FR-084**: Dashboard MUST show anomaly alerts

#### 4.3.2 Navigation
- **FR-090**: Navigation MUST include: Dashboard, Transactions, Invoices, Reports, Insights
- **FR-091**: Entity selector MUST be in header/navigation
- **FR-092**: Navigation MUST indicate current page
- **FR-093**: Navigation MUST work on mobile (hamburger menu)

#### 4.3.3 Data Visualization
- **FR-100**: Charts MUST use Recharts library
- **FR-101**: Charts MUST be responsive (mobile-friendly)
- **FR-102**: Charts MUST support click-to-drill-down
- **FR-103**: Charts MUST be exportable as PNG/PDF
- **FR-104**: Charts MUST render in <100ms for datasets <1000 points

#### 4.3.4 Forms
- **FR-110**: Forms MUST use React Hook Form + Zod validation
- **FR-111**: Forms MUST show inline validation errors
- **FR-112**: Forms MUST prevent submission with invalid data
- **FR-113**: Forms MUST show loading states during submission
- **FR-114**: Forms MUST handle server errors gracefully

#### 4.3.5 Tables
- **FR-120**: Tables MUST support sorting, filtering, pagination
- **FR-121**: Tables MUST use virtual scrolling for >100 rows
- **FR-122**: Tables MUST support bulk selection
- **FR-123**: Tables MUST be mobile-responsive (horizontal scroll)
- **FR-124**: Tables MUST show loading skeletons

---

## 5. Non-Functional Requirements

### 5.1 Performance

#### 5.1.1 Load Times
- **NFR-001**: Initial page load MUST be <2 seconds on 4G
- **NFR-002**: Subsequent navigation MUST be <500ms (SPA-style)
- **NFR-003**: Chart rendering MUST be <100ms for datasets <1000 points
- **NFR-004**: Transaction search MUST return results in <200ms

#### 5.1.2 Scalability
- **NFR-010**: System MUST handle 10,000+ transactions without performance degradation
- **NFR-011**: System MUST support 100+ invoices per entity
- **NFR-012**: System MUST scale from 300 to 100,000+ database rows
- **NFR-013**: Virtual scrolling MUST handle lists of 50,000+ items

#### 5.1.3 Optimization
- **NFR-020**: Code splitting MUST be used for each phase (6 bundles)
- **NFR-021**: Heavy chart components MUST be lazy-loaded
- **NFR-022**: Images/assets MUST be optimized and CDN-served
- **NFR-023**: API responses MUST be cached appropriately

### 5.2 Security

#### 5.2.1 Authentication
- **NFR-030**: System MUST use Supabase Authentication
- **NFR-031**: Sessions MUST expire after 7 days of inactivity
- **NFR-032**: System MUST support password reset flow
- **NFR-033**: System MUST enforce strong password requirements

#### 5.2.2 Authorization
- **NFR-040**: System MUST implement Row-Level Security (RLS) in Supabase
- **NFR-041**: Users MUST only access data for their entities
- **NFR-042**: API routes MUST validate authentication before processing
- **NFR-043**: Server actions MUST validate permissions

#### 5.2.3 Data Protection
- **NFR-050**: All data in transit MUST be encrypted (HTTPS)
- **NFR-051**: All data at rest MUST be encrypted (Supabase default)
- **NFR-052**: Sensitive data MUST NOT be logged
- **NFR-053**: Financial data MUST comply with Australian privacy laws

#### 5.2.4 Input Validation
- **NFR-060**: All user inputs MUST be validated server-side
- **NFR-061**: SQL injection MUST be prevented (Supabase parameterized queries)
- **NFR-062**: XSS attacks MUST be prevented (React auto-escaping + CSP)
- **NFR-063**: CSRF attacks MUST be prevented (Next.js built-in protection)

### 5.3 Reliability

#### 5.3.1 Uptime
- **NFR-070**: System MUST have 99.9% uptime (Vercel + Supabase SLA)
- **NFR-071**: Planned maintenance MUST be <1 hour per month
- **NFR-072**: System MUST gracefully handle Supabase outages

#### 5.3.2 Error Handling
- **NFR-080**: All errors MUST be logged (Sentry or similar)
- **NFR-081**: Users MUST see friendly error messages (not stack traces)
- **NFR-082**: Critical errors MUST trigger alerts
- **NFR-083**: System MUST recover from transient errors (retry logic)

#### 5.3.3 Data Integrity
- **NFR-090**: Financial calculations MUST be accurate to 2 decimal places
- **NFR-091**: Database transactions MUST be used for multi-step operations
- **NFR-092**: System MUST prevent duplicate transactions
- **NFR-093**: System MUST maintain audit trails for all data changes

### 5.4 Accessibility

#### 5.4.1 WCAG Compliance
- **NFR-100**: System MUST meet WCAG 2.1 AA standards
- **NFR-101**: All interactive elements MUST be keyboard accessible
- **NFR-102**: Color contrast MUST meet 4.5:1 ratio
- **NFR-103**: Screen readers MUST be fully supported

#### 5.4.2 Usability
- **NFR-110**: System MUST work on latest 2 versions of Chrome, Firefox, Safari, Edge
- **NFR-111**: System MUST work on iOS Safari and Android Chrome
- **NFR-112**: System MUST support browser zoom up to 200%
- **NFR-113**: Forms MUST provide clear validation feedback

### 5.5 Maintainability

#### 5.5.1 Code Quality
- **NFR-120**: TypeScript MUST be used throughout (100% type coverage)
- **NFR-121**: Code MUST follow ESLint rules (Airbnb style)
- **NFR-122**: Components MUST be documented with JSDoc
- **NFR-123**: Complex logic MUST have inline comments

#### 5.5.2 Testing
- **NFR-130**: Financial calculation functions MUST have 100% test coverage
- **NFR-131**: Critical user flows MUST have E2E tests
- **NFR-132**: All components MUST have unit tests
- **NFR-133**: Integration tests MUST cover Supabase queries

#### 5.5.3 Documentation
- **NFR-140**: API routes MUST be documented
- **NFR-141**: Component props MUST be documented
- **NFR-142**: Database schema MUST be documented
- **NFR-143**: Deployment process MUST be documented

---

## 6. Technical Constraints

### 6.1 Technology Stack

#### 6.1.1 Framework
- **Next.js 14+** with App Router (Required)
  - Rationale: SSR for SEO, Server Components for performance, Vercel optimization
  - Constraint: Must use App Router (not Pages Router)

#### 6.1.2 Language
- **TypeScript 5+** (Required)
  - Rationale: Type safety critical for financial calculations
  - Constraint: 100% TypeScript, no JavaScript files

#### 6.1.3 Database
- **Supabase** (Fixed)
  - Project: `gshsshaodoyttdxippwx`
  - Constraint: Cannot modify existing schema (23 tables)
  - Rationale: Existing data and integrations

#### 6.1.4 UI Library
- **shadcn/ui v4** (Required)
  - Rationale: Modern, accessible, customizable components
  - Constraint: Must use shadcn components where available

#### 6.1.5 Charts
- **Recharts** (Recommended)
  - Rationale: React integration, shadcn default, good performance
  - Alternative: Chart.js if Recharts insufficient

#### 6.1.6 State Management
- **React Query** (Server state)
- **Zustand** (Client state)
  - Rationale: Simple, performant, type-safe

#### 6.1.7 Forms
- **React Hook Form + Zod** (Required)
  - Rationale: Type-safe validation, good performance
  - Constraint: All forms must use this stack

### 6.2 Deployment

#### 6.2.1 Hosting
- **Vercel** (Free Tier)
  - Constraint: Must stay within free tier limits initially
  - Limits: 100GB bandwidth, 100 serverless function executions/day
  - Upgrade path: Pro tier ($20/month) if needed

#### 6.2.2 CI/CD
- **Vercel Auto-Deploy** from Git
  - Constraint: Must use Git for version control
  - Preview deployments for all PRs

### 6.3 External Integrations

#### 6.3.1 UpBank (Fixed)
- Constraint: Must display synced data from personal_transactions
- Constraint: Cannot modify UpBank sync logic (separate system)

#### 6.3.2 MindsDB ML Pipeline (Fixed)
- Constraint: Must display ML predictions as-is
- Constraint: Cannot retrain models from dashboard

### 6.4 Data Constraints

#### 6.4.1 Existing Schema
- **23 Supabase Tables** (Cannot modify)
  - See Section 7 for complete schema documentation

#### 6.4.2 Multi-Entity Support
- Entities: Personal, MOKAI PTY LTD, MOK HOUSE PTY LTD
- Constraint: All data must be segregated by entity

#### 6.4.3 Australian Tax Compliance
- Constraint: GST must be calculated at 10%
- Constraint: BAS statements must match ATO format
- Constraint: Financial year is July 1 - June 30

---

## 7. Data Model & Schema

### 7.1 Core Entities

#### 7.1.1 Entities Table (3 rows)
```typescript
interface Entity {
  id: uuid
  name: string // "MOKAI PTY LTD", "MOK HOUSE PTY LTD", "Harrison Sayers"
  type: string // "company", "individual"
  abn?: string
  tax_id?: string
  created_at: timestamp
  updated_at: timestamp
}
```

#### 7.1.2 Contacts Table (3 rows)
```typescript
interface Contact {
  id: uuid
  entity_id: uuid // FK to entities
  name: string
  type: string // "customer", "supplier", "employee"
  email?: string
  phone?: string
  abn?: string
  created_at: timestamp
  updated_at: timestamp
}
```

#### 7.1.3 Bank Accounts Table (3 rows)
```typescript
interface BankAccount {
  id: uuid
  entity_id: uuid
  account_name: string
  account_number: string
  bsb?: string
  balance: decimal
  currency: string // "AUD"
  created_at: timestamp
  updated_at: timestamp
}
```

### 7.2 Transactions

#### 7.2.1 Personal Transactions - UpBank (256 rows)
```typescript
interface PersonalTransaction {
  id: uuid
  account_id: uuid // FK to personal_accounts
  description: string
  amount: decimal
  transaction_date: timestamp
  category_id?: uuid // FK to personal_finance_categories
  upbank_category_id?: uuid // FK to upbank_categories
  ai_category?: string // ML-assigned
  ai_confidence?: decimal // 0-1
  ml_features?: jsonb
  anomaly_score?: decimal
  is_business_expense: boolean
  project?: string // "DiDi", "Repco", "Nintendo"
  created_at: timestamp
  updated_at: timestamp
}
```

#### 7.2.2 Business Transactions (1 row)
```typescript
interface Transaction {
  id: uuid
  entity_id: uuid
  account_id: uuid // FK to accounts (chart of accounts)
  description: string
  amount: decimal
  transaction_date: timestamp
  type: string // "income", "expense"
  category?: string
  ai_category?: string
  ai_confidence?: decimal
  ml_features?: jsonb
  anomaly_score?: decimal
  project?: string
  contact_id?: uuid
  invoice_id?: uuid
  created_at: timestamp
  updated_at: timestamp
}
```

### 7.3 Invoicing

#### 7.3.1 Invoices Table (30 rows)
```typescript
interface Invoice {
  id: uuid
  entity_id: uuid
  invoice_number: string
  contact_id: uuid // customer or supplier
  type: string // "receivable", "payable"
  status: string // "draft", "sent", "paid", "overdue"
  issue_date: date
  due_date: date
  subtotal: decimal
  gst_amount: decimal // 10% of subtotal
  total: decimal
  payment_date?: date
  payment_method?: string
  notes?: string
  created_at: timestamp
  updated_at: timestamp
}
```

### 7.4 Chart of Accounts

#### 7.4.1 Accounts Table (52 rows)
```typescript
interface Account {
  id: uuid
  entity_id: uuid
  account_code: string // "1100", "4000", etc.
  account_name: string // "Cash", "Revenue", etc.
  account_type: string // "asset", "liability", "equity", "income", "expense"
  parent_account_id?: uuid // for sub-accounts
  balance: decimal
  is_active: boolean
  created_at: timestamp
  updated_at: timestamp
}
```

### 7.5 ML & Analytics

#### 7.5.1 ML Models Table (7 rows)
```typescript
interface MLModel {
  id: uuid
  model_name: string
  model_type: string // "categorization", "anomaly", "forecasting"
  version: string
  accuracy?: decimal
  last_trained_at: timestamp
  is_active: boolean
  created_at: timestamp
}
```

#### 7.5.2 AI Predictions Table (0 rows)
```typescript
interface AIPrediction {
  id: uuid
  model_id: uuid
  entity_id: uuid
  prediction_type: string
  prediction_value: jsonb
  confidence_score: decimal
  created_at: timestamp
}
```

#### 7.5.3 AI Insights Table (0 rows)
```typescript
interface AIInsight {
  id: uuid
  entity_id: uuid
  insight_type: string // "spending_pattern", "cost_saving", "risk_alert"
  title: string
  description: string
  confidence: decimal
  priority: string // "high", "medium", "low"
  related_data?: jsonb
  created_at: timestamp
}
```

#### 7.5.4 Anomaly Detections Table (0 rows)
```typescript
interface AnomalyDetection {
  id: uuid
  transaction_id: uuid
  anomaly_type: string
  severity: string // "high", "medium", "low"
  explanation: string
  false_positive: boolean
  created_at: timestamp
}
```

#### 7.5.5 Cash Flow Forecasts Table (0 rows)
```typescript
interface CashFlowForecast {
  id: uuid
  entity_id: uuid
  forecast_date: date
  predicted_inflow: decimal
  predicted_outflow: decimal
  predicted_balance: decimal
  confidence_interval_low: decimal
  confidence_interval_high: decimal
  created_at: timestamp
}
```

### 7.6 Supporting Tables

**Categories:**
- `upbank_categories` (44 rows)
- `personal_finance_categories` (10 rows)
- `categorization_rules` (3 rows)

**Sync:**
- `sync_sessions` (11 rows)
- `sync_errors` (26 rows)
- `transaction_sync_status`
- `rate_limit_status`

**Reconciliation:**
- `balance_reconciliations`
- `recurring_transactions` (26 rows)
- `business_keywords` (18 rows)

---

## 8. User Interface Specifications

### 8.1 Dashboard Layout

**Header:**
- Entity selector dropdown (Personal / MOKAI / MOK HOUSE)
- Search bar (Cmd+K)
- User avatar + settings
- Dark mode toggle

**Navigation:**
- Dashboard (home)
- Transactions (list)
- Invoices (file)
- Reports (chart)
- Insights (lightbulb)
- Settings (gear)

**Main Content:**
1. **KPI Cards** (4 across):
   - Total Income (this month, % change)
   - Total Expenses (this month, % change)
   - Net (income - expenses, % change)
   - Cash Balance (current, trend)

2. **Spending Breakdown**:
   - Donut chart (top 10 categories)
   - Legend with percentages
   - Click to drill down

3. **Recent Transactions**:
   - Table (last 10)
   - Columns: Date, Description, Category, Amount
   - "View All" link

4. **Alerts**:
   - Overdue invoices (count + total)
   - Anomaly alerts (count + severity)
   - Budget alerts (count + categories)

**Responsive:**
- Mobile: 320-767px (single column)
- Tablet: 768-1023px (2 column)
- Desktop: 1024px+ (full layout)

### 8.2 Component Library

**shadcn/ui Components:**
- `table`, `card`, `badge`, `skeleton`
- `form`, `input`, `select`, `date-picker`, `combobox`, `textarea`
- `navigation-menu`, `tabs`, `breadcrumb`
- `toast`, `alert`, `dialog`, `sheet`

**Custom Components:**
- `EntitySelector` (dropdown with logos)
- `TransactionTable` (virtual scrolling, inline edit)
- `InvoiceCard` (status-based styling)
- `KPICard` (metric + trend + sparkline)
- `ChartCard` (Recharts wrapper)
- `DateRangePicker` (presets + custom)
- `CategoryBadge` (color-coded, editable)
- `AnomalyAlert` (severity-based styling)

---

## 9. Success Metrics & KPIs

### 9.1 Technical Metrics
- **Performance**: <2s page load, <100ms chart render
- **Reliability**: 99.9% uptime
- **Accuracy**: 100% financial calculation accuracy
- **Test Coverage**: 100% for financial functions

### 9.2 User Metrics
- **Adoption**: Daily active usage
- **Efficiency**: 50% reduction in bookkeeping time
- **Categorization**: <5 clicks per transaction
- **Invoice Creation**: <2 minutes per invoice

### 9.3 Business Metrics
- **Coverage**: 100% of transactions tracked
- **Real-time**: Data updated within 10 minutes
- **BAS Accuracy**: Match ATO requirements
- **AI Accuracy**: 90%+ categorization, 95%+ anomaly precision

---

## 10. Timeline & Phasing

**Total Duration**: 12-14 weeks

### Phase 1: Transaction & Spending (3 weeks)
- Week 1: Foundation (Next.js, Supabase, auth)
- Week 2: Core features (transaction list, filtering, charts)
- Week 3: Polish (mobile, testing, deployment)

### Phase 2: Invoicing & Cash Flow (3 weeks)
- Week 1: Invoice CRUD
- Week 2: Payment tracking, PDF generation
- Week 3: Cash flow dashboard, forecasting

### Phase 3: Budgeting & Alerts (2 weeks)
- Week 1: Budget creation and tracking
- Week 2: Alerts (budget, anomaly)

### Phase 4: Accounting & Reporting (3 weeks)
- Week 1: P&L, Balance Sheet
- Week 2: BAS, Chart of Accounts
- Week 3: Export, testing with accountant

### Phase 5: Analytics & ML Insights (2 weeks)
- Week 1: Insights dashboard, trends
- Week 2: Advanced analytics, predictions

### Phase 6: Polish & UX (2 weeks)
- Week 1: Export (CSV/PDF), mobile optimization, dark mode
- Week 2: Keyboard shortcuts, bulk actions, final testing

---

## 11. Risks & Mitigation

### 11.1 Critical Risks

**Financial Calculation Errors** (High Impact)
- Mitigation: 100% test coverage, server-side validation, accountant verification

**Supabase RLS Misconfiguration** (Critical Impact)
- Mitigation: Comprehensive RLS testing, security audit, audit trails

**Performance Degradation** (Medium Impact)
- Mitigation: Virtual scrolling, pagination, database indexes, query optimization

**Vercel Free Tier Limits** (Medium Impact)
- Mitigation: Usage monitoring, optimization, upgrade path ($20/month)

### 11.2 Compliance Risks

**Australian Tax Compliance** (High Impact)
- Mitigation: ATO documentation reference, accountant verification, annual review

**Data Privacy** (High Impact)
- Mitigation: Encryption (HTTPS, at-rest), RLS policies, no logging of sensitive data

---

## 12. Open Questions

### Technical Decisions
1. React Query vs Server Components balance?
2. Chart performance with 1000+ data points?
3. TanStack Table vs shadcn Data Table?
4. PDF generation (client vs server)?
5. Dark mode timing (Phase 1 setup, Phase 6 implementation)?

### Design Questions
1. MOKAI/MOK HOUSE logos for invoices?
2. Invoice template style preference?
3. Custom brand colors or shadcn default?

### Functional Clarifications
1. Multi-entity permissions (single user assumption)?
2. Invoice numbering (per entity or global)?
3. Currency support (AUD only for MVP)?
4. Recurring transaction automation?
5. Anomaly false positive handling?

### Integration Clarifications
1. UpBank sync trigger (display only for MVP)?
2. ML model retraining frequency?
3. Export to accounting software (defer to Phase 6+)?

### Compliance Clarifications
1. Audit trail level (created_at/updated_at sufficient)?
2. Data retention (indefinite for MVP)?
3. Multi-user support (single user for MVP)?

---

## Appendices

### Appendix A: Acronyms
- **ATO**: Australian Taxation Office
- **BAS**: Business Activity Statement
- **GST**: Goods and Services Tax (10%)
- **P&L**: Profit & Loss statement
- **RLS**: Row-Level Security
- **ML**: Machine Learning
- **KPI**: Key Performance Indicator
- **WCAG**: Web Content Accessibility Guidelines

### Appendix B: Technical Stack Summary

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| Framework | Next.js | 14+ | App Router, SSR, Server Components |
| Language | TypeScript | 5+ | Type safety for financial calculations |
| Database | Supabase | - | Existing infrastructure (23 tables) |
| UI Library | shadcn/ui | v4 | Accessible, customizable |
| Charts | Recharts | - | React integration, performance |
| State (Server) | React Query | - | Caching, polling |
| State (Client) | Zustand | - | Lightweight global state |
| Forms | React Hook Form + Zod | - | Type-safe validation |
| Tables | TanStack Table | - | Virtual scrolling |
| PDF | react-pdf | - | Invoice generation |
| Deployment | Vercel | - | Next.js optimization |
| Testing | Vitest + Testing Library + Playwright | - | Unit, integration, E2E |

---

**End of Product Requirements Document**
