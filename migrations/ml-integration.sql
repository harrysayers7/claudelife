-- ML Integration for UpBank Transactions
-- Adds AI categorization, business expense detection, and prediction functions

-- Add ML-related columns to personal_transactions
ALTER TABLE personal_transactions
ADD COLUMN IF NOT EXISTS ai_category TEXT,
ADD COLUMN IF NOT EXISTS ai_confidence DECIMAL(3,2),
ADD COLUMN IF NOT EXISTS ml_features JSONB;

-- Business keyword matching table
CREATE TABLE IF NOT EXISTS business_keywords (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    keyword TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL, -- e.g., "Business Subscription", "Professional Services"
    is_tax_deductible BOOLEAN DEFAULT TRUE,
    confidence_boost DECIMAL(3,2) DEFAULT 0.1, -- How much to boost confidence when matched
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default business keywords
INSERT INTO business_keywords (keyword, category, is_tax_deductible) VALUES
('Setapp', 'Business Subscription', TRUE),
('Adobe', 'Business Software', TRUE),
('AWS', 'Cloud Services', TRUE),
('Google Cloud', 'Cloud Services', TRUE),
('Digital Ocean', 'Cloud Services', TRUE),
('Heroku', 'Cloud Services', TRUE),
('GitHub', 'Development Tools', TRUE),
('Linear', 'Project Management', TRUE),
('Notion', 'Productivity Software', TRUE),
('Slack', 'Business Communication', TRUE),
('Zoom', 'Business Communication', TRUE),
('Office 365', 'Business Software', TRUE),
('Microsoft 365', 'Business Software', TRUE),
('Xero', 'Accounting Software', TRUE),
('QuickBooks', 'Accounting Software', TRUE),
('Canva Pro', 'Design Tools', TRUE),
('Figma', 'Design Tools', TRUE)
ON CONFLICT (keyword) DO NOTHING;

-- ML prediction function for transaction categorization
-- This is a placeholder that can be replaced with actual MindsDB integration
CREATE OR REPLACE FUNCTION predict_transaction_category(
    p_amount INTEGER,
    p_description TEXT,
    p_vendor_name TEXT DEFAULT NULL
)
RETURNS TABLE (
    category TEXT,
    confidence DECIMAL(3,2),
    is_business BOOLEAN
) AS $$
BEGIN
    -- Check for business keywords first
    IF EXISTS (
        SELECT 1 FROM business_keywords
        WHERE LOWER(p_description) LIKE '%' || LOWER(keyword) || '%'
    ) THEN
        RETURN QUERY
        SELECT
            bk.category,
            0.95::DECIMAL(3,2) as confidence,
            TRUE as is_business
        FROM business_keywords bk
        WHERE LOWER(p_description) LIKE '%' || LOWER(bk.keyword) || '%'
        LIMIT 1;
        RETURN;
    END IF;

    -- Fallback rules based on amount and description patterns
    -- Negative amounts are expenses, positive are income
    IF p_amount < 0 THEN
        -- Expense categorization rules
        IF LOWER(p_description) LIKE '%uber%' OR LOWER(p_description) LIKE '%taxi%' THEN
            RETURN QUERY SELECT 'Transport'::TEXT, 0.7::DECIMAL(3,2), FALSE::BOOLEAN;
        ELSIF LOWER(p_description) LIKE '%woolworths%' OR LOWER(p_description) LIKE '%coles%' THEN
            RETURN QUERY SELECT 'Groceries'::TEXT, 0.7::DECIMAL(3,2), FALSE::BOOLEAN;
        ELSIF LOWER(p_description) LIKE '%spotify%' OR LOWER(p_description) LIKE '%netflix%' THEN
            RETURN QUERY SELECT 'Entertainment'::TEXT, 0.7::DECIMAL(3,2), FALSE::BOOLEAN;
        ELSE
            RETURN QUERY SELECT 'Uncategorized'::TEXT, 0.3::DECIMAL(3,2), FALSE::BOOLEAN;
        END IF;
    ELSE
        -- Income categorization
        RETURN QUERY SELECT 'Income'::TEXT, 0.7::DECIMAL(3,2), FALSE::BOOLEAN;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Function to automatically categorize transactions
CREATE OR REPLACE FUNCTION auto_categorize_transaction()
RETURNS TRIGGER AS $$
DECLARE
    prediction RECORD;
BEGIN
    -- Get ML prediction for this transaction
    SELECT * INTO prediction
    FROM predict_transaction_category(
        NEW.amount_cents,
        NEW.description,
        NULL -- vendor name if available
    )
    LIMIT 1;

    -- Apply prediction to transaction
    IF prediction IS NOT NULL THEN
        NEW.ai_category := prediction.category;
        NEW.ai_confidence := prediction.confidence;
        NEW.is_business_related := prediction.is_business;

        -- Auto-flag tax deductible if business and high confidence
        IF prediction.is_business AND prediction.confidence >= 0.8 THEN
            NEW.is_tax_deductible := TRUE;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for auto-categorization on insert
DROP TRIGGER IF EXISTS auto_categorize_on_insert ON personal_transactions;
CREATE TRIGGER auto_categorize_on_insert
    BEFORE INSERT ON personal_transactions
    FOR EACH ROW
    EXECUTE FUNCTION auto_categorize_transaction();

-- Function to recategorize existing transactions
CREATE OR REPLACE FUNCTION recategorize_all_transactions()
RETURNS INTEGER AS $$
DECLARE
    updated_count INTEGER := 0;
    tx RECORD;
    prediction RECORD;
BEGIN
    FOR tx IN SELECT * FROM personal_transactions WHERE ai_category IS NULL
    LOOP
        -- Get prediction
        SELECT * INTO prediction
        FROM predict_transaction_category(
            tx.amount_cents,
            tx.description,
            NULL
        )
        LIMIT 1;

        IF prediction IS NOT NULL THEN
            UPDATE personal_transactions
            SET
                ai_category = prediction.category,
                ai_confidence = prediction.confidence,
                is_business_related = prediction.is_business,
                is_tax_deductible = CASE
                    WHEN prediction.is_business AND prediction.confidence >= 0.8 THEN TRUE
                    ELSE is_tax_deductible
                END
            WHERE id = tx.id;

            updated_count := updated_count + 1;
        END IF;
    END LOOP;

    RETURN updated_count;
END;
$$ LANGUAGE plpgsql;

-- Indexes for ML features
CREATE INDEX IF NOT EXISTS idx_personal_transactions_ai_category ON personal_transactions(ai_category);
CREATE INDEX IF NOT EXISTS idx_personal_transactions_ai_confidence ON personal_transactions(ai_confidence);
CREATE INDEX IF NOT EXISTS idx_personal_transactions_is_business ON personal_transactions(is_business_related);

-- Comments for documentation
COMMENT ON COLUMN personal_transactions.ai_category IS 'ML-predicted transaction category';
COMMENT ON COLUMN personal_transactions.ai_confidence IS 'Confidence score for AI prediction (0.00-1.00)';
COMMENT ON COLUMN personal_transactions.ml_features IS 'Feature vector used for ML prediction';
COMMENT ON FUNCTION predict_transaction_category IS 'Predicts transaction category using ML or rule-based logic';
COMMENT ON FUNCTION auto_categorize_transaction IS 'Trigger function to automatically categorize new transactions';
COMMENT ON FUNCTION recategorize_all_transactions IS 'Batch recategorize all uncategorized transactions';

-- Grant permissions
GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO service_role;
