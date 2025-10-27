#!/usr/bin/env node

/**
 * Generate invoice PDF from Handlebars template
 * Properly renders template before converting to PDF
 */

const fs = require("fs");
const path = require("path");
const Handlebars = require("handlebars");
const puppeteer = require("puppeteer");
const nodemailer = require("nodemailer");

// Register Handlebars helpers
Handlebars.registerHelper("format_currency", function (amount) {
  return parseFloat(amount).toFixed(2);
});

// Invoice data
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

// Load and compile template
const templatePath = path.join(__dirname, "templates/invoice.html");
const templateSource = fs.readFileSync(templatePath, "utf8");
const template = Handlebars.compile(templateSource);

// Render HTML
const html = template(invoiceData);

// Write to temp HTML file
const htmlFile = `/tmp/invoice-${invoiceData.invoice_number}.html`;
fs.writeFileSync(htmlFile, html);
console.log(`✓ HTML rendered: ${htmlFile}`);

// Convert to PDF with Puppeteer
const pdfFile = `/tmp/invoice-${invoiceData.invoice_number}.pdf`;
(async () => {
  try {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Load the HTML file
    await page.goto(`file://${htmlFile}`, { waitUntil: "networkidle0" });

    // Generate PDF with proper formatting
    await page.pdf({
      path: pdfFile,
      format: "A4",
      margin: { top: 0, bottom: 0, left: 0, right: 0 },
      printBackground: true,
    });

    await browser.close();

    const stats = fs.statSync(pdfFile);
    console.log(`✓ PDF generated: ${pdfFile} (${(stats.size / 1024).toFixed(2)} KB)`);

    // Send email with attachment
    const transporter = nodemailer.createTransport({
      service: "gmail",
      auth: {
        user: process.env.GMAIL_USER,
        pass: process.env.GMAIL_APP_PASSWORD,
      },
    });

    const recipientEmail = process.env.RECIPIENT_EMAIL || "harry@sayers1.com";

    const mailOptions = {
      from: process.env.GMAIL_USER,
      to: recipientEmail,
      subject: `Invoice ${invoiceData.invoice_number} - MOK HOUSE`,
      html: `
        <p>Hi,</p>
        <p>Please find attached your invoice.</p>
        <p><strong>Invoice Number:</strong> ${invoiceData.invoice_number}<br>
        <strong>Date:</strong> ${invoiceData.invoice_date}<br>
        <strong>Total:</strong> $${invoiceData.grand_total}</p>
        <p>Thank you for your business.</p>
        <p>Best regards,<br>MOK HOUSE PTY LTD</p>
      `,
      attachments: [
        {
          filename: `INV-${invoiceData.invoice_number}.pdf`,
          path: pdfFile,
        },
      ],
    };

    transporter.sendMail(mailOptions, (error, info) => {
      if (error) {
        console.error("❌ Email failed:", error.message);
        process.exit(1);
      }
      console.log(`✓ Email sent to ${recipientEmail}`);
      console.log(`📎 Attachment: INV-${invoiceData.invoice_number}.pdf`);
      console.log(`\nPDF_FILE=${pdfFile}`);
    });
  } catch (error) {
    console.error("❌ PDF generation failed:", error.message);
    process.exit(1);
  }
})();
