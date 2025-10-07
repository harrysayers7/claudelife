# Epic 1: Foundation & Core Infrastructure

<!-- Powered by BMAD™ Core -->

## Epic Overview

**Epic Goal**: Establish the foundational project infrastructure including Next.js application setup, Supabase database integration, authentication system, base application layout with responsive navigation, and initial deployment pipeline to Vercel. This epic delivers a functional authenticated application with entity switching capability and a basic dashboard landing page, setting the stage for all subsequent feature development while ensuring security, performance, and deployment foundations are solid.

**Dependencies**: None (foundational epic)

**Success Criteria**:
- Next.js 14+ application deployed to Vercel with production URL
- Authentication working via Supabase Auth with session management
- Multi-entity selector operational with data isolation verified
- Responsive navigation accessible on desktop, tablet, and mobile
- Basic dashboard landing page displaying placeholder UI

---

## Story 1.1: Project Setup & Next.js Application Initialization

As a developer,
I want to initialize a Next.js 14+ application with TypeScript, Tailwind CSS, and shadcn/ui,
so that I have a modern, type-safe foundation for building the finance dashboard.

### Acceptance Criteria

1. Next.js 14+ project created using `create-next-app` with App Router, TypeScript, and Tailwind CSS enabled
2. Project structure follows monorepo conventions with `/app`, `/components`, `/lib`, `/types`, `/hooks`, `/public` directories
3. shadcn/ui initialized with `npx shadcn-ui init` and base components installed: Button, Card, Input, Label, Select, Table
4. Tailwind CSS configured with custom theme colors: primary (blue), success (green), danger (red), warning (amber), neutral grays
5. TypeScript strict mode enabled in `tsconfig.json` with path aliases configured (`@/components`, `@/lib`, etc.)
6. ESLint and Prettier configured with Next.js recommended rules and consistent code formatting
7. Git repository initialized with `.gitignore` excluding `node_modules`, `.next`, `.env.local`, and build artifacts
8. `package.json` includes all required dependencies: Next.js, React, TypeScript, Tailwind, shadcn/ui, date-fns, zod, react-hook-form
9. Development server runs successfully on `localhost:3000` with hot module replacement working
10. README.md created with project description, setup instructions, and development commands

### Technical Notes from Architecture

**Technology Stack**:
- Next.js 14.2+
- TypeScript 5.3+ (strict mode)
- Tailwind CSS 3.4+
- shadcn/ui (Radix UI + Tailwind)
- React Hook Form 7.49+
- Zod 3.22+ for validation
- date-fns 3.0+ for date utilities

**Project Structure**:
```
/
├── app/                # Next.js App Router
├── components/         # React components
├── lib/               # Utilities, Supabase client
├── types/             # TypeScript types (shared)
├── hooks/             # Custom React hooks
├── public/            # Static assets
```

**Configuration Requirements**:
- `tsconfig.json`: Enable strict mode, configure path aliases
- `tailwind.config.ts`: Custom theme colors (primary, success, danger, warning)
- `.eslintrc.json`: Next.js recommended rules
- `.prettierrc`: Consistent formatting rules

---

## Story 1.2: Supabase Integration & Type Generation

As a developer,
I want to integrate Supabase client with TypeScript type generation from the existing database schema,
so that I have type-safe database queries and autocomplete for all tables.

### Acceptance Criteria

1. `@supabase/ssr` package installed and configured for Next.js App Router compatibility
2. Supabase client instances created: `createClient()` for server components, `createBrowserClient()` for client components
3. Environment variables configured in `.env.local`: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`
4. TypeScript types generated from Supabase schema using CLI: `supabase gen types typescript` for all 24+ tables
5. Generated types saved to `/types/supabase.ts` and imported in Supabase client configuration
6. Helper functions created in `/lib/supabase.ts`: `getServerClient()`, `getBrowserClient()` with proper typing
7. Test query implemented (e.g., fetch entities) to verify Supabase connection works from server component
8. Error handling implemented: graceful failure messages for connection issues, missing environment variables
9. RLS policies verified: confirm entity_id filtering works correctly by querying entities table
10. Documentation added to README: Supabase setup instructions, type regeneration steps, environment variable requirements

### Technical Notes from Architecture

**Supabase Configuration**:
- Project ID: `gshsshaodoyttdxippwx` (SAYERS DATA)
- Region: AWS Sydney
- Existing Infrastructure: 13 tables, 230+ personal transactions, 29 invoices, ML models active

**Client Patterns**:
```typescript
// Server Components
import { createClient } from '@/lib/supabase-server'
const supabase = createClient()

// Client Components
import { createBrowserClient } from '@/lib/supabase-client'
const supabase = createBrowserClient()
```

**Type Generation**:
```bash
npx supabase gen types typescript --project-id=gshsshaodoyttdxippwx > types/supabase.ts
```

**Key Tables to Verify**:
- `entities` (MOKAI, MOK HOUSE, Harrison Sayers)
- `personal_transactions` (UpBank sync data)
- `invoices` (receivables/payables)
- `contacts` (customers/suppliers)
- `accounts` (chart of accounts)

---

## Story 1.3: Authentication System with Supabase Auth

As a user,
I want to log in with email and password,
so that I can securely access my financial data.

### Acceptance Criteria

1. Supabase Auth configured in Supabase project settings: email/password provider enabled, email confirmation disabled for development
2. Login page created at `/app/login/page.tsx` with email and password input fields using shadcn/ui Form components
3. Login form implements React Hook Form + Zod validation: email format, password minimum 8 characters, required field validation
4. Authentication logic implemented: `supabase.auth.signInWithPassword()` with error handling for invalid credentials, network errors
5. Successful login redirects user to `/dashboard` route with session cookie set via Supabase SSR middleware
6. Logout functionality implemented: sign out button in navigation triggers `supabase.auth.signOut()` and redirects to `/login`
7. Session management middleware created: `/middleware.ts` checks authentication status, redirects unauthenticated users to `/login`
8. Protected routes configured: all `/app` routes except `/login` require authentication via middleware check
9. User session persists across browser refreshes using Supabase session cookies
10. Error messages display clearly: "Invalid credentials", "Network error", field-specific validation errors with red text

### Technical Notes from Architecture

**Authentication Pattern**:
```typescript
// middleware.ts
import { createServerClient } from '@supabase/ssr'

export async function middleware(request: NextRequest) {
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    { cookies: { get: (name) => request.cookies.get(name)?.value } }
  )

  const { data: { session } } = await supabase.auth.getSession()

  if (!session && !request.nextUrl.pathname.startsWith('/login')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}
```

**Security Requirements**:
- HTTPS only in production
- Session cookies with httpOnly flag
- CSRF protection via Supabase SSR
- No credentials stored in localStorage

---

## Story 1.4: Base Application Layout & Responsive Navigation

As a user,
I want to see a consistent header, sidebar navigation, and content area across all pages,
so that I can easily navigate between different sections of the dashboard.

### Acceptance Criteria

1. Root layout created at `/app/layout.tsx` with responsive structure: header, sidebar (desktop), mobile menu, main content area
2. Header component includes: application logo/name ("SAYERS Finance"), entity selector dropdown (placeholder), user menu with logout
3. Sidebar navigation (desktop 1280px+) displays menu items: Dashboard, Transactions, Invoices, Reports, Contacts, Accounts, Settings
4. Mobile navigation (< 1280px) uses hamburger menu icon triggering slide-out drawer with same menu items
5. Active route highlighting implemented: current page menu item visually distinct with background color/border
6. Navigation items use Next.js `<Link>` components for client-side routing with prefetching enabled
7. Layout is responsive: header stacks on mobile, sidebar hidden behind hamburger, content area takes full width
8. Accessibility features implemented: skip to main content link, keyboard navigation (tab/arrows), focus indicators on interactive elements
9. Footer component (optional) includes: copyright text, link to privacy policy (placeholder), app version number
10. All layout components use shadcn/ui primitives (Card, Button, Sheet for mobile menu) with consistent Tailwind spacing/colors

### Technical Notes from Architecture

**Responsive Breakpoints**:
- Desktop: 1920px+ (full feature set, multi-column layouts)
- Laptop: 1280px-1919px (condensed layouts, collapsible sidebars)
- Tablet: 768px-1279px (single column, stacked cards)
- Mobile: 320px-767px (mobile-first navigation, essential features)

**Component Structure**:
```
components/
├── layout/
│   ├── Header.tsx         # App header with entity selector
│   ├── Sidebar.tsx        # Desktop navigation
│   ├── MobileMenu.tsx     # Mobile drawer navigation
│   └── Footer.tsx         # Optional footer
```

**Navigation Menu Items**:
- Dashboard (`/dashboard`) - Overview and KPIs
- Transactions (`/transactions`) - Transaction list and management
- Invoices (`/invoices`) - Invoice management
- Reports (`/reports`) - BAS, P&L, exports
- Contacts (`/settings/contacts`) - Customer/supplier management
- Accounts (`/settings/accounts`) - Chart of accounts
- Settings (`/settings`) - User preferences and admin

---

## Story 1.5: Multi-Entity Selector & Context Management

As a user,
I want to select which business entity I'm viewing (MOKAI, MOK HOUSE, personal),
so that I see only the relevant financial data for that entity.

### Acceptance Criteria

1. Entity selector dropdown component created in header using shadcn/ui Select component
2. Entities fetched from Supabase `entities` table on component mount: entity_id, name, type displayed in dropdown
3. Active entity state managed using React Context: `EntityContext` provider wraps application in root layout
4. Selected entity persists in browser localStorage: key `selectedEntityId`, restored on page refresh
5. Default entity set on first login: if no localStorage value, default to first entity in list (MOKAI PTY LTD)
6. Entity change triggers data refresh: context value update causes dependent components to re-fetch with new entity_id filter
7. Visual indicator shows active entity: selected entity name displayed in header with entity type badge (e.g., "MOKAI PTY LTD (Company)")
8. Entity switching logs audit event: timestamp, user_id, old_entity_id, new_entity_id written to audit log table (if exists, otherwise console log)
9. Loading state handled during entity fetch: skeleton loader shown in dropdown until entities loaded from Supabase
10. Error handling: if entities fetch fails, show error toast, disable entity selector, log error to console

### Technical Notes from Architecture

**Entity Context Pattern**:
```typescript
// contexts/EntityContext.tsx
interface EntityContextType {
  entityId: string | null
  entity: Entity | null
  entities: Entity[]
  setEntityId: (id: string) => void
  isLoading: boolean
}

export const EntityContext = createContext<EntityContextType>()
```

**Multi-Entity Data Isolation (RLS)**:
- All Supabase queries MUST include entity_id filter
- Row Level Security policies enforce entity-based access control
- Context provides automatic filtering for all child components

**Existing Entities**:
1. **MOKAI PTY LTD** - Indigenous tech consultancy (Company)
2. **MOK HOUSE PTY LTD** - Creative house (Company)
3. **Harrison Robert Sayers** - Personal finances (Sole Trader)

---

## Story 1.6: Basic Dashboard Landing Page

As a user,
I want to see a dashboard landing page when I log in,
so that I know the application is working and I have a starting point for navigation.

### Acceptance Criteria

1. Dashboard page created at `/app/dashboard/page.tsx` as default route after login
2. Page header displays: "Dashboard" title, active entity name subtitle, date range selector (placeholder, default "Last 30 Days")
3. KPI placeholder cards rendered in responsive grid: 4 cards on desktop (1920px+), 2 cards on tablet (768px+), 1 card on mobile (<768px)
4. Each KPI card displays: metric label (e.g., "Total Revenue"), placeholder value ("$0.00"), icon, trend indicator (placeholder +0%)
5. Chart placeholder section below KPIs: empty state message "Charts coming soon" with chart icon, proper spacing/borders
6. Recent activity widget placeholder: "Recent Transactions" heading, empty state "No recent transactions" message, bordered container
7. All components use shadcn/ui Card component with consistent spacing, shadows, and responsive behavior
8. Page implements proper loading state: skeleton loaders for cards/widgets shown while data would be fetching (simulated 1s delay)
9. Responsive behavior verified: layout stacks vertically on mobile, side-by-side on tablet/desktop, no horizontal scroll
10. Navigation from sidebar "Dashboard" menu item highlights correctly and loads this page

### Technical Notes from Architecture

**Dashboard Layout Structure**:
```
┌─────────────────────────────────────────────┐
│ Dashboard Header + Entity Selector          │
├─────────────────────────────────────────────┤
│ [KPI 1] [KPI 2] [KPI 3] [KPI 4]           │  Desktop
├─────────────────────────────────────────────┤
│ Trend Chart                   | Recent     │
│                               | Activity   │
├─────────────────────────────────────────────┤
│ Category Chart  | Anomaly Alerts           │
└─────────────────────────────────────────────┘
```

**Placeholder KPIs**:
- Total Revenue: $0.00 (+0%)
- Total Expenses: $0.00 (+0%)
- Net Profit/Loss: $0.00
- Cash Flow: $0.00

---

## Story 1.7: Vercel Deployment & Environment Configuration

As a developer,
I want to deploy the application to Vercel with proper environment variables,
so that I have a live staging environment accessible via URL.

### Acceptance Criteria

1. Vercel project created and connected to GitHub repository with automatic deployments enabled on `main` branch
2. Environment variables configured in Vercel dashboard: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` set to production Supabase project
3. Build settings configured: Next.js framework preset selected, build command `npm run build`, output directory `.next`
4. Production deployment succeeds: build completes without errors, application accessible at Vercel-provided URL (e.g., `sayers-finance.vercel.app`)
5. Deployment preview environments created: pull requests trigger preview deployments with unique URLs
6. Custom domain configured (optional): if available, custom domain pointed to Vercel deployment with SSL enabled
7. Environment variable security verified: no secrets exposed in client-side code, `NEXT_PUBLIC_` prefix only on public variables
8. Deployment monitoring enabled: Vercel Analytics and Speed Insights integrated for performance tracking (optional)
9. Rollback capability verified: previous deployment accessible via Vercel dashboard, one-click rollback tested
10. Deployment documentation added to README: deployment steps, environment variable setup, domain configuration instructions

### Technical Notes from Architecture

**Deployment Configuration**:
- **Platform**: Vercel (native Next.js optimization)
- **Region**: Sydney, Australia (optimal latency)
- **Build Settings**:
  - Framework: Next.js
  - Build Command: `npm run build`
  - Output Directory: `.next`
  - Install Command: `npm install`

**Environment Variables (Production)**:
```
NEXT_PUBLIC_SUPABASE_URL=https://gshsshaodoyttdxippwx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=[production_anon_key]
```

**Deployment Pipeline**:
```
Git Push → GitHub → Vercel Build → Deploy → Production URL
                  ↓
              PR Preview Deployments
```

---

## Epic Dependencies

This epic has **no dependencies** on other epics as it establishes the foundation.

## Epic Deliverables

1. ✅ Next.js application with TypeScript, Tailwind, shadcn/ui
2. ✅ Supabase integration with type-safe queries
3. ✅ Authentication system with session management
4. ✅ Responsive navigation (desktop sidebar, mobile drawer)
5. ✅ Multi-entity context with localStorage persistence
6. ✅ Basic dashboard placeholder page
7. ✅ Production deployment on Vercel

## Testing Requirements

**Unit Tests** (Vitest):
- Entity context: entity switching logic, localStorage persistence
- Utility functions: date formatting, currency formatting

**Integration Tests** (React Testing Library):
- Login flow: form validation, successful auth, error handling
- Navigation: menu highlighting, route navigation
- Entity selector: dropdown interaction, context updates

**E2E Tests** (Playwright):
- Full authentication flow: login → dashboard → logout
- Entity switching: select entity → verify data refresh
- Responsive layout: verify mobile, tablet, desktop layouts

## Definition of Done

- [ ] All 7 stories completed with acceptance criteria met
- [ ] Application deployed to Vercel with production URL
- [ ] Authentication working with proper session management
- [ ] Multi-entity selector operational with RLS verified
- [ ] Responsive navigation tested on mobile, tablet, desktop
- [ ] README documentation complete with setup instructions
- [ ] Unit tests passing for critical utilities
- [ ] E2E test for login flow passing

---

**Epic Status**: Ready for Implementation
**Estimated Effort**: 5-7 days
**Priority**: P0 (Foundational)
