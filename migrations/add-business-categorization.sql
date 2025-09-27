-- Add business categorization columns to personal_transactions
-- These support the enhanced business expense detection and ML categorization

ALTER TABLE personal_transactions
ADD COLUMN IF NOT EXISTS business_category TEXT,
ADD COLUMN IF NOT EXISTS business_subcategory TEXT;

-- Add index for business category queries
CREATE INDEX IF NOT EXISTS idx_personal_transactions_business_category
ON personal_transactions(business_category);

-- Comments for documentation
COMMENT ON COLUMN personal_transactions.business_category IS 'Business expense category (e.g., Software & Tools, Professional Services)';
COMMENT ON COLUMN personal_transactions.business_subcategory IS 'Business expense subcategory for detailed tracking';
