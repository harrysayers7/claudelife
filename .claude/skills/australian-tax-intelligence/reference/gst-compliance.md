# GST Compliance & BAS Guide

**Based on**: A New Tax System (Goods and Services Tax) Act 1999
**Last Updated**: October 2025

## GST Overview

### What is GST?
- **Rate**: 10% of the sale price
- **Purpose**: Tax on consumption of goods and services
- **Collection**: Businesses collect GST on behalf of the ATO
- **Refund mechanism**: Input Tax Credits (ITC) for business purchases

### Who Must Register?
- **Mandatory registration**: Turnover ≥$75,000 per year
- **Voluntary registration**: Can register below threshold if beneficial
- **Non-profit threshold**: ≥$150,000 per year

---

## Registration Requirements

### Turnover Calculation

**Turnover includes**:
- Sales of goods and services (excluding GST)
- GST-free sales (exports, some food, health, education)
- Exempt supplies are NOT included

**Turnover does NOT include**:
- Input-taxed sales (residential rent, financial supplies)
- Sales of capital assets (unless regular business activity)
- Amounts not for payment (gifts, donations)

**Time period**: Rolling 12-month period
- Look back: Previous 12 months
- Look forward: Next 12 months (projected)

**Example** (MOK HOUSE monthly tracking):
```
Month         Income    Cumulative    % of Threshold
───────────────────────────────────────────────────────
January       $1,200    $1,200        1.6%
February      $800      $2,000        2.7%
March         $2,500    $4,500        6.0%
...
October       $1,800    $14,000       18.7%  ← Current
November      (proj)    $15,800       21.1%
December      (proj)    $17,600       23.5%

Alert threshold: $52,500 (70% of $75K)
Registration required: $75,000
```

### When to Register

**Mandatory timeline**:
- Within **21 days** of exceeding $75,000 threshold
- Effective from the date turnover exceeded threshold (not registration date)

**Voluntary registration**:
- Can register anytime (even $0 turnover)
- Useful if:
  - Making B2B sales (clients expect tax invoices)
  - High business expenses (claim ITCs immediately)
  - Exporting goods/services (GST-free sales, claim ITCs)

**Strategic registration** (MOK HOUSE example):
- Current turnover: $14,000 (19% of threshold)
- Recommendation: Register at 70% ($52,500) to avoid rushing
- Benefit: Time to update invoices, accounting systems, marketing materials

### How to Register

**Online** (recommended):
1. Log into Business Portal (business.gov.au)
2. Select "Register for GST"
3. Provide ABN, business details
4. Choose BAS frequency (monthly, quarterly, annually)
5. Receive GST registration confirmation

**Processing time**: Usually instant to 2 business days

**What changes after registration**:
- ✅ Add GST to invoices (10% on top of prices)
- ✅ Issue tax invoices (not just invoices)
- ✅ Claim input tax credits on business purchases
- ✅ Lodge Business Activity Statements (BAS)
- ✅ Update website/marketing to include "ABN: XX XXX XXX XXX (GST registered)"

---

## Harry's Entity GST Status

### Harrison Robert Sayers (Sole Trader)
- **ABN**: 89 184 087 850
- **Income**: ~$35,000/year (APRA royalties)
- **Registered**: No
- **Reason**: Below $75K threshold, APRA royalties not subject to GST
- **Action**: No registration needed (APRA pays directly, no invoicing)

### MOK HOUSE PTY LTD
- **ABN**: 38 690 628 212
- **Income**: ~$14,000/year (19% of threshold)
- **Registered**: No (as of October 2025)
- **Projected growth**: Monitor monthly, register at 70% ($52,500)
- **Alert system**: Supabase financial dashboard tracks monthly
- **Action required**: Proactive registration when approaching threshold

### SAFIA Unit Trust
- **ABN**: [To be confirmed]
- **Income**: Variable ($30K-$100K/year depending on touring)
- **Registered**: Yes ✅
- **Reason**: Turnover exceeds $75K, issues tax invoices to venues/promoters
- **BAS lodged by**: Band accountant (quarterly)

### MOKAI PTY LTD
- **ABN**: [To be confirmed]
- **Income**: $0 (not yet operational)
- **Registered**: Not yet
- **Action required**: Register **before first government invoice**
- **Reason**: Government contracts require GST invoicing (B2G)
- **Timeline**: Register during setup phase (voluntary registration)

---

## Tax Invoices vs Invoices

### Tax Invoice Requirements

**Must include** (for sales ≥$82.50 including GST):
1. The words "Tax Invoice" prominently displayed
2. Seller's identity (business name)
3. Seller's ABN
4. Date of issue
5. Brief description of items sold
6. GST amount (if any) OR statement "Total price includes GST"
7. Buyer's identity (if total ≥$1,000)

**Example** (MOK HOUSE tax invoice):
```
──────────────────────────────────────────
           TAX INVOICE

MOK HOUSE PTY LTD
ABN: 38 690 628 212

Invoice #: MH-2025-042
Date: 15 October 2025

To: Advertising Agency Pty Ltd
    ABN: 12 345 678 901

──────────────────────────────────────────
Music Production - Nando's Commercial
Sound Design & Mixing              $4,545.45
GST (10%)                            $454.55
──────────────────────────────────────────
TOTAL (inc GST)                    $5,000.00
──────────────────────────────────────────

Payment terms: Net 30 days
BSB: 123-456  Account: 12345678
──────────────────────────────────────────
```

### Recipient Created Tax Invoices (RCTI)

**Used when**: Buyer creates the tax invoice (not seller)
- Common in government procurement, large corporate buyers
- Requires written agreement between parties
- Both parties must be GST registered
- Buyer takes responsibility for GST reporting

**Relevance to MOKAI**: Government agencies may issue RCTIs for services

---

## Business Activity Statement (BAS)

### What is BAS?

- **Purpose**: Report and pay GST, PAYG withholding, other taxes
- **Frequency**: Monthly, quarterly, or annually (depends on turnover)
- **Due dates**: 28 days after end of period (or lodgment due date)

### BAS Frequency Options

**Monthly** (if turnover >$20M or opted in):
- Due: 21st of following month (if lodging electronically)
- Example: January BAS due 21 February

**Quarterly** (most small businesses):
- Due: 28 days after quarter end
- Q1 (Jul-Sep): Due 28 October
- Q2 (Oct-Dec): Due 28 January
- Q3 (Jan-Mar): Due 28 April
- Q4 (Apr-Jun): Due 28 July

**Annual** (if turnover <$20M, GST turnover <$75K, and meet other criteria):
- Due: Same as annual tax return
- Not common (quarterly is standard)

**Recommendation for Harry's entities**:
- MOK HOUSE: Quarterly (when registered)
- MOKAI: Quarterly (government contracts usually quarterly)
- SAFIA: Quarterly (current arrangement)

### What to Report on BAS

**For GST-registered businesses**:

**G1**: Total sales (including GST)
**1A**: GST on sales (G1 ÷ 11)
**G2**: Export sales (GST-free)
**G3**: Other GST-free sales
**G10**: Capital purchases (>$1,000 inc GST)
**G11**: Non-capital purchases (inc GST)
**1B**: GST credits claimed (G10 + G11) ÷ 11
**1C**: Adjustments (if any)
**1D**: **GST payable or refund** (1A - 1B + 1C)

**Example** (MOK HOUSE quarterly BAS):
```
──────────────────────────────────────────
       BAS - Quarter 1 (Jul-Sep 2025)
──────────────────────────────────────────
G1  Total sales (inc GST)         $16,500
1A  GST on sales                   $1,500  ← G1 ÷ 11

G10 Capital purchases                  $0
G11 Non-capital purchases         $3,300
1B  GST credits                      $300  ← (G10+G11) ÷ 11

1D  GST payable                    $1,200  ← 1A - 1B
──────────────────────────────────────────
Amount due: $1,200
Due date: 28 October 2025
──────────────────────────────────────────
```

### PAYG Withholding (if applicable)

**W1**: Total salary/wages paid
**W2**: Tax withheld from salaries
**W3**: Other amounts withheld
**4**: **Total PAYG withheld** (W2 + W3)

**Relevance**:
- MOK HOUSE: No employees currently (only Harry as director)
- MOKAI: May have employees in future (compliance staff, admin)
- **Contractors with ABN**: No PAYG withholding required

### How to Lodge BAS

**Options**:
1. **Business Portal** (business.gov.au) - Free, manual entry
2. **Tax agent** - Recommended for complex situations (~$300-$500/quarter)
3. **Accounting software** (Xero, MYOB, QuickBooks) - Auto-calculate, e-lodge

**Recommendation for Harry**:
- Use accounting software (Xero) connected to UpBank
- Auto-categorize GST on income/expenses
- One-click BAS lodgment
- Reduced errors, saves time

---

## Input Tax Credits (ITCs)

### What are ITCs?

- **Purpose**: Claim back GST paid on business purchases
- **Rate**: 10% of purchase price (if GST was charged)
- **Timing**: Claim in BAS for period when purchase made

### ITC Requirements

**All of the following must be true**:
1. ✅ You are GST registered
2. ✅ Purchase is for a **creditable purpose** (business use, not private)
3. ✅ GST was charged on the purchase (supplier was GST registered)
4. ✅ You have a **tax invoice** (if purchase ≥$82.50 inc GST)

**Example** (MOK HOUSE claims):
```
Purchase: Audio interface (Focusrite Scarlett)
Price: $500 + $50 GST = $550 total
Paid to: Music store (GST registered)
Business use: 100% (music production for clients)
Tax invoice: Yes ✅

ITC claimable: $50

Quarterly BAS:
- G11 (purchases): $550
- 1B (GST credits): $550 ÷ 11 = $50
```

### Partial ITCs (Mixed Use)

**If asset used partly for business, partly private**:
- Claim ITC only on business use %
- Same % as used for income tax deduction

**Example** (Tesla - 50% business use):
```
Purchase: Tesla service ($500 + $50 GST)
Business use: 50%
ITC claimable: $50 × 50% = $25

Report on BAS:
- G11: $275 (50% of $550)
- 1B: $25 (GST credit)
```

**Note**: Adjust ITC if business use % changes over time

### Common ITC Scenarios

| Purchase | GST Charged? | Creditable? | ITC? |
|----------|--------------|-------------|------|
| **Musical instrument** (for client work) | ✅ Yes | ✅ Yes | ✅ $$ |
| **Gym membership** (personal) | ✅ Yes | ❌ No | ❌ $0 |
| **Tesla service** (50% business) | ✅ Yes | ⚠️ Partial | ⚠️ 50% |
| **Exported services** (overseas client) | ❌ No (GST-free) | N/A | ❌ $0 |
| **Bank fees** (input-taxed) | ❌ No | N/A | ❌ $0 |
| **Salary to employee** (not supply) | ❌ No | N/A | ❌ $0 |

---

## GST-Free vs Input-Taxed

### GST-Free Supplies (0% GST)

**No GST charged, but ITC claimable**:
- Exports of goods and services
- Basic food (bread, milk, meat - not restaurant meals)
- Most health services (GP, dentist)
- Most education courses
- Some childcare

**Relevance to Harry**:
- MOKAI: Services to overseas clients (if any) are GST-free exports
- Can claim ITCs on expenses even though no GST charged on sales

### Input-Taxed Supplies

**No GST charged, no ITC claimable**:
- Financial supplies (bank fees, loan interest)
- Residential rent (not commercial)
- Sale of residential premises (as ongoing concern)

**Relevance to Harry**:
- Tesla loan interest: Input-taxed (no ITC)
- Bank account fees: Input-taxed (no ITC)
- Cannot claim GST credits on these even if GST-registered

---

## GST Adjustments

### When Adjustments Required

**Increasing adjustments** (owe more GST):
- Bad debts recovered (previously written off)
- Private use of business asset (adjustment for ITC claimed)
- Sale of business asset (balancing adjustment)

**Decreasing adjustments** (reduce GST owed):
- Bad debts written off (genuine attempt to recover)
- Change in creditable purpose (business use % increased)

**Example** (MOK HOUSE bad debt):
```
Invoice issued: $5,000 + $500 GST = $5,500
Reported GST: $500 (on original BAS)
Client never paid: Debt written off after 12 months

Adjustment (decreasing):
- 1C: -$500 (reduce GST payable)
- Net effect: Claim back $500 GST
```

---

## Penalties & Compliance

### Late Lodgment

**Penalty**: Failure to Lodge (FTL) penalty
- **1 entity**: 1 penalty unit per 28 days (or part thereof) late
- **Penalty unit**: $313 (2024-25, indexed annually)
- **Maximum**: 5 penalty units ($1,565)

**Example** (MOK HOUSE late BAS):
```
Due date: 28 October 2025
Lodged: 15 November 2025 (18 days late)

Penalty: 1 penalty unit × 1 entity = $313
```

**Mitigation**: Request remission if first offense or reasonable excuse

### Late Payment

**Penalty**: General Interest Charge (GIC)
- **Rate**: ~9-10% per annum (varies quarterly)
- **Calculated daily**: On outstanding amount
- **Compounds**: Interest on interest

**Example** (MOK HOUSE late payment):
```
BAS amount: $1,200
Due date: 28 October 2025
Paid: 28 November 2025 (31 days late)

GIC: $1,200 × 9% × (31/365) = $9.18
```

### Avoiding Penalties

✅ **Best practices**:
- Lodge on time (even if can't pay - request payment plan)
- Set calendar reminders (21 days before due date)
- Use accounting software with auto-reminders
- Engage tax agent (extended lodgment deadlines)
- Maintain accurate records (tax invoices, receipts)

---

## Record Keeping Requirements

### What to Keep

**Tax invoices**:
- All purchases ≥$82.50 (inc GST)
- Sales ≥$82.50 (copies of invoices issued)

**Other records**:
- Bank statements
- Cash register tapes/point-of-sale reports
- Credit card statements
- Receipt books
- Invoices for purchases <$82.50 (if claiming ITC)

### How Long to Keep

**Minimum**: 5 years from date of:
- BAS lodgment (for GST records)
- Transaction (for other records)

**Format**: Paper or electronic (must be accessible)

**Example** (MOK HOUSE):
```
BAS lodged: 28 October 2025 (Q1 FY2025-26)
Records keep until: 28 October 2030

If destroyed early: Lose right to claim ITCs/defend audit
```

---

## Special Situations

### Changing from Cash to Accrual Accounting

**Cash basis** (when receive payment):
- Report GST when you receive payment
- Claim ITCs when you pay

**Accrual basis** (when invoice issued):
- Report GST when you issue invoice
- Claim ITCs when you receive tax invoice

**Who uses cash basis**:
- Turnover <$10M (optional)
- Simpler for small businesses

**Who must use accrual**:
- Turnover ≥$10M (mandatory)

**Recommendation for Harry**: Cash basis for all entities (simpler)

### GST on Imports

**Goods imported into Australia**:
- GST payable on imports ≥$1,000
- Paid to Australian Border Force (not supplier)
- Can claim ITC on next BAS (if creditable purpose)

**Relevance**: If MOK HOUSE imports audio equipment, GST paid at border

### Margin Scheme (Property)

**Not relevant to Harry** (no property development)

---

## Quick Decision Trees

### Should I Register for GST?

```
Is turnover ≥$75,000? ─── YES ──→ Must register within 21 days
        │
        NO
        ↓
Do I want to claim ITCs? ─── YES ──→ Consider voluntary registration
        │
        NO
        ↓
Are clients expecting tax invoices? ─── YES ──→ Consider voluntary registration
        │
        NO
        ↓
Don't register (but monitor turnover monthly)
```

### Can I Claim an ITC?

```
Am I GST registered? ─── NO ──→ Cannot claim ITC
        │
       YES
        ↓
Was GST charged? ─── NO ──→ Cannot claim ITC
        │
       YES
        ↓
Is it for business use? ─── NO ──→ Cannot claim ITC
        │
       YES
        ↓
Do I have a tax invoice? ─── NO ──→ Cannot claim (if ≥$82.50)
        │
       YES
        ↓
Claim ITC on BAS (business use % only)
```

---

## Harry-Specific GST Strategy

### Current State (October 2025)

| Entity | Turnover | GST Status | Action |
|--------|----------|------------|--------|
| **Harrison (Sole Trader)** | $35K | Not registered | ✅ No action needed |
| **MOK HOUSE** | $14K (19%) | Not registered | ⚠️ Monitor monthly, alert at $52.5K |
| **SAFIA Trust** | Variable | ✅ Registered | ✅ BAS lodged quarterly |
| **MOKAI** | $0 (setup) | Not registered | ⚠️ Register before first invoice |

### Monitoring System

**Supabase Financial Dashboard**:
- Track MOK HOUSE monthly income
- Calculate % of $75K threshold
- Alert at 70% ($52,500)
- Forecast turnover (rolling 12 months)

**Alert triggers**:
1. 🟡 **50% threshold** ($37,500): Review growth trend
2. 🟠 **70% threshold** ($52,500): Prepare for registration
3. 🔴 **90% threshold** ($67,500): Register immediately

### Registration Checklist (MOK HOUSE)

When approaching $52,500 turnover:
- [ ] Register for GST via Business Portal
- [ ] Choose quarterly BAS frequency
- [ ] Update invoice templates (add "Tax Invoice", GST line)
- [ ] Update website ("ABN: 38 690 628 212 (GST registered)")
- [ ] Set up accounting software (Xero) for BAS automation
- [ ] Configure UpBank categorization (GST on income/expenses)
- [ ] Set calendar reminders (BAS due dates)
- [ ] Notify existing clients (prices now include GST)

### MOKAI GST Registration (Before First Invoice)

**Why register voluntarily**:
- Government clients expect tax invoices
- Can claim ITCs on setup costs immediately
- Professional appearance (B2G contracting)

**Setup checklist**:
- [ ] Obtain ABN (if not already)
- [ ] Register for GST
- [ ] Design tax invoice template
- [ ] Set up BAS lodgment system
- [ ] Coordinate with Marlon (co-owner)

---

**Always consult registered tax agent for GST registration and BAS lodgment.**
**ATO resources**: [ato.gov.au/business/gst](https://www.ato.gov.au/business/gst)
