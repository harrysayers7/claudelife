-- Personal Banking Database Schema for Harrison Sayers
-- Compatible with UpBank API data structure

-- Personal bank accounts (from UpBank API)
CREATE TABLE IF NOT EXISTS personal_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    upbank_account_id TEXT UNIQUE NOT NULL, -- UpBank's account ID
    display_name TEXT NOT NULL,
    account_type TEXT NOT NULL, -- "SAVER", "TRANSACTIONAL", etc.
    ownership_type TEXT, -- "INDIVIDUAL", "JOINT", etc.
    balance_cents INTEGER NOT NULL DEFAULT 0,
    balance_currency_code TEXT NOT NULL DEFAULT 'AUD',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Personal bank transactions (from UpBank API)
CREATE TABLE IF NOT EXISTS personal_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    upbank_transaction_id TEXT UNIQUE NOT NULL, -- UpBank's transaction ID
    account_id UUID NOT NULL REFERENCES personal_accounts(id) ON DELETE CASCADE,

    -- Transaction details
    description TEXT NOT NULL,
    message TEXT, -- Additional transaction message
    amount_cents INTEGER NOT NULL, -- Positive for credits, negative for debits
    currency_code TEXT NOT NULL DEFAULT 'AUD',

    -- Timing
    transaction_date TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    settled_at TIMESTAMP WITH TIME ZONE,

    -- Transaction metadata
    status TEXT NOT NULL DEFAULT 'SETTLED', -- HELD, SETTLED
    is_categorizable BOOLEAN DEFAULT true,
    hold_info JSONB, -- For pending transactions
    round_up JSONB, -- Round up information if applicable
    cashback JSONB, -- Cashback information if applicable

    -- UpBank categorization
    upbank_category_id TEXT,
    upbank_parent_category_id TEXT,

    -- Custom categorization (for personal finance tracking)
    personal_category TEXT,
    personal_subcategory TEXT,
    tags TEXT[], -- Array of custom tags

    -- Notes and classification
    notes TEXT,
    is_business_related BOOLEAN DEFAULT FALSE,
    is_tax_deductible BOOLEAN DEFAULT FALSE,

    -- Raw UpBank data (for reference and future API changes)
    raw_data JSONB,

    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- UpBank categories reference table
CREATE TABLE IF NOT EXISTS upbank_categories (
    id TEXT PRIMARY KEY, -- UpBank category ID
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
    file_path TEXT NOT NULL, -- Supabase storage path
    file_type TEXT,
    file_size INTEGER,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_personal_transactions_account_id ON personal_transactions(account_id);
CREATE INDEX IF NOT EXISTS idx_personal_transactions_date ON personal_transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_personal_transactions_amount ON personal_transactions(amount_cents);
CREATE INDEX IF NOT EXISTS idx_personal_transactions_category ON personal_transactions(personal_category);
CREATE INDEX IF NOT EXISTS idx_personal_transactions_upbank_id ON personal_transactions(upbank_transaction_id);
CREATE INDEX IF NOT EXISTS idx_personal_accounts_upbank_id ON personal_accounts(upbank_account_id);

-- RLS Policies (Row Level Security)
ALTER TABLE personal_accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE personal_transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE upbank_categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE personal_finance_categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE transaction_attachments ENABLE ROW LEVEL SECURITY;

-- Basic RLS policies (adjust based on your authentication setup)
CREATE POLICY "Harrison can manage his accounts" ON personal_accounts
    FOR ALL USING (true); -- Adjust when you add user auth

CREATE POLICY "Harrison can manage his transactions" ON personal_transactions
    FOR ALL USING (true); -- Adjust when you add user auth

CREATE POLICY "Harrison can manage categories" ON personal_finance_categories
    FOR ALL USING (true);

CREATE POLICY "Harrison can manage attachments" ON transaction_attachments
    FOR ALL USING (true);

CREATE POLICY "Anyone can read upbank categories" ON upbank_categories
    FOR SELECT USING (true);

-- Update triggers for timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_personal_accounts_updated_at
    BEFORE UPDATE ON personal_accounts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_personal_transactions_updated_at
    BEFORE UPDATE ON personal_transactions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Sample personal finance categories
INSERT INTO personal_finance_categories (name, is_expense, is_tax_deductible) VALUES
('Income', FALSE, FALSE),
('Business Income', FALSE, FALSE),
('Investment Income', FALSE, FALSE),
('Salary/Wages', FALSE, FALSE),

-- Expense categories
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
('Other', TRUE, FALSE);

-- Comments for documentation
COMMENT ON TABLE personal_accounts IS 'Personal bank accounts synced from UpBank API';
COMMENT ON TABLE personal_transactions IS 'Personal bank transactions synced from UpBank API with custom categorization';
COMMENT ON TABLE upbank_categories IS 'Reference table for UpBank''s transaction categories';
COMMENT ON TABLE personal_finance_categories IS 'Custom personal finance categories for better tracking';
COMMENT ON TABLE transaction_attachments IS 'File attachments for transactions (receipts, invoices, etc.)';

COMMENT ON COLUMN personal_transactions.amount_cents IS 'Amount in cents - positive for credits (money in), negative for debits (money out)';
COMMENT ON COLUMN personal_transactions.raw_data IS 'Complete UpBank API response for this transaction';
COMMENT ON COLUMN personal_transactions.is_business_related IS 'Flag for transactions related to MOKAI/MOK HOUSE business';
