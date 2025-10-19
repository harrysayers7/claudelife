---
created: "2025-10-19 17:00"
version: "1.0"
description: |
  Syncs paid invoice data from Supabase to MOK HOUSE dashboard for accurate 12-month average calculation.
  Updates the supabasePaidInvoices array in mokhouse-dashboard.md with latest payment data from the database.
---

# Sync MOK HOUSE Invoice Data from Supabase

This command updates the MOK HOUSE dashboard with the latest paid invoice data from Supabase to ensure accurate 12-month average income calculations.

## What This Command Does

1. **Query Supabase** for all invoices paid in the last 12 months for MOK HOUSE entity
2. **Read dashboard file** to find the `supabasePaidInvoices` array
3. **Update the array** with fresh data from Supabase
4. **Update timestamp** to show when data was last synced

## Usage

```bash
/mokhouse-sync-invoices
```

## Process

### Step 1: Query Supabase for Paid Invoices

**Use:** `mcp__supabase__execute_sql`

Execute this query:
```sql
SELECT
  invoice_number,
  total_amount,
  paid_on
FROM invoices
WHERE entity_id = '550e8400-e29b-41d4-a716-446655440002'
AND status = 'paid'
AND paid_on IS NOT NULL
AND paid_on >= (CURRENT_DATE - INTERVAL '12 months')
ORDER BY paid_on DESC;
```

**Entity ID Reference:**
- MOK HOUSE: `550e8400-e29b-41d4-a716-446655440002`

### Step 2: Read Dashboard File

**Use:** `Read` tool

Read `/Users/harrysayers/Developer/claudelife/01-areas/business/mokhouse/mokhouse-dashboard.md`

Find the section containing:
```javascript
const supabasePaidInvoices = [
    // ... invoice data
];
```

### Step 3: Update Dashboard Data

**Use:** `Edit` tool

Replace the `supabasePaidInvoices` array with fresh Supabase data:

```javascript
// Calculate 12-month average income from Supabase invoice data
// This data is fetched from Supabase invoices table (entity_id: MOK HOUSE)
// Data source: Supabase invoices.paid_on dates (more accurate than Obsidian frontmatter)
// Last updated: YYYY-MM-DD
const supabasePaidInvoices = [
    { invoice_number: "INV-XXX", total_amount: XXXX, paid_on: "YYYY-MM-DD" },
    // ... all invoices from Supabase query
];

// Calculate total from Supabase data (last 12 months)
const last12MonthsRevenue = supabasePaidInvoices.reduce((sum, inv) => sum + inv.total_amount, 0);
const monthlyAverage = last12MonthsRevenue / 12;

// Note: Run /mokhouse-sync-invoices to update this data from Supabase
```

**Format requirements:**
- `total_amount`: Convert from string to number (remove decimal points, e.g., "3300.00" → 3300)
- `paid_on`: Keep as YYYY-MM-DD string format
- `invoice_number`: Keep as string
- Update "Last updated" comment with current date (YYYY-MM-DD)

### Step 4: Verify Results

Calculate and display:
```
✅ Invoice Data Synced to Dashboard
────────────────────────────────────
Invoices found: [count]
Total 12-month revenue: $[amount]
Monthly average: $[average]
Last updated: [YYYY-MM-DD]
────────────────────────────────────
Dashboard location: mokhouse-dashboard.md
```

## When to Run This Command

- After marking an invoice as paid using `/mokhouse-mark-paid`
- Monthly, to ensure dashboard shows accurate financial data
- When you notice the dashboard 12-month average seems outdated
- After creating new invoices in Supabase

## Technical Details

### Data Flow
1. **Supabase** (`invoices.paid_on`) → Source of truth for payment dates
2. **Dashboard** (`supabasePaidInvoices` array) → Used for 12-month average calculation
3. **Obsidian frontmatter** (`Date Paid` field) → Still tracked for reference, but not used in financial calculations

### Why This Approach

- **Accuracy**: Supabase `paid_on` dates are more reliable than manual Obsidian frontmatter updates
- **Consistency**: Single source of truth for financial data
- **Performance**: Pre-calculated array in dashboard is fast to render
- **Maintainability**: Easy to update via slash command

## Example Output

```javascript
// Last updated: 2025-10-19
const supabasePaidInvoices = [
    { invoice_number: "HS-FF-001", total_amount: 3300, paid_on: "2025-12-16" },
    { invoice_number: "HS-STK-001", total_amount: 1000, paid_on: "2025-11-18" },
    { invoice_number: "NLOLWU0R-0003", total_amount: 4500, paid_on: "2025-10-17" },
    { invoice_number: "INV-58", total_amount: 5250, paid_on: "2025-10-03" },
    // ... more invoices
];
```

## Error Handling

**Supabase query fails:**
- Verify project ID is correct (`gshsshaodoyttdxippwx`)
- Check entity ID matches MOK HOUSE
- Confirm Supabase MCP server is connected

**Dashboard file modified:**
- Read file again before attempting edit
- Verify `supabasePaidInvoices` array still exists in expected location

**Data format issues:**
- Convert total_amount from string to number
- Ensure paid_on is valid date format (YYYY-MM-DD)
- Remove any null or invalid records

## Related Commands

- `/mokhouse-mark-paid` - Marks invoice as paid (updates Supabase `paid_on` date)
- `/mokhouse-create-invoice` - Creates new invoice in Supabase

---

**Version:** 1.0
**Integration:** Supabase + Obsidian
**File Location:** `01-areas/business/mokhouse/mokhouse-dashboard.md`
**Entity ID:** MOK HOUSE (`550e8400-e29b-41d4-a716-446655440002`)
