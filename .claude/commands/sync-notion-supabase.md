# Sync Notion Supabase

This command performs **one-way synchronization** from your Supabase financial database to Notion databases under DATABASE MASTER, using validated direct MCP tools for reliable data transfer.

## Usage

```bash
/sync-notion-supabase [to-notion] [tables]
```

**Arguments:**
- `direction` (optional): `to-notion` (default and only supported direction)
- `tables` (optional): Comma-separated list of tables or `all` (default: all relevant tables)

## Interactive Process

When you run this command, I will:

1. **Verify MCP Environment Setup**
   - Confirm Supabase MCP server is accessible (project: gshsshaodoyttdxippwx)
   - Test Notion MCP tools connectivity and permissions
   - Validate all target Notion database IDs are accessible

2. **Confirm Sync Parameters**
   - Display which tables will be synced (entities, contacts, transactions, invoices, accounts)
   - Show estimated record counts from Supabase for each table
   - Confirm one-way sync direction (Supabase → Notion only)

3. **Execute Sync with Live Progress**
   - Use direct MCP tools for reliable data transfer
   - Process each table with validated property mapping
   - Handle errors gracefully with 0.5s rate limiting between records

4. **Provide Comprehensive Report**
   - Summary of records successfully created in Notion
   - List of any validation/API errors encountered
   - Performance metrics and total sync duration

## Input Requirements

Before running this command, ensure:
1. **MCP Servers Configured**: Supabase and Notion MCP servers active in Claude Code
2. **Database Access**: Supabase project `gshsshaodoyttdxippwx` accessible via MCP
3. **Notion Setup**: DATABASE MASTER page with all 5 target databases created and accessible
4. **Permissions**: Claude Code has access to both `mcp__supabase__*` and `mcp__notion__*` tools

## Process

I'll execute the sync using validated direct MCP approach:

1. **Verify MCP Connectivity**
   - Test Supabase MCP: `mcp__supabase__execute_sql` with simple query
   - Test Notion MCP: `mcp__notion__API-get-self` to verify authentication
   - Validate all 5 target database IDs are accessible

2. **Analyze Current Data State**
   - Query each Supabase table: `SELECT * FROM [table] ORDER BY created_at DESC`
   - Count records per table for sync planning
   - Estimate total sync duration based on record counts

3. **Execute One-Way Sync (Supabase → Notion)**
   - **Entities**: business_name → "Entity Name", entity_type → "Type" select
   - **Contacts**: Proper null handling for phone/email fields
   - **Transactions**: Amount as number, proper date formatting
   - **Invoices**: Status/Type as select options, FK relationships
   - **Accounts**: Account Type select, Balance as number, Is Active checkbox

4. **Apply Validated Property Mappings**
   - Use exact property types discovered during validation
   - Handle empty values correctly (null vs empty string)
   - Apply 0.5s rate limiting between API calls

5. **Generate Detailed Report**
   - Success/failure count per table
   - Any validation errors with specific field details
   - Total sync duration and performance metrics

## Technical Implementation Guide

### Relevant Tables for Sync

```javascript
const SYNC_TABLES = {
  // Human-readable business data only
  'entities': '2784a17b-b7f0-8188-a62f-ffb7975db5e5',      // Business Entities
  'contacts': '2784a17b-b7f0-8124-a67f-c51dd6c75a93',      // Contacts
  'transactions': '2784a17b-b7f0-81a5-94c9-d5aba1625d49',  // Transactions
  'invoices': '2784a17b-b7f0-8166-803d-e6cc7330d8c1',      // Invoices
  'accounts': '2784a17b-b7f0-8189-ad95-d6c1fd78db1c'       // Accounts

  // Excluded AI/ML tables: ml_models, ai_predictions, ai_insights,
  // anomaly_detections, categorization_rules, cash_flow_forecasts
};
```

### Validated Property Mappings

```python
# Exact mappings validated during testing - WORKING IMPLEMENTATION
def uuid_to_number(uuid_str):
    """Convert UUID string to consistent integer for Notion number fields"""
    if not uuid_str:
        return 0
    return abs(int(hashlib.md5(str(uuid_str).encode()).hexdigest()[:8], 16))

PROPERTY_MAPPINGS = {
  entities: {
    "ID": {"title": [{"text": {"content": str(record.get('id', ''))}}]},
    "Entity Name": {"rich_text": [{"text": {"content": record.get('business_name', 'Unknown')}}]},
    "ABN": {"rich_text": [{"text": {"content": str(record.get('abn', ''))}}]},
    "Type": {"select": {"name": "Sole Trader" if record.get('entity_type') == 'individual' else "Company"}},
    "Created": {"date": {"start": record.get('created_at', datetime.now().isoformat())[:10]}}
  },
  contacts: {
    "ID": {"title": [{"text": {"content": str(record.get('id', ''))}}]},
    "Name": {"rich_text": [{"text": {"content": record.get('name', 'Unknown')}}]},
    "Email": {"email": record.get('email') or None},  # None for null validation
    "Phone": {"phone_number": record.get('phone') or None},  # None for null validation
    "Company": {"rich_text": [{"text": {"content": record.get('company', '')}}]},
    "Entity ID": {"number": uuid_to_number(record.get('entity_id', ''))}  # UUID conversion
  },
  transactions: {
    "ID": {"title": [{"text": {"content": str(record.get('id', ''))}}]},
    "Description": {"rich_text": [{"text": {"content": record.get('description', 'Unknown Transaction')}}]},
    "Amount": {"number": float(record.get('amount', 0))},
    "Transaction Date": {"date": {"start": record.get('transaction_date', datetime.now().date().isoformat())[:10]}},
    "Account ID": {"number": uuid_to_number(record.get('account_id', ''))},  # UUID conversion
    "Entity ID": {"number": uuid_to_number(record.get('entity_id', ''))},  # UUID conversion
    "Reference Number": {"rich_text": [{"text": {"content": record.get('reference_number', '')}}]},
    "Notes": {"rich_text": [{"text": {"content": record.get('notes', '')}}]},
    "Vendor Name": {"rich_text": [{"text": {"content": record.get('vendor_name', '')}}]}
  },
  invoices: {
    "ID": {"title": [{"text": {"content": str(record.get('id', ''))}}]},
    "Invoice Number": {"rich_text": [{"text": {"content": record.get('invoice_number', 'Unknown')}}]},
    "Total Amount": {"number": float(record.get('total_amount', 0))},
    # CRITICAL: Handle None dates to prevent NoneType errors
    "Due Date": {"date": {"start": record.get('due_date')[:10] if record.get('due_date') else datetime.now().date().isoformat()}},
    "Invoice Date": {"date": {"start": record.get('invoice_date')[:10] if record.get('invoice_date') else datetime.now().date().isoformat()}},
    "Status": {"select": {"name": record.get('status', 'draft')}},
    "Entity ID": {"number": uuid_to_number(record.get('entity_id', ''))},  # UUID conversion
    "Contact ID": {"number": uuid_to_number(record.get('contact_id', ''))},  # UUID conversion
    "Type": {"select": {"name": record.get('type', 'receivable')}}
  },
  accounts: {
    "ID": {"title": [{"text": {"content": str(record.get('id', ''))}}]},
    "Account Name": {"rich_text": [{"text": {"content": record.get('account_name', 'Unknown Account')}}]},
    "Account Type": {"select": {"name": record.get('account_type', 'asset')}},
    "Balance": {"number": float(record.get('current_balance', 0))},
    "Entity ID": {"number": uuid_to_number(record.get('entity_id', ''))},  # UUID conversion
    "Account Code": {"rich_text": [{"text": {"content": record.get('account_code', '')}}]},
    "Description": {"rich_text": [{"text": {"content": record.get('description', '')}}]},
    "Is Active": {"checkbox": bool(record.get('is_active', True))}
  }
};
```

### Error Handling with MCP Tools

```javascript
// Direct MCP tool approach with validation
const createNotionRecord = async (databaseId, properties) => {
  try {
    const result = await mcp__notion__API_post_page({
      parent: { database_id: databaseId },
      properties: properties
    });

    if (result.object === 'page') {
      return { success: true, pageId: result.id };
    } else {
      return { success: false, error: 'Invalid response format' };
    }
  } catch (error) {
    // Handle specific validation errors
    if (error.message?.includes('body failed validation')) {
      return { success: false, error: 'Property validation failed', details: error.message };
    }
    return { success: false, error: error.message };
  }
};

// Rate limiting with simple delays
const RATE_LIMIT_DELAY = 500; // 0.5s between requests (validated)
```

## Output Format

I'll provide:

1. **Pre-Sync Analysis**
   ```
   📊 Sync Analysis
   ├── Supabase Records: entities(3), contacts(2), transactions(1), invoices(6), accounts(52)
   ├── Notion Records: entities(1), contacts(1), transactions(1), invoices(0), accounts(0)
   ├── Estimated Operations: 63 creates, 3 updates, 0 conflicts
   └── Estimated Duration: ~2 minutes
   ```

2. **Live Progress Updates**
   ```
   🔄 Syncing entities... [████████████████████] 100% (3/3) ✓
   🔄 Syncing contacts... [████████████████████] 100% (2/2) ✓
   🔄 Syncing transactions... [██████████████████] 90% (9/10) ⏳
   ```

3. **Comprehensive Final Report**
   ```
   ✅ Sync Complete - 2m 34s

   📈 Summary:
   ├── Total Records Processed: 63
   ├── Successfully Synced: 61
   ├── Conflicts Resolved: 2 (Supabase priority)
   ├── Errors: 0
   └── API Calls Made: 127 (within rate limits)

   📋 Details by Table:
   ├── entities: 3 created in Notion, 0 updated
   ├── contacts: 2 created in Notion, 0 updated
   ├── transactions: 1 created in Notion, 0 updated
   ├── invoices: 6 created in Notion, 0 updated
   └── accounts: 49 created in Notion, 3 updated

   💡 Recommendations:
   └── All syncs successful - databases are now in sync
   ```

## Examples

### Example 1: Full Bidirectional Sync

**Command:** `/sync-notion-supabase`

**Process:**
1. I verify your environment variables are configured
2. Start the FastAPI server and test connections
3. Analyze current data: Supabase has 64 total records, Notion has 3
4. Execute bidirectional sync with live progress bars
5. Report: 61 new records created in Notion, 0 conflicts, 2m 15s duration

### Example 2: Notion-Only Update Sync

**Command:** `/sync-notion-supabase to-supabase contacts,invoices`

**Process:**
1. I focus only on contacts and invoices tables
2. Check for changes made in Notion since last sync
3. Find 2 updated contact records in Notion
4. Sync changes back to Supabase with conflict resolution
5. Report: 2 records updated in Supabase, 0 conflicts, 15s duration

### Example 3: Recovery from API Errors

**Command:** `/sync-notion-supabase to-notion`

**Process:**
1. I start syncing but encounter Notion API rate limits
2. Implement exponential backoff (2s, 4s, 8s delays)
3. Continue processing with retry logic
4. One record fails due to validation error - skip and continue
5. Report: 62/63 successful, 1 validation error with details for manual fix

## Evaluation Criteria

A successful sync should:

1. **Data Integrity**: All successfully synced records match between systems
2. **Conflict Resolution**: Supabase takes priority in timestamp conflicts
3. **Error Resilience**: Continue processing despite individual record failures
4. **Performance**: Complete within reasonable time (under 5 minutes for <1000 records)
5. **Comprehensive Reporting**: Clear success/failure status for each table and record
6. **Rate Limit Compliance**: Respect API limits with proper backoff strategies
7. **Duplicate Prevention**: Use unique IDs to avoid creating duplicate records

## Related Resources

- FastAPI Server: `/Users/harrysayers/Developer/claudelife/.mcp/financial_api_server.py`
- Database Schema: `/Users/harrysayers/Developer/claudelife/context/finance/database/supabase-schema.md`
- MCP Configuration: `/Users/harrysayers/Developer/claudelife/.mcp.json`
- Notion Database IDs: Stored in DATABASE_MAPPINGS within FastAPI server

## Troubleshooting

**Common Issues:**
- **Auth Errors**: Verify SUPABASE_ACCESS_TOKEN and NOTION_TOKEN in environment
- **Missing Dependencies**: Run `uv pip install fastapi uvicorn python-dotenv supabase notion-client`
- **Rate Limits**: Command automatically handles with exponential backoff
- **Validation Errors**: Check Notion database schema matches expected field types
- **Connection Timeout**: Verify network connectivity and API service status

**Recovery Steps:**
1. Check environment variables: `echo $SUPABASE_ACCESS_TOKEN $NOTION_TOKEN`
2. Test individual API connections: Use MCP tools to verify access
3. Restart FastAPI server if it becomes unresponsive
4. Re-run sync command - it will skip already-synced records
