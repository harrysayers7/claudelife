---
date: "2025-10-17 00:00"
type: project-spec
status: planning
---

# Financial Dashboard Requirements

## Purpose
Build a comprehensive financial management dashboard to track ALL financial activity:
- Personal spending (UpBank sync)
- Business spending (to be set up)
- Business invoicing (receivables/payables)
- Cash flow analysis
- Budget tracking
- Accounting reports (P&L, Balance Sheet, BAS statements)

**Goal**: Complete financial visibility for both personal and business (MOKAI, MOK HOUSE) in one unified system.

## Data Sources
- **Supabase Project**: `gshsshaodoyttdxippwx` (SAYERS DATA)
- **Key Tables** (23 tables total):

### Business Financial Data
- **entities** (3 rows) - Companies, divisions, projects (MOKAI, MOK HOUSE)
- **transactions** (1 row) - Business transactions with ML categorization
- **invoices** (30 rows) - Receivables/payables with payment tracking
- **accounts** (52 rows) - Chart of accounts (asset, liability, equity, income, expense)
- **contacts** (3 rows) - Customers, suppliers, employees
- **bank_accounts** (3 rows) - Business bank accounts with forecasting

### Personal Financial Data (UpBank Integration)
- **personal_accounts** (4 rows) - UpBank accounts
- **personal_transactions** (256 rows) - Personal spending with ML categorization
- **upbank_categories** (44 rows) - UpBank's category system
- **personal_finance_categories** (10 rows) - Custom personal categories
- **recurring_transactions** (26 rows) - Detected recurring patterns
- **business_keywords** (18 rows) - Business expense detection

### ML & Analytics
- **ml_models** (7 rows) - Trained models for predictions
- **ai_predictions** (0 rows) - Model predictions with confidence scores
- **ai_insights** (0 rows) - AI-generated financial insights
- **anomaly_detections** (0 rows) - Unusual transaction detection
- **cash_flow_forecasts** (0 rows) - Predictive cash flow analysis
- **categorization_rules** (3 rows) - Auto-categorization rules

### System Tables
- **sync_sessions** (11 rows) - UpBank sync history
- **sync_errors** (26 rows) - Error tracking
- **transaction_sync_status** - Individual transaction sync tracking
- **balance_reconciliations** - Account balance verification
- **rate_limit_status** - API rate limiting

### Key Features in Schema
- **ML Integration**: All transaction tables have `ai_category`, `ai_confidence`, `ml_features`, `anomaly_score`
- **Project Tracking**: Many tables have `project` column (DiDi, Repco, Nintendo, etc.)
- **Real-time Ready**: Supabase supports real-time subscriptions
- **Rich Metadata**: JSONB fields for flexible data storage

## Core Features to Implement

### Phase 1: Transaction & Spending Tracking (MVP)
- [ ] **Unified transaction view** - Personal + Business transactions combined
- [ ] **Multi-entity filtering** - View by person/MOKAI/MOK HOUSE
- [ ] **Category breakdown** - Visual spending by category with drill-down
- [ ] **Search & filters** - Date range, amount, category, project, description
- [ ] **Real-time/periodic sync** - Poll Supabase every 10 minutes for updates
- [ ] **Project-based tracking** - Filter by DiDi, Repco, Nintendo, etc.

### Phase 2: Invoicing & Cash Flow
- [ ] **Invoice management** - Create, edit, track receivables/payables
- [ ] **Payment tracking** - Mark invoices paid, track due dates
- [ ] **Cash flow dashboard** - Visual timeline of inflows/outflows
- [ ] **Cash flow forecasting** - Use ML predictions from Supabase
- [ ] **Overdue alerts** - Highlight overdue invoices
- [ ] **Client/vendor insights** - Payment behavior, risk scores

### Phase 3: Budgeting & Alerts
- [ ] **Budget creation** - Set budgets by category/project/entity
- [ ] **Budget vs actual** - Real-time comparison with visual indicators
- [ ] **Spending alerts** - Notifications when approaching/exceeding budgets
- [ ] **Recurring transaction tracking** - Monitor subscriptions and regular payments
- [ ] **Anomaly detection** - Flag unusual transactions using ML scores

### Phase 4: Accounting & Reporting
- [ ] **Profit & Loss (P&L)** - Income statement by period/entity/project
- [ ] **Balance Sheet** - Assets, liabilities, equity view
- [ ] **BAS statement generation** - GST calculation for Australian tax
- [ ] **Chart of accounts view** - Account balances and transactions
- [ ] **Tax deductibility tracking** - Separate personal vs business expenses
- [ ] **Multi-entity comparison** - Side-by-side MOKAI vs MOK HOUSE

### Phase 5: Analytics & ML Insights
- [ ] **AI insights dashboard** - Display ML-generated financial insights
- [ ] **Spending trends** - Historical analysis with predictions
- [ ] **Category optimization** - Suggestions for cost savings
- [ ] **Payment behavior analysis** - Client payment patterns
- [ ] **Risk scoring** - Highlight high-risk transactions/contacts

### Phase 6: Polish & UX
- [ ] **Export capabilities** - CSV, PDF, Excel for all reports
- [ ] **Mobile responsive** - Works on phone/tablet
- [ ] **Dark mode** - Eye-friendly nighttime viewing
- [ ] **Keyboard shortcuts** - Power user efficiency
- [ ] **Bulk actions** - Select multiple transactions for batch operations

## Technical Stack Considerations

### Frontend Framework
- **Option 1**: Next.js 14+ (App Router) with React Server Components
- **Option 2**: Vite + React (SPA)
- **Preference**: [TBD after BMAD scan]

### UI Library
- **shadcn/ui v4** (confirmed via MCP)
- Components needed: table, card, chart, dialog, select, date-picker, badge

### Data Visualization
- **Options**: Recharts (shadcn default), Chart.js, D3.js
- **Preference**: [TBD]

### State Management
- **Options**: React Query (server state), Zustand (client state), Context API
- **Preference**: [TBD]

### Supabase Integration
- Supabase JS client
- Real-time subscriptions for live updates
- Row-level security (RLS) considerations

## Architectural Decisions (Pre-BMAD)

### Confirmed Requirements
- **Scope**: Comprehensive financial management (personal + business)
- **Data refresh**: Periodic polling (every 10 minutes) - real-time nice-to-have
- **Deployment**: Vercel (free tier if possible)
- **Scale**: 23 tables, ~300 rows currently (will grow significantly)

### Questions for BMAD Scan

1. **Framework Choice**:
   - Next.js 14+ (App Router, SSR, Server Components)?
   - Vite + React (SPA, faster dev, simpler)?
   - Consideration: Complex dashboard with many charts/tables

2. **Data Fetching Strategy**:
   - React Query for client-side caching + polling?
   - Next.js Server Components for initial data?
   - How to handle 23 tables efficiently (avoid N+1 queries)?
   - Best pattern for Supabase + periodic refresh?

3. **Chart Library**:
   - Recharts (shadcn default, simpler)?
   - Chart.js (more features, heavier)?
   - Tremor (built for dashboards)?
   - D3.js (maximum flexibility, steeper learning)?

4. **State Management**:
   - React Query + Context (server + UI state)?
   - Zustand (lightweight global state)?
   - Jotai (atomic state)?
   - Redux Toolkit (overkill?)?

5. **Component Architecture**:
   - Feature-based folders (transactions/, invoices/, reports/)?
   - Atomic design (atoms/molecules/organisms)?
   - How to share components across 6 phases?

6. **Form Handling**:
   - React Hook Form + Zod (type-safe validation)?
   - Formik?
   - Native form handling with Server Actions?

7. **Table/Grid Component**:
   - TanStack Table (powerful, complex)?
   - shadcn Data Table (simpler, less features)?
   - AG Grid (enterprise features, paid)?

8. **Authentication**:
   - Supabase Auth (built-in)?
   - How to secure multi-entity data (RLS policies)?
   - Session management patterns?

9. **Type Safety**:
   - Generate TypeScript types from Supabase schema?
   - How to maintain type safety across 23 tables?
   - Zod schemas for runtime validation?

10. **Performance Optimization**:
    - Code splitting strategy for 6 phases?
    - Lazy loading for heavy chart components?
    - Virtual scrolling for large transaction lists?
    - Caching strategy for reports?

11. **Testing Strategy**:
    - Unit tests (Vitest)?
    - Integration tests (Testing Library)?
    - E2E tests (Playwright)?
    - How much testing for financial accuracy?

12. **Deployment & CI/CD**:
    - Vercel auto-deploy from Git?
    - Environment variables for Supabase keys?
    - Preview deployments for PRs?
    - Database migrations strategy?

## Success Criteria
- Fast initial load (<2s)
- Real-time updates when data changes
- Accessible (WCAG AA)
- Type-safe (TypeScript throughout)
- Maintainable component architecture

## Related Context
- Supabase MCP tools: `mcp__supabase__*`
- shadcn MCP: `mcp__shadcn-ui__*`
- Context7 MCP: `mcp__context7__*`
- Server: 134.199.159.190 (could host the app)

---

**Next Steps**:
1. Review and refine requirements
2. Run `/bmad` scan with this context
3. Make architectural decisions based on scan results
4. Begin implementation with Task Master
