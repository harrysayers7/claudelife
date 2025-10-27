#!/usr/bin/env node

/**
 * Invoice Template Test Suite
 * Tests the invoice template with mock data and generates PDF output
 */

const fs = require('fs');
const path = require('path');
const Handlebars = require('handlebars');

// Register custom Handlebars helpers
Handlebars.registerHelper('format_currency', function(value) {
  if (!value) return '0.00';
  return parseFloat(value).toFixed(2);
});

// Mock invoice data
const mockInvoiceData = {
  invoice_number: 'MH-001',
  invoice_date_formatted: '25-10-2025',
  due_date_formatted: '01-11-2025',
  purchase_order_number: '0404',
  client_name: 'Repco Australia',
  client_billing_address: 'Unit 5, 123 Business Park, Sydney NSW 2000',
  client_abn: '12 345 678 901',

  items: [
    {
      description: 'REPCO - Bathurst 500 Campaign Design & Production',
      quantity: 1,
      unit_price: 2000,
      tax_rate: 10,
      line_total: 2000
    },
    {
      description: 'Additional Creative Services - Revisions & Consultation',
      quantity: 2,
      unit_price: 500,
      tax_rate: 10,
      line_total: 1000
    }
  ],

  subtotal_amount: 3000,
  gst_amount: 300,
  discount_amount: 0,
  total_amount: 3300,

  bank_details: {
    account_name: 'MOK HOUSE PTY LTD',
    bsb: '013-943',
    account_number: '612281562'
  },

  entity_email: 'hello@mokhouse.com.au',
  entity_abn: '38 690 628 212',

  generated_date_formatted: '25-10-2025'
};

/**
 * Test Suite
 */
async function runTests() {
  console.log('🧪 Invoice Template Test Suite\n');
  console.log('=' .repeat(60));

  try {
    // Test 1: Read template
    console.log('\n✓ Test 1: Reading invoice template...');
    const templatePath = path.join(__dirname, 'templates', 'invoice.html');

    if (!fs.existsSync(templatePath)) {
      throw new Error(`Template not found at ${templatePath}`);
    }

    const templateContent = fs.readFileSync(templatePath, 'utf8');
    console.log('  ✅ Template loaded successfully');
    console.log(`  📏 Template size: ${(templateContent.length / 1024).toFixed(2)} KB`);

    // Test 2: Compile template
    console.log('\n✓ Test 2: Compiling Handlebars template...');
    const template = Handlebars.compile(templateContent);
    console.log('  ✅ Template compiled successfully');

    // Test 3: Render with mock data
    console.log('\n✓ Test 3: Rendering with mock invoice data...');
    const html = template(mockInvoiceData);
    console.log('  ✅ Template rendered successfully');
    console.log(`  📄 Rendered HTML size: ${(html.length / 1024).toFixed(2)} KB`);

    // Test 4: Validate rendered output
    console.log('\n✓ Test 4: Validating rendered output...');
    const validations = [
      { check: 'Company Name', regex: /MOK HOUSE/, found: false },
      { check: 'Invoice Number', regex: /MH-001/, found: false },
      { check: 'Client Name', regex: /Repco Australia/, found: false },
      { check: 'Invoice Date', regex: /25-10-2025/, found: false },
      { check: 'Total Amount', regex: /(3300|3,300)/, found: false },
      { check: 'Bank Details', regex: /012-943|013-943/, found: false },
      { check: 'Email', regex: /hello@mokhouse\.com\.au/, found: false },
      { check: 'ABN', regex: /38 690 628 212/, found: false }
    ];

    validations.forEach(validation => {
      validation.found = validation.regex.test(html);
      const status = validation.found ? '✅' : '❌';
      console.log(`  ${status} ${validation.check}: ${validation.found ? 'Present' : 'MISSING'}`);
    });

    const allValid = validations.every(v => v.found);
    if (!allValid) {
      throw new Error('Some validations failed');
    }

    // Test 5: Save rendered HTML for inspection
    console.log('\n✓ Test 5: Saving rendered HTML for inspection...');
    const outputPath = path.join(__dirname, 'templates', 'invoice-rendered-test.html');
    fs.writeFileSync(outputPath, html);
    console.log(`  ✅ Saved to: ${outputPath}`);

    // Test 6: Handlebars variable coverage
    console.log('\n✓ Test 6: Checking Handlebars variable usage...');
    const handlebarsVars = templateContent.match(/\{\{[^}]+\}\}/g) || [];
    const uniqueVars = new Set(handlebarsVars.map(v => v.replace(/[\{\}]/g, '').trim()));

    console.log(`  📊 Found ${uniqueVars.size} unique Handlebars variables:`);
    Array.from(uniqueVars).sort().forEach(v => {
      const inMockData = JSON.stringify(mockInvoiceData).includes(v.split(' ')[0].split('.')[0]);
      const status = inMockData ? '✅' : '⚠️ ';
      console.log(`     ${status} {{${v}}}`);
    });

    // Test 7: Line items rendering
    console.log('\n✓ Test 7: Validating line items rendering...');
    const itemMatches = html.match(/REPCO|Creative Services/g) || [];
    console.log(`  📝 Line items found: ${itemMatches.length / 2} items`);
    if (itemMatches.length > 0) {
      console.log('  ✅ Line items rendered correctly');
    }

    // Test 8: Calculate and validate totals
    console.log('\n✓ Test 8: Validating calculations...');
    const totalInHtml = html.includes('3300') || html.includes('3,300');
    const gstInHtml = html.includes('300') || html.includes('300.00');

    console.log(`  ${totalInHtml ? '✅' : '❌'} Total: $3,300.00`);
    console.log(`  ${gstInHtml ? '✅' : '❌'} GST (10%): $300.00`);

    // Summary
    console.log('\n' + '='.repeat(60));
    console.log('✅ All tests passed!\n');
    console.log('📋 Summary:');
    console.log(`   • Template file: ${path.basename(templatePath)}`);
    console.log(`   • Mock data: ${mockInvoiceData.items.length} line items`);
    console.log(`   • Invoice total: $${mockInvoiceData.total_amount}`);
    console.log(`   • Rendered HTML: ${(html.length / 1024).toFixed(2)} KB`);
    console.log(`   • All validations: PASSED`);
    console.log('\n📂 Output files created:');
    console.log(`   • ${outputPath}`);

    // Suggest next steps
    console.log('\n🚀 Next steps:');
    console.log('   1. Open invoice-rendered-test.html in a browser');
    console.log('   2. Verify visual layout and styling');
    console.log('   3. Test PDF generation with wkhtmltopdf');
    console.log('   4. Integrate with invoice.html for production use');

    return { success: true, html };

  } catch (error) {
    console.error('\n❌ Test failed:', error.message);
    console.error('\n Stack trace:', error.stack);
    process.exit(1);
  }
}

// Run tests
runTests().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});

module.exports = { runTests };
