-- ========================================
-- ADD ANOMALY SCORE COLUMN
-- Supplementary migration for anomaly detection
-- ========================================

-- Add missing anomaly detection column to personal_transactions
ALTER TABLE personal_transactions
ADD COLUMN IF NOT EXISTS anomaly_score DECIMAL(3,2);

-- Add index for anomaly detection queries
CREATE INDEX IF NOT EXISTS idx_personal_transactions_anomaly_score
ON personal_transactions(anomaly_score) WHERE anomaly_score > 0.5;

-- Add comment
COMMENT ON COLUMN personal_transactions.anomaly_score IS 'ML-generated anomaly detection score (0.00-1.00)';

-- Migration complete
SELECT 'Anomaly score column added successfully!' as status;
