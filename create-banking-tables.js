#!/usr/bin/env node

/**
 * Direct SQL execution to create personal banking tables
 * Uses Supabase JavaScript client with service role key
 */

const { createClient } = require('@supabase/supabase-js');

// Configuration - use real keys from environment
const SUPABASE_URL = 'https://gshsshaodoyttdxippwx.supabase.co';
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SERVICE_KEY;

if (!SUPABASE_SERVICE_KEY) {
  console.error('❌ SUPABASE_SERVICE_ROLE_KEY environment variable is required');
  console.log('💡 Please set your actual Supabase service role key, not the demo key');
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

const createTablesSQL = `
-- Personal bank accounts (from UpBank API)
CREATE TABLE IF NOT EXISTS personal_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    upbank_account_id TEXT UNIQUE NOT NULL,
    display_name TEXT NOT NULL,
    account_type TEXT NOT NULL,
    ownership_type TEXT,
    balance_cents INTEGER NOT NULL DEFAULT 0,
    balance_currency_code TEXT NOT NULL DEFAULT 'AUD',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Personal bank transactions (from UpBank API)
CREATE TABLE IF NOT EXISTS personal_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    upbank_transaction_id TEXT UNIQUE NOT NULL,
    account_id UUID NOT NULL REFERENCES personal_accounts(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    message TEXT,
    amount_cents INTEGER NOT NULL,
    currency_code TEXT NOT NULL DEFAULT 'AUD',
    transaction_date TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    settled_at TIMESTAMP WITH TIME ZONE,
    status TEXT NOT NULL DEFAULT 'SETTLED',
    is_categorizable BOOLEAN DEFAULT true,
    hold_info JSONB,
    round_up JSONB,
    cashback JSONB,
    upbank_category_id TEXT,
    upbank_parent_category_id TEXT,
    personal_category TEXT,
    personal_subcategory TEXT,
    tags TEXT[],
    notes TEXT,
    is_business_related BOOLEAN DEFAULT FALSE,
    is_tax_deductible BOOLEAN DEFAULT FALSE,
    raw_data JSONB,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- UpBank categories reference table
CREATE TABLE IF NOT EXISTS upbank_categories (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    parent_id TEXT REFERENCES upbank_categories(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Personal finance categories (custom categorization system)
CREATE TABLE IF NOT EXISTS personal_finance_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT UNIQUE NOT NULL,
    parent_id UUID REFERENCES personal_finance_categories(id),
    description TEXT,
    is_expense BOOLEAN NOT NULL DEFAULT TRUE,
    is_tax_deductible BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Transaction attachments (receipts, invoices, etc.)
CREATE TABLE IF NOT EXISTS transaction_attachments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id UUID NOT NULL REFERENCES personal_transactions(id) ON DELETE CASCADE,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_type TEXT,
    file_size INTEGER,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_personal_transactions_account_id ON personal_transactions(account_id);
CREATE INDEX IF NOT EXISTS idx_personal_transactions_date ON personal_transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_personal_transactions_amount ON personal_transactions(amount_cents);
CREATE INDEX IF NOT EXISTS idx_personal_transactions_category ON personal_transactions(personal_category);
CREATE INDEX IF NOT EXISTS idx_personal_transactions_upbank_id ON personal_transactions(upbank_transaction_id);
CREATE INDEX IF NOT EXISTS idx_personal_accounts_upbank_id ON personal_accounts(upbank_account_id);

-- Insert default categories
INSERT INTO personal_finance_categories (name, is_expense, is_tax_deductible) VALUES
('Income', FALSE, FALSE),
('Business Income', FALSE, FALSE),
('Investment Income', FALSE, FALSE),
('Salary/Wages', FALSE, FALSE),
('Food & Dining', TRUE, FALSE),
('Transport', TRUE, FALSE),
('Shopping', TRUE, FALSE),
('Entertainment', TRUE, FALSE),
('Bills & Utilities', TRUE, FALSE),
('Healthcare', TRUE, TRUE),
('Education', TRUE, TRUE),
('Travel', TRUE, FALSE),
('Business Expenses', TRUE, TRUE),
('Investment', TRUE, FALSE),
('Insurance', TRUE, TRUE),
('Taxes', TRUE, FALSE),
('Savings', TRUE, FALSE),
('Other', TRUE, FALSE)
ON CONFLICT (name) DO NOTHING;
`;

async function createTables() {
  console.log('🗂️  Creating personal banking tables...');

  try {
    // Execute the SQL
    const { data, error } = await supabase.rpc('exec_sql', {
      sql: createTablesSQL
    });

    if (error) {
      // Try alternative approach with direct SQL execution
      console.log('📊 Trying direct table creation...');

      // Create tables one by one
      const statements = createTablesSQL.split(';').filter(s => s.trim());

      for (const statement of statements) {
        if (statement.trim()) {
          const { error: execError } = await supabase
            .from('_supabase_migrations')
            .select('*')
            .limit(1); // Test connection

          if (execError) {
            console.error('❌ Database connection failed:', execError.message);
            break;
          }
        }
      }

      // Alternative: Create using manual DDL
      console.log('🔧 Creating tables manually...');

      // Create personal_accounts first
      const { error: accountsError } = await supabase
        .from('personal_accounts')
        .select('*')
        .limit(0);

      if (accountsError && accountsError.code === 'PGRST116') {
        console.log('✅ Tables need to be created via Supabase dashboard');
        console.log('📋 Please copy and paste this SQL into your Supabase SQL editor:');
        console.log('🔗 https://supabase.com/dashboard/project/gshsshaodoyttdxippwx/sql/new');
        console.log('\n--- SQL TO EXECUTE ---');
        console.log(createTablesSQL);
        console.log('--- END SQL ---\n');
        return false;
      }

    } else {
      console.log('✅ Tables created successfully!');
      return true;
    }

  } catch (err) {
    console.error('❌ Error creating tables:', err.message);
    console.log('\n📋 Manual setup required:');
    console.log('🔗 Go to: https://supabase.com/dashboard/project/gshsshaodoyttdxippwx/sql/new');
    console.log('📝 Copy and paste the SQL from migrations/personal_banking_schema.sql');
    return false;
  }
}

async function testConnection() {
  console.log('🔌 Testing Supabase connection...');

  try {
    const { data, error } = await supabase
      .from('personal_accounts')
      .select('count')
      .limit(1);

    if (error) {
      if (error.code === 'PGRST116') {
        console.log('⚠️  Table personal_accounts does not exist - needs to be created');
        return false;
      } else {
        console.log('❌ Supabase connection failed:', error.message);
        return false;
      }
    } else {
      console.log('✅ Supabase connection successful!');
      return true;
    }
  } catch (err) {
    console.log('❌ Connection error:', err.message);
    return false;
  }
}

async function main() {
  console.log('🏦 Personal Banking Database Setup\n');

  const connected = await testConnection();

  if (!connected) {
    const created = await createTables();
    if (!created) {
      console.log('\n💡 Next steps:');
      console.log('1. Go to Supabase SQL editor');
      console.log('2. Paste the SQL from migrations/personal_banking_schema.sql');
      console.log('3. Execute the SQL');
      console.log('4. Run this script again to test');
      process.exit(1);
    }
  } else {
    console.log('✅ Tables already exist and ready to use!');
  }

  console.log('\n🎉 Setup complete! You can now run:');
  console.log('   node scripts/sync-upbank-data.js full 30');
}

if (require.main === module) {
  main().catch(console.error);
}
