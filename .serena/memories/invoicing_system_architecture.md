# Invoicing System Architecture

## Updated October 26, 2025

### Template System
- **Active Template**: `src/invoicing/templates/invoice.html`
- **Type**: Handlebars-based HTML template with professional design
- **Design**: 70px centered header with [MOK HOUSE], square bracket labels, single line item layout
- **Spacing**: Condensed for single-page PDF (65px padding, 45px header margin)
- **Status**: Professionally designed, DO NOT modify without explicit approval

### Invoice Generation Workflow
```
Data → Handlebars Compile → HTML Render → Puppeteer PDF → Gmail MCP Send
```

### Key Files
- **Template**: `src/invoicing/templates/invoice.html`
- **Generator Script**: `src/invoicing/generate-invoice.js`
- **Configuration**: Invoice data hardcoded in generate-invoice.js (future: load from Supabase MCP)

### Template Variables (Current Schema)
- `invoice_number`: String (e.g., "TEST-001")
- `invoice_date`: String (e.g., "25-10-2025")
- `po_number`: String (e.g., "0896")
- `client_name`: String
- `client_address`: String
- `project_name`: String
- `fee_type`: String
- `quantity`: Number
- `unit_price`: String (formatted as "1000.00")
- `total`: String (line item total)
- `subtotal`: String
- `gst`: String
- `grand_total`: String

### PDF Generation
- **Tool**: Puppeteer (Chromium browser engine)
- **Format**: A4, zero margins, print background enabled
- **Why Puppeteer**: Accurate CSS3 rendering (Grid, Flexbox) - wkhtmltopdf causes text repositioning
- **Output**: `/tmp/invoice-{invoice_number}.pdf`

### Email Sending
- **Tool**: Gmail MCP (`mcp__gmail__send_email`)
- **Attachment Support**: Yes (PDF sent as attachment)
- **Recipient**: Configurable (default: harry@sayers1.com)

### Important Rules
✅ **DO**:
- Use Handlebars for template rendering
- Use Puppeteer for PDF generation
- Use Gmail MCP for sending with attachments
- Preserve template design exactly

❌ **DON'T**:
- Modify template HTML/CSS without approval
- Use wkhtmltopdf (causes text repositioning)
- Use string replacement instead of Handlebars
- Change variable names without updating template

### Documentation
- Guide: `04-resources/guides/invoicing-email-workflow.md`
- Last updated: October 26, 2025 (complete workflow refresh)
