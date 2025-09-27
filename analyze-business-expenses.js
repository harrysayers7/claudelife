#!/usr/bin/env node

const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(
  'https://gshsshaodoyttdxippwx.supabase.co',
  process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SERVICE_KEY
);

async function identifyBusinessExpenses() {
  console.log('🔍 Identifying potential business expenses using ML categorization...');

  // Get uncategorized transactions with descriptions
  const { data: transactions, error } = await supabase
    .from('personal_transactions')
    .select('id, description, amount_cents, settled_at, ai_category, ai_confidence, is_business_related')
    .eq('status', 'SETTLED')
    .lt('amount_cents', 0) // Only spending transactions
    .is('ai_category', null) // Uncategorized
    .order('amount_cents', { ascending: true }); // Largest expenses first

  if (error) {
    console.error('❌ Error fetching transactions:', error);
    return;
  }

  console.log(`📊 Found ${transactions.length} uncategorized spending transactions`);

  // Business keywords for pattern matching
  const businessKeywords = [
    // Technology & Software
    'adobe', 'microsoft', 'google', 'aws', 'github', 'notion', 'slack', 'zoom', 'office',
    'software', 'subscription', 'saas', 'hosting', 'domain', 'ssl',

    // Business Services
    'accountant', 'lawyer', 'consultant', 'professional', 'service', 'invoice',
    'xero', 'quickbooks', 'accounting', 'bookkeeping',

    // Marketing & Advertising
    'advertising', 'marketing', 'facebook', 'google ads', 'linkedin', 'social media',
    'design', 'branding', 'website', 'seo',

    // Business Equipment & Supplies
    'office', 'equipment', 'computer', 'laptop', 'printer', 'stationery',
    'desk', 'chair', 'monitor', 'keyboard', 'mouse',

    // Travel & Business Meals
    'hotel', 'flight', 'uber', 'taxi', 'conference', 'meeting', 'business lunch',
    'restaurant', 'cafe', 'catering',

    // Utilities & Services
    'internet', 'phone', 'mobile', 'electricity', 'insurance', 'business'
  ];

  let potentialBusinessCount = 0;
  let alreadyFlagged = 0;

  console.log('\n🔍 Potential Business Expenses (largest first):');

  // Analyze each transaction
  transactions.slice(0, 20).forEach(tx => {
    const description = tx.description.toLowerCase();
    const amount = Math.abs(tx.amount_cents) / 100;

    // Check if already flagged as business
    if (tx.is_business_related) {
      alreadyFlagged++;
      return;
    }

    // Check for business keywords
    const matchedKeywords = businessKeywords.filter(keyword =>
      description.includes(keyword.toLowerCase())
    );

    if (matchedKeywords.length > 0) {
      potentialBusinessCount++;
      console.log(`  💼 AUD $${amount.toFixed(2)} - ${tx.description}`);
      console.log(`     Keywords: ${matchedKeywords.join(', ')}`);
      console.log(`     Date: ${tx.settled_at.substring(0, 10)}`);
    }
  });

  console.log(`\n📊 Summary:`);
  console.log(`  • Already flagged as business: ${alreadyFlagged} transactions`);
  console.log(`  • Potential new business expenses: ${potentialBusinessCount} transactions`);
  console.log(`  • ML categorization coverage: ${((transactions.length - potentialBusinessCount) / transactions.length * 100).toFixed(1)}% need attention`);

  // Show some examples of unclear transactions that need manual review
  console.log('\n❓ Transactions needing manual review (sample):');
  transactions
    .filter(tx => {
      const description = tx.description.toLowerCase();
      const hasBusinessKeywords = businessKeywords.some(keyword =>
        description.includes(keyword.toLowerCase())
      );
      return !hasBusinessKeywords && !tx.is_business_related;
    })
    .slice(0, 10)
    .forEach(tx => {
      const amount = Math.abs(tx.amount_cents) / 100;
      console.log(`  ❓ AUD $${amount.toFixed(2)} - ${tx.description} (${tx.settled_at.substring(0, 10)})`);
    });

  return { potentialBusinessCount, alreadyFlagged, totalUncategorized: transactions.length };
}

async function updateBusinessExpenseFlags() {
  console.log('🔧 Updating business expense flags in database...');

  // Define specific business patterns with categories
  const businessPatterns = [
    { pattern: 'claude', category: 'AI & Software Subscriptions', confidence: 0.95 },
    { pattern: 'practice pty', category: 'Professional Services', confidence: 0.9 },
    { pattern: 'tesla', category: 'Business Vehicle', confidence: 0.8 },
    { pattern: 'adobe', category: 'Software Subscriptions', confidence: 0.9 },
    { pattern: 'microsoft', category: 'Software Subscriptions', confidence: 0.9 },
    { pattern: 'google', category: 'Software Subscriptions', confidence: 0.85 },
    { pattern: 'github', category: 'Development Tools', confidence: 0.9 },
    { pattern: 'aws', category: 'Cloud Services', confidence: 0.9 },
    { pattern: 'notion', category: 'Software Subscriptions', confidence: 0.85 },
    { pattern: 'zoom', category: 'Software Subscriptions', confidence: 0.8 }
  ];

  // Get transactions that match business patterns but aren't flagged yet
  const { data: transactions, error } = await supabase
    .from('personal_transactions')
    .select('id, description, amount_cents, is_business_related')
    .eq('status', 'SETTLED')
    .lt('amount_cents', 0)
    .eq('is_business_related', false); // Only unflagged transactions

  if (error) {
    console.error('❌ Error fetching transactions:', error);
    return;
  }

  let updatedCount = 0;
  let totalAmount = 0;

  console.log(`📊 Checking ${transactions.length} unflagged transactions...`);

  for (const tx of transactions) {
    const description = tx.description.toLowerCase();

    // Find matching business pattern
    const match = businessPatterns.find(bp =>
      description.includes(bp.pattern.toLowerCase())
    );

    if (match) {
      // Update the transaction
      const { error: updateError } = await supabase
        .from('personal_transactions')
        .update({
          is_business_related: true,
          business_category: match.category,
          ai_confidence: match.confidence,
          is_tax_deductible: true,
          notes: `Auto-flagged: ${match.pattern} pattern (${(match.confidence * 100).toFixed(0)}% confidence)`
        })
        .eq('id', tx.id);

      if (updateError) {
        console.error(`❌ Error updating transaction ${tx.id}:`, updateError);
      } else {
        updatedCount++;
        totalAmount += Math.abs(tx.amount_cents);
        console.log(`✅ Updated: ${tx.description} → ${match.category} (${(match.confidence * 100).toFixed(0)}% confidence)`);
      }
    }
  }

  console.log(`\n📊 Summary:`);
  console.log(`  • Transactions updated: ${updatedCount}`);
  console.log(`  • Total business expenses flagged: AUD $${(totalAmount / 100).toFixed(2)}`);

  return { updatedCount, totalAmount };
}

// Run both functions
async function runAnalysis() {
  try {
    console.log('=== Business Expense Analysis ===\n');

    // First, identify potential business expenses
    await identifyBusinessExpenses();

    console.log('\n=== Updating Database ===\n');

    // Then update the database with flags
    await updateBusinessExpenseFlags();

    console.log('\n✅ Analysis complete!');

  } catch (error) {
    console.error('❌ Analysis failed:', error);
  }
}

runAnalysis();
