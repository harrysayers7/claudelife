---
date: "2025-10-25 11:35"
issue-id: issue-003
category: mcp-server
severity: high
---

# Lesson: Python Supabase Client API Methods for Schema-Qualified Tables

## Problem

Invoicing MCP tools (`get_invoice()`, `list_entity_invoices()`) were returning "not found" errors and empty lists despite invoices existing in the Supabase database. Tests showed:
- ✅ Direct SQL queries found the data
- ❌ MCP tools couldn't find the same data
- ✅ Data existed in views located in non-public schemas

## Root Cause

The Python Supabase client's `.table()` API method **only works with the `public` schema**. When code tried to access views in the `invoicing` schema using `.table('invoicing.v_invoice_with_items')`, the API silently failed to find any results instead of throwing an error.

Additionally, chaining `.order()` and `.limit()` methods on filtered queries (`.eq()`) caused the Supabase Python ORM to return empty results, even though the underlying query was valid.

## Technical Details

### Issue #1: Wrong API Method for Non-Public Schemas

**What was wrong:**
```python
# ❌ WRONG - .table() only works with public schema
response = self.supabase.table('invoicing.v_invoice_with_items') \
    .select('*').eq('id', invoice_id).single().execute()
# Result: Empty/not found, no error thrown
```

**Why it failed:**
- `.table()` method is hardcoded for public schema in Supabase Python client
- Passing schema-qualified names doesn't raise an error, just returns no results
- Silently fails - very hard to debug

**What fixed it:**
```python
# ✅ CORRECT - .from_() method handles any schema
response = self.supabase.from_('invoicing.v_invoice_with_items') \
    .select('*').eq('id', invoice_id).execute()
# Result: Returns data from invoicing schema view
```

### Issue #2: Chained Method Query Failure

**What was wrong:**
```python
# ❌ BROKEN - Chaining .order().limit() breaks the query
response = self.supabase.from_('invoicing.v_invoice_with_items') \
    .select('*') \
    .eq('entity_id', entity_id) \
    .order('invoice_date', descending=True) \
    .limit(limit) \
    .execute()
# Result: Returns empty list even when data exists
```

**Why it failed:**
- Supabase Python client has a bug/limitation where chaining `.order()` and `.limit()` after `.eq()` breaks the query
- Works fine individually, fails when chained
- Difficult to diagnose because the query syntax is valid

**What fixed it:**
```python
# ✅ CORRECT - Fetch all results, sort in Python
response = self.supabase.from_('invoicing.v_invoice_with_items') \
    .select('*') \
    .eq('entity_id', entity_id) \
    .execute()

# Then sort and limit in Python
invoices = sorted(response.data, key=lambda x: x['invoice_date'], reverse=True)[:limit]
```

## Solution Applied

**File:** `src/invoicing/invoicing_service.py`

### Changed Methods:
1. **fetchInvoiceData()** - Changed `.table()` → `.from_()`
2. **fetchEntityInvoices()** - Changed `.table()` → `.from_()`, removed chaining
3. **getPdfStatus()** - Changed `.table()` → `.from_()`

### Python API Reference:
| Method | Use Case | Limitations |
|--------|----------|------------|
| `.table('name')` | Public schema tables only | Cannot access other schemas |
| `.from_('schema.view')` | Any schema, tables & views | Properly handles schema-qualified names |
| `.select().eq()` | Single filter | Works fine |
| `.select().eq().order().limit()` | Filtered + sorted + limited | ❌ Breaks in Python client |

## Prevention

### For Users:
- When querying non-public schema objects in Supabase with Python client, **always use `.from_()` instead of `.table()`**
- Never chain `.order().limit()` after filters - fetch all results and process in Python
- Test MCP tools after modifying schema queries

### For System:
- Add code review checklist for Supabase ORM usage:
  - [ ] Verify correct API method for schema (`.table()` = public only, `.from_()` = any schema)
  - [ ] Don't chain `.order().limit()` with `.eq()` filters
  - [ ] Test queries with non-public schema data
- Add unit tests for schema-qualified table access
- Document Python Supabase client limitations in project guide

## Related

- **Issue**: [[issue-003-invoicing-mcp-sync]]
- **Files**: `src/invoicing/invoicing_service.py`
- **Database**: `gshsshaodoyttdxippwx` (SAYERS DATA)
- **Similar patterns**: Schema access issues in Supabase
- **Test invoice**: `e992dec8-1287-4fa8-9e92-aebd12b22baf` (MOK HOUSE)

## Test Verification

✅ **After fix**:
```javascript
// Both now return correct data:
mcp__invoicing__get_invoice("e992dec8-1287-4fa8-9e92-aebd12b22baf")
// Returns: Full invoice object

mcp__invoicing__list_entity_invoices("bdea5242-9627-43c1-a367-1990caa939f1")
// Returns: Array of 10 invoices
```
