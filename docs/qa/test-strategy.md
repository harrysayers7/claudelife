# SAYERS Finance Dashboard - Test Strategy

<!-- Powered by BMAD™ Core -->

**Project**: SAYERS Finance Dashboard
**Version**: 1.0
**Date**: 2025-10-03
**QA Agent**: BMad Method QA
**Status**: Ready for Implementation

---

## Executive Summary

This comprehensive test strategy ensures the SAYERS Finance Dashboard meets **NFR5's 100% financial accuracy requirement** and all other quality gates before production deployment. The strategy implements a robust test pyramid with emphasis on financial calculation correctness, multi-entity data isolation, and Australian tax compliance.

### Testing Philosophy

**Quality Gates**:
- **Financial Calculations**: 100% accuracy (non-negotiable)
- **Security (RLS)**: Zero data leakage between entities
- **Performance**: <2s page loads, <100ms API responses
- **Accessibility**: WCAG AA compliance
- **Tax Compliance**: ATO-aligned BAS/GST calculations

**Test Pyramid Distribution**:
```
      /\
     /E2E\      ← 5% (Critical user journeys)
    /------\
   /  INT   \   ← 20% (Component integration, API)
  /----------\
 /    UNIT    \ ← 75% (Calculations, utilities, pure functions)
/--------------\
```

### Coverage Targets

| Category | Coverage Target | Rationale |
|----------|----------------|-----------|
| **Financial Calculations** | 100% | NFR5 requirement, tax compliance |
| **Utility Functions** | 100% | Core business logic reliability |
| **React Components** | ≥80% | UI reliability, accessibility |
| **Integration Tests** | Critical paths | User journey validation |
| **E2E Tests** | 5 core workflows | Production readiness |

---

## 1. Testing Philosophy

### Test Pyramid Strategy

#### Unit Tests (75% of total tests)

**Purpose**: Validate individual functions in isolation
**Tool**: Vitest
**Coverage Goals**:
- Financial calculations: 100%
- Utility functions: 100%
- Pure functions: 95%+

**Characteristics**:
- Fast execution (<1ms per test)
- No external dependencies
- Deterministic results
- Run on every commit

**Test Ratio**: ~300-400 unit tests for 41 user stories

#### Integration Tests (20% of total tests)

**Purpose**: Validate component interactions and API integrations
**Tools**: Vitest + React Testing Library + Supabase Test Client
**Coverage Goals**:
- Form workflows: All critical forms
- Supabase queries: RLS enforcement
- State management: Entity switching, form state

**Characteristics**:
- Use Supabase local development
- Mock external APIs (UpBank, MindsDB)
- Reset database between tests
- Run before merging PRs

**Test Ratio**: ~80-100 integration tests

#### End-to-End Tests (5% of total tests)

**Purpose**: Validate complete user journeys in production-like environment
**Tool**: Playwright
**Coverage Goals**: 5 critical journeys

**Characteristics**:
- Run against staging environment
- Use seed data
- Test multi-entity workflows
- Visual regression (optional)
- Run before production deployment

**Test Ratio**: ~20-25 E2E tests

---

## 2. Test Categories

### A. Unit Tests (Vitest)

#### Financial Calculation Tests

**Location**: `/lib/__tests__/calculations.test.ts`

```typescript
describe('GST Calculations', () => {
  it('calculates 10% GST correctly for whole dollars', () => {
    expect(calculateGST(100, 'exclusive')).toBe(10)
    expect(calculateGST(1000, 'exclusive')).toBe(100)
  })

  it('handles rounding correctly (banker\'s rounding)', () => {
    // 0.005 rounds to 0.00 (even)
    expect(calculateGST(0.05, 'exclusive')).toBe(0.00)
    // 0.015 rounds to 0.02 (even)
    expect(calculateGST(0.15, 'exclusive')).toBe(0.02)
  })

  it('calculates GST-inclusive prices', () => {
    const result = calculateGSTInclusive(110)
    expect(result.net).toBe(100)
    expect(result.gst).toBe(10)
  })

  it('calculates GST-exclusive prices', () => {
    const result = calculateGSTExclusive(100)
    expect(result.net).toBe(100)
    expect(result.gst).toBe(10)
    expect(result.total).toBe(110)
  })

  it('handles zero amounts', () => {
    expect(calculateGST(0, 'exclusive')).toBe(0)
  })

  it('handles negative amounts (refunds)', () => {
    expect(calculateGST(-100, 'exclusive')).toBe(-10)
  })

  it('matches ATO examples exactly', () => {
    // ATO Example 1: $100 + GST = $110
    expect(calculateGST(100, 'exclusive')).toBe(10)
    expect(calculateTotal(100, 10)).toBe(110)

    // ATO Example 2: $110 inc GST → $100 ex GST
    const result = calculateGSTInclusive(110)
    expect(result.net).toBe(100)
    expect(result.gst).toBe(10)
  })
})

describe('BAS Statement Generation', () => {
  it('calculates G1 (Total Sales) correctly', () => {
    const transactions = [
      { type: 'sale', net: 1000, gst: 100 },
      { type: 'sale', net: 500, gst: 50 }
    ]
    expect(calculateBASField('G1', transactions)).toBe(1500)
  })

  it('calculates 1A (GST on Sales) correctly', () => {
    const transactions = [
      { type: 'sale', net: 1000, gst: 100 },
      { type: 'sale', net: 500, gst: 50 }
    ]
    expect(calculateBASField('1A', transactions)).toBe(150)
  })

  it('calculates 1B (GST on Purchases) correctly', () => {
    const transactions = [
      { type: 'purchase', net: 500, gst: 50 },
      { type: 'purchase', net: 300, gst: 30 }
    ]
    expect(calculateBASField('1B', transactions)).toBe(80)
  })

  it('calculates net GST payable/refundable', () => {
    const transactions = [
      { type: 'sale', net: 1000, gst: 100 },
      { type: 'purchase', net: 500, gst: 50 }
    ]
    const bas = calculateBAS(transactions)
    expect(bas.net).toBe(50) // GST payable
  })

  it('handles multiple entities separately', () => {
    const mokaiTx = [{ entity_id: 'mokai', type: 'sale', net: 1000, gst: 100 }]
    const mokHouseTx = [{ entity_id: 'mokhouse', type: 'sale', net: 500, gst: 50 }]

    expect(calculateBAS(mokaiTx, 'mokai').G1).toBe(1000)
    expect(calculateBAS(mokHouseTx, 'mokhouse').G1).toBe(500)
  })

  it('filters by date range correctly', () => {
    const transactions = [
      { date: '2025-01-15', type: 'sale', net: 1000, gst: 100 },
      { date: '2025-02-15', type: 'sale', net: 500, gst: 50 }
    ]
    const result = calculateBAS(
      transactions,
      'mokai',
      '2025-01-01',
      '2025-01-31'
    )
    expect(result.G1).toBe(1000) // Only January transaction
  })
})

describe('Invoice Totals', () => {
  it('sums line items correctly', () => {
    const lineItems = [
      { qty: 1, price: 100, gst: true },
      { qty: 2, price: 50, gst: true }
    ]
    expect(calculateInvoiceSubtotal(lineItems)).toBe(200)
  })

  it('applies GST to each line', () => {
    const lineItems = [
      { qty: 1, price: 100, gst: true },
      { qty: 2, price: 50, gst: false }
    ]
    const result = calculateInvoiceTotals(lineItems)
    expect(result.subtotal).toBe(200)
    expect(result.gst).toBe(10) // Only first line
    expect(result.total).toBe(210)
  })

  it('calculates invoice total', () => {
    const lineItems = [
      { qty: 10, price: 150, gst: true }
    ]
    const result = calculateInvoiceTotals(lineItems)
    expect(result.subtotal).toBe(1500)
    expect(result.gst).toBe(150)
    expect(result.total).toBe(1650)
  })

  it('handles discounts', () => {
    const lineItems = [
      { qty: 1, price: 100, gst: true }
    ]
    const discount = 10 // $10 discount
    const result = calculateInvoiceTotals(lineItems, discount)
    expect(result.subtotal).toBe(90)
    expect(result.gst).toBe(9)
    expect(result.total).toBe(99)
  })

  it('validates against known invoices', () => {
    // Real invoice from Supabase: INV-001
    const lineItems = [
      { qty: 1, price: 1500, gst: true },
      { qty: 40, price: 75, gst: true }
    ]
    const result = calculateInvoiceTotals(lineItems)
    expect(result.subtotal).toBe(4500)
    expect(result.gst).toBe(450)
    expect(result.total).toBe(4950)
  })
})
```

#### Utility Function Tests

**Location**: `/lib/__tests__/utils.test.ts`

```typescript
describe('Date Formatting', () => {
  it('formats date in Australian format (DD/MM/YYYY)', () => {
    const date = new Date('2025-01-15')
    expect(formatDate(date, 'DD/MM/YYYY')).toBe('15/01/2025')
  })

  it('handles timezone correctly (Australia/Sydney)', () => {
    const date = new Date('2025-01-15T00:00:00Z')
    expect(formatDate(date, 'DD/MM/YYYY', 'Australia/Sydney')).toBe('15/01/2025')
  })
})

describe('Currency Formatting', () => {
  it('formats currency with dollar sign and commas', () => {
    expect(formatCurrency(1234.56)).toBe('$1,234.56')
    expect(formatCurrency(1000)).toBe('$1,000.00')
  })

  it('handles negative amounts with minus sign', () => {
    expect(formatCurrency(-1234.56)).toBe('-$1,234.56')
  })

  it('rounds to 2 decimal places', () => {
    expect(formatCurrency(123.456)).toBe('$123.46')
    expect(formatCurrency(123.454)).toBe('$123.45')
  })
})

describe('Entity Data Isolation Helpers', () => {
  it('filters transactions by entity ID', () => {
    const transactions = [
      { id: 1, entity_id: 'mokai' },
      { id: 2, entity_id: 'mokhouse' },
      { id: 3, entity_id: 'mokai' }
    ]
    const filtered = filterByEntity(transactions, 'mokai')
    expect(filtered).toHaveLength(2)
    expect(filtered.every(t => t.entity_id === 'mokai')).toBe(true)
  })
})

describe('ML Confidence Interpretation', () => {
  it('categorizes confidence scores correctly', () => {
    expect(getConfidenceLevel(0.95)).toBe('high')
    expect(getConfidenceLevel(0.85)).toBe('medium')
    expect(getConfidenceLevel(0.65)).toBe('low')
  })

  it('returns correct badge color', () => {
    expect(getConfidenceBadgeColor(0.95)).toBe('green')
    expect(getConfidenceBadgeColor(0.85)).toBe('amber')
    expect(getConfidenceBadgeColor(0.65)).toBe('red')
  })
})
```

#### React Component Tests

**Location**: `/components/__tests__/KPICard.test.tsx`

```typescript
import { render, screen } from '@testing-library/react'
import { KPICard } from '@/components/KPICard'

describe('KPICard', () => {
  it('renders title and value correctly', () => {
    render(
      <KPICard
        title="Revenue"
        value="$12,345.00"
      />
    )
    expect(screen.getByText('Revenue')).toBeInTheDocument()
    expect(screen.getByText('$12,345.00')).toBeInTheDocument()
  })

  it('displays change indicator with correct color', () => {
    render(
      <KPICard
        title="Revenue"
        value="$12,345.00"
        change={{ value: 15, period: 'vs last month' }}
      />
    )
    const badge = screen.getByText('+15%')
    expect(badge).toHaveClass('text-green-600') // Positive change
  })

  it('shows loading skeleton when loading prop is true', () => {
    render(
      <KPICard
        title="Revenue"
        value="$12,345.00"
        loading={true}
      />
    )
    expect(screen.getByTestId('skeleton-loader')).toBeInTheDocument()
  })
})

describe('MLConfidenceIndicator', () => {
  it('shows high confidence badge for ≥0.9', () => {
    render(<MLConfidenceIndicator confidence={0.95} />)
    const badge = screen.getByText('High')
    expect(badge).toHaveClass('bg-green-100')
  })

  it('shows medium confidence badge for 0.7-0.89', () => {
    render(<MLConfidenceIndicator confidence={0.85} />)
    const badge = screen.getByText('Medium')
    expect(badge).toHaveClass('bg-amber-100')
  })

  it('shows low confidence badge for <0.7', () => {
    render(<MLConfidenceIndicator confidence={0.65} />)
    const badge = screen.getByText('Low')
    expect(badge).toHaveClass('bg-red-100')
  })

  it('has accessible aria-label', () => {
    render(<MLConfidenceIndicator confidence={0.95} />)
    expect(screen.getByLabelText('High confidence: 0.95')).toBeInTheDocument()
  })
})
```

### B. Integration Tests (Vitest + React Testing Library)

#### Form Workflow Tests

**Location**: `/app/__tests__/invoices/create.test.tsx`

```typescript
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { InvoiceCreatePage } from '@/app/invoices/new/page'
import { mockSupabase } from '@/test/mocks/supabase'

describe('Invoice Creation Form', () => {
  it('loads client list from Supabase', async () => {
    mockSupabase.from.mockResolvedValue({
      data: [
        { id: 1, name: 'Acme Corp' },
        { id: 2, name: 'Tech Pty' }
      ],
      error: null
    })

    render(<InvoiceCreatePage />)

    await waitFor(() => {
      expect(screen.getByText('Acme Corp')).toBeInTheDocument()
    })
  })

  it('validates required fields', async () => {
    render(<InvoiceCreatePage />)
    const user = userEvent.setup()

    const submitButton = screen.getByText('Save & Send')
    await user.click(submitButton)

    expect(await screen.findByText('Please select a client')).toBeInTheDocument()
    expect(await screen.findByText('At least one line item required')).toBeInTheDocument()
  })

  it('adds/removes line items', async () => {
    render(<InvoiceCreatePage />)
    const user = userEvent.setup()

    expect(screen.getAllByRole('row')).toHaveLength(1) // Header + 1 default row

    const addButton = screen.getByText('Add Line Item')
    await user.click(addButton)

    expect(screen.getAllByRole('row')).toHaveLength(2)

    const deleteButton = screen.getAllByLabelText('Delete line item')[0]
    await user.click(deleteButton)

    expect(screen.getAllByRole('row')).toHaveLength(1)
  })

  it('calculates totals in real-time', async () => {
    render(<InvoiceCreatePage />)
    const user = userEvent.setup()

    const qtyInput = screen.getByLabelText('Quantity')
    const priceInput = screen.getByLabelText('Unit Price')

    await user.type(qtyInput, '10')
    await user.type(priceInput, '150')

    await waitFor(() => {
      expect(screen.getByText('Subtotal: $1,500.00')).toBeInTheDocument()
      expect(screen.getByText('GST: $150.00')).toBeInTheDocument()
      expect(screen.getByText('Total: $1,650.00')).toBeInTheDocument()
    })
  })

  it('saves draft to Supabase', async () => {
    const mockInsert = vi.fn().mockResolvedValue({ data: { id: 1 }, error: null })
    mockSupabase.from.mockReturnValue({ insert: mockInsert })

    render(<InvoiceCreatePage />)
    const user = userEvent.setup()

    // Fill form
    await user.selectOptions(screen.getByLabelText('Client'), 'Acme Corp')
    await user.type(screen.getByLabelText('Description'), 'Web Design')
    await user.type(screen.getByLabelText('Quantity'), '1')
    await user.type(screen.getByLabelText('Unit Price'), '1500')

    const draftButton = screen.getByText('Save as Draft')
    await user.click(draftButton)

    await waitFor(() => {
      expect(mockInsert).toHaveBeenCalledWith(
        expect.objectContaining({
          status: 'draft',
          line_items: expect.arrayContaining([
            expect.objectContaining({ description: 'Web Design' })
          ])
        })
      )
    })
  })

  it('submits final invoice', async () => {
    const mockInsert = vi.fn().mockResolvedValue({ data: { id: 1 }, error: null })
    mockSupabase.from.mockReturnValue({ insert: mockInsert })

    render(<InvoiceCreatePage />)
    const user = userEvent.setup()

    // Fill form
    await user.selectOptions(screen.getByLabelText('Client'), 'Acme Corp')
    await user.type(screen.getByLabelText('Description'), 'Web Design')
    await user.type(screen.getByLabelText('Quantity'), '1')
    await user.type(screen.getByLabelText('Unit Price'), '1500')

    const sendButton = screen.getByText('Save & Send')
    await user.click(sendButton)

    await waitFor(() => {
      expect(mockInsert).toHaveBeenCalledWith(
        expect.objectContaining({ status: 'sent' })
      )
      expect(screen.getByText('Invoice sent successfully')).toBeInTheDocument()
    })
  })

  it('handles API errors gracefully', async () => {
    mockSupabase.from.mockResolvedValue({
      data: null,
      error: { message: 'Database error' }
    })

    render(<InvoiceCreatePage />)
    const user = userEvent.setup()

    const sendButton = screen.getByText('Save & Send')
    await user.click(sendButton)

    await waitFor(() => {
      expect(screen.getByText('Failed to save invoice')).toBeInTheDocument()
    })
  })
})
```

#### Transaction Categorization Tests

**Location**: `/app/__tests__/transactions/categorize.test.tsx`

```typescript
describe('Transaction Categorization', () => {
  it('displays ML prediction', async () => {
    mockSupabase.from.mockResolvedValue({
      data: [{
        id: 1,
        description: 'Office Works',
        ai_category: 'Office Supplies',
        ai_confidence: 0.95
      }],
      error: null
    })

    render(<TransactionListPage />)

    await waitFor(() => {
      expect(screen.getByText('Office Supplies')).toBeInTheDocument()
      expect(screen.getByText('High')).toBeInTheDocument()
    })
  })

  it('shows confidence score', async () => {
    mockSupabase.from.mockResolvedValue({
      data: [{
        id: 1,
        ai_confidence: 0.82
      }],
      error: null
    })

    render(<TransactionListPage />)

    await waitFor(() => {
      expect(screen.getByLabelText('Medium confidence: 0.82')).toBeInTheDocument()
    })
  })

  it('allows manual override', async () => {
    const mockUpdate = vi.fn().mockResolvedValue({ data: {}, error: null })
    mockSupabase.from.mockReturnValue({ update: mockUpdate })

    render(<TransactionListPage />)
    const user = userEvent.setup()

    const categoryCell = screen.getByText('Office Supplies')
    await user.dblClick(categoryCell)

    const dropdown = screen.getByRole('combobox')
    await user.selectOptions(dropdown, 'Groceries')

    await waitFor(() => {
      expect(mockUpdate).toHaveBeenCalledWith(
        expect.objectContaining({
          category: 'Groceries',
          ai_category_override: true
        })
      )
    })
  })

  it('saves to Supabase with RLS', async () => {
    const mockUpdate = vi.fn().mockResolvedValue({ data: {}, error: null })
    mockSupabase.from.mockReturnValue({ update: mockUpdate })

    render(<TransactionListPage entityId="mokai" />)
    const user = userEvent.setup()

    // Override category
    const categoryCell = screen.getByText('Office Supplies')
    await user.dblClick(categoryCell)
    await user.selectOptions(screen.getByRole('combobox'), 'Groceries')

    await waitFor(() => {
      expect(mockUpdate).toHaveBeenCalledWith(
        expect.objectContaining({ entity_id: 'mokai' })
      )
    })
  })

  it('updates UI optimistically', async () => {
    mockSupabase.from.mockReturnValue({
      update: vi.fn().mockImplementation(() => {
        // Simulate slow API
        return new Promise(resolve => setTimeout(() => resolve({ data: {}, error: null }), 500))
      })
    })

    render(<TransactionListPage />)
    const user = userEvent.setup()

    const categoryCell = screen.getByText('Office Supplies')
    await user.dblClick(categoryCell)
    await user.selectOptions(screen.getByRole('combobox'), 'Groceries')

    // Should update immediately (optimistic)
    expect(screen.getByText('Groceries')).toBeInTheDocument()
  })

  it('handles concurrent edits', async () => {
    // Test that concurrent updates don't cause race conditions
    const mockUpdate = vi.fn().mockResolvedValue({ data: {}, error: null })
    mockSupabase.from.mockReturnValue({ update: mockUpdate })

    render(<TransactionListPage />)
    const user = userEvent.setup()

    // Trigger two updates quickly
    const category1 = screen.getAllByText('Office Supplies')[0]
    const category2 = screen.getAllByText('Office Supplies')[1]

    await user.dblClick(category1)
    await user.selectOptions(screen.getAllByRole('combobox')[0], 'Groceries')

    await user.dblClick(category2)
    await user.selectOptions(screen.getAllByRole('combobox')[1], 'Rent')

    await waitFor(() => {
      expect(mockUpdate).toHaveBeenCalledTimes(2)
    })
  })
})
```

#### Supabase Integration Tests

**Location**: `/lib/__tests__/supabase/rls.test.ts`

```typescript
import { createClient } from '@/lib/supabase'

describe('Multi-Entity Data Isolation (RLS)', () => {
  let mokaiClient: SupabaseClient
  let mokHouseClient: SupabaseClient

  beforeEach(async () => {
    // Create clients with different entity contexts
    mokaiClient = createClient('mokai-user-token')
    mokHouseClient = createClient('mokhouse-user-token')
  })

  it('user can only see their entity\'s transactions', async () => {
    const { data: mokaiTx } = await mokaiClient
      .from('transactions')
      .select('*')

    const { data: mokHouseTx } = await mokHouseClient
      .from('transactions')
      .select('*')

    // Ensure no overlap
    const mokaiIds = mokaiTx.map(t => t.id)
    const mokHouseIds = mokHouseTx.map(t => t.id)

    expect(mokaiIds).not.toEqual(expect.arrayContaining(mokHouseIds))
  })

  it('prevents cross-entity invoice creation', async () => {
    const { data, error } = await mokaiClient
      .from('invoices')
      .insert({
        entity_id: 'mokhouse', // Attempt to create for different entity
        client_id: 1,
        line_items: []
      })

    expect(error).not.toBeNull()
    expect(error.message).toContain('RLS policy violation')
  })

  it('prevents cross-entity contact access', async () => {
    const { data: mokaiContacts } = await mokaiClient
      .from('contacts')
      .select('*')

    const { data: mokHouseContacts } = await mokHouseClient
      .from('contacts')
      .select('*')

    // Verify contacts are isolated
    expect(mokaiContacts.every(c => c.entity_id === 'mokai')).toBe(true)
    expect(mokHouseContacts.every(c => c.entity_id === 'mokhouse')).toBe(true)
  })

  it('prevents cross-entity report generation', async () => {
    const { data, error } = await mokaiClient.rpc('calculate_bas', {
      entity_id: 'mokhouse', // Attempt to generate report for different entity
      start_date: '2025-01-01',
      end_date: '2025-03-31'
    })

    expect(error).not.toBeNull()
  })
})
```

### C. End-to-End Tests (Playwright)

#### Journey 1: Complete Invoice Lifecycle

**Location**: `/e2e/invoices/lifecycle.spec.ts`

```typescript
import { test, expect } from '@playwright/test'

test.describe('Invoice Lifecycle', () => {
  test('User creates, sends, and tracks invoice payment', async ({ page }) => {
    // Login
    await page.goto('/login')
    await page.fill('input[name=email]', 'test@sayers.com')
    await page.fill('input[name=password]', 'testpassword')
    await page.click('button:has-text("Sign In")')

    await expect(page).toHaveURL('/dashboard')

    // Navigate to invoices
    await page.click('text=Invoices')
    await expect(page).toHaveURL('/invoices')

    // Create new invoice
    await page.click('text=Create Invoice')

    // Select client
    await page.click('button:has-text("Search clients")')
    await page.fill('input[placeholder="Search clients..."]', 'Acme')
    await page.click('text=Acme Corporation')

    // Add line item
    await page.fill('input[name="line_items.0.description"]', 'Web Development')
    await page.fill('input[name="line_items.0.quantity"]', '10')
    await page.fill('input[name="line_items.0.price"]', '150')

    // Verify GST calculation
    const gstAmount = await page.textContent('[data-testid=gst-amount]')
    expect(gstAmount).toBe('$150.00')

    const total = await page.textContent('[data-testid=total-amount]')
    expect(total).toBe('$1,650.00')

    // Save and send
    await page.click('button:has-text("Save & Send")')
    await expect(page.locator('text=Invoice sent successfully')).toBeVisible()

    // Verify in list
    await page.goto('/invoices')
    await expect(page.locator('text=Acme Corporation')).toBeVisible()
    await expect(page.locator('text=Sent')).toBeVisible()

    // Get invoice ID from table
    const invoiceRow = page.locator('tr:has-text("Acme Corporation")')
    const invoiceId = await invoiceRow.getAttribute('data-invoice-id')

    // Record payment
    await invoiceRow.click()
    await expect(page).toHaveURL(`/invoices/${invoiceId}`)

    await page.click('text=Record Payment')
    await page.fill('input[name=payment_amount]', '1650')
    await page.fill('input[name=payment_date]', '2025-01-15')
    await page.click('button:has-text("Save Payment")')

    // Verify status update
    await expect(page.locator('text=Paid')).toBeVisible()
    await expect(page.locator('text=Payment recorded: $1,650.00')).toBeVisible()
  })
})
```

#### Journey 2: Transaction Review with ML

**Location**: `/e2e/transactions/ml-review.spec.ts`

```typescript
test.describe('ML Transaction Review Workflow', () => {
  test('User reviews low-confidence predictions and corrects categories', async ({ page }) => {
    await page.goto('/login')
    // ... login steps

    // Navigate to transactions
    await page.click('text=Transactions')
    await expect(page).toHaveURL('/transactions')

    // Click "Needs Review" tab
    await page.click('text=Needs Review')

    // Verify filtered to low-confidence
    const rows = page.locator('tr[data-confidence-level="low"]')
    await expect(rows).toHaveCount(await rows.count())

    // Select first low-confidence transaction
    const firstRow = rows.first()
    const categoryCell = firstRow.locator('[data-field="category"]')

    // Double-click to edit
    await categoryCell.dblClick()

    // Select correct category
    await page.selectOption('select[name="category"]', 'Office Supplies')

    // Verify optimistic update
    await expect(categoryCell).toHaveText('Office Supplies')
    await expect(categoryCell.locator('text=Manual')).toBeVisible()

    // Verify confidence badge removed
    await expect(firstRow.locator('[data-testid="confidence-badge"]')).toHaveText('Manual')

    // Check row no longer highlighted
    await expect(firstRow).not.toHaveClass(/bg-yellow/)
  })

  test('Bulk categorize similar transactions', async ({ page }) => {
    await page.goto('/transactions')

    // Filter to uncategorized "Woolworths" transactions
    await page.fill('input[placeholder="Search..."]', 'Woolworths')

    // Select all visible
    await page.check('[data-testid="select-all"]')

    // Verify selection count
    const selectedCount = await page.textContent('[data-testid="selected-count"]')
    expect(parseInt(selectedCount)).toBeGreaterThan(0)

    // Click bulk categorize
    await page.click('button:has-text("Categorize Selected")')

    // Select category in modal
    await page.selectOption('select[name="bulk_category"]', 'Groceries')
    await page.click('button:has-text("Apply to X transactions")')

    // Verify success
    await expect(page.locator('text=X transactions updated successfully')).toBeVisible()

    // Verify all now show "Groceries"
    const categoryLabels = page.locator('[data-field="category"]:has-text("Groceries")')
    expect(await categoryLabels.count()).toBe(parseInt(selectedCount))
  })
})
```

#### Journey 3: BAS Report Generation

**Location**: `/e2e/reports/bas.spec.ts`

```typescript
test.describe('BAS Report Generation', () => {
  test('User generates BAS report for Q2 2025', async ({ page }) => {
    await page.goto('/login')
    // ... login

    // Navigate to reports
    await page.click('text=Reports')
    await page.click('text=BAS Report')

    // Select quarter
    await page.selectOption('select[name="quarter"]', 'Q2')
    await page.selectOption('select[name="year"]', '2025')

    // Generate report
    await page.click('button:has-text("Generate Report")')

    // Wait for calculation
    await page.waitForSelector('text=Business Activity Statement')

    // Verify GST summary
    const gstOnSales = await page.textContent('[data-field="1A"]')
    const gstOnPurchases = await page.textContent('[data-field="1B"]')
    const netGST = await page.textContent('[data-field="7"]')

    expect(gstOnSales).toMatch(/\$[\d,]+\.\d{2}/)
    expect(gstOnPurchases).toMatch(/\$[\d,]+\.\d{2}/)
    expect(netGST).toMatch(/\$[\d,]+\.\d{2}/)

    // Download PDF
    const [download] = await Promise.all([
      page.waitForEvent('download'),
      page.click('button:has-text("Download PDF")')
    ])

    const filename = download.suggestedFilename()
    expect(filename).toMatch(/BAS-Q2-2025-\d{8}\.pdf/)

    // Verify PDF size > 0
    const path = await download.path()
    const fs = require('fs')
    const stats = fs.statSync(path)
    expect(stats.size).toBeGreaterThan(0)
  })

  test('Validates calculations against manual verification', async ({ page }) => {
    await page.goto('/reports/bas')

    // Select known quarter with verified data
    await page.selectOption('select[name="quarter"]', 'Q1')
    await page.selectOption('select[name="year"]', '2025')

    await page.click('button:has-text("Generate Report")')
    await page.waitForSelector('text=Business Activity Statement')

    // Get calculated values
    const G1 = parseFloat((await page.textContent('[data-field="G1"]')).replace(/[\$,]/g, ''))
    const A1 = parseFloat((await page.textContent('[data-field="1A"]')).replace(/[\$,]/g, ''))
    const B1 = parseFloat((await page.textContent('[data-field="1B"]')).replace(/[\$,]/g, ''))

    // Verify G1 * 0.1 = 1A (GST on sales)
    expect(A1).toBeCloseTo(G1 * 0.1, 2)

    // Verify net calculation
    const net = parseFloat((await page.textContent('[data-field="7"]')).replace(/[\$,]/g, ''))
    expect(net).toBeCloseTo(A1 - B1, 2)
  })
})
```

#### Journey 4: Multi-Entity Data Isolation

**Location**: `/e2e/entities/isolation.spec.ts`

```typescript
test.describe('Multi-Entity Data Isolation', () => {
  test('User switches entities and sees isolated data', async ({ page }) => {
    await page.goto('/login')
    // ... login

    // Verify default entity (MOKAI)
    const entityDropdown = page.locator('[data-testid="entity-selector"]')
    await expect(entityDropdown).toHaveText('MOKAI PTY LTD')

    // Count transactions
    await page.click('text=Transactions')
    const mokaiCount = await page.locator('text=Showing').textContent()
    const mokaiTotal = parseInt(mokaiCount.match(/of (\d+)/)[1])

    // Switch to MOK HOUSE
    await entityDropdown.click()
    await page.click('text=MOK HOUSE PTY LTD')

    // Wait for reload
    await page.waitForURL(/entity=mok-house/)

    // Verify entity changed
    await expect(entityDropdown).toHaveText('MOK HOUSE PTY LTD')

    // Verify different transaction count
    await page.goto('/transactions')
    const mokHouseCount = await page.locator('text=Showing').textContent()
    const mokHouseTotal = parseInt(mokHouseCount.match(/of (\d+)/)[1])

    expect(mokHouseTotal).not.toBe(mokaiTotal)

    // Verify no cross-entity data leakage
    // Search for MOKAI-specific transaction
    await page.fill('input[placeholder="Search..."]', 'MOKAI-SPECIFIC-TRANSACTION')
    await expect(page.locator('text=No transactions found')).toBeVisible()
  })

  test('Entity selection persists across sessions', async ({ page, context }) => {
    await page.goto('/login')
    // ... login

    // Switch to MOK HOUSE
    await page.click('[data-testid="entity-selector"]')
    await page.click('text=MOK HOUSE PTY LTD')

    await expect(page.locator('[data-testid="entity-selector"]')).toHaveText('MOK HOUSE PTY LTD')

    // Close and reopen browser
    await page.close()
    const newPage = await context.newPage()

    await newPage.goto('/dashboard')

    // Verify entity persisted
    await expect(newPage.locator('[data-testid="entity-selector"]')).toHaveText('MOK HOUSE PTY LTD')
  })
})
```

#### Journey 5: Dashboard KPI Accuracy

**Location**: `/e2e/dashboard/kpis.spec.ts`

```typescript
test.describe('Dashboard KPI Accuracy', () => {
  test('KPI calculations match database queries', async ({ page }) => {
    await page.goto('/login')
    // ... login

    await page.goto('/dashboard')

    // Get displayed KPI values
    const revenueKPI = await page.textContent('[data-kpi="revenue"] [data-value]')
    const expensesKPI = await page.textContent('[data-kpi="expenses"] [data-value]')
    const profitKPI = await page.textContent('[data-kpi="profit"] [data-value]')

    const revenue = parseFloat(revenueKPI.replace(/[\$,]/g, ''))
    const expenses = parseFloat(expensesKPI.replace(/[\$,]/g, ''))
    const profit = parseFloat(profitKPI.replace(/[\$,]/g, ''))

    // Verify profit = revenue - expenses
    expect(profit).toBeCloseTo(revenue - expenses, 2)

    // Query Supabase directly to verify
    const { createClient } = require('@supabase/supabase-js')
    const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY)

    const { data: transactions } = await supabase
      .from('transactions')
      .select('amount_cents')
      .eq('entity_id', 'mokai')
      .gte('created_at', '2025-01-01')
      .lte('created_at', '2025-01-31')

    const dbRevenue = transactions
      .filter(t => t.amount_cents > 0)
      .reduce((sum, t) => sum + t.amount_cents, 0) / 100

    const dbExpenses = Math.abs(
      transactions
        .filter(t => t.amount_cents < 0)
        .reduce((sum, t) => sum + t.amount_cents, 0)
    ) / 100

    // Verify UI matches database
    expect(revenue).toBeCloseTo(dbRevenue, 2)
    expect(expenses).toBeCloseTo(dbExpenses, 2)
  })

  test('Charts display correct data', async ({ page }) => {
    await page.goto('/dashboard')

    // Wait for chart to load
    await page.waitForSelector('[data-chart="revenue-expense-trend"]')

    // Get chart data (via data attributes or DOM inspection)
    const chartData = await page.evaluate(() => {
      const chart = document.querySelector('[data-chart="revenue-expense-trend"]')
      return JSON.parse(chart.getAttribute('data-values'))
    })

    // Verify data points exist for last 6 months
    expect(chartData.length).toBe(6)

    // Verify each month has revenue and expense values
    chartData.forEach(point => {
      expect(point).toHaveProperty('month')
      expect(point).toHaveProperty('revenue')
      expect(point).toHaveProperty('expenses')
    })
  })
})
```

---

## 3. Quality Gates per Epic

### Epic 1: Foundation & Core Infrastructure

**Quality Gate**: ✅ All tests must pass before merging to main

#### Required Tests:
- ✅ Unit: Supabase client initialization (10 tests)
- ✅ Unit: Authentication helpers (8 tests)
- ✅ Unit: Entity context management (12 tests)
- ✅ Integration: Login flow (5 tests)
- ✅ Integration: Entity switching (8 tests)
- ✅ E2E: Login → Dashboard → Entity switch (1 test)

#### Quality Metrics:
- **Unit Test Coverage**: ≥95%
- **Integration Test Coverage**: ≥80%
- **E2E Tests**: 1 critical path
- **No console errors** in dev tools
- **Lighthouse score**: >90 (Performance, Accessibility)

#### Pre-Merge Checklist:
- [ ] All tests pass
- [ ] RLS policies verified (integration tests)
- [ ] Authentication works (E2E test)
- [ ] No ESLint errors
- [ ] Prettier formatting applied

---

### Epic 2: Dashboard & Visualization

**Quality Gate**: ✅ KPI calculations accurate + charts render correctly

#### Required Tests:
- ✅ Unit: KPI calculation functions (20 tests)
- ✅ Unit: Chart data transformations (15 tests)
- ✅ Component: KPICard rendering (12 tests)
- ✅ Component: FinancialChart rendering (18 tests)
- ✅ Integration: Dashboard data fetching (10 tests)
- ✅ E2E: Dashboard KPI accuracy (1 test)

#### Quality Metrics:
- **KPI Calculation Coverage**: 100%
- **Chart Component Coverage**: ≥85%
- **Responsive Design**: Tested (mobile/desktop)
- **Loading states**: Display correctly
- **Accessibility**: axe-core passes

#### Pre-Merge Checklist:
- [ ] KPI calculations match database queries (E2E test)
- [ ] Charts render with real data
- [ ] Responsive design verified (DevTools)
- [ ] Loading skeletons appear before data
- [ ] No accessibility violations (axe-core)

---

### Epic 3: Transaction Management

**Quality Gate**: ✅ ML prediction display accurate + categorization works + bulk operations tested

#### Required Tests:
- ✅ Unit: Transaction filtering logic (18 tests)
- ✅ Unit: Confidence score interpretation (8 tests)
- ✅ Component: TransactionRow (15 tests)
- ✅ Component: MLConfidenceIndicator (10 tests)
- ✅ Integration: Transaction list filtering (12 tests)
- ✅ Integration: Category override (10 tests)
- ✅ Integration: Bulk operations (8 tests)
- ✅ E2E: ML review workflow (1 test)
- ✅ E2E: Bulk categorize (1 test)

#### Quality Metrics:
- **Unit Test Coverage**: ≥90%
- **Integration Coverage**: ≥85%
- **E2E**: 2 critical journeys
- **Pagination**: Works with large datasets (virtual scrolling tested)
- **RLS**: Prevents cross-entity data access (integration test)

#### Pre-Merge Checklist:
- [ ] ML predictions display correctly
- [ ] Confidence scores categorized accurately (high/medium/low)
- [ ] Inline editing works (optimistic UI)
- [ ] Bulk operations complete successfully
- [ ] RLS integration tests pass

---

### Epic 4: Invoice Management & PDF Generation

**Quality Gate**: ✅ Invoice creation E2E + GST 100% accurate + PDF generates correctly

#### Required Tests:
- ✅ Unit: GST calculation (15 tests) ← **CRITICAL**
- ✅ Unit: Invoice totals (12 tests) ← **CRITICAL**
- ✅ Component: InvoiceLineItem (14 tests)
- ✅ Component: InvoiceTotals (10 tests)
- ✅ Integration: Invoice form validation (12 tests)
- ✅ Integration: Quick-add client (8 tests)
- ✅ Integration: PDF generation (10 tests)
- ✅ E2E: Invoice lifecycle (1 test) ← **CRITICAL**

#### Quality Metrics:
- **GST Calculation Coverage**: 100% ← **NON-NEGOTIABLE**
- **Invoice Totals Coverage**: 100%
- **Integration Coverage**: ≥85%
- **E2E**: 1 complete lifecycle test
- **PDF Validation**: Produces valid invoices (manual review)

#### ATO Test Cases (GST):
```typescript
// ATO Example 1: $100 + GST = $110
expect(calculateGST(100, 'exclusive')).toBe(10)
expect(calculateTotal(100, 10)).toBe(110)

// ATO Example 2: $110 inc GST → $100 ex GST
expect(calculateGSTInclusive(110)).toEqual({ net: 100, gst: 10 })

// ATO Example 3: BAS calculation
const transactions = [
  { type: 'sale', net: 1000, gst: 100 },
  { type: 'purchase', net: 500, gst: 50 }
]
expect(calculateBAS(transactions)).toEqual({
  G1: 1000,  // Total sales
  '1A': 100, // GST on sales
  '1B': 50,  // GST on purchases
  net: 50    // GST payable
})
```

#### Pre-Merge Checklist:
- [ ] GST calculations 100% tested against ATO examples
- [ ] Invoice totals match manual calculations
- [ ] PDF generates without errors (<5s)
- [ ] Invoice E2E test passes (create → send → pay)
- [ ] Status tracking updates correctly

---

### Epic 5: Reports & Tax Compliance

**Quality Gate**: ✅ BAS calculations match manual + P&L balances + exports validate

#### Required Tests:
- ✅ Unit: BAS calculation engine (25 tests) ← **CRITICAL**
- ✅ Unit: P&L calculation (18 tests)
- ✅ Unit: Export formatting (CSV/PDF) (12 tests)
- ✅ Integration: BAS report generation (10 tests)
- ✅ Integration: Date range filtering (8 tests)
- ✅ E2E: BAS generation and export (1 test) ← **CRITICAL**

#### Quality Metrics:
- **BAS Calculation Coverage**: 100% ← **NON-NEGOTIABLE**
- **P&L Calculation Coverage**: 100%
- **Export Validation**: All formats tested
- **E2E**: 1 BAS generation test
- **Tax Compliance**: Verified (accountant review)

#### BAS Calculation Tests:
```typescript
describe('BAS Field Calculations', () => {
  it('calculates G1 (Total Sales) correctly', () => {
    const transactions = [...]
    expect(calculateBASField('G1', transactions)).toBe(12500)
  })

  it('calculates 1A (GST on Sales) correctly', () => {
    expect(calculateBASField('1A', transactions)).toBe(1250)
  })

  it('calculates 1B (GST on Purchases) correctly', () => {
    expect(calculateBASField('1B', transactions)).toBe(780)
  })

  it('calculates net GST payable/refundable', () => {
    const bas = calculateBAS(transactions)
    expect(bas.net).toBe(470) // 1A - 1B
  })

  it('filters by date range correctly', () => {
    const result = calculateBAS(transactions, 'mokai', '2025-01-01', '2025-03-31')
    // Verify only Q1 transactions included
  })

  it('handles multiple entities separately', () => {
    const mokaiResult = calculateBAS(transactions, 'mokai', ...)
    const mokHouseResult = calculateBAS(transactions, 'mokhouse', ...)
    expect(mokaiResult.G1).not.toBe(mokHouseResult.G1)
  })
})
```

#### Pre-Merge Checklist:
- [ ] BAS calculations match manual calculations
- [ ] P&L statement balances (revenue - expenses = profit)
- [ ] CSV exports have correct format (accounting software compatible)
- [ ] PDF exports generate without errors
- [ ] Date range filtering tested (quarterly, annual, custom)

---

### Epic 6: Settings & Administration

**Quality Gate**: ✅ CRUD operations tested + audit log records all changes + user preferences persist

#### Required Tests:
- ✅ Unit: Audit log formatting (10 tests)
- ✅ Component: Entity management (12 tests)
- ✅ Component: Contact management (15 tests)
- ✅ Integration: User preferences (10 tests)
- ✅ Integration: Audit trail (12 tests)
- ✅ Integration: Chart of accounts CRUD (10 tests)

#### Quality Metrics:
- **CRUD Coverage**: ≥90% (all entities/contacts/accounts operations)
- **Audit Log**: Captures all modifications (integration tests)
- **User Preferences**: Persist across sessions (integration test)

#### Pre-Merge Checklist:
- [ ] Entity CRUD works (create/read/update/delete)
- [ ] Contact management with validation
- [ ] Chart of accounts editing
- [ ] User preferences persist (localStorage + Supabase)
- [ ] Audit log records all changes

---

## 4. Financial Accuracy Testing

### ATO Compliance Test Cases

**GST Calculation Accuracy**:

```typescript
describe('ATO GST Examples', () => {
  it('ATO Example 1: $100 + GST = $110', () => {
    expect(calculateGST(100, 'exclusive')).toBe(10)
    expect(calculateTotal(100, 10)).toBe(110)
  })

  it('ATO Example 2: $110 inc GST → $100 ex GST', () => {
    const result = calculateGSTInclusive(110)
    expect(result.net).toBe(100)
    expect(result.gst).toBe(10)
  })

  it('ATO Example 3: BAS calculation', () => {
    const transactions = [
      { type: 'sale', net: 1000, gst: 100 },
      { type: 'purchase', net: 500, gst: 50 }
    ]
    expect(calculateBAS(transactions)).toEqual({
      G1: 1000,  // Total sales
      '1A': 100, // GST on sales
      '1B': 50,  // GST on purchases
      net: 50    // GST payable
    })
  })

  it('ATO Example 4: Rounding (banker\'s rounding)', () => {
    // 0.005 rounds to 0.00 (even)
    expect(calculateGST(0.05, 'exclusive')).toBe(0.00)
    // 0.015 rounds to 0.02 (even)
    expect(calculateGST(0.15, 'exclusive')).toBe(0.02)
    // 0.025 rounds to 0.02 (even)
    expect(calculateGST(0.25, 'exclusive')).toBe(0.02)
  })
})
```

### Decimal Precision Testing

**Using decimal.js for Accuracy**:

```typescript
import Decimal from 'decimal.js'

describe('Decimal Precision', () => {
  it('uses decimal.js for all financial calculations', () => {
    const amount = new Decimal(100)
    const gst = amount.times(0.1)
    expect(gst.toNumber()).toBe(10)
  })

  it('handles floating point edge cases', () => {
    // JavaScript floating point error: 0.1 + 0.2 = 0.30000000000000004
    const jsResult = 0.1 + 0.2
    expect(jsResult).not.toBe(0.3) // Fails without decimal.js

    // Decimal.js correct result
    const decimalResult = new Decimal(0.1).plus(0.2)
    expect(decimalResult.toNumber()).toBe(0.3) // Passes with decimal.js
  })

  it('applies banker\'s rounding correctly', () => {
    Decimal.set({ rounding: Decimal.ROUND_HALF_EVEN })

    expect(new Decimal(0.005).toDecimalPlaces(2).toNumber()).toBe(0.00)
    expect(new Decimal(0.015).toDecimalPlaces(2).toNumber()).toBe(0.02)
    expect(new Decimal(0.025).toDecimalPlaces(2).toNumber()).toBe(0.02)
  })

  it('validates against manual calculations', () => {
    const lineItems = [
      { qty: 10, price: 150.50, gst: true }
    ]

    // Manual: 10 * 150.50 = 1505.00
    // GST: 1505.00 * 0.1 = 150.50
    // Total: 1505.00 + 150.50 = 1655.50

    const result = calculateInvoiceTotals(lineItems)
    expect(result.subtotal).toBe(1505.00)
    expect(result.gst).toBe(150.50)
    expect(result.total).toBe(1655.50)
  })

  it('validates against accounting software outputs', () => {
    // Compare to Xero/MYOB calculated values
    const xeroInvoice = {
      subtotal: 4500.00,
      gst: 450.00,
      total: 4950.00
    }

    const lineItems = [
      { qty: 1, price: 1500, gst: true },
      { qty: 40, price: 75, gst: true }
    ]

    const result = calculateInvoiceTotals(lineItems)
    expect(result).toEqual(xeroInvoice)
  })
})
```

### Known Invoice Validation

**Test Against Real Invoices**:

```typescript
describe('Known Invoice Validation', () => {
  it('validates against invoice INV-001 from Supabase', async () => {
    // Fetch real invoice from database
    const { data: invoice } = await supabase
      .from('invoices')
      .select('*, line_items(*)')
      .eq('invoice_number', 'INV-001')
      .single()

    // Recalculate totals
    const calculated = calculateInvoiceTotals(invoice.line_items)

    // Verify matches stored values
    expect(calculated.subtotal).toBe(invoice.subtotal_cents / 100)
    expect(calculated.gst).toBe(invoice.gst_cents / 100)
    expect(calculated.total).toBe(invoice.total_cents / 100)
  })

  it('validates against multiple production invoices', async () => {
    const { data: invoices } = await supabase
      .from('invoices')
      .select('*, line_items(*)')
      .eq('status', 'paid')
      .limit(10)

    for (const invoice of invoices) {
      const calculated = calculateInvoiceTotals(invoice.line_items)

      expect(calculated.total).toBeCloseTo(invoice.total_cents / 100, 2)
    }
  })
})
```

---

## 5. Security Testing

### RLS Policy Tests

**Multi-Entity Data Isolation**:

```typescript
describe('Multi-Entity Data Isolation (RLS)', () => {
  let mokaiUser: SupabaseClient
  let mokHouseUser: SupabaseClient

  beforeEach(async () => {
    mokaiUser = createClient('mokai-user-token')
    mokHouseUser = createClient('mokhouse-user-token')
  })

  it('user can only see their entity\'s transactions', async () => {
    const { data: mokaiTx } = await mokaiUser
      .from('transactions')
      .select('*')

    const { data: mokHouseTx } = await mokHouseUser
      .from('transactions')
      .select('*')

    // Ensure no overlap
    expect(mokaiTx).not.toContainAny(mokHouseTx)
  })

  it('prevents cross-entity invoice creation', async () => {
    const { error } = await mokaiUser
      .from('invoices')
      .insert({
        entity_id: 'mokhouse', // Wrong entity
        client_id: 1,
        line_items: []
      })

    expect(error).not.toBeNull()
    expect(error.code).toBe('42501') // RLS policy violation
  })

  it('prevents cross-entity contact access', async () => {
    const { data } = await mokaiUser
      .from('contacts')
      .select('*')
      .eq('entity_id', 'mokhouse') // Attempt to access wrong entity

    expect(data).toHaveLength(0) // RLS blocks this
  })

  it('prevents cross-entity report generation', async () => {
    const { error } = await mokaiUser.rpc('calculate_bas', {
      entity_id: 'mokhouse', // Wrong entity
      start_date: '2025-01-01',
      end_date: '2025-03-31'
    })

    expect(error).not.toBeNull()
  })
})
```

### Input Validation Tests

**SQL Injection Protection**:

```typescript
describe('SQL Injection Protection', () => {
  it('escapes malicious SQL in transaction description', async () => {
    const maliciousInput = "'; DROP TABLE transactions; --"

    const { data, error } = await supabase
      .from('transactions')
      .insert({
        description: maliciousInput,
        amount_cents: 100,
        entity_id: 'mokai'
      })

    // Supabase client escapes automatically
    expect(error).toBeNull()
    expect(data.description).toBe(maliciousInput) // Stored as-is, not executed
  })

  it('validates invoice input fields', async () => {
    const { error } = await supabase
      .from('invoices')
      .insert({
        client_id: "'; DELETE FROM clients; --", // SQL injection attempt
        line_items: []
      })

    // Type validation catches this
    expect(error).not.toBeNull()
  })
})
```

**XSS Protection**:

```typescript
describe('XSS Protection', () => {
  it('escapes malicious scripts in transaction description', () => {
    const maliciousInput = '<script>alert("XSS")</script>'

    render(<TransactionRow transaction={{ description: maliciousInput }} />)

    // React escapes automatically
    expect(screen.queryByRole('script')).not.toBeInTheDocument()
    expect(screen.getByText(maliciousInput)).toBeInTheDocument()
  })

  it('sanitizes invoice notes before rendering', () => {
    const maliciousNotes = '<img src=x onerror=alert("XSS")>'

    render(<InvoiceDetail invoice={{ notes: maliciousNotes }} />)

    // React escapes
    expect(screen.queryByRole('img')).not.toBeInTheDocument()
  })
})
```

### Authentication Tests

**Login/Logout Flow**:

```typescript
describe('Authentication Flow', () => {
  it('redirects unauthenticated users to login', async () => {
    const { req, res } = createMocks({
      method: 'GET',
      url: '/dashboard'
    })

    await middleware(req, res)

    expect(res._getRedirectUrl()).toBe('/login')
  })

  it('allows authenticated users to access dashboard', async () => {
    const { req, res } = createMocks({
      method: 'GET',
      url: '/dashboard',
      headers: {
        cookie: 'sb-access-token=valid-token'
      }
    })

    await middleware(req, res)

    expect(res.statusCode).toBe(200)
  })

  it('logs out user and clears session', async () => {
    await page.goto('/dashboard')
    await page.click('button:has-text("Logout")')

    // Verify redirect to login
    await expect(page).toHaveURL('/login')

    // Verify cannot access protected route
    await page.goto('/dashboard')
    await expect(page).toHaveURL('/login')
  })
})
```

---

## 6. Performance Testing

### Load Testing

**Dashboard Performance**:

```typescript
describe('Dashboard Performance', () => {
  it('loads dashboard <2s with 1000 transactions', async () => {
    // Seed database with 1000 transactions
    await seedTransactions(1000)

    const startTime = performance.now()
    await page.goto('/dashboard')
    await page.waitForSelector('[data-kpi="revenue"]')
    const endTime = performance.now()

    const loadTime = endTime - startTime
    expect(loadTime).toBeLessThan(2000) // NFR1: <2s
  })

  it('transaction list paginates efficiently', async () => {
    await seedTransactions(1000)

    const startTime = performance.now()
    await page.goto('/transactions')
    await page.waitForSelector('table')
    const endTime = performance.now()

    expect(endTime - startTime).toBeLessThan(1000) // Should be fast with pagination
  })

  it('charts render <500ms with large datasets', async () => {
    await seedTransactions(5000) // Large dataset

    await page.goto('/dashboard')

    const startTime = performance.now()
    await page.waitForSelector('[data-chart="revenue-expense-trend"]')
    const endTime = performance.now()

    expect(endTime - startTime).toBeLessThan(500)
  })
})
```

### API Response Time

**Supabase Query Performance**:

```typescript
describe('API Response Time', () => {
  it('transaction queries respond <100ms', async () => {
    const startTime = performance.now()

    const { data } = await supabase
      .from('transactions')
      .select('*')
      .eq('entity_id', 'mokai')
      .limit(50)

    const endTime = performance.now()

    expect(endTime - startTime).toBeLessThan(100) // NFR2
  })

  it('invoice queries with joins respond <150ms', async () => {
    const startTime = performance.now()

    const { data } = await supabase
      .from('invoices')
      .select('*, client:contacts(*), line_items(*)')
      .eq('entity_id', 'mokai')
      .limit(25)

    const endTime = performance.now()

    expect(endTime - startTime).toBeLessThan(150)
  })
})
```

### Bundle Size Optimization

**JavaScript Bundle Analysis**:

```bash
# Run after build
npm run build
npx @next/bundle-analyzer
```

**Target Metrics**:
- **Total bundle size**: <200KB (gzip)
- **First Load JS**: <100KB
- **Largest chunk**: <50KB

---

## 7. Accessibility Testing

### Automated Accessibility (axe-core)

**Dashboard Accessibility**:

```typescript
import { injectAxe, checkA11y } from 'axe-playwright'

test.describe('Dashboard Accessibility', () => {
  test('Dashboard is accessible (WCAG AA)', async ({ page }) => {
    await page.goto('/dashboard')
    await injectAxe(page)
    await checkA11y(page)
  })

  test('Transactions list is accessible', async ({ page }) => {
    await page.goto('/transactions')
    await injectAxe(page)
    await checkA11y(page)
  })

  test('Invoice creation form is accessible', async ({ page }) => {
    await page.goto('/invoices/new')
    await injectAxe(page)
    await checkA11y(page)
  })
})
```

### Manual Accessibility Testing

**Keyboard Navigation**:

```typescript
test.describe('Keyboard Navigation', () => {
  test('Can navigate dashboard with keyboard', async ({ page }) => {
    await page.goto('/dashboard')

    // Tab through KPI cards
    await page.keyboard.press('Tab')
    expect(await page.locator(':focus').getAttribute('data-kpi')).toBe('revenue')

    await page.keyboard.press('Tab')
    expect(await page.locator(':focus').getAttribute('data-kpi')).toBe('expenses')

    await page.keyboard.press('Tab')
    expect(await page.locator(':focus').getAttribute('data-kpi')).toBe('profit')
  })

  test('Can edit transaction with keyboard', async ({ page }) => {
    await page.goto('/transactions')

    // Tab to first row
    await page.keyboard.press('Tab')
    await page.keyboard.press('Tab')

    // Enter to navigate to detail
    await page.keyboard.press('Enter')
    await expect(page).toHaveURL(/\/transactions\/\d+/)

    // Tab to category field
    await page.keyboard.press('Tab')
    await page.keyboard.press('Tab')
    await page.keyboard.press('Tab')

    // Space to open dropdown
    await page.keyboard.press('Space')
    expect(await page.locator('select[name="category"]').isVisible()).toBe(true)
  })
})
```

**Screen Reader Compatibility**:

```typescript
test.describe('Screen Reader Support', () => {
  test('KPI cards have aria-labels', async ({ page }) => {
    await page.goto('/dashboard')

    const revenueCard = page.locator('[data-kpi="revenue"]')
    expect(await revenueCard.getAttribute('aria-label')).toBe('Revenue: $12,345.00, up 15% vs last month')
  })

  test('Confidence badges have descriptive labels', async ({ page }) => {
    await page.goto('/transactions')

    const badge = page.locator('[data-testid="confidence-badge"]').first()
    expect(await badge.getAttribute('aria-label')).toMatch(/confidence: 0\.\d+/)
  })

  test('Charts have alternative data tables', async ({ page }) => {
    await page.goto('/dashboard')

    // Check for screen-reader-only table
    const table = page.locator('table.sr-only')
    expect(await table.count()).toBeGreaterThan(0)
  })
})
```

**Color Contrast**:

```typescript
test.describe('Color Contrast (WCAG AA)', () => {
  test('Text has ≥4.5:1 contrast ratio', async ({ page }) => {
    await page.goto('/dashboard')

    // Check primary text
    const textColor = await page.evaluate(() => {
      const element = document.querySelector('h1')
      return window.getComputedStyle(element).color
    })

    const backgroundColor = await page.evaluate(() => {
      return window.getComputedStyle(document.body).backgroundColor
    })

    const contrastRatio = calculateContrast(textColor, backgroundColor)
    expect(contrastRatio).toBeGreaterThanOrEqual(4.5)
  })

  test('UI components have ≥3:1 contrast', async ({ page }) => {
    await page.goto('/dashboard')

    const buttonColor = await page.evaluate(() => {
      const button = document.querySelector('button')
      return window.getComputedStyle(button).borderColor
    })

    const bgColor = await page.evaluate(() => {
      return window.getComputedStyle(document.body).backgroundColor
    })

    const contrastRatio = calculateContrast(buttonColor, bgColor)
    expect(contrastRatio).toBeGreaterThanOrEqual(3)
  })
})
```

---

## 8. Regression Testing

### Continuous Testing

**CI/CD Pipeline Configuration** (`.github/workflows/test.yml`):

```yaml
name: Test Suite

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Run ESLint
        run: npm run lint

      - name: Run Prettier check
        run: npm run format:check

      - name: Run Vitest (unit + integration)
        run: npm run test:coverage

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3

      - name: Setup Playwright
        run: npx playwright install --with-deps

      - name: Run Playwright (E2E)
        run: npm run test:e2e

      - name: Upload Playwright report
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/

      - name: Comment PR with test results
        uses: daun/playwright-report-comment@v3
        if: always()
        with:
          report-path: playwright-report/index.html
```

**Test Data Management**:

```typescript
// test/setup.ts

import { createClient } from '@supabase/supabase-js'

beforeEach(async () => {
  // Reset database to seed state
  const supabase = createClient(
    process.env.SUPABASE_TEST_URL,
    process.env.SUPABASE_TEST_KEY
  )

  // Delete test data
  await supabase.from('transactions').delete().eq('entity_id', 'test-entity')
  await supabase.from('invoices').delete().eq('entity_id', 'test-entity')

  // Reseed with known data
  await seedDatabase()
})

async function seedDatabase() {
  // Insert test entities
  await supabase.from('entities').insert([
    { id: 'test-mokai', name: 'Test MOKAI', entity_type: 'company' },
    { id: 'test-mokhouse', name: 'Test MOK HOUSE', entity_type: 'company' }
  ])

  // Insert test transactions
  await supabase.from('transactions').insert([
    { entity_id: 'test-mokai', description: 'Test Transaction 1', amount_cents: 10000 },
    { entity_id: 'test-mokai', description: 'Test Transaction 2', amount_cents: -5000 }
  ])
}
```

### Visual Regression Tests

**Playwright Screenshot Comparison** (optional):

```typescript
test.describe('Visual Regression', () => {
  test('Dashboard matches baseline screenshot', async ({ page }) => {
    await page.goto('/dashboard')
    await page.waitForSelector('[data-kpi="revenue"]')

    await expect(page).toHaveScreenshot('dashboard-baseline.png')
  })

  test('Invoice PDF matches baseline', async ({ page }) => {
    await page.goto('/invoices/1')
    await page.click('text=View PDF')

    const pdfFrame = page.frameLocator('iframe')
    await expect(pdfFrame.locator('body')).toHaveScreenshot('invoice-pdf-baseline.png')
  })
})
```

---

## 9. Test Execution Plan

### Test Phases

**Phase 1: Unit Tests (Continuous)**
- **When**: On every commit
- **Duration**: ~30 seconds
- **Coverage**: All financial calculations, utilities, components
- **Tooling**: Vitest + React Testing Library
- **Pass Criteria**: 100% financial calculations, ≥80% overall

**Phase 2: Integration Tests (Pre-Merge)**
- **When**: Before merging PR to main
- **Duration**: ~2-3 minutes
- **Coverage**: Form workflows, Supabase queries, RLS enforcement
- **Tooling**: Vitest + Supabase Test Client
- **Pass Criteria**: All critical paths tested, RLS verified

**Phase 3: E2E Tests (Pre-Deploy)**
- **When**: Before deploying to staging/production
- **Duration**: ~5-8 minutes
- **Coverage**: 5 critical user journeys
- **Tooling**: Playwright
- **Pass Criteria**: All 5 journeys pass, no console errors

**Phase 4: Accessibility Audit (Pre-Deploy)**
- **When**: Before deploying to production
- **Duration**: ~10 minutes (manual + automated)
- **Coverage**: All pages, WCAG AA compliance
- **Tooling**: axe-core + manual testing
- **Pass Criteria**: No accessibility violations

**Phase 5: Performance Testing (Pre-Deploy)**
- **When**: Before deploying to production
- **Duration**: ~15 minutes
- **Coverage**: Page load times, API responses, bundle size
- **Tooling**: Lighthouse + Chrome DevTools
- **Pass Criteria**: All NFR metrics met

### CI/CD Pipeline

**Pull Request Workflow**:

1. **Developer commits code** → Triggers CI
2. **CI runs Phase 1 (Unit Tests)** → Must pass
3. **CI runs Phase 2 (Integration Tests)** → Must pass
4. **Developer requests review** → Reviewer checks tests
5. **CI runs Phase 3 (E2E Tests)** → Must pass
6. **PR approved** → Merge to main

**Staging Deployment Workflow**:

1. **Code merged to main** → Triggers deploy
2. **Vercel deploys to staging** → Automatic
3. **Phase 4 (Accessibility Audit)** → Manual check
4. **Phase 5 (Performance Testing)** → Lighthouse
5. **Staging verified** → Ready for production

**Production Deployment Workflow**:

1. **Create release tag** → Triggers production deploy
2. **Vercel deploys to production** → Automatic
3. **Smoke tests** → Basic E2E tests on production
4. **Monitor for errors** → Sentry alerts
5. **Rollback if needed** → Vercel instant rollback

### Pre-Merge Checklist Template

```markdown
## PR Checklist

### Code Quality
- [ ] All unit tests pass (100% financial calculations)
- [ ] All integration tests pass
- [ ] All E2E tests pass
- [ ] No ESLint errors
- [ ] Prettier formatting applied
- [ ] No console errors in dev tools

### Functional Testing
- [ ] Feature tested manually in browser
- [ ] Mobile responsive verified (DevTools)
- [ ] Multi-entity isolation tested
- [ ] Error handling verified

### Security
- [ ] RLS policies enforced (integration tests)
- [ ] Input validation works
- [ ] No hardcoded secrets
- [ ] Authentication checked

### Accessibility
- [ ] Keyboard navigation works
- [ ] Screen reader tested (VoiceOver/NVDA)
- [ ] Color contrast verified (≥4.5:1)
- [ ] axe-core passes (no violations)

### Performance
- [ ] Page load <2s
- [ ] API responses <100ms
- [ ] Bundle size <200KB (gzip)
- [ ] Lighthouse score >90

### Documentation
- [ ] README updated (if needed)
- [ ] Code comments added for complex logic
- [ ] Test coverage report reviewed
```

---

## 10. Test Maintenance

### Living Documentation

**Test Documentation Standards**:

```typescript
// Good: Clear test description aligned with acceptance criteria
describe('Invoice GST Calculation (AC #5 from Story 4.2)', () => {
  it('calculates 10% GST on line items with GST enabled', () => {
    // Arrange
    const lineItems = [{ qty: 1, price: 100, gst: true }]

    // Act
    const result = calculateInvoiceTotals(lineItems)

    // Assert
    expect(result.gst).toBe(10)
  })
})

// Bad: Vague test description
describe('Calculations', () => {
  it('works correctly', () => {
    expect(doSomething()).toBeTruthy()
  })
})
```

**Test Coverage Reports**:

```bash
# Generate coverage report
npm run test:coverage

# View in browser
open coverage/index.html
```

### Test Debt Management

**Flaky Test Protocol**:

1. **Identify**: Mark test as `test.skip()` with `// TODO: Fix flaky test` comment
2. **Document**: Create GitHub issue with reproduction steps
3. **Fix ASAP**: Flaky tests erode confidence
4. **Root Cause**: Usually timing issues, race conditions, or bad mocks

**Brittle Test Refactoring**:

```typescript
// Brittle: Depends on specific HTML structure
expect(screen.getByText('Revenue')).toBeInTheDocument()
expect(screen.getByText('Revenue').nextSibling.textContent).toBe('$12,345')

// Robust: Uses semantic queries and data attributes
const revenueKPI = screen.getByLabelText('Revenue')
expect(revenueKPI).toHaveTextContent('$12,345')
```

**Bug-Driven Testing**:

```typescript
// When bug found in production, add regression test FIRST

test('Bug #42: Negative GST calculation for refunds', () => {
  // Reproduce bug
  const refundAmount = -100
  const gst = calculateGST(refundAmount, 'exclusive')

  // Expected: -$10 (negative GST for refunds)
  expect(gst).toBe(-10)
})

// Then fix the bug in code
```

### Quarterly Test Review

**Every 3 Months**:

1. **Review test coverage**: Are we still at ≥80%?
2. **Audit slow tests**: Can we speed them up?
3. **Remove obsolete tests**: Features removed? Delete tests.
4. **Update test data**: Reflect production reality
5. **Review failures**: Any patterns? Address root causes.

---

## Summary

### Test Inventory

| Test Category | Estimated Count | Tools |
|--------------|----------------|-------|
| **Unit Tests** | 300-400 | Vitest |
| **Integration Tests** | 80-100 | Vitest + RTL + Supabase |
| **E2E Tests** | 20-25 | Playwright |
| **Total** | **400-525** | Mixed |

### Coverage Goals

| Category | Target | Critical |
|----------|--------|----------|
| Financial Calculations | 100% | ✅ YES |
| Utility Functions | 100% | ✅ YES |
| React Components | ≥80% | ⚠️ IMPORTANT |
| Integration Tests | Critical Paths | ⚠️ IMPORTANT |
| E2E Tests | 5 Journeys | ⚠️ IMPORTANT |

### Critical Test Cases (Top 10)

1. **GST Calculation Accuracy** (ATO examples) ← **HIGHEST PRIORITY**
2. **BAS Field Calculations** (G1, 1A, 1B, net) ← **HIGHEST PRIORITY**
3. **Invoice Totals Accuracy** (subtotal, GST, total)
4. **Multi-Entity RLS Isolation** (no data leakage)
5. **Invoice Creation E2E** (create → send → pay)
6. **ML Prediction Display** (confidence levels, categorization)
7. **Transaction Categorization Workflow** (override, bulk)
8. **BAS Report Generation E2E** (calculate → export)
9. **Entity Switching** (data refresh, context isolation)
10. **Financial KPI Accuracy** (match database queries)

### Testing Timeline (TDD vs After Implementation)

**Test-Driven Development (TDD)**:
- **Epic 4 (Invoices)**: Write GST calculation tests BEFORE implementing
- **Epic 5 (Reports)**: Write BAS calculation tests BEFORE implementing
- **Rationale**: Financial accuracy is critical, tests define correct behavior

**After Implementation**:
- **Epic 2 (Dashboard)**: Implement charts first, then test rendering
- **Epic 3 (Transactions)**: Implement UI, then test interactions
- **Epic 6 (Settings)**: Implement CRUD, then test operations

### Next Steps (Story 1.8 - Test Infrastructure Setup)

**Add to Epic 1 before starting development**:

```markdown
### Story 1.8: Test Infrastructure Setup

As a developer,
I want to configure testing frameworks (Vitest, Playwright, React Testing Library),
so that I can write and run tests from Epic 1 onwards.

#### Acceptance Criteria

1. Vitest installed and configured with TypeScript support
2. React Testing Library installed with Next.js compatibility
3. Playwright installed with browser binaries (Chromium, Firefox, WebKit)
4. Test environment configuration: `.env.test` with Supabase test project
5. Test scripts added to `package.json`: `test`, `test:watch`, `test:coverage`, `test:e2e`
6. GitHub Actions workflow configured to run tests on every PR
7. Code coverage reporting enabled (Codecov or similar)
8. Test utilities created: `mockSupabase`, `seedDatabase`, `testHelpers`
9. Example unit test passes: `lib/__tests__/example.test.ts`
10. Example E2E test passes: `e2e/example.spec.ts`
```

---

**This test strategy ensures the SAYERS Finance Dashboard is production-ready with 100% financial accuracy, robust security, and comprehensive quality coverage.**
