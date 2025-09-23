# Add Invoice to Database

Parse and add invoice(s) to Supabase database. Handles both single PDFs and directories.

**Usage:**
- `/add-invoice /path/to/invoice.pdf` - Single invoice
- `/add-invoice /path/to/invoices/` - Directory of PDFs
- `/add-invoice` - Use default invoice directory from Dropbox

## Steps:

1. **Determine source path:**
   - If $ARGUMENTS provided: Use exact path specified
   - If no arguments: Use `/Users/harrysayers/Dropbox/03_M4M/0302_M4M_Docs/0302.1_M4M_Invoices/`

2. **Parse invoice(s):**
   - Use invoice_parser.py to extract structured data
   - Handle both single files and directories
   - Validate all extracted fields

3. **Database schema investigation:**
   - Check Supabase table structures (invoices, transactions, contacts, entities)
   - Verify constraint values (status, contact_type, invoice_type)
   - Identify required foreign keys

4. **Create dependent records:**
   - Check if contact exists for vendor/supplier
   - If not, create new contact with proper type ('supplier' for payables)
   - Get entity_id for linking

5. **Insert invoice data:**
   - Insert transaction record (negative amount for expenses)
   - Insert invoice record with proper relationships
   - Use appropriate status values ('draft', 'posted', 'reconciled', 'voided')
   - Set correct invoice_type ('payable' for bills we owe)

6. **Verify completion:**
   - Query database to confirm all records were inserted
   - Show summary of added invoices with key details
   - Report any failures with specific error details

## Error handling:
- Database constraint violations: Check schema and use valid values
- Missing vendor info: Create minimal contact record with available data
- Parse failures: Report which files couldn't be processed
- Duplicate invoices: Check for existing invoice numbers before inserting
