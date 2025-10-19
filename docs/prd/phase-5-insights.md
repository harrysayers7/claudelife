---
date: "2025-10-17"
phase: 5
duration: "2 weeks"
status: "Ready for Implementation"
priority: "Should Have"
dependencies: ["Phase 1-4 Complete"]
---

# Phase 5: Analytics & ML Insights
## Implementation Guide

---

## Phase Overview

Leverage existing ML pipeline (MindsDB) to display AI-generated insights, spending trends, and predictions. This phase surfaces actionable intelligence from the financial data collected in Phases 1-4.

**Duration**: 2 weeks
- Week 1: Insights dashboard, trend analysis
- Week 2: Predictive analytics, advanced visualizations

**Success Criteria**: Users see ML-powered insights on spending patterns, anomalies, and cash flow predictions with confidence scores.

---

## User Stories from PRD

### Epic 5.1: AI Insights Dashboard

#### Story 5.1.1: Insight Display
**As a** user
**I want to** see AI-generated financial insights on my dashboard
**So that** I can make better financial decisions

**Acceptance Criteria**:
- [ ] Display insights from ai_insights table
- [ ] Show insight type, description, confidence
- [ ] Prioritize high-confidence insights (>0.8)
- [ ] Link to relevant data (transaction/category)

**Priority**: Should Have
**Dependencies**: None (ML pipeline pre-existing)

---

### Epic 5.2: Spending Trends & Predictions

#### Story 5.2.1: Trend Analysis
**As a** user
**I want to** see spending trends by category over time
**So that** I can identify patterns and seasonal changes

**Acceptance Criteria**:
- [ ] Line charts showing historical trends
- [ ] Identify seasonal patterns
- [ ] Show year-over-year comparison
- [ ] Highlight significant changes (>20% variance)

**Priority**: Should Have
**Dependencies**: Phase 1 (Category data)

---

#### Story 5.2.2: Predictive Spending
**As a** user
**I want to** see predicted future spending by category
**So that** I can anticipate financial needs

**Acceptance Criteria**:
- [ ] Use ML predictions from ai_predictions table
- [ ] Show confidence intervals
- [ ] Explain prediction basis
- [ ] Update monthly based on new data

**Priority**: Could Have
**Dependencies**: Story 5.2.1

---

## Technical Requirements

### Route Structure

```
app/(dashboard)/insights/
├── page.tsx                # Insights dashboard
├── trends/page.tsx         # Trend analysis
├── anomalies/page.tsx      # Anomaly details (from Phase 3)
└── forecasts/page.tsx      # Cash flow forecasts

components/insights/
├── InsightCard.tsx         # AI insight display
├── TrendChart.tsx          # Historical trend visualization
└── PredictionChart.tsx     # Future prediction with confidence
```

---

### Data Fetching (ML Tables)

```typescript
// hooks/use-ml-insights.ts
import { useQuery } from '@tanstack/react-query'
import { supabase } from '@/lib/supabase/client'

export function useMLInsights(entityId?: string) {
  return useQuery({
    queryKey: ['insights', entityId],
    queryFn: async () => {
      const query = supabase
        .from('ai_insights')
        .select('*')
        .order('confidence', { ascending: false })
        .gte('confidence', 0.8) // High-confidence only

      if (entityId) {
        query.eq('entity_id', entityId)
      }

      const { data, error } = await query
      if (error) throw error
      return data
    },
    staleTime: 60 * 60 * 1000, // 1 hour (insights update infrequently)
  })
}
```

---

### Insight Display

```typescript
// components/insights/InsightCard.tsx
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

export function InsightCard({ insight }: { insight: AIInsight }) {
  const typeIcon =
    insight.insight_type === 'spending_pattern' ? '📊' :
    insight.insight_type === 'cost_saving' ? '💰' :
    insight.insight_type === 'risk_alert' ? '⚠️' :
    '🔍'

  const priorityColor =
    insight.priority === 'high' ? 'destructive' :
    insight.priority === 'medium' ? 'default' :
    'secondary'

  return (
    <Card>
      <CardHeader>
        <div className="flex justify-between items-start">
          <div className="flex gap-2 items-center">
            <span className="text-2xl">{typeIcon}</span>
            <CardTitle>{insight.title}</CardTitle>
          </div>
          <Badge variant={priorityColor}>{insight.priority}</Badge>
        </div>
        <CardDescription>
          Confidence: {(insight.confidence * 100).toFixed(0)}%
        </CardDescription>
      </CardHeader>
      <CardContent>
        <p>{insight.description}</p>
        {insight.related_data && (
          <div className="mt-4">
            <Button variant="link" onClick={() => viewRelatedData(insight.related_data)}>
              View Details →
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
```

---

### Trend Analysis

```typescript
// lib/analytics/trend-analysis.ts
import Decimal from 'decimal.js'

export interface TrendData {
  period: string // "2025-01", "2025-02"
  amount: number
  percentChange: number
  isSignificant: boolean // >20% change
}

export async function analyzeCategoryTrend(
  categoryId: string,
  entityId: string,
  months: number = 12
): Promise<TrendData[]> {
  const supabase = await createClient()

  // Fetch transactions grouped by month
  const { data: transactions } = await supabase
    .from('transactions')
    .select('transaction_date, amount')
    .eq('category_id', categoryId)
    .eq('entity_id', entityId)
    .gte('transaction_date', getStartDate(months))
    .order('transaction_date', { ascending: true })

  // Group by month
  const monthlyData = groupByMonth(transactions)

  // Calculate percent change month-over-month
  return monthlyData.map((data, i) => {
    if (i === 0) {
      return { ...data, percentChange: 0, isSignificant: false }
    }

    const prevAmount = monthlyData[i - 1].amount
    const percentChange = new Decimal(data.amount)
      .minus(prevAmount)
      .div(prevAmount)
      .mul(100)
      .toNumber()

    return {
      ...data,
      percentChange,
      isSignificant: Math.abs(percentChange) > 20,
    }
  })
}
```

---

## UI Specifications

### Insights Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│ AI Insights                                    [Last 30 Days ▼] │
├─────────────────────────────────────────────────────────────────┤
│ ┌──────────────────────┐ ┌───────────────────────────────────┐ │
│ │ 💰 Cost Saving       │ │ 📊 Spending Pattern               │ │
│ │ Opportunity          │ │ Detected                           │ │
│ │                      │ │                                   │ │
│ │ You could save       │ │ Office supplies spending          │ │
│ │ $200/month by        │ │ increased 35% this month.         │ │
│ │ switching to vendor  │ │ Consider reviewing contracts.     │ │
│ │ X for software.      │ │                                   │ │
│ │ Confidence: 85%      │ │ Confidence: 92%                   │ │
│ │ [View Details →]     │ │ [View Details →]                  │ │
│ └──────────────────────┘ └───────────────────────────────────┘ │
│                                                                  │
│ ┌──────────────────────────────────────────────────────────────┐│
│ │ Spending Trends - Marketing                                 ││
│ │ ┌────────────────────────────────────────────────────────┐  ││
│ │ │  $3000                                                  │  ││
│ │ │  $2500 ─┬─────────────────────────────────────────────│  ││
│ │ │  $2000  │      ╱╲                                      │  ││
│ │ │  $1500  │     ╱  ╲    ╱╲                              │  ││
│ │ │  $1000  ├────╱────╲──╱──╲─────────────────────────────│  ││
│ │ │  $500   │                                              │  ││
│ │ │  $0 ────┴──────────────────────────────────────────────│  ││
│ │ │        Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec │  ││
│ │ └────────────────────────────────────────────────────────┘  ││
│ │ ⚠️ Significant increase in March (+35%)                    ││
│ └──────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

### Prediction Chart with Confidence

```typescript
// components/insights/PredictionChart.tsx
import { Line, Area, ComposedChart, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

export function PredictionChart({ data }: { data: PredictionData[] }) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <ComposedChart data={data}>
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />

        {/* Historical data (solid line) */}
        <Line
          type="monotone"
          dataKey="actual"
          stroke="hsl(217.2, 91.2%, 59.8%)"
          strokeWidth={2}
        />

        {/* Predicted data (dashed line) */}
        <Line
          type="monotone"
          dataKey="predicted"
          stroke="hsl(217.2, 91.2%, 59.8%)"
          strokeWidth={2}
          strokeDasharray="5 5"
        />

        {/* Confidence interval (shaded area) */}
        <Area
          type="monotone"
          dataKey="confidenceHigh"
          stroke="none"
          fill="hsl(217.2, 91.2%, 59.8%)"
          fillOpacity={0.2}
        />
        <Area
          type="monotone"
          dataKey="confidenceLow"
          stroke="none"
          fill="hsl(217.2, 91.2%, 59.8%)"
          fillOpacity={0.2}
        />
      </ComposedChart>
    </ResponsiveContainer>
  )
}
```

---

## Implementation Checklist

### Week 1: Insights Dashboard & Trends (Days 1-5)

- [ ] Fetch insights from ai_insights table (MindsDB)
- [ ] Implement InsightCard component
- [ ] Display insights on dashboard (prioritize high-confidence)
- [ ] Implement TrendChart component (Recharts line chart)
- [ ] Calculate month-over-month percent change
- [ ] Highlight significant changes (>20% variance)
- [ ] Test with existing ML data (7 models in ml_models table)

---

### Week 2: Predictions & Advanced Analytics (Days 6-10)

- [ ] Fetch predictions from ai_predictions table
- [ ] Implement PredictionChart with confidence intervals
- [ ] Display cash flow forecasts (from cash_flow_forecasts table)
- [ ] Add year-over-year comparison
- [ ] Implement seasonal pattern detection
- [ ] Test prediction accuracy (compare to actual data)
- [ ] Deploy Phase 5 to production

---

## Dependencies

### From Previous Phases
- [ ] Phase 1: Transaction and category data
- [ ] Phase 2: Cash flow data

### External
- **MindsDB ML Pipeline**: Existing (7 models in ml_models table)
- **Supabase Tables**: `ai_insights`, `ai_predictions`, `cash_flow_forecasts`, `ml_models`

---

## Success Criteria

### Functional ✅
- [ ] AI insights display on dashboard
- [ ] Trend charts show historical patterns
- [ ] Predictions display with confidence intervals
- [ ] Significant changes highlighted (>20%)

### Performance ✅
- [ ] Insights load <1 second
- [ ] Charts render <100ms

### Testing ✅
- [ ] Component tests for insight cards
- [ ] E2E test for insights dashboard
- [ ] Validate prediction accuracy (compare to actuals)

---

## Next Phase Prerequisites

Before Phase 6 (Polish):
- [ ] Insights dashboard functional
- [ ] Trends and predictions validated
- [ ] No critical bugs
- [ ] ML pipeline integration verified

---

**Phase Owner**: Scrum Master (SM Agent)
**Estimated Effort**: 80 hours (2 weeks × 40 hours)
**Status**: Ready for Sprint Planning
