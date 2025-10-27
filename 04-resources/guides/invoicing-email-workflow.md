---
date: "2025-10-26"
---

# Invoicing Email Workflow Guide

## Overview

This guide documents the complete process for generating invoices from templates and sending them via email. **DO NOT deviate from this process** or you will break the template.

## Critical Rule

**The template file MUST use Handlebars syntax** (`{{variable}}`, `{{#each}}`, `{{#if}}`). Any script that modifies the template HTML structure or CSS will corrupt the design. Always render templates properly using the Handlebars library.

---

## Files Involved

### 1. Template File
- **Location**: `src/invoicing/templates/invoice.html`
- **Type**: HTML with Handlebars templating
- **Status**: Professionally designed by user with condensed spacing - DO NOT MODIFY the HTML structure or CSS
- **Variables**: Uses `{{invoice_number}}`, `{{client_name}}`, `{{invoice_date}}`, `{{project_name}}`, `{{fee_type}}`, etc.
- **Design Features**: 70px centered header, square brackets labels, single line item template, professional 2-column layout

### 2. Invoice Generation Script
- **Location**: `src/invoicing/generate-invoice.js`
- **Purpose**: Loads template, renders Handlebars, converts to PDF
- **Key**: Uses Handlebars library to properly render before PDF conversion
- **Dependencies**: `handlebars` (already in package.json)

### 3. Invoice Data
- Currently hardcoded in `generate-invoice.js`
- In future: Should load from Supabase invoicing MCP

---

## Process Flow

### Step 1: Prepare Data
```javascript
const invoiceData = {
  invoice_number: "TEST-001",
  invoice_date: "25-10-2025",
  po_number: "0896",
  client_name: "Electric Sheep Music Pty Ltd",
  client_address: "Unit 5, 123 Business Park, Sydney NSW 2000",
  project_name: "Music Composition",
  fee_type: "Track Setup & Production",
  quantity: 1,
  unit_price: "1000.00",
  total: "1000.00",
  subtotal: "1000.00",
  gst: "100.00",
  grand_total: "1100.00",
};
```

### Step 2: Load & Compile Template
```javascript
const Handlebars = require("handlebars");
const templateSource = fs.readFileSync("src/invoicing/templates/invoice.html", "utf8");
const template = Handlebars.compile(templateSource);
```

### Step 3: Render to HTML
```javascript
// This is the critical step - Handlebars processes {{}} syntax
const html = template(invoiceData);
fs.writeFileSync("/tmp/invoice.html", html);
```

### Step 4: Convert HTML to PDF with Puppeteer
```javascript
const puppeteer = require("puppeteer");

const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.goto(`file:///tmp/invoice.html`, { waitUntil: "networkidle0" });
await page.pdf({
  path: "/tmp/invoice.pdf",
  format: "A4",
  margin: { top: 0, bottom: 0, left: 0, right: 0 },
  printBackground: true,
});
await browser.close();
```

**Why Puppeteer?** Uses Chromium browser engine for accurate CSS rendering. wkhtmltopdf has limited CSS3 support and causes text repositioning issues.

### Step 5: Send via Gmail MCP
```bash
# Use Claude Code's Gmail MCP to send the PDF
mcp__gmail__send_email({
  to: ["harry@sayers1.com"],
  subject: "Invoice TEST-001 - MOK HOUSE",
  body: "Hi,\n\nPlease find attached your invoice...",
  attachments: ["/tmp/invoice-TEST-001.pdf"]
});
```

Or in Claude Code terminal:
```bash
# After generate-invoice.js creates the PDF, send via Gmail MCP
```

---

## How to Run

### 1. Generate Invoice PDF
```bash
# Renders template with Handlebars, generates PDF with Puppeteer
node src/invoicing/generate-invoice.js

# Output:
# ✓ HTML rendered: /tmp/invoice-TEST-001.html
# ✓ PDF generated: /tmp/invoice-TEST-001.pdf (224.69 KB)
```

### 2. Send via Gmail MCP
In Claude Code, use the Gmail MCP tool:
```javascript
mcp__gmail__send_email({
  to: ["harry@sayers1.com"],
  subject: "Invoice TEST-001 - MOK HOUSE",
  body: "Hi,\n\nPlease find attached your invoice...",
  attachments: ["/tmp/invoice-TEST-001.pdf"]
});
```

The complete workflow: **Data → Handlebars Render → HTML → Puppeteer PDF → Gmail MCP Send**

---

## Handlebars Helpers

The script registers a custom helper for currency formatting:

```javascript
Handlebars.registerHelper("format_currency", function (amount) {
  return parseFloat(amount).toFixed(2);
});
```

This allows the template to use: `${{format_currency subtotal_amount}}`

---

## Template Variable Reference

| Variable | Type | Example | Used For |
|----------|------|---------|----------|
| `invoice_number` | String | "TEST-001" | Invoice header (MH-{{invoice_number}}) |
| `invoice_date` | String | "25-10-2025" | Invoice date field |
| `po_number` | String | "0896" | Purchase order field |
| `client_name` | String | "Electric Sheep Music Pty Ltd" | Bill To name |
| `client_address` | String | "Unit 5, 123 Business Park..." | Bill To address |
| `project_name` | String | "Music Composition" | Project description |
| `fee_type` | String | "Track Setup & Production" | Fee/service description |
| `quantity` | Number | 1 | Item quantity |
| `unit_price` | String | "1000.00" | Price per unit |
| `total` | String | "1000.00" | Line item total |
| `subtotal` | String | "1000.00" | Subtotal before GST |
| `gst` | String | "100.00" | GST amount (10%) |
| `grand_total` | String | "1100.00" | Total with GST |

---

## Common Issues & Solutions

### Issue: PDF is blank or 0 pages
**Cause**: Template wasn't properly rendered with Handlebars
**Solution**: Check that `template = Handlebars.compile(templateSource)` is being called before rendering

### Issue: Variables showing as `{{invoice_number}}` in PDF
**Cause**: Handlebars rendering step was skipped
**Solution**: Ensure `const html = template(invoiceData)` is called, not direct string replacement

### Issue: Template layout looks corrupted
**Cause**: HTML structure or CSS was modified
**Solution**: Restore from screenshot or original design - do NOT make CSS changes

### Issue: "handlebars module not found"
**Cause**: Module not installed
**Solution**: Check package.json has `"handlebars": "^4.7.8"` and run `npm install`

---

## Future Improvements

### Load data from Supabase
Instead of hardcoding `invoiceData`, fetch from Supabase invoicing MCP:
```javascript
const invoice = await supabase.from('invoices').select('*').eq('id', invoiceId);
const invoiceData = formatForTemplate(invoice);
```

### Parameterize the script
Accept invoice ID as command-line argument:
```bash
node src/invoicing/generate-invoice.js MH-001
```

### Template selection
Allow different templates based on entity type:
```javascript
const template = invoiceData.entity === 'mokhouse'
  ? 'invoice-mokhouse.html'
  : 'invoice-mokai.html';
```

---

## What NOT to Do

❌ **DO NOT** modify the template HTML structure
❌ **DO NOT** make CSS Grid/Flexbox changes without testing in browser first
❌ **DO NOT** use string replacement (`.replace()`) instead of Handlebars compilation
❌ **DO NOT** change variable names without updating template placeholders
❌ **DO NOT** overwrite the template file without backing it up first

---

## Template Design Notes

The current template (`invoice.html`) features:
- **70px centered header** with [MOK HOUSE] and ABN
- **Square brackets aesthetic labels** ([BILL TO], [DESCRIPTION], [QTY], etc.)
- **Professional single line item template** with grid layout
- **Right-aligned totals** section with grand total (28px font)
- **Payment details and contact info** in 2-column footer
- **Condensed spacing** optimized for single-page PDF (65px padding, 45px header margin)
- **Puppeteer-compatible CSS** with proper Grid layouts and print settings

This design was professionally crafted and carefully condensed. **Preserve it - DO NOT modify CSS or spacing without explicit user approval.**

---

## Quick Reference

```bash
# 1. Generate PDF with test data (Puppeteer rendering)
node src/invoicing/generate-invoice.js

# 2. Check generated PDF
ls -lh /tmp/invoice-TEST-001.pdf

# 3. Send via Gmail MCP in Claude Code
mcp__gmail__send_email({
  to: ["harry@sayers1.com"],
  subject: "Invoice TEST-001 - MOK HOUSE",
  body: "Hi,\n\nPlease find attached your invoice...",
  attachments: ["/tmp/invoice-TEST-001.pdf"]
});
```

## Complete Workflow

**Data → Handlebars Render → HTML → Puppeteer PDF → Gmail MCP**

✅ **DO**: Use Puppeteer for accurate CSS rendering
✅ **DO**: Use Gmail MCP for sending with attachments
✅ **DO**: Preserve the template design exactly
✅ **DO**: Update test data in generate-invoice.js for different invoices

❌ **DON'T**: Modify template HTML or CSS without approval
❌ **DON'T**: Use wkhtmltopdf (causes text repositioning)
❌ **DON'T**: Use string replacement instead of Handlebars
❌ **DON'T**: Change variable names without updating template
