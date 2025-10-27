#!/usr/bin/env node

/**
 * Test script: Render invoice-test.html template with real invoice data and send via email
 *
 * Process:
 * 1. Fetch real invoice data from Supabase
 * 2. Load invoice-test.html template
 * 3. Replace placeholders with real data
 * 4. Convert HTML to PDF using wkhtmltopdf
 * 5. Send PDF via Gmail MCP
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const invoiceData = {
  id: "ef511a20-6d45-46b1-bdcf-3f3ae4cd0f09",
  entity_id: "bdea5242-9627-43c1-a367-1990caa939f1",
  invoice_number: "TEST-001",
  invoice_date: "25-10-2025",
  due_date: "24-11-2025",
  subtotal_amount: 1000,
  gst_amount: 100,
  total_amount: 1100,
  paid_amount: 0,
  status: "draft",
  currency: "AUD",
  description: "Test invoice for PDF generation system",
  client_name: "Electric Sheep Music Pty Ltd",
  client_address: "Unit 5, 123 Business Park, Sydney NSW 2000",
  purchase_order_number: "0896",
  items: [
    {
      description: "Music Composition - Track Setup",
      quantity: 1,
      unit_price: 450.0,
      line_total: 450.0,
    },
    {
      description: "Production Services",
      quantity: 1,
      unit_price: 550.0,
      line_total: 550.0,
    },
  ],
  company_name: "[MOK HOUSE]",
  company_abn: "38 690 628 212",
  company_email: "hello@mokhouse.com.au",
  company_bsb: "013-943",
  company_account: "612281562",
  company_account_name: "MOK HOUSE PTY LTD",
};

// Helper to format currency
function formatCurrency(amount) {
  return `$${parseFloat(amount).toFixed(2)}`;
}

// Render line items as HTML
function renderLineItems(items) {
  return items
    .map(
      (item) => `      <div class="line-item">
        <div>${item.description}</div>
        <div>${item.quantity}</div>
        <div>${formatCurrency(item.unit_price)}</div>
        <div>${formatCurrency(item.line_total)}</div>
      </div>`
    )
    .join("\n    ");
}

// Load the template file
const templatePath = path.join(
  __dirname,
  "templates/invoice-test.html"
);
let htmlContent = fs.readFileSync(templatePath, "utf8");

// Replace invoice number
htmlContent = htmlContent.replace(/MH-001/g, invoiceData.invoice_number);

// Replace client name and address in Bill To section
htmlContent = htmlContent.replace(
  /<strong>Repco Australia<\/strong><br\/>\s*Unit 5, 123 Business Park<br\/>\s*Sydney NSW 2000/,
  `<strong>${invoiceData.client_name}</strong><br/>\n          ${invoiceData.client_address}`
);

// Replace PO number
htmlContent = htmlContent.replace(
  /<div class="bill-to-meta-value">0404<\/div>\s*<\/div>\s*<div class="bill-to-meta-item">\s*<div class="bill-to-meta-label">DATE/,
  `<div class="bill-to-meta-value">${invoiceData.purchase_order_number}</div>
          </div>
          <div class="bill-to-meta-item">
            <div class="bill-to-meta-label">DATE`
);

// Replace DATE value
htmlContent = htmlContent.replace(
  /<div class="bill-to-meta-value">25-10-2025<\/div>/,
  `<div class="bill-to-meta-value">${invoiceData.invoice_date}</div>`
);

// Replace line items - find the entire line-items div and replace it
const lineItemsRegex = /<div class="line-items">[\s\S]*?<\/div>\s*<hr \/>/;
const newLineItems = `<div class="line-items">
      ${renderLineItems(invoiceData.items)}
    </div>

    <hr />`;
htmlContent = htmlContent.replace(lineItemsRegex, newLineItems);

// Replace subtotal value - be very precise
htmlContent = htmlContent.replace(
  /\$3,000\.00/,
  formatCurrency(invoiceData.subtotal_amount)
);

// Replace GST value
htmlContent = htmlContent.replace(
  /\$300\.00/,
  formatCurrency(invoiceData.gst_amount)
);

// Replace grand total value
htmlContent = htmlContent.replace(
  /<div class="grand-total">\$3,300\.00<\/div>/,
  `<div class="grand-total">${formatCurrency(invoiceData.total_amount)}</div>`
);

// Write rendered HTML to temporary file
const htmlFile = path.join("/tmp", `invoice-${invoiceData.invoice_number}.html`);
fs.writeFileSync(htmlFile, htmlContent);
console.log(`✓ HTML rendered from template: ${htmlFile}`);

// Convert to PDF using wkhtmltopdf
const pdfFile = path.join("/tmp", `invoice-${invoiceData.invoice_number}.pdf`);

try {
  execSync(`wkhtmltopdf "${htmlFile}" "${pdfFile}"`, { stdio: "pipe" });
  console.log(`✓ PDF generated: ${pdfFile}`);

  // Check file exists and has size
  const stats = fs.statSync(pdfFile);
  console.log(`✓ PDF file size: ${(stats.size / 1024).toFixed(2)} KB`);

  // Output paths for use in email script
  console.log("\n=== READY FOR EMAIL ===");
  console.log(`PDF_FILE=${pdfFile}`);
  console.log(`INVOICE_NUMBER=${invoiceData.invoice_number}`);
  console.log(`INVOICE_DATE=${invoiceData.invoice_date}`);
  console.log(`TOTAL=${invoiceData.total_amount}`);

} catch (error) {
  console.error("❌ PDF generation failed:", error.message);
  process.exit(1);
}
