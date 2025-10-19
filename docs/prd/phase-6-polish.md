---
date: "2025-10-17"
phase: 6
duration: "2 weeks"
status: "Ready for Implementation"
priority: "Should Have - UX"
dependencies: ["Phase 1-5 Complete"]
---

# Phase 6: Polish & UX Enhancements
## Implementation Guide

---

## Phase Overview

Final polish to deliver professional user experience: export capabilities (CSV/PDF), mobile optimization, dark mode, keyboard shortcuts, and bulk operations. This phase transforms the MVP into a production-ready application.

**Duration**: 2 weeks
- Week 1: Export (CSV/PDF), mobile optimization, dark mode
- Week 2: Keyboard shortcuts, bulk actions, final testing

**Success Criteria**: Users can export all data, use the dashboard fluidly on mobile, toggle dark mode, and leverage keyboard shortcuts for efficiency.

---

## User Stories from PRD

### Epic 6.1: Export Capabilities

#### Story 6.1.1: Export to CSV/Excel
**As a** user
**I want to** export any table/report to CSV or Excel
**So that** I can use data in other systems

**Acceptance Criteria**:
- [ ] Export button on all data views (transactions, invoices, reports)
- [ ] Preserve formatting and calculations
- [ ] Include filters applied
- [ ] Filename includes date range (e.g., `transactions-2025-01-01-to-2025-03-31.csv`)

**Priority**: Should Have
**Dependencies**: None

---

#### Story 6.1.2: PDF Report Generation
**As a** user
**I want to** generate PDF reports for all financial statements
**So that** I can share professional documents

**Acceptance Criteria**:
- [ ] Professional formatting (header with logo, page numbers)
- [ ] Include charts as images
- [ ] Table of contents for multi-page reports
- [ ] Footer with generation date

**Priority**: Should Have
**Dependencies**: Story 6.1.1

---

### Epic 6.2: Mobile Responsiveness

#### Story 6.2.1: Mobile-Optimized Layout
**As a** user
**I want to** access the dashboard on my phone
**So that** I can check finances on-the-go

**Acceptance Criteria**:
- [ ] Responsive design down to 320px width
- [ ] Touch-friendly controls (44x44px minimum)
- [ ] Simplified charts for small screens
- [ ] Fast mobile performance (<3s load on 4G)

**Priority**: Should Have
**Dependencies**: All Phase 1-5 epics

---

### Epic 6.3: Keyboard Shortcuts

#### Story 6.3.1: Navigation Shortcuts
**As a** power user
**I want to** use keyboard shortcuts for common actions
**So that** I can work more efficiently

**Acceptance Criteria**:
- [ ] `Cmd+K` for search
- [ ] `Cmd+N` for new invoice/transaction
- [ ] `Cmd+E` for entity switcher
- [ ] `?` to show shortcut help

**Priority**: Could Have
**Dependencies**: Phase 1-4 epics

---

### Epic 6.4: Dark Mode

#### Story 6.4.1: Dark Mode Toggle
**As a** user
**I want to** toggle dark mode
**So that** I can reduce eye strain

**Acceptance Criteria**:
- [ ] Dark mode toggle in header
- [ ] Persist preference (localStorage)
- [ ] All components support dark mode
- [ ] Proper contrast ratios (WCAG AA)

**Priority**: Should Have
**Dependencies**: None

---

## Technical Requirements

### Export Functions

```typescript
// lib/export/csv.ts
import Papa from 'papaparse'

export function exportToCSV<T>(
  data: T[],
  filename: string,
  columns?: string[]
) {
  const csv = Papa.unparse(data, {
    columns,
    header: true,
  })

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `${filename}.csv`
  link.click()
}

// Usage
exportToCSV(
  transactions,
  'transactions-2025-01-01-to-2025-03-31',
  ['date', 'description', 'category', 'amount']
)
```

---

```typescript
// lib/export/pdf.ts
import { jsPDF } from 'jspdf'
import autoTable from 'jspdf-autotable'

export function exportTableToPDF(
  title: string,
  headers: string[],
  rows: string[][],
  filename: string
) {
  const doc = new jsPDF()

  // Header
  doc.setFontSize(18)
  doc.text(title, 14, 22)

  // Table
  autoTable(doc, {
    head: [headers],
    body: rows,
    startY: 30,
  })

  // Footer
  const pageCount = doc.internal.pages.length - 1
  doc.setFontSize(10)
  doc.text(
    `Generated on ${new Date().toLocaleDateString()}`,
    14,
    doc.internal.pageSize.height - 10
  )

  doc.save(`${filename}.pdf`)
}
```

---

### Mobile Optimization

**Responsive Breakpoints:**

```typescript
// hooks/use-media-query.ts
export function useMediaQuery(query: string) {
  const [matches, setMatches] = useState(false)

  useEffect(() => {
    const media = window.matchMedia(query)
    if (media.matches !== matches) {
      setMatches(media.matches)
    }

    const listener = () => setMatches(media.matches)
    media.addEventListener('change', listener)
    return () => media.removeEventListener('change', listener)
  }, [matches, query])

  return matches
}

// Usage
const isMobile = useMediaQuery('(max-width: 767px)')
const isTablet = useMediaQuery('(min-width: 768px) and (max-width: 1023px)')
const isDesktop = useMediaQuery('(min-width: 1024px)')
```

**Touch Optimization:**

```css
/* globals.css */
@media (hover: none) and (pointer: coarse) {
  /* Mobile touch devices */
  button, a {
    min-width: 44px;
    min-height: 44px;
  }
}
```

---

### Dark Mode Implementation

```typescript
// stores/ui-preferences.ts (from Phase 1, now activate)
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface UIPreferencesState {
  theme: 'light' | 'dark'
  toggleTheme: () => void
}

export const useUIPreferences = create<UIPreferencesState>()(
  persist(
    (set) => ({
      theme: 'light',
      toggleTheme: () => set((state) => ({
        theme: state.theme === 'light' ? 'dark' : 'light'
      })),
    }),
    {
      name: 'ui-preferences',
    }
  )
)
```

**Apply theme:**

```typescript
// components/layout/ThemeProvider.tsx
'use client'

import { useUIPreferences } from '@/stores/ui-preferences'
import { useEffect } from 'react'

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const { theme } = useUIPreferences()

  useEffect(() => {
    const root = document.documentElement
    root.classList.remove('light', 'dark')
    root.classList.add(theme)
  }, [theme])

  return <>{children}</>
}
```

**shadcn/ui dark mode CSS:**

```css
/* globals.css */
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 47.4% 11.2%;
    /* ... light mode variables */
  }

  .dark {
    --background: 222.2 47.4% 11.2%;
    --foreground: 210 40% 98%;
    /* ... dark mode variables */
  }
}
```

---

### Keyboard Shortcuts

```typescript
// hooks/use-keyboard-shortcuts.ts
import { useEffect } from 'react'

export function useKeyboardShortcuts() {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Cmd+K or Ctrl+K: Search
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        document.getElementById('search-input')?.focus()
      }

      // Cmd+N: New invoice/transaction
      if ((e.metaKey || e.ctrlKey) && e.key === 'n') {
        e.preventDefault()
        router.push('/invoices/new')
      }

      // Cmd+E: Entity switcher
      if ((e.metaKey || e.ctrlKey) && e.key === 'e') {
        e.preventDefault()
        document.getElementById('entity-selector')?.click()
      }

      // ?: Show shortcuts help
      if (e.key === '?') {
        e.preventDefault()
        openShortcutsDialog()
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])
}
```

**Shortcuts Help Dialog:**

```
┌─────────────────────────────────────┐
│ Keyboard Shortcuts                  │
├─────────────────────────────────────┤
│ Cmd+K     Open search               │
│ Cmd+N     New invoice/transaction   │
│ Cmd+E     Switch entity             │
│ ?         Show this help            │
│ Esc       Close dialog              │
└─────────────────────────────────────┘
```

---

## Implementation Checklist

### Week 1: Export, Mobile, Dark Mode (Days 1-5)

**Export (Days 1-2)**:
- [ ] Implement CSV export (papaparse)
- [ ] Add export button to all tables
- [ ] Implement PDF export (jsPDF + autoTable)
- [ ] Test CSV/PDF with large datasets (1000+ rows)

**Mobile Optimization (Days 3-4)**:
- [ ] Test on mobile devices (iPhone, Android)
- [ ] Fix layout issues (320px minimum width)
- [ ] Optimize touch targets (44x44px)
- [ ] Simplify charts for small screens
- [ ] Run Lighthouse mobile audit (target: 90+ score)

**Dark Mode (Day 5)**:
- [ ] Activate dark mode toggle (useUIPreferences)
- [ ] Add ThemeProvider to app layout
- [ ] Update shadcn/ui components for dark mode
- [ ] Test contrast ratios (WCAG AA compliance)

---

### Week 2: Shortcuts, Bulk Actions, Final Testing (Days 6-10)

**Keyboard Shortcuts (Days 6-7)**:
- [ ] Implement useKeyboardShortcuts hook
- [ ] Add Cmd+K (search), Cmd+N (new), Cmd+E (entity switcher)
- [ ] Create shortcuts help dialog (?)
- [ ] Test on Mac and Windows

**Bulk Actions (Days 8-9)**:
- [ ] Add bulk selection to transaction table
- [ ] Implement bulk categorization
- [ ] Implement bulk export
- [ ] Test with 100+ selected transactions

**Final Testing & Deployment (Day 10)**:
- [ ] Run full E2E test suite (Playwright)
- [ ] Lighthouse audit (target: 90+ performance, accessibility, best practices)
- [ ] Security scan (Snyk)
- [ ] Final user acceptance testing
- [ ] Deploy to production
- [ ] Tag v1.0.0 release

---

## Dependencies

### From Previous Phases
- [ ] All Phase 1-5 features complete
- [ ] No critical bugs

### External
- **Mobile Devices**: Test on real devices (iPhone, Android)
- **User Acceptance**: Final review by Harrison (user)

---

## Success Criteria

### Functional ✅
- [ ] All tables/reports export to CSV and PDF
- [ ] Dashboard works on mobile (320px minimum)
- [ ] Dark mode toggle works across all pages
- [ ] Keyboard shortcuts functional (Cmd+K, Cmd+N, Cmd+E, ?)

### Performance ✅
- [ ] Mobile load time <3s on 4G (Lighthouse)
- [ ] Lighthouse score: 90+ (performance, accessibility, best practices)
- [ ] Export 1000+ rows <5 seconds

### UX ✅
- [ ] Touch targets 44x44px minimum
- [ ] Dark mode contrast ratios meet WCAG AA
- [ ] Keyboard shortcuts discoverable (help dialog)

### Testing ✅
- [ ] E2E tests pass (Playwright)
- [ ] Mobile testing on real devices
- [ ] Cross-browser testing (Chrome, Firefox, Safari, Edge)

---

## Final Production Checklist

Before declaring MVP complete:

**Functional**:
- [ ] All 6 phases deployed
- [ ] All user stories implemented
- [ ] No critical bugs

**Performance**:
- [ ] Lighthouse score 90+ (all metrics)
- [ ] Page load <2s (desktop), <3s (mobile)
- [ ] Chart rendering <100ms

**Compliance**:
- [ ] Accountant sign-off (Phase 4 reports)
- [ ] BAS matches ATO requirements
- [ ] Financial calculations 100% accurate

**Security**:
- [ ] Supabase RLS policies tested
- [ ] No security vulnerabilities (Snyk scan)
- [ ] HTTPS enforced

**Documentation**:
- [ ] User guide (basic)
- [ ] API documentation
- [ ] Deployment guide

**User Acceptance**:
- [ ] Harrison (user) approval
- [ ] Daily usage confirmed
- [ ] Time savings validated (50% reduction in bookkeeping)

---

## Post-MVP Enhancements (Future)

Defer to future releases:
- [ ] Multi-user support (team collaboration)
- [ ] Email alerts (budget, overdue invoices)
- [ ] Xero/MYOB integration (accounting software export)
- [ ] Automated recurring transactions (cron jobs)
- [ ] Advanced ML model retraining
- [ ] Offline support (PWA)
- [ ] Multi-currency support

---

**Phase Owner**: Scrum Master (SM Agent)
**Estimated Effort**: 80 hours (2 weeks × 40 hours)
**Status**: Ready for Sprint Planning
**Milestone**: v1.0.0 MVP Release
