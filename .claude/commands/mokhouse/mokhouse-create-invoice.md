---
created: "2025-10-16 12:00"
updated: "2025-10-27 14:30"
version_history:
  - version: "1.2"
    date: "2025-10-27 14:30"
    changes: "Updated Step 2 Obsidian status from 'PO Received' to 'awaiting PO' to match expanded status constraint; Clarified that Step 7 updates existing project record with 'sent' status"
  - version: "1.1"
    date: "2025-10-27 12:00"
    changes: "Changed Step 7 from INSERT to UPDATE: now updates existing project record (created by mokhouse-create-project) with invoice details; Added project_id lookup before update; Integrated with Supabase start_date column; Updated evaluation criteria"
  - version: "1.0"
    date: "2025-10-16 12:00"
    changes: "Initial command creation"
description: |
  Creates invoices for MOK HOUSE projects across Stripe, Supabase, and Obsidian systems. Handles
  customer lookup/setup, GST calculation, duplicate detection, and multi-system coordination.
  Requires explicit user approval before creating invoices. Updates existing project record
  (created by /mokhouse-create-project) with invoice details. Supports both existing and new
  customers with flexible GST handling and payment terms.

  Outputs:
    - Stripe invoice with product, price, and finalization
    - Supabase project record UPDATE with invoice details (contact_id, invoice_number, amounts)
    - Updated Obsidian project file with invoice number and status
    - Payment link and dashboard URLs
    - Complete success report across all systems
examples:
  - /mokhouse-create-invoice "PO-1234 for Repco project from Electric Sheep"
  - /mokhouse-create-invoice "Create invoice for Provider Care demo, PO-0166 from Panda Candy"
  - /mokhouse-create-invoice "New customer XYZ, PO-5678, $500 demo fee, charge GST"
---

# Create MOK HOUSE Invoice

**Voice Transcription Note**: When Harry says "mock house" or "mok house", he means **MOK HOUSE** (all caps, two words).

This command handles the complete invoice creation process for MOK HOUSE projects, coordinating across Stripe (billing), Supabase (records), and Obsidian (project tracking).

## Usage

```bash
/mokhouse-create-invoice "[PO details, project name, customer]"
```

## What This Command Does

**Phase 3: PO Receipt & Invoice Creation**

Complete multi-system invoice workflow:
1. **Customer Lookup** → Find or setup customer in Supabase
2. **Duplicate Detection** → Check for existing invoices with same PO
3. **GST Calculation** → Apply customer-specific GST rules
4. **User Confirmation** → Present details and wait for explicit approval
5. **Stripe Invoice** → Create product, price, invoice, and finalize
6. **Supabase Record** → Store invoice data with proper relationships
7. **Obsidian Update** → Update project status and invoice number

**CRITICAL:** This command will NOT create invoices without your explicit approval.

## Interactive Process

When you run this command, I will:

1. **Extract PO information:**
   - PO number
   - Project name/description
   - Customer name
   - Amount (from PO or project file)

2. **Lookup or setup customer:**
   - Search Supabase contacts table
   - If not found → trigger customer setup workflow
   - Load customer preferences (payment terms, GST, Stripe ID)

3. **Check for duplicates:**
   - Search Supabase for matching PO + customer
   - Warn if duplicate found
   - Confirm whether to proceed

4. **Calculate invoice amounts:**
   - Apply customer's GST preference
   - Calculate subtotal, GST, total
   - Determine payment terms and due date

5. **Present confirmation:**
   - Show complete invoice details
   - Wait for explicit "yes" to proceed
   - Do NOT create without approval

6. **Create invoice (after approval):**
   - Stripe: Product → Price → Invoice → Finalize
   - Supabase: Insert invoice record
   - Obsidian: Update project status and invoice #

7. **Provide complete report:**
   - Stripe links (payment + dashboard)
   - Supabase record IDs
   - Obsidian file updated
   - All system confirmation

## Input Requirements

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

Before running, prepare:

1. **PO information:**
   - PO number (e.g., "PO-1234" or just "1234")
   - Total amount (if not in project file)

2. **Project identification:**
   - Project name or description
   - Customer name

3. **New customer details (if applicable):**
   - Legal name
   - Email address
   - ABN (optional)
   - GST preference (charge or no charge)
   - Payment terms (default: 14 days)

## Process

### Step 1: Identify Customer from PO

**Extract from user input:**
- Customer name (e.g., "Electric Sheep Music", "Panda Candy")
- PO number

**Use:** `mcp__supabase__execute_sql`

Query contacts table:
```sql
SELECT * FROM contacts
WHERE entity_id = '550e8400-e29b-41d4-a716-446655440002'
AND (name ILIKE '%[customer name]%' OR display_name ILIKE '%[customer name]%')
AND contact_type = 'customer'
AND is_active = true
```

**If customer found:**
- Load preferences (payment terms, GST handling, Stripe customer ID)
- Proceed to duplicate check

**If customer NOT found:**
- Trigger Step 1a (New Customer Setup)

### Step 1a: New Customer Setup (When Needed)

**Prompt user for:**

1. **Legal name** (e.g., "Panda Candy Pty Ltd")
2. **Display name** (e.g., "Panda Candy")
3. **Email address** (for invoicing)
4. **ABN** (optional, for Australian businesses)
5. **Payment terms** (days, default: 14)
6. **GST handling:** "Charge GST" or "No GST"
7. **Stripe invoice template** name (e.g., "Panda Candy", "ESM Invoice Template")

**Create contact record:**

**Use:** `mcp__supabase__execute_sql`

```sql
INSERT INTO contacts (
  entity_id, contact_type, name, display_name, email,
  abn, payment_terms_days, is_active
) VALUES (
  '550e8400-e29b-41d4-a716-446655440002',
  'customer',
  '[Legal name]',
  '[Display name]',
  '[Email]',
  '[ABN or NULL]',
  [Days],
  true
) RETURNING id
```

**Link to Stripe customer:**

**Use:** `mcp__stripe__list_customers` with email filter

- If Stripe customer found → Update contact with `stripe_customer_id`
- If NOT found → Inform user (don't auto-create Stripe customers)

**Store preferences in contact metadata:**
- GST preference
- Invoice template name

### Step 2: Update Obsidian Project

**Use:** `mcp__claudelife-obsidian__patch_content`

Update project file:
```yaml
status: "awaiting PO"
PO: "[PO number without prefix]"
customer: "[Customer name]"
```

### Step 3: Check for Duplicate Invoices

**Use:** `mcp__supabase__execute_sql`

Query invoices table:
```sql
SELECT * FROM invoices
WHERE contact_id = '[Customer contact ID]'
AND purchase_order_number = '[PO number]'
AND entity_id = '550e8400-e29b-41d4-a716-446655440002'
```

**If duplicate found:**
```
⚠️  DUPLICATE INVOICE WARNING
────────────────────────────
Existing Invoice: [invoice_number]
Amount: $[amount] AUD
Status: [status]
Created: [date]

This PO has already been invoiced.

Proceed anyway? (yes/no)
────────────────────────────
```

**If no duplicate:**
- Proceed to invoice preparation

### Step 4: Prepare Invoice Details

**Retrieve from Supabase contact:**
- Payment terms days
- Email address
- Stripe customer ID
- Display name
- GST preference (from metadata or known rules)

**Determine project type and fees:**

**If total amount < $1,000:**
- Auto-set: Demo fee only (project not won)
- `demo_fee`: [total amount]
- `award_fee`: 0
- `won_project`: false
- `apra_registered`: false (not needed for non-won projects)

**If total amount ≥ $1,000:**
- Ask: "Did you win this project? (yes/no)"
- If **yes**:
  - Ask: "What was the demo fee?" (default: $500)
  - Calculate: `award_fee = total - demo_fee`
  - Set: `won_project: true`, `apra_registered: false`
- If **no**:
  - Set: `demo_fee: [total]`, `award_fee: 0`, `won_project: false`

**Determine GST handling:**

**Known GST Rules:**
- **Electric Sheep Music:** No GST (legacy agreement)
- **Panda Candy:** No GST (per agreement)
- **New customers:** Ask user explicitly

**Calculate amounts:**

**If GST is charged:**
```
Subtotal = PO amount ÷ 1.1
GST = Subtotal × 0.1
Total = PO amount
```

**If NO GST charged:**
```
Subtotal = PO amount
GST = 0
Total = PO amount
```

**Calculate due date:**
```
Due Date = Today + Payment Terms Days
```

**Generate next project ID:**
```sql
SELECT project_id FROM invoices
WHERE entity_id = '550e8400-e29b-41d4-a716-446655440002'
ORDER BY project_id DESC LIMIT 1;
```
- Extract number from last ID (e.g., "MH-017" → 17)
- Increment and format: "MH-018"

### Step 5: Confirm Invoice Details (WAIT FOR APPROVAL)

**Present summary and STOP:**

```
📋 Invoice Details for Approval
────────────────────────────
Client: [Customer legal name]
Job Number: [Job number]
PO Number: PO-[####]
Description: [Project description]

Amount (excl GST): $[amount] AUD
GST: $[gst] AUD ([GST % or "No GST"])
Total: $[total] AUD

Product Line: [Description] PO-[####]
Due: [Due date] ([payment terms] days)
Issue Date: [Today's date]

Issued By: MOK HOUSE PTY LTD
Customer: [Customer legal name]
Email: [Customer email]
Stripe Customer ID: [Stripe ID]

Integrations: Stripe ✓ | Obsidian ✓ | Supabase ✓
Template: [Template name]
────────────────────────────

⚠️  Proceed with invoice creation? (yes/no)
```

**Do NOT proceed without explicit "yes" from user.**

### Step 6: Create Invoice in Stripe

**CRITICAL:** Stop immediately if any step fails. Execute in order:

#### 6.1: Verify Customer Exists

**Use:** `mcp__stripe__list_customers` with email parameter

- If not found → Stop and inform user
- If found → Confirm Stripe customer ID matches contact record

#### 6.2: Create Product

**Use:** `mcp__stripe__create_product`

```javascript
{
  name: "[Description] PO-[####]",
  description: "Demo Fee for Job [####]"
}
```

Store product ID for next step.

#### 6.3: Create Price

**Use:** `mcp__stripe__create_price`

```javascript
{
  product: "[Product ID from 6.2]",
  unit_amount: [Total amount × 100], // Convert AUD to cents
  currency: "aud"
}
```

Store price ID for next step.

#### 6.4: Create Draft Invoice

**Use:** `mcp__stripe__create_invoice`

```javascript
{
  customer: "[Stripe customer ID]",
  days_until_due: [Payment terms from contact]
}
```

Store invoice ID for next steps.

#### 6.5: Add Line Item

**Use:** `mcp__stripe__create_invoice_item`

```javascript
{
  customer: "[Stripe customer ID]",
  price: "[Price ID from 6.3]",
  invoice: "[Invoice ID from 6.4]"
}
```

#### 6.6: Finalize Invoice

**Use:** `mcp__stripe__finalize_invoice`

```javascript
{
  invoice: "[Invoice ID from 6.4]"
}
```

Returns:
- Invoice number (from Stripe)
- Hosted invoice URL (payment link)
- Invoice ID (for dashboard link)

**If any step fails:**
- Report which step failed with error details
- Do NOT continue to next steps
- Do NOT create Supabase/Obsidian records
- Offer retry options

### Step 7: Record Invoice in Supabase (UPDATE existing project)

**Use:** `mcp__supabase__execute_sql`

**Only execute AFTER Stripe finalization succeeds.**

**IMPORTANT:** This step UPDATES the existing project record (created in `/mokhouse-create-project`) with invoice details. The project_id must already exist in the invoices table.

**First, lookup the existing project record:**

```sql
SELECT id, project_id FROM public.invoices
WHERE entity_id = '550e8400-e29b-41d4-a716-446655440002'
AND project_id = '[Project ID from command argument, e.g., MH-018]'
AND contact_id IS NULL  -- Project records have NULL contact_id
LIMIT 1;
```

**Then UPDATE with invoice details:**

```sql
UPDATE public.invoices
SET
  contact_id = '[Contact ID from customer lookup]',
  invoice_type = 'receivable',
  invoice_number = '[Invoice number from Stripe]',
  invoice_date = '[Today YYYY-MM-DD]',
  due_date = '[Due date YYYY-MM-DD]',
  subtotal_amount = [Subtotal],
  gst_amount = [GST amount],
  total_amount = [Total],
  paid_amount = 0.0,
  status = 'sent',
  currency = 'AUD',
  purchase_order_number = '[PO number without prefix]',
  description = '[Project description]',
  project = '[Project name]',
  client = '[Customer legal name]',
  billed_to = '[Customer display name]'
WHERE
  entity_id = '550e8400-e29b-41d4-a716-446655440002'
  AND project_id = '[Project ID, e.g., MH-018]'
RETURNING id, project_id, invoice_number
```

**Store returned:**
- `invoice_record_id` (the updated project record)
- Confirm `project_id` and `invoice_number` match expectations

### Step 8: Update Obsidian Project

**Use:** `mcp__claudelife-obsidian__patch_content`

Update project frontmatter (project_id already exists from `/mokhouse-create-project`):
```yaml
status: "Invoiced"
"Invoice #": "[Invoice number from Stripe]"
demo_fee: [Demo fee amount]
award_fee: [Award fee amount or 0]
won_project: [true/false]
apra_registered: false
```

### Step 9: Provide Complete Success Report

```
✅ Invoice Created Successfully
────────────────────────────

PROJECT DETAILS
────────────────────────────
Client: [Customer name]
Job Number: [Job number]
PO Number: PO-[####]
Description: [Description]

INVOICE DETAILS
────────────────────────────
Invoice Number: [Stripe invoice number]
Amount: $[total] AUD ([GST status])
Issue Date: [YYYY-MM-DD]
Due Date: [YYYY-MM-DD]
Status: Sent

STRIPE
────────────────────────────
✓ Product Created: [product ID]
✓ Price Created: [price ID]
✓ Invoice Finalized

Payment Link:
[Hosted invoice URL]

Dashboard Link:
https://dashboard.stripe.com/invoices/[invoice_id]

SUPABASE
────────────────────────────
✓ Contact: [contact ID] ([customer name])
✓ Project Updated: [project ID, e.g., MH-018] ([invoice record ID])

OBSIDIAN
────────────────────────────
✓ Project Updated: [project file]

SEND TO
────────────────────────────
[Customer email]

────────────────────────────
All systems updated successfully!
```

## Known Customers Reference

### Electric Sheep Music Pty Ltd
```yaml
Contact ID: cadaf83f-9fee-4891-8bb3-5dbc14433a99
Stripe ID: cus_T7k1T3pHOO9mXg
Email: esmusic@dext.cc
Payment Terms: 14 days
GST: No GST charged
Template: "ESM Invoice Template"
Display Name: "Electric Sheep Music"
```

### Panda Candy Pty Ltd
```yaml
Contact ID: 7459d407-5fb9-4951-ad0e-b37cb639fe5a
Stripe ID: cus_TErB6bmyo2T2nb
Email: accounts@pandacandy.com.au
ABN: 48648289696
Payment Terms: 14 days
GST: No GST charged
Template: "Panda Candy"
Display Name: "Panda Candy"
```

## Examples

### Example 1: Known Customer Invoice

**User request:**
```
"Create invoice for Repco project, PO-1234 from Electric Sheep, $1500"
```

**Command execution:**

1. Look up "Electric Sheep" in Supabase contacts → Found
2. Load preferences: 14 day terms, no GST
3. Check for duplicate PO-1234 → None found
4. Calculate amounts:
   - Subtotal: $1500
   - GST: $0 (no GST)
   - Total: $1500
5. Present confirmation with all details
6. **WAIT for user approval**
7. After "yes":
   - Create Stripe invoice (6 steps)
   - Record in Supabase
   - Update Obsidian project
8. Provide complete success report with links

### Example 2: New Customer Invoice

**User request:**
```
"Invoice for new customer Acme Corp, PO-5678, $2200"
```

**Command execution:**

1. Search Supabase for "Acme Corp" → Not found
2. **Trigger customer setup:**
   - Prompt for: legal name, email, ABN, payment terms, GST preference
   - Create contact in Supabase
   - Link to Stripe customer if exists
3. Proceed with normal invoice flow
4. Calculate with GST (if user said to charge):
   - Subtotal: $2000
   - GST: $200
   - Total: $2200
5. Present confirmation
6. Create after approval
7. Complete success report

### Example 3: Duplicate Detection

**User request:**
```
"Create invoice for Panda Candy, PO-0166"
```

**Command execution:**

1. Look up Panda Candy → Found
2. Check for duplicate → Found existing invoice INV-001
3. **Show warning:**
   ```
   ⚠️  DUPLICATE INVOICE WARNING
   Existing Invoice: INV-001
   Amount: $500 AUD
   Status: sent
   Created: 2025-10-10

   Proceed anyway? (yes/no)
   ```
4. If user says "no" → Stop, suggest checking existing invoice
5. If user says "yes" → Proceed with normal flow

## Error Handling

### Gmail/Project Issues
- **Project file not found:** Search mokhouse projects, ask user to clarify
- **Missing PO amount:** Ask user for amount or find in project brief

### Customer Issues
- **Customer not in database:** Trigger customer setup workflow
- **Stripe customer not found:** Inform user, ask if they want to create one
- **Missing GST preference:** Ask user explicitly

### Stripe Issues
- **Product creation fails:** Report error, stop workflow
- **Price creation fails:** Report error, stop workflow
- **Invoice creation fails:** Report error, do NOT create Supabase record
- **Finalization fails:** Report error, invoice remains in draft

### Supabase Issues
- **Insert fails:** Report error, but Stripe invoice still exists (warn user)
- **Duplicate constraint:** Treat as duplicate warning

### Obsidian Issues
- **Patch fails:** Report error, but invoice already created (warn user)

## MOK HOUSE Entity Reference

```yaml
Entity ID: 550e8400-e29b-41d4-a716-446655440002
Legal Name: MOK HOUSE PTY LTD
ABN: 38690628212
ACN: 690628212
Trading Name: Mok House
GST Registered: Yes
Bank Details:
  Account Name: MOK HOUSE PTY LTD
  Account Number: 612281562
  BSB: 013943
```

## Critical Rules

1. ✅ **Always query Supabase contacts** before invoice creation
2. ✅ **Never hardcode customer details** - always look up from database
3. ✅ **Always trigger customer setup** if contact not found
4. ✅ **Always ask user about GST** for new customers
5. ✅ **Always confirm invoice details** before Stripe creation
6. ✅ **Always check Obsidian and Supabase** for duplicates first
7. ✅ **Always use exact IDs** from database lookups
8. ✅ **Always convert AUD → cents** for Stripe (amount × 100)
9. ✅ **Always provide payment + dashboard links**
10. ✅ **Always update all systems** (Stripe, Supabase, Obsidian)
11. ❌ **Never create without explicit confirmation**
12. ❌ **Never assume customer details** if unclear
13. ❌ **Never continue if Stripe creation fails**
14. ❌ **Stop and ask** if customer not in database

## Evaluation Criteria

A successful invoice creation should:

1. ✅ **Correct customer identified** or properly setup if new
2. ✅ **Duplicate check performed** before creation
3. ✅ **Proper GST calculation** based on customer preference
4. ✅ **User confirmation obtained** before any creation
5. ✅ **Stripe invoice complete** with all 6 steps successful
6. ✅ **Existing project record found** by project_id (created in `/mokhouse-create-project`)
7. ✅ **Supabase project updated** with invoice details via UPDATE (not INSERT)
8. ✅ **Obsidian project updated** with invoice number and status
9. ✅ **Complete report provided** with all system links
10. ✅ **Proper error handling** if any step fails
11. ✅ **No orphaned records** if workflow stops mid-way

## Related Commands

- `/mokhouse-create-project` - Create project from brief (before invoice)
- `/mokhouse-update-status` - Update project to "PO Received" status
- `/mokhouse-mark-paid` - Mark invoice as paid after payment received

---

**Version:** 1.0
**Integration:** Stripe + Supabase + Obsidian
**Entity:** MOK HOUSE PTY LTD (550e8400-e29b-41d4-a716-446655440002)
