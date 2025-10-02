---
date: "2025-10-02 12:59"
---

# Supabase SAYERS DATA - System Documentation

## Overview

**Project ID**: `gshsshaodoyttdxippwx`
**Project Name**: SAYERS DATA
**Purpose**: AI-powered financial management system for Harrison Robert Sayers' business entities

**System Type**: Multi-entity financial intelligence platform with ML-driven automation, compliance tracking, and predictive analytics.

---

## Business Context

### Managed Entities

#### 1. MOK HOUSE PTY LTD
- **ABN**: 38690628212
- **Type**: Indigenous-owned creative consultancy
- **Focus**: Music business, creative services, sonic branding
- **Key Clients**: Repco, Nintendo, corporate/government buyers
- **Revenue Streams**:
  - MOK Music: Project-based music/sonic branding
  - MOK Studio: Scalable branding, design, content, paid media retainers
- **Compliance**: Supply Nation certified, Indigenous procurement eligible

#### 2. MOKAI PTY LTD
- **Type**: Indigenous-owned technology consultancy
- **Focus**: Cybersecurity services (penetration testing, GRC, IRAP assessments)
- **Target Market**: Government and enterprise organizations
- **Value Proposition**: Direct procurement eligibility via IPP (Indigenous Procurement Policy)
- **Services**: Security assessments, compliance audits, technology solutions

#### 3. Harrison Robert Sayers (Sole Trader)
- **Role**: Owner/CEO of both companies
- **Services**: Individual consulting, music production
- **Projects**: Personal music work, individual consulting engagements

---

## Database Architecture

### Core Financial Tables (7 tables)

#### 1. **entities** (3 records)
**Purpose**: Business entity management (MOK HOUSE, MOKAI, Harrison Sayers)

**Key Fields**:
- Entity identification (ABN, ACN)
- Entity type (PTY LTD, Sole Trader)
- Indigenous business status
- Compliance certifications
- Contact details

#### 2. **accounts** (52 records)
**Purpose**: Chart of accounts - Australian accounting standards

**Structure**:
- Income accounts
- Expense accounts (by category)
- Asset accounts
- Liability accounts
- Equity accounts
- GST tracking accounts

#### 3. **bank_accounts** (3 records)
**Purpose**: Bank account tracking per entity

**Integration**: UpBank API sync for real-time balances

#### 4. **contacts** (2 records)
**Purpose**: Vendors, clients, suppliers

**Relationships**: Links to invoices, payments, projects

---

### Transaction Management Tables (3 tables)

#### 5. **transactions** (1 record)
**Purpose**: General ledger transactions

**Features**:
- Multi-entity support
- Project attribution
- GST calculation
- Audit trail

#### 6. **transaction_lines** (0 records - new system)
**Purpose**: Double-entry accounting line items

**Design**: Links transactions to chart of accounts

#### 7. **invoices** (6 records)
**Purpose**: Receivables and payables tracking

**Key Features**:
- Client/vendor attribution
- Payment terms
- Due date tracking
- Payment prediction integration
- Project/entity assignment

---

### Personal Banking Tables (UpBank Integration)

#### **personal_accounts**
**Purpose**: Personal bank accounts synced from UpBank API

**Fields**:
- `upbank_account_id` - Unique UpBank identifier
- `display_name` - Account name ("Spending", "Savings", etc.)
- `account_type` - SAVER, TRANSACTIONAL
- `balance_cents` - Current balance (real-time sync)
- `ownership_type` - INDIVIDUAL, JOINT

**Sync Frequency**: Automated via GitHub Actions + n8n workflows

#### **personal_transactions**
**Purpose**: Personal bank transactions with AI categorization

**Core Fields**:
- `upbank_transaction_id` - Unique transaction ID
- `description` - Transaction description
- `amount_cents` - Amount (negative = expense, positive = income)
- `transaction_date` - When transaction occurred
- `status` - HELD, SETTLED

**AI/ML Fields**:
- `ai_category` - ML-predicted category
- `ai_confidence` - Confidence score (0.00-1.00)
- `is_business_related` - Auto-detected business expenses
- `is_tax_deductible` - Tax optimization flag
- `ml_features` - Feature vector for predictions

**Custom Fields**:
- `personal_category` / `personal_subcategory` - User overrides
- `tags[]` - Custom transaction tags
- `notes` - Additional context

**Automation**:
- **Trigger**: `auto_categorize_on_insert` - Runs ML categorization on insert
- **Function**: `predict_transaction_category()` - Business keyword matching + ML
- **Confidence Thresholds**:
  - ≥0.90: Auto-apply categorization
  - 0.70-0.89: Suggest with review
  - <0.70: Manual categorization required

#### **business_keywords**
**Purpose**: Keyword-based business expense detection

**Examples**:
- "Setapp" → Business Subscription (Tax Deductible)
- "Adobe" → Business Software (Tax Deductible)
- "AWS" / "Google Cloud" → Cloud Services (Tax Deductible)
- "GitHub" / "Linear" → Development Tools (Tax Deductible)

**Logic**: If transaction description matches keyword → auto-flag as business, boost confidence to 0.95

#### **upbank_categories**
**Purpose**: Reference table for UpBank's built-in categories

#### **personal_finance_categories**
**Purpose**: Custom categorization hierarchy

**Categories**:
- Income (Business Income, Investment Income, Salary/Wages)
- Expenses (Food & Dining, Transport, Shopping, Entertainment, Bills & Utilities, Healthcare, Education, Travel, Business Expenses, Investment, Insurance, Taxes, Savings)

---

### AI/ML System Tables (6 tables)

#### 8. **ml_models** (7 records)
**Purpose**: Model registry and performance tracking

**Active Models**:
1. `transaction_categorizer` - Primary expense/income classification
2. `expense_classifier` - Specialized expense categorization
3. `vendor_classifier` - Vendor-based categorization rules
4. `payment_predictor` - Invoice payment date forecasting
5. `collection_risk_model` - Late payment probability
6. `cash_flow_forecaster` - 30-90 day cash flow predictions
7. `anomaly_detector` - Unusual transaction detection
8. `insight_generator` - Actionable business recommendations

**Metadata**:
- Model type (classification, regression, time series)
- Training date
- Accuracy scores
- Feature importance
- Retraining schedule

#### 9. **ai_predictions** (0 records - ready for production)
**Purpose**: Store all AI predictions for audit and improvement

**Schema**:
- Transaction/invoice ID
- Model used
- Prediction value
- Confidence score
- Actual outcome (for accuracy tracking)
- Feature vector used

#### 10. **ai_insights** (0 records - ready for production)
**Purpose**: Business intelligence recommendations

**Insight Types**:
- **Cost Saving**: Expense reduction opportunities
- **Revenue Opportunity**: Growth potential identification
- **Risk Warning**: Financial risk alerts
- **Efficiency**: Process improvement suggestions
- **Compliance**: Regulatory adherence checks
- **Tax Optimization**: Deduction and timing strategies

**Categories**:
- Cash Flow
- Expenses
- Revenue
- Tax
- Operations

#### 11. **anomaly_detections** (0 records - ready for production)
**Purpose**: Identify unusual transactions and potential fraud

**Anomaly Types**:
- **Amount**: Unusually large/small transactions
- **Frequency**: Unexpected transaction patterns
- **Timing**: Off-schedule payments/receipts
- **Vendor**: New or suspicious vendors
- **Category**: Misclassified transactions
- **Pattern**: Breaks from historical norms

**Severity Levels**:
- **Critical**: Potential fraud, immediate action required
- **High**: Significant deviations, review immediately
- **Medium**: Moderate anomalies, review within 24-48 hours
- **Low**: Minor deviations, investigate if time permits

#### 12. **categorization_rules** (3 records)
**Purpose**: Business logic for transaction categorization

**Rule Types**:
- Keyword matching (vendor name → category)
- Amount patterns (subscription ranges → category)
- Historical patterns (vendor history → likely category)
- Project attribution (client → project → entity)

#### 13. **cash_flow_forecasts** (0 records - ready for production)
**Purpose**: Predictive cash flow modeling

**Forecast Horizon**: 30, 60, 90 days

**Outputs**:
- `predicted_inflow` - Expected incoming payments
- `predicted_outflow` - Expected expenses
- `predicted_balance` - Projected account balances
- `confidence_interval_low/high` - Forecast range
- `variance` - Prediction uncertainty

**Features Used**:
- Historical cash flow patterns
- Outstanding invoices + payment predictions
- Recurring expense patterns
- Seasonal business cycles
- Project pipeline and timing

---

## ML Pipeline Architecture

### Real-Time Prediction Workflow

**1. Transaction Ingestion**
```
New UpBank transaction → Feature extraction → Pattern analysis → Vendor matching
```

**2. Multi-Model Processing**
```
Categorization model → Account assignment
Anomaly detection   → Risk scoring
Pattern analysis    → Insight generation
```

**3. Confidence Assessment**
```
Model agreement        → Confidence scoring
Historical accuracy   → Reliability weighting
Human feedback        → Continuous learning
```

**4. Action Triggers**
```
High confidence (≥0.9)   → Auto-processing
Medium confidence (0.7-0.9) → Review queue
Low confidence (<0.7)    → Manual handling
Anomalies detected       → Alert generation
```

### Batch Processing Schedule

#### Daily Tasks
- **Morning**: Cash flow forecast update
- **Midday**: Payment prediction refresh
- **Evening**: Anomaly detection scan
- **Nightly**: Business insights compilation

#### Weekly Tasks
- **Model Performance**: Accuracy assessment and retraining needs
- **Pattern Updates**: New categorization rules based on feedback
- **Risk Assessment**: Vendor and customer risk score updates
- **Compliance Check**: Regulatory adherence monitoring

#### Monthly Tasks
- **Model Retraining**: Full model refresh with new data
- **Feature Engineering**: New predictive features based on patterns
- **Threshold Tuning**: Confidence and alert threshold optimization
- **Business Review**: Strategic insights and recommendations

---

## Key Database Functions

### ML Prediction Function
```sql
predict_transaction_category(
    p_amount INTEGER,
    p_description TEXT,
    p_vendor_name TEXT DEFAULT NULL
)
```

**Returns**:
- `category` - Predicted category
- `confidence` - Confidence score (0.00-1.00)
- `is_business` - Business expense flag

**Logic**:
1. Check `business_keywords` table for matches → confidence 0.95
2. Apply pattern-based rules (Uber=Transport, Woolworths=Groceries)
3. Fallback to "Uncategorized" with low confidence

### Auto-Categorization Trigger
```sql
auto_categorize_on_insert
```

**Behavior**: Automatically runs `predict_transaction_category()` on new transactions, applies:
- `ai_category`
- `ai_confidence`
- `is_business_related`
- `is_tax_deductible` (if business + confidence ≥0.8)

### Batch Recategorization
```sql
recategorize_all_transactions()
```

**Purpose**: Recategorize all transactions missing AI categorization

**Use Case**: After adding new business keywords or improving ML model

---

## Business Intelligence Features

### Automated Workflows

#### Invoice Processing
1. **PDF Receipt** → AI extraction (vendor, amount, PO, project)
2. **Auto-categorization** → Account assignment and tax treatment
3. **Payment prediction** → Cash flow impact assessment
4. **Project attribution** → Client profitability tracking

#### Transaction Management
1. **Bank import** (UpBank API) → Transaction creation and matching
2. **AI categorization** → Chart of accounts assignment
3. **Project allocation** → Business unit attribution
4. **Anomaly detection** → Unusual pattern alerts

#### Financial Reporting
1. **Real-time dashboards** → Entity and project performance
2. **Predictive analytics** → Forward-looking insights
3. **Compliance reports** → GST, indigenous business status
4. **Strategic insights** → Growth opportunities and risks

---

## Compliance & Reporting

### Australian Tax Compliance
- **GST Tracking**: Quarterly BAS preparation
- **Income Tax**: Multi-entity tax optimization
- **Deduction Maximization**: ML-driven categorization
- **Audit Trail**: Complete transaction history

### Indigenous Business Requirements
- **Supply Nation Certification**: Maintained per entity
- **IPP Eligibility**: Direct procurement documentation
- **Minority Business Reporting**: Compliance tracking

### Financial Controls
- **Entity Segregation**: Separate P&L per entity
- **Approval Workflows**: Large expense controls
- **Reconciliation**: Automated bank matching
- **Risk Management**: Predictive analytics

---

## Integration Points

### External Systems

#### UpBank API
- **Purpose**: Real-time personal banking sync
- **Tables**: `personal_accounts`, `personal_transactions`
- **Frequency**: Automated via GitHub Actions (daily) + n8n (on-demand)
- **Sync Script**: `scripts/sync-upbank.ts` with enhanced error handling

#### MindsDB
- **Purpose**: AI/ML prediction engine
- **Models**: 7 active models for categorization, forecasting, anomaly detection
- **Integration**: SQL-based model deployment and inference

#### OpenAI
- **Purpose**: Document processing (invoice OCR, receipt parsing)
- **Use Cases**: PDF extraction, natural language insights

#### n8n (134.199.159.190)
- **Purpose**: Workflow automation and orchestration
- **Workflows**: UpBank sync triggers, error recovery, notification systems

---

## Performance Targets

### ML Accuracy Goals
- **Categorization**: >95% automatic accuracy
- **Payment Prediction**: 85% accuracy within ±3 days
- **Cash Flow Forecast**: 80% accuracy for 30-day forecasts
- **Anomaly Detection**: <10% false positives, >90% recall

### Operational Metrics
- **Invoice Processing**: Minutes (vs hours manually)
- **Compliance Automation**: Minimal manual intervention
- **Reporting**: Real-time (vs monthly)
- **Anomaly Response**: 15-minute alert generation

---

## Security & Access Control

### Row Level Security (RLS)
- **Enabled** on all tables
- **Policies**: User-based access (currently Harrison-only)
- **Service Role**: Full permissions for automation scripts

### Data Protection
- **Encryption**: At rest and in transit (Supabase default)
- **Audit Logging**: Complete transaction history
- **Backup**: Automated daily snapshots

---

## Future Enhancements

### Advanced ML Models
- **Time Series Forecasting**: Seasonal pattern recognition
- **NLP**: Better transaction description analysis
- **Computer Vision**: Receipt/invoice image processing
- **Reinforcement Learning**: Adaptive recommendation systems

### Business Intelligence
- **Competitive Analysis**: Industry benchmark comparisons
- **Market Trends**: Economic indicator integration
- **Strategic Planning**: Long-term growth modeling
- **Risk Management**: Advanced scenario planning

### Automation
- **Payment Automation**: Auto-pay approved invoices
- **Compliance Automation**: Auto-generate BAS reports
- **Client Invoicing**: AI-driven invoice generation
- **Project Profitability**: Real-time margin tracking

---

## Technical Notes

### Schema Metadata
- **Last Updated**: 2025-09-22T11:06:45.728Z
- **Total Tables**: 13 (7 core financial + 6 ML/AI)
- **Total Records**: 74 (as of last sync)

### Access Requirements
- **Supabase Access Token**: Required for API operations
- **Environment Variable**: `SUPABASE_ACCESS_TOKEN` or `--access-token` flag

### Related Documentation
- [Supabase ML Pipeline](../context/finance/database/supabase-ml-pipeline.md)
- [Supabase Purpose](../context/finance/database/supabase-purpose.md)
- [Supabase Schema](../context/finance/database/supabase-schema.md)

---

## Quick Reference

**Project ID**: `gshsshaodoyttdxippwx`
**Database**: PostgreSQL (Supabase hosted)
**Primary Use Case**: Multi-entity financial management with AI automation
**Key Feature**: ML-driven transaction categorization and business expense detection
**Integration**: UpBank API, MindsDB, OpenAI, n8n

**Contact**: Harrison Robert Sayers (Owner/CEO)
