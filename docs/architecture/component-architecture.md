# React Component Architecture

## Component Hierarchy

```
App (Root Layout)
├── EntityProvider (Context)
├── Header
│   ├── Logo
│   ├── EntitySelector
│   └── UserMenu
├── Sidebar (Desktop)
│   └── NavMenu
├── MobileMenu (Mobile)
│   └── NavMenu
└── Page Content
    ├── Server Components (Data Fetching)
    └── Client Components (Interactivity)
```

## Server Components (Default)

**Dashboard Page**:
- Fetches KPI data on server
- Renders initial HTML
- Fast Time to First Byte (TTFB)

**Transaction List Initial Render**:
- First page of transactions from Supabase
- Server-side filtering applied
- Hydrates with client interactivity

**Invoice Detail Page**:
- Full invoice data fetched server-side
- Static content rendered
- PDF generation on demand

## Client Components

**Charts** ('use client'):
```typescript
'use client'
import { LineChart } from 'recharts'

export function TrendChart({ data }) {
  return <LineChart data={data} />
}
```

**Forms** ('use client'):
```typescript
'use client'
import { useForm } from 'react-hook-form'

export function InvoiceForm() {
  const form = useForm()
  // Interactive form logic
}
```

**Filters** ('use client'):
```typescript
'use client'
import { useState } from 'react'

export function TransactionFilters({ onFilter }) {
  const [filters, setFilters] = useState({})
  // Interactive filtering
}
```

## Component Patterns

**Compound Components** (shadcn/ui):
```typescript
<Card>
  <CardHeader>
    <CardTitle>Revenue</CardTitle>
  </CardHeader>
  <CardContent>
    <KpiValue value={revenue} />
  </CardContent>
</Card>
```

**Render Props**:
```typescript
<DataTable
  data={transactions}
  renderRow={(transaction) => (
    <TransactionRow transaction={transaction} />
  )}
/>
```

**Higher-Order Components**:
```typescript
export function withAuth(Component) {
  return async function AuthenticatedComponent(props) {
    const session = await getSession()
    if (!session) redirect('/login')
    return <Component {...props} />
  }
}
```
