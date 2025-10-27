---
date: "2025-10-25"
---

# Invoice Generation System

Complete invoice PDF generation and management system with Playwright-based rendering and Supabase Storage integration.

## 📁 File Structure

```
src/invoicing/
├── pdf-generator.ts          # Core PDF generation using Playwright
├── supabase-storage.ts       # Supabase Storage bucket management
├── invoicing-service.ts      # Main service orchestrating all operations
├── test-pdf-generation.ts    # Test script for validation
├── templates/
│   └── invoice.html          # Australian-compliant invoice template
└── README.md                 # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
npm install playwright handlebars @supabase/supabase-js
```

All dependencies are already in `package.json` for this project.

### 2. Set Environment Variables

```bash
export SUPABASE_URL="https://gshsshaodoyttdxippwx.supabase.co"
export SUPABASE_KEY="your-service-role-key-here"
```

### 3. Generate a Single Invoice PDF

```typescript
import { InvoicingService } from './src/invoicing/invoicing-service';

const service = new InvoicingService(supabaseUrl, supabaseKey);
await service.initialize();

// Generate and store PDF (includes database metadata insertion)
const success = await service.generateAndStorePdf('invoice-uuid-here');

await service.cleanup();
```

### 4. Test PDF Generation

```bash
# Test with specific invoice
SUPABASE_URL=... SUPABASE_KEY=... INVOICE_ID=<uuid> npm run test:invoices

# Test with entity's first invoice
SUPABASE_URL=... SUPABASE_KEY=... ENTITY_ID=<uuid> npm run test:invoices
```

## 📋 Features

### PDF Generation
- ✅ **Playwright-based rendering** - Fast, lightweight, no external dependencies
- ✅ **Handlebars templates** - Dynamic invoice generation with clean separation of concerns
- ✅ **Australian compliance** - ABN formatting, GST labeling, proper currency format
- ✅ **Responsive layout** - A4 page format, professional styling
- ✅ **Line item aggregation** - JSON items properly rendered in table format
- ✅ **Batch processing** - Generate multiple PDFs efficiently

### Storage Integration
- ✅ **Supabase Storage** - Secure cloud storage for PDFs
- ✅ **Auto-bucket creation** - Bucket created automatically on first use
- ✅ **Public URLs** - Generated URLs for easy access
- ✅ **Signed URLs** - Temporary access URLs if needed
- ✅ **Path organization** - PDFs stored as `/entity-id/year/invoice-number.pdf`

### Data Integration
- ✅ **View-based queries** - Uses `invoicing.v_invoice_with_items` view
- ✅ **Complete data** - All invoice details including PO numbers, line items, taxes
- ✅ **Bank details** - JSONB bank account information stored and displayed
- ✅ **Custom footer** - Per-entity customizable footer text

### Database Integration
- ✅ **Metadata insertion** - PDF records automatically inserted into `invoicing.invoice_pdfs`
- ✅ **Audit trail** - File names, storage paths, sizes tracked
- ✅ **Transaction safety** - Generation and metadata insertion atomic

## 📊 Invoice Data Structure

Data is fetched from `invoicing.v_invoice_with_items` view:

```typescript
interface InvoiceData {
  id: string;
  invoice_number: string;                    // e.g., "MH-001"
  purchase_order_number?: string;            // e.g., "0896"
  invoice_date: string;                      // ISO 8601
  due_date: string;
  subtotal_amount: number;
  gst_amount: number;
  total_amount: number;
  client_name: string;                       // Electric Sheep Music
  client_abn?: string;
  entity_name: string;                       // MOK HOUSE PTY LTD
  entity_abn: string;
  trading_name?: string;
  bank_details?: {
    account_name?: string;
    bsb?: string;
    account_number?: string;
    swift_code?: string;
  };
  footer_text?: string;
  items: Array<{
    description: string;
    quantity: number;
    unit_price: number;
    tax_rate: number;
    line_total: number;
    line_tax: number;
  }>;
}
```

## 🎨 Template Features

### Australian Compliance
- **ABN Display** - Entity and client ABN numbers prominently displayed
- **GST Labeling** - GST tax properly labeled and calculated (10%)
- **Currency Format** - Australian dollar format ($XXX.XX)
- **Date Format** - DD/MM/YYYY format
- **Trading Name** - Support for trading names (e.g., Mok Music)

### Professional Design
- **Header Section** - Company logo/name with invoice details
- **Client Information** - Clear separation of invoice from/to
- **Line Items Table** - Quantity, unit price, tax rate, totals
- **Summary** - Subtotal, GST, total amount
- **Bank Details** - Editable JSONB data displayed as key-value pairs
- **Footer** - Payment terms and customizable notes

### Dynamic Content
- All template variables automatically populated from database
- Conditional rendering (e.g., trading name only if provided)
- Currency formatting via Handlebars helpers
- Date formatting (ISO to DD/MM/YYYY)

## 🔧 API Reference

### InvoicingService

Main orchestration class handling all operations.

```typescript
// Initialize service
const service = new InvoicingService(supabaseUrl, supabaseKey, templatePath?);
await service.initialize();

// Single invoice
const success = await service.generateAndStorePdf(invoiceId);

// Batch processing
const results = await service.generateBatch(invoiceIds);

// Direct data access
const invoiceData = await service.fetchInvoiceData(invoiceId);
const allInvoices = await service.fetchEntityInvoices(entityId);

// Cleanup
await service.cleanup();
```

### InvoicePdfGenerator

Low-level PDF generation.

```typescript
const generator = new InvoicePdfGenerator(templatePath?);
await generator.initialize();

// Generate PDF
const pdfPath = await generator.generatePdf(invoiceData, outputPath);

// Batch generation
const results = await generator.generatePdfBatch(invoices, outputDir);

await generator.close();
```

### InvoicePdfStorage

Supabase Storage management.

```typescript
const storage = new InvoicePdfStorage(supabaseUrl, supabaseKey);

// Ensure bucket exists
await storage.ensureBucket();

// Upload PDF
const publicUrl = await storage.uploadPdf(localPath, invoiceNumber, entityId);

// Get signed URL (temporary access)
const signedUrl = await storage.getSignedUrl(invoiceNumber, entityId, expiresIn);

// List PDFs
const pdfs = await storage.listEntityPdfs(entityId);

// Download PDF
await storage.downloadPdf(invoiceNumber, entityId, outputPath);

// Delete PDF
await storage.deletePdf(invoiceNumber, entityId);
```

## 📝 Invoice Number Format

Generated format: `PREFIX-NNN` (no year component)

| Entity | Prefix | Example |
|--------|--------|---------|
| MOK HOUSE PTY LTD | MH | MH-001, MH-002, MH-003 |
| MOKAI PTY LTD | MK | MK-001, MK-002, MK-003 |
| Other Entities | INV | INV-001, INV-002 |

**Note**: Auto-increments per entity. Resets are manual via `invoicing.invoice_settings`.

## 🗂️ Storage Structure

PDFs are stored in Supabase Storage with this path structure:

```
invoice-pdfs/
├── <entity-id>/
│   ├── 2024/
│   │   ├── MH-001.pdf
│   │   ├── MH-002.pdf
│   │   └── MH-003.pdf
│   ├── 2025/
│   │   ├── MH-004.pdf
│   │   └── MH-005.pdf
│   └── ...
└── ...
```

## 📊 Database Integration

### `invoicing.invoice_pdfs` Table

Records created automatically on successful generation:

```sql
INSERT INTO invoicing.invoice_pdfs (
  invoice_id,
  pdf_url,           -- Public Supabase URL
  file_name,         -- "MH-001.pdf"
  storage_path,      -- "entity-id/2025/MH-001.pdf"
  pdf_size_bytes,    -- File size in bytes
  generated_at       -- Timestamp
) VALUES (...)
```

## 🧪 Testing

### Test Script

```bash
# Test with specific invoice
SUPABASE_URL=... SUPABASE_KEY=... INVOICE_ID=<uuid> npm run test:invoices

# Test with entity (fetches first invoice)
SUPABASE_URL=... SUPABASE_KEY=... ENTITY_ID=<uuid> npm run test:invoices
```

### Manual Testing

```typescript
// 1. Generate PDF
const pdfPath = await generator.generatePdf(invoiceData, '/tmp/test-invoice');
// Expected: PDF file created at /tmp/test-invoice.pdf

// 2. Upload to Supabase
const publicUrl = await storage.uploadPdf(pdfPath, 'MH-001', entityId);
// Expected: URL like https://gshsshaodoyttdxippwx.supabase.co/storage/v1/object/public/invoice-pdfs/...

// 3. Verify in database
const pdfs = await supabase
  .from('invoicing.invoice_pdfs')
  .select('*')
  .eq('invoice_id', invoiceId);
// Expected: Record with pdf_url, file_name, pdf_size_bytes

// 4. Download and verify
await storage.downloadPdf('MH-001', entityId, '/tmp/verify-invoice.pdf');
// Expected: Downloaded PDF matches original
```

## 🔄 Workflow

1. **Query** - Fetch invoice data from `invoicing.v_invoice_with_items` view
2. **Render** - Populate Handlebars template with invoice data
3. **Generate** - Use Playwright to render HTML to PDF
4. **Upload** - Upload PDF to Supabase Storage with organized path
5. **Record** - Insert metadata into `invoicing.invoice_pdfs` table
6. **Return** - Public URL available for download/email

## ⚙️ Configuration

### Environment Variables

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key-here
```

### Template Path

Custom template location:
```typescript
const service = new InvoicingService(
  supabaseUrl,
  supabaseKey,
  '/custom/path/to/invoice.html'
);
```

### Storage Configuration

Auto-configured but editable:
```typescript
// In supabase-storage.ts
private bucketName = 'invoice-pdfs';
private fileSizeLimit = 52428800; // 50MB
```

## 📦 Dependencies

- **playwright** - Headless browser for PDF rendering
- **@supabase/supabase-js** - Supabase client for database and storage
- **handlebars** - Template engine for invoice HTML generation

## 🐛 Troubleshooting

### "Browser not found" Error
- Playwright chromium not installed
- **Fix**: `npx playwright install chromium`

### "Bucket does not exist" Error
- Bucket not created in Supabase
- **Fix**: Service auto-creates on first run, or manually:
  ```bash
  # Use Supabase dashboard or API
  ```

### PDF Upload Fails
- Authentication issue with Supabase
- **Fix**: Verify SUPABASE_KEY has Storage write permissions

### Template Variables Not Rendering
- Handlebars helper not registered
- **Fix**: Check `registerHelpers()` in pdf-generator.ts

### PDF Quality Issues
- Playwright settings need adjustment
- **Fix**: Modify PDF rendering options in `generatePdf()` method

## 📚 Related Files

- [Invoicing Schema](../../../context/finance/database/migrate-invoicing-schema.sql) - Database schema
- [Integration Guide](../../../context/finance/database/invoicing-integration-guide.md) - Complete workflow
- [Implementation Status](../../../context/finance/database/invoicing-implementation-status.md) - Current state

## 🔐 Security Notes

- All PDFs stored in private Supabase bucket (not publicly listed)
- Public URLs are standard Supabase format (can be made private if needed)
- Signed URLs available for temporary access control
- No sensitive data in file paths (entity-id only, not secrets)

## 🚀 Next Steps

1. **Email Integration** - Send PDFs via SMTP
2. **Payment Tracking** - Link PDF generation to payment notifications
3. **API Endpoints** - REST/GraphQL endpoints for PDF generation
4. **MCP Server** - Expose as Claude Code tool for automation
5. **Scheduled Jobs** - Auto-generate PDFs for sent invoices
