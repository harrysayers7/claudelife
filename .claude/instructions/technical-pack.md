# Technical & Infrastructure Pack

<!-- PACK_HASH: 74e1acec9ae4ba4bfdb491f16ce36715 -->
<!-- LAST_UPDATED: 2025-09-24T01:05:29.070Z -->

**Load when**: Keywords detected - "MCP", "database", "supabase", "API", "FastAPI", "infrastructure", "server", "docker", "n8n", "FastMCP"

## Supabase Database

# Supabase Database Schema




**Project ID**: `gshsshaodoyttdxippwx`
**Purpose**: AI-powered financial management system for Australian business entities

## Schema Summary

**Tables**: 13 total
**Last Sync**: 2025-09-22T11:06:45.728Z


### Core Financial
- **entities** (3 records) - No description
- **accounts** (52 records) - No description
- **bank_accounts** (3 records) - No description
- **contacts** (2 records) - No description

### Transaction Management
- **transactions** (1 records) - No description
- **transaction_lines** (0 records) - No description
- **invoices** (6 records) - No description

### AI/ML System
- **ml_models** (7 records) - No description
- **ai_predictions** (0 records) - No description
- **ai_insights** (0 records) - No description
- **anomaly_detections** (0 records) - No description
- **categorization_rules** (3 records) - No description
- **cash_flow_forecasts** (0 records) - No description

## Detailed Table Information

### entities

**Rows**: 3
**Columns**: 0

### accounts

**Rows**: 52
**Columns**: 0

### bank_accounts

**Rows**: 3
**Columns**: 0

### contacts

**Rows**: 2
**Columns**: 0

### transactions

**Rows**: 1
**Columns**: 0

### transaction_lines

**Rows**: 0
**Columns**: 0

### invoices

**Rows**: 6
**Columns**: 0

### ml_models

**Rows**: 7
**Columns**: 0

### ai_predictions

**Rows**: 0
**Columns**: 0

### ai_insights

**Rows**: 0
**Columns**: 0

### anomaly_detections

**Rows**: 0
**Columns**: 0

### categorization_rules

**Rows**: 3
**Columns**: 0

### cash_flow_forecasts

**Rows**: 0
**Columns**: 0

### Database Purpose

# Supabase Financial System - Business Purpose

## System Overview

**AI-Powered Financial Management System** for Indigenous-owned Australian technology consultancies with predictive analytics and compliance automation.

## Primary Business Entities

### MOK HOUSE PTY LTD
- **Type**: Indigenous-owned consultancy (ABN: 38690628212)
- **Focus**: Music business, creative services
- **Projects**: Repco marketing campaigns, Nintendo entertainment projects
- **Compliance**: Supply Nation certified, Indigenous procurement eligible

### MOKAI PTY LTD
- **Type**: Indigenous-owned technology consultancy
- **Focus**: Cybersecurity, GRC, IRAP assessments
- **Target Market**: Government and enterprise organizations
- **Value Proposition**: Single accountable partner for cyber expertise

### Harrison Robert Sayers
- **Type**: Sole trader
- **Services**: Individual consulting, music production
- **Projects**: DiDi flute introduction, personal music work
- **Role**: Owner/CEO of both companies

## Business Requirements

### Multi-Entity Management
- **Separate P&L** for each entity
- **Cross-entity projects** with proper attribution
- **Compliance tracking** per entity type
- **Consolidated reporting** for business overview

### Project-Based Accounting
- **Client attribution**: DiDi, Repco, Nintendo projects
- **Revenue tracking** by project and entity
- **Cost allocation** across business units
- **Profitability analysis** per client/project

### Australian Compliance
- **GST management** with quarterly reporting
- **Indigenous business** documentation and certification
- **ABN/ACN tracking** for all entities
- **Payment terms** and credit management

## AI/ML Business Objectives

### Predictive Cash Flow
- **Payment prediction** for outstanding invoices
- **Cash flow forecasting** 30-90 days ahead
- **Risk assessment** for late payments
- **Working capital optimization**

### Automated Categorization
- **Expense classification** using transaction patterns
- **Project attribution** from invoice descriptions
- **Vendor categorization** and risk scoring
- **Tax deduction optimization**

### Business Intelligence
- **Performance insights** across entities and projects
- **Cost-saving opportunities** identification
- **Revenue optimization** recommendations
- **Compliance monitoring** and alerts

## Workflow Integration

### Invoice Processing
1. **PDF Receipt** → AI extraction (vendor, amount, PO, project)
2. **Auto-categorization** → Account assignment and tax treatment
3. **Payment prediction** → Cash flow impact assessment
4. **Project attribution** → Client profitability tracking

### Transaction Management
1. **Bank import** → Transaction creation and matching
2. **AI categorization** → Chart of accounts assignment
3. **Project allocation** → Business unit attribution
4. **Anomaly detection** → Unusual pattern alerts

### Financial Reporting
1. **Real-time dashboards** → Entity and project performance
2. **Predictive analytics** → Forward-looking insights
3. **Compliance reports** → GST, indigenous business status
4. **Strategic insights** → Growth opportunities and risks

## Compliance Framework

### Indigenous Business Requirements
- **Supply Nation certification** maintenance
- **IPP eligibility** documentation
- **Direct procurement** qualification
- **Minority business** reporting

### Tax Compliance
- **Quarterly GST** calculation and filing
- **Income tax** optimization across entities
- **Deduction maximization** through proper categorization
- **Audit trail** maintenance

### Financial Controls
- **Segregation of duties** across entities
- **Approval workflows** for large expenses
- **Reconciliation processes** for all accounts
- **Risk management** through predictive analytics

## Success Metrics

### Financial Performance
- **Cash flow predictability** (85%+ accuracy)
- **Payment collection** optimization (reduce days outstanding)
- **Cost categorization** accuracy (95%+ automated)
- **Profitability visibility** per project and entity

### Operational Efficiency
- **Invoice processing time** reduction (minutes vs hours)
- **Compliance automation** (minimal manual intervention)
- **Anomaly detection** response time
- **Reporting automation** (real-time vs monthly)

### Business Growth Support
- **Revenue trend analysis** across clients and projects
- **Cost optimization** through pattern recognition
- **Strategic insights** for business development
- **Risk mitigation** through predictive analytics

## Technology Stack Integration

### Core Systems
- **Supabase** (PostgreSQL) - Primary financial database
- **MindsDB** - AI/ML prediction engine
- **OpenAI** - Document processing and insights
- **Up Bank** - Transaction import and reconciliation

### Business Applications
- **Invoice parsing** - PDF to structured data
- **Bank reconciliation** - Automated transaction matching
- **Financial reporting** - Real-time dashboards
- **Compliance monitoring** - Automated alerts and reports

### ML Pipeline

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

## MCP Server Infrastructure

```json
{
  "mcpServers": {
    "notion": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@notionhq/notion-mcp-server"
      ],
      "env": {
        "NOTION_TOKEN": "$NOTION_TOKEN"
      }
    },
    "supabase": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@supabase/mcp-server-supabase@latest",
        "--access-token",
        "$SUPABASE_ACCESS_TOKEN"
      ]
    },
    "task-master-ai": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "--package=task-master-ai",
        "task-master-ai"
      ],
      "env": {
        "ANTHROPIC_API_KEY": "$ANTHROPIC_API_KEY",
        "PERPLEXITY_API_KEY": "$PERPLEXITY_API_KEY",
        "OPENAI_API_KEY": "$OPENAI_API_KEY",
        "GOOGLE_API_KEY": "$GOOGLE_API_KEY",
        "XAI_API_KEY": "$XAI_API_KEY",
        "OPENROUTER_API_KEY": "$OPENROUTER_API_KEY",
        "MISTRAL_API_KEY": "$MISTRAL_API_KEY",
        "AZURE_OPENAI_API_KEY": "$AZURE_OPENAI_API_KEY",
        "OLLAMA_API_KEY": "$OLLAMA_API_KEY"
      }
    },
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "$GITHUB_PERSONAL_ACCESS_TOKEN"
      }
    },
    "memory": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ],
      "env": {
        "MEMORY_FILE_PATH": "/Users/harrysayers/.cursor/memory.json"
      }
    },
    "shadcn-ui": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@jpisnice/shadcn-ui-mcp-server",
        "--github-api-key",
        "$GITHUB_PERSONAL_ACCESS_TOKEN"
      ]
    },
    "exa": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "exa-mcp-server"
      ],
      "env": {
        "EXA_API_KEY": "$EXA_API_KEY"
      }
    },
    "n8n": {
      "type": "stdio",
      "command": "node",
      "args": [
        "/Users/harrysayers/n8n-mcp/dist/mcp/index.js"
      ],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error",
        "DISABLE_CONSOLE_OUTPUT": "true",
        "N8N_API_URL": "https://n8n.sayers.app",
        "N8N_API_KEY": "$N8N_API_KEY"
      }
    },
    "awesome-n8n-templates": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://gitmcp.io/enescingoz/awesome-n8n-templates"
      ]
    },
    "graphiti-personal": {
      "type": "stdio",
      "command": "/opt/homebrew/bin/uv",
      "args": [
        "run",
        "--isolated",
        "--directory",
        "/Users/harrysayers/Developer/claudelife/graphiti_mcp_server",
        "--project",
        ".",
        "graphiti_mcp_server.py",
        "--transport",
        "stdio",
        "--group-id",
        "personal"
      ],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "neo4j",
        "OPENAI_API_KEY": "$OPENAI_API_KEY",
        "MODEL_NAME": "gpt-4o-mini",
        "GRAPHITI_TELEMETRY_ENABLED": "false"
      }
    },
    "graphiti-finance": {
      "type": "stdio",
      "command": "/opt/homebrew/bin/uv",
      "args": [
        "run",
        "--isolated",
        "--directory",
        "/Users/harrysayers/Developer/claudelife/graphiti_mcp_server",
        "--project",
        ".",
        "graphiti_mcp_server.py",
        "--transport",
        "stdio",
        "--group-id",
        "finance"
      ],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "neo4j",
        "OPENAI_API_KEY": "$OPENAI_API_KEY",
        "MODEL_NAME": "gpt-4o-mini",
        "GRAPHITI_TELEMETRY_ENABLED": "false"
      }
    },
    "graphiti-mokai": {
      "type": "stdio",
      "command": "/opt/homebrew/bin/uv",
      "args": [
        "run",
        "--isolated",
        "--directory",
        "/Users/harrysayers/Developer/claudelife/graphiti_mcp_server",
        "--project",
        ".",
        "graphiti_mcp_server.py",
        "--transport",
        "stdio",
        "--group-id",
        "mokai"
      ],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "neo4j",
        "OPENAI_API_KEY": "$OPENAI_API_KEY",
        "MODEL_NAME": "gpt-4o-mini",
        "GRAPHITI_TELEMETRY_ENABLED": "false"
      }
    },
    "graphiti-mok-house": {
      "type": "stdio",
      "command": "/opt/homebrew/bin/uv",
      "args": [
        "run",
        "--isolated",
        "--directory",
        "/Users/harrysayers/Developer/claudelife/graphiti_mcp_server",
        "--project",
        ".",
        "graphiti_mcp_server.py",
        "--transport",
        "stdio",
        "--group-id",
        "mok-house"
      ],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "neo4j",
        "OPENAI_API_KEY": "$OPENAI_API_KEY",
        "MODEL_NAME": "gpt-4o-mini",
        "GRAPHITI_TELEMETRY_ENABLED": "false"
      }
    },
    "graphiti-ai-brain": {
      "type": "stdio",
      "command": "/opt/homebrew/bin/uv",
      "args": [
        "run",
        "--isolated",
        "--directory",
        "/Users/harrysayers/Developer/claudelife/graphiti_mcp_server",
        "--project",
        ".",
        "graphiti_mcp_server.py",
        "--transport",
        "stdio",
        "--group-id",
        "ai-brain"
      ],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "neo4j",
        "OPENAI_API_KEY": "$OPENAI_API_KEY",
        "MODEL_NAME": "gpt-4o-mini",
        "GRAPHITI_TELEMETRY_ENABLED": "false"
      }
    },
    "graphiti-claudelife": {
      "type": "stdio",
      "command": "/opt/homebrew/bin/uv",
      "args": [
        "run",
        "--isolated",
        "--directory",
        "/Users/harrysayers/Developer/claudelife/graphiti_mcp_server",
        "--project",
        ".",
        "graphiti_mcp_server.py",
        "--transport",
        "stdio",
        "--group-id",
        "claudelife"
      ],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "neo4j",
        "OPENAI_API_KEY": "$OPENAI_API_KEY",
        "MODEL_NAME": "gpt-4o-mini",
        "GRAPHITI_TELEMETRY_ENABLED": "false"
      }
    },
    "context7": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@upstash/context7-mcp"
      ],
      "env": {
        "CONTEXT7_API_KEY": "$CONTEXT7_API_KEY"
      }
    },
    "upbank": {
      "type": "stdio",
      "command": "/Users/harrysayers/Developer/claudelife/.mcp/fastmcp-env/bin/python",
      "args": [
        "/Users/harrysayers/Developer/claudelife/.mcp/upbank_server.py"
      ],
      "env": {
        "UPBANK_API_TOKEN": "$UPBANK_API_TOKEN",
        "UPBANK_API_BASE_URL": "https://api.up.com.au/api/v1"
      }
    },
    "fastmcp-brain": {
      "type": "stdio",
      "command": "/Users/harrysayers/Developer/claudelife/.mcp/fastmcp-env/bin/python",
      "args": [
        "/Users/harrysayers/Developer/claudelife/.mcp/fastmcp_server.py"
      ],
      "env": {}
    },
    "claudelife-business-api": {
      "type": "sse",
      "url": "http://localhost:8001/mcp",
      "env": {}
    },
    "claudelife-financial-api": {
      "type": "sse",
      "url": "http://localhost:8002/mcp",
      "env": {
        "SUPABASE_URL": "$SUPABASE_URL",
        "SUPABASE_ANON_KEY": "$SUPABASE_ANON_KEY",
        "SUPABASE_DB_HOST": "db.gshsshaodoyttdxippwx.supabase.co",
        "SUPABASE_DB_PORT": "6543",
        "SUPABASE_DB_NAME": "postgres",
        "SUPABASE_DB_USER": "postgres.gshsshaodoyttdxippwx",
        "SUPABASE_DB_PASSWORD": "$SUPABASE_DB_PASSWORD"
      }
    },
    "mindsdb": {
      "type": "sse",
      "url": "http://localhost:47334/mcp/sse",
      "env": {}
    },
    "docker": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "docker-mcp"
      ],
      "env": {}
    },
    "executeautomation-playwright-server": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@executeautomation/playwright-mcp-server"
      ]
    }
  }
}
```

## Server Infrastructure

- **Primary Server**: 134.199.159.190 (sayers-server)
- **Services**: n8n automation, Supabase database, Docker containers
- **Platform**: Ubuntu, 4 CPU, 7.8GB RAM
