import { createClient, SupabaseClient } from '@supabase/supabase-js';
import { InvoicePdfGenerator, InvoiceData } from './pdf-generator';
import { InvoicePdfStorage } from './supabase-storage';
import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';

/**
 * Complete invoicing service
 * Handles: database queries, PDF generation, storage, and metadata tracking
 */
export class InvoicingService {
  private supabase: SupabaseClient;
  private pdfGenerator: InvoicePdfGenerator;
  private pdfStorage: InvoicePdfStorage;
  private tempDir: string;

  constructor(
    supabaseUrl: string,
    supabaseKey: string,
    templatePath?: string
  ) {
    this.supabase = createClient(supabaseUrl, supabaseKey);
    this.pdfGenerator = new InvoicePdfGenerator(templatePath);
    this.pdfStorage = new InvoicePdfStorage(supabaseUrl, supabaseKey);
    this.tempDir = path.join(os.tmpdir(), 'invoice-pdfs');

    // Create temp directory if it doesn't exist
    if (!fs.existsSync(this.tempDir)) {
      fs.mkdirSync(this.tempDir, { recursive: true });
    }
  }

  /**
   * Initialize service (create storage bucket, setup browser)
   */
  async initialize() {
    await this.pdfStorage.ensureBucket();
    await this.pdfGenerator.initialize();
  }

  /**
   * Fetch invoice data from database
   */
  async fetchInvoiceData(invoiceId: string): Promise<InvoiceData | null> {
    try {
      // Fetch invoice from public schema
      const { data: invoiceData, error: invoiceError } = await this.supabase
        .from('invoices')
        .select('*')
        .eq('id', invoiceId)
        .single();

      if (invoiceError) {
        console.error('Error fetching invoice:', invoiceError);
        return null;
      }

      // Fetch entity and contact details
      const { data: entityData } = await this.supabase
        .from('entities')
        .select('*')
        .eq('id', invoiceData.entity_id)
        .single();

      const { data: contactData } = await this.supabase
        .from('contacts')
        .select('*')
        .eq('id', invoiceData.contact_id)
        .single();

      // Map database record to InvoiceData interface
      const mapped: InvoiceData = {
        id: invoiceData.id,
        entity_id: invoiceData.entity_id,
        contact_id: invoiceData.contact_id,
        invoice_number: invoiceData.invoice_number,
        purchase_order_number: invoiceData.purchase_order_number,
        invoice_date: invoiceData.invoice_date,
        due_date: invoiceData.due_date,
        project: invoiceData.project,
        project_id: invoiceData.project_id,
        subtotal_amount: parseFloat(invoiceData.subtotal_amount || '0'),
        gst_amount: parseFloat(invoiceData.gst_amount || '0'),
        total_amount: parseFloat(invoiceData.total_amount || '0'),
        status: invoiceData.status,
        client_name: contactData?.name || invoiceData.client || '',
        client_email: contactData?.email,
        client_abn: contactData?.abn,
        billing_address: invoiceData.billed_to,
        entity_name: entityData?.name || '',
        entity_abn: entityData?.abn || '',
        trading_name: entityData?.trading_name,
        invoice_prefix: invoiceData.invoice_number?.split('-')[0] || 'INV',
        items: [], // No line items in current schema
      };

      return mapped;
    } catch (error) {
      console.error('Error fetching invoice data:', error);
      return null;
    }
  }

  /**
   * Fetch all invoices for an entity
   */
  async fetchEntityInvoices(entityId: string): Promise<InvoiceData[]> {
    try {
      const { data: invoices, error } = await this.supabase
        .from('invoices')
        .select('*')
        .eq('entity_id', entityId)
        .order('invoice_date', { ascending: false });

      if (error) {
        console.error('Error fetching entity invoices:', error);
        return [];
      }

      // Fetch entity and contacts data for enrichment
      const { data: entityData } = await this.supabase
        .from('entities')
        .select('*')
        .eq('id', entityId)
        .single();

      const contactIds = [...new Set((invoices || []).map(i => i.contact_id))];
      const { data: contactsData } = await this.supabase
        .from('contacts')
        .select('*')
        .in('id', contactIds);

      const contactMap = new Map(contactsData?.map(c => [c.id, c]) || []);

      // Map all invoices
      const mapped = (invoices || []).map(inv => ({
        id: inv.id,
        entity_id: inv.entity_id,
        contact_id: inv.contact_id,
        invoice_number: inv.invoice_number,
        purchase_order_number: inv.purchase_order_number,
        invoice_date: inv.invoice_date,
        due_date: inv.due_date,
        project: inv.project,
        project_id: inv.project_id,
        subtotal_amount: parseFloat(inv.subtotal_amount || '0'),
        gst_amount: parseFloat(inv.gst_amount || '0'),
        total_amount: parseFloat(inv.total_amount || '0'),
        status: inv.status,
        client_name: contactMap.get(inv.contact_id)?.name || inv.client || '',
        client_email: contactMap.get(inv.contact_id)?.email,
        client_abn: contactMap.get(inv.contact_id)?.abn,
        billing_address: inv.billed_to,
        entity_name: entityData?.name || '',
        entity_abn: entityData?.abn || '',
        trading_name: entityData?.trading_name,
        invoice_prefix: inv.invoice_number?.split('-')[0] || 'INV',
        items: [], // No line items in current schema
      } as InvoiceData));

      return mapped;
    } catch (error) {
      console.error('Error fetching entity invoices:', error);
      return [];
    }
  }

  /**
   * Generate and store invoice PDF
   * Returns URL and metadata for database insertion
   */
  async generateInvoicePdf(invoiceId: string): Promise<{
    pdf_url: string;
    file_name: string;
    storage_path: string;
    pdf_size_bytes: number;
  } | null> {
    try {
      // Fetch invoice data
      const invoiceData = await this.fetchInvoiceData(invoiceId);
      if (!invoiceData) {
        throw new Error(`Invoice not found: ${invoiceId}`);
      }

      // Generate PDF locally
      const tempPdfPath = path.join(
        this.tempDir,
        `${invoiceData.invoice_number.replace(/\//g, '-')}-${Date.now()}`
      );

      const pdfPath = await this.pdfGenerator.generatePdf(
        invoiceData,
        tempPdfPath
      );

      // Get file size
      const stats = fs.statSync(pdfPath);
      const fileSizeBytes = stats.size;

      // Upload to Supabase Storage
      const publicUrl = await this.pdfStorage.uploadPdf(
        pdfPath,
        invoiceData.invoice_number,
        invoiceData.entity_id
      );

      // Generate storage path (same as used in storage)
      const date = new Date();
      const year = date.getFullYear();
      const storagePath = `${invoiceData.entity_id}/${year}/${invoiceData.invoice_number.replace(/\//g, '-')}.pdf`;

      // Generate file name
      const fileName = `${invoiceData.invoice_number}.pdf`;

      // Clean up temporary file
      fs.unlinkSync(pdfPath);

      console.log(`✓ Successfully generated invoice PDF for ${invoiceData.invoice_number}`);

      return {
        pdf_url: publicUrl,
        file_name: fileName,
        storage_path: storagePath,
        pdf_size_bytes: fileSizeBytes,
      };
    } catch (error) {
      console.error('Error generating invoice PDF:', error);
      return null;
    }
  }

  /**
   * Save PDF metadata to database
   * Note: Currently skipped as invoice_pdfs table doesn't exist in schema
   * PDF URL is already stored in Supabase Storage and accessible
   */
  async savePdfMetadata(
    invoiceId: string,
    pdfData: {
      pdf_url: string;
      file_name: string;
      storage_path: string;
      pdf_size_bytes: number;
    }
  ) {
    try {
      // TODO: When invoice_pdfs table is created, implement metadata storage here
      // const { error } = await this.supabase
      //   .from('invoice_pdfs')
      //   .insert({
      //     invoice_id: invoiceId,
      //     pdf_url: pdfData.pdf_url,
      //     file_name: pdfData.file_name,
      //     storage_path: pdfData.storage_path,
      //     pdf_size_bytes: pdfData.pdf_size_bytes,
      //     generated_at: new Date().toISOString(),
      //   });

      console.log(`✓ PDF stored for invoice ${invoiceId}: ${pdfData.pdf_url}`);
    } catch (error) {
      console.error('Error saving PDF metadata:', error);
      throw error;
    }
  }

  /**
   * Complete workflow: Generate PDF and save metadata
   */
  async generateAndStorePdf(invoiceId: string): Promise<boolean> {
    try {
      const pdfData = await this.generateInvoicePdf(invoiceId);
      if (!pdfData) {
        return false;
      }

      await this.savePdfMetadata(invoiceId, pdfData);
      return true;
    } catch (error) {
      console.error('Error in generate and store workflow:', error);
      return false;
    }
  }

  /**
   * Generate PDFs for multiple invoices
   */
  async generateBatch(invoiceIds: string[]): Promise<{
    success: number;
    failed: number;
    results: Array<{ invoiceId: string; success: boolean; error?: string }>;
  }> {
    const results = [];
    let successCount = 0;
    let failureCount = 0;

    for (const invoiceId of invoiceIds) {
      try {
        const success = await this.generateAndStorePdf(invoiceId);
        if (success) {
          successCount++;
          results.push({ invoiceId, success: true });
        } else {
          failureCount++;
          results.push({ invoiceId, success: false, error: 'Generation failed' });
        }
      } catch (error) {
        failureCount++;
        results.push({
          invoiceId,
          success: false,
          error: String(error),
        });
      }
    }

    console.log(
      `✓ Batch complete: ${successCount} succeeded, ${failureCount} failed`
    );

    return {
      success: successCount,
      failed: failureCount,
      results,
    };
  }

  /**
   * Clean up resources
   */
  async cleanup() {
    await this.pdfGenerator.close();

    // Clean up temp directory
    if (fs.existsSync(this.tempDir)) {
      const files = fs.readdirSync(this.tempDir);
      for (const file of files) {
        fs.unlinkSync(path.join(this.tempDir, file));
      }
      fs.rmdirSync(this.tempDir);
    }
  }
}

/**
 * Example usage / CLI entry point
 */
async function main() {
  const supabaseUrl = process.env.SUPABASE_URL || '';
  const supabaseKey = process.env.SUPABASE_KEY || '';

  if (!supabaseUrl || !supabaseKey) {
    console.error('Missing SUPABASE_URL or SUPABASE_KEY environment variables');
    process.exit(1);
  }

  const service = new InvoicingService(supabaseUrl, supabaseKey);

  try {
    await service.initialize();
    console.log('✓ Invoicing service initialized');

    // Example: Generate PDF for a specific invoice
    // Uncomment to test:
    // const success = await service.generateAndStorePdf('invoice-uuid-here');
    // console.log('Generation result:', success);

  } catch (error) {
    console.error('Error:', error);
  } finally {
    await service.cleanup();
  }
}

// Uncomment to run as CLI
// if (require.main === module) {
//   main();
// }
