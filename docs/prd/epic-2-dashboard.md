# Epic 2: Financial Dashboard & Visualization

<!-- Powered by BMAD™ Core -->

## Epic Overview

**Epic Goal**: Transform the placeholder dashboard landing page into a fully functional financial overview interface that displays real-time KPIs calculated from Supabase transaction data, renders interactive charts showing revenue/expense trends and category breakdowns using Recharts, presents recent transactions with ML prediction insights, and surfaces anomaly alerts with drill-down capability.

**Dependencies**: Epic 1 (Foundation & Core Infrastructure) must be completed

**Success Criteria**:
- Real-time KPIs displaying accurate financial metrics from Supabase
- Interactive charts (trend, category breakdown) rendering properly
- Recent transactions widget showing ML predictions with confidence scores
- Anomaly alerts surfacing high-risk transactions
- Date range selector filtering all dashboard data
- Responsive layout working across all device sizes

---

## User Stories

### Story 2.1: KPI Calculation & Display Components
### Story 2.2: Revenue & Expense Trend Chart
### Story 2.3: Category Breakdown Pie Chart
### Story 2.4: Recent Transactions Widget with ML Insights
### Story 2.5: Anomaly Alerts Section with Drill-Down
### Story 2.6: Dashboard Date Range Selector & Filter Logic
### Story 2.7: Dashboard Responsive Layout & Mobile Optimization

---

## Key Technical Implementation

**Data Sources**:
- `personal_transactions` table (UpBank sync data)
- `invoices` table (receivables/payables)
- `ai_predictions` table (ML categorization confidence)
- `anomaly_detections` table (ML anomaly scores)

**Visualization Library**: Recharts 2.10+
- `<LineChart>` for revenue/expense trends
- `<PieChart>` for category breakdown
- `<ResponsiveContainer>` for responsive sizing

**KPI Calculations**:
- Revenue: SUM(transactions WHERE amount > 0 OR category IN revenue_categories)
- Expenses: SUM(transactions WHERE amount < 0 OR category IN expense_categories)
- Profit/Loss: Revenue - Expenses
- Cash Flow: SUM(bank_account balances)

**ML Integration**:
- Display `ai_category` with `ai_confidence` score
- Highlight low confidence (<0.7) predictions for review
- Surface anomalies with `anomaly_score > 0.7`

---

## Epic Dependencies

- **Requires**: Epic 1 (authentication, entity context, Supabase integration)
- **Blocks**: None (dashboard is independent from other features)

## Testing Requirements

**Unit Tests**:
- KPI calculation functions (revenue, expenses, profit/loss)
- Date range filtering logic
- Currency formatting utilities

**Integration Tests**:
- Chart components render with mock data
- Date range selector triggers data refresh
- Entity switching updates all dashboard widgets

**E2E Tests**:
- Full dashboard load flow with real data
- Date range selection updates all widgets
- Responsive layout on mobile/tablet/desktop

## Definition of Done

- [ ] All 7 stories completed
- [ ] KPIs display accurate real-time data
- [ ] Charts render without performance issues
- [ ] ML predictions visible with confidence indicators
- [ ] Anomaly alerts functional with drill-down
- [ ] Date range filtering works across all widgets
- [ ] Responsive layout tested on all breakpoints
- [ ] Chart accessibility verified (WCAG AA)

---

**Epic Status**: Ready for Implementation
**Estimated Effort**: 7-10 days
**Priority**: P1 (High - Core Feature)
