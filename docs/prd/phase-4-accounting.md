---
date: "2025-10-17"
phase: 4
duration: "3 weeks"
status: "Ready for Implementation"
priority: "Must Have - Compliance"
dependencies: ["Phase 1-3 Complete"]
---

# Phase 4: Accounting & Reporting
## Implementation Guide

---

## Phase Overview

Implement comprehensive financial reporting (P&L, Balance Sheet, BAS) and chart of accounts management. This phase is CRITICAL for Australian tax compliance and provides professional-grade accounting features.

**Duration**: 3 weeks
- Week 1: P&L and Balance Sheet
- Week 2: BAS (Business Activity Statement) - Australian tax
- Week 3: Chart of Accounts, export, testing with accountant

**Success Criteria**: Generate accurate P&L, Balance Sheet, and BAS reports that match ATO requirements and accountant verification.

---

## User Stories from PRD

### Epic 4.1: Profit & Loss Statement

#### Story 4.1.1: P&L Report Generation ⭐ CRITICAL
**As a** business owner
**I want to** generate P&L statements for any date range
**So that** I can understand business profitability

**Acceptance Criteria**:
- [ ] Calculate revenue (income accounts)
- [ ] Calculate expenses (expense accounts)
- [ ] Show gross profit, operating profit, net profit
- [ ] Compare to previous period
- [ ] Export to PDF/Excel

**Priority**: Must Have
**Dependencies**: None

---

#### Story 4.1.2: Multi-Entity P&L Comparison
**As a** user
**I want to** compare P&L across entities
**So that** I can see which business is most profitable

**Acceptance Criteria**:
- [ ] Side-by-side comparison table
- [ ] Highlight variance (positive/negative)
- [ ] Consolidate all entities option
- [ ] Drill down to account level

**Priority**: Should Have
**Dependencies**: Story 4.1.1

---

### Epic 4.2: Balance Sheet

#### Story 4.2.1: Balance Sheet Report ⭐ CRITICAL
**As a** business owner
**I want to** generate balance sheets for any date
**So that** I can understand financial position

**Acceptance Criteria**:
- [ ] Calculate from accounts table (52 accounts)
- [ ] Show current balances
- [ ] Group by account type (asset/liability/equity)
- [ ] Verify accounting equation (Assets = Liabilities + Equity)

**Priority**: Must Have
**Dependencies**: None

---

### Epic 4.3: BAS Statement Generation

#### Story 4.3.1: BAS Calculation ⭐ CRITICAL (Australian Tax)
**As an** Australian business owner
**I want to** calculate GST for BAS quarterly reporting
**So that** I comply with ATO requirements

**Acceptance Criteria**:
- [ ] Calculate GST collected (sales)
- [ ] Calculate GST paid (purchases)
- [ ] Compute net GST owing/refund
- [ ] Match ATO BAS form structure
- [ ] Include all required fields (G1, 1A, 1B, etc.)

**Priority**: Must Have
**Dependencies**: Phase 1 (Transactions)

---

#### Story 4.3.2: Export BAS for ATO Lodgment ⭐ CRITICAL
**As a** business owner
**I want to** export BAS in ATO-compatible format
**So that** I can lodge with the tax office

**Acceptance Criteria**:
- [ ] Generate PDF matching ATO form
- [ ] Include all required metadata
- [ ] Validate calculations
- [ ] Provide export for accountant review

**Priority**: Must Have
**Dependencies**: Story 4.3.1

---

### Epic 4.4: Chart of Accounts

#### Story 4.4.1: Account List View
**As a** user
**I want to** see all accounts with balances
**So that** I can verify financial accuracy

**Acceptance Criteria**:
- [ ] Display 52 accounts from accounts table
- [ ] Show current balance, account type, description
- [ ] Sort by type, name, balance
- [ ] Search by account name/code

**Priority**: Should Have
**Dependencies**: None

---

#### Story 4.4.2: Account Transaction History
**As a** user
**I want to** see all transactions for an account
**So that** I can audit account activity

**Acceptance Criteria**:
- [ ] Drill down from account to transactions
- [ ] Show running balance
- [ ] Filter by date range
- [ ] Export to CSV

**Priority**: Should Have
**Dependencies**: Story 4.4.1

---

## Technical Requirements

### Route Structure

```
app/(dashboard)/reports/
├── page.tsx                    # Reports dashboard
├── profit-loss/page.tsx        # P&L generator
├── balance-sheet/page.tsx      # Balance sheet
├── bas/page.tsx                # BAS calculator
└── components/
    ├── DateRangePicker.tsx     # Date range selector
    └── ReportCard.tsx          # Report display

app/api/reports/
├── profit-loss/route.ts        # POST - Generate P&L
├── balance-sheet/route.ts      # POST - Generate Balance Sheet
└── bas/route.ts                # POST - Generate BAS
```

---

### P&L Calculation (CRITICAL)

```typescript
// lib/calculations/profit-loss.ts
import Decimal from 'decimal.js'

export interface ProfitLoss {
  revenue: number // In cents
  costOfGoodsSold: number
  grossProfit: number
  operatingExpenses: number
  operatingProfit: number
  otherIncome: number
  otherExpenses: number
  netProfit: number
}

export async function calculateProfitLoss(
  entityId: string,
  startDate: Date,
  endDate: Date
): Promise<ProfitLoss> {
  const supabase = await createClient()

  // Fetch transactions for date range
  const { data: transactions } = await supabase
    .from('transactions')
    .select('*, account:accounts(*)')
    .eq('entity_id', entityId)
    .gte('transaction_date', startDate.toISOString())
    .lte('transaction_date', endDate.toISOString())

  // Sum by account type
  const revenue = sumAccountType(transactions, 'income')
  const expenses = sumAccountType(transactions, 'expense')
  const cogs = sumAccountCategory(transactions, 'cost_of_goods_sold')

  const grossProfit = new Decimal(revenue).minus(cogs).toNumber()
  const operatingExpenses = new Decimal(expenses).minus(cogs).toNumber()
  const operatingProfit = new Decimal(grossProfit).minus(operatingExpenses).toNumber()
  const netProfit = operatingProfit // Simplified for MVP

  return {
    revenue,
    costOfGoodsSold: cogs,
    grossProfit,
    operatingExpenses,
    operatingProfit,
    otherIncome: 0,
    otherExpenses: 0,
    netProfit,
  }
}
```

---

### Balance Sheet Calculation (CRITICAL)

```typescript
// lib/calculations/balance-sheet.ts
import Decimal from 'decimal.js'

export interface BalanceSheet {
  assets: {
    current: number
    fixed: number
    total: number
  }
  liabilities: {
    current: number
    longTerm: number
    total: number
  }
  equity: {
    capital: number
    retainedEarnings: number
    total: number
  }
  balances: boolean // Assets = Liabilities + Equity
}

export async function calculateBalanceSheet(
  entityId: string,
  asOfDate: Date
): Promise<BalanceSheet> {
  const supabase = await createClient()

  // Fetch all accounts with balances
  const { data: accounts } = await supabase
    .from('accounts')
    .select('*')
    .eq('entity_id', entityId)

  const currentAssets = sumAccountCategory(accounts, 'current_asset')
  const fixedAssets = sumAccountCategory(accounts, 'fixed_asset')
  const currentLiabilities = sumAccountCategory(accounts, 'current_liability')
  const longTermLiabilities = sumAccountCategory(accounts, 'long_term_liability')
  const capital = sumAccountCategory(accounts, 'equity')

  const totalAssets = new Decimal(currentAssets).plus(fixedAssets).toNumber()
  const totalLiabilities = new Decimal(currentLiabilities).plus(longTermLiabilities).toNumber()
  const totalEquity = new Decimal(capital).toNumber()

  // Verify accounting equation
  const balances = new Decimal(totalAssets)
    .equals(new Decimal(totalLiabilities).plus(totalEquity))

  return {
    assets: {
      current: currentAssets,
      fixed: fixedAssets,
      total: totalAssets,
    },
    liabilities: {
      current: currentLiabilities,
      longTerm: longTermLiabilities,
      total: totalLiabilities,
    },
    equity: {
      capital,
      retainedEarnings: 0, // Calculate from P&L
      total: totalEquity,
    },
    balances,
  }
}
```

---

### BAS Calculation (CRITICAL - Australian Tax)

```typescript
// lib/calculations/bas.ts
import Decimal from 'decimal.js'

export interface BASStatement {
  quarter: string // "Q1 2025"
  entityId: string
  gstCollected: number // G1 - Total sales (inc GST)
  gstOnSales: number // 1A - GST on sales
  gstPaid: number // G10 - Total purchases (inc GST)
  gstOnPurchases: number // 1B - GST on purchases
  netGST: number // 1A minus 1B (owing if positive, refund if negative)
}

export async function calculateBAS(
  entityId: string,
  quarter: { start: Date; end: Date }
): Promise<BASStatement> {
  const supabase = await createClient()

  // Fetch all transactions for quarter
  const { data: transactions } = await supabase
    .from('transactions')
    .select('*')
    .eq('entity_id', entityId)
    .gte('transaction_date', quarter.start.toISOString())
    .lte('transaction_date', quarter.end.toISOString())

  // Separate income (sales) and expenses (purchases)
  const sales = transactions.filter(t => t.type === 'income')
  const purchases = transactions.filter(t => t.type === 'expense')

  // Calculate GST (10% Australian rate)
  const gstCollected = sumAmounts(sales)
  const gstOnSales = new Decimal(gstCollected).div(11).toNumber() // GST = Amount / 11

  const gstPaid = sumAmounts(purchases)
  const gstOnPurchases = new Decimal(gstPaid).div(11).toNumber()

  const netGST = new Decimal(gstOnSales).minus(gstOnPurchases).toNumber()

  return {
    quarter: formatQuarter(quarter.start),
    entityId,
    gstCollected,
    gstOnSales,
    gstPaid,
    gstOnPurchases,
    netGST,
  }
}
```

---

## UI Specifications

### P&L Report Display

```
Profit & Loss Statement
MOKAI PTY LTD
July 1, 2025 - September 30, 2025 (Q1 FY2026)

Revenue                          $45,000.00
Cost of Goods Sold              -$12,000.00
────────────────────────────────────────
Gross Profit                     $33,000.00

Operating Expenses
  Marketing                       -$5,000.00
  Software                        -$2,500.00
  Office                          -$1,200.00
────────────────────────────────────────
Total Operating Expenses         -$8,700.00

Operating Profit                 $24,300.00

Net Profit                       $24,300.00
════════════════════════════════════════
```

---

### BAS Form (ATO Format)

```
Business Activity Statement
ABN: 12 345 678 901
Quarter: Q3 2025 (Jul-Sep)

G1  Total Sales (inc GST)         $110,000.00
1A  GST on Sales                   $10,000.00

G10 Total Purchases (inc GST)      $55,000.00
1B  GST on Purchases                $5,000.00

Net GST (1A - 1B)                   $5,000.00
                                   ══════════
Amount Owing to ATO                 $5,000.00
```

---

## Implementation Checklist

### Week 1: P&L & Balance Sheet (Days 1-5)

- [ ] Implement P&L calculation (lib/calculations/profit-loss.ts)
- [ ] Test P&L against manual calculations (100% accuracy)
- [ ] Implement Balance Sheet calculation (lib/calculations/balance-sheet.ts)
- [ ] Validate accounting equation (Assets = Liabilities + Equity)
- [ ] Create report display components
- [ ] Add date range picker
- [ ] Test with accountant (Phase 4 prerequisite)

---

### Week 2: BAS (Australian Tax) (Days 6-10)

- [ ] Implement BAS calculation (lib/calculations/bas.ts)
- [ ] Test GST formulas (Amount / 11 for inclusive pricing)
- [ ] Create BAS form UI (match ATO structure)
- [ ] Validate all required fields (G1, 1A, G10, 1B)
- [ ] Generate BAS PDF (ATO format)
- [ ] Test with accountant for ATO compliance

---

### Week 3: Chart of Accounts & Export (Days 11-15)

- [ ] Display 52 accounts from accounts table
- [ ] Implement account drill-down (transactions per account)
- [ ] Add running balance calculation
- [ ] Implement export to PDF (all reports)
- [ ] Implement export to Excel (CSV format)
- [ ] Final testing with accountant
- [ ] Deploy Phase 4 to production

---

## Dependencies

### From Previous Phases
- [ ] Phase 1: Transaction data
- [ ] Phase 2: Invoice data
- [ ] Supabase Tables: `accounts` (52 rows), `transactions`, `invoices`

### External
- **Accountant Review**: CRITICAL - Must verify all calculations before production
- **ATO BAS Form**: Reference ATO website for latest form structure

---

## Success Criteria (CRITICAL)

### Functional ✅
- [ ] P&L matches accountant manual calculation (100% accuracy)
- [ ] Balance Sheet balances (Assets = Liabilities + Equity)
- [ ] BAS matches ATO requirements (G1, 1A, 1B fields)
- [ ] All reports export to PDF/Excel

### Compliance ✅
- [ ] **Accountant sign-off** on P&L, Balance Sheet, BAS
- [ ] BAS format matches ATO form
- [ ] GST calculation correct (10% Australian rate)

### Performance ✅
- [ ] Report generation <2 seconds
- [ ] Export to PDF <2 seconds

### Testing ✅
- [ ] 100% test coverage for all financial calculations
- [ ] Integration test with accountant review
- [ ] E2E test for report generation

---

## Risks & Mitigation

### Risk 1: Financial Calculation Errors
**Probability**: Medium
**Impact**: CRITICAL (tax compliance, legal issues)
**Mitigation**: 100% test coverage, accountant verification, manual calculation comparison

---

### Risk 2: BAS Non-Compliance with ATO
**Probability**: Low
**Impact**: CRITICAL (penalties, tax issues)
**Mitigation**: ATO form reference, accountant review, quarterly validation

---

## Next Phase Prerequisites

Before Phase 5 (Analytics):
- [ ] **CRITICAL**: Accountant sign-off on all reports
- [ ] P&L, Balance Sheet, BAS fully functional
- [ ] All financial calculations verified (100% accuracy)
- [ ] Export functionality tested
- [ ] No critical bugs

---

**Phase Owner**: Scrum Master (SM Agent)
**Estimated Effort**: 120 hours (3 weeks × 40 hours)
**Status**: Ready for Sprint Planning
**CRITICAL**: Accountant review required before production deployment
