# BMad: Financial Dashboard

Comprehensive financial management system for tracking personal spending, business transactions (MOKAI, MOK HOUSE), invoicing, cash flow, budgets, and generating Australian tax reports.

## Project Type
**Greenfield Fullstack Web Application** (FinTech/Accounting)

## Tech Stack (Confirmed)
- **Framework:** Next.js 14+ (App Router, Server Components)
- **Language:** TypeScript 5.4+
- **Database:** Supabase (project: gshsshaodoyttdxippwx)
- **UI:** shadcn/ui v4 + Tailwind CSS
- **Charts:** Recharts v2.10+
- **Tables:** TanStack Table v8
- **State:** React Query v5 + React Context
- **Forms:** React Hook Form + Zod
- **Testing:** Vitest + Testing Library + Playwright
- **Deployment:** Vercel (free tier)

## Recommended BMad Workflow
**Use:** `.claude/.bmad-core/workflows/greenfield-fullstack.yaml`

## Agent Execution Sequence

### Planning Phase (Weeks 1-2)

#### 1. PM (Product Manager)
**Goal:** Create comprehensive PRD from BMAD scan analysis

**Input:**
- BMAD scan results (@00-inbox/bmad-scan-prompt.md)
- Financial dashboard requirements (@00-inbox/financial-dashboard-requirements.md)

**Tasks:**
- Create detailed PRD covering all 6 phases
- Define acceptance criteria for each phase
- Specify financial calculation requirements
- Document Australian tax compliance needs (BAS)

**Output:** `docs/prd.md`

**Template:** Use `.bmad-core/templates/prd-tmpl.yaml`

---

#### 2. Architect
**Goal:** Design scalable system architecture

**Input:**
- PRD from PM
- Tech stack recommendations (Next.js, Supabase, shadcn)
- 23 existing Supabase tables

**Tasks:**
- Design Next.js folder structure (feature-based)
- Define component hierarchy
- Plan data fetching strategy (Server Components + React Query)
- Design type safety approach (Supabase → TypeScript → Zod)
- Specify performance optimizations (virtual scrolling, caching)

**Output:** `docs/architecture.md`

**Template:** Use `.bmad-core/templates/architecture-tmpl.yaml`

---

#### 3. UX Expert (Recommended)
**Goal:** Create dashboard UI specifications

**Input:**
- PRD + Architecture docs
- Financial dashboard best practices
- shadcn/ui v4 component library

**Tasks:**
- Design dashboard layout (sidebar, header, entity selector)
- Specify chart types for financial data (spending breakdown, cash flow, trends)
- Design form layouts (invoice creation, budget setup)
- Plan responsive breakpoints
- Define dark mode color scheme

**Output:** `docs/front-end-spec.md`

**Template:** Use `.bmad-core/templates/front-end-spec-tmpl.yaml`

---

### Validation Phase (Week 2)

#### 4. PO (Product Owner)
**Goal:** Validate documents and create sharded epics

**Tasks:**
- Run master checklist against PRD/Architecture
- Verify all 6 phases are well-defined
- Shard PRD into phase-specific documents
- Validate financial accuracy requirements
- Ensure Australian tax compliance is addressed

**Outputs:**
- `docs/prd/phase-1-transactions.md`
- `docs/prd/phase-2-invoicing.md`
- `docs/prd/phase-3-budgeting.md`
- `docs/prd/phase-4-accounting.md`
- `docs/prd/phase-5-insights.md`
- `docs/prd/phase-6-polish.md`

---

#### 5. QA (Quality Assurance)
**Goal:** Define testing strategy for financial accuracy

**Input:**
- Architecture + financial calculation requirements
- Risk assessment (financial accuracy critical)

**Tasks:**
- Define test coverage targets (100% for calculations, 80% for components)
- Create test plan for BAS/P&L/Balance Sheet calculations
- Specify E2E test scenarios (invoice creation, payment flow)
- Document ATO calculation examples for unit tests
- Plan performance testing for large datasets

**Output:** `docs/qa/test-strategy.md`

**Template:** Use `.bmad-core/templates/qa-gate-tmpl.yaml`

---

### Execution Phase (Weeks 3-14)

#### 6. SM (Scrum Master)
**Goal:** Sprint planning for Phase 1 (MVP)

**Tasks:**
- Break Phase 1 into 2-week sprint stories
- Define story acceptance criteria
- Set sprint goals
- Plan story dependencies

**Phase 1 Sprint Breakdown:**

**Sprint 1 (Week 3-4): Foundation**
- [ ] Next.js project setup + TypeScript configuration
- [ ] Supabase client + type generation script
- [ ] shadcn/ui installation (button, card, table, dialog components)
- [ ] Auth flow (Supabase Auth, login/logout)
- [ ] Dashboard layout (sidebar, header, responsive)
- [ ] Entity selector context (Personal/MOKAI/MOK HOUSE/All)

**Sprint 2 (Week 5-6): Transaction Viewing**
- [ ] Transaction list page (Server Component initial load)
- [ ] React Query setup + 10-minute polling
- [ ] Virtual scrolling for transaction list (@tanstack/react-virtual)
- [ ] Date range filter
- [ ] Category filter
- [ ] Amount filter
- [ ] Transaction detail modal

**Sprint 3 (Week 7-8): Charts & Search**
- [ ] Spending by category chart (Recharts)
- [ ] Monthly spending trend chart
- [ ] Project-based filtering
- [ ] Search functionality (description, amount)
- [ ] Responsive design refinement
- [ ] Unit tests for data transformations
- [ ] E2E test for transaction flow

**Output:** Sprint backlog in Task Master or Linear

**Template:** Use `.bmad-core/templates/story-tmpl.yaml`

---

#### 7. Dev (Developer)
**Goal:** Implement features following architectural patterns

**Coding Standards:**
- **TypeScript:** Strict mode enabled, no `any` types
- **Components:** Functional components with TypeScript
- **Styling:** Tailwind CSS classes, no inline styles
- **Testing:** Test-driven for financial calculations
- **Naming:** Feature-based folders, descriptive names
- **Commits:** Conventional commits (feat:, fix:, test:)

**Key Implementation Patterns:**

**Data Fetching:**
```typescript
// Server Component for initial load
export default async function Page() {
  const data = await fetchInitialData();
  return <ClientComponent initialData={data} />;
}

// Client Component with React Query
'use client';
export function ClientComponent({ initialData }) {
  const { data } = useQuery({
    queryKey: ['transactions'],
    initialData,
    refetchInterval: 10 * 60 * 1000,
  });
}
```

**Type Safety:**
```typescript
// Generate types: npm run types:generate
import type { Database } from '@/types/database';

// Use in queries
const { data } = await supabase
  .from('personal_transactions')
  .select('*');
// data is fully typed!
```

**Financial Calculations:**
```typescript
// Always test financial logic!
// tests/unit/calculations/bas.test.ts
import { calculateBAS } from '@/lib/calculations/bas';

it('matches ATO example 1', () => {
  const result = calculateBAS(atoExampleData);
  expect(result.totalGST).toBe(expectedGST);
});
```

---

#### 8. QA (Quality Assurance - Continuous)
**Goal:** Validate each sprint delivery

**Per Sprint:**
- [ ] Run unit tests (npm run test)
- [ ] Run integration tests (npm run test:integration)
- [ ] Run E2E tests (npm run test:e2e)
- [ ] Manual exploratory testing
- [ ] Financial accuracy validation
- [ ] Performance testing (transaction list with 1000+ rows)
- [ ] Cross-browser testing
- [ ] Mobile responsive testing

**Quality Gates:**
- All tests passing
- No TypeScript errors
- Financial calculations validated
- Performance benchmarks met (<2s page load)
- Accessibility audit passed

---

## Quick Start

### 1. Install BMad Method (if not done)
```bash
cd /Users/harrysayers/Developer/claudelife
# BMad already installed in .bmad-core/
```

### 2. Review BMAD Scan Analysis
Read this document thoroughly to understand:
- Architectural decisions (Next.js, React Query, etc.)
- Tech stack rationale
- Project structure
- Implementation roadmap

### 3. Run PM Agent
```bash
# Create comprehensive PRD
/bmad:pm Create PRD from @00-inbox/bmad-scan-prompt.md and @00-inbox/financial-dashboard-requirements.md
```

### 4. Run Architect Agent
```bash
# Design system architecture
/bmad:architect Design architecture based on docs/prd.md
```

### 5. (Optional) Run UX Expert
```bash
# Create UI specifications
/bmad:ux-expert Design dashboard UI from PRD and architecture
```

### 6. Run PO Agent
```bash
# Validate and shard documents
/bmad:po Validate and shard PRD into phase-specific docs
```

### 7. Run QA Agent
```bash
# Create test strategy
/bmad:qa Create test strategy for financial dashboard
```

### 8. Begin Implementation (Phase 1)
```bash
# Setup project
mkdir financial-dashboard
cd financial-dashboard
npx create-next-app@latest . --typescript --tailwind --app --src-dir=false

# Follow Sprint 1 tasks from SM agent
```

---

## Key Configuration

### Environment Variables (.env.local)
```bash
NEXT_PUBLIC_SUPABASE_URL=https://gshsshaodoyttdxippwx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon_key>
SUPABASE_SERVICE_ROLE_KEY=<service_role_key>
```

### Supabase Type Generation
```json
{
  "scripts": {
    "types:generate": "npx supabase gen types typescript --project-id gshsshaodoyttdxippwx > types/database.ts",
    "predev": "npm run types:generate",
    "prebuild": "npm run types:generate"
  }
}
```

### Vercel Deployment
1. Connect GitHub repo to Vercel
2. Add environment variables in Vercel dashboard
3. Enable preview deployments for PRs
4. Set production branch to `main`

---

## Templates to Use

Planning:
- [x] `project-brief-tmpl.yaml` (if needed)
- [ ] `prd-tmpl.yaml` (PM agent)
- [ ] `architecture-tmpl.yaml` (Architect agent)
- [ ] `front-end-spec-tmpl.yaml` (UX Expert agent)

Execution:
- [ ] `story-tmpl.yaml` (SM agent for sprint planning)
- [ ] `qa-gate-tmpl.yaml` (QA agent for quality checkpoints)

---

## Critical Success Factors

1. **Type Safety:** End-to-end TypeScript from Supabase → Components
2. **Financial Accuracy:** 100% test coverage for calculations (BAS, P&L, Balance Sheet)
3. **Performance:** Virtual scrolling, caching, lazy loading for large datasets
4. **Scalability:** Architecture supports 6-phase roadmap without refactoring
5. **Australian Tax Compliance:** BAS calculations match ATO requirements
6. **Multi-Entity Support:** Properly segregate Personal/MOKAI/MOK HOUSE data

---

## Risk Mitigation

**High-Risk Areas:**
- **Financial calculation errors** → Mitigate with 100% test coverage + ATO examples
- **Supabase RLS misconfiguration** → Mitigate with thorough testing of multi-entity data access
- **Performance degradation** → Mitigate with virtual scrolling, pagination, database indexes
- **Vercel free tier limits** → Monitor usage, plan upgrade path if needed

**Testing Strategy:**
- Financial calculations: Unit tests against ATO examples
- Data security: Integration tests for RLS policies
- User flows: E2E tests with Playwright
- Performance: Load testing with 1000+ transactions

---

## Timeline (Solo Developer + AI)

- **Weeks 1-2:** Planning (PM → Architect → UX → PO → QA)
- **Weeks 3-8:** Phase 1 MVP (3 sprints)
- **Weeks 9-10:** Phase 2 Invoicing
- **Weeks 11-12:** Phase 3 Budgeting
- **Weeks 13-15:** Phase 4 Accounting & Reports
- **Weeks 16-17:** Phase 5 ML Insights
- **Weeks 18-19:** Phase 6 Polish

**Total:** 12-14 weeks to full feature set

---

## Next Steps

1. **Immediate:**
   - [ ] Run `/bmad:pm` to create comprehensive PRD
   - [ ] Run `/bmad:architect` to design system architecture
   - [ ] Review and approve PRD + Architecture

2. **This Week:**
   - [ ] Run `/bmad:ux-expert` for dashboard UI design
   - [ ] Run `/bmad:po` to validate and shard documents
   - [ ] Run `/bmad:qa` to create test strategy

3. **Next Week:**
   - [ ] Initialize Next.js project
   - [ ] Setup Supabase client + type generation
   - [ ] Install shadcn/ui components
   - [ ] Implement auth flow
   - [ ] Begin Phase 1 Sprint 1

---

## Notes

- **Solo development:** Use AI agents (PM, Architect, QA) extensively to maintain velocity
- **Financial accuracy:** Consult with accountant for BAS validation
- **Existing data:** 23 Supabase tables already populated with ~300 rows
- **Growth:** Architecture designed for 10,000+ transactions
- **MCPs available:** shadcn (UI), Context7 (docs), Supabase (DB ops), Task Master (project mgmt)

**BMad Method:** Follow agent sequence above for structured, validated approach to building production-ready financial management system.
