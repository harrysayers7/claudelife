import { createClient, SupabaseClient } from '@supabase/supabase-js';
import * as fs from 'fs';
import * as path from 'path';

/**
 * Supabase Storage integration for invoice PDFs
 * Handles upload, retrieval, and deletion of invoice PDFs from Supabase Storage
 */
export class InvoicePdfStorage {
  private supabase: SupabaseClient;
  private bucketName = 'invoice-pdfs';

  constructor(supabaseUrl: string, supabaseKey: string) {
    this.supabase = createClient(supabaseUrl, supabaseKey);
  }

  /**
   * Create the bucket if it doesn't exist
   */
  async ensureBucket() {
    try {
      const { data: buckets } = await this.supabase.storage.listBuckets();

      const bucketExists = buckets?.some((b) => b.name === this.bucketName);

      if (!bucketExists) {
        const { error } = await this.supabase.storage.createBucket(
          this.bucketName,
          {
            public: false,
            fileSizeLimit: 52428800, // 50MB
          }
        );

        if (error) {
          console.error('Error creating bucket:', error);
          throw new Error(`Failed to create storage bucket: ${error.message}`);
        }

        console.log(`✓ Created storage bucket: ${this.bucketName}`);
      }
    } catch (error) {
      console.error('Error ensuring bucket:', error);
      throw error;
    }
  }

  /**
   * Upload PDF to Supabase Storage
   * @param localPdfPath Path to local PDF file
   * @param invoiceNumber Invoice number for naming
   * @param entityId Entity ID for organization
   * @returns Public URL of uploaded PDF
   */
  async uploadPdf(
    localPdfPath: string,
    invoiceNumber: string,
    entityId: string
  ): Promise<string> {
    try {
      // Verify file exists
      if (!fs.existsSync(localPdfPath)) {
        throw new Error(`PDF file not found: ${localPdfPath}`);
      }

      // Read file
      const fileBuffer = fs.readFileSync(localPdfPath);

      // Generate storage path: /entity-id/year/invoice-number.pdf
      const date = new Date();
      const year = date.getFullYear();
      const storagePath = `${entityId}/${year}/${invoiceNumber.replace(/\//g, '-')}.pdf`;

      // Upload to Supabase (upsert: true allows overwriting existing PDFs)
      const { data, error } = await this.supabase.storage
        .from(this.bucketName)
        .upload(storagePath, fileBuffer, {
          contentType: 'application/pdf',
          upsert: true,
        });

      if (error) {
        throw new Error(`Upload failed: ${error.message}`);
      }

      // Get public URL
      const { data: urlData } = this.supabase.storage
        .from(this.bucketName)
        .getPublicUrl(storagePath);

      const publicUrl = urlData.publicUrl;

      console.log(
        `✓ Uploaded invoice ${invoiceNumber} to Supabase Storage`
      );
      console.log(`  Path: ${storagePath}`);
      console.log(`  URL: ${publicUrl}`);

      return publicUrl;
    } catch (error) {
      console.error('Error uploading PDF:', error);
      throw new Error(`Failed to upload PDF for invoice ${invoiceNumber}: ${error}`);
    }
  }

  /**
   * Delete PDF from Supabase Storage
   */
  async deletePdf(invoiceNumber: string, entityId: string) {
    try {
      const date = new Date();
      const year = date.getFullYear();
      const storagePath = `${entityId}/${year}/${invoiceNumber.replace(/\//g, '-')}.pdf`;

      const { error } = await this.supabase.storage
        .from(this.bucketName)
        .remove([storagePath]);

      if (error) {
        throw new Error(`Delete failed: ${error.message}`);
      }

      console.log(`✓ Deleted invoice ${invoiceNumber} from storage`);
    } catch (error) {
      console.error('Error deleting PDF:', error);
      throw error;
    }
  }

  /**
   * Get signed URL for temporary access (useful for private PDFs)
   */
  async getSignedUrl(
    invoiceNumber: string,
    entityId: string,
    expiresIn: number = 3600
  ): Promise<string> {
    try {
      const date = new Date();
      const year = date.getFullYear();
      const storagePath = `${entityId}/${year}/${invoiceNumber.replace(/\//g, '-')}.pdf`;

      const { data, error } = await this.supabase.storage
        .from(this.bucketName)
        .createSignedUrl(storagePath, expiresIn);

      if (error) {
        throw new Error(`Signed URL creation failed: ${error.message}`);
      }

      return data.signedUrl;
    } catch (error) {
      console.error('Error getting signed URL:', error);
      throw error;
    }
  }

  /**
   * List all PDFs for an entity
   */
  async listEntityPdfs(entityId: string) {
    try {
      const { data, error } = await this.supabase.storage
        .from(this.bucketName)
        .list(entityId, {
          limit: 1000,
          offset: 0,
          sortBy: { column: 'name', order: 'desc' },
        });

      if (error) {
        throw new Error(`List failed: ${error.message}`);
      }

      return data || [];
    } catch (error) {
      console.error('Error listing PDFs:', error);
      throw error;
    }
  }

  /**
   * Download PDF from storage
   */
  async downloadPdf(
    invoiceNumber: string,
    entityId: string,
    outputPath: string
  ) {
    try {
      const date = new Date();
      const year = date.getFullYear();
      const storagePath = `${entityId}/${year}/${invoiceNumber.replace(/\//g, '-')}.pdf`;

      const { data, error } = await this.supabase.storage
        .from(this.bucketName)
        .download(storagePath);

      if (error) {
        throw new Error(`Download failed: ${error.message}`);
      }

      // Write to local file
      fs.writeFileSync(outputPath, Buffer.from(await data.arrayBuffer()));

      console.log(`✓ Downloaded invoice ${invoiceNumber} to ${outputPath}`);
    } catch (error) {
      console.error('Error downloading PDF:', error);
      throw error;
    }
  }
}

/**
 * Convenience function for quick uploads
 */
export async function uploadInvoicePdf(
  localPdfPath: string,
  invoiceNumber: string,
  entityId: string,
  supabaseUrl: string,
  supabaseKey: string
): Promise<string> {
  const storage = new InvoicePdfStorage(supabaseUrl, supabaseKey);
  await storage.ensureBucket();
  return await storage.uploadPdf(localPdfPath, invoiceNumber, entityId);
}
