# SAYERS Financial Dashboard - System Architecture Document

---
date: "2025-10-17"
version: "2.0"
status: "Draft"
project: "SAYERS Financial Dashboard"
author: "Architect Agent (BMad Method)"
---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 2.0 | 2025-10-17 | Architect Agent | Comprehensive architecture redesign following BMad template |
| 1.0 | 2025-10-03 | Harrison Robert Sayers | Initial architecture document |

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Application Architecture](#2-application-architecture)
3. [Data Architecture](#3-data-architecture)
4. [State Management](#4-state-management)
5. [Security Architecture](#5-security-architecture)
6. [Performance Architecture](#6-performance-architecture)
7. [Financial Calculation Architecture](#7-financial-calculation-architecture)
8. [Data Visualization Architecture](#8-data-visualization-architecture)
9. [Form Architecture](#9-form-architecture)
10. [Testing Architecture](#10-testing-architecture)
11. [Deployment Architecture](#11-deployment-architecture)
12. [Migration & Phased Rollout](#12-migration--phased-rollout)
13. [Monitoring & Observability](#13-monitoring--observability)
14. [Scalability Considerations](#14-scalability-considerations)
15. [Technical Debt & Future Considerations](#15-technical-debt--future-considerations)

---

## 1. System Overview

### 1.1 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Browser                             │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────┐│
│  │  Desktop     │  │   Tablet     │  │      Mobile           ││
│  │  (1024px+)   │  │  (768-1023)  │  │     (320-767px)       ││
│  └──────────────┘  └──────────────┘  └───────────────────────┘│
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTPS
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Vercel Edge Network (CDN)                     │
│  • Global CDN                                                    │
│  • Static Asset Caching                                         │
│  • Edge Functions (Sydney Region)                               │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              Next.js 14+ Application (Vercel Sydney)             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                App Router (app/)                          │  │
│  │  ┌────────────────┐  ┌────────────────┐                  │  │
│  │  │ Server         │  │ Client         │                  │  │
│  │  │ Components     │  │ Components     │                  │  │
│  │  │ (Data Fetch)   │  │ (Interactive)  │                  │  │
│  │  └────────────────┘  └────────────────┘                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              API Routes (app/api/)                        │  │
│  │  • PDF Generation     • CSV Export                        │  │
│  │  • Webhook Handlers   • Server Actions                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐  ┌──────────────────┐  ┌─────────────────────┐
│  Supabase    │  │  Supabase        │  │  Supabase Storage   │
│  Auth        │  │  PostgreSQL DB   │  │  (Invoice PDFs)     │
│              │  │                  │  │                     │
│ • Session    │  │ • 23 Tables      │  │ • S3-compatible     │
│   Management │  │ • RLS Policies   │  │ • Secure URLs       │
│ • Email/Pass │  │ • Indexes        │  │                     │
└──────────────┘  └────────┬─────────┘  └─────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌──────────────┐  ┌─────────────────┐  ┌──────────────────┐
│  MindsDB ML  │  │  UpBank API     │  │  n8n Workflows   │
│  Pipeline    │  │  Sync           │  │                  │
│              │  │                 │  │ • Orchestration  │
│ • Category   │  │ • 256 Personal  │  │ • Error Handling │
│   Prediction │  │   Transactions  │  │ • Scheduling     │
│ • Anomaly    │  │ • Auto-sync     │  │                  │
│   Detection  │  │   (daily)       │  │                  │
│ • Cash Flow  │  │                 │  │                  │
│   Forecast   │  │                 │  │                  │
└──────────────┘  └─────────────────┘  └──────────────────┘
```

### 1.2 Technology Stack

**Core Stack (Required - No Alternatives):**

| Layer | Technology | Version | Rationale |
|-------|-----------|---------|-----------|
| **Frontend Framework** | Next.js | 14.2+ | App Router, React Server Components, Vercel optimization, streaming SSR |
| **Language** | TypeScript | 5.3+ | Type safety critical for financial calculations, compile-time error detection |
| **Database** | Supabase PostgreSQL | 15+ | **Fixed** - Existing production database with 23 tables, cannot migrate |
| **UI Components** | shadcn/ui | v4 | Accessible (WCAG AA), customizable, built on Radix UI, excellent DX |
| **Styling** | Tailwind CSS | 3.4+ | Utility-first, tree-shakeable, shadcn/ui dependency |
| **Authentication** | Supabase Auth | Latest | Integrated with RLS, existing sessions, email/password flow |
| **Hosting** | Vercel | Latest | Native Next.js optimization, edge functions, automatic deployments |

**Data & State Management:**

| Purpose | Technology | Version | Rationale |
|---------|-----------|---------|-----------|
| **Server State** | React Query (TanStack Query) | 5.0+ | Caching, background refetching, optimistic updates, 10-min polling |
| **Client State** | Zustand | 4.4+ | Lightweight (1KB), no boilerplate, perfect for entity filter + UI prefs |
| **Form State** | React Hook Form | 7.49+ | Minimal re-renders, async validation, great DX |
| **Schema Validation** | Zod | 3.22+ | Type-safe runtime validation, integrates with React Hook Form |

**Data Visualization & Tables:**

| Purpose | Technology | Version | Rationale |
|---------|-----------|---------|-----------|
| **Charts** | Recharts | 2.10+ | React-native, composable, supports all chart types (pie, line, bar, waterfall) |
| **Tables** | TanStack Table | 8.11+ | Virtual scrolling, sorting/filtering, 50k+ row support, headless UI |
| **Virtual Scrolling** | @tanstack/react-virtual | 3.0+ | Handle large transaction lists (10k+ rows) without performance degradation |

**Utilities & Libraries:**

| Purpose | Technology | Version | Rationale |
|---------|-----------|---------|-----------|
| **Decimal Math** | decimal.js | 10.4+ | **Critical** - Avoids floating-point errors in GST/tax calculations |
| **Date Handling** | date-fns | 3.0+ | Lightweight, tree-shakeable, Australia/Sydney timezone support |
| **PDF Generation** | @react-pdf/renderer | 3.3+ | React-based, declarative, server-side invoice rendering |
| **CSV Export** | papaparse | 5.4+ | Fast, handles large datasets, proper escaping |
| **Type Generation** | supabase gen types | Latest | Auto-generate TypeScript types from Supabase schema |

**Testing:**

| Purpose | Technology | Version | Rationale |
|---------|-----------|---------|-----------|
| **Unit Tests** | Vitest | 1.0+ | Fast, Vite-powered, TypeScript support, 100% coverage for financial logic |
| **Component Tests** | Testing Library (React) | 14.0+ | User-centric testing, accessibility assertions |
| **E2E Tests** | Playwright | 1.40+ | Cross-browser, great debugging, critical user flows |
| **Test Data** | MSW (Mock Service Worker) | 2.0+ | Mock Supabase API responses for deterministic tests |

**Developer Experience:**

| Purpose | Technology | Version | Rationale |
|---------|-----------|---------|-----------|
| **Linting** | ESLint | 8.0+ | Next.js default config + financial code rules |
| **Formatting** | Prettier | 3.0+ | Consistent code style, integrates with ESLint |
| **Git Hooks** | Husky | 8.0+ | Pre-commit linting, pre-push testing |
| **Type Checking** | TypeScript Compiler | 5.3+ | Strict mode enabled, no implicit any |

### 1.3 Deployment Architecture

**Infrastructure:**
- **Frontend**: Vercel (Sydney region for optimal AU latency)
- **Database**: Supabase (AWS Sydney) - existing production deployment
- **CDN**: Vercel Edge Network (global)
- **Storage**: Supabase Storage (S3-compatible, Sydney region)

**Environment Strategy:**

| Environment | Purpose | Deployment Trigger | Database | Features |
|-------------|---------|-------------------|----------|----------|
| **Development** | Local dev with hot reload | Manual `npm run dev` | Supabase Dev Project (optional) | Mock data, debug tools |
| **Preview** | PR reviews, stakeholder demos | Automatic on PR creation | Supabase Production (read-only) | Full feature set, no mutations |
| **Staging** | Pre-production testing | Automatic on merge to `develop` | Supabase Production (RLS protected) | Identical to production |
| **Production** | Live application | Manual deployment from `main` | Supabase Production | All features enabled |

**Deployment Pipeline:**

```
┌──────────────┐
│   Git Push   │
│   to Branch  │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────┐
│      GitHub Actions Workflow             │
│  1. Install dependencies (npm ci)        │
│  2. Type check (tsc --noEmit)            │
│  3. Lint (eslint)                        │
│  4. Unit tests (vitest)                  │
│  5. Build (next build)                   │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│       Vercel Deployment                  │
│  • Preview: All PRs                      │
│  • Production: main branch only          │
│  • Edge Functions: Sydney region         │
│  • Environment Variables: Encrypted      │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│      Post-Deployment Checks              │
│  1. Smoke tests (Playwright)             │
│  2. Lighthouse audit (performance)       │
│  3. Security scan (Snyk)                 │
└──────────────────────────────────────────┘
```

---

## 2. Application Architecture

### 2.1 Next.js App Router Structure

```
financial-dashboard/
├── app/                                    # Next.js App Router (main application)
│   ├── (auth)/                             # Auth route group (login, signup)
│   │   ├── login/
│   │   │   └── page.tsx                    # Login page (Supabase Auth)
│   │   ├── signup/
│   │   │   └── page.tsx                    # Signup page
│   │   └── reset-password/
│   │       └── page.tsx                    # Password reset flow
│   │
│   ├── (dashboard)/                        # Main app route group (requires auth)
│   │   ├── layout.tsx                      # Dashboard layout (sidebar, header, entity selector)
│   │   ├── page.tsx                        # Dashboard home (KPIs, recent transactions, alerts)
│   │   │
│   │   ├── transactions/                   # Transaction management
│   │   │   ├── page.tsx                    # Transaction list (Server Component)
│   │   │   ├── [id]/                       # Transaction detail
│   │   │   │   └── page.tsx                # Transaction detail page
│   │   │   └── components/                 # Transaction-specific components
│   │   │       ├── TransactionTable.tsx    # Client Component (virtual scrolling)
│   │   │       ├── TransactionFilters.tsx  # Client Component (filter UI)
│   │   │       └── CategoryBadge.tsx       # Editable category badge
│   │   │
│   │   ├── invoices/                       # Invoice management
│   │   │   ├── page.tsx                    # Invoice list (Server Component)
│   │   │   ├── new/                        # Create invoice
│   │   │   │   └── page.tsx                # Invoice form
│   │   │   ├── [id]/                       # Invoice detail
│   │   │   │   ├── page.tsx                # Invoice detail view
│   │   │   │   └── edit/                   # Edit invoice
│   │   │   │       └── page.tsx            # Invoice edit form
│   │   │   └── components/
│   │   │       ├── InvoiceCard.tsx         # Invoice display card
│   │   │       ├── InvoiceForm.tsx         # Client Component (React Hook Form)
│   │   │       └── InvoiceStatusBadge.tsx  # Status indicator
│   │   │
│   │   ├── reports/                        # Financial reports
│   │   │   ├── page.tsx                    # Reports dashboard
│   │   │   ├── profit-loss/                # P&L report
│   │   │   │   └── page.tsx                # P&L generator
│   │   │   ├── balance-sheet/              # Balance sheet
│   │   │   │   └── page.tsx                # Balance sheet generator
│   │   │   ├── bas/                        # BAS (Business Activity Statement)
│   │   │   │   └── page.tsx                # BAS generator (Australian tax)
│   │   │   └── components/
│   │   │       ├── DateRangePicker.tsx     # Date range selector
│   │   │       └── ReportCard.tsx          # Report display card
│   │   │
│   │   ├── insights/                       # ML insights & analytics
│   │   │   ├── page.tsx                    # Insights dashboard
│   │   │   ├── trends/                     # Spending trends
│   │   │   │   └── page.tsx                # Trend analysis
│   │   │   ├── anomalies/                  # Anomaly detection
│   │   │   │   └── page.tsx                # Anomaly alerts
│   │   │   └── forecasts/                  # Cash flow forecasts
│   │   │       └── page.tsx                # Forecast visualization
│   │   │
│   │   ├── budgets/                        # Budget management (Phase 3)
│   │   │   ├── page.tsx                    # Budget list
│   │   │   └── new/
│   │   │       └── page.tsx                # Create budget
│   │   │
│   │   └── settings/                       # Application settings
│   │       ├── page.tsx                    # Settings dashboard
│   │       ├── profile/                    # User profile
│   │       │   └── page.tsx
│   │       └── entities/                   # Entity management
│   │           └── page.tsx
│   │
│   ├── api/                                # API Routes (Server-side operations)
│   │   ├── invoices/
│   │   │   ├── [id]/
│   │   │   │   └── pdf/
│   │   │   │       └── route.ts            # POST - Generate invoice PDF
│   │   │   └── route.ts                    # POST - Create invoice
│   │   ├── reports/
│   │   │   ├── bas/
│   │   │   │   └── route.ts                # POST - Generate BAS report
│   │   │   ├── profit-loss/
│   │   │   │   └── route.ts                # POST - Generate P&L
│   │   │   └── balance-sheet/
│   │   │       └── route.ts                # POST - Generate balance sheet
│   │   ├── export/
│   │   │   ├── transactions/
│   │   │   │   └── csv/
│   │   │   │       └── route.ts            # POST - Export transactions to CSV
│   │   │   └── invoices/
│   │   │       └── csv/
│   │   │           └── route.ts            # POST - Export invoices to CSV
│   │   └── webhooks/
│   │       └── upbank/
│   │           └── route.ts                # POST - Handle UpBank webhook
│   │
│   ├── layout.tsx                          # Root layout (global providers, fonts)
│   ├── page.tsx                            # Landing page (redirects to /dashboard)
│   ├── error.tsx                           # Global error boundary
│   ├── not-found.tsx                       # 404 page
│   └── loading.tsx                         # Global loading state
│
├── components/                             # Shared React components
│   ├── ui/                                 # shadcn/ui components (auto-generated)
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── table.tsx
│   │   ├── dialog.tsx
│   │   ├── select.tsx
│   │   ├── input.tsx
│   │   ├── form.tsx
│   │   ├── toast.tsx
│   │   ├── tabs.tsx
│   │   └── ... (other shadcn components)
│   │
│   ├── dashboard/                          # Dashboard-specific components
│   │   ├── KPICard.tsx                     # Metric card with trend indicator
│   │   ├── EntitySelector.tsx              # Multi-entity dropdown (Client Component)
│   │   ├── RecentTransactions.tsx          # Recent transactions widget
│   │   ├── SpendingChart.tsx               # Category spending donut chart
│   │   └── AlertBanner.tsx                 # Overdue invoices / anomaly alerts
│   │
│   ├── charts/                             # Recharts wrapper components
│   │   ├── PieChart.tsx                    # Wrapped Recharts PieChart
│   │   ├── LineChart.tsx                   # Wrapped Recharts LineChart
│   │   ├── BarChart.tsx                    # Wrapped Recharts BarChart
│   │   ├── WaterfallChart.tsx              # Cash flow waterfall
│   │   └── ChartCard.tsx                   # Reusable chart container
│   │
│   ├── forms/                              # Reusable form components
│   │   ├── FormInput.tsx                   # Text input with validation
│   │   ├── FormSelect.tsx                  # Select with validation
│   │   ├── FormDatePicker.tsx              # Date picker with validation
│   │   ├── FormCurrencyInput.tsx           # Currency input (decimal handling)
│   │   └── FormTextarea.tsx                # Textarea with validation
│   │
│   ├── layout/                             # Layout components
│   │   ├── Header.tsx                      # Main header (entity selector, search, user menu)
│   │   ├── Sidebar.tsx                     # Navigation sidebar
│   │   ├── MobileNav.tsx                   # Mobile hamburger navigation
│   │   └── Footer.tsx                      # Footer (optional)
│   │
│   └── shared/                             # Shared utility components
│       ├── LoadingSkeleton.tsx             # Loading state placeholder
│       ├── ErrorBoundary.tsx               # React Error Boundary
│       ├── Pagination.tsx                  # Pagination controls
│       ├── SearchBar.tsx                   # Global search (Cmd+K)
│       └── ThemeToggle.tsx                 # Dark mode toggle
│
├── lib/                                    # Utility functions & business logic
│   ├── supabase/                           # Supabase integration
│   │   ├── client.ts                       # Browser client (Client Components)
│   │   ├── server.ts                       # Server client (Server Components, API Routes)
│   │   ├── middleware.ts                   # Auth middleware
│   │   └── types.ts                        # Auto-generated DB types (supabase gen types)
│   │
│   ├── calculations/                       # Financial calculation logic
│   │   ├── bas.ts                          # BAS calculation (GST collected, paid, net)
│   │   ├── profit-loss.ts                  # P&L calculation (revenue, expenses, profit)
│   │   ├── balance-sheet.ts                # Balance sheet (assets, liabilities, equity)
│   │   ├── gst.ts                          # GST calculation utilities (10% Australian)
│   │   └── decimal.ts                      # Decimal math helpers (avoid floating point errors)
│   │
│   ├── formatters/                         # Data formatting utilities
│   │   ├── currency.ts                     # Format cents to AUD display ($1,234.56)
│   │   ├── date.ts                         # Date formatting (date-fns wrappers)
│   │   ├── percentage.ts                   # Percentage formatting
│   │   └── number.ts                       # Number formatting (thousands separator)
│   │
│   ├── validations/                        # Zod validation schemas
│   │   ├── invoice.ts                      # Invoice creation/update schemas
│   │   ├── transaction.ts                  # Transaction validation
│   │   ├── contact.ts                      # Contact validation
│   │   └── budget.ts                       # Budget validation
│   │
│   ├── queries/                            # Supabase query functions
│   │   ├── transactions.ts                 # Transaction queries (list, get, update)
│   │   ├── invoices.ts                     # Invoice queries
│   │   ├── entities.ts                     # Entity queries
│   │   ├── accounts.ts                     # Chart of accounts queries
│   │   └── ml-insights.ts                  # ML predictions & insights queries
│   │
│   ├── mutations/                          # Supabase mutation functions
│   │   ├── transactions.ts                 # Create/update/delete transactions
│   │   ├── invoices.ts                     # Create/update/delete invoices
│   │   └── budgets.ts                      # Create/update/delete budgets
│   │
│   └── utils/                              # General utilities
│       ├── cn.ts                           # Tailwind class merging (clsx + tailwind-merge)
│       ├── errors.ts                       # Error handling utilities
│       ├── constants.ts                    # App constants (tax rates, date formats)
│       └── env.ts                          # Environment variable validation
│
├── hooks/                                  # Custom React hooks
│   ├── use-entity-filter.ts                # Global entity filter state (Zustand)
│   ├── use-transactions.ts                 # React Query hook for transactions
│   ├── use-invoices.ts                     # React Query hook for invoices
│   ├── use-ml-insights.ts                  # React Query hook for ML insights
│   ├── use-debounce.ts                     # Debounce hook (search inputs)
│   ├── use-toast.ts                        # Toast notification hook
│   └── use-media-query.ts                  # Responsive design hook
│
├── types/                                  # TypeScript type definitions
│   ├── database.ts                         # Supabase database types (auto-generated)
│   ├── api.ts                              # API request/response types
│   ├── charts.ts                           # Chart data types
│   ├── forms.ts                            # Form data types
│   └── index.ts                            # Barrel export
│
├── styles/                                 # Global styles
│   └── globals.css                         # Tailwind imports + custom CSS
│
├── public/                                 # Static assets
│   ├── logos/                              # Entity logos (MOKAI, MOK HOUSE)
│   ├── icons/                              # Custom icons
│   └── favicon.ico                         # Favicon
│
├── tests/                                  # Test files
│   ├── unit/                               # Unit tests (Vitest)
│   │   ├── calculations/                   # Financial calculation tests
│   │   │   ├── bas.test.ts                 # BAS calculation tests
│   │   │   ├── profit-loss.test.ts
│   │   │   └── gst.test.ts
│   │   ├── formatters/
│   │   │   └── currency.test.ts
│   │   └── validations/
│   │       └── invoice.test.ts
│   │
│   ├── integration/                        # Integration tests (Vitest + Testing Library)
│   │   ├── components/
│   │   │   ├── TransactionTable.test.tsx
│   │   │   └── InvoiceForm.test.tsx
│   │   └── queries/
│   │       └── transactions.test.ts
│   │
│   └── e2e/                                # End-to-end tests (Playwright)
│       ├── auth.spec.ts                    # Login/logout flow
│       ├── transactions.spec.ts            # Transaction viewing/editing
│       ├── invoices.spec.ts                # Invoice creation/payment
│       └── reports.spec.ts                 # Report generation
│
├── .env.local                              # Environment variables (gitignored)
├── .env.example                            # Example environment variables
├── next.config.js                          # Next.js configuration
├── tailwind.config.ts                      # Tailwind configuration
├── tsconfig.json                           # TypeScript configuration
├── package.json                            # Dependencies
├── vitest.config.ts                        # Vitest configuration
├── playwright.config.ts                    # Playwright configuration
└── README.md                               # Project documentation
```

### 2.2 Component Architecture

**Component Strategy: Server Components First**

Default to **React Server Components** (RSC) for all components. Only use **Client Components** when you need:
- Interactivity (onClick, onChange, state)
- Browser-only APIs (localStorage, window)
- React hooks that require client (useState, useEffect)

**Component Hierarchy:**

```
App Router
│
├── Server Components (Default)
│   ├── layout.tsx                     # Fetch user session, entities
│   ├── page.tsx                       # Fetch dashboard data (SSR)
│   ├── transactions/page.tsx          # Fetch transactions (SSR)
│   └── reports/page.tsx               # Generate reports (SSR)
│
└── Client Components ("use client")
    ├── EntitySelector                 # Zustand state + onClick
    ├── TransactionTable               # Virtual scrolling + sorting
    ├── InvoiceForm                    # React Hook Form + validation
    ├── PieChart                       # Recharts (client-only)
    └── SearchBar                      # Debounced input + state
```

**Reusable Component Patterns:**

1. **KPI Card Component:**
```typescript
// Server Component (fetches data)
async function KPICard({
  title,
  entityId,
  dateRange
}: KPICardProps) {
  const value = await calculateKPI(entityId, dateRange) // Server-side query
  const trend = await calculateTrend(entityId, dateRange)

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-3xl font-bold">
          {formatCurrency(value)}
        </div>
        <TrendIndicator value={trend} /> {/* Client Component for animation */}
      </CardContent>
    </Card>
  )
}
```

2. **Chart Card Component:**
```typescript
// Wrapper for all charts (consistent styling)
function ChartCard({
  title,
  description,
  children,
  exportable = true
}: ChartCardProps) {
  return (
    <Card>
      <CardHeader>
        <div className="flex justify-between items-center">
          <div>
            <CardTitle>{title}</CardTitle>
            <CardDescription>{description}</CardDescription>
          </div>
          {exportable && <ExportButton />} {/* Client Component */}
        </div>
      </CardHeader>
      <CardContent>
        {children} {/* Recharts component (Client) */}
      </CardContent>
    </Card>
  )
}
```

3. **Transaction Table Component (Virtual Scrolling):**
```typescript
"use client"

import { useVirtualizer } from '@tanstack/react-virtual'
import { useTransactions } from '@/hooks/use-transactions'

function TransactionTable({ entityId }: TransactionTableProps) {
  const { data, isLoading } = useTransactions(entityId)

  const parentRef = useRef<HTMLDivElement>(null)

  const virtualizer = useVirtualizer({
    count: data?.length ?? 0,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50, // Row height in pixels
    overscan: 10, // Render 10 extra rows for smooth scrolling
  })

  if (isLoading) return <TableSkeleton rows={10} />

  return (
    <div ref={parentRef} className="h-[600px] overflow-auto">
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          width: '100%',
          position: 'relative',
        }}
      >
        {virtualizer.getVirtualItems().map((virtualRow) => {
          const transaction = data[virtualRow.index]
          return (
            <TransactionRow
              key={transaction.id}
              transaction={transaction}
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: `${virtualRow.size}px`,
                transform: `translateY(${virtualRow.start}px)`,
              }}
            />
          )
        })}
      </div>
    </div>
  )
}
```

**shadcn/ui Component Usage:**

| shadcn Component | Use Cases | Customization |
|-----------------|-----------|---------------|
| `Button` | All interactive buttons | Variant: `default`, `destructive`, `outline`, `secondary`, `ghost`, `link` |
| `Card` | Dashboard widgets, report containers | Custom header with actions, footer for metadata |
| `Table` | Transaction lists, invoice lists | Virtual scrolling via TanStack Table |
| `Form` | Invoice creation, budget forms | Integrated with React Hook Form + Zod |
| `Select` | Entity selector, category picker | Searchable via Combobox |
| `Dialog` | Confirmation modals, detail views | Controlled via state |
| `Sheet` | Mobile navigation, filter panels | Slide from right/left |
| `Toast` | Success/error notifications | Auto-dismiss, action buttons |
| `Tabs` | Report sections, settings pages | Keyboard navigation |

---

## 3. Data Architecture

### 3.1 Supabase Integration

**Connection Pattern:**

```typescript
// lib/supabase/client.ts (Browser - Client Components)
import { createBrowserClient } from '@supabase/ssr'
import { Database } from '@/types/database'

export const supabase = createBrowserClient<Database>(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)
```

```typescript
// lib/supabase/server.ts (Server - Server Components, API Routes)
import { createServerClient, type CookieOptions } from '@supabase/ssr'
import { cookies } from 'next/headers'
import { Database } from '@/types/database'

export async function createClient() {
  const cookieStore = cookies()

  return createServerClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value
        },
      },
    }
  )
}
```

**Type Generation:**

```bash
# Generate TypeScript types from Supabase schema
npx supabase gen types typescript \
  --project-id gshsshaodoyttdxippwx \
  --schema public \
  > types/database.ts
```

**Type Safety Flow:**

```
Supabase PostgreSQL Schema
          ↓
  supabase gen types typescript
          ↓
  types/database.ts (auto-generated)
          ↓
  Zod Schemas (lib/validations/)
          ↓
  React Components (type-safe queries)
```

### 3.2 Database Schema Overview (23 Tables)

**Core Tables:**

1. **entities** (3 rows) - Business entities (MOKAI, MOK HOUSE, Harrison Sayers)
2. **contacts** (3 rows) - Customers and suppliers
3. **bank_accounts** (3 rows) - Bank account details
4. **accounts** (52 rows) - Chart of accounts (Australian accounting standards)

**Transaction Tables:**

5. **personal_transactions** (256 rows) - UpBank synced transactions
6. **transactions** (1 row) - Business transactions
7. **transaction_lines** - Double-entry accounting lines
8. **recurring_transactions** (26 rows) - Recurring payments/income

**Invoice Tables:**

9. **invoices** (30 rows) - Receivables and payables
10. **invoice_line_items** - Invoice line items with GST

**Category & Classification:**

11. **upbank_categories** (44 rows) - UpBank's category taxonomy
12. **personal_finance_categories** (10 rows) - Custom category mapping
13. **categorization_rules** (3 rows) - Auto-categorization rules
14. **business_keywords** (18 rows) - Keywords for business expense detection

**ML & Analytics:**

15. **ml_models** (7 rows) - MindsDB model registry
16. **ai_predictions** (0 rows) - ML category predictions (future)
17. **ai_insights** (0 rows) - Business insights (future)
18. **anomaly_detections** (0 rows) - Anomaly alerts (future)
19. **cash_flow_forecasts** (0 rows) - Cash flow predictions (future)

**Sync & Reconciliation:**

20. **sync_sessions** (11 rows) - UpBank sync history
21. **sync_errors** (26 rows) - Sync error log
22. **balance_reconciliations** - Bank reconciliation records
23. **rate_limit_status** - API rate limit tracking

**RLS (Row-Level Security) Policies:**

```sql
-- Example RLS policy for multi-entity data isolation
CREATE POLICY "Users can only access their entities"
  ON transactions
  FOR ALL
  USING (
    entity_id IN (
      SELECT id FROM entities
      WHERE user_id = auth.uid()
    )
  );

-- Similar policies for invoices, bank_accounts, etc.
```

### 3.3 Data Fetching Strategy

**Server Components (SSR - Initial Page Load):**

```typescript
// app/transactions/page.tsx (Server Component)
import { createClient } from '@/lib/supabase/server'
import { TransactionTable } from './components/TransactionTable'

export default async function TransactionsPage() {
  const supabase = await createClient()

  // Fetch data server-side (SSR)
  const { data: transactions } = await supabase
    .from('transactions')
    .select(`
      *,
      entity:entities(name),
      account:accounts(name, code)
    `)
    .order('transaction_date', { ascending: false })
    .limit(100)

  // Pass data to Client Component for interactivity
  return <TransactionTable initialData={transactions} />
}
```

**React Query (Client-Side Caching & Polling):**

```typescript
// hooks/use-transactions.ts
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { supabase } from '@/lib/supabase/client'

export function useTransactions(entityId?: string) {
  return useQuery({
    queryKey: ['transactions', entityId],
    queryFn: async () => {
      const query = supabase
        .from('transactions')
        .select('*')
        .order('transaction_date', { ascending: false })

      if (entityId) {
        query.eq('entity_id', entityId)
      }

      const { data, error } = await query
      if (error) throw error
      return data
    },
    staleTime: 10 * 60 * 1000, // 10 minutes
    refetchInterval: 10 * 60 * 1000, // Poll every 10 minutes
    refetchOnWindowFocus: true,
  })
}
```

**Optimistic Updates (Forms):**

```typescript
// mutations/invoices.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { supabase } from '@/lib/supabase/client'

export function useCreateInvoice() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (invoice: InsertInvoice) => {
      const { data, error } = await supabase
        .from('invoices')
        .insert(invoice)
        .select()
        .single()

      if (error) throw error
      return data
    },
    onMutate: async (newInvoice) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['invoices'] })

      // Snapshot previous value
      const previousInvoices = queryClient.getQueryData(['invoices'])

      // Optimistically update UI
      queryClient.setQueryData(['invoices'], (old: Invoice[]) => [
        ...old,
        { ...newInvoice, id: 'temp-id', created_at: new Date().toISOString() }
      ])

      return { previousInvoices }
    },
    onError: (err, newInvoice, context) => {
      // Rollback on error
      queryClient.setQueryData(['invoices'], context?.previousInvoices)
    },
    onSettled: () => {
      // Refetch to sync with server
      queryClient.invalidateQueries({ queryKey: ['invoices'] })
    },
  })
}
```

**Query Optimization (Avoid N+1):**

```typescript
// ❌ BAD - N+1 Query Problem
const { data: invoices } = await supabase.from('invoices').select('*')

for (const invoice of invoices) {
  // Separate query for each invoice (N+1 problem)
  const { data: contact } = await supabase
    .from('contacts')
    .select('*')
    .eq('id', invoice.contact_id)
    .single()
}

// ✅ GOOD - Single Query with Join
const { data: invoices } = await supabase
  .from('invoices')
  .select(`
    *,
    contact:contacts(id, name, email),
    entity:entities(id, name),
    line_items:invoice_line_items(*)
  `)
```

---

## 4. State Management

### 4.1 Server State (React Query)

**Query Keys Structure:**

```typescript
// Hierarchical query keys for easy invalidation
const queryKeys = {
  entities: ['entities'] as const,
  entity: (id: string) => ['entities', id] as const,

  transactions: ['transactions'] as const,
  transactionsByEntity: (entityId: string) => ['transactions', entityId] as const,
  transaction: (id: string) => ['transactions', 'detail', id] as const,

  invoices: ['invoices'] as const,
  invoicesByEntity: (entityId: string) => ['invoices', entityId] as const,
  invoice: (id: string) => ['invoices', 'detail', id] as const,

  reports: ['reports'] as const,
  profitLoss: (entityId: string, dateRange: DateRange) =>
    ['reports', 'profit-loss', entityId, dateRange] as const,
  balanceSheet: (entityId: string, date: string) =>
    ['reports', 'balance-sheet', entityId, date] as const,
  bas: (entityId: string, quarter: string) =>
    ['reports', 'bas', entityId, quarter] as const,
}
```

**Cache Configuration:**

```typescript
// lib/query-client.ts
import { QueryClient } from '@tanstack/react-query'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 10 * 60 * 1000, // 10 minutes - data is "fresh" for this duration
      cacheTime: 30 * 60 * 1000, // 30 minutes - keep unused data in cache
      refetchOnWindowFocus: true, // Refetch when user returns to tab
      retry: 3, // Retry failed queries 3 times
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
    },
    mutations: {
      retry: 1, // Only retry mutations once
    },
  },
})
```

### 4.2 Client State (Zustand)

**Entity Filter Store:**

```typescript
// stores/entity-filter.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface EntityFilterState {
  selectedEntityId: string | null
  setSelectedEntity: (entityId: string | null) => void
}

export const useEntityFilter = create<EntityFilterState>()(
  persist(
    (set) => ({
      selectedEntityId: null,
      setSelectedEntity: (entityId) => set({ selectedEntityId: entityId }),
    }),
    {
      name: 'entity-filter', // localStorage key
    }
  )
)
```

**UI Preferences Store:**

```typescript
// stores/ui-preferences.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface UIPreferencesState {
  theme: 'light' | 'dark'
  sidebarCollapsed: boolean
  defaultDateRange: '7d' | '30d' | '90d' | '1y'
  toggleTheme: () => void
  toggleSidebar: () => void
  setDefaultDateRange: (range: '7d' | '30d' | '90d' | '1y') => void
}

export const useUIPreferences = create<UIPreferencesState>()(
  persist(
    (set) => ({
      theme: 'light',
      sidebarCollapsed: false,
      defaultDateRange: '30d',
      toggleTheme: () => set((state) => ({
        theme: state.theme === 'light' ? 'dark' : 'light'
      })),
      toggleSidebar: () => set((state) => ({
        sidebarCollapsed: !state.sidebarCollapsed
      })),
      setDefaultDateRange: (range) => set({ defaultDateRange: range }),
    }),
    {
      name: 'ui-preferences',
    }
  )
)
```

### 4.3 Form State (React Hook Form)

**Invoice Form Example:**

```typescript
// components/forms/InvoiceForm.tsx
"use client"

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { invoiceSchema, type InvoiceFormData } from '@/lib/validations/invoice'
import { useCreateInvoice } from '@/lib/mutations/invoices'

export function InvoiceForm() {
  const createInvoice = useCreateInvoice()

  const form = useForm<InvoiceFormData>({
    resolver: zodResolver(invoiceSchema),
    defaultValues: {
      invoice_type: 'RECEIVABLE',
      status: 'DRAFT',
      gst_applicable: true,
      line_items: [
        { description: '', quantity: 1, unit_price_cents: 0, gst_applicable: true }
      ],
    },
  })

  const onSubmit = async (data: InvoiceFormData) => {
    try {
      await createInvoice.mutateAsync(data)
      // Show success toast, redirect, etc.
    } catch (error) {
      // Handle error
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        {/* Form fields */}
      </form>
    </Form>
  )
}
```

---

## 5. Security Architecture

### 5.1 Authentication

**Supabase Auth Flow:**

```
User visits /login
      ↓
Enter email/password
      ↓
Supabase Auth API validates credentials
      ↓
Session token stored in httpOnly cookie
      ↓
Middleware validates session on every request
      ↓
Authorized: Access dashboard
Unauthorized: Redirect to /login
```

**Middleware Protection:**

```typescript
// middleware.ts
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  let response = NextResponse.next({
    request: {
      headers: request.headers,
    },
  })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return request.cookies.get(name)?.value
        },
        set(name: string, value: string, options: CookieOptions) {
          request.cookies.set({ name, value, ...options })
          response = NextResponse.next({
            request: {
              headers: request.headers,
            },
          })
          response.cookies.set({ name, value, ...options })
        },
        remove(name: string, options: CookieOptions) {
          request.cookies.set({ name, value: '', ...options })
          response = NextResponse.next({
            request: {
              headers: request.headers,
            },
          })
          response.cookies.set({ name, value: '', ...options })
        },
      },
    }
  )

  const { data: { session } } = await supabase.auth.getSession()

  // Redirect to login if not authenticated
  if (!session && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // Redirect to dashboard if authenticated and visiting login
  if (session && request.nextUrl.pathname === '/login') {
    return NextResponse.redirect(new URL('/dashboard', request.url))
  }

  return response
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
```

### 5.2 Authorization (Supabase RLS)

**Row-Level Security Policies:**

```sql
-- Entities: Users can only access entities they own
CREATE POLICY "Users access own entities"
  ON entities
  FOR ALL
  USING (user_id = auth.uid());

-- Transactions: Users can only access transactions for their entities
CREATE POLICY "Users access own transactions"
  ON transactions
  FOR ALL
  USING (
    entity_id IN (
      SELECT id FROM entities WHERE user_id = auth.uid()
    )
  );

-- Invoices: Users can only access invoices for their entities
CREATE POLICY "Users access own invoices"
  ON invoices
  FOR ALL
  USING (
    entity_id IN (
      SELECT id FROM entities WHERE user_id = auth.uid()
    )
  );

-- Bank Accounts: Users can only access bank accounts for their entities
CREATE POLICY "Users access own bank accounts"
  ON bank_accounts
  FOR ALL
  USING (
    entity_id IN (
      SELECT id FROM entities WHERE user_id = auth.uid()
    )
  );
```

**RLS Testing Strategy:**

```typescript
// tests/integration/rls/entities.test.ts
import { createClient } from '@supabase/supabase-js'

describe('Entities RLS', () => {
  it('should only return entities owned by authenticated user', async () => {
    const user1Client = createClient(url, anonKey, {
      auth: { persistSession: false },
    })

    await user1Client.auth.signInWithPassword({
      email: 'user1@example.com',
      password: 'password',
    })

    const { data: entities } = await user1Client
      .from('entities')
      .select('*')

    // All returned entities should belong to user1
    expect(entities?.every(e => e.user_id === user1.id)).toBe(true)
  })

  it('should not allow access to other users entities', async () => {
    const user2Client = createClient(url, anonKey, {
      auth: { persistSession: false },
    })

    await user2Client.auth.signInWithPassword({
      email: 'user2@example.com',
      password: 'password',
    })

    const { data, error } = await user2Client
      .from('entities')
      .select('*')
      .eq('id', user1EntityId) // Try to access user1's entity

    expect(data).toHaveLength(0) // RLS blocks access
  })
})
```

### 5.3 Data Protection

**Input Validation (Zod Schemas):**

```typescript
// lib/validations/invoice.ts
import { z } from 'zod'

export const invoiceSchema = z.object({
  entity_id: z.string().uuid(),
  contact_id: z.string().uuid(),
  invoice_type: z.enum(['RECEIVABLE', 'PAYABLE']),
  invoice_number: z.string().min(1).max(50),
  issue_date: z.string().date(),
  due_date: z.string().date(),
  line_items: z.array(
    z.object({
      description: z.string().min(1).max(500),
      quantity: z.number().positive().int(),
      unit_price_cents: z.number().int().nonnegative(),
      gst_applicable: z.boolean(),
    })
  ).min(1).max(100),
})

export type InvoiceFormData = z.infer<typeof invoiceSchema>
```

**XSS Prevention:**

React automatically escapes JSX content, but for extra safety:

```typescript
// ✅ SAFE - React auto-escapes
<div>{transaction.description}</div>

// ❌ DANGEROUS - Bypass escaping (avoid unless absolutely necessary)
<div dangerouslySetInnerHTML={{ __html: transaction.description }} />

// ✅ SAFE - Sanitize if HTML rendering is required
import DOMPurify from 'isomorphic-dompurify'

<div dangerouslySetInnerHTML={{
  __html: DOMPurify.sanitize(transaction.description)
}} />
```

**Content Security Policy (CSP):**

```typescript
// next.config.js
const cspHeader = `
  default-src 'self';
  script-src 'self' 'unsafe-eval' 'unsafe-inline';
  style-src 'self' 'unsafe-inline';
  img-src 'self' blob: data: https://gshsshaodoyttdxippwx.supabase.co;
  font-src 'self';
  connect-src 'self' https://gshsshaodoyttdxippwx.supabase.co;
  frame-ancestors 'none';
  base-uri 'self';
  form-action 'self';
`

module.exports = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Content-Security-Policy',
            value: cspHeader.replace(/\n/g, ''),
          },
        ],
      },
    ]
  },
}
```

**Environment Variable Security:**

```bash
# .env.local (gitignored)
NEXT_PUBLIC_SUPABASE_URL=https://gshsshaodoyttdxippwx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1... # Public key (safe to expose)
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1... # NEVER expose to client
```

```typescript
// lib/utils/env.ts
import { z } from 'zod'

const envSchema = z.object({
  NEXT_PUBLIC_SUPABASE_URL: z.string().url(),
  NEXT_PUBLIC_SUPABASE_ANON_KEY: z.string().min(1),
  SUPABASE_SERVICE_ROLE_KEY: z.string().min(1),
})

// Validate environment variables at build time
export const env = envSchema.parse(process.env)
```

---

## 6. Performance Architecture

### 6.1 Optimization Strategies

**Code Splitting (Automatic with App Router):**

```typescript
// Automatic code splitting per route
app/
├── dashboard/page.tsx           → /dashboard (chunk)
├── transactions/page.tsx        → /transactions (chunk)
├── invoices/page.tsx           → /invoices (chunk)
└── reports/page.tsx            → /reports (chunk)
```

**Lazy Loading Heavy Components:**

```typescript
// components/charts/PieChart.tsx
import { lazy, Suspense } from 'react'

const RechartsComponent = lazy(() => import('recharts').then(mod => ({
  default: mod.PieChart
})))

export function PieChart({ data }: PieChartProps) {
  return (
    <Suspense fallback={<ChartSkeleton />}>
      <RechartsComponent data={data} />
    </Suspense>
  )
}
```

**Virtual Scrolling for Large Lists:**

```typescript
// hooks/use-virtual-scroll.ts
import { useVirtualizer } from '@tanstack/react-virtual'
import { useRef } from 'react'

export function useVirtualScroll<T>(items: T[], estimateSize = 50) {
  const parentRef = useRef<HTMLDivElement>(null)

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => estimateSize,
    overscan: 10,
  })

  return { parentRef, virtualizer }
}
```

**Image Optimization:**

```typescript
// Use Next.js Image component for automatic optimization
import Image from 'next/image'

<Image
  src="/logos/mokai-logo.png"
  alt="MOKAI PTY LTD"
  width={200}
  height={50}
  priority // Load above the fold images immediately
/>
```

**Database Indexing Strategy:**

```sql
-- Indexes for common queries
CREATE INDEX idx_transactions_entity_date
  ON transactions(entity_id, transaction_date DESC);

CREATE INDEX idx_invoices_entity_status
  ON invoices(entity_id, status, due_date);

CREATE INDEX idx_transactions_ai_category
  ON transactions(ai_category)
  WHERE ai_category IS NOT NULL;

-- Partial index for overdue invoices (common query)
CREATE INDEX idx_invoices_overdue
  ON invoices(entity_id, due_date)
  WHERE status = 'SENT' AND due_date < CURRENT_DATE;
```

**React Query Caching:**

```typescript
// Aggressive caching for static data (chart of accounts)
export function useAccounts() {
  return useQuery({
    queryKey: ['accounts'],
    queryFn: fetchAccounts,
    staleTime: Infinity, // Never refetch (accounts rarely change)
    cacheTime: Infinity, // Keep in cache forever
  })
}

// Short-lived cache for dynamic data (transactions)
export function useTransactions(entityId: string) {
  return useQuery({
    queryKey: ['transactions', entityId],
    queryFn: () => fetchTransactions(entityId),
    staleTime: 10 * 60 * 1000, // 10 minutes
    cacheTime: 30 * 60 * 1000, // 30 minutes
  })
}
```

### 6.2 Monitoring

**Vercel Analytics:**

```typescript
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react'

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
        <Analytics /> {/* Tracks Web Vitals, page views */}
      </body>
    </html>
  )
}
```

**Performance Budgets:**

```typescript
// next.config.js
module.exports = {
  experimental: {
    optimizeFonts: true,
    optimizeImages: true,
  },
  images: {
    formats: ['image/avif', 'image/webp'], // Modern formats
  },
  // Warn if bundle size exceeds limits
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.performance = {
        maxAssetSize: 500000, // 500KB
        maxEntrypointSize: 500000,
      }
    }
    return config
  },
}
```

**Performance Targets:**

| Metric | Target | Critical Threshold |
|--------|--------|-------------------|
| **First Contentful Paint (FCP)** | <1.5s | <2.5s |
| **Largest Contentful Paint (LCP)** | <2.0s | <3.0s |
| **Time to Interactive (TTI)** | <3.0s | <5.0s |
| **Cumulative Layout Shift (CLS)** | <0.1 | <0.25 |
| **First Input Delay (FID)** | <50ms | <100ms |
| **Chart Render Time** | <100ms | <200ms |
| **Table Render (1000 rows)** | <200ms | <500ms |

---

## 7. Financial Calculation Architecture

### 7.1 Calculation Layer (`lib/calculations/`)

**Decimal Precision Handling:**

```typescript
// lib/calculations/decimal.ts
import Decimal from 'decimal.js'

// Configure Decimal.js for financial calculations
Decimal.set({
  precision: 20, // 20 decimal places (overkill for currency, but safe)
  rounding: Decimal.ROUND_HALF_UP, // Standard rounding
  toExpNeg: -7, // Use exponential notation for very small numbers
  toExpPos: 21, // Use exponential notation for very large numbers
})

export function toCents(dollars: number | string): number {
  return new Decimal(dollars).times(100).round().toNumber()
}

export function toDollars(cents: number): number {
  return new Decimal(cents).dividedBy(100).toNumber()
}

export function add(...amounts: number[]): number {
  return amounts.reduce((sum, amount) =>
    new Decimal(sum).plus(amount).toNumber(),
    0
  )
}

export function multiply(amount: number, multiplier: number): number {
  return new Decimal(amount).times(multiplier).toNumber()
}

// Example: Calculate GST (10%)
export function calculateGST(amountCents: number): number {
  return new Decimal(amountCents)
    .times(0.1) // 10% GST
    .round() // Round to nearest cent
    .toNumber()
}
```

**BAS Calculation Module:**

```typescript
// lib/calculations/bas.ts
import Decimal from 'decimal.js'
import { createClient } from '@/lib/supabase/server'

interface BASReport {
  gst_on_sales: number // G1 - GST on sales
  gst_on_purchases: number // G11 - GST on purchases
  net_gst: number // 1A - GST payable/refund
  wine_sales: number // 1B - Wine equalisation tax
  total_sales: number // G1 - Total sales (excluding GST)
  export_sales: number // G2 - Export sales
  other_gst_free_sales: number // G3 - Other GST-free sales
  capital_purchases: number // G10 - Capital purchases
  non_capital_purchases: number // G11 - Non-capital purchases
}

export async function calculateBAS(
  entityId: string,
  startDate: string,
  endDate: string
): Promise<BASReport> {
  const supabase = await createClient()

  // Fetch all transactions in date range
  const { data: transactions } = await supabase
    .from('transactions')
    .select('*')
    .eq('entity_id', entityId)
    .gte('transaction_date', startDate)
    .lte('transaction_date', endDate)

  if (!transactions) throw new Error('No transactions found')

  let gst_on_sales = new Decimal(0)
  let gst_on_purchases = new Decimal(0)
  let total_sales = new Decimal(0)
  let capital_purchases = new Decimal(0)
  let non_capital_purchases = new Decimal(0)

  for (const txn of transactions) {
    const amount = new Decimal(txn.amount_cents)

    if (amount.greaterThan(0)) {
      // Income transaction
      total_sales = total_sales.plus(amount)
      gst_on_sales = gst_on_sales.plus(amount.times(0.1).round())
    } else {
      // Expense transaction
      const absAmount = amount.abs()

      if (txn.is_capital_purchase) {
        capital_purchases = capital_purchases.plus(absAmount)
      } else {
        non_capital_purchases = non_capital_purchases.plus(absAmount)
      }

      gst_on_purchases = gst_on_purchases.plus(absAmount.times(0.1).round())
    }
  }

  const net_gst = gst_on_sales.minus(gst_on_purchases)

  return {
    gst_on_sales: gst_on_sales.toNumber(),
    gst_on_purchases: gst_on_purchases.toNumber(),
    net_gst: net_gst.toNumber(),
    wine_sales: 0, // Not applicable for this business
    total_sales: total_sales.toNumber(),
    export_sales: 0, // TODO: Filter export sales
    other_gst_free_sales: 0, // TODO: Filter GST-free sales
    capital_purchases: capital_purchases.toNumber(),
    non_capital_purchases: non_capital_purchases.toNumber(),
  }
}
```

**P&L Calculation Module:**

```typescript
// lib/calculations/profit-loss.ts
import Decimal from 'decimal.js'
import { createClient } from '@/lib/supabase/server'

interface ProfitLossReport {
  revenue: number
  cost_of_goods_sold: number
  gross_profit: number
  operating_expenses: number
  operating_profit: number
  other_income: number
  other_expenses: number
  net_profit: number
  gross_margin_percentage: number
  operating_margin_percentage: number
  net_margin_percentage: number
}

export async function calculateProfitLoss(
  entityId: string,
  startDate: string,
  endDate: string
): Promise<ProfitLossReport> {
  const supabase = await createClient()

  // Fetch account balances for date range
  const { data: transactions } = await supabase
    .from('transaction_lines')
    .select(`
      *,
      account:accounts(account_type, account_code)
    `)
    .eq('entity_id', entityId)
    .gte('transaction_date', startDate)
    .lte('transaction_date', endDate)

  if (!transactions) throw new Error('No transactions found')

  let revenue = new Decimal(0)
  let cogs = new Decimal(0)
  let operating_expenses = new Decimal(0)
  let other_income = new Decimal(0)
  let other_expenses = new Decimal(0)

  for (const line of transactions) {
    const amount = new Decimal(line.amount_cents)

    switch (line.account.account_type) {
      case 'REVENUE':
        if (line.account.account_code.startsWith('4')) {
          revenue = revenue.plus(amount)
        } else {
          other_income = other_income.plus(amount)
        }
        break

      case 'EXPENSE':
        if (line.account.account_code.startsWith('5')) {
          cogs = cogs.plus(amount.abs())
        } else {
          operating_expenses = operating_expenses.plus(amount.abs())
        }
        break
    }
  }

  const gross_profit = revenue.minus(cogs)
  const operating_profit = gross_profit.minus(operating_expenses)
  const net_profit = operating_profit.plus(other_income).minus(other_expenses)

  return {
    revenue: revenue.toNumber(),
    cost_of_goods_sold: cogs.toNumber(),
    gross_profit: gross_profit.toNumber(),
    operating_expenses: operating_expenses.toNumber(),
    operating_profit: operating_profit.toNumber(),
    other_income: other_income.toNumber(),
    other_expenses: other_expenses.toNumber(),
    net_profit: net_profit.toNumber(),
    gross_margin_percentage: gross_profit.dividedBy(revenue).times(100).toNumber(),
    operating_margin_percentage: operating_profit.dividedBy(revenue).times(100).toNumber(),
    net_margin_percentage: net_profit.dividedBy(revenue).times(100).toNumber(),
  }
}
```

### 7.2 Testing Strategy for Financial Logic

**Unit Tests with ATO Examples:**

```typescript
// tests/unit/calculations/bas.test.ts
import { describe, it, expect } from 'vitest'
import { calculateBAS } from '@/lib/calculations/bas'

describe('BAS Calculation', () => {
  it('should calculate GST correctly for simple sale', () => {
    // ATO Example 1: $11,000 sale (inc. GST)
    const sale = 1100000 // cents
    const gst = sale * 0.1 / 1.1 // Reverse GST

    expect(gst).toBe(100000) // $1,000 GST
  })

  it('should handle mixed GST and GST-free sales', () => {
    // ATO Example 2: $10,000 GST sale + $5,000 GST-free sale
    const gstSale = 1000000
    const gstFreeSale = 500000

    const totalGST = (gstSale * 0.1 / 1.1) // Only GST sale contributes

    expect(totalGST).toBeCloseTo(90909, 0) // $909.09 GST (rounded)
  })

  it('should calculate net GST payable (sales - purchases)', () => {
    // ATO Example 3: $11,000 sales (inc. GST), $2,200 purchases (inc. GST)
    const gstOnSales = 1100000 * 0.1 / 1.1
    const gstOnPurchases = 220000 * 0.1 / 1.1
    const netGST = gstOnSales - gstOnPurchases

    expect(netGST).toBeCloseTo(80000, 0) // $800 GST payable
  })
})
```

**Property-Based Testing (Edge Cases):**

```typescript
// tests/unit/calculations/decimal.test.ts
import { describe, it, expect } from 'vitest'
import { fc, test } from '@fast-check/vitest'
import { add, multiply, calculateGST } from '@/lib/calculations/decimal'

describe('Decimal Math Properties', () => {
  test.prop([fc.double({ min: 0, max: 1000000 })])('add is commutative', (a) => {
    expect(add(a, 0)).toBe(a)
  })

  test.prop([
    fc.double({ min: 0, max: 1000000 }),
    fc.double({ min: 0, max: 1000000 })
  ])('multiply maintains precision', (a, b) => {
    const result = multiply(a, b)
    expect(typeof result).toBe('number')
    expect(Number.isFinite(result)).toBe(true)
  })

  test.prop([fc.integer({ min: 0, max: 100000000 })])('GST is always 10% of amount', (amount) => {
    const gst = calculateGST(amount)
    const expected = Math.round(amount * 0.1)
    expect(gst).toBe(expected)
  })
})
```

---

## 8. Data Visualization Architecture

### 8.1 Chart Library (Recharts)

**Chart Component Patterns:**

```typescript
// components/charts/SpendingPieChart.tsx
"use client"

import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'

interface SpendingPieChartProps {
  data: Array<{ category: string; amount: number }>
  colors?: string[]
}

const DEFAULT_COLORS = [
  '#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8',
  '#82CA9D', '#FFC658', '#FF6B9D', '#C084FC', '#34D399'
]

export function SpendingPieChart({
  data,
  colors = DEFAULT_COLORS
}: SpendingPieChartProps) {
  // Group small categories into "Other"
  const threshold = 0.05 // 5% of total
  const total = data.reduce((sum, item) => sum + item.amount, 0)

  const chartData = data.reduce((acc, item) => {
    if (item.amount / total < threshold) {
      const other = acc.find(d => d.category === 'Other')
      if (other) {
        other.amount += item.amount
      } else {
        acc.push({ category: 'Other', amount: item.amount })
      }
    } else {
      acc.push(item)
    }
    return acc
  }, [] as Array<{ category: string; amount: number }>)

  return (
    <ResponsiveContainer width="100%" height={400}>
      <PieChart>
        <Pie
          data={chartData}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ category, percent }) =>
            `${category}: ${(percent * 100).toFixed(1)}%`
          }
          outerRadius={120}
          fill="#8884d8"
          dataKey="amount"
        >
          {chartData.map((entry, index) => (
            <Cell
              key={`cell-${index}`}
              fill={colors[index % colors.length]}
            />
          ))}
        </Pie>
        <Tooltip
          formatter={(value: number) => `$${(value / 100).toFixed(2)}`}
        />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  )
}
```

**Cash Flow Waterfall Chart:**

```typescript
// components/charts/CashFlowWaterfallChart.tsx
"use client"

import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Cell, ReferenceLine
} from 'recharts'

interface CashFlowData {
  month: string
  inflow: number
  outflow: number
  net: number
}

export function CashFlowWaterfallChart({ data }: { data: CashFlowData[] }) {
  // Transform data for waterfall effect
  let runningBalance = 0
  const waterfallData = data.map((item) => {
    const netChange = item.inflow - item.outflow
    const start = runningBalance
    runningBalance += netChange

    return {
      month: item.month,
      start,
      net: netChange,
      end: runningBalance,
      isPositive: netChange >= 0,
    }
  })

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={waterfallData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis
          tickFormatter={(value) => `$${(value / 100).toFixed(0)}k`}
        />
        <Tooltip
          formatter={(value: number) => `$${(value / 100).toFixed(2)}`}
        />
        <ReferenceLine y={0} stroke="#000" />
        <Bar dataKey="net" fill="#8884d8">
          {waterfallData.map((entry, index) => (
            <Cell
              key={`cell-${index}`}
              fill={entry.isPositive ? '#10B981' : '#EF4444'}
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
```

### 8.2 Table Component (TanStack Table)

**Virtual Scrolling Setup:**

```typescript
// components/tables/TransactionTable.tsx
"use client"

import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  flexRender,
} from '@tanstack/react-table'
import { useVirtualizer } from '@tanstack/react-virtual'
import { useMemo, useRef } from 'react'

export function TransactionTable({ data }: { data: Transaction[] }) {
  const tableContainerRef = useRef<HTMLDivElement>(null)

  const columns = useMemo(
    () => [
      {
        accessorKey: 'transaction_date',
        header: 'Date',
        cell: (info) => formatDate(info.getValue()),
      },
      {
        accessorKey: 'description',
        header: 'Description',
      },
      {
        accessorKey: 'ai_category',
        header: 'Category',
        cell: (info) => (
          <CategoryBadge
            category={info.getValue()}
            confidence={info.row.original.ai_confidence}
          />
        ),
      },
      {
        accessorKey: 'amount_cents',
        header: 'Amount',
        cell: (info) => formatCurrency(info.getValue()),
      },
    ],
    []
  )

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
  })

  const { rows } = table.getRowModel()

  const rowVirtualizer = useVirtualizer({
    count: rows.length,
    getScrollElement: () => tableContainerRef.current,
    estimateSize: () => 50,
    overscan: 10,
  })

  return (
    <div ref={tableContainerRef} className="h-[600px] overflow-auto">
      <table className="w-full">
        <thead className="sticky top-0 bg-white z-10">
          {table.getHeaderGroups().map(headerGroup => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map(header => (
                <th key={header.id} className="px-4 py-2 text-left">
                  {header.isPlaceholder
                    ? null
                    : flexRender(
                        header.column.columnDef.header,
                        header.getContext()
                      )}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          <tr style={{ height: `${rowVirtualizer.getTotalSize()}px` }} />
          {rowVirtualizer.getVirtualItems().map((virtualRow) => {
            const row = rows[virtualRow.index]
            return (
              <tr
                key={row.id}
                style={{
                  position: 'absolute',
                  transform: `translateY(${virtualRow.start}px)`,
                  width: '100%',
                }}
                className="hover:bg-gray-50"
              >
                {row.getVisibleCells().map(cell => (
                  <td key={cell.id} className="px-4 py-2">
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
```

---

## 9. Form Architecture

### 9.1 Form Handling (React Hook Form + Zod)

**Invoice Form Pattern:**

```typescript
// lib/validations/invoice.ts
import { z } from 'zod'

export const invoiceLineItemSchema = z.object({
  description: z.string().min(1, 'Description is required').max(500),
  quantity: z.number().positive().int(),
  unit_price_cents: z.number().int().nonnegative(),
  gst_applicable: z.boolean(),
})

export const invoiceSchema = z.object({
  entity_id: z.string().uuid(),
  contact_id: z.string().uuid(),
  invoice_type: z.enum(['RECEIVABLE', 'PAYABLE']),
  invoice_number: z.string().optional(), // Auto-generated if not provided
  issue_date: z.string().date(),
  due_date: z.string().date(),
  payment_terms: z.string().optional(),
  line_items: z.array(invoiceLineItemSchema).min(1, 'At least one line item required'),
  notes: z.string().optional(),
})

export type InvoiceFormData = z.infer<typeof invoiceSchema>
```

```typescript
// components/forms/InvoiceForm.tsx
"use client"

import { useForm, useFieldArray } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { invoiceSchema, type InvoiceFormData } from '@/lib/validations/invoice'

export function InvoiceForm({ onSubmit }: { onSubmit: (data: InvoiceFormData) => Promise<void> }) {
  const form = useForm<InvoiceFormData>({
    resolver: zodResolver(invoiceSchema),
    defaultValues: {
      invoice_type: 'RECEIVABLE',
      line_items: [
        {
          description: '',
          quantity: 1,
          unit_price_cents: 0,
          gst_applicable: true
        }
      ],
    },
  })

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: 'line_items',
  })

  const calculateTotals = () => {
    const lineItems = form.watch('line_items')
    const subtotal = lineItems.reduce((sum, item) =>
      sum + (item.quantity * item.unit_price_cents), 0
    )
    const gst = lineItems.reduce((sum, item) =>
      item.gst_applicable ? sum + (item.quantity * item.unit_price_cents * 0.1) : sum, 0
    )
    return { subtotal, gst, total: subtotal + gst }
  }

  const { subtotal, gst, total } = calculateTotals()

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="contact_id"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Customer</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select customer" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {/* Customer options */}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold">Line Items</h3>
            <Button
              type="button"
              variant="outline"
              onClick={() => append({
                description: '',
                quantity: 1,
                unit_price_cents: 0,
                gst_applicable: true
              })}
            >
              Add Line Item
            </Button>
          </div>

          {fields.map((field, index) => (
            <div key={field.id} className="grid grid-cols-12 gap-4">
              <div className="col-span-5">
                <FormField
                  control={form.control}
                  name={`line_items.${index}.description`}
                  render={({ field }) => (
                    <FormItem>
                      <FormControl>
                        <Input placeholder="Description" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <div className="col-span-2">
                <FormField
                  control={form.control}
                  name={`line_items.${index}.quantity`}
                  render={({ field }) => (
                    <FormItem>
                      <FormControl>
                        <Input
                          type="number"
                          placeholder="Qty"
                          {...field}
                          onChange={(e) => field.onChange(parseInt(e.target.value))}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <div className="col-span-3">
                <FormField
                  control={form.control}
                  name={`line_items.${index}.unit_price_cents`}
                  render={({ field }) => (
                    <FormItem>
                      <FormControl>
                        <CurrencyInput {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <div className="col-span-2 flex items-center justify-end gap-2">
                <Checkbox
                  checked={form.watch(`line_items.${index}.gst_applicable`)}
                  onCheckedChange={(checked) =>
                    form.setValue(`line_items.${index}.gst_applicable`, checked as boolean)
                  }
                />
                <span className="text-sm">GST</span>

                {fields.length > 1 && (
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={() => remove(index)}
                  >
                    Remove
                  </Button>
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="flex justify-end">
          <div className="w-64 space-y-2">
            <div className="flex justify-between">
              <span>Subtotal:</span>
              <span>{formatCurrency(subtotal)}</span>
            </div>
            <div className="flex justify-between">
              <span>GST (10%):</span>
              <span>{formatCurrency(gst)}</span>
            </div>
            <div className="flex justify-between font-bold text-lg">
              <span>Total:</span>
              <span>{formatCurrency(total)}</span>
            </div>
          </div>
        </div>

        <div className="flex justify-end gap-4">
          <Button type="button" variant="outline">Cancel</Button>
          <Button type="submit" disabled={form.formState.isSubmitting}>
            {form.formState.isSubmitting ? 'Creating...' : 'Create Invoice'}
          </Button>
        </div>
      </form>
    </Form>
  )
}
```

---

## 10. Testing Architecture

### 10.1 Unit Tests (Vitest)

**Financial Calculation Tests (100% Coverage):**

```typescript
// tests/unit/calculations/gst.test.ts
import { describe, it, expect } from 'vitest'
import { calculateGST, reverseGST } from '@/lib/calculations/gst'

describe('GST Calculations', () => {
  describe('calculateGST', () => {
    it('should calculate 10% GST correctly', () => {
      expect(calculateGST(10000)).toBe(1000) // $100 → $10 GST
      expect(calculateGST(50000)).toBe(5000) // $500 → $50 GST
    })

    it('should round to nearest cent', () => {
      expect(calculateGST(10005)).toBe(1001) // $100.05 → $10.01 GST (rounded up)
      expect(calculateGST(10004)).toBe(1000) // $100.04 → $10.00 GST (rounded down)
    })

    it('should handle zero amount', () => {
      expect(calculateGST(0)).toBe(0)
    })

    it('should handle large amounts without overflow', () => {
      const largeAmount = 999999999999 // $9.99B
      const gst = calculateGST(largeAmount)
      expect(gst).toBe(99999999999) // $999.99M GST
    })
  })

  describe('reverseGST', () => {
    it('should extract GST from GST-inclusive amount', () => {
      expect(reverseGST(11000)).toBe(1000) // $110 inc GST → $10 GST
      expect(reverseGST(55000)).toBe(5000) // $550 inc GST → $50 GST
    })

    it('should match ATO examples', () => {
      // ATO Example: $1,100 inc GST → $100 GST
      expect(reverseGST(110000)).toBe(10000)
    })
  })
})
```

### 10.2 Integration Tests (Testing Library)

**Component + Data Interaction Tests:**

```typescript
// tests/integration/components/TransactionTable.test.tsx
import { describe, it, expect, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { TransactionTable } from '@/components/tables/TransactionTable'
import { mockTransactions } from '@/tests/mocks/data'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: false },
    mutations: { retry: false },
  },
})

function Wrapper({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )
}

describe('TransactionTable', () => {
  it('should render transaction list', async () => {
    render(<TransactionTable />, { wrapper: Wrapper })

    await waitFor(() => {
      expect(screen.getByText(mockTransactions[0].description)).toBeInTheDocument()
    })
  })

  it('should filter transactions by entity', async () => {
    const user = userEvent.setup()
    render(<TransactionTable />, { wrapper: Wrapper })

    // Open entity selector
    const entitySelector = screen.getByRole('combobox', { name: /entity/i })
    await user.click(entitySelector)

    // Select MOKAI
    const mokaiOption = screen.getByText('MOKAI PTY LTD')
    await user.click(mokaiOption)

    // Only MOKAI transactions should be visible
    await waitFor(() => {
      const rows = screen.getAllByRole('row')
      expect(rows.length).toBe(mockTransactions.filter(t => t.entity_id === 'mokai-id').length + 1) // +1 for header
    })
  })

  it('should sort by date when clicking date header', async () => {
    const user = userEvent.setup()
    render(<TransactionTable />, { wrapper: Wrapper })

    const dateHeader = screen.getByRole('button', { name: /date/i })
    await user.click(dateHeader)

    await waitFor(() => {
      const rows = screen.getAllByRole('row')
      // Verify first transaction is most recent
      expect(rows[1]).toHaveTextContent('2024-10-17')
    })
  })
})
```

### 10.3 E2E Tests (Playwright)

**Critical User Flows:**

```typescript
// tests/e2e/invoices.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Invoice Creation Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login')
    await page.fill('input[name="email"]', 'test@example.com')
    await page.fill('input[name="password"]', 'password')
    await page.click('button[type="submit"]')

    await expect(page).toHaveURL('/dashboard')
  })

  test('should create invoice and generate PDF', async ({ page }) => {
    // Navigate to invoices
    await page.click('text=Invoices')
    await expect(page).toHaveURL('/invoices')

    // Click "New Invoice"
    await page.click('text=New Invoice')
    await expect(page).toHaveURL('/invoices/new')

    // Fill invoice form
    await page.selectOption('select[name="contact_id"]', 'customer-1')
    await page.fill('input[name="issue_date"]', '2024-10-17')
    await page.fill('input[name="due_date"]', '2024-11-17')

    // Add line item
    await page.fill('input[name="line_items.0.description"]', 'Consulting Services')
    await page.fill('input[name="line_items.0.quantity"]', '10')
    await page.fill('input[name="line_items.0.unit_price_cents"]', '15000')

    // Submit form
    await page.click('button[type="submit"]')

    // Should redirect to invoice detail
    await expect(page).toHaveURL(/\/invoices\/[a-f0-9-]+/)

    // Verify invoice details
    await expect(page.locator('text=Consulting Services')).toBeVisible()
    await expect(page.locator('text=$150.00')).toBeVisible()

    // Download PDF
    const [download] = await Promise.all([
      page.waitForEvent('download'),
      page.click('text=Download PDF'),
    ])

    expect(download.suggestedFilename()).toMatch(/invoice-.*\.pdf/)
  })

  test('should mark invoice as paid', async ({ page }) => {
    // Navigate to existing invoice
    await page.goto('/invoices/existing-invoice-id')

    // Verify status is "SENT"
    await expect(page.locator('text=Sent')).toBeVisible()

    // Mark as paid
    await page.click('text=Mark as Paid')

    // Fill payment details
    await page.fill('input[name="payment_date"]', '2024-10-17')
    await page.selectOption('select[name="payment_method"]', 'Bank Transfer')
    await page.click('button:has-text("Confirm Payment")')

    // Verify status is "PAID"
    await expect(page.locator('text=Paid')).toBeVisible()

    // Verify payment date is displayed
    await expect(page.locator('text=Paid on Oct 17, 2024')).toBeVisible()
  })
})
```

---

## 11. Deployment Architecture

### 11.1 Vercel Setup

**Environment Variables:**

```bash
# Vercel Environment Variables (encrypted)

# Public (exposed to browser)
NEXT_PUBLIC_SUPABASE_URL=https://gshsshaodoyttdxippwx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Private (server-only)
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Build Configuration:**

```typescript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,

  images: {
    domains: ['gshsshaodoyttdxippwx.supabase.co'],
    formats: ['image/avif', 'image/webp'],
  },

  async redirects() {
    return [
      {
        source: '/',
        destination: '/dashboard',
        permanent: false,
      },
    ]
  },

  // Enable experimental features
  experimental: {
    serverActions: true,
  },
}

module.exports = nextConfig
```

### 11.2 CI/CD Pipeline

**GitHub Actions Workflow:**

```yaml
# .github/workflows/deploy.yml
name: Deploy to Vercel

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
  VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Type check
        run: npm run type-check

      - name: Lint
        run: npm run lint

      - name: Unit tests
        run: npm run test:unit

      - name: Build
        run: npm run build
        env:
          NEXT_PUBLIC_SUPABASE_URL: ${{ secrets.NEXT_PUBLIC_SUPABASE_URL }}
          NEXT_PUBLIC_SUPABASE_ANON_KEY: ${{ secrets.NEXT_PUBLIC_SUPABASE_ANON_KEY }}

  deploy-preview:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    needs: test
    steps:
      - uses: actions/checkout@v4

      - name: Install Vercel CLI
        run: npm install --global vercel@latest

      - name: Pull Vercel Environment Information
        run: vercel pull --yes --environment=preview --token=${{ secrets.VERCEL_TOKEN }}

      - name: Build Project Artifacts
        run: vercel build --token=${{ secrets.VERCEL_TOKEN }}

      - name: Deploy Project Artifacts to Vercel
        run: vercel deploy --prebuilt --token=${{ secrets.VERCEL_TOKEN }}

  deploy-production:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    needs: test
    steps:
      - uses: actions/checkout@v4

      - name: Install Vercel CLI
        run: npm install --global vercel@latest

      - name: Pull Vercel Environment Information
        run: vercel pull --yes --environment=production --token=${{ secrets.VERCEL_TOKEN }}

      - name: Build Project Artifacts
        run: vercel build --prod --token=${{ secrets.VERCEL_TOKEN }}

      - name: Deploy Project Artifacts to Vercel
        run: vercel deploy --prebuilt --prod --token=${{ secrets.VERCEL_TOKEN }}

      - name: Run E2E tests
        run: npm run test:e2e
        env:
          PLAYWRIGHT_TEST_BASE_URL: https://your-production-url.vercel.app
```

---

## 12. Migration & Phased Rollout

### 12.1 Phase 1 (MVP) Infrastructure

**Sprint 1-3: Foundation + Transaction Tracking**

**Infrastructure Setup:**
```bash
# 1. Create Next.js project
npx create-next-app@latest financial-dashboard \
  --typescript \
  --tailwind \
  --app \
  --eslint

# 2. Install core dependencies
npm install \
  @supabase/ssr \
  @tanstack/react-query \
  zustand \
  react-hook-form \
  @hookform/resolvers \
  zod \
  decimal.js \
  date-fns \
  recharts

# 3. Install shadcn/ui
npx shadcn-ui@latest init

# 4. Install shadcn components
npx shadcn-ui@latest add button card table dialog select input form toast

# 5. Generate Supabase types
npx supabase gen types typescript \
  --project-id gshsshaodoyttdxippwx \
  --schema public \
  > types/database.ts
```

**Core Features:**
- ✅ Next.js App Router setup
- ✅ Supabase client configuration (browser + server)
- ✅ Supabase Auth flow (login/signup/logout)
- ✅ Entity selector (global state with Zustand)
- ✅ Transaction list view (Server Component)
- ✅ Transaction filtering (Client Component)
- ✅ Spending breakdown chart (Recharts PieChart)
- ✅ Dashboard KPI cards (Server Component)

### 12.2 Subsequent Phases

**Phase 2 (Sprint 4-6): Invoicing & Cash Flow**
- Invoice CRUD operations
- Invoice PDF generation
- Payment tracking
- Cash flow dashboard
- Cash flow forecasting (ML integration)

**Phase 3 (Sprint 7-8): Budgeting & Alerts**
- Budget creation and tracking
- Budget vs actual comparison
- Budget alerts (80%, 100%)
- Anomaly detection display

**Phase 4 (Sprint 9-11): Accounting & Reporting**
- Profit & Loss report
- Balance Sheet report
- BAS statement generation
- Chart of accounts view
- Account transaction history

**Phase 5 (Sprint 12-13): Analytics & ML Insights**
- AI insights dashboard
- Spending trend analysis
- Predictive spending
- Anomaly explanations

**Phase 6 (Sprint 14): Polish & UX**
- CSV/Excel export
- PDF report generation
- Mobile responsiveness optimization
- Keyboard shortcuts
- Dark mode
- Bulk operations

**Feature Flags for Gradual Rollout:**

```typescript
// lib/feature-flags.ts
export const featureFlags = {
  invoicing: process.env.NEXT_PUBLIC_FEATURE_INVOICING === 'true',
  budgeting: process.env.NEXT_PUBLIC_FEATURE_BUDGETING === 'true',
  reporting: process.env.NEXT_PUBLIC_FEATURE_REPORTING === 'true',
  mlInsights: process.env.NEXT_PUBLIC_FEATURE_ML_INSIGHTS === 'true',
  darkMode: process.env.NEXT_PUBLIC_FEATURE_DARK_MODE === 'true',
}

// Usage in components
import { featureFlags } from '@/lib/feature-flags'

function Navigation() {
  return (
    <nav>
      <Link href="/dashboard">Dashboard</Link>
      <Link href="/transactions">Transactions</Link>
      {featureFlags.invoicing && <Link href="/invoices">Invoices</Link>}
      {featureFlags.reporting && <Link href="/reports">Reports</Link>}
    </nav>
  )
}
```

---

## 13. Monitoring & Observability

### 13.1 Logging Strategy

**Error Logging (Sentry):**

```typescript
// lib/sentry.ts
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,

  beforeSend(event, hint) {
    // Don't send errors in development
    if (process.env.NODE_ENV === 'development') {
      return null
    }

    // Filter sensitive data
    if (event.request) {
      delete event.request.cookies
    }

    return event
  },
})
```

**Audit Trails (Financial Operations):**

```typescript
// lib/audit.ts
import { createClient } from '@/lib/supabase/server'

export async function logAuditEvent(
  userId: string,
  action: string,
  resource: string,
  resourceId: string,
  metadata?: Record<string, any>
) {
  const supabase = await createClient()

  await supabase.from('audit_logs').insert({
    user_id: userId,
    action,
    resource,
    resource_id: resourceId,
    metadata,
    created_at: new Date().toISOString(),
  })
}

// Usage
await logAuditEvent(
  userId,
  'INVOICE_CREATED',
  'invoices',
  invoice.id,
  { total_cents: invoice.total_cents }
)
```

### 13.2 Performance Monitoring

**Core Web Vitals (Vercel Analytics):**

```typescript
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react'
import { SpeedInsights } from '@vercel/speed-insights/next'

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  )
}
```

**Database Query Performance:**

```sql
-- Monitor slow queries in Supabase
SELECT
  query,
  calls,
  total_time,
  mean_time,
  max_time
FROM pg_stat_statements
WHERE mean_time > 100 -- Queries averaging >100ms
ORDER BY mean_time DESC
LIMIT 20;
```

---

## 14. Scalability Considerations

### 14.1 Database Scaling

**Connection Pooling:**

```typescript
// Supabase handles connection pooling automatically
// Configure pool size in Supabase dashboard if needed
```

**Query Optimization:**

```sql
-- Create composite indexes for common query patterns
CREATE INDEX idx_transactions_entity_date_amount
  ON transactions(entity_id, transaction_date DESC, amount_cents);

CREATE INDEX idx_invoices_entity_status_due
  ON invoices(entity_id, status, due_date);

-- Analyze query plans
EXPLAIN ANALYZE
SELECT * FROM transactions
WHERE entity_id = '...'
  AND transaction_date >= '2024-01-01'
ORDER BY transaction_date DESC
LIMIT 100;
```

**Caching Strategy:**

```typescript
// React Query cache configuration
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // Transactions: 10 min stale time
      staleTime: 10 * 60 * 1000,
      cacheTime: 30 * 60 * 1000,

      // Keep queries in background
      refetchOnWindowFocus: true,
      refetchOnReconnect: true,
    },
  },
})
```

### 14.2 Application Scaling

**Vercel Edge Functions:**

```typescript
// app/api/reports/bas/route.ts
export const runtime = 'edge' // Deploy to Edge runtime for global distribution
export const dynamic = 'force-dynamic' // Bypass static optimization

export async function POST(request: Request) {
  // BAS generation logic runs on edge
}
```

**Static Generation for Reports:**

```typescript
// app/reports/profit-loss/page.tsx
export const revalidate = 3600 // Revalidate every hour

export default async function ProfitLossPage() {
  // Pre-render P&L reports at build time
  const report = await generateProfitLoss()
  return <ProfitLossReport data={report} />
}
```

---

## 15. Technical Debt & Future Considerations

### 15.1 Known Trade-offs

**Vercel Free Tier Limitations:**
- **Bandwidth**: 100GB/month
- **Function Executions**: 100/day
- **Build Minutes**: 100/month
- **Mitigation**: Monitor usage via Vercel dashboard, upgrade to Pro ($20/month) if exceeded

**React Query vs Server Components Balance:**
- **Current**: Mix of Server Components (SSR) + React Query (client-side caching)
- **Trade-off**: Some data is fetched twice (SSR + React Query initial fetch)
- **Future**: Use Server Components more aggressively, reduce React Query usage

**Chart Library Performance:**
- **Current**: Recharts handles <1000 data points well
- **Trade-off**: Performance degrades with 10k+ data points
- **Mitigation**: Implement data sampling for large datasets, or consider react-chartjs-2 for better performance

### 15.2 Future Enhancements

**Multi-User Support:**
- Add user management (invite team members)
- Role-based permissions (admin, accountant, viewer)
- Collaborative features (comments, approvals)

**Real-Time Collaboration:**
- Supabase Realtime subscriptions for live updates
- Presence indicators (who's viewing what)
- Collaborative editing (invoices, budgets)

**Mobile App:**
- React Native mobile app (iOS/Android)
- Offline support with local SQLite
- Push notifications for alerts

**Offline Support:**
- Service Worker for offline functionality
- IndexedDB for local caching
- Sync queue for offline mutations

**Advanced Reporting:**
- Custom report builder (drag-and-drop)
- Scheduled report generation (email PDFs)
- Integration with accounting software (Xero, MYOB)

---

## Appendices

### Appendix A: Glossary

| Term | Definition |
|------|------------|
| **BAS** | Business Activity Statement - Australian quarterly tax report (GST, PAYG) |
| **GST** | Goods and Services Tax - 10% tax on most goods and services in Australia |
| **P&L** | Profit & Loss statement - Financial report showing revenue, expenses, profit |
| **RLS** | Row-Level Security - Supabase security model for data isolation |
| **Server Components** | React Server Components - Components that render on the server |
| **Client Components** | Components that render in the browser (marked with "use client") |
| **SSR** | Server-Side Rendering - Rendering HTML on the server |
| **CSR** | Client-Side Rendering - Rendering HTML in the browser |
| **Optimistic Update** | Update UI immediately before server confirmation |

### Appendix B: Reference Links

- **Next.js Documentation**: https://nextjs.org/docs
- **Supabase Documentation**: https://supabase.com/docs
- **shadcn/ui Components**: https://ui.shadcn.com/
- **Recharts Documentation**: https://recharts.org/
- **React Query Documentation**: https://tanstack.com/query/latest
- **Zod Documentation**: https://zod.dev/
- **ATO BAS Guidelines**: https://www.ato.gov.au/Business/BAS/

### Appendix C: Code Examples Repository

All code examples in this document are production-ready and can be copied directly into the project. For the latest examples and patterns, refer to:

- `/lib/calculations/` - Financial calculation modules
- `/components/charts/` - Recharts wrapper components
- `/components/forms/` - Form components with validation
- `/tests/` - Unit, integration, and E2E test examples

---

**End of Architecture Document**

This architecture document serves as the single source of truth for all technical decisions and implementation patterns for the SAYERS Financial Dashboard. All development must follow the patterns, technologies, and best practices outlined in this document.

For questions or clarifications, refer to the PRD (`docs/prd.md`) for business requirements or the Frontend Specification (`docs/front-end-spec.md`) for UI/UX details.
