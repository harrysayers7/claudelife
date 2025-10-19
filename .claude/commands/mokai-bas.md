# MOKAI PTY LTD - BAS Preparation Support

Prepare Business Activity Statement (BAS) for MOKAI PTY LTD with GST reconciliation, PAYG calculations, and export for tax agent lodgement.

**Arguments**: $ARGUMENTS (e.g., "Q2 2025" or "October 2025" for monthly)

## Entity Details

**MOKAI PTY LTD** (ABN: 12345678901)
- Indigenous-owned technology consultancy
- Cybersecurity services (penetration testing, GRC, IRAP)
- Prime contractor model with subcontractors
- Supply Nation certified
- **GST Status**: Will register immediately when operational

## Instructions

### Step 1: Parse BAS Period

Extract period from `$ARGUMENTS`:
- **Quarterly**: Q1 (Jul-Sep), Q2 (Oct-Dec), Q3 (Jan-Mar), Q4 (Apr-Jun)
- **Monthly**: Specific month and year
- **Default**: Current quarter if no args provided

Determine:
- Start date: First day of period
- End date: Last day of period
- Lodgement deadline: 28 days after period end (or 25th of month following for monthly)

### Step 2: Fetch BAS Data from Supabase

Use `mcp__supabase__execute_sql`:

#### A. GST Collected (Sales/Revenue)
```sql
SELECT
  t.transaction_number,
  t.transaction_date,
  t.description,
  t.total_amount,
  t.gst_amount,
  c.name AS customer_name
FROM transactions t
LEFT JOIN invoices i ON i.transaction_id = t.id
LEFT JOIN contacts c ON c.id = i.contact_id
WHERE t.entity_id = (SELECT id FROM entities WHERE name = 'MOKAI PTY LTD' LIMIT 1)
  AND t.transaction_date >= '[START_DATE]'
  AND t.transaction_date <= '[END_DATE]'
  AND t.gst_amount > 0  -- GST collected on sales
  AND t.status = 'posted'
ORDER BY t.transaction_date;
```

#### B. GST Paid (Purchases/Expenses - Input Tax Credits)
```sql
SELECT
  t.transaction_number,
  t.transaction_date,
  t.description,
  t.total_amount,
  t.gst_amount,
  c.name AS supplier_name
FROM transactions t
LEFT JOIN invoices i ON i.transaction_id = t.id
LEFT JOIN contacts c ON c.id = i.contact_id
WHERE t.entity_id = (SELECT id FROM entities WHERE name = 'MOKAI PTY LTD' LIMIT 1)
  AND t.transaction_date >= '[START_DATE]'
  AND t.transaction_date <= '[END_DATE]'
  AND t.gst_amount < 0  -- GST paid on purchases (input tax credits)
  AND t.status = 'posted'
ORDER BY t.transaction_date;
```

#### C. PAYG Withholding (Contractors/Employees)
```sql
SELECT
  t.transaction_number,
  t.transaction_date,
  t.description,
  t.total_amount,
  c.name AS payee_name,
  c.abn AS payee_abn
FROM transactions t
LEFT JOIN transaction_lines tl ON tl.transaction_id = t.id
LEFT JOIN accounts a ON a.id = tl.account_id
LEFT JOIN contacts c ON c.id = t.contact_id  -- Assuming contact linkage
WHERE t.entity_id = (SELECT id FROM entities WHERE name = 'MOKAI PTY LTD' LIMIT 1)
  AND t.transaction_date >= '[START_DATE]'
  AND t.transaction_date <= '[END_DATE]'
  AND a.account_name ILIKE '%PAYG%'  -- PAYG withholding account
  AND t.status = 'posted'
ORDER BY t.transaction_date;
```

**Note**: If no ABN quoted by contractor, PAYG withholding at 47% required.

#### D. PAYG Instalments (Company Tax Pre-Payment)
```sql
-- Check if MOKAI is required to pay PAYG instalments
-- Based on prior year tax liability and ATO notice
SELECT
  'PAYG Instalment' AS type,
  '[CALCULATED_AMOUNT]' AS amount,
  'Based on ATO instalment notice or prior year tax' AS note
-- This may need manual entry if not tracked in transactions
```

### Step 3: Calculate BAS Figures

#### GST Calculations
```
G1  Total Sales (GST inclusive)           = SUM(sales total_amount)
G2  Export Sales (GST-free)              = $0 (unless international)
G3  Other GST-free Sales                 = $0 (unless charity/education)
G4  Input Taxed Sales                    = $0 (unless financial services)
G5  = G2 + G3 + G4                       (Total non-taxable sales)
G6  = G1 - G5                            (Total taxable sales)
G7  Adjustments                          = $0 (manual adjustments if any)
G8  = G6 + G7                            (Total sales subject to GST)
G9  = G8 ÷ 11                            (GST on sales - 10% of total)

G10 Capital Purchases (GST inclusive)    = SUM(capital purchase total_amount)
G11 Non-Capital Purchases (GST inclusive) = SUM(expense total_amount)
G12 = G10 + G11                          (Total purchases)
G13 Purchases for making input taxed sales = $0
G14 Purchases without GST in price       = $0 (e.g., wages)
G15 Estimated purchases for private use  = $0
G16 = G13 + G14 + G15                    (Total non-creditable purchases)
G17 = G12 - G16                          (Total creditable purchases)
G18 Adjustments                          = $0 (manual adjustments)
G19 = G17 + G18                          (Total purchases with GST credits)
G20 = G19 ÷ 11                           (GST credits - 10% of total)

G21 = G9 - G20                           (GST Payable or Refundable)
     If positive: Amount payable to ATO
     If negative: Refund from ATO
```

#### PAYG Withholding
```
W1  Total salary, wages and other payments = SUM(employee/contractor payments)
W2  Amounts withheld from W1                = SUM(PAYG withholding amounts)
W3  Amounts withheld from other payments    = $0 (unless unusual)
W4  = W2 + W3                               (Total PAYG withheld)
```

#### PAYG Instalments
```
T1  PAYG instalment income                  = Company revenue for period
T2  Instalment rate (from ATO)             = [X]% (from ATO notice)
T3  = T1 × T2                               (PAYG instalment amount)

OR if notional tax method:
T4  Estimated tax on instalment income     = [MANUAL_CALCULATION]
```

**Note**: PAYG instalments only apply if ATO has issued an instalment notice (usually after first profitable year).

### Step 4: Generate BAS Report

```markdown
# MOKAI PTY LTD - BAS Summary
## Period: [Quarter/Month Year]
**ABN**: 12345678901
**GST Registered**: [Yes/No - check registration status]
**Lodgement Due**: [28 days after period end]
**Prepared**: [current date]

---

## GST Calculation

### Sales (GST Collected)
| Date | Description | Customer | Total (inc GST) | GST Amount |
|------|-------------|----------|-----------------|------------|
[List all sales transactions]

**G1 Total Sales**: $[amount]
**G9 GST on Sales**: $[amount] (÷11)

### Purchases (GST Credits)
| Date | Description | Supplier | Total (inc GST) | GST Credit |
|------|-------------|----------|-----------------|------------|
[List all purchase transactions]

**G11 Non-Capital Purchases**: $[amount]
**G20 GST Credits**: $[amount] (÷11)

### GST Summary
```
G9  GST on Sales:          $[amount]
G20 GST Credits:          -$[amount]
────────────────────────────────────
G21 GST Payable/(Refund): $[amount]
```

**Action Required**:
- ✅ If payable: Pay ATO by [due date]
- ✅ If refund: Will be refunded to nominated bank account

---

## PAYG Withholding

### Payments to Contractors/Employees
| Date | Payee | ABN | Payment | PAYG Withheld |
|------|-------|-----|---------|---------------|
[List all contractor/employee payments]

**W4 Total PAYG Withheld**: $[amount]

**Action Required**:
- ✅ Pay withheld amount to ATO by [due date]
- ✅ Ensure payment summaries issued to contractors/employees

**ABN Verification**:
[Flag any contractors without ABN - 47% withholding required]

---

## PAYG Instalments (Company Tax Pre-Payment)

**T1 Instalment Income (Revenue)**: $[amount]
**T2 Instalment Rate (ATO)**: [X]% [or "Not applicable - no ATO notice"]
**T3 PAYG Instalment**: $[amount]

**Note**: PAYG instalments only apply if ATO has issued an instalment notice (usually after first profitable year).

---

## BAS Summary - Amount Payable to ATO

```
GST Payable (G21):        $[amount]
PAYG Withheld (W4):       $[amount]
PAYG Instalment (T3):     $[amount]
────────────────────────────────────
TOTAL PAYABLE:            $[TOTAL]
```

**Payment Details**:
- **Due Date**: [28 days after period end]
- **Payment Method**: BPAY, Direct Debit, or via myGov
- **BPAY Biller Code**: [from ATO notice]
- **BPAY Reference**: [from ATO notice]

---

## Reconciliation Checks

### Bank Reconciliation
- [ ] All bank transactions coded
- [ ] GST amounts verified against invoices
- [ ] Contractor ABNs verified
- [ ] Input tax credits substantiated (tax invoices obtained)

### Supporting Documentation
- [ ] Sales invoices (GST-compliant)
- [ ] Purchase invoices/receipts (GST tax invoices)
- [ ] Contractor payment records with ABNs
- [ ] PAYG withholding calculations

### Common Issues to Check
- ⚠️ Contractors without ABN (47% withholding?)
- ⚠️ GST-free vs GST-inclusive coding
- ⚠️ Input tax credits without valid tax invoice
- ⚠️ Personal expenses incorrectly claimed

---

## Indigenous Business Compliance (MOKAI Specific)

### Supply Nation Reporting
- [ ] Contract revenue tracked by client
- [ ] Indigenous subcontractor spend documented
- [ ] Community benefit activities recorded
- [ ] Annual Supply Nation submission prepared

### Government Contract Compliance
- [ ] Payment terms verified (Commonwealth 20-day rule)
- [ ] Invoice milestones aligned to contract
- [ ] Retention amounts tracked
- [ ] Contract variations documented

---

## Specialist Review Flags

⚠️ **Registered Tax Agent (TPB) Required for**:
- Final BAS lodgement (only RTA can lodge electronically)
- Complex GST issues (margin schemes, going concern, etc.)
- PAYG instalment calculations
- ATO debt/payment arrangements

⚠️ **Accountant Review Recommended for**:
- First BAS after GST registration
- Large GST refund claims (>$10K)
- Unusual transactions or adjustments
- Contractor vs employee classification

---

## Next Steps

### Immediate Actions
1. **Review this BAS summary** for accuracy
2. **Verify all transactions** are coded correctly
3. **Obtain missing documentation** (tax invoices, ABNs)
4. **Send to Registered Tax Agent** for lodgement

### Before Next BAS
1. Set up contractor ABN verification process
2. Implement GST-compliant invoicing
3. Regular bank reconciliation (monthly)
4. Track PAYG withholding obligations

---

## Export for Tax Agent

**Data Export Ready**: All figures calculated and reconciled
**Format**: This markdown file
**Additional Files Needed**:
- Bank statements for period
- Sales invoices (GST-compliant)
- Purchase invoices/receipts
- Contractor payment records

**Tax Agent Checklist**:
- [ ] Review calculations
- [ ] Verify GST coding
- [ ] Check PAYG withholding compliance
- [ ] Lodge BAS via ATO portal
- [ ] Arrange payment if amount payable

---

## Disclaimer

> This BAS preparation is for review purposes only. A **Registered Tax Agent (TPB)** must lodge the BAS with the ATO. Review all figures with your tax agent before lodgement.

**Prepared for**: MOKAI PTY LTD
**Period**: [Quarter/Month Year]
**Generated**: [date/time]

---

**Saved to**: `01-areas/business/mokai/finance/bas/mokai-bas-[period]-[date].md`
```

### Step 5: Save BAS Report

Use Write tool to save:

**Path**: `01-areas/business/mokai/finance/bas/mokai-bas-[period]-[YYYY-MM-DD].md`

**Frontmatter**:
```yaml
---
date: "YYYY-MM-DD HH:MM"
type: bas-preparation
entity: MOKAI PTY LTD
period: [Q1/Q2/Q3/Q4 YYYY or Month YYYY]
lodgement_due: [date]
---
```

### Step 6: Alert for Key Issues

Check and flag:

1. **GST Registration Status**
   - If MOKAI not yet registered: "⚠️ MOKAI not GST registered - cannot claim input tax credits or charge GST"
   - If operational but not registered: "🚨 URGENT: Register for GST immediately (gov contracts)"

2. **Contractor ABN Issues**
   - Missing ABN: "⚠️ Contractor [Name] - No ABN quoted, 47% withholding required"
   - Invalid ABN: "⚠️ Verify ABN on ABN Lookup before processing"

3. **Large Refund/Payment**
   - Refund >$10K: "⚠️ Large GST refund - expect ATO verification, ensure documentation ready"
   - Payment >$20K: "⚠️ Large BAS liability - ensure cash flow available by [due date]"

4. **Missing Documentation**
   - "⚠️ [X] transactions missing tax invoices - cannot claim input tax credits without substantiation"

## Usage Examples

### Example 1: Quarterly BAS
```
/mokai-bas Q2 2025
```
→ Prepares BAS for October-December 2025

### Example 2: Monthly BAS (if registered for monthly)
```
/mokai-bas October 2025
```

### Example 3: Current Period (Default)
```
/mokai-bas
```
→ Prepares BAS for current quarter/month

---

**You are now ready to prepare MOKAI's BAS. Calculate all figures, reconcile transactions, and export for tax agent lodgement.**
