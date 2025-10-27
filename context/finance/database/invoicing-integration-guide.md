---
date: "2025-10-25"
date created: Sat, 10 25th 25, 1:11:10 pm
date modified: Sat, 10 25th 25, 1:12:11 pm
---

# Invoicing Schema Integration Guide

## 🔗 How the New Invoicing Schema Works With Your Existing System

Your existing system has:
- **public.entities** (3 rows): MOK HOUSE PTY LTD, MOKAI, Trusts
- **public.contacts** (3 rows): Electric Sheep Music, suppliers, team members
- **public.invoices** (31 rows): All invoices from both businesses

The new **invoicing schema** extends this WITHOUT duplication:

```
┌─────────────────────────────────────────┐
│         public.invoices (existing)      │
│  - invoice_number (e.g., "INV-2025-1") │
│  - entity_id (MOK HOUSE, MOKAI)        │
│  - contact_id (Electric Sheep Music)   │
│  - project_id (DiDi, Repco, Nintendo) │
│  - total_amount                         │
│  - status (draft/sent/paid)            │
│  - created_at: 31 existing invoices    │
└─────────────────────────────────────────┘
           ↓ (foreign key references)
┌─────────────────────────────────────────┐
│      invoicing schema (NEW)             │
│  ├─ invoice_items (line items)         │
│  ├─ invoice_payments (payment tracking)│
│  ├─ invoice_settings (MH-2025-001, etc)│
│  ├─ invoice_pdfs (generated PDFs)      │
│  └─ email_deliveries (SMTP log)        │
└─────────────────────────────────────────┘
```

## 📋 Integration Points

### 1. Your Existing Invoice System
```sql
-- Your current invoices table (unchanged)
SELECT * FROM public.invoices;
-- Result: 31 invoices for MOK HOUSE, MOKAI
-- Fields: invoice_number, entity_id, contact_id, project_id, project, status
```

### 2. Client References
```sql
-- Reuse existing contacts (Electric Sheep Music, etc.)
SELECT c.name, c.project, c.email
FROM public.contacts c
WHERE c.entity_id = (SELECT id FROM public.entities WHERE name = 'MOK HOUSE PTY LTD');
-- Result: Electric Sheep Music, other clients (reused!)
```

### 3. Project Tracking
```sql
-- Your existing project system is preserved
SELECT DISTINCT project, project_id
FROM public.invoices
WHERE entity_id = (SELECT id FROM public.entities WHERE name = 'MOK HOUSE PTY LTD');
-- Result: DiDi, Repco, Nintendo, Nintendo - EM (your projects)
```

### 4. Invoice Numbering System
```sql
-- Your new invoice number generation (MH-2025-001, MK-2025-001, etc.)
SELECT invoicing.get_next_invoice_number(entity_id);
-- Automatically generates: MH-2025-001, MH-2025-002, etc.
-- Resets prefix per entity (MOK HOUSE = "MH", MOKAI = "MK")
```

## 🔄 Data Flow For Invoice Creation

### Step 1: Create Invoice in public.invoices
```sql
INSERT INTO public.invoices (
  entity_id,              -- MOK HOUSE entity_id
  contact_id,             -- Electric Sheep Music contact_id
  invoice_number,         -- MH-001 (auto-generated)
  purchase_order_number,  -- "0896" (client's PO reference)
  invoice_date,           -- TODAY
  due_date,               -- TODAY + 14 days
  subtotal_amount,        -- $1000
  gst_amount,             -- $100
  total_amount,           -- $1100
  status,                 -- draft
  project,                -- "DiDi"
  project_id              -- existing project ID
)
VALUES (...) RETURNING id;
-- Returns: new invoice UUID
```

### Step 2: Add Line Items
```sql
INSERT INTO invoicing.invoice_items (
  invoice_id,             -- UUID from step 1
  description,            -- "Music Composition - Track 1"
  quantity,               -- 1
  unit_price,             -- 1000.00
  tax_rate                -- 10 (for GST)
)
VALUES (...);
-- Auto-calculates: line_total = 1000, line_tax = 100
```

### Step 3: Generate PDF
```sql
-- Query the view with all details (includes PO number)
SELECT * FROM invoicing.v_invoice_with_items
WHERE id = 'invoice-uuid';

-- Returns:
-- {
--   invoice_number: "MH-001",
--   purchase_order_number: "0896",
--   client_name: "Electric Sheep Music",
--   client_email: "booking@esp.com",
--   entity_name: "MOK HOUSE PTY LTD",
--   entity_abn: "12345678901",
--   items: [
--     { description: "Music Composition", quantity: 1, unit_price: 1000, line_tax: 100 }
--   ],
--   total_amount: 1100,
--   gst_amount: 100,
--   bank_details: { ... }
-- }
```

### Step 4: Store PDF
```sql
INSERT INTO invoicing.invoice_pdfs (
  invoice_id,
  pdf_url,                -- Supabase Storage path
  file_name,              -- "MH-2025-001.pdf"
  generated_at
)
VALUES (...);
```

### Step 5: Send Email
```sql
INSERT INTO invoicing.email_deliveries (
  invoice_id,
  recipient_email,        -- electric.sheep.music@email.com
  status                  -- pending
)
VALUES (...);
-- Mark as 'sent' after SMTP delivery
```

### Step 6: Track Payment
```sql
INSERT INTO invoicing.invoice_payments (
  invoice_id,
  amount_paid,            -- 1100
  payment_date,           -- TODAY
  payment_method,         -- "bank_transfer"
  reference               -- "ESP-001"
)
VALUES (...);

-- Check payment status
SELECT * FROM invoicing.v_invoice_payment_status
WHERE invoice_id = 'invoice-uuid';
-- Returns: payment_status = 'paid', remaining_balance = 0
```

## 🗂️ Invoice Number Format Per Entity

Your system auto-generates invoice numbers based on entity with simple, clean numbering:

| Entity | Prefix | Format | Example |
|--------|--------|--------|---------|
| MOK HOUSE PTY LTD | MH | MH-NNN | MH-001, MH-002, MH-003 |
| MOKAI PTY LTD | MK | MK-NNN | MK-001, MK-002, MK-003 |
| Other Entities | INV | INV-NNN | INV-001, INV-002 |

**Customizable**: Edit `invoicing.invoice_settings.invoice_prefix` to use your own format or adjust numbering strategy.

## 🔐 Linking to Existing Data

### Existing Clients (Electric Sheep Music)
```sql
-- Already in public.contacts - fully reused
SELECT * FROM public.contacts WHERE name = 'Electric Sheep Music';
-- Rows: name, email, phone, billing_address, project, stripe_customer_id
```

### Existing Project IDs
```sql
-- Your projects are fully preserved
SELECT DISTINCT project, project_id FROM public.invoices;
-- All 31 invoices can link to invoicing schema items
```

### Entity Separation
```sql
-- MOK HOUSE invoices stay with MOK HOUSE entity
SELECT * FROM invoicing.v_invoice_details
WHERE entity_id = (SELECT id FROM public.entities WHERE name = 'MOK HOUSE PTY LTD');

-- MOKAI invoices stay with MOKAI entity
SELECT * FROM invoicing.v_invoice_details
WHERE entity_id = (SELECT id FROM public.entities WHERE name ILIKE '%MOKAI%');
```

## 📊 Schema Tables Reference

### public.invoices (YOUR EXISTING TABLE)
- `invoice_number`: TEXT (e.g., "MH-2025-001")
- `entity_id`: FK → public.entities
- `contact_id`: FK → public.contacts
- `project`: VARCHAR (e.g., "DiDi", "Repco")
- `project_id`: VARCHAR (your project ID)
- **NOT CHANGED** - fully backward compatible

### invoicing.invoice_items (NEW)
- `invoice_id`: FK → public.invoices(id)
- `description`: Text of line item
- `quantity`, `unit_price`: Numbers
- `line_total`, `line_tax`: Auto-calculated

### invoicing.invoice_payments (NEW)
- `invoice_id`: FK → public.invoices(id)
- `amount_paid`: Amount of payment
- `payment_date`: When paid
- `payment_method`: "bank_transfer", "credit_card", etc.

### invoicing.invoice_settings (NEW)
- `entity_id`: FK → public.entities(id)
- `invoice_prefix`: "MH", "MK", "INV"
- `next_invoice_number`: Auto-incremented counter
- `bank_details`: JSONB for bank account info

### invoicing.invoice_pdfs (NEW)
- `invoice_id`: FK → public.invoices(id)
- `pdf_url`: Supabase Storage URL
- `file_name`: e.g., "MH-2025-001.pdf"

### invoicing.email_deliveries (NEW)
- `invoice_id`: FK → public.invoices(id)
- `recipient_email`: Email address
- `status`: pending/sent/failed/bounced/opened
- `opened_at`, `opened_count`: Tracking

## 🚀 Ready to Implement?

The `migrate-invoicing-schema.sql` file contains:
1. ✅ Full schema with 5 new tables
2. ✅ Foreign keys to YOUR existing data
3. ✅ 4 ready-to-use views for PDF/email
4. ✅ Functions for invoice number generation
5. ✅ Auto-populated settings for your entities

Next steps:
1. Review this schema structure with your existing 31 invoices
2. Run migration: `psql $SUPABASE_URL -f migrate-invoicing-schema.sql`
3. Verify integration: `SELECT * FROM invoicing.v_invoice_details;`
4. Build PDF generation (Puppeteer template)
5. Build email delivery (SMTP integration)
6. Expose as MCP server
