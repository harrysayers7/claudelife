/**
 * Test script for invoice PDF generation
 *
 * Usage:
 *   npm run test:invoices
 *   INVOICE_ID=invoice-uuid-here npm run test:invoices
 */

import { InvoicingService } from './invoicing-service';
import * as path from 'path';

async function testPdfGeneration() {
  const supabaseUrl = process.env.SUPABASE_URL || '';
  const supabaseKey = process.env.SUPABASE_KEY || '';
  const invoiceId = process.env.INVOICE_ID || '';

  if (!supabaseUrl || !supabaseKey) {
    console.error('❌ Missing required environment variables:');
    console.error('   SUPABASE_URL and SUPABASE_KEY must be set');
    process.exit(1);
  }

  const service = new InvoicingService(supabaseUrl, supabaseKey);

  try {
    console.log('🔄 Initializing invoicing service...');
    await service.initialize();
    console.log('✅ Service initialized\n');

    if (invoiceId) {
      // Test single invoice
      console.log(`📄 Testing PDF generation for invoice: ${invoiceId}`);
      const success = await service.generateAndStorePdf(invoiceId);

      if (success) {
        console.log('✅ PDF generated and stored successfully');
      } else {
        console.log('❌ Failed to generate PDF');
        process.exit(1);
      }
    } else {
      // Fetch and test with first available invoice
      console.log('🔍 Fetching MOK HOUSE invoices for testing...');

      // You'll need to replace this with actual entity ID from your database
      // For now, this is a placeholder
      const entityId = process.env.ENTITY_ID;

      if (!entityId) {
        console.warn('⚠️  ENTITY_ID not provided. Please set one of:');
        console.warn('   INVOICE_ID=<uuid> (to test specific invoice)');
        console.warn('   ENTITY_ID=<uuid> (to test first invoice for entity)');
        process.exit(0);
      }

      const invoices = await service.fetchEntityInvoices(entityId);

      if (invoices.length === 0) {
        console.log('❌ No invoices found for entity');
        process.exit(1);
      }

      console.log(`📊 Found ${invoices.length} invoices for entity`);
      console.log(`\nTesting with first invoice:`);
      console.log(`   Invoice: ${invoices[0].invoice_number}`);
      console.log(`   PO #: ${invoices[0].purchase_order_number || 'N/A'}`);
      console.log(`   Total: $${invoices[0].total_amount.toFixed(2)}`);
      console.log(`   Items: ${invoices[0].items?.length || 0}\n`);

      const success = await service.generateAndStorePdf(invoices[0].id);

      if (success) {
        console.log('✅ PDF generated and stored successfully');
      } else {
        console.log('❌ Failed to generate PDF');
        process.exit(1);
      }
    }

    console.log('\n📋 Test Summary:');
    console.log('   ✅ PDF generation working');
    console.log('   ✅ Supabase Storage integration working');
    console.log('   ✅ Database metadata insertion working');

  } catch (error) {
    console.error('❌ Test failed:', error);
    process.exit(1);
  } finally {
    console.log('\n🧹 Cleaning up...');
    await service.cleanup();
    console.log('✅ Done\n');
  }
}

// Run test
testPdfGeneration().catch((error) => {
  console.error('Unexpected error:', error);
  process.exit(1);
});
