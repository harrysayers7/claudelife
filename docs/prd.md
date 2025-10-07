# SAYERS Finance Dashboard Product Requirements Document (PRD)

<!-- Powered by BMAD™ Core -->

## Goals and Background Context

### Goals

- Provide real-time visibility into financial performance across multiple business entities (MOKAI, MOK HOUSE, personal)
- Automate transaction categorization using ML to reduce manual bookkeeping effort by 80%
- Enable accurate tax compliance reporting (BAS, income statements) with one-click generation
- Surface financial anomalies and insights proactively through AI-powered detection
- Streamline invoice management from creation to payment tracking
- Support multi-entity accounting with proper data isolation and entity switching
- Export financial data in formats compatible with accounting software (Xero, MYOB, CSV)
- Deliver mobile-responsive experience for on-the-go financial monitoring

### Background Context

Harrison Robert Sayers manages three distinct financial entities: MOKAI PTY LTD (Indigenous tech consultancy), MOK HOUSE PTY LTD (creative house), and personal finances. Currently, financial data exists in Supabase with automated UpBank sync running hourly, ML categorization via MindsDB, and anomaly detection, but lacks a unified interface to view, manage, and act on this data. The existing infrastructure includes 24+ database tables with 230+ personal transactions, 29 invoices, ML models for categorization/anomaly detection, and multi-entity support.

The current pain points include: no visual dashboard to understand financial health across entities, manual intervention required for ML prediction review (transactions with <0.9 confidence), no streamlined invoice creation workflow, difficulty generating tax compliance documents, and inability to export data for accountant review. This dashboard solves these problems by providing a modern, web-based interface that leverages existing Supabase infrastructure while adding visualization, management workflows, and compliance reporting capabilities.

### Change Log

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| 2025-10-03 | 1.0 | Initial PRD creation | Harrison Robert Sayers |

## Requirements

### Functional Requirements

- FR1: Dashboard displays real-time KPIs across selected entity: total revenue, expenses, profit/loss, cash flow, receivables, payables
- FR2: Dashboard renders interactive charts: revenue/expense trends (6-month default), category breakdown (pie/bar), anomaly timeline
- FR3: Dashboard shows recent transactions widget (last 10 with category, amount, confidence score)
- FR4: Dashboard highlights anomaly alerts with severity indicators and drill-down capability
- FR5: Transaction list view supports filtering by: entity, date range, category, confidence score range, anomaly flag, amount range
- FR6: Transaction list supports search across: description, merchant, category, reference fields
- FR7: Transaction list displays ML predictions: AI category, confidence score, anomaly score with visual indicators
- FR8: Users can manually override ML categorization with reason logging and confidence reset
- FR9: Users can bulk categorize multiple transactions with confirmation dialog
- FR10: Users can edit transaction metadata: description, notes, tags, split amounts
- FR11: Invoice creation form captures: client/supplier (from contacts), line items, GST calculation, due date, payment terms
- FR12: Invoice list view supports filtering: entity, status (draft/sent/paid/overdue), date range, client/supplier
- FR13: System generates PDF invoices with professional formatting, entity branding, GST breakdown, payment instructions
- FR14: Invoice status tracking: draft → sent → paid with automatic overdue flagging based on due date
- FR15: System calculates BAS (Business Activity Statement) data: GST collected, GST paid, net GST position for selected quarter
- FR16: System generates income statements (P&L) with: revenue by category, expenses by category, net profit/loss for selected period
- FR17: Users can export transactions to CSV with selectable columns: all fields, accounting format (date, description, amount, category, GST)
- FR18: Users can export invoices to PDF (single/batch) and CSV format
- FR19: Multi-entity selector in header allows switching active entity with data refresh and context persistence
- FR20: Contact management: create, edit, list, archive contacts with fields (name, ABN, email, phone, address, type: customer/supplier/both)
- FR21: Account management: view chart of accounts, activate/deactivate accounts, edit account details (name, type, tax treatment)
- FR22: System displays ML model performance metrics: categorization accuracy, prediction confidence distribution, anomaly detection rate
- FR23: User preferences: default entity, date format, currency display, notification settings, dashboard layout customization
- FR24: System logs all financial data modifications: who, what, when, old/new values for audit trail
- FR25: System syncs with UpBank hourly (existing automation) and displays last sync status/timestamp
- FR26: Users receive in-app notifications for: new anomalies detected, invoices overdue, ML predictions requiring review (<0.7 confidence)

### Non-Functional Requirements

- NFR1: All pages must load within 2 seconds on standard broadband connection (5Mbps+)
- NFR2: Transaction lists must implement virtual scrolling for datasets >100 records to maintain performance
- NFR3: System must enforce Supabase Row Level Security (RLS) policies for multi-entity data isolation
- NFR4: All financial data must be encrypted at rest (Supabase default) and in transit (HTTPS only)
- NFR5: System must maintain 100% accuracy in financial calculations: GST (10%), totals, balances, rounding (to 2 decimal places)
- NFR6: System must comply with Australian tax regulations: GST calculation, BAS reporting format, invoice requirements (ABN, GST breakdown)
- NFR7: All user-facing interfaces must meet WCAG AA accessibility standards minimum
- NFR8: Application must be fully responsive: desktop (1920px+), tablet (768px-1919px), mobile (320px-767px)
- NFR9: System must maintain audit trail for all financial modifications with 7-year retention minimum
- NFR10: Application uptime target: 99.9% excluding planned maintenance windows
- NFR11: Database queries must use indexed fields for filters: entity_id, created_at, category, status
- NFR12: PDF generation must complete within 5 seconds for standard invoices (<20 line items)
- NFR13: Chart rendering must handle datasets up to 1000 points without performance degradation
- NFR14: System must implement optimistic UI updates with graceful error handling and rollback
- NFR15: All forms must implement client-side validation with immediate feedback before submission
- NFR16: System must handle concurrent entity switching without data leakage or stale state
- NFR17: Export operations must process up to 10,000 records with progress indication
- NFR18: Application must function offline for read-only views with clear online/offline status indicator

## User Interface Design Goals

### Overall UX Vision

The SAYERS Finance Dashboard delivers a clean, professional, data-focused experience that transforms complex financial data into actionable insights. The interface prioritizes clarity and efficiency, enabling Harrison to quickly understand financial health across entities, act on ML-flagged items requiring review, and generate compliance documents without friction. The design aesthetic balances modern SaaS polish (shadcn/ui components) with financial application conventions (tables, charts, forms), ensuring familiarity for users accustomed to accounting software while providing superior visualization and workflow efficiency.

### Key Interaction Paradigms

- **Dashboard-first navigation**: Landing on overview dashboard with KPIs, charts, and alerts provides immediate context
- **Contextual entity switching**: Persistent header dropdown for entity selection with visual indicator of active context
- **Filter-driven exploration**: Transaction and invoice lists use faceted filters (date, category, status) with live result counts
- **Inline editing patterns**: Click-to-edit for transaction categorization, invoice line items, contact details without modal interruptions
- **Confidence-based workflows**: ML predictions with <0.9 confidence surfaced in review queue requiring explicit user action
- **Progressive disclosure**: Summary cards expand to detailed views, charts drill down to underlying transactions
- **Bulk operations**: Multi-select with batch actions (categorize, export, archive) for efficiency at scale
- **Responsive table patterns**: Desktop shows full columns, tablet/mobile collapse to cards with expandable details

### Core Screens and Views

- **Dashboard (Overview)**: KPI cards, trend charts, recent transactions widget, anomaly alerts, entity selector
- **Transactions List**: Filterable/searchable table with ML predictions, inline category editing, bulk actions, export
- **Transaction Detail**: Full transaction view with history, ML insights, category override, split transaction, notes
- **Invoices List**: Filterable table with status indicators, quick actions (view PDF, mark paid, send), create button
- **Invoice Create/Edit**: Multi-step form (client selection, line items, GST calculation, preview), PDF generation
- **Reports**: Tax documents (BAS, income statement) with period selection, preview, export options
- **Contacts**: List/grid view with quick actions, create/edit modal, archive functionality
- **Accounts**: Chart of accounts table with filters, activate/deactivate toggles, edit modal
- **Settings**: Multi-tab interface (preferences, entity management, integrations, audit log, ML model metrics)
- **Login/Auth**: Supabase Auth UI integration with email/password, session management

### Accessibility: WCAG AA

- Semantic HTML structure with proper heading hierarchy (h1-h6)
- Keyboard navigation support for all interactive elements (tab order, focus indicators, shortcut keys)
- Color contrast ratios meeting 4.5:1 minimum for text, 3:1 for UI components
- Screen reader compatibility: ARIA labels, roles, live regions for dynamic updates
- Form validation with clear error messaging and associations (aria-describedby)
- Chart accessibility: data tables as alternatives, descriptive labels, keyboard navigation
- Focus management: modals trap focus, form errors receive focus, clear skip links
- Responsive text scaling: interface remains functional up to 200% zoom

### Branding

Professional financial SaaS aesthetic leveraging shadcn/ui design system. Color palette: neutral grays for backgrounds/chrome, blue primary for actions/links, green for positive financial indicators (revenue, profit), red for negative indicators (expenses, losses, overdue), amber for warnings (anomalies, low confidence predictions). Typography: Clean sans-serif (Inter/system fonts) for readability at financial data density levels. Visual hierarchy: Card-based layouts, subtle shadows for elevation, consistent spacing (8px grid), bordered tables for data clarity. No specific corporate branding required beyond professional, trustworthy appearance suitable for financial management.

### Target Device and Platforms: Web Responsive

Primary: Desktop browsers (Chrome, Firefox, Safari, Edge) at 1920x1080+
Secondary: Tablet devices (iPad, Android tablets) at 768x1024+
Tertiary: Mobile browsers (iOS Safari, Chrome Android) at 375x667+ (iPhone 8 minimum)

Responsive breakpoints:
- Desktop: 1920px+ (full feature set, multi-column layouts, expanded charts)
- Laptop: 1280px-1919px (condensed layouts, collapsible sidebars)
- Tablet: 768px-1279px (single column with stacked cards, simplified charts)
- Mobile: 320px-767px (mobile-first navigation, card-based views, essential features only)

Progressive Web App (PWA) capabilities: offline read access, home screen installation, background sync for updates.

## Technical Assumptions

### Repository Structure: Monorepo

Single Next.js repository containing all application code. Structure:
```
/app - Next.js App Router pages and API routes
/components - React components (shadcn/ui + custom)
/lib - Utilities, Supabase client, data fetching
/types - TypeScript type definitions
/hooks - Custom React hooks
/public - Static assets
/supabase - Database types, migrations (reference only)
```

### Service Architecture

Monolith: Next.js 14+ App Router application with:
- Server Components for data fetching and initial page loads
- Client Components for interactivity (charts, forms, filters)
- API Routes for server-side operations (PDF generation, exports)
- Supabase client for database queries (client-side and server-side patterns)
- Edge Runtime for performance-critical routes (dashboard, transaction list)

Rationale: Project scope fits monolith pattern. Supabase handles backend complexity (database, auth, real-time). Next.js provides SSR/SSG optimization. No need for microservices overhead at current scale.

### Testing Requirements

Full Testing Pyramid:
- **Unit Tests**: Vitest for utility functions, calculation logic (GST, totals, date formatting), data transformations
- **Integration Tests**: React Testing Library for component behavior, form validation, user interactions
- **E2E Tests**: Playwright for critical user journeys (login → dashboard view, transaction categorization workflow, invoice creation → PDF generation)
- **Visual Regression**: Optional Playwright screenshots for key screens (dashboard, invoice preview)
- **Manual Testing**: Checklist for tax calculation accuracy, PDF formatting, multi-entity data isolation

Test coverage targets: 80%+ for business logic, 60%+ for components, 100% for critical financial calculations.

### Additional Technical Assumptions and Requests

- **Supabase Client**: Use `@supabase/ssr` package for App Router compatibility with server/client client instances
- **UI Library**: shadcn/ui components (built on Radix UI primitives) with Tailwind CSS for styling
- **Charts**: Recharts library for all data visualizations (line, bar, pie, area charts)
- **Forms**: React Hook Form + Zod schema validation for all user inputs
- **PDF Generation**: `@react-pdf/renderer` or `puppeteer` for server-side invoice PDF creation
- **Data Export**: `papaparse` for CSV generation, `xlsx` for Excel format
- **Date Handling**: `date-fns` for date manipulation, formatting, timezone handling (Australia/Sydney)
- **State Management**: React Context for global state (active entity, user preferences), TanStack Query for server state caching
- **Type Safety**: TypeScript strict mode, generate Supabase types from database schema
- **RLS Enforcement**: All Supabase queries must include entity_id filters, rely on RLS policies for security boundary
- **Error Handling**: Error boundaries for component failures, toast notifications for user-facing errors, Sentry for production error tracking
- **Performance**: React Server Components default, Client Components only when interactivity required, dynamic imports for heavy components (charts)
- **Deployment**: Vercel for hosting (automatic deployments from main branch), environment variables for Supabase keys
- **Database Migrations**: Supabase Studio for schema changes, track migration SQL in repo for reference
- **Authentication**: Supabase Auth with email/password, session management via cookies
- **ML Integration**: Read-only access to ML prediction tables (ai_predictions, anomaly_detections), no model training in dashboard
- **Real-time Updates**: Optional Supabase Realtime subscriptions for transaction list live updates (nice-to-have, not MVP)

## Epic List

**Epic 1: Foundation & Core Infrastructure**
Establish Next.js application setup, Supabase integration, authentication, base layout/navigation, and deploy foundation to Vercel with basic dashboard landing page.

**Epic 2: Financial Dashboard & Visualization**
Implement dashboard KPIs, trend charts, recent transactions widget, anomaly alerts using Recharts and Supabase queries with proper entity filtering.

**Epic 3: Transaction Management & ML Review**
Build transaction list view with filtering, search, inline categorization, ML prediction display, and bulk operations for efficient transaction management.

**Epic 4: Invoice Management & PDF Generation**
Create invoice CRUD workflows, line item management, GST calculation, status tracking, and professional PDF generation with download/email capabilities.

**Epic 5: Reports & Tax Compliance**
Implement BAS calculation, income statement generation, data export functionality (CSV/Excel), and tax-compliant reporting formats.

**Epic 6: Settings, Administration & Multi-Entity**
Build settings interface for user preferences, entity management, contact/account administration, audit log viewing, and ML model performance metrics.

## Epic 1: Foundation & Core Infrastructure

**Epic Goal**: Establish the foundational project infrastructure including Next.js application setup, Supabase database integration, authentication system, base application layout with responsive navigation, and initial deployment pipeline to Vercel. This epic delivers a functional authenticated application with entity switching capability and a basic dashboard landing page, setting the stage for all subsequent feature development while ensuring security, performance, and deployment foundations are solid.

### Story 1.1: Project Setup & Next.js Application Initialization

As a developer,
I want to initialize a Next.js 14+ application with TypeScript, Tailwind CSS, and shadcn/ui,
so that I have a modern, type-safe foundation for building the finance dashboard.

#### Acceptance Criteria

1. Next.js 14+ project created using `create-next-app` with App Router, TypeScript, and Tailwind CSS enabled
2. Project structure follows monorepo conventions with `/app`, `/components`, `/lib`, `/types`, `/hooks`, `/public` directories
3. shadcn/ui initialized with `npx shadcn-ui init` and base components installed: Button, Card, Input, Label, Select, Table
4. Tailwind CSS configured with custom theme colors: primary (blue), success (green), danger (red), warning (amber), neutral grays
5. TypeScript strict mode enabled in `tsconfig.json` with path aliases configured (`@/components`, `@/lib`, etc.)
6. ESLint and Prettier configured with Next.js recommended rules and consistent code formatting
7. Git repository initialized with `.gitignore` excluding `node_modules`, `.next`, `.env.local`, and build artifacts
8. `package.json` includes all required dependencies: Next.js, React, TypeScript, Tailwind, shadcn/ui, date-fns, zod, react-hook-form
9. Development server runs successfully on `localhost:3000` with hot module replacement working
10. README.md created with project description, setup instructions, and development commands

### Story 1.2: Supabase Integration & Type Generation

As a developer,
I want to integrate Supabase client with TypeScript type generation from the existing database schema,
so that I have type-safe database queries and autocomplete for all tables.

#### Acceptance Criteria

1. `@supabase/ssr` package installed and configured for Next.js App Router compatibility
2. Supabase client instances created: `createClient()` for server components, `createBrowserClient()` for client components
3. Environment variables configured in `.env.local`: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`
4. TypeScript types generated from Supabase schema using CLI: `supabase gen types typescript` for all 24+ tables
5. Generated types saved to `/types/supabase.ts` and imported in Supabase client configuration
6. Helper functions created in `/lib/supabase.ts`: `getServerClient()`, `getBrowserClient()` with proper typing
7. Test query implemented (e.g., fetch entities) to verify Supabase connection works from server component
8. Error handling implemented: graceful failure messages for connection issues, missing environment variables
9. RLS policies verified: confirm entity_id filtering works correctly by querying entities table
10. Documentation added to README: Supabase setup instructions, type regeneration steps, environment variable requirements

### Story 1.3: Authentication System with Supabase Auth

As a user,
I want to log in with email and password,
so that I can securely access my financial data.

#### Acceptance Criteria

1. Supabase Auth configured in Supabase project settings: email/password provider enabled, email confirmation disabled for development
2. Login page created at `/app/login/page.tsx` with email and password input fields using shadcn/ui Form components
3. Login form implements React Hook Form + Zod validation: email format, password minimum 8 characters, required field validation
4. Authentication logic implemented: `supabase.auth.signInWithPassword()` with error handling for invalid credentials, network errors
5. Successful login redirects user to `/dashboard` route with session cookie set via Supabase SSR middleware
6. Logout functionality implemented: sign out button in navigation triggers `supabase.auth.signOut()` and redirects to `/login`
7. Session management middleware created: `/middleware.ts` checks authentication status, redirects unauthenticated users to `/login`
8. Protected routes configured: all `/app` routes except `/login` require authentication via middleware check
9. User session persists across browser refreshes using Supabase session cookies
10. Error messages display clearly: "Invalid credentials", "Network error", field-specific validation errors with red text

### Story 1.4: Base Application Layout & Responsive Navigation

As a user,
I want to see a consistent header, sidebar navigation, and content area across all pages,
so that I can easily navigate between different sections of the dashboard.

#### Acceptance Criteria

1. Root layout created at `/app/layout.tsx` with responsive structure: header, sidebar (desktop), mobile menu, main content area
2. Header component includes: application logo/name ("SAYERS Finance"), entity selector dropdown (placeholder), user menu with logout
3. Sidebar navigation (desktop 1280px+) displays menu items: Dashboard, Transactions, Invoices, Reports, Contacts, Accounts, Settings
4. Mobile navigation (< 1280px) uses hamburger menu icon triggering slide-out drawer with same menu items
5. Active route highlighting implemented: current page menu item visually distinct with background color/border
6. Navigation items use Next.js `<Link>` components for client-side routing with prefetching enabled
7. Layout is responsive: header stacks on mobile, sidebar hidden behind hamburger, content area takes full width
8. Accessibility features implemented: skip to main content link, keyboard navigation (tab/arrows), focus indicators on interactive elements
9. Footer component (optional) includes: copyright text, link to privacy policy (placeholder), app version number
10. All layout components use shadcn/ui primitives (Card, Button, Sheet for mobile menu) with consistent Tailwind spacing/colors

### Story 1.5: Multi-Entity Selector & Context Management

As a user,
I want to select which business entity I'm viewing (MOKAI, MOK HOUSE, personal),
so that I see only the relevant financial data for that entity.

#### Acceptance Criteria

1. Entity selector dropdown component created in header using shadcn/ui Select component
2. Entities fetched from Supabase `entities` table on component mount: entity_id, name, type displayed in dropdown
3. Active entity state managed using React Context: `EntityContext` provider wraps application in root layout
4. Selected entity persists in browser localStorage: key `selectedEntityId`, restored on page refresh
5. Default entity set on first login: if no localStorage value, default to first entity in list (MOKAI PTY LTD)
6. Entity change triggers data refresh: context value update causes dependent components to re-fetch with new entity_id filter
7. Visual indicator shows active entity: selected entity name displayed in header with entity type badge (e.g., "MOKAI PTY LTD (Company)")
8. Entity switching logs audit event: timestamp, user_id, old_entity_id, new_entity_id written to audit log table (if exists, otherwise console log)
9. Loading state handled during entity fetch: skeleton loader shown in dropdown until entities loaded from Supabase
10. Error handling: if entities fetch fails, show error toast, disable entity selector, log error to console

### Story 1.6: Basic Dashboard Landing Page

As a user,
I want to see a dashboard landing page when I log in,
so that I know the application is working and I have a starting point for navigation.

#### Acceptance Criteria

1. Dashboard page created at `/app/dashboard/page.tsx` as default route after login
2. Page header displays: "Dashboard" title, active entity name subtitle, date range selector (placeholder, default "Last 30 Days")
3. KPI placeholder cards rendered in responsive grid: 4 cards on desktop (1920px+), 2 cards on tablet (768px+), 1 card on mobile (<768px)
4. Each KPI card displays: metric label (e.g., "Total Revenue"), placeholder value ("$0.00"), icon, trend indicator (placeholder +0%)
5. Chart placeholder section below KPIs: empty state message "Charts coming soon" with chart icon, proper spacing/borders
6. Recent activity widget placeholder: "Recent Transactions" heading, empty state "No recent transactions" message, bordered container
7. All components use shadcn/ui Card component with consistent spacing, shadows, and responsive behavior
8. Page implements proper loading state: skeleton loaders for cards/widgets shown while data would be fetching (simulated 1s delay)
9. Responsive behavior verified: layout stacks vertically on mobile, side-by-side on tablet/desktop, no horizontal scroll
10. Navigation from sidebar "Dashboard" menu item highlights correctly and loads this page

### Story 1.7: Vercel Deployment & Environment Configuration

As a developer,
I want to deploy the application to Vercel with proper environment variables,
so that I have a live staging environment accessible via URL.

#### Acceptance Criteria

1. Vercel project created and connected to GitHub repository with automatic deployments enabled on `main` branch
2. Environment variables configured in Vercel dashboard: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` set to production Supabase project
3. Build settings configured: Next.js framework preset selected, build command `npm run build`, output directory `.next`
4. Production deployment succeeds: build completes without errors, application accessible at Vercel-provided URL (e.g., `sayers-finance.vercel.app`)
5. Deployment preview environments created: pull requests trigger preview deployments with unique URLs
6. Custom domain configured (optional): if available, custom domain pointed to Vercel deployment with SSL enabled
7. Environment variable security verified: no secrets exposed in client-side code, `NEXT_PUBLIC_` prefix only on public variables
8. Deployment monitoring enabled: Vercel Analytics and Speed Insights integrated for performance tracking (optional)
9. Rollback capability verified: previous deployment accessible via Vercel dashboard, one-click rollback tested
10. Deployment documentation added to README: deployment steps, environment variable setup, domain configuration instructions

---

## Epic 2: Financial Dashboard & Visualization

**Epic Goal**: Transform the placeholder dashboard landing page into a fully functional financial overview interface that displays real-time KPIs calculated from Supabase transaction data, renders interactive charts showing revenue/expense trends and category breakdowns using Recharts, presents recent transactions with ML prediction insights, and surfaces anomaly alerts with drill-down capability. This epic delivers immediate value by enabling Harrison to understand financial health at a glance, identify trends, and proactively address anomalies, all filtered by the selected entity context established in Epic 1.

### Story 2.1: KPI Calculation & Display Components

As a user,
I want to see accurate KPI metrics (total revenue, expenses, profit/loss, cash flow) on the dashboard,
so that I understand my current financial position at a glance.

#### Acceptance Criteria

1. KPI calculation service created in `/lib/kpis.ts` with functions: `calculateRevenue()`, `calculateExpenses()`, `calculateProfit()`, `calculateCashFlow()`
2. Each KPI function queries Supabase `transactions` table filtered by: active entity_id, date range (default last 30 days), status (exclude cancelled)
3. Revenue calculation: sum of all transactions where `amount > 0` OR `category IN (revenue categories)` with proper GST handling
4. Expense calculation: sum of all transactions where `amount < 0` OR `category IN (expense categories)` with GST excluded from totals
5. Profit/loss calculation: revenue - expenses with accurate arithmetic, displayed with positive (green) or negative (red) color coding
6. Cash flow calculation: sum of all bank_account balances for active entity with timestamp of last update displayed
7. KPI Card component created: accepts props (label, value, icon, trend, loading state), formats currency with `Intl.NumberFormat('en-AU', { style: 'currency', currency: 'AUD' })`
8. Dashboard page replaces placeholder cards with live KPI components fetching real data on mount and entity change
9. Loading states implemented: skeleton loaders show during data fetch (minimum 300ms to prevent flashing)
10. Error handling: if KPI fetch fails, display fallback value "$--" with error icon, log error to console, show retry button

### Story 2.2: Revenue & Expense Trend Chart

As a user,
I want to see a line chart showing revenue and expense trends over the last 6 months,
so that I can identify financial patterns and track business performance over time.

#### Acceptance Criteria

1. Trend chart component created using Recharts `LineChart` with responsive container (`ResponsiveContainer` width 100%, height 300px)
2. Chart data service in `/lib/charts.ts` with `getTrendData(entityId, months)` function querying transactions grouped by month
3. Data aggregation logic: group transactions by month using `date-fns` `startOfMonth()`, sum revenue and expenses separately per month
4. Chart displays two lines: revenue (green color `#10b981`), expenses (red color `#ef4444`) with smooth curves (`type="monotone"`)
5. X-axis shows month labels (format "MMM YYYY" e.g., "Jan 2025") using Recharts `XAxis` with `dataKey="month"`
6. Y-axis shows currency amounts formatted with `Intl.NumberFormat` using Recharts `YAxis` with `tickFormatter`
7. Tooltip component displays: month name, revenue amount (green), expenses amount (red), net profit/loss (calculated)
8. Legend positioned below chart showing color-coded labels: "Revenue", "Expenses"
9. Chart handles empty data gracefully: if no transactions in period, display "No data available for selected period" message
10. Chart updates when entity or date range changes: useEffect dependency on entityId and dateRange triggers re-fetch

### Story 2.3: Category Breakdown Pie Chart

As a user,
I want to see a pie chart showing expense breakdown by category,
so that I can understand where my money is going and identify top spending areas.

#### Acceptance Criteria

1. Pie chart component created using Recharts `PieChart` with responsive container (width 100%, height 350px)
2. Category data service in `/lib/charts.ts` with `getCategoryBreakdown(entityId, dateRange, type)` function where type = "expense" or "revenue"
3. Data aggregation: query transactions filtered by entity and date range, group by category (use ML `ai_category` if confidence > 0.9, else manual category), sum amounts
4. Chart renders sectors for top 6 categories by amount, groups remaining into "Other" category if more than 6 exist
5. Pie slices use distinct colors from Tailwind color palette: blue-500, green-500, yellow-500, red-500, purple-500, pink-500, gray-500
6. Chart labels show: category name, percentage of total (calculated as `(categoryAmount / totalExpenses) * 100`)
7. Interactive hover state: slice enlarges slightly on hover, tooltip displays category name, amount (currency formatted), percentage
8. Legend positioned to right of chart (desktop) or below (mobile) with color boxes and category names
9. Toggle buttons above chart: "Expenses" (default) and "Revenue" to switch between expense and revenue category breakdowns
10. Empty state handled: if no transactions in selected categories, display "No category data available" message with info icon

### Story 2.4: Recent Transactions Widget with ML Insights

As a user,
I want to see my 10 most recent transactions with ML categorization and confidence scores,
so that I can quickly review latest activity and identify transactions needing manual review.

#### Acceptance Criteria

1. Recent transactions component created displaying compact table with columns: Date, Description, Category, Amount, Confidence
2. Data service in `/lib/transactions.ts` with `getRecentTransactions(entityId, limit)` querying transactions table ordered by `created_at DESC` limit 10
3. Each row displays: transaction date (format "DD MMM" e.g., "15 Jan"), description (truncated to 30 chars with ellipsis), AI category, amount (currency formatted with +/- sign)
4. Confidence score displayed as colored badge: green (≥0.9 "High"), amber (0.7-0.89 "Medium"), red (<0.7 "Low") using shadcn/ui Badge component
5. Clicking transaction row navigates to transaction detail page (link to `/transactions/[id]`, Epic 3 implementation)
6. Anomaly indicator icon shown in row if transaction has `anomaly_score > 0.7` with red warning triangle icon
7. Widget header displays: "Recent Transactions" title, "View All" link routing to `/transactions` page (Epic 3)
8. Widget uses shadcn/ui Card component with proper spacing, bordered table rows, hover states on rows
9. Empty state handled: if no transactions exist, display "No recent transactions" message with icon
10. Loading state: skeleton loader with 10 placeholder rows shown during data fetch, smooth transition to real data

### Story 2.5: Anomaly Alerts Section with Drill-Down

As a user,
I want to see a list of financial anomalies detected by ML with severity indicators,
so that I can investigate unusual transactions and prevent fraud or errors.

#### Acceptance Criteria

1. Anomaly alerts component created displaying list of transactions flagged by ML anomaly detection (anomaly_score > 0.7)
2. Data service queries `anomaly_detections` table joined with `transactions` filtered by entity and date range, ordered by anomaly_score DESC
3. Each alert card displays: transaction description, amount, date, anomaly score (0-1), severity badge (High: >0.9 red, Medium: 0.7-0.9 amber)
4. Alert cards show anomaly reason if available from ML model (e.g., "Unusually large amount for category", "Rare merchant"), fallback to "Anomaly detected"
5. "View Details" button on each card navigates to transaction detail page with anomaly information highlighted
6. Alerts section displays maximum 5 most recent/severe anomalies, "View All Anomalies" link routes to filtered transactions page (Epic 3)
7. Severity icon shown: red warning triangle for high severity, amber alert icon for medium severity
8. Anomaly count badge displayed in section header: "Anomaly Alerts (X)" where X is total count of unresolved anomalies
9. Empty state handled: if no anomalies detected, display "No anomalies detected" message with green checkmark icon and congratulatory text
10. Anomaly dismissal action (optional): "Dismiss" button marks anomaly as reviewed, removes from active alerts list (updates `reviewed_at` timestamp in anomaly_detections)

### Story 2.6: Dashboard Date Range Selector & Filter Logic

As a user,
I want to select different date ranges (last 7 days, 30 days, 3 months, 6 months, 1 year, custom range),
so that I can view dashboard metrics and charts for specific time periods.

#### Acceptance Criteria

1. Date range selector component created using shadcn/ui Select with preset options: "Last 7 Days", "Last 30 Days", "Last 3 Months", "Last 6 Months", "Last Year", "Custom Range"
2. Date range state managed in dashboard page using React useState with default value "Last 30 Days"
3. Preset selection calculates date range using `date-fns`: `subDays()`, `subMonths()`, `subYears()` from current date
4. Custom range selection opens date picker modal (shadcn/ui Popover + Calendar) allowing user to select start and end dates
5. Selected date range displayed in dashboard header: "Showing data for [range]" (e.g., "Showing data for Jan 1, 2025 - Jan 31, 2025")
6. Date range change triggers re-fetch of all dashboard data: KPIs, charts, recent transactions, anomalies via useEffect dependency
7. Date range selection persists in URL query params: `/dashboard?range=30d` or `/dashboard?start=2025-01-01&end=2025-01-31` for shareable links
8. All data fetching services accept `startDate` and `endDate` parameters, filter Supabase queries with `created_at >= startDate AND created_at <= endDate`
9. Loading states shown during re-fetch: KPI cards, charts, widgets display skeleton loaders while data loads
10. Validation implemented: custom range start date cannot be after end date, date range cannot exceed 5 years, error toast shown for invalid selections

### Story 2.7: Dashboard Responsive Layout & Mobile Optimization

As a user,
I want the dashboard to work seamlessly on my mobile device,
so that I can check financial metrics on the go.

#### Acceptance Criteria

1. Dashboard layout uses CSS Grid with responsive breakpoints: 4 columns (desktop 1920px+), 2 columns (tablet 768-1919px), 1 column (mobile <768px)
2. KPI cards stack vertically on mobile with full width, maintain side-by-side on tablet (2-up), 4-up grid on desktop
3. Trend chart maintains aspect ratio on all screen sizes: full width with 300px height on desktop, 250px on mobile using ResponsiveContainer
4. Pie chart repositions legend below chart on mobile (<768px), to right side on desktop for better space utilization
5. Recent transactions widget uses card-based layout on mobile (stacked vertically) instead of table to improve readability
6. Anomaly alerts stack vertically on mobile, 2-up grid on tablet, 3-up grid on desktop
7. Date range selector remains accessible on mobile: full-width dropdown, touch-friendly tap targets (minimum 44x44px)
8. All touch interactions optimized: no hover-dependent functionality, clear active states for taps, swipe gestures for chart zooming (optional)
9. Typography scales appropriately: larger font sizes on mobile for readability, condensed spacing to fit more content
10. Tested on real devices or browser DevTools device emulation: iPhone SE (375px), iPad (768px), desktop (1920px) with no layout breaking or horizontal scroll

---

## Epic 3: Transaction Management & ML Review

**Epic Goal**: Build a comprehensive transaction management interface that enables efficient browsing, searching, filtering, and categorization of financial transactions. The interface displays ML predictions with confidence scores, supports inline category overrides with audit logging, implements bulk operations for categorizing multiple transactions at once, and provides detailed transaction views with edit capabilities. This epic directly addresses the pain point of manual ML prediction review by surfacing low-confidence predictions in a dedicated review queue and streamlining the workflow to approve, override, or split transactions, ultimately reducing bookkeeping effort by 80% through intelligent automation and efficient manual intervention when needed.

### Story 3.1: Transaction List Page with Pagination

As a user,
I want to browse all transactions in a paginated table,
so that I can review financial activity without performance issues from large datasets.

#### Acceptance Criteria

1. Transaction list page created at `/app/transactions/page.tsx` with table layout using shadcn/ui Table component
2. Table columns display: Date, Description/Merchant, Category, Amount, Confidence Score, Anomaly Indicator, Actions (View/Edit)
3. Data fetching service in `/lib/transactions.ts` queries Supabase transactions table with pagination: `from`, `to` calculated from page number and page size
4. Pagination controls implemented using shadcn/ui Pagination component: Previous, page numbers (show 5 max), Next buttons
5. Page size selector dropdown with options: 25, 50, 100 transactions per page, default 50
6. Total transaction count displayed: "Showing X-Y of Z transactions" text above table
7. Table rows clickable to navigate to transaction detail page: `/transactions/[id]`
8. Loading state during fetch: skeleton loader rows (10 placeholders) with shimmer animation using shadcn/ui Skeleton
9. Empty state handled: if no transactions found, display "No transactions found" message with "Add Transaction" button (Epic 3 later story)
10. URL query params track pagination state: `/transactions?page=2&pageSize=50` for shareable/bookmarkable links, browser back/forward navigation works

### Story 3.2: Transaction Filtering & Search

As a user,
I want to filter transactions by category, date range, confidence score, and anomaly flag, and search by description,
so that I can quickly find specific transactions or groups of transactions.

#### Acceptance Criteria

1. Filter panel component created above transaction table with collapsible sections: Date Range, Category, Confidence Score, Anomaly Flag, Search
2. Date range filter uses shadcn/ui Calendar component with start/end date selection, preset buttons: "This Month", "Last Month", "Last Quarter", "Custom"
3. Category filter displays multi-select dropdown populated from unique categories in transactions table (both manual and AI categories), allows selecting multiple categories
4. Confidence score filter shows range slider (0.0-1.0) with visual segments: Low (<0.7), Medium (0.7-0.89), High (≥0.9), allows selecting min/max thresholds
5. Anomaly flag filter provides checkbox: "Show only anomalies" which filters for transactions where `anomaly_score > 0.7`
6. Search input field provides real-time search (debounced 300ms) across: description, merchant name, reference fields using Supabase `ilike` query
7. Active filters displayed as removable badges below filter panel showing: "Category: Groceries", "Date: Jan 2025", "Confidence: <0.7" with X button to remove individual filters
8. "Clear All Filters" button resets all filters to default state and refreshes transaction list
9. Filter state persists in URL query params: `/transactions?category=groceries&startDate=2025-01-01&confidence=0.7-1.0` for shareable links
10. Filtered transaction count updates dynamically: "Showing X of Y transactions (Z filtered)" with Y being total unfiltered count

### Story 3.3: ML Prediction Display & Confidence Indicators

As a user,
I want to see ML categorization predictions with visual confidence indicators,
so that I can quickly identify which transactions need manual review.

#### Acceptance Criteria

1. Category column in transaction table displays AI-predicted category from `ai_category` field with fallback to manual category
2. Confidence score displayed as colored badge in dedicated column: High (≥0.9, green), Medium (0.7-0.89, amber), Low (<0.7, red)
3. Low-confidence transactions (<0.7) highlighted with yellow background row color to draw attention
4. Tooltip on confidence badge shows exact confidence score (e.g., "0.82 confidence") on hover using shadcn/ui Tooltip
5. Category cell shows both AI category (if exists) and manual category (if overridden) with strikethrough on AI category if manual override exists
6. "Needs Review" filter preset button added to filter panel: one-click filter for transactions with confidence < 0.7 OR anomaly_score > 0.7
7. Review queue count badge displayed in transactions navigation menu: "Transactions (X)" where X is count of transactions needing review
8. Sort functionality added: clicking confidence column header sorts transactions by confidence score ascending/descending
9. Batch selection enabled for low-confidence transactions: checkbox column on left of table, "Select All Low Confidence" button
10. ML model name/version displayed in table header tooltip: "Categories predicted by Model: transaction-categorizer-v2" with link to settings/ML metrics page

### Story 3.4: Inline Category Override & Audit Logging

As a user,
I want to manually override incorrect ML categorizations directly in the transaction table,
so that I can correct mistakes without navigating to detail pages.

#### Acceptance Criteria

1. Category column cells made editable: double-click or click pencil icon activates inline edit mode with dropdown
2. Category dropdown populated from `accounts` table filtered by account_type (expense/revenue categories) relevant to transaction amount sign
3. Selecting new category triggers immediate update: Supabase update query sets `category` field, `ai_category_override = true`, `confidence_score = null`
4. Override action logged to audit trail: timestamp, user_id, transaction_id, old_category (AI), new_category (manual), reason field (optional modal prompt)
5. Visual indicator shows overridden categories: manual category displayed with badge "Manual" next to category name, AI category shown in strikethrough in tooltip
6. Undo capability: "Revert to AI" button appears on overridden categories, clicking restores `ai_category`, sets `ai_category_override = false`
7. Bulk override modal for selected transactions: "Categorize Selected" button opens modal with category dropdown, applies same category to all selected transactions
8. Optimistic UI update: category change reflects immediately in table before Supabase confirmation, shows spinner during save
9. Error handling: if update fails, revert optimistic change, display error toast "Failed to update category", log error
10. Success feedback: green checkmark animation on successful category update, toast notification "X transactions updated"

### Story 3.5: Transaction Detail Page with Full Edit

As a user,
I want to view complete transaction details including ML insights and edit all fields,
so that I can correct errors, add notes, and review anomaly information.

#### Acceptance Criteria

1. Transaction detail page created at `/app/transactions/[id]/page.tsx` with two-column layout: details (left), ML insights (right)
2. Left column displays editable fields using React Hook Form + Zod: Description, Amount, Date, Category (dropdown), Notes (textarea), Tags (multi-select)
3. Right column shows ML insights: AI Category (read-only, badge), Confidence Score (progress bar), Anomaly Score (if >0.5, with severity indicator), Model Version
4. Anomaly section (if applicable) displays: Anomaly Score (0-1), Reason from ML model, Similar transactions comparison (optional), "Mark as False Positive" button
5. Transaction metadata shown: Transaction ID, Created Date, Last Modified Date, Modified By (user), Bank Account (if synced from UpBank)
6. Edit form validation: amount must be number with 2 decimal places, date cannot be future, category required, description max 200 characters
7. "Save Changes" button triggers Supabase update with optimistic UI update, logs edit to audit trail with changed fields tracked
8. "Cancel" button reverts form to original values without saving, returns to transaction list with confirmation dialog if unsaved changes exist
9. Delete transaction action: "Delete" button (red, with confirmation modal) soft-deletes transaction (sets `deleted_at` timestamp), redirects to transaction list
10. Breadcrumb navigation: "Transactions > [Transaction Description]" links back to transaction list preserving filters via URL state

### Story 3.6: Bulk Transaction Operations

As a user,
I want to select multiple transactions and perform bulk actions (categorize, delete, export),
so that I can efficiently manage large numbers of similar transactions.

#### Acceptance Criteria

1. Checkbox column added to left of transaction table for row selection, header checkbox selects/deselects all visible rows
2. Selection state managed in React useState: array of selected transaction IDs, persists across pagination pages
3. Bulk action toolbar appears when ≥1 transaction selected: fixed bar at top of table showing "X selected" count and action buttons
4. "Categorize Selected" action opens modal with category dropdown, "Apply to X transactions" button, confirmation shows list of transactions to update
5. "Delete Selected" action shows confirmation modal listing transactions to delete, "Confirm Delete" button soft-deletes all selected transactions
6. "Export Selected" action triggers CSV download with selected transactions only, includes all fields: date, description, category, amount, confidence, anomaly score
7. "Deselect All" button clears selection, hides bulk action toolbar
8. Bulk operations show progress indicator: modal with progress bar "Processing X of Y transactions...", prevents user from navigating away during operation
9. Error handling for bulk ops: if any transaction fails, show detailed error modal listing failed transaction IDs, successfully processed count, option to retry failed
10. Success feedback: toast notification "X transactions updated successfully", table refreshes with updated data, selection cleared

### Story 3.7: Transaction Split Functionality

As a user,
I want to split a single transaction into multiple line items with different categories,
so that I can accurately categorize mixed-purpose expenses (e.g., office supplies + food in one receipt).

#### Acceptance Criteria

1. "Split Transaction" button added to transaction detail page and table row actions menu
2. Split modal displays: original transaction amount (read-only header), form to add split line items (description, category, amount)
3. Add line item button creates new row in split form with fields: Description (text), Category (dropdown), Amount (number), delete row icon
4. Split amounts must sum to original transaction amount: validation shows error if total ≠ original, disabled "Save Split" button until valid
5. Real-time sum calculation displayed: "Total: $X / $Y" where X is current split total, Y is original amount, color-coded red if mismatch, green if match
6. Saving split creates child transactions in database: parent transaction gets `is_split = true` flag, child transactions reference parent via `parent_transaction_id`
7. Parent transaction displayed in list with split indicator icon, clicking expands to show child transactions indented below with amounts summing to parent
8. Child transactions inherit parent metadata: date, bank_account_id, but have independent categories, descriptions, confidence scores (set to null as manual)
9. Undo split action: "Unsplit" button on parent transaction deletes child transactions, restores parent to normal single transaction
10. Split transactions appear in exports and reports as separate line items with parent transaction ID included for traceability

---

## Epic 4: Invoice Management & PDF Generation

**Epic Goal**: Create a complete invoice management system that handles the full lifecycle from creation to payment tracking. Users can create professional invoices with multiple line items, automatic GST calculation, and client/supplier selection from contacts. The system generates PDF invoices with proper formatting, entity branding, and Australian tax compliance (ABN, GST breakdown). Invoice status tracking (draft, sent, paid, overdue) with automatic overdue flagging enables proactive follow-up. This epic eliminates the current pain point of manual invoice creation and tracking, provides professional client-facing documents, and ensures tax compliance for all receivables and payables.

### Story 4.1: Invoice List Page with Status Filtering

As a user,
I want to view all invoices in a filterable list with status indicators,
so that I can quickly see outstanding invoices, overdue items, and payment status.

#### Acceptance Criteria

1. Invoice list page created at `/app/invoices/page.tsx` with table layout displaying columns: Invoice Number, Client/Supplier, Issue Date, Due Date, Amount, Status, Actions
2. Data fetching service queries Supabase `invoices` table with joins to `contacts` for client/supplier names, filtered by active entity_id
3. Status column displays colored badges: Draft (gray), Sent (blue), Paid (green), Overdue (red) using shadcn/ui Badge component
4. Status calculation logic: Overdue if `due_date < current_date AND status != 'paid'`, automatically updates on page load
5. Filter panel above table with filters: Status (multi-select dropdown), Date Range (issue date or due date selector), Client/Supplier (dropdown from contacts), Amount Range (min/max inputs)
6. Sort functionality: clicking column headers sorts by Invoice Number (numeric), Date (chronological), Amount (numeric) ascending/descending
7. Quick action buttons in Actions column: "View PDF" (opens PDF in new tab), "Mark as Paid" (updates status with payment date modal), "Edit" (navigates to edit page), "Delete" (with confirmation)
8. Summary cards above table show KPIs: Total Outstanding (sum of unpaid invoice amounts), Overdue Count, Paid This Month (sum), Draft Count
9. "Create Invoice" button in page header navigates to `/invoices/new` (Story 4.2)
10. Empty state handled: if no invoices exist, display "No invoices yet" message with large "Create Your First Invoice" button

### Story 4.2: Invoice Creation Form with Line Items

As a user,
I want to create a new invoice with multiple line items and client selection,
so that I can bill clients for services or products with itemized details.

#### Acceptance Criteria

1. Invoice creation page at `/app/invoices/new` with multi-section form: Invoice Details (top), Line Items (middle), Totals (right sidebar)
2. Invoice Details section fields using React Hook Form + Zod validation: Client (searchable dropdown from contacts table filtered by type='customer' or type='both'), Issue Date (date picker, default today), Due Date (date picker, default +30 days), Payment Terms (dropdown: "Net 7", "Net 14", "Net 30", "Net 60"), Invoice Number (auto-generated from sequence, editable)
3. Line Items section displays dynamic table: Description (text), Quantity (number), Unit Price (currency), GST (checkbox, default checked), Amount (calculated: qty * price, read-only)
4. "Add Line Item" button appends new row to line items array, "Remove" icon on each row deletes line item (minimum 1 row required)
5. Totals sidebar calculates in real-time: Subtotal (sum of line amounts excluding GST), GST (10% of GST-applicable line items), Total (Subtotal + GST) displayed with large bold text
6. Form validation: Client required, Issue Date cannot be future, Due Date must be after Issue Date, at least one line item required, all line item fields required
7. "Save as Draft" button saves invoice with status='draft', shows success toast, redirects to invoice list
8. "Save & Send" button (future: sends email to client) saves with status='sent', generates PDF (Story 4.3), shows success modal with PDF preview and send confirmation
9. "Cancel" button returns to invoice list with confirmation dialog if unsaved changes exist
10. Auto-save draft functionality: every 30 seconds, save form state to localStorage with key `invoice-draft-[timestamp]`, restore on page load if draft exists with "Resume Draft" prompt

### Story 4.3: PDF Invoice Generation with Branding

As a user,
I want to generate professional PDF invoices with my business branding and GST details,
so that I can send compliant tax invoices to clients.

#### Acceptance Criteria

1. PDF generation service created using `@react-pdf/renderer` in `/lib/pdf/invoice.tsx` with custom Document component
2. PDF layout includes header: Entity name (MOKAI PTY LTD), ABN (fetched from entities table), logo (optional, placeholder if not available), address, contact details
3. Invoice details section displays: Invoice number (large, bold), Issue Date, Due Date, Payment Terms in structured table on right side of header
4. Bill To section shows: Client name, ABN (if available), address from contacts table in left column below header
5. Line items table with columns: Description, Quantity, Unit Price (inc/ex GST based on preference), GST, Amount with alternating row colors for readability
6. Totals section at bottom right: Subtotal, GST (10%, itemized), Total Due with bold text, large font
7. Footer includes: Payment instructions text ("Please pay to: [bank account details]"), Terms & Conditions (optional text from settings), "Tax Invoice" label for GST compliance
8. PDF styling: Professional sans-serif font (Helvetica), entity brand colors (if configured, fallback to neutral gray/blue), proper spacing, page margins 20mm
9. PDF generation triggered by "Download PDF" button on invoice detail page or "View PDF" in invoice list, opens in new browser tab or triggers download
10. File naming convention: `invoice-[invoice_number]-[client_name]-[date].pdf` (e.g., "invoice-INV-001-MOKAI-2025-01-15.pdf"), stored temporarily for download

### Story 4.4: Invoice Status Tracking & Payment Recording

As a user,
I want to update invoice status from sent to paid and record payment details,
so that I can track which invoices have been settled and when.

#### Acceptance Criteria

1. "Mark as Paid" button on invoice detail page and quick action in invoice list opens payment modal
2. Payment modal form captures: Payment Date (date picker, default today), Amount Paid (number, default invoice total, allows partial payments), Payment Method (dropdown: Bank Transfer, Credit Card, Cash, Cheque, Other), Reference/Notes (text area)
3. Submitting payment form updates invoice: status='paid', payment_date set, payment_method stored, notes saved
4. Partial payment handling: if amount paid < invoice total, status='partially_paid' (new status), remaining balance calculated and displayed
5. Payment history table on invoice detail page: shows all payment records for invoice (date, amount, method, reference) if multiple partial payments exist
6. Automatic overdue status update: background job or on-page-load check compares due_date with current date, updates status='overdue' if unpaid and past due
7. Overdue invoice notification: red badge on invoice in list, "Overdue by X days" text, email reminder option (future: automated emails)
8. "Unpay" action on paid invoices (optional, for corrections): button reverts status to 'sent', clears payment_date, logs action in audit trail
9. Dashboard KPI updates when payment recorded: Outstanding amount decreases, Paid This Month increases with real-time refresh
10. Payment recorded audit log entry: timestamp, user_id, invoice_id, old_status, new_status, amount_paid, payment_method

### Story 4.5: Invoice Edit & Delete Functionality

As a user,
I want to edit draft invoices and delete invoices that were created in error,
so that I can correct mistakes before sending to clients.

#### Acceptance Criteria

1. Invoice detail page displays "Edit Invoice" button for invoices with status='draft', navigates to `/invoices/[id]/edit`
2. Edit page pre-populates form with existing invoice data: client, dates, line items, all fields editable
3. Editing sent/paid invoices shows warning: "This invoice has been sent. Editing will create a new version and mark the original as superseded." with confirmation required
4. Invoice versioning: editing sent invoice creates new row with version incremented, original invoice gets `superseded_by_id` reference to new version
5. "Delete Invoice" button (red, with trash icon) available on draft invoices only, shows confirmation modal "Are you sure? This cannot be undone."
6. Delete action soft-deletes invoice: sets `deleted_at` timestamp, removes from list views but retains in database for audit, logs deletion in audit trail
7. Sent/paid invoices cannot be deleted directly, require "Void" action: button creates credit note (future feature) or marks status='voided' with reason required
8. Edit form validation same as creation: client required, dates valid, line items valid, totals calculated correctly
9. "Save Changes" updates invoice, regenerates PDF if line items or amounts changed, shows success toast
10. Version history displayed on invoice detail page for invoices with versions: "Version 2 (Current)" with link to "View Version 1" showing read-only original

### Story 4.6: Client/Supplier Quick Add from Invoice Form

As a user,
I want to quickly add a new client while creating an invoice without leaving the form,
so that I don't lose my invoice draft when creating a client for the first time.

#### Acceptance Criteria

1. Client dropdown in invoice form includes "+ Add New Client" option at top of list
2. Clicking "+ Add New Client" opens modal overlay with contact creation form (does not navigate away from invoice page)
3. Contact quick-add form fields: Name (required), Email (optional), Phone (optional), ABN (optional, 11-digit validation), Address (optional), Type (radio: Customer, Supplier, Both - default Customer)
4. Form validation in modal: Name required (min 2 chars), Email valid format if provided, ABN exactly 11 digits if provided
5. "Save & Select" button in modal creates contact in Supabase `contacts` table linked to active entity_id, closes modal, auto-selects new contact in invoice client dropdown
6. "Cancel" button closes modal without saving, returns focus to client dropdown in invoice form
7. Contact creation logged in audit trail: timestamp, user_id, contact_id, created_from='invoice_form'
8. Newly created contact immediately available in client dropdown without page refresh (optimistic UI update)
9. Error handling: if contact creation fails (e.g., duplicate name check), display error in modal, do not close, allow user to correct and retry
10. Success feedback: green checkmark animation in modal on successful save, contact name highlighted in dropdown after selection

### Story 4.7: Invoice Batch Actions & Export

As a user,
I want to select multiple invoices and perform batch operations (download PDFs, mark paid, export CSV),
so that I can efficiently manage invoices in bulk.

#### Acceptance Criteria

1. Checkbox column added to invoice list table for row selection, header checkbox selects/deselects all visible invoices
2. Selection state persists across pagination: selected invoice IDs stored in state array
3. Bulk action toolbar appears when ≥1 invoice selected: "X selected" count, action buttons (Download PDFs, Mark as Paid, Export CSV, Delete)
4. "Download PDFs" action generates ZIP file containing PDFs of all selected invoices, triggers browser download with filename `invoices-[date].zip`
5. "Mark as Paid" batch action opens modal: Payment Date (single date for all), Payment Method (single method for all), applies to all selected invoices, shows confirmation with list
6. "Export CSV" generates CSV file with columns: Invoice Number, Client Name, Issue Date, Due Date, Amount, GST, Total, Status, exports selected invoices only
7. "Delete" batch action shows confirmation modal with list of invoice numbers to delete, only allows deletion of draft invoices (filters out sent/paid with warning)
8. Progress indicator for batch operations: modal shows "Processing X of Y invoices..." with progress bar during PDF generation or updates
9. Error handling: if any invoice fails during batch operation, show summary modal "X succeeded, Y failed" with list of failed invoice numbers and retry option
10. Success feedback: toast notification "X invoices processed successfully", clears selection, refreshes table data

---

## Epic 5: Reports & Tax Compliance

**Epic Goal**: Implement comprehensive reporting and tax compliance features that enable accurate, one-click generation of Business Activity Statements (BAS) with GST calculations following Australian tax rules, income statements (Profit & Loss) with revenue/expense breakdowns by category, and flexible data export functionality in multiple formats (CSV, Excel, accounting software compatible). These reports leverage existing transaction and invoice data from Supabase, apply proper GST treatment based on account configurations, and provide period selection (monthly, quarterly, annual, custom) with preview capabilities. This epic solves the critical pain point of tax compliance document preparation, reduces accountant review time, and ensures Harrison can submit BAS returns confidently without manual spreadsheet work.

### Story 5.1: BAS Calculation Engine & Data Service

As a developer,
I want to implement a BAS calculation service that accurately computes GST collected, paid, and net position,
so that BAS reports display correct tax figures following Australian tax rules.

#### Acceptance Criteria

1. BAS calculation service created in `/lib/reports/bas.ts` with function `calculateBAS(entityId, startDate, endDate)` returning structured BAS data
2. GST collected calculation: sum of GST amounts from invoices with status='paid' where entity is supplier, filtered by payment_date in selected period
3. GST paid calculation: sum of GST amounts from transactions where category.gst_claimable=true (business expenses), filtered by transaction_date in selected period
4. Net GST calculation: GST Collected - GST Paid, positive value = amount owed to ATO, negative value = refund due
5. Revenue calculations for BAS fields: G1 (Total Sales including GST), G2 (Export sales), G3 (Other GST-free sales) based on transaction categories and GST treatment flags
6. Expense calculations: G10 (Capital purchases), G11 (Non-capital purchases) from categorized expenses with GST amounts
7. Wine Equalization Tax (WET) fields included as placeholders (G13-G18) defaulting to $0 unless relevant transactions exist
8. Luxury Car Tax (LCT) fields included as placeholders (G19-G20) defaulting to $0 unless relevant transactions exist
9. PAYG withholding fields (4, 5A, 5B) calculated from payroll transactions if payroll module exists, otherwise default to $0 with user override option
10. Calculation accuracy tested: unit tests verify GST rounding rules (round to nearest cent), negative value handling, edge cases (zero transactions, partial period)

### Story 5.2: BAS Report Generation Page

As a user,
I want to generate a BAS report for a specific quarter and preview before submitting,
so that I can verify tax figures are correct before filing with the ATO.

#### Acceptance Criteria

1. BAS report page created at `/app/reports/bas` with period selector: Quarter dropdown (Q1 Jan-Mar, Q2 Apr-Jun, Q3 Jul-Sep, Q4 Oct-Dec), Year selector, Entity selector
2. "Generate BAS" button triggers calculation service with selected period, displays loading spinner during computation
3. BAS report displays in ATO-compliant format with sections: Sales & Income (G1-G3, 1A, 1B), Purchases & Expenses (G10-G11), GST Summary (1A, 1B, 7), Other Taxes (WET, LCT, PAYG)
4. Each BAS field shows: Field label (e.g., "G1 Total Sales"), Calculated amount (currency formatted), Explanation tooltip (what transactions are included)
5. GST Summary section prominently displays: GST on Sales (1A), GST on Purchases (1B), Net Amount (7) with large bold text, color-coded green (refund) or red (payment due)
6. "View Supporting Transactions" expandable sections for each field: clicking shows filtered transaction list that contributed to that BAS field amount
7. Manual adjustment capability: each field has "Adjust" button opening modal to add manual adjustment amount with required reason text (logged in audit trail)
8. PDF export button generates BAS PDF in ATO-compatible format with all fields, entity details (ABN, name, address), reporting period, generation date
9. CSV export option provides machine-readable format with field codes and amounts for upload to accounting software or ATO portal
10. Warning indicators: if any field has manual adjustments, show warning icon with "This field includes manual adjustments" tooltip

### Story 5.3: Income Statement (P&L) Generation

As a user,
I want to generate a Profit & Loss statement showing revenue and expenses by category,
so that I can understand financial performance for tax reporting and business analysis.

#### Acceptance Criteria

1. Income statement page created at `/app/reports/income-statement` with period selector: Month, Quarter, Year, Custom Date Range, Entity selector
2. "Generate Report" button triggers calculation service in `/lib/reports/income-statement.ts` with function `calculatePnL(entityId, startDate, endDate)`
3. Revenue section displays categories with amounts: sum of transactions where amount > 0 OR category.type='revenue', grouped by category name, subtotal all revenue
4. Expense section displays categories with amounts: sum of transactions where amount < 0 OR category.type='expense', grouped by category name, subtotal all expenses
5. Category grouping logic: uses parent categories from chart of accounts (e.g., "Operating Expenses" > "Rent", "Utilities"), displays hierarchical tree structure
6. Cost of Goods Sold (COGS) section (if applicable): separate from operating expenses, calculates from inventory/materials categories
7. Net Profit calculation: Total Revenue - Total Expenses - COGS, displayed with large bold text, color-coded green (profit) or red (loss)
8. Comparison column option: checkbox to show "Compare with Previous Period", displays prior period amounts and variance ($ and %) side-by-side
9. Chart visualization: horizontal bar chart showing top 5 revenue categories and top 5 expense categories by amount using Recharts
10. Export options: PDF (formatted statement with entity header, period, signature line), CSV (category, amount, type), Excel (with formulas preserved)

### Story 5.4: Report Period Selection & Fiscal Year Support

As a user,
I want to select reporting periods using calendar months, quarters, fiscal years, or custom ranges,
so that I can generate reports aligned with my business and tax reporting requirements.

#### Acceptance Criteria

1. Period selector component created with dropdown options: This Month, Last Month, This Quarter, Last Quarter, This Financial Year, Last Financial Year, Custom Range
2. Financial year definition configurable in Settings: default July 1 - June 30 (Australian standard), allows override to Jan 1 - Dec 31 or custom start month
3. Quarter calculation based on fiscal year setting: Q1 = Jul-Sep, Q2 = Oct-Dec, Q3 = Jan-Mar, Q4 = Apr-Jun for July start, adjusts if different fiscal year
4. Custom range selection opens date picker modal: start date and end date selectors, validation ensures start < end, max range 5 years
5. Selected period displayed clearly: "Reporting Period: [Start Date] - [End Date]" with fiscal year indicator if applicable (e.g., "FY 2024-25")
6. Period selection persists in URL query params: `/reports/bas?period=Q1&fiscalYear=2025` for shareable links
7. Period comparison logic in reports: "Previous Period" automatically calculates equivalent prior period (e.g., if Q2 2025 selected, previous = Q2 2024)
8. Year-to-date (YTD) calculations: option to show YTD figures from fiscal year start to current date alongside period-specific figures
9. Period boundary handling: transactions dated exactly on period boundary dates included in period (inclusive start and end dates)
10. Multi-year reports supported: custom range can span multiple fiscal years, reports group data by year with subtotals if >1 year selected

### Story 5.5: Transaction Data Export (CSV, Excel, Accounting Formats)

As a user,
I want to export transaction data in multiple formats compatible with accounting software,
so that I can share data with my accountant or import into Xero/MYOB.

#### Acceptance Criteria

1. Export page created at `/app/reports/export` with options: Data Type (Transactions, Invoices, Contacts, Accounts), Format (CSV, Excel, Xero, MYOB), Period, Entity
2. CSV export generates file with columns: Date, Description, Reference, Category, Account Code, Debit, Credit, GST, Net Amount using `papaparse` library
3. Excel export generates .xlsx file with formatted table: headers bold, currency columns formatted, date columns formatted, freeze top row, auto-column width using `xlsx` library
4. Xero format export follows Xero bank import CSV spec: Date, Amount, Payee, Description, Reference, Code (account code) with proper header row
5. MYOB format export follows MYOB import spec: Date, Amount, Memo, Account, Job (optional), Category with tab-delimited option
6. Column selector allows customizing export fields: checkboxes for all available columns (Transaction ID, Entity, ML Confidence, Anomaly Score, etc.), drag-to-reorder
7. Filter application: exports respect active filters from transaction list page (category, date range, confidence score) with "Export Filtered" button
8. Large dataset handling: for exports >10,000 records, show progress modal "Generating export X of Y records...", stream data to prevent memory issues
9. File naming convention: `[entity-name]-[data-type]-[start-date]-[end-date].[format]` (e.g., "MOKAI-transactions-2025-01-01-2025-01-31.csv")
10. Success feedback: download triggers automatically, toast notification "Export completed: X records", option to email export file (future feature)

### Story 5.6: Report Preview & Validation

As a user,
I want to preview reports before generating PDFs or exporting data,
so that I can verify calculations and data accuracy without repeatedly generating files.

#### Acceptance Criteria

1. All report pages (BAS, Income Statement, Export) display preview pane: split view with filters/options on left, live preview on right
2. Preview updates in real-time as period or filters change: debounced 500ms after user interaction, shows loading spinner during recalculation
3. Preview pane displays report exactly as it will appear in PDF: same formatting, fonts, layout using HTML/CSS matching PDF renderer
4. Validation warnings shown in preview: "No transactions found for period", "Missing GST information for X transactions", "Manual adjustments applied to Y fields"
5. Data source indicators: tooltips on amounts show "Based on X transactions from [date range]", clickable to drill down to transaction list
6. Calculation breakdown accordion sections: expandable sections showing how totals are computed (e.g., "Revenue: Category A $X + Category B $Y = Total $Z")
7. Preview refresh button: manual refresh option if data has changed (new transactions synced) since preview was generated
8. Print preview mode: "Print" button opens browser print dialog with report optimized for A4 paper, proper page breaks
9. Watermark on preview: "PREVIEW ONLY - NOT FOR SUBMISSION" watermark overlaid on preview pane, removed in final PDF
10. Side-by-side comparison mode: option to show two periods side-by-side in preview for visual comparison (e.g., This Quarter vs Last Quarter)

### Story 5.7: Scheduled Report Generation & Email Delivery

As a user,
I want to schedule automatic monthly BAS and P&L report generation with email delivery,
so that I receive reports without manually generating them each month.

#### Acceptance Criteria

1. Report scheduling page created at `/app/reports/schedules` with options to create scheduled report jobs
2. Schedule creation form fields: Report Type (BAS, Income Statement, Export), Frequency (Weekly, Monthly, Quarterly), Day of Week/Month, Time, Recipients (email addresses)
3. Email recipients field accepts multiple email addresses (comma-separated), validates email format using Zod schema
4. Schedule storage in Supabase table `report_schedules` with fields: entity_id, report_type, frequency, schedule_config (cron expression), recipients, active (boolean)
5. Background job runner (Vercel Cron or similar) checks schedules daily, triggers report generation at configured time
6. Email service integration: uses Supabase Edge Function or Vercel Serverless Function to send emails with report PDF attached via SendGrid/SES
7. Email template includes: Entity name, Report period, PDF attachment, link to view online in dashboard, "Reply to unsubscribe" footer
8. Schedule management UI: list of active schedules, toggle active/inactive, edit schedule, delete schedule, "Run Now" button to trigger immediately
9. Execution history log: table showing last 10 executions per schedule with timestamp, status (success/failed), recipient count, error message if failed
10. Error handling: if report generation fails, email admin with error details, retry mechanism (3 attempts with exponential backoff), log failure in execution history

---

## Epic 6: Settings, Administration & Multi-Entity

**Epic Goal**: Build comprehensive settings and administration interfaces that enable configuration of user preferences (default entity, date formats, dashboard layouts), management of business entities, contacts, and chart of accounts, viewing of audit logs for compliance, and monitoring of ML model performance metrics. This epic provides the administrative foundation for multi-entity accounting, ensures data governance through audit trails, allows customization of user experience, and surfaces ML system health indicators. By consolidating all configuration and administrative functions in a centralized settings area, users can efficiently manage system behavior, maintain data quality, and troubleshoot issues without developer intervention.

### Story 6.1: User Preferences Settings Page

As a user,
I want to configure my personal preferences (default entity, date format, currency display, notifications),
so that the dashboard behaves according to my working style and regional settings.

#### Acceptance Criteria

1. Settings page created at `/app/settings/preferences` with tabbed interface: General, Display, Notifications, Security (tabs)
2. General tab fields using React Hook Form + Zod: Default Entity (dropdown from user's accessible entities), Language (dropdown: English AU, future: other locales), Timezone (dropdown: Australia/Sydney, etc.)
3. Display tab fields: Date Format (dropdown: DD/MM/YYYY, MM/DD/YYYY, YYYY-MM-DD), Currency Display (AUD symbol placement: $X,XXX.XX or X,XXX.XX AUD), Number Format (comma/period separators)
4. Dashboard Layout section: checkbox options to show/hide widgets (Recent Transactions, Anomaly Alerts, Charts), drag-and-drop reordering (optional, nice-to-have)
5. Notifications tab: toggle switches for notification types (Email: New Anomalies, Overdue Invoices, Low Confidence Predictions; In-App: same options), email address field for notifications
6. Security tab: "Change Password" button opening modal for password update via Supabase Auth, "Session Management" showing active sessions with "Logout All" option
7. Preferences stored in Supabase `user_preferences` table with user_id foreign key, JSON column for flexible preference storage
8. "Save Preferences" button triggers update query, shows success toast "Preferences saved", applies changes immediately (date format, currency display refresh)
9. "Reset to Defaults" button restores all preferences to system defaults with confirmation dialog
10. Real-time preview: changes to date/currency format show live preview example above input fields (e.g., "Example: 15/01/2025, $1,234.56")

### Story 6.2: Entity Management Interface

As a user,
I want to view, create, and edit business entity details (name, ABN, address, banking),
so that I can manage multiple businesses accurately in the system.

#### Acceptance Criteria

1. Entity management page created at `/app/settings/entities` displaying list of entities with cards: entity name, type (Company, Sole Trader), ABN, status (active/inactive)
2. "Add Entity" button opens modal with form fields: Name (required), Type (dropdown: Company, Sole Trader, Partnership, Trust), ABN (11-digit validation), Address (structured: street, city, state, postcode), Email, Phone
3. Entity edit action: clicking entity card or edit icon opens same modal pre-populated with entity data, allows updating all fields except entity_id
4. Banking details section in entity form: Bank Name, BSB (6-digit validation), Account Number, Account Name for payment instructions on invoices
5. Logo upload field: file input accepting image formats (PNG, JPG), max 2MB, stores image URL in Supabase Storage, displays thumbnail preview
6. Entity activation toggle: switch to set entity active/inactive status, inactive entities hidden from entity selector dropdown but retained in database
7. Entity creation saves to `entities` table with created_by user_id, logs creation in audit trail
8. Default entity designation: radio button in list to set one entity as default for new users, stored in user_preferences
9. Entity deletion prevention: if entity has transactions/invoices, show error "Cannot delete entity with existing data", allow archive instead (sets deleted_at timestamp)
10. Access control: only admin users can create/edit/delete entities, regular users can only switch between entities (role-based access control check)

### Story 6.3: Contact Management (Customers & Suppliers)

As a user,
I want to manage my customer and supplier contacts with detailed information,
so that I can select them efficiently when creating invoices and categorizing transactions.

#### Acceptance Criteria

1. Contacts page created at `/app/settings/contacts` with table view displaying: Name, Type (Customer, Supplier, Both), Email, Phone, ABN, Actions
2. Filter/search bar above table: search by name or ABN, filter by type (Customer, Supplier, Both), filter by active/archived status
3. "Add Contact" button opens modal with form fields: Name (required), Type (radio: Customer, Supplier, Both), Email (validated format), Phone (formatted input), ABN (11-digit, optional), Address (structured fields), Notes (textarea)
4. Contact edit action: clicking row or edit icon opens modal with pre-populated data, all fields editable
5. Contact detail view: clicking contact name navigates to `/settings/contacts/[id]` showing full details, transaction history with this contact, invoices sent/received, total amounts
6. Bulk import functionality: "Import Contacts" button accepts CSV file with column mapping interface (map CSV columns to contact fields), validates and imports with error reporting
7. Archive contact action: sets `archived_at` timestamp, removes from dropdown selectors but retains in database and shows in "Archived" filter view
8. Duplicate detection: when creating contact, if name or ABN matches existing contact, show warning "Similar contact exists: [Name]" with option to view or continue
9. Contact merge functionality: select two duplicate contacts, "Merge" button combines data (choose primary, migrate transactions/invoices to primary, soft-delete duplicate)
10. Export contacts: "Export" button generates CSV with all contact fields, respects active filters (exports filtered subset if filters applied)

### Story 6.4: Chart of Accounts Management

As a user,
I want to view and configure my chart of accounts with tax treatment settings,
so that I can categorize transactions accurately for tax reporting.

#### Acceptance Criteria

1. Chart of accounts page created at `/app/settings/accounts` displaying hierarchical tree: parent accounts with expandable child accounts
2. Account table columns: Account Code, Account Name, Type (Asset, Liability, Equity, Revenue, Expense), Tax Treatment (GST-free, Input Taxed, GST), Status (Active/Inactive)
3. Account type filtering: buttons to filter view by account type (show only Revenue accounts, only Expense accounts, etc.)
4. "Add Account" button opens modal with fields: Account Code (auto-generated from sequence or manual entry), Name (required), Parent Account (dropdown of parent accounts, optional), Type (dropdown), Tax Treatment (dropdown: GST on Income, GST on Expenses, GST-free, Input Taxed, Not Reportable), Description (textarea)
5. Tax treatment configuration determines: whether GST is added to amounts, whether GST is claimable on BAS, how account appears in reports
6. Account editing: click account row to edit code, name, tax treatment, cannot change type if transactions exist (show warning)
7. Account activation toggle: inactive accounts hidden from category selectors in transaction forms but retained in database, transactions retain reference
8. Default accounts system: pre-populate standard Australian chart of accounts on entity creation (100s Assets, 200s Liabilities, 300s Equity, 400s Revenue, 500s Expenses)
9. Account usage statistics: each account row shows transaction count, total amount (sum of transactions using this account), last used date
10. Account merge/reassign: if deleting account with transactions, require selecting target account to reassign all transactions before deletion allowed

### Story 6.5: Audit Log Viewer

As a user,
I want to view a comprehensive audit log of all data changes,
so that I can track who modified financial data and when for compliance and troubleshooting.

#### Acceptance Criteria

1. Audit log page created at `/app/settings/audit-log` with table displaying: Timestamp, User, Action (Created, Updated, Deleted), Object Type (Transaction, Invoice, Contact, etc.), Object ID, Changes (summary)
2. Audit log data fetched from `audit_log` table with columns: id, timestamp, user_id (FK to auth.users), action, object_type, object_id, old_values (JSON), new_values (JSON), ip_address, user_agent
3. Filter panel with options: Date Range (calendar picker), User (dropdown of all users), Action Type (checkboxes: Created, Updated, Deleted), Object Type (dropdown: Transaction, Invoice, Contact, Account, etc.)
4. Search functionality: text input searches across object_type, object_id, and change summaries
5. Changes column displays diff view: "Category: Groceries → Office Supplies", "Amount: $50.00 → $55.00" showing old and new values side-by-side
6. Expandable row detail: clicking row expands to show full JSON diff of old_values vs new_values with syntax highlighting
7. Pagination and sorting: table supports sorting by timestamp (default newest first), pagination with 50 entries per page
8. Export audit log: "Export" button generates CSV with all log entries respecting active filters, includes all columns
9. Retention policy indicator: banner shows "Audit logs retained for 7 years" (NFR9 requirement), displays oldest available log entry date
10. Performance optimization: audit log queries use database indexes on timestamp, user_id, object_type for fast filtering even with millions of records

### Story 6.6: ML Model Performance Metrics Dashboard

As a user,
I want to view ML model performance metrics (accuracy, confidence distribution, prediction counts),
so that I can understand how well the AI is categorizing transactions and identify areas for improvement.

#### Acceptance Criteria

1. ML metrics page created at `/app/settings/ml-metrics` with overview cards: Total Predictions, Average Confidence, Categorization Accuracy, Anomalies Detected
2. Model list section displays active models from `ml_models` table: model_id, model_name (e.g., "transaction-categorizer-v2"), version, deployment_date, status (active/retired)
3. Categorization accuracy calculation: percentage of predictions with confidence ≥0.9 that were NOT manually overridden (indicates model correctness)
4. Confidence distribution chart: histogram using Recharts showing count of predictions in buckets (0-0.1, 0.1-0.2, ..., 0.9-1.0) with color coding (red <0.7, amber 0.7-0.89, green ≥0.9)
5. Category prediction breakdown table: shows top 10 categories by prediction count, accuracy % (predictions accepted vs overridden), average confidence
6. Anomaly detection metrics: total anomalies detected, false positive rate (anomalies marked as false positive / total anomalies), detection rate by severity (high, medium)
7. Model performance trend chart: line chart showing accuracy % and average confidence over last 6 months to identify degradation
8. Prediction volume chart: bar chart showing count of predictions per week to monitor system usage
9. Model comparison view: if multiple model versions exist, side-by-side comparison table of accuracy, confidence, prediction counts for A/B testing insights
10. Refresh data button: manually trigger recalculation of metrics from `ai_predictions` and `transactions` tables, shows last updated timestamp

### Story 6.7: System Integration Settings & API Keys

As a user,
I want to configure integrations with external services (UpBank sync, accounting software),
so that I can control data sync behavior and API connections.

#### Acceptance Criteria

1. Integrations page created at `/app/settings/integrations` with cards for each integration: UpBank, Xero, MYOB, Email Service
2. UpBank integration card displays: Status (Connected/Disconnected), Last Sync Time, Sync Frequency (dropdown: Hourly, Daily, Manual), "Sync Now" button
3. UpBank sync configuration: checkbox to enable/disable auto-sync, account mapping (map UpBank accounts to entities), transaction import rules (min amount, categories to exclude)
4. "Disconnect UpBank" button removes API credentials from Supabase, disables auto-sync, shows confirmation dialog "Future transactions will not sync"
5. Xero/MYOB integration cards (future): "Connect" button initiates OAuth flow, stores access tokens securely in Supabase encrypted columns, shows connected account name
6. API key management section: masked display of API keys (e.g., "sk_test_***************"), "Regenerate Key" button with confirmation, "Copy" button for clipboard
7. Email service settings: SMTP configuration fields (server, port, username, password, from address) for invoice sending, "Test Email" button sends test message
8. Webhook configuration: input field for webhook URL to receive real-time notifications on transaction creation, invoice status change, anomaly detection
9. Integration logs viewer: table showing recent sync attempts (timestamp, status: success/failed, records processed, error message if failed), last 50 entries
10. Error alerting: if integration fails (e.g., UpBank sync error), display banner notification in integrations page and send email to admin user with error details

---

## Checklist Results Report

[To be completed after full PRD review using pm-checklist]

## Next Steps

### UX Expert Prompt

Review the SAYERS Finance Dashboard PRD (docs/prd.md) and create a comprehensive UX architecture document addressing:

1. Detailed interaction flows for key user journeys: transaction categorization workflow, invoice creation to payment, BAS generation and review
2. Component library specifications based on shadcn/ui with custom financial dashboard components (KPI cards, transaction tables, chart layouts)
3. Responsive design patterns for financial data visualization across desktop, tablet, mobile with specific breakpoints and layout transformations
4. Accessibility implementation guide: keyboard navigation maps, screen reader optimizations for charts/tables, WCAG AA compliance checklist
5. Visual design specifications: color usage for financial indicators (profit/loss, confidence levels, anomaly severity), typography hierarchy for dense financial data, spacing system

Reference Epic 2 (Dashboard), Epic 3 (Transactions), and Epic 4 (Invoices) for primary UX focus areas. Prioritize clarity and efficiency for financial data review workflows.

### Architect Prompt

Review the SAYERS Finance Dashboard PRD (docs/prd.md) and create a comprehensive technical architecture document addressing:

1. Next.js App Router application structure: file organization, routing strategy, server vs client component decisions
2. Supabase integration patterns: RLS policy implementation for multi-entity isolation, query optimization strategies, real-time subscription usage (if applicable)
3. Data fetching and caching strategy: TanStack Query setup, optimistic updates patterns, server-side data fetching in Server Components
4. State management architecture: React Context for global state (entity selection, user preferences), form state with React Hook Form
5. PDF generation implementation: comparison of `@react-pdf/renderer` vs `puppeteer` approaches, performance considerations for batch operations
6. Testing strategy: unit test setup (Vitest), component tests (React Testing Library), E2E critical paths (Playwright), financial calculation test coverage
7. Build and deployment configuration: Vercel deployment settings, environment variable management, CI/CD pipeline recommendations
8. Security implementation: authentication flow, RLS enforcement patterns, input validation strategies, audit logging implementation
9. Performance optimization: bundle size management, code splitting strategy, chart rendering optimization, virtual scrolling for large lists
10. Database schema review: validate existing Supabase schema supports all PRD requirements, identify any missing tables/columns, index recommendations

Reference Technical Assumptions section and all Epic acceptance criteria for detailed requirements. Prioritize financial calculation accuracy, security (RLS), and performance (large datasets).
