---
date: "2025-10-17"
phase: 3
duration: "2 weeks"
status: "Ready for Implementation"
priority: "Should Have"
dependencies: ["Phase 1-2 Complete"]
---

# Phase 3: Budgeting & Alerts
## Implementation Guide

---

## Phase Overview

Add budget creation, tracking, and intelligent alerts for overspending and anomalies. This phase helps users proactively manage finances through budget limits and AI-powered anomaly detection.

**Duration**: 2 weeks
- Week 1: Budget creation and tracking
- Week 2: Alerts (budget limits, anomalies)

**Success Criteria**: Users can set category budgets, see budget vs actual progress, and receive alerts for overspending and unusual transactions.

---

## User Stories from PRD

### Epic 3.1: Budget Creation & Tracking

#### Story 3.1.1: Create Budgets
**As a** user
**I want to** set monthly budgets by category
**So that** I can control spending

**Acceptance Criteria**:
- [ ] Budget form with category selector and amount
- [ ] Support multiple time periods (weekly/monthly/yearly)
- [ ] Copy budgets from previous period
- [ ] Entity-specific budgets

**Priority**: Should Have
**Dependencies**: Phase 1 (Story 1.2.1 - Category Breakdown)

---

#### Story 3.1.2: Budget vs Actual
**As a** user
**I want to** compare budget to actual spending
**So that** I can track financial discipline

**Acceptance Criteria**:
- [ ] Progress bars showing percentage spent
- [ ] Color coding (green/yellow/red based on threshold)
- [ ] Show remaining budget
- [ ] Trend indicator (on track/over budget/under budget)

**Priority**: Should Have
**Dependencies**: Story 3.1.1

---

### Epic 3.2: Spending Alerts

#### Story 3.2.1: Budget Alert System
**As a** user
**I want to** receive alerts at 80% and 100% of budget
**So that** I can adjust spending proactively

**Acceptance Criteria**:
- [ ] Dashboard notification badge
- [ ] Alert list with category and percentage
- [ ] Dismissible notifications
- [ ] Email alerts (optional, future)

**Priority**: Could Have
**Dependencies**: Story 3.1.2

---

### Epic 3.3: Anomaly Detection

#### Story 3.3.1: Anomaly Alerts
**As a** user
**I want to** see transactions flagged as anomalies
**So that** I can catch errors or fraud

**Acceptance Criteria**:
- [ ] Use anomaly_score from ML pipeline
- [ ] Show anomalies on dashboard
- [ ] Explain why transaction is flagged
- [ ] Allow marking as normal/fraud

**Priority**: Should Have
**Dependencies**: Phase 1 (Story 1.1.1 - Transactions)

---

## Technical Requirements

### Route Structure

```
app/(dashboard)/budgets/
├── page.tsx                # Budget list
├── new/page.tsx            # Create budget
└── components/
    ├── BudgetCard.tsx      # Budget progress card
    ├── BudgetForm.tsx      # Create/edit budget
    └── ProgressBar.tsx     # Budget progress indicator

components/dashboard/
├── AlertBanner.tsx         # Updated with budget alerts
└── AnomalyAlert.tsx        # Anomaly display component
```

---

### Budget Schema

```typescript
// lib/validations/budget.ts
import { z } from 'zod'

export const budgetSchema = z.object({
  entity_id: z.string().uuid(),
  category_id: z.string().uuid(),
  amount: z.number().positive(), // In cents
  period: z.enum(['weekly', 'monthly', 'quarterly', 'yearly']),
  start_date: z.date(),
  end_date: z.date(),
}).refine((data) => data.end_date > data.start_date, {
  message: 'End date must be after start date',
  path: ['end_date'],
})
```

---

### Budget Progress Calculation

```typescript
// lib/calculations/budget-progress.ts
import Decimal from 'decimal.js'

export function calculateBudgetProgress(
  budgetAmountCents: number,
  spentAmountCents: number
): {
  percentage: number
  remaining: number
  status: 'on-track' | 'warning' | 'over-budget'
} {
  const percentage = new Decimal(spentAmountCents)
    .div(budgetAmountCents)
    .mul(100)
    .toNumber()

  const remaining = budgetAmountCents - spentAmountCents

  const status =
    percentage >= 100 ? 'over-budget' :
    percentage >= 80 ? 'warning' :
    'on-track'

  return { percentage, remaining, status }
}
```

---

### Anomaly Detection Display

```typescript
// components/dashboard/AnomalyAlert.tsx
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'

export function AnomalyAlert({ anomaly }: { anomaly: AnomalyDetection }) {
  const severityColor =
    anomaly.severity === 'high' ? 'destructive' :
    anomaly.severity === 'medium' ? 'default' :
    'secondary'

  return (
    <Alert variant={severityColor}>
      <AlertTitle>Unusual Transaction Detected</AlertTitle>
      <AlertDescription>
        <p>{anomaly.transaction.description} - {formatCurrency(anomaly.transaction.amount)}</p>
        <p className="text-sm text-muted-foreground">{anomaly.explanation}</p>
        <div className="mt-2 flex gap-2">
          <Button size="sm" onClick={() => markAsNormal(anomaly.id)}>
            Mark as Normal
          </Button>
          <Button size="sm" variant="destructive" onClick={() => markAsFraud(anomaly.id)}>
            Report Fraud
          </Button>
        </div>
      </AlertDescription>
    </Alert>
  )
}
```

---

## UI Specifications

### Budget Progress Card

```
┌──────────────────────────────┐
│ Office Supplies              │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│ $450 / $500 (90%)            │  <- Yellow (warning)
│ $50 remaining                │
│ ⚠️ 90% of budget used        │
└──────────────────────────────┘

┌──────────────────────────────┐
│ Marketing                    │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│ $1,200 / $1,000 (120%)       │  <- Red (over budget)
│ -$200 over budget            │
│ 🚨 Budget exceeded           │
└──────────────────────────────┘
```

**Progress Bar Colors**:
- 0-79%: Green (`bg-green-500`)
- 80-99%: Yellow (`bg-amber-500`)
- 100%+: Red (`bg-red-500`)

---

## Implementation Checklist

### Week 1: Budget Creation & Tracking (Days 1-5)

- [ ] Create budget schema (Zod validation)
- [ ] Implement budget creation form
- [ ] Add category selector (from Phase 1)
- [ ] Support weekly/monthly/quarterly/yearly periods
- [ ] Implement "copy from previous period" feature
- [ ] Calculate budget progress (spent vs limit)
- [ ] Display budget cards with progress bars
- [ ] Test budget creation and tracking

---

### Week 2: Alerts & Anomaly Detection (Days 6-10)

- [ ] Implement budget alert system (80%, 100% thresholds)
- [ ] Add notification badge to dashboard
- [ ] Display alert list (dismissible)
- [ ] Query anomaly_detections table (ML pipeline)
- [ ] Display anomaly alerts on dashboard
- [ ] Add "mark as normal/fraud" actions
- [ ] Store user feedback for ML model improvement (future)
- [ ] Test alert triggers
- [ ] Deploy Phase 3 to production

---

## Dependencies

### From Previous Phases
- [ ] Phase 1: Transaction categories
- [ ] Phase 1: Dashboard layout
- [ ] Phase 2: Entity budgets

### External
- **ML Pipeline**: Anomaly detection scores (MindsDB)
- **Supabase Tables**: `budgets` (may need to create), `anomaly_detections`

---

## Success Criteria

### Functional ✅
- [ ] Users can create budgets by category
- [ ] Budget vs actual displays correctly
- [ ] Alerts trigger at 80% and 100%
- [ ] Anomalies display with explanations
- [ ] User can mark anomalies as normal/fraud

### Performance ✅
- [ ] Budget page loads <1 second
- [ ] Alert calculations real-time (<100ms)

### Testing ✅
- [ ] Unit tests for budget progress calculation
- [ ] E2E test for budget creation
- [ ] Component test for progress bars

---

## Next Phase Prerequisites

Before Phase 4 (Accounting):
- [ ] Budget system functional
- [ ] Alerts working correctly
- [ ] Anomaly detection validated
- [ ] No critical bugs

---

**Phase Owner**: Scrum Master (SM Agent)
**Estimated Effort**: 80 hours (2 weeks × 40 hours)
**Status**: Ready for Sprint Planning
