---
date: "2025-10-17"
phase: 1
duration: "3 weeks"
status: "Ready for Implementation"
priority: "Must Have - MVP"
---

# Phase 1: Transaction & Spending Tracking (MVP)
## Implementation Guide

---

## Phase Overview

Build the foundational MVP that provides complete visibility into personal and business transactions. This phase establishes the core architecture (Next.js + Supabase + shadcn/ui) and delivers immediate value through transaction viewing, filtering, and category-based spending analysis.

**Duration**: 3 weeks
- Week 1: Foundation (Next.js setup, Supabase integration, auth)
- Week 2: Core features (transaction list, filtering, charts)
- Week 3: Polish (mobile, testing, deployment)

**Success Criteria**: Users can view all transactions across entities, filter by category/date/project, and visualize spending patterns.

---

## User Stories from PRD

### Epic 1.1: Unified Transaction View

#### Story 1.1.1: View All Transactions ⭐ CRITICAL
**As a** user
**I want to** see all transactions (personal + business) in one place
**So that** I have complete financial visibility

**Acceptance Criteria**:
- [ ] Display transaction date, description, amount, category, entity
- [ ] Show ML-assigned category and confidence score
- [ ] Include project tags (DiDi, Repco, Nintendo, etc.)
- [ ] Support pagination (50 transactions per page)
- [ ] Load initial view in <2 seconds

**Priority**: Must Have
**Dependencies**: None

---

#### Story 1.1.2: Filter by Entity ⭐ CRITICAL
**As a** user
**I want to** filter transactions by entity (Personal/MOKAI/MOK HOUSE)
**So that** I can focus on specific business or personal finances

**Acceptance Criteria**:
- [ ] Entity selector dropdown in header
- [ ] Filter persists across page navigation (localStorage)
- [ ] Show entity-specific totals
- [ ] Update charts to match filter

**Priority**: Must Have
**Dependencies**: Story 1.1.1

---

#### Story 1.1.3: Search Transactions
**As a** user
**I want to** search transactions by description, amount, or category
**So that** I can quickly find specific transactions

**Acceptance Criteria**:
- [ ] Real-time search (debounced 300ms)
- [ ] Match partial strings in description
- [ ] Support amount ranges (e.g., "$50-$100")
- [ ] Highlight search terms in results

**Priority**: Must Have
**Dependencies**: Story 1.1.1

---

### Epic 1.2: Category Breakdown & Analysis

#### Story 1.2.1: Category Spending Chart ⭐ CRITICAL
**As a** user
**I want to** see a pie/donut chart of spending by category
**So that** I understand where money is going

**Acceptance Criteria**:
- [ ] Show top 10 categories with percentages
- [ ] "Other" category for remaining
- [ ] Responsive design (mobile-friendly)
- [ ] Click category to drill down to transactions

**Priority**: Must Have
**Dependencies**: Story 1.1.1

---

#### Story 1.2.2: Spending Trends Over Time
**As a** user
**I want to** see spending trends by month/week
**So that** I can track financial patterns

**Acceptance Criteria**:
- [ ] Line chart with time selector (week/month/quarter/year)
- [ ] Compare current period to previous
- [ ] Show trend direction (up/down percentage)
- [ ] Export chart as PNG/PDF

**Priority**: Should Have
**Dependencies**: Story 1.2.1

---

### Epic 1.3: Project-Based Tracking

#### Story 1.3.1: Project Filter
**As a** business owner
**I want to** filter transactions by project (DiDi, Repco, Nintendo, etc.)
**So that** I can understand project profitability

**Acceptance Criteria**:
- [ ] Project selector shows all active projects
- [ ] Display project-specific totals
- [ ] Show project timeline (start/end dates if available)
- [ ] Calculate project ROI if revenue data available

**Priority**: Should Have
**Dependencies**: Story 1.1.1

---

## Technical Requirements from Architecture

### 2.1 Next.js App Router Structure

**Create these routes/components**:

```
app/
├── (auth)/
│   ├── login/page.tsx                 # Supabase Auth login
│   ├── signup/page.tsx                # Supabase Auth signup
│   └── reset-password/page.tsx        # Password reset
│
├── (dashboard)/
│   ├── layout.tsx                     # Dashboard shell (sidebar, header, entity selector)
│   ├── page.tsx                       # Dashboard home (KPIs, recent transactions, alerts)
│   │
│   └── transactions/
│       ├── page.tsx                   # Transaction list (Server Component)
│       └── components/
│           ├── TransactionTable.tsx   # Client Component (virtual scrolling)
│           ├── TransactionFilters.tsx # Client Component (filter UI)
│           └── CategoryBadge.tsx      # Editable category badge
│
components/
├── ui/                                # shadcn/ui components
│   ├── button.tsx
│   ├── card.tsx
│   ├── table.tsx
│   ├── input.tsx
│   └── ... (install as needed)
│
├── dashboard/
│   ├── KPICard.tsx                    # Metric card with trend
│   ├── EntitySelector.tsx             # Multi-entity dropdown
│   ├── RecentTransactions.tsx         # Recent transactions widget
│   ├── SpendingChart.tsx              # Donut chart
│   └── AlertBanner.tsx                # Alerts widget
│
└── charts/
    ├── PieChart.tsx                   # Recharts pie chart
    ├── LineChart.tsx                  # Recharts line chart
    └── ChartCard.tsx                  # Reusable chart container
```

---

### 2.2 Data Fetching Pattern

**Server Components First (SSR):**

```typescript
// app/transactions/page.tsx (Server Component)
import { createClient } from '@/lib/supabase/server'
import { TransactionTable } from './components/TransactionTable'

export default async function TransactionsPage() {
  const supabase = await createClient()

  // Fetch data server-side (SSR) - CRITICAL: Combine both tables
  const [personalTxns, businessTxns] = await Promise.all([
    supabase
      .from('personal_transactions')
      .select(`
        id,
        description,
        amount,
        transaction_date,
        category:personal_finance_categories(name),
        ai_category,
        ai_confidence,
        project
      `)
      .order('transaction_date', { ascending: false })
      .limit(100),

    supabase
      .from('transactions')
      .select(`
        id,
        description,
        amount,
        transaction_date,
        category,
        ai_category,
        ai_confidence,
        project,
        entity:entities(name)
      `)
      .order('transaction_date', { ascending: false })
      .limit(100)
  ])

  // Combine and sort by date
  const allTransactions = [
    ...(personalTxns.data || []),
    ...(businessTxns.data || [])
  ].sort((a, b) =>
    new Date(b.transaction_date).getTime() - new Date(a.transaction_date).getTime()
  )

  return <TransactionTable initialData={allTransactions} />
}
```

**React Query for Client Interactions:**

```typescript
// hooks/use-transactions.ts
import { useQuery } from '@tanstack/react-query'
import { supabase } from '@/lib/supabase/client'

export function useTransactions(entityId?: string) {
  return useQuery({
    queryKey: ['transactions', entityId],
    queryFn: async () => {
      // Fetch both personal and business transactions
      const [personal, business] = await Promise.all([
        supabase
          .from('personal_transactions')
          .select('*')
          .order('transaction_date', { ascending: false }),

        supabase
          .from('transactions')
          .select('*')
          .eq('entity_id', entityId)
          .order('transaction_date', { ascending: false })
      ])

      return [...(personal.data || []), ...(business.data || [])]
    },
    staleTime: 10 * 60 * 1000, // 10 minutes
    refetchInterval: 10 * 60 * 1000, // Poll every 10 minutes
    refetchOnWindowFocus: true,
  })
}
```

---

### 2.3 Virtual Scrolling (TanStack Table + TanStack Virtual)

**Critical for performance with 256+ transactions:**

```typescript
// components/transactions/TransactionTable.tsx
"use client"

import { useVirtualizer } from '@tanstack/react-virtual'
import { useTransactions } from '@/hooks/use-transactions'
import { useEntityFilter } from '@/stores/entity-filter'

export function TransactionTable({ initialData }: { initialData: Transaction[] }) {
  const { selectedEntityId } = useEntityFilter()
  const { data = initialData } = useTransactions(selectedEntityId)

  const parentRef = useRef<HTMLDivElement>(null)

  const virtualizer = useVirtualizer({
    count: data.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50, // Row height
    overscan: 10, // Extra rows for smooth scrolling
  })

  return (
    <div ref={parentRef} className="h-[600px] overflow-auto">
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
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

---

### 2.4 Entity Filter (Zustand Global State)

**Critical for multi-entity isolation:**

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
      selectedEntityId: null, // null = all entities
      setSelectedEntity: (entityId) => set({ selectedEntityId: entityId }),
    }),
    {
      name: 'entity-filter', // localStorage key
    }
  )
)
```

```typescript
// components/dashboard/EntitySelector.tsx
"use client"

import { useEntityFilter } from '@/stores/entity-filter'
import { Select } from '@/components/ui/select'

export function EntitySelector({ entities }: { entities: Entity[] }) {
  const { selectedEntityId, setSelectedEntity } = useEntityFilter()

  return (
    <Select
      value={selectedEntityId || 'all'}
      onValueChange={(value) => setSelectedEntity(value === 'all' ? null : value)}
    >
      <SelectTrigger>
        <SelectValue />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="all">All Entities</SelectItem>
        {entities.map((entity) => (
          <SelectItem key={entity.id} value={entity.id}>
            {entity.name}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  )
}
```

---

## UI Specifications from Frontend Spec

### 3.1 Dashboard Home Page

**Wireframe**:
```
┌─────────────────────────────────────────────────────────────────┐
│ Dashboard                                      [Last 30 Days ▼] │
├─────────────────────────────────────────────────────────────────┤
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐    │
│ │ Income   │ │ Expenses │ │ Net      │ │ Cash Balance     │    │
│ │ $12,450  │ │ $8,320   │ │ $4,130   │ │ $34,567          │    │
│ │ ↑ 12%    │ │ ↓ 5%     │ │ ↑ 25%    │ │ ─────────        │    │
│ └──────────┘ └──────────┘ └──────────┘ └──────────────────┘    │
├─────────────────────────────────────────────────────────────────┤
│ ┌──────────────────────┐ ┌───────────────────────────────────┐ │
│ │ Spending by Category │ │ Recent Transactions               │ │
│ │ ┌────────────────┐   │ │ Oct 17  Office Supplies  -$45.00  │ │
│ │ │   Donut Chart  │   │ │ Oct 16  Client Payment   +$2,500  │ │
│ │ │                │   │ │ ...                                │ │
│ │ └────────────────┘   │ │ [View All →]                      │ │
│ └──────────────────────┘ └───────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**Components**:
- 4x `KPICard` (income, expenses, net, balance)
- 1x `SpendingChart` (donut chart)
- 1x `RecentTransactions` (table)

---

### 3.2 Transactions Page

**Wireframe**:
```
┌─────────────────────────────────────────────────────────────────┐
│ Transactions                                   [+ New Transaction]│
├─────────────────────────────────────────────────────────────────┤
│ [Search...] [Category ▼] [Date Range ▼] [Project ▼] [Export ⬇] │
├─────────────────────────────────────────────────────────────────┤
│ ┌───────────────────────────────────────────────────────────┐   │
│ │ Date ↓ │ Description         │ Category      │ Amount    │   │
│ ├────────┼─────────────────────┼───────────────┼───────────┤   │
│ │ Oct 17 │ Office Supplies     │ 📦 Supplies   │ -$45.00   │   │
│ │ Oct 16 │ Client Payment      │ 💰 Income     │ +$2,500.00│   │
│ │ ...    │ ...                 │ ...           │ ...       │   │
│ └───────────────────────────────────────────────────────────┘   │
│ Showing 1-50 of 256                        [← 1 2 3 4 5 →]      │
└─────────────────────────────────────────────────────────────────┘
```

**Components**:
- `SearchBar` (debounced 300ms)
- `TransactionFilters` (Category, Date, Project)
- `TransactionTable` (TanStack Table + Virtual Scrolling)
- `Pagination` (50 per page)

---

### 3.3 Design System (shadcn/ui)

**Colors**:
```
Primary:     hsl(222.2, 47.4%, 11.2%)  // Slate 950
Secondary:   hsl(210, 40%, 96.1%)      // Slate 50
Accent:      hsl(217.2, 91.2%, 59.8%)  // Blue 500

Success:     hsl(142.1, 76.2%, 36.3%)  // Green 600 (income)
Error:       hsl(0, 72.2%, 50.6%)      // Red 600 (expense)
```

**Typography**:
```
Font: Inter, -apple-system, BlinkMacSystemFont
Heading 1:   text-3xl (30px)
Body:        text-base (16px)
Small:       text-sm (14px)
```

**Spacing**: 4px base unit (space-1 to space-12)

---

## Implementation Checklist

### Week 1: Foundation (Days 1-5)

**Day 1-2: Project Setup**
- [ ] Initialize Next.js 14+ project with TypeScript
- [ ] Install shadcn/ui and configure Tailwind
- [ ] Set up Supabase integration (client + server)
- [ ] Configure environment variables (.env.local)
- [ ] Generate TypeScript types from Supabase (`supabase gen types`)

**Day 3: Authentication**
- [ ] Implement login page (`app/(auth)/login/page.tsx`)
- [ ] Implement signup page (`app/(auth)/signup/page.tsx`)
- [ ] Set up Supabase Auth middleware
- [ ] Test auth flow (login/logout/session persistence)

**Day 4-5: Dashboard Layout**
- [ ] Create dashboard layout (`app/(dashboard)/layout.tsx`)
- [ ] Implement Header with EntitySelector
- [ ] Implement Sidebar navigation
- [ ] Set up Zustand entity filter store
- [ ] Test entity filter persistence (localStorage)

---

### Week 2: Core Features (Days 6-10)

**Day 6-7: Transaction List**
- [ ] Fetch transactions server-side (combine personal + business tables)
- [ ] Implement TransactionTable with virtual scrolling
- [ ] Add sorting by date/amount/category
- [ ] Test with 256 transactions (performance <2s load)

**Day 8: Filtering & Search**
- [ ] Implement TransactionFilters (category, date, project)
- [ ] Add SearchBar with 300ms debounce
- [ ] Connect filters to React Query
- [ ] Test filter persistence via URL params

**Day 9-10: Charts & Dashboard**
- [ ] Implement SpendingChart (Recharts donut chart)
- [ ] Implement KPICard components (income, expenses, net, balance)
- [ ] Implement RecentTransactions widget
- [ ] Calculate KPI metrics server-side

---

### Week 3: Polish & Deployment (Days 11-15)

**Day 11: Mobile Responsiveness**
- [ ] Test on mobile (320px minimum)
- [ ] Implement mobile navigation (hamburger menu)
- [ ] Optimize charts for small screens
- [ ] Test touch interactions

**Day 12: Testing**
- [ ] Write unit tests for KPI calculations (Vitest, 100% coverage)
- [ ] Write component tests for TransactionTable (Testing Library)
- [ ] Write E2E test for auth flow (Playwright)
- [ ] Write E2E test for transaction viewing (Playwright)

**Day 13: Performance Optimization**
- [ ] Lazy load charts (`React.lazy()`)
- [ ] Optimize images with Next.js `<Image>`
- [ ] Run Lighthouse audit (target: <2s load, 90+ score)
- [ ] Test virtual scrolling with 10k rows

**Day 14: Deployment**
- [ ] Set up Vercel project
- [ ] Configure environment variables on Vercel
- [ ] Set up GitHub Actions CI/CD pipeline
- [ ] Deploy to production

**Day 15: User Acceptance Testing**
- [ ] Review with Harrison (user acceptance)
- [ ] Fix critical bugs
- [ ] Document any Phase 2 prerequisites
- [ ] Tag Phase 1 release

---

## Dependencies

### External Dependencies
- **Supabase Database**: Existing production database (gshsshaodoyttdxippwx)
  - Tables: `personal_transactions` (256 rows), `transactions` (1 row), `entities` (3 rows)
  - RLS policies must be configured before Phase 1
- **UpBank Sync**: External (n8n workflow) - display synced data only

### Technical Dependencies
- Node.js 18+
- npm or yarn
- Supabase CLI (for type generation)

---

## Success Criteria

### Functional Requirements ✅
- [ ] Users can view all 256+ transactions in unified list
- [ ] Entity filter works (Personal/MOKAI/MOK HOUSE)
- [ ] Search returns results in <200ms
- [ ] Category chart displays top 10 categories
- [ ] Project filter works for DiDi, Repco, Nintendo, etc.

### Performance Requirements ✅
- [ ] Initial page load <2 seconds (Lighthouse)
- [ ] Chart rendering <100ms (256 transactions)
- [ ] Virtual scrolling handles 10k+ rows without lag
- [ ] Mobile load time <3 seconds on 4G

### Testing Requirements ✅
- [ ] 100% test coverage for financial calculations
- [ ] E2E tests pass for auth and transaction viewing
- [ ] Component tests pass for all major components
- [ ] No TypeScript errors (`tsc --noEmit`)

### Deployment Requirements ✅
- [ ] Successfully deployed to Vercel
- [ ] CI/CD pipeline passing (GitHub Actions)
- [ ] Environment variables configured
- [ ] Production database connection verified

---

## Risks & Mitigation

### Risk 1: Performance with Large Datasets
**Probability**: Medium
**Impact**: High
**Mitigation**: Virtual scrolling (TanStack Virtual), pagination (50 per page), lazy loading

---

### Risk 2: Supabase RLS Misconfiguration
**Probability**: Low
**Impact**: Critical (data leak)
**Mitigation**: Comprehensive RLS testing, security audit before production

---

### Risk 3: Mobile Performance
**Probability**: Medium
**Impact**: Medium
**Mitigation**: Mobile-first design, responsive testing on real devices, Lighthouse mobile audit

---

## Next Phase Prerequisites

Before starting Phase 2 (Invoicing):
- [ ] Phase 1 deployed to production
- [ ] User acceptance testing complete
- [ ] No critical bugs
- [ ] Performance benchmarks met (<2s load, <100ms charts)

---

**Phase Owner**: Scrum Master (SM Agent)
**Estimated Effort**: 120 hours (3 weeks × 40 hours)
**Status**: Ready for Sprint Planning
