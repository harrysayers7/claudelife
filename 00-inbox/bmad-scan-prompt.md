---
date: 2025-10-17 00:00
title: bmad-scan-prompt
aliases: ["BMAD SCAN: COMPREHENSIVE FINANCIAL DASHBOARD"]
linter-yaml-title-alias: "BMAD SCAN: COMPREHENSIVE FINANCIAL DASHBOARD"
date created: Fri, 10 17th 25, 3:26:49 pm
date modified: Fri, 10 17th 25, 8:02:55 pm
---

# BMAD SCAN: COMPREHENSIVE FINANCIAL DASHBOARD

## PROJECT SUMMARY
Building a complete financial management system to track personal spending, business transactions, invoicing, cash flow, budgets, and generate accounting reports (P&L, Balance Sheet, BAS statements for Australian tax).

**Multi-entity tracking**: Personal, MOKAI PTY LTD (cybersecurity consultancy), MOK HOUSE PTY LTD (music production)

## CURRENT STATE
- **Database**: Supabase (project: gshsshaodoyttdxippwx)
- **Data**: 23 tables, ~300 rows (will grow significantly)
  - 256 personal transactions (UpBank integration)
  - 30 business invoices
  - 52 chart of accounts entries
  - ML categorization, anomaly detection, forecasting built-in
- **Confirmed Stack**:
  - UI: shadcn/ui v4 (verified via MCP)
  - Deployment: Vercel (free tier preferred)
  - Data refresh: Polling every 10 minutes (real-time nice-to-have)

## FEATURES (6 PHASES)

### PHASE 1: TRANSACTION & SPENDING (MVP)
Unified transaction view, multi-entity filtering, category breakdown, search/filters, project tracking

### PHASE 2: INVOICING & CASH FLOW
Invoice management, payment tracking, cash flow dashboard, forecasting, overdue alerts

### PHASE 3: BUDGETING & ALERTS
Budget creation, budget vs actual, spending alerts, recurring transaction tracking, anomaly detection

### PHASE 4: ACCOUNTING & REPORTING
P&L, Balance Sheet, BAS statement generation, chart of accounts, tax deductibility, multi-entity comparison

### PHASE 5: ANALYTICS & ML INSIGHTS
AI insights dashboard, spending trends, category optimization, payment behavior analysis, risk scoring

### PHASE 6: POLISH & UX
Export (CSV/PDF/Excel), mobile responsive, dark mode, keyboard shortcuts, bulk actions

## KEY ARCHITECTURAL QUESTIONS

### CRITICAL DECISIONS NEEDED:
1. **Framework**: Next.js 14 App Router (SSR, Server Components) vs Vite + React (SPA)?
   - Complex dashboard with many charts/tables/reports
   - Need efficient data fetching for 23 tables
   - Vercel deployment (Next.js optimized)

2. **Data Fetching**:
   - React Query (client-side caching + polling)?
   - Server Components for initial load?
   - How to avoid N+1 queries across 23 tables?
   - Best pattern for Supabase + 10-minute polling?

3. **Chart Library**:
   - Recharts (shadcn default)?
   - Tremor (dashboard-focused)?
   - Chart.js? D3.js?

4. **State Management**:
   - React Query + Context sufficient?
   - Zustand for global UI state?
   - Or overkill for this use case?

5. **Table Component**:
   - TanStack Table (powerful, complex)?
   - shadcn Data Table (simpler)?
   - Need: sorting, filtering, virtual scrolling for large datasets

6. **Form Handling**:
   - React Hook Form + Zod for type-safe validation?
   - Server Actions for invoice creation?

7. **Type Safety**:
   - Generate TS types from Supabase schema?
   - Maintain type safety across 23 tables?
   - Runtime validation strategy?

8. **Performance**:
   - Code splitting for 6 phases?
   - Lazy loading charts?
   - Virtual scrolling for transaction lists?
   - Report caching strategy?

9. **Auth & Security**:
   - Supabase Auth?
   - RLS policies for multi-entity data?
   - How to securely handle financial data?

10. **Testing**:
    - Financial accuracy critical - how much testing needed?
    - Unit, integration, E2E strategy?

## SUCCESS METRICS
- Fast load (<2s initial)
- Smooth interactions with large datasets
- Accurate financial calculations (BAS, P&L, Balance Sheet)
- Easy to extend (6-phase roadmap)
- Type-safe throughout
- Production-ready architecture

## AVAILABLE TOOLS
- **shadcn MCP**: Get component source code
- **Context7 MCP**: Library documentation
- **Supabase MCP**: Database operations
- **Task Master**: Project/task management

## WHAT BMAD SHOULD DELIVER
1. Framework recommendation (Next.js vs Vite) with reasoning
2. Complete tech stack with specific library versions
3. Project structure (folder organization, component architecture)
4. Data fetching strategy for Supabase + polling
5. State management approach
6. Type safety implementation plan
7. Performance optimization strategy
8. Testing approach for financial accuracy
9. Phased implementation roadmap
10. Potential gotchas and how to avoid them

**Focus**: Architecture that scales from MVP to full 6-phase system while maintaining type safety, performance, and financial accuracy.
