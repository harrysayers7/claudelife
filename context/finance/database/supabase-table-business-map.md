# Supabase Table Business Context Map

**Last Updated**: 2025-10-20
**Purpose**: Business context for all Supabase tables to enable intelligent querying and data interpretation

---

## Entity Mapping

### Primary Business Entities

| Entity Name | UUID | ABN | Type | Primary Use |
|-------------|------|-----|------|-------------|
| **Harrison Robert Sayers** | `bdea5242-9627-43c1-a367-1990caa939f1` | 89 184 087 850 | Sole Trader | Personal finances, individual consulting, music production |
| **MOK HOUSE PTY LTD** | `550e8400-e29b-41d4-a716-446655440002` | 38690628212 | Company | Music business, creative services, Repco/Nintendo projects |
| **MOKAI PTY LTD** | `550e8400-e29b-41d4-a716-446655440001` | 12345678901 | Company | Cybersecurity, GRC, IRAP assessments |

---

## Table-by-Table Business Context

### Core Financial Tables

#### **invoices** (31 rows)
- **Entity Ownership**: Shared across all entities
- **Business Context**:
  - **Before Repco project**: Harrison's sole trader ABN invoices
  - **From Repco onwards**: MOK HOUSE PTY LTD invoices
- **Use Cases**:
  - Track receivables for MOK HOUSE projects (Repco, Nintendo)
  - Historical sole trader invoicing
- **Query Context**: When filtering by entity, check date ranges:
  - Pre-Repco → Harrison (`bdea5242-9627-43c1-a367-1990caa939f1`)
  - Post-Repco → MOK HOUSE (`550e8400-e29b-41d4-a716-446655440002`)

#### **transactions** (1 row)
- **Entity Ownership**: Unknown
- **Business Context**: Likely deprecated, could be deleted
- **Use Cases**: None identified
- **Status**: ⚠️ Under review for deletion

#### **contacts** (3 rows)
- **Entity Ownership**: Shared between MOK HOUSE and personal; MOKAI is separated
- **Business Context**:
  - MOK HOUSE clients/vendors can overlap with personal contacts
  - MOKAI contacts are kept separate (different client base)
- **Use Cases**:
  - MOK HOUSE: Music industry contacts, creative project clients
  - Personal: Individual network, sole trader clients
  - MOKAI: Government/enterprise cybersecurity clients (isolated)

---

### Personal Finance Tables

#### **personal_transactions** (261 rows)
- **Entity Ownership**: Harrison Robert Sayers (sole trader ABN: 89 184 087 850)
- **Business Context**:
  - Source: UpBank personal account
  - Mix of personal and business transactions
  - Tracks daily spending from UpBank "Spending" account
- **Use Cases**:
  - Personal expense tracking
  - Business expense categorization for sole trader tax deductions
  - Cash flow monitoring
- **Important**: Contains both personal and business data - categorization needed

#### **personal_accounts** (4 rows)
- **Entity Ownership**: Harrison Robert Sayers
- **Business Context**:
  - UpBank account structure
  - Main account: "Spending" (active transactions)
  - Savings accounts: "Greece", "Crypto" (not used for transactions)
- **Use Cases**:
  - Track UpBank account balances
  - Separate spending from savings
- **Important**: Savings accounts (Greece, Crypto) are balance tracking only, not transaction logs

---

### Tax & Compliance Tables (Not Set Up Yet)

#### **trust_distributions** (0 rows)
- **Status**: ⚠️ Not properly set up, ignore for now
- **Future Use**: Trust distribution tracking (if/when implemented)

#### **crypto_assets** (0 rows)
- **Status**: ⚠️ Not set up yet, ignore
- **Future Use**: Cryptocurrency holdings tracking

#### **crypto_transactions** (0 rows)
- **Status**: ⚠️ Not set up yet, ignore
- **Future Use**: Crypto buy/sell/transfer tracking

#### **gst_threshold_monitoring** (0 rows)
- **Status**: ⚠️ Not properly set up
- **Future Use**: Australian GST threshold tracking for entities

---

### AI/ML Tables (Intended for MindsDB - Not Set Up Yet)

#### **ml_models** (7 rows)
- **Status**: ⚠️ Not properly set up yet
- **Future Use**: MindsDB model registry

#### **ai_predictions** (0 rows)
- **Status**: ⚠️ Intended for MindsDB, not set up
- **Future Use**: AI prediction storage

#### **categorization_rules** (3 rows)
- **Status**: ⚠️ Not properly set up yet
- **Future Use**: Transaction categorization rules for ML

---

### Sync Infrastructure Tables

#### **sync_sessions** (11 rows)
- **Business Context**: Tracks UpBank → Supabase sync sessions for `personal_transactions`
- **Use Cases**: Monitor sync health, detect sync issues

#### **recurring_transactions** (26 rows)
- **Entity Ownership**: Mix of personal and business
- **Use Cases**: Track subscription services, recurring bills

---

## Project Attribution Context

### MOK HOUSE Projects
All projects (DiDi, Repco, Nintendo) belong to **MOK HOUSE PTY LTD**.

- **DiDi**: Flute introduction project (historical)
- **Repco**: Marketing campaign project (turning point for invoice entity ownership)
- **Nintendo**: Entertainment project

### MOKAI Projects
None currently identified in database. Future MOKAI projects will be kept separate from MOK HOUSE.

---

## High-Level System Purpose

**Primary Goal**: Track all financial data across Harrison's personal finances and business entities (MOK HOUSE, MOKAI), with crypto tracking and ML-powered categorization planned for future.

**Data Domains**:
1. **Personal Finance**: UpBank transactions, personal accounts, sole trader income
2. **MOK HOUSE**: Music business invoices, creative project revenue/expenses
3. **MOKAI**: Cybersecurity consulting (separated from personal/MOK HOUSE)
4. **Crypto** (future): Asset tracking and transaction logging
5. **Compliance** (future): GST monitoring, trust distributions

**Integration Points**:
- **UpBank Sync**: Automated import to `personal_transactions`
- **MindsDB** (future): ML categorization and predictions
- **n8n** (existing): Workflow automation for invoice processing

---

## Query Intelligence Guidelines

### Entity-Based Queries
When user asks "Show me MOK HOUSE invoices":
- Filter `invoices` where:
  - `entity_id = '550e8400-e29b-41d4-a716-446655440002'` (post-Repco)
  - OR check date range for pre-Repco Harrison invoices

### Personal vs Business Separation
When user asks "Show me personal transactions":
- Use `personal_transactions` table (all rows)
- Consider adding business categorization filter (future feature)

When user asks "Show me business expenses":
- Could span multiple tables:
  - `personal_transactions` (sole trader business expenses)
  - `invoices` (MOK HOUSE/MOKAI business income)

### Project-Based Queries
When user asks "Show me Repco project data":
- Filter tables by `project` column matching "Repco"
- Should return MOK HOUSE entity data

---

## Data Quality Notes

✅ **High Quality**:
- `entities` (3 rows) - Core business entities well-defined
- `invoices` (31 rows) - Active use, clear entity attribution
- `personal_transactions` (261 rows) - Active UpBank sync
- `contacts` (3 rows) - Small but active

⚠️ **Needs Attention**:
- `transactions` (1 row) - Consider deletion
- ML tables - Intended for MindsDB but not implemented
- Crypto tables - Planned but empty
- Compliance tables - Not properly configured

🚧 **Future Development**:
- MindsDB integration for AI categorization
- Crypto asset tracking
- GST compliance monitoring
- Trust distribution tracking
