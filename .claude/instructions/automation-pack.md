# Automation & Workflow Pack

<!-- PACK_HASH: f1f8892db5ecb9946e72b7b3fd0888a4 -->
<!-- LAST_UPDATED: 2025-09-24T01:05:29.075Z -->

**Load when**: Keywords detected - "workflow", "automation", "trigger", "schedule", "integration", "sync", "n8n"

## Active Automations

# n8n Workflows

## Daily Summary
- **Webhook**: http://134.199.159.190:5678/webhook/daily-summary
- **Triggers**: Every day at 5pm or manual
- **Inputs**: None required
- **Output**: Sends email with summary

## Process Inbox
- **Webhook**: http://134.199.159.190:5678/webhook/process-inbox
- **Triggers**: Manual or every 2 hours
- **Inputs**: email_category (optional)
- **Output**: Sorted emails, created tasks

## Context-Aware Task Creation
- **Webhook**: http://134.199.159.190:5678/webhook/smart-task-creation
- **Triggers**: Email, voice note, or manual input
- **Inputs**: task_description, context_hints (business/personal/technical)
- **Logic**:
  - Analyze input for business keywords (Mokai, clients, cybersecurity)
  - Auto-assign to correct project based on context/business/projects.md
  - Set priority based on context/personal/routines.md
- **Output**: Task created in appropriate system with context tags

## Smart Email Processing
- **Webhook**: http://134.199.159.190:5678/webhook/context-email-processor
- **Triggers**: New emails to monitored addresses
- **Inputs**: Email content and sender
- **Logic**:
  - Check sender against context/business/ profiles
  - Route Mokai emails to business workflows
  - Route personal emails based on context/personal/ settings
- **Output**: Categorized, prioritized, and routed appropriately

## Context Sync
- **Webhook**: http://134.199.159.190:5678/webhook/context-sync
- **Triggers**: Daily at 6am
- **Inputs**: None
- **Logic**:
  - Check for updates in /context directory
  - Sync changes to Graphiti memory
  - Update automation rules based on context changes
- **Output**: Updated memory and automation rules

## Financial ML Pipeline

# Supabase ML Pipeline - AI Financial Intelligence

## ML Architecture Overview

**7 Active ML Models** integrated with MindsDB for real-time financial predictions and insights.

## Model Categories

### 1. Transaction Categorization Models
**Purpose**: Automatically classify expenses and income into chart of accounts

**Models**:
- `transaction_categorizer` - Primary classification model
- `expense_classifier` - Specialized expense categorization
- `vendor_classifier` - Vendor-based categorization rules

**Features**:
- Transaction description analysis
- Amount patterns and ranges
- Vendor name matching
- Historical categorization patterns
- Project context integration

**Confidence Thresholds**:
- High confidence (>0.9): Auto-apply categorization
- Medium confidence (0.7-0.9): Suggest with review
- Low confidence (<0.7): Manual categorization required

### 2. Payment Prediction Models
**Purpose**: Forecast invoice payment dates and collection probability

**Models**:
- `payment_predictor` - Payment date forecasting
- `collection_risk_model` - Late payment probability

**Features**:
- Customer payment history
- Invoice amount and terms
- Industry payment patterns
- Seasonal payment trends
- Economic indicators

**Outputs**:
- `predicted_payment_date` - Expected payment date
- `payment_probability` - Likelihood of on-time payment (0-1)
- `collection_risk_score` - Risk of late/non-payment

### 3. Cash Flow Forecasting
**Purpose**: Predict future cash position and working capital needs

**Model**: `cash_flow_forecaster`

**Features**:
- Historical cash flow patterns
- Outstanding invoices and payment predictions
- Recurring expense patterns
- Seasonal business cycles
- Project pipeline and timing

**Outputs**:
- `predicted_inflow/outflow` - Expected cash movements
- `predicted_balance` - Projected account balances
- `confidence_interval_low/high` - Forecast range
- `variance` - Prediction uncertainty

### 4. Anomaly Detection
**Purpose**: Identify unusual transactions and potential fraud

**Model**: `anomaly_detector`

**Anomaly Types**:
- **Amount**: Unusually large/small transactions
- **Frequency**: Unexpected transaction patterns
- **Timing**: Off-schedule payments or receipts
- **Vendor**: New or suspicious vendors
- **Category**: Misclassified transactions
- **Pattern**: Breaks from historical norms

**Severity Levels**:
- **Low**: Minor deviations, investigate if time permits
- **Medium**: Moderate anomalies, review within 24-48 hours
- **High**: Significant deviations, review immediately
- **Critical**: Potential fraud, immediate action required

### 5. Business Insights Generation
**Purpose**: Generate actionable recommendations for financial optimization

**Model**: `insight_generator`

**Insight Types**:
- **Cost Saving**: Identify expense reduction opportunities
- **Revenue Opportunity**: Spot growth potential
- **Risk Warning**: Alert to financial risks
- **Efficiency**: Process improvement suggestions
- **Compliance**: Regulatory adherence recommendations
- **Tax Optimization**: Deduction and timing strategies

**Insight Categories**:
- **Cash Flow**: Liquidity management recommendations
- **Expenses**: Cost optimization opportunities
- **Revenue**: Income enhancement strategies
- **Tax**: Compliance and optimization advice
- **Operations**: Process efficiency improvements

## ML Workflow Integration

### Real-Time Prediction Pipeline

1. **Transaction Ingestion**
   - New transaction → Feature extraction
   - Historical context → Pattern analysis
   - Vendor matching → Risk assessment

2. **Multi-Model Processing**
   - Categorization model → Account assignment
   - Anomaly detection → Risk scoring
   - Pattern analysis → Insight generation

3. **Confidence Assessment**
   - Model agreement → Confidence scoring
   - Historical accuracy → Reliability weighting
   - Human feedback → Continuous learning

4. **Action Triggers**
   - High confidence → Auto-processing
   - Medium confidence → Review queue
   - Low confidence → Manual handling
   - Anomalies → Alert generation

### Batch Processing Workflows

#### Daily Insights Generation
- **Morning**: Cash flow forecast update
- **Midday**: Payment prediction refresh
- **Evening**: Anomaly detection scan
- **Nightly**: Business insights compilation

#### Weekly Analysis
- **Model Performance**: Accuracy assessment and retraining needs
- **Pattern Updates**: New categorization rules based on feedback
- **Risk Assessment**: Vendor and customer risk score updates
- **Compliance Check**: Regulatory adherence monitoring

#### Monthly Optimization
- **Model Retraining**: Full model refresh with new data
- **Feature Engineering**: New predictive features based on patterns
- **Threshold Tuning**: Confidence and alert threshold optimization
- **Business Review**: Strategic insights and recommendations

## Model Performance Metrics

### Categorization Accuracy
- **Target**: >95% automatic categorization accuracy
- **Current**: Tracked in `ml_models.accuracy_score`
- **Feedback Loop**: Human corrections improve model performance

### Payment Prediction Accuracy
- **Target**: 85% payment date accuracy within ±3 days
- **Monitoring**: Compare `predicted_payment_date` vs `paid_on`
- **Calibration**: Confidence scores align with actual accuracy

### Cash Flow Forecast Accuracy
- **Target**: 80% accuracy for 30-day forecasts
- **Validation**: Daily comparison of predicted vs actual balances
- **Improvement**: Seasonal adjustment and pattern recognition

### Anomaly Detection Effectiveness
- **Precision**: Minimize false positives (<10%)
- **Recall**: Catch true anomalies (>90%)
- **Response Time**: Alert generation within 15 minutes

## Human-AI Collaboration

### Feedback Integration
- **Categorization Corrections** → Model retraining data
- **Payment Confirmations** → Prediction accuracy assessment
- **Anomaly Reviews** → False positive reduction
- **Insight Actions** → Recommendation effectiveness tracking

### Learning Mechanisms
- **Active Learning**: Focus on uncertain predictions
- **Transfer Learning**: Apply patterns across similar entities
- **Ensemble Methods**: Combine multiple model predictions
- **Continuous Updates**: Real-time model improvement

### Decision Support
- **Confidence Indicators**: Clear uncertainty communication
- **Explanation Features**: Why predictions were made
- **Alternative Suggestions**: Multiple categorization options
- **Risk Indicators**: Visual risk assessment displays

## MindsDB Integration

### Model Deployment
```sql
-- Example categorization model
CREATE MODEL transaction_categorizer
FROM supabase_integration.transactions
PREDICT ai_category
USING engine = 'lightgbm',
      features = ['description', 'total_amount', 'vendor_name'];
```

### Real-Time Predictions
```sql
-- Get categorization prediction
SELECT ai_category, ai_confidence
FROM transaction_categorizer
WHERE description = 'Office supplies purchase'
  AND total_amount = 150.00;
```

### Batch Processing
```sql
-- Update all uncategorized transactions
UPDATE transactions
SET ai_category = (
  SELECT ai_category
  FROM transaction_categorizer
  WHERE description = transactions.description
),
ai_confidence = (
  SELECT ai_confidence
  FROM transaction_categorizer
  WHERE description = transactions.description
)
WHERE ai_category IS NULL;
```

## Future ML Enhancements

### Advanced Models
- **Time Series Forecasting**: Seasonal pattern recognition
- **Natural Language Processing**: Better description analysis
- **Computer Vision**: Receipt and invoice image processing
- **Reinforcement Learning**: Adaptive recommendation systems

### Business Intelligence
- **Competitive Analysis**: Industry benchmark comparisons
- **Market Trends**: Economic indicator integration
- **Strategic Planning**: Long-term growth modeling
- **Risk Management**: Advanced scenario planning

## UpBank Sync System

Enhanced sync script with error recovery and checkpoint management.

### Implementation Details
```javascript
#!/usr/bin/env node

/**
 * Enhanced UpBank to Supabase Sync Script
 * With comprehensive error handling, recovery, and monitoring
 */

const { createClient } = require('@supabase/supabase-js');
const { v4: uuidv4 } = require('uuid');

// Configuration
const SUPABASE_URL = process.env.SUPABASE_URL || 'https://gshsshaodoyttdxippwx.supabase.co';
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SERVICE_KEY;
const UPBANK_TOKEN = process.env.UPBANK_API_TOKEN;

// Error types
const ErrorTypes = {
  AUTH: 'AUTH_ERROR',
  RATE_LIMIT: 'RATE_LIMIT',
  NETWORK: 'NETWORK_ERROR',
  DATABASE: 'DATABASE_ERROR',
  DATA_INTEGRITY: 'DATA_INTEGRITY',
  CONSTRAINT_VIOLATION: 'CONSTRAINT_VIOLATION',
  UNKNOWN: 'UNKNOWN_ERROR'
};

// Validate environment
if (!SUPABASE_SERVICE_KEY) {
  console.error('❌ SUPABASE_SERVICE_ROLE_KEY environment variable is required');
  process.exit(1);
}

if (!UPBANK_TOKEN) {
  console.error('❌ UPBANK_API_TOKEN environment variable is re
...
```

## Workflow Patterns

### Error Recovery
- Categorized retries (network, data, system errors)
- Checkpoint system for resume capability
- State management via database

### Business Rule Automation
- Keyword matching for business expense detection
- Tax deductibility auto-flagging
- ML prediction threshold routing
