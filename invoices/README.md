# Invoice Parsing System

## How to Add Past Invoices

Your PDF invoice parsing system is now ready! Here's how to use it:

### 1. Single Invoice Upload

Upload a PDF invoice via HTTP POST:

```bash
curl -X POST "http://localhost:8002/financial/parse-invoice" \
  -F "file=@your-invoice.pdf" \
  -F "entity_id=1" \
  -F "account_id=1" \
  -F "auto_create_transaction=true"
```

This will:
- Extract text from the PDF
- Use OpenAI GPT-4o-mini to parse vendor, amount, date, etc.
- Automatically create a financial transaction in your database

### 2. Batch Processing

Drop multiple PDFs in the `invoices/` directory and process them all:

```bash
curl -X POST "http://localhost:8002/financial/parse-invoices-directory" \
  -H "Content-Type: application/json" \
  -d '{
    "entity_id": 1,
    "account_id": 1,
    "auto_create_transactions": true
  }'
```

### 3. Test the Parser

Check if everything is working:

```bash
curl -X GET "http://localhost:8002/financial/test-invoice-parser"
```

## What Gets Extracted

The AI extracts these fields from your invoices:
- Vendor name
- Invoice number
- Invoice date
- Due date
- Total amount
- Tax amount
- Subtotal
- Description of goods/services
- Line items with quantities and prices
- Vendor ABN (if available)
- Payment terms

## Database Integration

Parsed invoices are automatically:
- Stored as transactions (negative amounts for expenses)
- Tagged with vendor information
- Linked to the correct entity and account
- Timestamped with parsing metadata

Just drop your PDF invoices in this folder and run the batch processing endpoint!
