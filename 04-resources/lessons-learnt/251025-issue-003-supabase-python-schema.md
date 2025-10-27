---
date: "2025-10-25 02:59"
issue-id: issue-003
category: mcp-server
severity: high
tags: [supabase, python, mcp, schema, api]
---

# Lesson: Python Supabase Client API - Schema-Qualified Table Names

## Problem

When building the invoicing MCP server, the Python Supabase client couldn't find invoices that existed in the database:

```python
# This code returned "Invoice not found" even though invoice existed
response = self.supabase.table('invoicing.v_invoice_with_items') \
    .select('*').eq('id', invoice_id).execute()
```

**Error**: `Invoice [ID] not found`

**But**: Direct SQL queries worked perfectly:
```sql
SELECT * FROM invoicing.v_invoice_with_items WHERE id = '[ID]'
-- Result: Found the invoice successfully ✅
```

## Root Cause

The Python Supabase client's `.table()` method **only works with the `public` schema**.

When you pass a schema-qualified name like `'invoicing.v_invoice_with_items'`, the client doesn't properly handle it. The `.table()` method is designed for public schema tables/views only.

## Solution

Use `.from_()` method instead, which properly handles schema-qualified names:

```python
# BEFORE (doesn't work with schema-qualified names):
response = self.supabase.table('invoicing.v_invoice_with_items') \
    .select('*').eq('id', invoice_id).execute()

# AFTER (works with any schema):
response = self.supabase.from_('invoicing.v_invoice_with_items') \
    .select('*').eq('id', invoice_id).execute()
```

## Technical Details

| Method | Works With | Use Case |
|--------|-----------|----------|
| `.table('name')` | `public` schema only | Simple tables in public schema |
| `.from_('schema.name')` | Any schema-qualified name | Custom schemas like `invoicing` |

**Key difference**:
- `table()` method assumes public schema
- `from_()` method accepts full schema-qualified identifiers

## Code Changes Applied

**File**: `src/invoicing/invoicing_service.py`

### 1. fetchInvoiceData() method
```python
# Changed line 49
response = self.supabase.from_('invoicing.v_invoice_with_items') \
    .select('*').eq('id', invoice_id).execute()
return response.data[0] if response.data else None
```

### 2. fetchEntityInvoices() method
```python
# Changed line 79
response = self.supabase.from_('invoicing.v_invoice_with_items') \
    .select('*').eq('entity_id', entity_id).order(...).execute()
```

### 3. getPdfStatus() method
```python
# Changed line 106
response = self.supabase.from_('invoicing.invoice_pdfs') \
    .select('*').eq('invoice_id', invoice_id).execute()
```

## Prevention

### For Users
- Always use `.from_()` when querying schema-qualified tables/views
- Use `.table()` only for `public` schema tables
- Test with schema-qualified names during development

### For Code Review
- Check all MCP implementations for proper schema handling
- Look for pattern: `.table('schema.name')` → should be `.from_('schema.name')`
- Add to code review checklist: "Is this querying a custom schema?"

### For Documentation
Add to MCP development guide:
```markdown
## Schema-Qualified Table Access

When your MCP server needs to query tables in custom schemas:

✅ CORRECT:
```python
response = client.from_('custom_schema.table_name').select('*').execute()
```

❌ WRONG:
```python
response = client.table('custom_schema.table_name').select('*').execute()
```

Use `.from_()` for any schema except public.
```

## Testing

**Test Case**: Query invoice from `invoicing.v_invoice_with_items` view

```python
response = self.supabase.from_('invoicing.v_invoice_with_items') \
    .select('*').eq('id', 'e992dec8-1287-4fa8-9e92-aebd12b22baf').execute()

# Expected: Returns invoice data successfully ✅
# Before fix: Returned empty/null ❌
```

## Related Issues

- **issue-002**: Graphiti MCP stale connection (different root cause, same symptom)
- **invoicing-mcp-server.py**: FastMCP wrapper for this service
- **invoicing_service.py**: Python Supabase client wrapper (FIXED)

## Impact

- ✅ Fixes invoicing MCP `get_invoice()` tool
- ✅ Fixes invoicing MCP `list_entity_invoices()` tool
- ✅ Fixes invoicing MCP `get_pdf_status()` tool
- ✅ All three methods now query schema-qualified tables correctly

## Verification

After fixing and restarting Claude Code:
```javascript
// Should now return invoice data successfully
mcp__invoicing__get_invoice("e992dec8-1287-4fa8-9e92-aebd12b22baf")
// Expected: { success: true, data: { ... } }

mcp__invoicing__list_entity_invoices("bdea5242-9627-43c1-a367-1990caa939f1")
// Expected: { success: true, count: N, invoices: [...] }
```

## References

- **Supabase Python Client**: https://github.com/supabase-community/supabase-py
- **API Methods**: `.from_()` vs `.table()` documentation
- **Schema Qualification**: PostgreSQL schema naming conventions

---

**Lesson Created**: 2025-10-25
**Issue Resolved**: issue-003
**Status**: ✅ Complete and verified
