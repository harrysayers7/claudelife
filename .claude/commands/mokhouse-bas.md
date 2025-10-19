# MOK HOUSE PTY LTD - BAS Preparation Support

Prepare Business Activity Statement (BAS) for MOK HOUSE PTY LTD with GST reconciliation, PAYG calculations, and export for tax agent lodgement.

**Arguments**: $ARGUMENTS (e.g., "Q2 2025" or "October 2025" for monthly)

## Entity Details

**MOK HOUSE PTY LTD** (ABN: 38690628212)
- Music production company
- Indigenous-owned (transfer to HS Family Trust in progress)
- **GST Status**: Not registered (turnover < $75K)
- **Current Status**: Living off personal savings, no income extraction yet

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

### Step 2: Check GST Registration Status

**CRITICAL CHECK**:
```sql
SELECT
  gst_registered,
  registration_date,
  current_turnover,
  threshold_percentage
FROM gst_threshold_monitoring
WHERE entity_id = (SELECT id FROM entities WHERE name = 'MOK HOUSE PTY LTD' LIMIT 1)
  AND financial_year = 'FY2025-26';
```

**If `gst_registered = false`**:
```markdown
## ⚠️ MOK HOUSE NOT GST REGISTERED

**Current Status**: Not registered for GST (turnover < $75,000)

**Implications**:
- ❌ Cannot charge GST on invoices
- ❌ Cannot claim GST input tax credits
- ❌ BAS lodgement NOT required
- ✅ Simpler accounting (no GST reconciliation needed)

**Current Turnover**: $[amount] ([X]% of $75K threshold)

**Action Required**:
- Monitor turnover monthly
- Register for GST if approaching $75K in financial year
- Use `/accountant` to track GST threshold progress

**Next Steps**:
1. Continue monitoring turnover
2. Alert if threshold approaches (80% = $60K)
3. Voluntary registration available if clients expect GST invoices

---

**No BAS required for this period** (not GST registered)

---
```

**If `gst_registered = true`**, continue with full BAS preparation below.

### Step 3: Fetch BAS Data from Supabase (If GST Registered)

Use `mcp__supabase__execute_sql`:

#### A. GST Collected (Sales/Revenue)
```sql
SELECT
  t.transaction_number,
  t.transaction_date,
  t.description,
  t.total_amount,
  t.gst_amount,
  t.project,
  c.name AS customer_name
FROM transactions t
LEFT JOIN invoices i ON i.transaction_id = t.id
LEFT JOIN contacts c ON c.id = i.contact_id
WHERE t.entity_id = (SELECT id FROM entities WHERE name = 'MOK HOUSE PTY LTD' LIMIT 1)
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
  t.project,
  c.name AS supplier_name
FROM transactions t
LEFT JOIN invoices i ON i.transaction_id = t.id
LEFT JOIN contacts c ON c.id = i.contact_id
WHERE t.entity_id = (SELECT id FROM entities WHERE name = 'MOK HOUSE PTY LTD' LIMIT 1)
  AND t.transaction_date >= '[START_DATE]'
  AND t.transaction_date <= '[END_DATE]'
  AND t.gst_amount < 0  -- GST paid on purchases (input tax credits)
  AND t.status = 'posted'
ORDER BY t.transaction_date;
```

#### C. PAYG Withholding (Employees/Contractors)
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
LEFT JOIN contacts c ON c.id = t.contact_id
WHERE t.entity_id = (SELECT id FROM entities WHERE name = 'MOK HOUSE PTY LTD' LIMIT 1)
  AND t.transaction_date >= '[START_DATE]'
  AND t.transaction_date <= '[END_DATE]'
  AND a.account_name ILIKE '%PAYG%'  -- PAYG withholding account
  AND t.status = 'posted'
ORDER BY t.transaction_date;
```

**Note**: Currently MOK HOUSE has no employee/contractor payments (living off savings). This will apply when salary extraction begins.

### Step 4: Calculate BAS Figures (If GST Registered)

#### GST Calculations
```
G1  Total Sales (GST inclusive)           = SUM(sales total_amount)
G9  GST on Sales                          = G1 ÷ 11 (10% of total)

G10 Capital Purchases (GST inclusive)     = SUM(capital purchase total_amount)
G11 Non-Capital Purchases (GST inclusive) = SUM(expense total_amount)
G12 = G10 + G11                           (Total purchases)
G20 GST Credits                           = G12 ÷ 11 (10% of total)

G21 = G9 - G20                            (GST Payable or Refundable)
     If positive: Amount payable to ATO
     If negative: Refund from ATO
```

#### PAYG Withholding
```
W1  Total salary, wages and other payments = SUM(employee/contractor payments)
W2  Amounts withheld from W1                = SUM(PAYG withholding amounts)
W4  Total PAYG Withheld                     = W2
```

**Current Context**: MOK HOUSE not yet paying salary/contractors (living off savings), so W4 = $0.

### Step 5: Generate BAS Report

```markdown
# MOK HOUSE PTY LTD - BAS Summary
## Period: [Quarter/Month Year]
**ABN**: 38690628212
**GST Registered**: [Yes/No]
**Lodgement Due**: [28 days after period end, or N/A if not registered]
**Prepared**: [current date]

---

## GST Registration Status Check

[If not registered, show warning from Step 2 and stop here]

[If registered, continue with full BAS below]

---

## GST Calculation

### Sales (GST Collected)
| Date | Description | Customer | Project | Total (inc GST) | GST Amount |
|------|-------------|----------|---------|-----------------|------------|
[List all sales transactions by project]

**G1 Total Sales**: $[amount]
**G9 GST on Sales**: $[amount] (÷11)

### Project Breakdown
[Group sales by project for MOK HOUSE music production tracking]
| Project | Revenue (inc GST) | GST Collected |
|---------|-------------------|---------------|
| [Project 1] | $[amount] | $[amount] |
| [Project 2] | $[amount] | $[amount] |

### Purchases (GST Credits)
| Date | Description | Supplier | Total (inc GST) | GST Credit |
|------|-------------|----------|-----------------|------------|
[List all purchase transactions - music equipment, software, studio costs]

**G11 Non-Capital Purchases**: $[amount]
**G10 Capital Purchases**: $[amount] (equipment >$1K if applicable)
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

### Payments to Employees/Contractors
[Current Status: No payments yet - living off personal savings]

| Date | Payee | ABN | Payment | PAYG Withheld |
|------|-------|-----|---------|---------------|
[When salary extraction begins, list here]

**W4 Total PAYG Withheld**: $0 (no employee/contractor payments this period)

**Future Planning**:
- When profitable: Pay Harry salary (<$45K to stay in 19% bracket)
- PAYG withholding required on salary payments
- Superannuation Guarantee: 12% from 1 July 2025

---

## PAYG Instalments (Company Tax Pre-Payment)

**Current Status**: Not applicable (no ATO instalment notice yet)

**Note**: PAYG instalments apply after first profitable year when ATO issues instalment notice.

---

## BAS Summary - Amount Payable to ATO

```
GST Payable (G21):        $[amount or $0 if not registered]
PAYG Withheld (W4):       $0 (no employee payments yet)
PAYG Instalment (T3):     $0 (no ATO notice)
────────────────────────────────────
TOTAL PAYABLE:            $[TOTAL or $0]
```

**Payment Details** (if amount payable):
- **Due Date**: [28 days after period end]
- **Payment Method**: BPAY, Direct Debit, or via myGov
- **BPAY Biller Code**: [from ATO notice]
- **BPAY Reference**: [from ATO notice]

---

## Reconciliation Checks

### Bank Reconciliation
- [ ] All bank transactions coded
- [ ] GST amounts verified against invoices (if registered)
- [ ] Music project revenue tracked separately
- [ ] Equipment purchases categorized (capital vs expense)
- [ ] Input tax credits substantiated (tax invoices obtained)

### Supporting Documentation
- [ ] Sales invoices (music production services, licensing)
- [ ] Purchase invoices/receipts (studio equipment, software, APRA fees)
- [ ] Bank statements reconciled
- [ ] Project tracking aligned to invoices

### Common Music Industry Deductions to Check
- ✅ APRA/SAFIR membership fees
- ✅ Music software subscriptions (Ableton, Logic, plugins)
- ✅ Studio equipment (monitors, interfaces, controllers)
- ✅ Instrument purchases/maintenance
- ✅ Marketing and promotion costs
- ✅ Collaboration fees to other artists
- ✅ Home studio depreciation (if applicable)

### Personal vs Business Expense Alert
- ⚠️ Music equipment for personal use (not tax deductible)
- ⚠️ Personal streaming subscriptions (Spotify, etc.) - not deductible
- ⚠️ Concert tickets for personal enjoyment (not deductible)

---

## Indigenous Business Compliance (MOK HOUSE)

### Current Status
- **Indigenous Ownership**: Yes (transfer to HS Family Trust in progress)
- **Supply Nation**: Not certified (MOKAI is certified)
- **Trust Transfer**: Ensure 51% Indigenous ownership maintained via trust

### Trust Ownership Implications
- [ ] Confirm trust structure preserves Indigenous status
- [ ] Document ownership transfer for compliance
- [ ] Update business registrations if needed
- [ ] Consider Supply Nation certification for MOK HOUSE if beneficial

---

## Income Extraction Planning (Future)

### Current Strategy
- **Now**: Living off personal savings (no income extraction)
- **When Profitable**: Start salary payments
- **Target**: Keep Harry's salary <$45K (19% tax bracket)
- **Dividends**: Use when highly profitable (franked dividends via trust)

### Tax-Optimized Extraction Plan
1. **Phase 1** (First profitable months):
   - Pay minimum salary to Harry (~$45K/year = $3,750/month)
   - PAYG withholding at marginal rate
   - Super Guarantee 12%

2. **Phase 2** (Consistent profitability):
   - Maintain salary at <$45K
   - Distribute excess profit via trust (when trust owns MOK HOUSE)
   - Distribute to wife if in lower bracket
   - Maximize franking credit benefits

3. **Phase 3** (High profitability):
   - Consider dividend strategy
   - Optimize trust distributions annually
   - Use `/accountant --mode=tax-planning` for scenarios

---

## Specialist Review Flags

⚠️ **Registered Tax Agent (TPB) Required for**:
- BAS lodgement (only RTA can lodge)
- GST registration when threshold approached
- Trust ownership transfer tax implications
- PAYG calculations when salary extraction begins

⚠️ **Accountant Review Recommended for**:
- First BAS after GST registration (if registered)
- Trust structure optimization (transfer in progress)
- Music industry specific deductions
- Capital vs expense equipment classification

---

## Next Steps

### Immediate Actions (If Not GST Registered)
1. ✅ Monitor turnover using `/accountant` GST threshold tracking
2. ✅ Continue current simplified accounting (no GST)
3. ✅ Alert if approaching 80% of $75K threshold
4. ✅ Prepare for GST registration when required

### Immediate Actions (If GST Registered)
1. **Review this BAS summary** for accuracy
2. **Verify all transactions** are coded correctly
3. **Obtain missing documentation** (tax invoices, receipts)
4. **Send to Registered Tax Agent** for lodgement

### Before Next BAS
1. Continue bank reconciliation monthly
2. Track music projects separately for revenue analysis
3. Document equipment purchases (capital vs expense)
4. Plan salary extraction timing (when profitable)

---

## Export for Tax Agent

**Data Export Ready**: All figures calculated (if GST registered)
**Format**: This markdown file
**Additional Files Needed**:
- Bank statements for period
- Sales invoices (music production services)
- Purchase invoices (equipment, software, studio costs)
- APRA/SAFIR income statements

**Tax Agent Checklist**:
- [ ] Review GST registration status
- [ ] Verify music industry deductions
- [ ] Check capital equipment classification
- [ ] Lodge BAS if registered (or confirm exemption)
- [ ] Arrange payment if amount payable

---

## GST Threshold Alert

**Current Turnover (FY2025-26)**: $[amount]
**Threshold Progress**: [X]% of $75,000

[If >80%, show urgent registration warning]
[If 60-80%, show monitoring alert]
[If <60%, show continue tracking message]

---

## Disclaimer

> This BAS preparation is for review purposes only. A **Registered Tax Agent (TPB)** must lodge the BAS with the ATO (if GST registered). Review all figures with your tax agent before lodgement.

**Prepared for**: MOK HOUSE PTY LTD
**Period**: [Quarter/Month Year]
**Generated**: [date/time]

---

**Saved to**: `01-areas/business/mokhouse/finance/bas/mokhouse-bas-[period]-[date].md`
```

### Step 6: Save BAS Report

Use Write tool to save:

**Path**: `01-areas/business/mokhouse/finance/bas/mokhouse-bas-[period]-[YYYY-MM-DD].md`

**Frontmatter**:
```yaml
---
date: "YYYY-MM-DD HH:MM"
type: bas-preparation
entity: MOK HOUSE PTY LTD
period: [Q1/Q2/Q3/Q4 YYYY or Month YYYY]
gst_registered: [true/false]
lodgement_due: [date or N/A]
---
```

### Step 7: Alert for Key Issues

Check and flag:

1. **GST Registration Status** (Most Important)
   - If not registered: "✅ BAS not required - continue monitoring turnover with `/accountant`"
   - If approaching threshold: "⚠️ Approaching $75K - plan GST registration"
   - If registered: Proceed with full BAS

2. **Personal Savings Runway**
   - Check burn rate: "⚠️ Personal savings runway: [X] months at current burn rate"
   - Recommend salary extraction timing: "💡 Start salary extraction when monthly profit >$4K"

3. **Music Industry Deductions**
   - "✅ APRA/SAFIR fees deductible"
   - "✅ Studio equipment deductible (if business use)"
   - "⚠️ Personal music consumption not deductible"

4. **Trust Transfer Impact**
   - "⚠️ Trust ownership transfer in progress - confirm tax implications with RTA"
   - "✅ Preserve Indigenous ownership status (51% threshold)"

## Usage Examples

### Example 1: Quarterly BAS (If Registered)
```
/mokhouse-bas Q2 2025
```
→ Prepares BAS for October-December 2025 OR shows "not registered" message

### Example 2: Monthly BAS
```
/mokhouse-bas October 2025
```

### Example 3: Current Period (Default)
```
/mokhouse-bas
```
→ Checks GST status first, then prepares BAS if registered

### Example 4: GST Status Check
```
/mokhouse-bas status
```
→ Shows GST registration status and threshold progress

---

**You are now ready to prepare MOK HOUSE's BAS. First check GST registration status, then calculate figures if registered, or provide monitoring guidance if not registered.**
