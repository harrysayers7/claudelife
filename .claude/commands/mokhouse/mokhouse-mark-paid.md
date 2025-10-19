---
created: "2025-10-16 12:10"
description: |
  Marks MOK HOUSE invoices as paid and completes project lifecycle. Updates payment status across
  Obsidian project files, Supabase invoice records, and Stripe invoices. Automatically sets
  completion status and tracks payment dates. Maintains sync across all systems for accurate
  financial reporting.

  Outputs:
    - Updated Obsidian project with paid status and date
    - Updated Supabase invoice record with payment info
    - Updated Stripe invoice marked as paid (out-of-band)
    - Project status set to "Complete"
    - Confirmation of payment recorded across all systems
examples:
  - /mokhouse-mark-paid "Repco project payment received today"
  - /mokhouse-mark-paid "Mark Panda Candy Provider Care invoice as paid"
  - /mokhouse-mark-paid "Payment received for Nintendo campaign, paid 2025-10-15"
---

# Mark MOK HOUSE Invoice as Paid

**Voice Transcription Note**: When Harry says "mock house" or "mok house", he means **MOK HOUSE** (all caps, two words).

This command completes the MOK HOUSE project lifecycle by marking invoices as paid and updating both Obsidian and Supabase systems.

## Usage

```bash
/mokhouse-mark-paid "[project name or invoice details]"
```

## What This Command Does

**Phase 4: Payment & Completion Tracking**

Finalizes project payment status:
1. **Identify project/invoice** → Find the project or invoice to mark paid
2. **Update Obsidian** → Set paid: true, Date Paid, status: "Complete"
3. **Update Supabase** → Set paid_amount, status: "paid", paid_on date
4. **Confirm completion** → Provide summary of changes

## Interactive Process

When you run this command, I will:

1. **Identify the project:**
   - Which project was paid?
   - Confirm project file and invoice number

2. **Determine payment date:**
   - When was payment received?
   - Default to today if not specified

3. **Update both systems:**
   - Obsidian: paid, Date Paid, status
   - Supabase: paid_amount, status, paid_on

4. **Confirm completion:**
   - Show updated project status
   - Confirm payment recorded

## Input Requirements

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

Before running, prepare:

1. **Project identification:**
   - Project name OR
   - Customer name OR
   - Invoice number

2. **Payment date (optional):**
   - Date payment was received
   - Defaults to today if not specified

## Process

### Step 1: Find Project File

**Use:** `mcp__claudelife-obsidian__simple_search` or `mcp__claudelife-obsidian__list_files`

Search in: `/02-projects/mokhouse/`

Look for:
- Matching project name
- Matching customer
- Projects with status "Invoiced" (most likely candidates)

**If multiple matches:**
- Present list with project name, customer, invoice number, amount
- Ask user to select correct project

### Step 2: Read Current State

**Use:** `mcp__claudelife-obsidian__get_file_contents`

Extract from project file:
- Current status
- Invoice number
- Customer name
- Total amount (demo fee + award fee if applicable)
- Current paid status

**Verify invoice exists:**
- If no invoice number → Ask user if invoice was created
- If invoice number exists → Proceed

### Step 3: Determine Payment Date

**Ask user or use default:**
- "When was payment received?"
- If not specified → Use today's date (YYYY-MM-DD)

### Step 4: Update Obsidian Project

**Use:** `mcp__claudelife-obsidian__patch_content`

Update frontmatter:
```yaml
paid: true
Date Paid: "YYYY-MM-DD"
status: "Complete"
```

### Step 5: Update Supabase Invoice Record

**Use:** `mcp__supabase__execute_sql`

Find invoice by invoice number:
```sql
SELECT id, total_amount FROM invoices
WHERE invoice_number = '[Invoice number from project]'
AND entity_id = '550e8400-e29b-41d4-a716-446655440002'
```

Update invoice:
```sql
UPDATE invoices
SET
  paid_amount = [total_amount],
  status = 'paid',
  paid_on = '[YYYY-MM-DD]'
WHERE id = '[Invoice ID from query]'
RETURNING id, invoice_number, paid_amount
```

### Step 6: Update Stripe Invoice Status

**CRITICAL**: After updating Supabase, the Stripe invoice must also be marked as paid to maintain sync.

#### Retrieve Stripe Invoice ID

From the Supabase query in Step 5, we have the `invoice_number` (e.g., "INV-1234").

Query Stripe for the invoice ID:

**Use:** `mcp__stripe__list_invoices`

```javascript
mcp__stripe__list_invoices({
  limit: 1
  // Filter by invoice number if possible, or search recent invoices
})
```

Alternatively, construct the Stripe dashboard URL using the invoice number pattern.

#### Mark Invoice as Paid in Stripe

**Use:** Stripe API Pay Invoice endpoint with `paid_out_of_band` parameter

The Stripe MCP server should have a tool similar to:

```javascript
// Stripe Pay Invoice (out-of-band payment)
// This marks the invoice as paid when payment was received outside Stripe
{
  invoice: "[Stripe invoice ID]",
  paid_out_of_band: true
}
```

**If the tool is not available**, use the Stripe Dashboard:

1. Open invoice in Stripe Dashboard:
   ```
   https://dashboard.stripe.com/invoices/[invoice_id]
   ```

2. Click **⋯** (overflow menu) → **Change invoice status** → **Paid**

3. Confirm the action

**Why this matters**: Keeping Stripe and Supabase in sync ensures:
- Accurate financial reporting in Stripe
- Correct invoice status for customer portal
- Proper accounting reconciliation
- No confusion when reviewing payment history

### Step 7: Provide Completion Confirmation

**Check for APRA registration requirement:**

Read project frontmatter to check if `won_project: true`:

**If won_project is true:**

```
✅ Payment Recorded
────────────────────────────
Project: [project name]
Customer: [customer]
Invoice: [invoice number]
Amount: $[amount] AUD

OBSIDIAN UPDATES
────────────────────────────
✓ paid: false → true
✓ Date Paid: [YYYY-MM-DD]
✓ status: Invoiced → Complete

SUPABASE UPDATES
────────────────────────────
✓ Invoice ID: [record ID]
✓ paid_amount: $[amount]
✓ status: sent → paid
✓ paid_on: [YYYY-MM-DD]

STRIPE UPDATES
────────────────────────────
✓ Invoice marked as paid (out-of-band)
✓ Dashboard: https://dashboard.stripe.com/invoices/[invoice_id]

────────────────────────────
Project lifecycle complete! ✓
All systems synchronized ✓
────────────────────────────

⚠️ APRA REGISTRATION REMINDER
────────────────────────────
This is an AWARDED track (won project).

Next Steps:
- [ ] Register track with APRA AMCOS
- Project: [project name]
- Project ID: [project_id]
- Client: [customer]
- Award Fee: $[award_fee] AUD

Update the frontmatter field:
  apra_registered: true

Once registered.
────────────────────────────
```

**If won_project is false (demo fee only):**

```
✅ Payment Recorded
────────────────────────────
Project: [project name]
Customer: [customer]
Invoice: [invoice number]
Amount: $[amount] AUD (Demo fee only)

OBSIDIAN UPDATES
────────────────────────────
✓ paid: false → true
✓ Date Paid: [YYYY-MM-DD]
✓ status: Invoiced → Complete

SUPABASE UPDATES
────────────────────────────
✓ Invoice ID: [record ID]
✓ paid_amount: $[amount]
✓ status: sent → paid
✓ paid_on: [YYYY-MM-DD]

STRIPE UPDATES
────────────────────────────
✓ Invoice marked as paid (out-of-band)
✓ Dashboard: https://dashboard.stripe.com/invoices/[invoice_id]

────────────────────────────
Project lifecycle complete! ✓
All systems synchronized ✓
────────────────────────────
```

## Examples

### Example 1: Simple Payment Recording

**User request:**
```
"Mark Repco project as paid"
```

**Command execution:**

1. Search for "Repco" project in mokhouse
2. Find: `251016-repco-automotive-q4.md`
3. Read current state:
   - Invoice #: INV-1234
   - Amount: $1500
   - Status: "Invoiced"
4. Ask: "When was payment received?" → User: "today"
5. Update Obsidian:
   - paid: true
   - Date Paid: "2025-10-16"
   - status: "Complete"
6. Update Supabase invoice INV-1234:
   - paid_amount: 1500
   - status: "paid"
   - paid_on: "2025-10-16"
7. Update Stripe invoice status to "paid" (out-of-band)
8. Confirm completion with all systems synced

### Example 2: Payment with Specific Date

**User request:**
```
"Panda Candy Provider Care paid on October 15th"
```

**Command execution:**

1. Find Panda Candy Provider Care project
2. Extract invoice number: INV-0166
3. Use specified date: "2025-10-15"
4. Update both systems with that date
5. Confirm payment recorded

### Example 3: Payment for Awarded Project

**User request:**
```
"Nintendo campaign payment received, they paid the award fee too"
```

**Command execution:**

1. Find Nintendo campaign project
2. Read amounts:
   - demo fee: 1500
   - award fee: 2000
   - Total: 3500
3. Update with full payment amount ($3500)
4. Mark as complete
5. Confirm all fees paid

## Payment Date Handling

**Date input formats accepted:**
- "today" → Current date
- "yesterday" → Yesterday's date
- "October 15" or "Oct 15" → Parse to YYYY-MM-DD
- "2025-10-15" → Use as-is
- No date specified → Default to today

**Date output format:**
- Always stored as YYYY-MM-DD in both systems

## Status Transitions

### Before Payment:
```yaml
status: "Invoiced"
paid: false
Date Paid: ""
```

### After Payment:
```yaml
status: "Complete"
paid: true
Date Paid: "YYYY-MM-DD"
```

### Supabase Before:
```sql
status: 'sent'
paid_amount: 0.0
paid_on: NULL
```

### Supabase After:
```sql
status: 'paid'
paid_amount: [total_amount]
paid_on: 'YYYY-MM-DD'
```

## Error Handling

**Project not found:**
- Try alternate search terms
- List recent "Invoiced" projects
- Ask user to clarify project name

**No invoice number in project:**
- Check if invoice was created
- Suggest running `/mokhouse-create-invoice` first
- Ask if user wants to continue anyway

**Supabase invoice not found:**
- Warn that Supabase record doesn't exist
- Update Obsidian only
- Suggest manual Supabase check

**Already marked as paid:**
- Show existing payment date
- Ask if user wants to update the date
- Confirm before changing

**Patch operation failed:**
- Verify file still exists
- Retry operation
- Report error details

**Stripe invoice not found:**
- Verify invoice number matches Stripe
- Check Stripe dashboard manually
- Warn user but proceed with Supabase/Obsidian updates

**Stripe update failed:**
- Report error but confirm Supabase/Obsidian updated
- Provide Stripe dashboard link for manual update
- Document the sync mismatch for follow-up

## Partial Payments

**Not currently supported by this command.**

For partial payments:
1. Use Stripe dashboard to record partial payment
2. Manually update Supabase with partial amount
3. Only use this command when fully paid

Or ask user to implement partial payment support if needed frequently.

## Award Fee Handling

**This command handles total payment automatically:**

If project has both demo fee and award fee:
- Command uses sum of both for paid_amount
- No need to specify separate amounts
- Both fees counted toward total payment

Example:
```yaml
demo fee: 1500
award fee: 2000
# Total payment recorded: $3500
```

## Evaluation Criteria

A successful payment recording should:

1. ✅ **Correct project identified** from user description
2. ✅ **Invoice verified** to exist before marking paid
3. ✅ **Proper date format** (YYYY-MM-DD) in all systems
4. ✅ **Obsidian updated** with paid: true, Date Paid, status: "Complete"
5. ✅ **Supabase updated** with paid_amount, status: "paid", paid_on
6. ✅ **Stripe updated** with invoice marked as paid (out-of-band)
7. ✅ **Correct amount** including both demo and award fees if applicable
8. ✅ **Clear confirmation** showing all system updates
9. ✅ **All systems synchronized** (Stripe, Supabase, Obsidian)
10. ✅ **Project lifecycle completed** with "Complete" status

## Related Commands

- `/mokhouse-create-project` - Create project from brief
- `/mokhouse-update-status` - Update project status during work
- `/mokhouse-create-invoice` - Create invoice when PO received

## Quick Payment Workflow

**Typical usage after payment received:**

1. Check email for payment notification
2. Run: `/mokhouse-mark-paid "[project name] paid today"`
3. Confirm project and payment date
4. Done! Project marked complete in all systems

**Time to complete:** < 30 seconds

---

**Version:** 1.0
**Integration:** Obsidian + Supabase
**File Location:** `/02-projects/mokhouse/`
**Entity:** MOK HOUSE PTY LTD (550e8400-e29b-41d4-a716-446655440002)
