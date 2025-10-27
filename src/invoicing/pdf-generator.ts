import { chromium, Browser, Page } from 'playwright';
import * as fs from 'fs';
import * as path from 'path';
import Handlebars from 'handlebars';

/**
 * Invoice data type matching the v_invoice_with_items view structure
 */
export interface InvoiceLineItem {
  id: string;
  description: string;
  quantity: number;
  unit_price: number;
  tax_rate: number;
  line_total: number;
  line_tax: number;
}

export interface InvoiceData {
  id: string;
  entity_id: string;
  contact_id: string;
  invoice_number: string;
  purchase_order_number?: string;
  invoice_date: string;
  due_date: string;
  project?: string;
  project_id?: string;
  subtotal_amount: number;
  gst_amount: number;
  total_amount: number;
  status: string;
  client_name: string;
  client_email?: string;
  client_abn?: string;
  billing_address?: string;
  entity_name: string;
  entity_abn: string;
  trading_name?: string;
  invoice_prefix: string;
  bank_details?: {
    account_name?: string;
    bsb?: string;
    account_number?: string;
    swift_code?: string;
  };
  footer_text?: string;
  items: InvoiceLineItem[];
}

/**
 * PDF Generator for invoices using Playwright
 * Renders HTML templates to PDF and stores in specified directory
 */
export class InvoicePdfGenerator {
  private browser: Browser | null = null;
  private templatePath: string;

  constructor(templatePath?: string) {
    this.templatePath =
      templatePath ||
      path.join(__dirname, 'templates', 'invoice.html');
  }

  /**
   * Initialize browser instance (call once per application)
   */
  async initialize() {
    if (!this.browser) {
      this.browser = await chromium.launch({
        headless: true,
      });
    }
  }

  /**
   * Format currency for display (Australian format)
   */
  private formatCurrency(amount: number): string {
    return amount.toFixed(2);
  }

  /**
   * Format date to Australian format (DD/MM/YYYY)
   */
  private formatDate(dateString: string): string {
    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
  }

  /**
   * Register Handlebars helpers for template rendering
   */
  private registerHelpers() {
    Handlebars.registerHelper('format_currency', (amount: number) => {
      return this.formatCurrency(amount);
    });

    Handlebars.registerHelper('if', function (this: any, condition: any, options: any) {
      if (condition) {
        return options.fn(this);
      } else {
        return options.inverse(this);
      }
    });

    Handlebars.registerHelper('each', function (context: any, options: any) {
      let output = '';
      if (Array.isArray(context)) {
        for (let i = 0; i < context.length; i++) {
          output += options.fn(context[i]);
        }
      }
      return output;
    });
  }

  /**
   * Generate PDF from invoice data
   * @param invoiceData Invoice data from database
   * @param outputPath Path to save PDF (without extension)
   * @returns Path to generated PDF file
   */
  async generatePdf(
    invoiceData: InvoiceData,
    outputPath: string
  ): Promise<string> {
    if (!this.browser) {
      await this.initialize();
    }

    try {
      this.registerHelpers();

      // Read and compile template
      const templateHtml = fs.readFileSync(this.templatePath, 'utf-8');
      const template = Handlebars.compile(templateHtml);

      // Prepare data for template
      const templateData = {
        ...invoiceData,
        invoice_date_formatted: this.formatDate(invoiceData.invoice_date),
        due_date_formatted: this.formatDate(invoiceData.due_date),
        generated_date_formatted: this.formatDate(new Date().toISOString()),
        entity_billing_address:
          invoiceData.billing_address || '[Address not provided]',
        client_billing_address:
          invoiceData.billing_address || '[Address not provided]',
        payment_terms_days: 14, // Default, can be customized per entity
        subtotal_amount: invoiceData.subtotal_amount,
        gst_amount: invoiceData.gst_amount,
        total_amount: invoiceData.total_amount,
      };

      // Render HTML
      const html = template(templateData);

      // Create page and generate PDF
      const page = await this.browser!.newPage();
      await page.setContent(html, { waitUntil: 'networkidle' });

      const pdfPath = `${outputPath}.pdf`;
      await page.pdf({
        path: pdfPath,
        format: 'A4',
        margin: {
          top: '0mm',
          right: '0mm',
          bottom: '0mm',
          left: '0mm',
        },
        printBackground: true,
      });

      await page.close();

      return pdfPath;
    } catch (error) {
      console.error('Error generating PDF:', error);
      throw new Error(`Failed to generate PDF for invoice ${invoiceData.invoice_number}: ${error}`);
    }
  }

  /**
   * Generate multiple PDFs in batch
   */
  async generatePdfBatch(
    invoices: InvoiceData[],
    outputDir: string
  ): Promise<{ invoice_number: string; pdf_path: string }[]> {
    const results = [];

    for (const invoice of invoices) {
      const outputPath = path.join(
        outputDir,
        `${invoice.invoice_number.replace(/\//g, '-')}`
      );

      try {
        const pdfPath = await this.generatePdf(invoice, outputPath);
        results.push({
          invoice_number: invoice.invoice_number,
          pdf_path: pdfPath,
        });
        console.log(
          `✓ Generated PDF for invoice ${invoice.invoice_number}`
        );
      } catch (error) {
        console.error(
          `✗ Failed to generate PDF for invoice ${invoice.invoice_number}:`,
          error
        );
        results.push({
          invoice_number: invoice.invoice_number,
          pdf_path: '',
        });
      }
    }

    return results;
  }

  /**
   * Close browser instance (call on application shutdown)
   */
  async close() {
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
    }
  }
}

/**
 * Convenience function for one-off PDF generation
 */
export async function generateInvoicePdf(
  invoiceData: InvoiceData,
  outputPath: string,
  templatePath?: string
): Promise<string> {
  const generator = new InvoicePdfGenerator(templatePath);
  try {
    await generator.initialize();
    return await generator.generatePdf(invoiceData, outputPath);
  } finally {
    await generator.close();
  }
}
