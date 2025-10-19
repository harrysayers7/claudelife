# Frontend UI/UX Specification
## SAYERS Financial Dashboard

---
date: "2025-10-17"
version: "1.0"
status: "Draft"
author: "UX Expert Agent (BMad Method)"
---

## 1. Design System

### 1.1 Color Palette

**Brand Colors:**
```
Primary:     hsl(222.2, 47.4%, 11.2%)  // Slate 950 (dark mode compatible)
Secondary:   hsl(210, 40%, 96.1%)      // Slate 50
Accent:      hsl(217.2, 91.2%, 59.8%)  // Blue 500
```

**Semantic Colors:**
```
Success:     hsl(142.1, 76.2%, 36.3%)  // Green 600
Warning:     hsl(32.1, 94.6%, 43.7%)   // Amber 500
Error:       hsl(0, 72.2%, 50.6%)      // Red 600
Info:        hsl(199.4, 89.2%, 48.4%)  // Cyan 500
```

**Chart Colors (8-color palette):**
```
Chart-1:     hsl(12, 76%, 61%)         // Coral
Chart-2:     hsl(173, 58%, 39%)        // Teal
Chart-3:     hsl(197, 37%, 24%)        // Navy
Chart-4:     hsl(43, 74%, 66%)         // Gold
Chart-5:     hsl(27, 87%, 67%)         // Orange
Chart-6:     hsl(339, 82%, 67%)        // Pink
Chart-7:     hsl(142, 76%, 36%)        // Green
Chart-8:     hsl(221, 83%, 53%)        // Blue
```

**Financial Status Colors:**
```
Paid:        hsl(142.1, 76.2%, 36.3%)  // Green 600
Overdue:     hsl(0, 72.2%, 50.6%)      // Red 600
Pending:     hsl(32.1, 94.6%, 43.7%)   // Amber 500
Draft:       hsl(215.4, 16.3%, 46.9%)  // Slate 500
Income:      hsl(142.1, 70.6%, 45.3%)  // Green 500
Expense:     hsl(0, 84.2%, 60.2%)      // Red 500
```

### 1.2 Typography Scale

**Font Stack:** `Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`

**Scale:**
```
Display:     text-4xl (36px / 40px line-height) - Dashboard titles
Heading 1:   text-3xl (30px / 36px) - Page titles
Heading 2:   text-2xl (24px / 32px) - Section titles
Heading 3:   text-xl (20px / 28px) - Card titles
Body:        text-base (16px / 24px) - Default body text
Small:       text-sm (14px / 20px) - Descriptions, metadata
Tiny:        text-xs (12px / 16px) - Labels, captions
```

**Weights:**
- Regular: 400 (body text)
- Medium: 500 (emphasized text, buttons)
- Semibold: 600 (headings)
- Bold: 700 (KPIs, critical data)

### 1.3 Spacing System

**Scale:** `4px base unit`
```
xs:  4px   (space-1)   - Tight spacing
sm:  8px   (space-2)   - Badge/tag padding
md:  16px  (space-4)   - Card padding, element spacing
lg:  24px  (space-6)   - Section spacing
xl:  32px  (space-8)   - Page margins
2xl: 48px  (space-12)  - Major section breaks
```

### 1.4 shadcn/ui Component Mapping

| Purpose | shadcn Component | Customization |
|---------|-----------------|---------------|
| **Data Display** |
| Transaction list | `table` | Virtual scrolling via TanStack Table |
| Invoice cards | `card` | Status-based border colors |
| KPI metrics | `card` + custom KPICard | Trend arrows, sparklines |
| Category labels | `badge` | Color-coded by category, editable |
| Status indicators | `badge` | Semantic colors (paid/overdue) |
| Loading states | `skeleton` | Match card/table structure |
| **Forms** |
| Invoice creation | `form` + `input` + `select` | React Hook Form + Zod |
| Date selection | `calendar` + `popover` | Presets (This Month, Last Quarter) |
| Category dropdown | `combobox` | Searchable, ML suggestions |
| Currency input | `input` | Custom decimal handling |
| Notes/descriptions | `textarea` | Auto-resize |
| **Navigation** |
| Main navigation | `sidebar` (v4) | Collapsible, mobile drawer |
| Entity switcher | `dropdown-menu` | Logos + entity names |
| Page tabs | `tabs` | Transactions/Invoices views |
| Breadcrumbs | `breadcrumb` | Deep navigation paths |
| **Feedback** |
| Notifications | `sonner` | Success/error toasts |
| Alerts | `alert` | Overdue invoices, anomalies |
| Confirmations | `alert-dialog` | Delete invoice, mark paid |
| Modals | `dialog` | Quick edit transaction |
| Side panels | `sheet` | Filter sidebar (mobile) |
| Tooltips | `tooltip` | Chart data points, icons |
| **Charts** |
| All charts | Custom wrappers | Recharts + Card container |

---

## 2. Layout Architecture

### 2.1 Dashboard Shell

**ASCII Wireframe:**
```
┌─────────────────────────────────────────────────────────────────┐
│ Header (h-16)                                                    │
│  [Logo] [Entity ▼] [Search 🔍]      [Alerts 🔔] [User ⚙️] [🌙]  │
└─────────────────────────────────────────────────────────────────┘
┌──────────┬──────────────────────────────────────────────────────┐
│          │                                                       │
│ Sidebar  │              Main Content                            │
│ (w-64)   │              (flex-1, p-8)                           │
│          │                                                       │
│ [Home]   │  ┌────────────────────────────────────────────────┐ │
│ [Trans]  │  │  Page Content                                  │ │
│ [Invoic] │  │                                                │ │
│ [Report] │  │                                                │ │
│ [Insigh] │  │                                                │ │
│ [Budget] │  │                                                │ │
│ [Settin] │  │                                                │ │
│          │  │                                                │ │
│          │  └────────────────────────────────────────────────┘ │
│          │                                                       │
└──────────┴──────────────────────────────────────────────────────┘
```

**Component Structure:**
```tsx
<DashboardLayout>
  <Header>
    <EntitySelector />
    <SearchBar />
    <AlertBadge />
    <UserMenu />
    <ThemeToggle />
  </Header>
  <div className="flex">
    <Sidebar />
    <main className="flex-1 p-8">
      {children} {/* Page content */}
    </main>
  </div>
</DashboardLayout>
```

### 2.2 Responsive Breakpoints

| Breakpoint | Width | Layout Changes |
|------------|-------|----------------|
| **Mobile** | 320-767px | Sidebar → Drawer (hamburger), Single column, Stacked cards |
| **Tablet** | 768-1023px | Sidebar visible, 2-column grids, Horizontal scroll tables |
| **Desktop** | 1024px+ | Full layout, 4-column KPIs, All charts visible |

**Mobile Adaptations:**
- Header: Hamburger menu, compact entity selector
- Sidebar: Slide-out drawer (Sheet component)
- Tables: Horizontal scroll, sticky first column
- Charts: Single-column stack, simplified legends

---

## 3. Key Page Specifications

### 3.1 Dashboard Home (`/dashboard`)

**Wireframe:**
```
┌─────────────────────────────────────────────────────────────────┐
│ Dashboard                                      [Last 30 Days ▼] │
├─────────────────────────────────────────────────────────────────┤
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐    │
│ │ Income   │ │ Expenses │ │ Net      │ │ Cash Balance     │    │
│ │ $12,450  │ │ $8,320   │ │ $4,130   │ │ $34,567          │    │
│ │ ↑ 12%    │ │ ↓ 5%     │ │ ↑ 25%    │ │ ─────────        │    │
│ └──────────┘ └──────────┘ └──────────┘ └──────────────────┘    │
├─────────────────────────────────────────────────────────────────┤
│ ┌──────────────────────┐ ┌───────────────────────────────────┐ │
│ │ Spending by Category │ │ Recent Transactions               │ │
│ │ ┌────────────────┐   │ │ Oct 17  Office Supplies  -$45.00  │ │
│ │ │   Donut Chart  │   │ │ Oct 16  Client Payment   +$2,500  │ │
│ │ │                │   │ │ Oct 15  Software Sub     -$99.00  │ │
│ │ │                │   │ │ Oct 14  Coffee Shop      -$12.50  │ │
│ │ └────────────────┘   │ │ Oct 13  Uber Trip        -$28.00  │ │
│ │ [View All →]         │ │ Oct 13  Invoice Payment  +$1,200  │ │
│ └──────────────────────┘ │ [View All →]                      │ │
│                          └───────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│ ┌──────────────────────────────────────────────────────────────┐│
│ │ 🚨 Alerts                                                    ││
│ │ • 3 overdue invoices ($4,500 total) - Due 5+ days          ││
│ │ • 1 anomaly detected - Unusual transaction on Oct 15        ││
│ └──────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

**Components:**
- 4x `KPICard` (income, expenses, net, balance)
- 1x `SpendingChart` (donut chart in Card)
- 1x `RecentTransactions` (Table in Card)
- 1x `AlertBanner` (Alert component)

**Interactions:**
- KPI cards: Click to view filtered transactions
- Chart segments: Click to drill down to category
- Transaction rows: Click to view/edit detail
- Date range: Dropdown to change period

---

### 3.2 Transactions Page (`/transactions`)

**Wireframe:**
```
┌─────────────────────────────────────────────────────────────────┐
│ Transactions                                   [+ New Transaction]│
├─────────────────────────────────────────────────────────────────┤
│ [Search...] [Category ▼] [Date Range ▼] [Project ▼] [Export ⬇] │
├─────────────────────────────────────────────────────────────────┤
│ ┌───────────────────────────────────────────────────────────┐   │
│ │ Date ↓ │ Description         │ Category      │ Amount    │   │
│ ├────────┼─────────────────────┼───────────────┼───────────┤   │
│ │ Oct 17 │ Office Supplies     │ 📦 Supplies   │ -$45.00   │   │
│ │ Oct 16 │ Client Payment      │ 💰 Income     │ +$2,500.00│   │
│ │ Oct 15 │ Software Sub        │ 💻 Software   │ -$99.00   │   │
│ │ Oct 14 │ Coffee Shop         │ 🍽️ Meals      │ -$12.50   │   │
│ │ Oct 13 │ Uber Trip           │ 🚗 Transport  │ -$28.00   │   │
│ │ ...    │ ...                 │ ...           │ ...       │   │
│ └───────────────────────────────────────────────────────────┘   │
│ Showing 1-50 of 256                        [← 1 2 3 4 5 →]      │
└─────────────────────────────────────────────────────────────────┘
```

**Components:**
- `SearchBar` (debounced 300ms)
- `TransactionFilters` (Category, Date, Project, Entity)
- `TransactionTable` (TanStack Table + Virtual Scrolling)
- `Pagination` (50 per page)
- `Button` (Export CSV)

**Interactions:**
- Row click: Open quick edit Dialog
- Category badge: Click to change category (Combobox)
- Sorting: Click column headers
- Bulk select: Checkbox column, bulk actions menu

---

### 3.3 Invoices Page (`/invoices`)

**Wireframe:**
```
┌─────────────────────────────────────────────────────────────────┐
│ Invoices                                          [+ New Invoice] │
├─────────────────────────────────────────────────────────────────┤
│ [🔍 Search] [Status ▼] [Contact ▼] [Date Range ▼] [Export ⬇]   │
├─────────────────────────────────────────────────────────────────┤
│ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ │
│ │ INV-001          │ │ INV-002          │ │ INV-003          │ │
│ │ Acme Corp        │ │ Tech Ltd         │ │ Consulting Co    │ │
│ │ $2,500.00        │ │ $1,200.00        │ │ $3,800.00        │ │
│ │ ✅ Paid          │ │ 🚨 Overdue (5d)  │ │ ⏳ Pending       │ │
│ │ Due: Oct 15      │ │ Due: Oct 10      │ │ Due: Oct 25      │ │
│ │ [View] [PDF]     │ │ [View] [PDF]     │ │ [View] [PDF]     │ │
│ └──────────────────┘ └──────────────────┘ └──────────────────┘ │
│ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ │
│ │ INV-004          │ │ INV-005          │ │ ...              │ │
│ │ ...              │ │ ...              │ │ ...              │ │
│ └──────────────────┘ └──────────────────┘ └──────────────────┘ │
│ Showing 1-6 of 30                          [← 1 2 3 4 5 →]      │
└─────────────────────────────────────────────────────────────────┘
```

**Components:**
- `InvoiceCard` (Card with status-based border)
- `InvoiceFilters` (Status, Contact, Date)
- Grid layout (responsive: 1/2/3 columns)
- `Pagination`

**Status Colors:**
- Paid: Green border-l-4
- Overdue: Red border-l-4, pulsing animation
- Pending: Amber border-l-4
- Draft: Slate border-l-4

---

### 3.4 Reports Page (`/reports`)

**Wireframe:**
```
┌─────────────────────────────────────────────────────────────────┐
│ Reports                                                          │
├─────────────────────────────────────────────────────────────────┤
│ ┌────────────────────────────────────────────────────────────┐  │
│ │ Generate Report                                            │  │
│ │ [Report Type ▼] [Date Range ▼] [Entity ▼] [Generate →]   │  │
│ └────────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ │
│ │ 📊 Profit & Loss │ │ 💼 Balance Sheet │ │ 🧾 BAS Statement │ │
│ │ Last Quarter     │ │ Current Position │ │ Q3 2025          │ │
│ │ [View] [PDF]     │ │ [View] [PDF]     │ │ [View] [PDF]     │ │
│ └──────────────────┘ └──────────────────┘ └──────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**Components:**
- `ReportGenerator` (Form with Select + DateRangePicker)
- `ReportCard` (Card with report metadata)
- Report type options: P&L, Balance Sheet, BAS

---

## 4. Component Specifications

### 4.1 EntitySelector

**Purpose:** Switch between Personal/MOKAI/MOK HOUSE

**Appearance:**
```
┌────────────────────────┐
│ 🏢 MOKAI PTY LTD    ▼ │
└────────────────────────┘

(Dropdown)
┌────────────────────────┐
│ ✓ 🏢 MOKAI PTY LTD     │
│   🎵 MOK HOUSE PTY LTD │
│   👤 Harrison Sayers   │
└────────────────────────┘
```

**Props:**
```typescript
interface EntitySelectorProps {
  value: string;           // Current entity ID
  onChange: (id: string) => void;
  entities: Entity[];      // List of entities
}
```

**State:** Zustand global store (`useEntityFilter`)

---

### 4.2 TransactionTable

**Features:**
- Virtual scrolling (50,000+ rows)
- Inline category editing
- Sortable columns
- Sticky header

**Columns:**
```
Date (sortable)
Description (searchable)
Category (editable badge)
Amount (right-aligned, color-coded)
Actions (... menu)
```

**Implementation:** TanStack Table v8 + @tanstack/react-virtual

---

### 4.3 KPICard

**Anatomy:**
```
┌────────────────────────┐
│ Label (text-sm muted)  │
│ $12,450 (text-3xl bold)│
│ ↑ 12% vs last period   │
│ ▁▂▃▅▆▇ (sparkline)     │
└────────────────────────┘
```

**Props:**
```typescript
interface KPICardProps {
  label: string;
  value: number;            // In cents
  trend: number;            // Percentage change
  trendData: number[];      // For sparkline
  icon?: ReactNode;
  onClick?: () => void;
}
```

---

### 4.4 Chart Components

**ChartCard Wrapper:**
```tsx
<ChartCard title="Spending by Category" description="Last 30 days">
  <PieChart data={categoryData} />
</ChartCard>
```

**Chart Types:**
- `PieChart` / `DonutChart`: Category breakdown
- `LineChart`: Trends over time
- `BarChart`: Month-over-month comparison
- `WaterfallChart`: Cash flow visualization

**Data Format (Recharts):**
```typescript
interface ChartData {
  name: string;      // Label
  value: number;     // Data point
  fill?: string;     // Color
}
```

---

### 4.5 InvoiceForm

**Fields:**
```
Contact (Combobox, searchable)
Issue Date (DatePicker)
Due Date (DatePicker)
Line Items (Dynamic array)
  - Description (Input)
  - Amount (CurrencyInput)
  - [Remove]
[+ Add Line Item]
Subtotal (calculated)
GST (10%, calculated)
Total (calculated)
Notes (Textarea, optional)
[Save as Draft] [Send Invoice]
```

**Validation:** Zod schema
```typescript
const invoiceSchema = z.object({
  contact_id: z.string().uuid(),
  issue_date: z.date(),
  due_date: z.date().min(issueDate),
  line_items: z.array(z.object({
    description: z.string().min(1),
    amount: z.number().positive(),
  })).min(1),
  notes: z.string().optional(),
});
```

---

## 5. Interaction Patterns

### 5.1 Filtering & Search

**Transaction Filter Flow:**
1. User types in SearchBar (debounced 300ms)
2. URL updates: `/transactions?search=coffee`
3. Server Component re-renders with filtered data
4. Table updates instantly (React Suspense boundary)

**Filter Persistence:** URL params (shareable links)

---

### 5.2 Form Validation

**Inline Validation (React Hook Form + Zod):**
```
┌─────────────────────────────┐
│ Contact *                   │
│ [Select contact...      ▼] │ <- Required
│                             │
│ Amount *                    │
│ [$____________]             │ <- Must be positive
│ ❌ Amount must be positive  │ <- Error message
│                             │
│ [Cancel] [Save]             │ <- Save disabled until valid
└─────────────────────────────┘
```

**Error States:**
- Red border on invalid input
- Error text below field (text-sm text-red-600)
- Submit button disabled until valid

---

### 5.3 Loading States

**Skeleton Loading:**
```tsx
// Transaction list loading
<Table>
  {Array(10).fill(0).map((_, i) => (
    <TableRow key={i}>
      <TableCell><Skeleton className="h-4 w-20" /></TableCell>
      <TableCell><Skeleton className="h-4 w-40" /></TableCell>
      <TableCell><Skeleton className="h-4 w-24" /></TableCell>
      <TableCell><Skeleton className="h-4 w-16" /></TableCell>
    </TableRow>
  ))}
</Table>
```

**Suspense Boundaries:** Wrap async Server Components
```tsx
<Suspense fallback={<TransactionSkeleton />}>
  <TransactionList />
</Suspense>
```

---

### 5.4 Empty States

**No Transactions:**
```
┌─────────────────────────────┐
│           📊                │
│    No transactions yet      │
│                             │
│  [+ Create Transaction]     │
└─────────────────────────────┘
```

**No Search Results:**
```
┌─────────────────────────────┐
│           🔍                │
│   No results for "coffee"   │
│                             │
│   [Clear Search]            │
└─────────────────────────────┘
```

---

## 6. Accessibility & Mobile

### 6.1 WCAG AA Requirements

**Color Contrast:**
- Text: 4.5:1 minimum
- Large text (18px+): 3:1 minimum
- Interactive elements: 3:1 minimum

**Keyboard Navigation:**
- All interactive elements: Tab/Shift+Tab
- Dropdowns: Arrow keys
- Dialogs: Esc to close
- Search: Cmd+K to focus

**Screen Reader:**
- ARIA labels on all icons
- `role="region"` on major sections
- `aria-live="polite"` on status updates
- Form error announcements

**Focus Indicators:**
- Visible focus ring (ring-2 ring-offset-2 ring-primary)
- Skip to main content link

---

### 6.2 Touch Optimization (Mobile)

**Touch Targets:** Minimum 44x44px (iOS/Android guidelines)

**Gestures:**
- Swipe: Navigate between tabs
- Pull-to-refresh: Update transaction list
- Long-press: Open context menu

**Mobile Navigation:**
```
(Hamburger)
┌────────────────┐
│ ☰              │
└────────────────┘

(Drawer opens)
┌────────────────┐
│ ← Dashboard    │
│   Transactions │
│   Invoices     │
│   Reports      │
│   Settings     │
│                │
│ [Entity ▼]     │
└────────────────┘
```

---

## 7. shadcn/ui Component Map

| Feature | Component | Usage |
|---------|-----------|-------|
| **Dashboard KPIs** | `card` | Container for metrics |
| **Transaction List** | `table` | Data display with TanStack Table |
| **Virtual Scrolling** | `scroll-area` | Large lists (10k+ items) |
| **Invoice Cards** | `card` | Invoice summary display |
| **Status Badges** | `badge` | Paid/Overdue/Draft indicators |
| **Category Labels** | `badge` (editable) | Transaction categories |
| **Loading States** | `skeleton` | Content placeholders |
| **Charts** | Custom + `card` | Recharts wrapped in Card |
| **Forms** | `form` + `input` + `select` | All form inputs |
| **Date Picker** | `calendar` + `popover` | Date selection |
| **Category Selector** | `combobox` | Searchable dropdown |
| **Currency Input** | `input` (custom) | Decimal number handling |
| **Sidebar Nav** | `sidebar` (v4) | Main navigation |
| **Entity Switcher** | `dropdown-menu` | Switch entities |
| **Page Tabs** | `tabs` | Sub-navigation |
| **Breadcrumbs** | `breadcrumb` | Navigation path |
| **Toasts** | `sonner` | Success/error messages |
| **Alerts** | `alert` | System alerts |
| **Confirmations** | `alert-dialog` | Destructive actions |
| **Quick Edit** | `dialog` | Transaction edit modal |
| **Filter Panel** | `sheet` | Mobile filter sidebar |
| **Tooltips** | `tooltip` | Icon explanations |

---

## 8. Implementation Notes

**Critical:**
- Use Server Components by default, Client Components only when needed
- All financial calculations server-side (never trust client)
- Virtual scrolling for transaction tables (TanStack Virtual)
- Decimal.js for currency math (avoid floating-point errors)
- Mobile-first responsive design (320px minimum)

**Performance:**
- Code splitting per phase (6 route groups)
- Lazy load charts (`React.lazy()`)
- Optimize images with Next.js `<Image>`
- Cache API responses (React Query)

**Security:**
- Server-side validation (Zod schemas)
- RLS policies enforce entity access
- CSRF protection (Next.js built-in)
- Sanitize user inputs (React auto-escapes)

---

## Appendix: Design Tokens

**Border Radius:**
```
sm: 0.375rem (6px)
md: 0.5rem (8px)
lg: 0.75rem (12px)
```

**Shadows:**
```
sm: 0 1px 2px 0 rgb(0 0 0 / 0.05)
md: 0 4px 6px -1px rgb(0 0 0 / 0.1)
lg: 0 10px 15px -3px rgb(0 0 0 / 0.1)
```

**Animations:**
```
Fade in: opacity 0 → 1 (200ms)
Slide in: translateY(4px) → 0 (200ms)
Pulse: scale 1 → 1.05 → 1 (1s loop)
```

---

**Total Pages: 11**

This spec provides everything needed to implement the UI without guesswork. All components, layouts, and interactions are defined with shadcn/ui mappings and implementation details.
