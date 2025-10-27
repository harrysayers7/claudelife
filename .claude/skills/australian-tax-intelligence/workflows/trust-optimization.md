# Trust Distribution Optimization Workflow

**Purpose**: Calculate optimal trust income distributions to minimize Harry's household tax burden while maximizing cash flow and franking credit utilization.

---

## Overview

### Trust Structure (Planned)

```
┌──────────────────────────────────────┐
│      HS Family Trust (Proposed)      │
│  Discretionary Family Trust          │
│  Trustee: MOK HOUSE PTY LTD          │
└──────────────┬───────────────────────┘
               │
       ┌───────┴────────┬──────────────┬────────────────┐
       │                │              │                │
┌──────▼──────┐  ┌─────▼─────┐  ┌────▼─────┐   ┌─────▼────┐
│   Harrison   │  │ Harrison's│  │ Future   │   │  Other   │
│   Sayers     │  │   Wife    │  │ Children │   │  Family  │
│ Beneficiary  │  │Beneficiary│  │          │   │          │
└──────────────┘  └───────────┘  └──────────┘   └──────────┘
```

### Trust Tax Rules

**Key principle**: Trust income must be fully distributed by 30 June each year

- ✅ **Distributed income**: Taxed at beneficiary's marginal rate
- ❌ **Undistributed income**: Taxed at 45% (trust rate) ⚠️ **MUST AVOID**
- ✅ **Franking credits**: Flow through to beneficiaries (refundable if rate <25%)

### Optimization Goal

**Minimize household tax** by:
1. Distributing income to lowest marginal rate beneficiaries first
2. Utilizing franking credits (25% company tax already paid)
3. Keeping beneficiaries in target tax brackets (19% if possible)
4. Avoiding trust accumulation (45% tax)

---

## STEP 1: Gather Input Data

### Income Sources

**MOK HOUSE PTY LTD → HS Family Trust**:
- **Dividends from MOK HOUSE** (with 25% franking credits)
- Example: $10,000 dividend = $7,500 cash + $2,500 franking credit

**SAFIA Unit Trust → Harrison** (Not via HS Family Trust):
- **Band income distribution** (already determined by SAFIA Trust)
- Harry receives 1/3 share directly
- Taxed at Harrison's marginal rate

**MOKAI PTY LTD** (Future):
- **Dividends to shareholders** (Harrison + Marlon)
- May distribute via HS Family Trust if owned by trust

### Trust Income Available for Distribution

**Example** (FY2025-26):
```
MOK HOUSE dividend: $10,000 cash
Franking credit (25%): $2,500
Gross distribution: $12,500

Available for distribution: $12,500
Cash to distribute: $10,000
```

### Beneficiary Tax Positions

**Collect current income for each beneficiary**:

| Beneficiary | Other Income | Tax Bracket | Marginal Rate |
|-------------|--------------|-------------|---------------|
| **Harrison** | $35K (APRA) + $10K (SAFIA) = $45K | At limit (19%) | 19% |
| **Wife** | $48K (employment) | 32.5% bracket | 32.5% |
| **Future child** | $0 | Tax-free threshold | 0% |
| **Other family** | Varies | Unknown | TBD |

**Note**: These are **pre-trust distribution** incomes

---

## STEP 2: Calculate Optimal Distribution

### Distribution Strategy

**Goal**: Keep beneficiaries in lowest tax brackets possible

**Priority order**:
1. **Tax-free beneficiaries** (0% rate): Future children, low-income family
2. **19% bracket beneficiaries** (<$45K): Harrison (if room left), wife (if brought down)
3. **32.5% bracket beneficiaries** ($45K-$135K): Wife (if already over $45K)
4. **Avoid 37%+ brackets**: Only if necessary for cash flow

### Calculation Method

**For each beneficiary**:
```
1. Determine current income (before trust distribution)
2. Calculate remaining capacity in current tax bracket
3. Calculate tax on trust distribution at marginal rate
4. Calculate benefit of franking credits (if applicable)
5. Calculate net tax vs retaining in company (25%)
```

**Example** (Harrison - currently $45K, at 19% limit):

```
Harrison's current income: $45,000 (APRA $35K + SAFIA $10K)
Remaining 19% capacity: $0 (at limit)

Trust distribution: $12,500 gross ($10K cash + $2.5K franking)

Tax calculation:
  Grossed-up income: $45,000 + $12,500 = $57,500
  Tax payable (on $57,500):
    $0-$18,200: $0
    $18,201-$45,000: $5,092
    $45,001-$57,500: ($57,500 - $45,000) × 32.5% = $4,063
    Subtotal: $9,155

  Less franking credit: -$2,500
  Net tax: $6,655

Tax on distribution: $9,155 - $5,092 (tax on $45K) = $4,063
Less franking credit: -$2,500
Harrison pays: $1,563 additional tax

Effective tax rate on distribution: $1,563 / $10,000 cash = 15.63%
```

**Alternative** (Wife - currently $48K, in 32.5% bracket):

```
Wife's current income: $48,000 (employment)
Already in 32.5% bracket

Trust distribution: $12,500 gross ($10K cash + $2.5K franking)

Tax calculation:
  Grossed-up income: $48,000 + $12,500 = $60,500
  Tax payable (on $60,500):
    $0-$18,200: $0
    $18,201-$45,000: $5,092
    $45,001-$60,500: ($60,500 - $45,000) × 32.5% = $5,038
    Subtotal: $10,130

  Less franking credit: -$2,500
  Net tax: $7,630

Tax on distribution: $10,130 - $7,252 (tax on $48K) = $2,878
Less franking credit: -$2,500
Wife pays: $378 additional tax

Effective tax rate on distribution: $378 / $10,000 cash = 3.78%
```

**Comparison**:
- Distribute to Harrison: 15.63% effective tax
- Distribute to Wife: 3.78% effective tax
- **Optimal**: Distribute to Wife ✅

**Why?** Franking credits ($2,500) offset most of the 32.5% tax

---

## STEP 3: Model Distribution Scenarios

### Scenario 1: All to Harrison (Simple, but suboptimal)

**Assumption**: Distribute $10,000 cash to Harrison

```
Harrison's income: $45K + $12.5K gross = $57.5K
Tax: $9,155
Less franking credit: -$2,500
Net tax: $6,655

Household tax (Harrison + Wife):
  Harrison: $6,655
  Wife: $7,252 (unchanged)
  Total: $13,907
```

### Scenario 2: All to Wife (Better utilization of franking credits)

**Assumption**: Distribute $10,000 cash to Wife

```
Wife's income: $48K + $12.5K gross = $60.5K
Tax: $10,130
Less franking credit: -$2,500
Net tax: $7,630

Household tax (Harrison + Wife):
  Harrison: $5,092 (unchanged)
  Wife: $7,630
  Total: $12,722

Savings vs Scenario 1: $13,907 - $12,722 = $1,185
```

### Scenario 3: Split Distribution (Optimize both brackets)

**Assumption**: Distribute strategically to fill Harrison's 19% bracket first

```
Harrison currently: $45,000 (at 19% limit)
Wife currently: $48,000 (in 32.5% bracket)

Available to distribute: $12,500 gross

Option A: Give Harrison $0, Wife $12,500 (Scenario 2)
  Household tax: $12,722 ✅

Option B: Give Harrison small amount to stay under $45K (not possible - already at limit)
  Not applicable

Option C: Split based on cash needs
  Harrison: $5,000 cash ($6,250 gross with franking)
  Wife: $5,000 cash ($6,250 gross with franking)

  Harrison's tax:
    Income: $45K + $6.25K = $51.25K
    Tax: $7,123
    Less franking: -$1,250
    Net: $5,873 (additional $781)

  Wife's tax:
    Income: $48K + $6.25K = $54.25K
    Tax: $8,566
    Less franking: -$1,250
    Net: $7,316 (additional $64)

  Household tax: $5,873 + $7,316 = $13,189
  Savings vs Scenario 1: $718

  ❌ SUBOPTIMAL (worse than giving all to Wife)
```

**Conclusion**: **Scenario 2 is optimal** (all to Wife)

### Scenario 4: Future Child Beneficiary (Tax-free)

**Assumption**: When child exists, distribute to child (0% tax)

```
Child's income: $0 + $12,500 gross = $12,500
Tax: $0 (under $18,200 tax-free threshold)
Less franking credit: $2,500 refundable
Net tax: -$2,500 (refund!)

Household benefit:
  $10,000 cash distributed
  $2,500 franking credit refunded
  Total value: $12,500

Effective tax rate: -25% (refund of franking credits)
```

**Why this is optimal**:
- Child has no other income → uses tax-free threshold
- Franking credits fully refundable (child's tax rate 0% < company tax 25%)
- Household gets full value of company tax already paid

**Limitation**: Child must exist and have TFN

---

## STEP 4: Consider Cash Flow Needs

**Distribution is not just about tax** - consider:

### Cash Flow Requirements

**Harrison's needs**:
- Living expenses
- Loan repayments (Tesla)
- Business reinvestment (equipment, software)

**Wife's needs**:
- Living expenses
- Savings goals

**Question**: Who needs the cash more?

### Franking Credit Refundability

**If beneficiary's tax < franking credits**:
- Excess franking credits → refunded by ATO
- Example: Child with $0 tax gets $2,500 refund

**If beneficiary's tax > franking credits**:
- Franking credits reduce tax payable
- No refund, just offset

### Trust Deed Restrictions

**Check trust deed for**:
- Minimum/maximum distribution amounts
- Beneficiary eligibility rules
- Timing restrictions

**Most discretionary trusts**: Trustee has full discretion (no restrictions)

---

## STEP 5: Document Distribution Resolution

### Trustee Resolution Template

**Before 30 June each year**, trustee must resolve distribution:

```
HS FAMILY TRUST
TRUSTEE RESOLUTION - INCOME DISTRIBUTION FY2025-26

Date: 25 June 2026
Trustee: MOK HOUSE PTY LTD
Director: Harrison Robert Sayers

RESOLVED that the income of the HS Family Trust for the financial year ending
30 June 2026 be distributed as follows:

Income Available for Distribution:
  Dividend income (MOK HOUSE PTY LTD): $10,000
  Franking credits (25%): $2,500
  Total income: $12,500

Distribution:
  To [Beneficiary name]: $12,500 (100%)
  To other beneficiaries: $0

Rationale:
  [Brief explanation of tax optimization reasoning]

Cash Payment:
  Beneficiary to receive: $10,000 (cash component)
  Beneficiary to receive franking credit: $2,500 (tax return)

This resolution is made in accordance with the HS Family Trust Deed dated [date].

Signed: _______________________
        Harrison Robert Sayers
        Director, MOK HOUSE PTY LTD (Trustee)

Date: 25 June 2026
```

### Distribution Timeline

```
1 July 2025: FY2025-26 begins
  ↓
Throughout year: Trust receives income (dividends, etc.)
  ↓
May 2026: Calculate projected trust income
  ↓
June 2026: Model distribution scenarios (use this workflow)
  ↓
25 June 2026: Trustee resolution (distribute before 30 June)
  ↓
30 June 2026: FY2025-26 ends
  ↓
July 2026: Prepare distribution statements for beneficiaries
  ↓
October 2026: Lodge trust tax return + beneficiary tax returns
```

---

## Python Optimization Script

**Script**: `scripts/optimize_trust_distribution.py`

**Purpose**: Calculate optimal distribution automatically

**Usage**:
```bash
python scripts/optimize_trust_distribution.py \
  --trust-income 12500 \
  --harrison-income 45000 \
  --wife-income 48000 \
  --child-income 0 \
  --franking-rate 0.25
```

**Output**:
```
TRUST DISTRIBUTION OPTIMIZATION
─────────────────────────────────────────────────────────────

Trust Income Available:
  Cash: $10,000
  Franking credits (25%): $2,500
  Gross: $12,500

Beneficiary Tax Positions (before distribution):
  Harrison: $45,000 (19% bracket, at limit)
  Wife: $48,000 (32.5% bracket)
  Child: $0 (tax-free threshold)

SCENARIO ANALYSIS
─────────────────────────────────────────────────────────────

Scenario 1: All to Harrison
  Harrison tax: $6,655 (15.63% effective)
  Household tax: $13,907

Scenario 2: All to Wife
  Wife tax: $7,630 (3.78% effective)
  Household tax: $12,722
  Savings vs Scenario 1: $1,185 ✅

Scenario 3: All to Child
  Child tax: $0 (0% rate)
  Franking refund: $2,500
  Household benefit: $12,500
  Savings vs Scenario 1: $1,407 🏆 OPTIMAL

RECOMMENDATION
─────────────────────────────────────────────────────────────

Distribute: $12,500 gross to Child
  Cash payment: $10,000
  Franking credit: $2,500 (refundable)
  Household tax savings: $1,407
  Effective tax rate: -25% (refund)

Rationale:
  - Child has no other income ($0)
  - Utilizes tax-free threshold ($18,200 capacity)
  - Franking credits fully refundable
  - Maximum household tax efficiency
```

**Script content** (see `scripts/optimize_trust_distribution.py` for full implementation)

---

## Advanced Considerations

### Streaming Franking Credits

**If trust holds shares in company**:
- Dividends received by trust include franking credits
- Trust "streams" franking credits to specific beneficiaries
- Beneficiary must receive both income AND franking credit

**Example**:
```
MOK HOUSE pays $10K dividend to HS Family Trust
Franking: $2,500 (25%)

If trust distributes:
  $10,000 income to Wife
  $0 income to Harrison

Then franking credits flow to:
  $2,500 to Wife (attached to income)
  $0 to Harrison
```

**Cannot split**: Can't give income to one beneficiary and franking to another

### Family Trust Election (FTE)

**Relevant if**:
- Trust holds shares in company
- Company wants to prevent distribution outside "family group"

**HS Family Trust**: Should make FTE (if holds MOK HOUSE shares)

**Effect**:
- Restricts beneficiaries to "family group"
- Prevents tax-effective distributions to unrelated parties
- Required for franking credit integrity

### Child Under 18 (Minor Beneficiary)

**Special tax rates apply**:
- **Unearned income** >$416: Taxed at 66% (penalty rate)
- **Earned income**: Normal tax rates
- **Excepted income**: Normal tax rates (e.g., deceased estate)

**Trust distributions = unearned income** ⚠️

**Impact**:
```
Child receives $12,500 trust distribution

Tax calculation:
  First $416: Tax-free
  Next $1,306 ($417-$1,722): 66%
  Remaining ($1,723+): 66%

Tax: Approximately 66% of ($12,500 - $416) = $7,975

❌ NOT TAX EFFECTIVE for minors <18
```

**Solution**: Wait until child turns 18, or distribute to adult beneficiaries

---

## Integration with Graphiti & Serena

### Graphiti: Store Distribution Decisions

**After finalizing distribution**:
```javascript
mcp__graphiti__add_memory({
  name: "Trust Distribution FY2025-26",
  episode_body: "HS Family Trust distributed $12,500 gross income to [Beneficiary name] on [date]. Cash component: $10,000. Franking credit: $2,500. Household tax saved: $[amount] vs alternative scenarios. Rationale: [reason].",
  source: "message",
  group_id: "harry-financial-entities"
})
```

### Serena: Store Optimization Patterns

**Store calculation methods**:
```javascript
mcp__serena__write_memory({
  memory_name: "harry_trust_distribution_patterns",
  content: `
# Trust Distribution Optimization Patterns

## FY2025-26 Distribution Logic
- Beneficiaries: Harrison, Wife, Future Children
- Income sources: MOK HOUSE dividends (25% franked)
- Optimization goal: Minimize household tax, utilize franking credits

## Decision Tree:
1. If child exists (adult, 18+):
   → Distribute to child (0% tax, franking refund)

2. Else if Wife income < $45K:
   → Distribute to Wife (fills 19% bracket)

3. Else if Harrison income < $45K:
   → Distribute to Harrison (fills 19% bracket)

4. Else:
   → Distribute to Wife (franking credit offset at 32.5% better than Harrison)

## Calculation Formula:
Effective tax = (Tax on distribution - Franking credit) / Cash distributed
`
})
```

---

## Workflow Checklist

**Annual distribution planning (May-June each year)**:
- [ ] Calculate trust income available (cash + franking)
- [ ] Gather beneficiary income (before trust distribution)
- [ ] Model distribution scenarios (use Python script)
- [ ] Consider cash flow needs
- [ ] Check trust deed restrictions
- [ ] Draft trustee resolution
- [ ] Sign resolution before 30 June
- [ ] Store distribution decision in Graphiti
- [ ] Update Serena with any new patterns

**Before 30 June deadline**:
- [ ] **Trustee resolution signed** (legal requirement)
- [ ] Distribution recorded in trust accounts
- [ ] Beneficiaries notified (distribution statement)

**After 30 June** (tax return preparation):
- [ ] Trust tax return (by October)
- [ ] Beneficiary tax returns (include trust distribution)
- [ ] Claim franking credits (on beneficiary returns)

---

## Quick Reference: Distribution Priorities

### Priority 1: Tax-Free Beneficiaries (0% tax)
- Children (18+) with no other income
- Low-income family members
- **Benefit**: Franking credit refunds

### Priority 2: 19% Bracket Beneficiaries (<$45K)
- Harrison or Wife (if room in bracket)
- **Benefit**: Low marginal tax rate + franking offset

### Priority 3: 32.5% Bracket Beneficiaries ($45K-$135K)
- Wife (if already over $45K)
- **Benefit**: Franking offset reduces effective rate

### Avoid: Retaining in Trust
- **Trust rate**: 45% on undistributed income
- **Result**: Maximum tax, no franking benefit
- **Never retain income** - always distribute 100%

---

## Example: Year-End Distribution (FY2025-26)

**Scenario**: MOK HOUSE declares $20,000 dividend to HS Family Trust

**Step 1: Calculate gross income**:
```
Cash dividend: $20,000
Franking credit (25%): $5,000
Gross income: $25,000
```

**Step 2: Beneficiary positions** (May 2026):
```
Harrison: $45,000 (APRA $35K + SAFIA $10K) - at 19% limit
Wife: $50,000 (employment) - in 32.5% bracket
Child: Not yet born / under 18 - not eligible
```

**Step 3: Model scenarios**:
```
Scenario A: All to Harrison
  Tax: $12,155
  Less franking: -$5,000
  Net tax: $7,155
  Effective: 7.155% on $20K cash = 35.78%

Scenario B: All to Wife
  Tax: $13,382
  Less franking: -$5,000
  Net tax: $8,382
  Effective: 8.382% on $20K cash = 41.91%

Scenario C: Split (not optimal - analysis omitted)
```

**Wait!** Franking credit reduces Wife's tax more than Harrison's?

**Recalculate**:
```
Harrison:
  Current tax (on $45K): $5,092
  New tax (on $70K gross): $12,155
  Additional tax: $7,063
  Less franking: -$5,000
  Harrison pays: $2,063
  Effective rate: $2,063 / $20,000 = 10.32%

Wife:
  Current tax (on $50K): $7,717
  New tax (on $75K gross): $15,467
  Additional tax: $7,750
  Less franking: -$5,000
  Wife pays: $2,750
  Effective rate: $2,750 / $20,000 = 13.75%

Optimal: Distribute to Harrison ✅
```

**Step 4: Trustee resolution** (25 June 2026):
```
Resolved: Distribute $25,000 gross to Harrison Robert Sayers
  Cash: $20,000
  Franking: $5,000

Rationale: Lowest household tax ($2,063 additional vs $2,750)
```

**Step 5: Tax returns** (October 2026):
```
Harrison's tax return:
  Assessable income: $70,000 ($45K other + $25K trust)
  Tax: $12,155
  Franking credits: $5,000
  Net tax: $7,155
  Already withheld (PAYE on wife's salary): [amount]
  Refund/payment: [balance]
```

---

**Use this workflow annually to optimize trust distributions.**
**Always consult tax agent before finalizing distributions.**
**Trust resolutions must be signed before 30 June each year.**
