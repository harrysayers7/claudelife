---
date: "2025-10-27 12:00"
title: "MOK HOUSE Project-Invoice Integration Guide"
---

# MOK HOUSE Project-Invoice Integration

Quick reference for how `/mokhouse-create-project` and `/mokhouse-create-invoice` work together.

## Overview

The commands work as a **two-phase system**:
1. **Phase 1**: Project brief → Obsidian file + Supabase project record
2. **Phase 2**: PO receipt → Stripe invoice + Supabase update

## Workflow

### Phase 1: /mokhouse-create-project

**Triggered when**: Client brief email arrives

**What it does**:
```
1. Search Gmail for brief email
2. Extract Google Doc content
3. Create Obsidian project file
4. Generate AI suggestions & SUNO prompt
5. INSERT into public.invoices:
   - project_id (MH-001, MH-002, etc.)
   - project_name
   - client
   - start_date (today)
   - status: 'Brief Received'
```

**Outputs**:
- ✅ Obsidian file in `/02-projects/mokhouse/` with `project_id` in frontmatter
- ✅ Supabase row with project metadata
- ✅ AI suggestions & SUNO prompt

---

### Phase 2: /mokhouse-create-invoice

**Triggered when**: Purchase Order (PO) arrives

**What it does**:
```
1. Look up customer in Supabase
2. Check for duplicate POs
3. Get user approval
4. Create Stripe invoice
5. UPDATE existing project record:
   - WHERE entity_id=... AND project_id='MH-XXX'
   - SET contact_id, invoice_number, amounts, status='sent'
```

**Outputs**:
- ✅ Stripe invoice finalized
- ✅ Supabase project row UPDATED with invoice details
- ✅ Obsidian file updated with invoice number & status

---

## Data Fields

### Supabase Invoices Table (Project Record)

**Created in Phase 1** (`/mokhouse-create-project`):
```yaml
entity_id: "550e8400-e29b-41d4-a716-446655440002"  # MOK HOUSE
project_id: "MH-001"                               # Generated (MH-###)
project_name: "Repco Automotive Q4"
client: "Electric Sheep Music"
start_date: "2025-10-27"                           # Today
status: "Brief Received"
```

**Updated in Phase 2** (`/mokhouse-create-invoice`):
```yaml
contact_id: "cadaf83f-9fee-4891-8bb3-5dbc14433a99"
invoice_number: "INV-001234"
invoice_date: "2025-10-27"
due_date: "2025-11-10"
subtotal_amount: 1500.00
gst_amount: 0
total_amount: 1500.00
purchase_order_number: "1234"
status: "sent"
# ... other invoice fields
```

### Obsidian Project File

**Frontmatter added in Phase 1**:
```yaml
project_id: "MH-001"
project name: "Repco Automotive Q4"
customer: "Electric Sheep Music"
status: "Brief Received"
start date: "2025-10-27"
```

**Frontmatter updated in Phase 2**:
```yaml
status: "Invoiced"
Invoice #: "INV-001234"
demo_fee: 500
award_fee: 1000
won_project: true
```

---

## Key Points

✅ **project_id is the link**: Generated once in Phase 1, used to find project in Phase 2
✅ **Dual-purpose table**: `public.invoices` stores both project metadata AND invoice details
✅ **start_date**: Tracks project commencement (set automatically to today)
✅ **Single record**: One row per project, updated as invoice is added
✅ **Dependency**: Phase 2 requires Phase 1 to have run first

---

## Common Queries

### Find all projects without invoices
```sql
SELECT project_id, project_name, client, start_date
FROM public.invoices
WHERE entity_id = '550e8400-e29b-41d4-a716-446655440002'
AND invoice_number IS NULL
ORDER BY start_date DESC;
```

### Find all invoiced projects
```sql
SELECT project_id, project_name, client, invoice_number, total_amount
FROM public.invoices
WHERE entity_id = '550e8400-e29b-41d4-a716-446655440002'
AND invoice_number IS NOT NULL
ORDER BY invoice_date DESC;
```

### Find projects by client
```sql
SELECT project_id, project_name, status, invoice_number
FROM public.invoices
WHERE entity_id = '550e8400-e29b-41d4-a716-446655440002'
AND client = 'Electric Sheep Music'
ORDER BY start_date DESC;
```

---

## Phase Comparison

| Aspect | Phase 1 (Create Project) | Phase 2 (Create Invoice) |
|--------|---|---|
| **Trigger** | Client brief email | PO arrives |
| **Command** | `/mokhouse-create-project` | `/mokhouse-create-invoice` |
| **DB Operation** | INSERT project row | UPDATE project row |
| **project_id** | Generated | Used |
| **Obsidian** | Create file | Update file |
| **Stripe** | None | Create invoice |
| **Status** | "Brief Received" | "Invoiced" |

---

**Last updated**: 2025-10-27
**Version**: 1.0
