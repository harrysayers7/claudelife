# Next.js App Structure & Routing

## App Router File Structure

```
app/
├── layout.tsx                    # Root layout (auth, entity context)
├── page.tsx                      # Root redirect → /dashboard
├── login/
│   └── page.tsx                  # Login page (unprotected)
├── dashboard/
│   └── page.tsx                  # Dashboard overview (Server Component)
├── transactions/
│   ├── page.tsx                  # Transaction list (mixed SSR/CSR)
│   └── [id]/
│       └── page.tsx              # Transaction detail (Server Component)
├── invoices/
│   ├── page.tsx                  # Invoice list
│   ├── new/
│   │   └── page.tsx              # Create invoice
│   └── [id]/
│       ├── page.tsx              # Invoice detail
│       └── edit/
│           └── page.tsx          # Edit invoice
├── reports/
│   ├── bas/
│   │   └── page.tsx              # BAS report generator
│   ├── income-statement/
│   │   └── page.tsx              # P&L report
│   └── export/
│       └── page.tsx              # Data export
└── settings/
    ├── page.tsx                  # User preferences
    ├── entities/
    │   └── page.tsx              # Entity management
    ├── contacts/
    │   ├── page.tsx              # Contact list
    │   └── [id]/
    │       └── page.tsx          # Contact detail
    └── accounts/
        └── page.tsx              # Chart of accounts
```

## API Routes

```
app/api/
├── invoices/
│   ├── [id]/
│   │   └── pdf/
│   │       └── route.ts          # GET: Generate invoice PDF
│   └── route.ts                  # POST: Create invoice
├── reports/
│   ├── bas/
│   │   └── route.ts              # POST: Generate BAS
│   ├── income-statement/
│   │   └── route.ts              # POST: Generate P&L
│   └── export/
│       └── route.ts              # POST: Export CSV/Excel
└── webhooks/
    └── upbank/
        └── route.ts              # POST: UpBank sync webhook
```

## Server vs Client Components

**Server Components (Default)**:
- Dashboard page (data fetching)
- Transaction list initial render
- Invoice list/detail pages
- Report pages

**Client Components (Interactive)**:
- Charts (Recharts)
- Forms (React Hook Form)
- Filters (multi-select, date pickers)
- Modals and dialogs

## Routing Patterns

**Protected Routes** (middleware.ts):
- All routes except `/login` require authentication
- Middleware checks Supabase session
- Unauthenticated users → redirect to `/login`

**Entity Context**:
- Entity selector in root layout
- Context provider wraps all pages
- Entity change triggers data refresh

## Loading States

```typescript
// loading.tsx pattern for instant feedback
export default function Loading() {
  return <DashboardSkeleton />
}
```

## Error Boundaries

```typescript
// error.tsx pattern for graceful errors
'use client'
export default function Error({ error, reset }) {
  return <ErrorDisplay error={error} retry={reset} />
}
```
