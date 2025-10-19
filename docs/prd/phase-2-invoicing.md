---
date: "2025-10-17"
phase: 2
duration: "3 weeks"
status: "Ready for Implementation"
priority: "Must Have"
dependencies: ["Phase 1 Complete"]
---

# Phase 2: Invoicing & Cash Flow
## Implementation Guide

---

## Phase Overview

Add comprehensive invoice management (receivables/payables) and cash flow visualization. This phase builds on Phase 1's transaction foundation to enable professional invoicing, payment tracking, and cash flow forecasting.

**Duration**: 3 weeks
- Week 1: Invoice CRUD operations
- Week 2: Payment tracking, PDF generation
- Week 3: Cash flow dashboard, forecasting

**Success Criteria**: Users can create/manage invoices, track payments, generate PDFs, and visualize cash flow trends.

---

## User Stories from PRD

### Epic 2.1: Invoice Management

#### Story 2.1.1: Invoice List View ⭐ CRITICAL
**As a** business owner
**I want to** see all invoices with status indicators
**So that** I can track receivables and payables

**Acceptance Criteria**:
- [ ] Display invoice number, contact, amount, due date, status
- [ ] Color-coded status (draft/sent/paid/overdue)
- [ ] Sort by date, amount, status
- [ ] Filter by entity, contact, status, date range

**Priority**: Must Have
**Dependencies**: None

---

#### Story 2.1.2: Create Invoice ⭐ CRITICAL
**As a** business owner
**I want to** create new invoices
**So that** I can bill customers

**Acceptance Criteria**:
- [ ] Form validation (contact, amount, due date required)
- [ ] Line item support with descriptions
- [ ] GST calculation (10% Australian tax)
- [ ] Auto-increment invoice numbers per entity
- [ ] Save as draft or mark sent

**Priority**: Must Have
**Dependencies**: Story 2.1.1

---

#### Story 2.1.3: Invoice Payment Tracking
**As a** business owner
**I want to** mark invoices as paid
**So that** I can track cash collection

**Acceptance Criteria**:
- [ ] Record payment date and method
- [ ] Link to bank transaction if applicable
- [ ] Calculate days to payment (metrics)
- [ ] Update account balances

**Priority**: Must Have
**Dependencies**: Stories 2.1.1, 2.1.2

---

#### Story 2.1.4: Generate Invoice PDF
**As a** business owner
**I want to** download professional invoice PDFs
**So that** I can send invoices to clients

**Acceptance Criteria**:
- [ ] Professional template with logo/branding
- [ ] Include all invoice details + line items
- [ ] Show GST breakdown
- [ ] Include payment instructions

**Priority**: Should Have
**Dependencies**: Story 2.1.2

---

### Epic 2.2: Cash Flow Dashboard

#### Story 2.2.1: Cash Flow Timeline ⭐ CRITICAL
**As a** business owner
**I want to** visualize cash flow over time
**So that** I can plan expenses and investments

**Acceptance Criteria**:
- [ ] Waterfall chart showing daily/weekly/monthly cash flow
- [ ] Separate bars for income vs expenses
- [ ] Running balance line overlay
- [ ] Zoom to specific time periods

**Priority**: Must Have
**Dependencies**: Story 2.1.1

---

#### Story 2.2.2: Cash Flow Forecasting
**As a** business owner
**I want to** see predicted future cash flow
**So that** I can avoid liquidity issues

**Acceptance Criteria**:
- [ ] Use ML predictions from cash_flow_forecasts table
- [ ] Show confidence intervals
- [ ] Include recurring transactions
- [ ] Highlight predicted low-balance periods

**Priority**: Should Have
**Dependencies**: Story 2.2.1

---

#### Story 2.2.3: Overdue Invoice Alerts
**As a** business owner
**I want to** be notified of overdue invoices
**So that** I can follow up on payments

**Acceptance Criteria**:
- [ ] Dashboard alert badge showing count
- [ ] List of overdue invoices with days overdue
- [ ] One-click to send reminder email (future)
- [ ] Track reminder history (future)

**Priority**: Should Have
**Dependencies**: Story 2.1.1

---

## Technical Requirements

### Route Structure

```
app/(dashboard)/invoices/
├── page.tsx                    # Invoice list (Server Component)
├── new/page.tsx                # Create invoice form
├── [id]/
│   ├── page.tsx                # Invoice detail view
│   └── edit/page.tsx           # Edit invoice
└── components/
    ├── InvoiceCard.tsx         # Invoice display card
    ├── InvoiceForm.tsx         # React Hook Form + Zod
    ├── InvoiceStatusBadge.tsx  # Status indicator
    └── LineItemsField.tsx      # Dynamic line items

app/api/invoices/
├── route.ts                    # POST - Create invoice
└── [id]/
    ├── route.ts                # GET, PATCH, DELETE
    └── pdf/route.ts            # POST - Generate PDF
```

---

### Data Fetching

**Invoice List (Server Component)**:

```typescript
// app/(dashboard)/invoices/page.tsx
import { createClient } from '@/lib/supabase/server'

export default async function InvoicesPage() {
  const supabase = await createClient()

  const { data: invoices } = await supabase
    .from('invoices')
    .select(`
      *,
      contact:contacts(id, name, email),
      entity:entities(id, name),
      line_items:invoice_line_items(*)
    `)
    .order('issue_date', { ascending: false })

  return <InvoiceGrid invoices={invoices} />
}
```

---

### Invoice Form (React Hook Form + Zod)

```typescript
// lib/validations/invoice.ts
import { z } from 'zod'

export const invoiceSchema = z.object({
  entity_id: z.string().uuid(),
  contact_id: z.string().uuid(),
  issue_date: z.date(),
  due_date: z.date(),
  line_items: z.array(z.object({
    description: z.string().min(1),
    amount: z.number().positive(), // In cents
  })).min(1, 'At least one line item required'),
  notes: z.string().optional(),
}).refine((data) => data.due_date >= data.issue_date, {
  message: 'Due date must be after issue date',
  path: ['due_date'],
})
```

---

### GST Calculation

```typescript
// lib/calculations/gst.ts
import Decimal from 'decimal.js'

export function calculateGST(subtotalCents: number): {
  subtotal: number
  gst: number
  total: number
} {
  const subtotal = new Decimal(subtotalCents).div(100)
  const gst = subtotal.mul(0.10) // 10% Australian GST
  const total = subtotal.plus(gst)

  return {
    subtotal: subtotalCents,
    gst: Math.round(gst.mul(100).toNumber()),
    total: Math.round(total.mul(100).toNumber()),
  }
}
```

---

### PDF Generation (@react-pdf/renderer)

```typescript
// app/api/invoices/[id]/pdf/route.ts
import { Document, Page, Text, View, StyleSheet } from '@react-pdf/renderer'
import { renderToStream } from '@react-pdf/renderer'

export async function POST(
  request: Request,
  { params }: { params: { id: string } }
) {
  const invoice = await getInvoice(params.id)

  const doc = (
    <Document>
      <Page size="A4" style={styles.page}>
        <View style={styles.header}>
          <Text style={styles.title}>INVOICE</Text>
          <Text>#{invoice.invoice_number}</Text>
        </View>

        <View style={styles.details}>
          <Text>To: {invoice.contact.name}</Text>
          <Text>Date: {formatDate(invoice.issue_date)}</Text>
          <Text>Due: {formatDate(invoice.due_date)}</Text>
        </View>

        {invoice.line_items.map((item, i) => (
          <View key={i} style={styles.lineItem}>
            <Text>{item.description}</Text>
            <Text>{formatCurrency(item.amount)}</Text>
          </View>
        ))}

        <View style={styles.totals}>
          <Text>Subtotal: {formatCurrency(invoice.subtotal)}</Text>
          <Text>GST (10%): {formatCurrency(invoice.gst_amount)}</Text>
          <Text style={styles.total}>Total: {formatCurrency(invoice.total)}</Text>
        </View>
      </Page>
    </Document>
  )

  const stream = await renderToStream(doc)

  return new Response(stream, {
    headers: {
      'Content-Type': 'application/pdf',
      'Content-Disposition': `attachment; filename="invoice-${invoice.invoice_number}.pdf"`,
    },
  })
}
```

---

## UI Specifications

### Invoice Card (Frontend Spec Section 3.3)

```
┌──────────────────┐
│ INV-001          │
│ Acme Corp        │
│ $2,500.00        │
│ ✅ Paid          │  <- Green border-l-4
│ Due: Oct 15      │
│ [View] [PDF]     │
└──────────────────┘

┌──────────────────┐
│ INV-002          │
│ Tech Ltd         │
│ $1,200.00        │
│ 🚨 Overdue (5d)  │  <- Red border-l-4, pulsing
│ Due: Oct 10      │
│ [View] [PDF]     │
└──────────────────┘
```

**Status Colors**:
- Paid: `border-l-4 border-green-600`
- Overdue: `border-l-4 border-red-600 animate-pulse`
- Pending: `border-l-4 border-amber-500`
- Draft: `border-l-4 border-slate-500`

---

### Cash Flow Chart (Recharts Waterfall)

```typescript
// components/charts/WaterfallChart.tsx
import { BarChart, Bar, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

export function WaterfallChart({ data }: { data: CashFlowData[] }) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data}>
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="income" fill="hsl(142.1, 76.2%, 36.3%)" />
        <Bar dataKey="expenses" fill="hsl(0, 72.2%, 50.6%)" />
        <Line type="monotone" dataKey="balance" stroke="hsl(217.2, 91.2%, 59.8%)" />
      </BarChart>
    </ResponsiveContainer>
  )
}
```

---

## Implementation Checklist

### Week 1: Invoice CRUD (Days 1-5)

- [ ] Create invoice schema (Zod validation)
- [ ] Implement invoice list page (Server Component)
- [ ] Implement invoice creation form (React Hook Form)
- [ ] Add GST calculation (10% Australian)
- [ ] Implement auto-increment invoice numbers per entity
- [ ] Test invoice creation with line items

---

### Week 2: Payment Tracking & PDF (Days 6-10)

- [ ] Implement invoice payment tracking (mark as paid)
- [ ] Link payments to bank transactions (optional)
- [ ] Calculate days to payment metrics
- [ ] Implement PDF generation (@react-pdf/renderer)
- [ ] Design invoice PDF template (professional)
- [ ] Add logo placeholders (MOKAI, MOK HOUSE)
- [ ] Test PDF download

---

### Week 3: Cash Flow Dashboard (Days 11-15)

- [ ] Implement cash flow timeline (waterfall chart)
- [ ] Calculate daily/weekly/monthly inflows and outflows
- [ ] Add running balance line overlay
- [ ] Implement cash flow forecasting (ML predictions)
- [ ] Display overdue invoice alerts on dashboard
- [ ] Test cash flow accuracy against manual calculations
- [ ] Deploy Phase 2 to production

---

## Dependencies

### From Phase 1
- [ ] Dashboard layout and navigation
- [ ] Entity filter (Zustand store)
- [ ] Supabase integration
- [ ] Authentication

### External
- **Logos**: MOKAI and MOK HOUSE logos (SVG or PNG) for invoice PDFs
- **Supabase Tables**: `invoices`, `invoice_line_items`, `contacts`

---

## Success Criteria

### Functional ✅
- [ ] Users can create invoices with line items
- [ ] GST calculated correctly (10%)
- [ ] Invoice PDFs download successfully
- [ ] Overdue invoices show alerts on dashboard
- [ ] Cash flow chart visualizes income/expenses

### Performance ✅
- [ ] Invoice list loads <2 seconds
- [ ] PDF generation <2 seconds
- [ ] Cash flow chart renders <100ms

### Testing ✅
- [ ] 100% test coverage for GST calculations
- [ ] E2E test for invoice creation
- [ ] Component test for invoice form validation

---

## Next Phase Prerequisites

Before Phase 3 (Budgeting):
- [ ] Invoice system fully functional
- [ ] PDF generation tested
- [ ] Cash flow chart validated
- [ ] No critical bugs

---

**Phase Owner**: Scrum Master (SM Agent)
**Estimated Effort**: 120 hours (3 weeks × 40 hours)
**Status**: Ready for Sprint Planning
